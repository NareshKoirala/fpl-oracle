"""
FPL-Oracle — FPL API Scraper
=============================
Async ingestion orchestrator for all Fantasy Premier League API endpoints.

This module owns **fetching only** — all Redis writes are delegated to
the ``db/`` writer modules (``players``, ``teams``, ``gameweeks``,
``fixtures``, ``players_history``, ``set_pieces``).

Endpoints:
  1. ``/api/bootstrap-static/``       → bootstrap ingest
  2. ``/api/fixtures/``               → fixtures ingest
  3. ``/api/element-summary/{id}/``   → player history ingest
  4. ``/api/team/set-piece-notes/``   → set-piece ingest
"""

import asyncio
import time
from datetime import datetime, timezone

from service.oracle.config.settings import (
    FIXTURES as FIXTURES_URL,
    FPL_BOOTSTRAP,
    PLAYER_HISTORY,
    SEASON,
)
from service.oracle.db.db_redis import RedisDB
from service.oracle.db.fixtures import save_fixture, save_season_fixture_index
from service.oracle.db.gameweeks import save_gameweek, save_system_state
from service.oracle.db.players import save_player
from service.oracle.db.players_history import (
    save_player_fixture_index,
    save_player_gw,
    save_player_season,
)
from service.oracle.db.teams import save_team
from service.oracle.utils.log import Logger
from service.oracle.utils import FPLClient

LOG = Logger("FPL_Scraper", "producer")
DB = RedisDB()


# =============================================================================
# HELPERS
# =============================================================================


def _derive_season() -> str:
    """Derive the end year from the ``SEASON`` setting.

    ``'2025/2026'`` → ``'2026'``
    """
    if "/" in SEASON:
        return SEASON.split("/")[-1]
    return SEASON


# =============================================================================
# PHASE 1 — BOOTSTRAP INGEST
# =============================================================================


async def ingest_bootstrap(client: FPLClient) -> str | None:
    """Fetch ``/api/bootstrap-static/`` and delegate writes.

    Returns:
        The current season string (e.g. ``"2026"``) or ``None`` on failure.
    """
    LOG.info("========== BOOTSTRAP INGEST ==========")
    start_bootstrap = time.perf_counter()

    data = await client.fetch(FPL_BOOTSTRAP)
    if not data:
        LOG.error("Bootstrap fetch failed — aborting bootstrap ingest.")
        return None

    elements = data.get("elements", [])
    teams = data.get("teams", [])
    events = data.get("events", [])

    LOG.info(
        f"Payload: {len(elements)} players, "
        f"{len(teams)} teams, {len(events)} gameweeks"
    )

    season = _derive_season()

    # Order matters: teams first (name index), then GWs (state), then players
    start_teams = time.perf_counter()
    LOG.info(f"Inserting {len(teams)} teams...")
    for team in teams:
        await save_team(team)
    elapsed_teams = time.perf_counter() - start_teams
    LOG.info(f"FPL Team Bootstrap complete in {elapsed_teams:.3f} seconds")

    start_gws = time.perf_counter()
    LOG.info(f"Processing {len(events)} gameweeks...")
    for event in events:
        await save_gameweek(event)
    await save_system_state(events, season)
    elapsed_gws = time.perf_counter() - start_gws
    LOG.info(f"GW Bootstrap complete in {elapsed_gws:.3f} seconds")

    start_players = time.perf_counter()
    LOG.info(f"Inserting {len(elements)} players...")
    for element in elements:
        await save_player(element)

    # Season-wide player index
    all_pids = [str(e["id"]) for e in elements]
    if all_pids:
        await DB.sadd_all("index:season_players", all_pids)
        LOG.info(f"index:season_players → {len(all_pids)} players")
    elapsed_players = time.perf_counter() - start_players
    LOG.info(f"Player Bootstrap complete in {elapsed_players:.3f} seconds")

    elapsed_bootstrap = time.perf_counter() - start_bootstrap
    LOG.info(
        f"========== BOOTSTRAP INGEST COMPLETE in {elapsed_bootstrap:.3f} seconds =========="
    )
    return season


# =============================================================================
# PHASE 2 — FIXTURES INGEST
# =============================================================================


async def ingest_fixtures(client: FPLClient, season: str | None = None):
    """Fetch ``/api/fixtures/`` and delegate writes."""
    LOG.info("========== FIXTURES INGEST ==========")
    start_fixtures = time.perf_counter()

    data = await client.fetch(FIXTURES_URL)
    if not data:
        LOG.error("Fixtures fetch failed — aborting fixtures ingest.")
        return

    LOG.info(f"Payload: {len(data)} fixtures")

    fixture_ids = []
    for raw in data:
        fid = await save_fixture(raw)
        fixture_ids.append(fid)

    await save_season_fixture_index(season, fixture_ids)

    elapsed_fixtures = time.perf_counter() - start_fixtures
    LOG.info(
        f"========== FIXTURES INGEST COMPLETE "
        f"({len(data)} fixtures) in {elapsed_fixtures:.3f} seconds =========="
    )


# =============================================================================
# PHASE 3 — PLAYER HISTORY INGEST
# =============================================================================


async def _fetch_one_player(
    client: FPLClient,
    semaphore: asyncio.Semaphore,
    pid: str,
):
    """Fetch one player's summary and delegate writes."""
    async with semaphore:
        url = f"{PLAYER_HISTORY}{pid}/"
        data = await client.fetch(url)

        if not data:
            LOG.error(f"  player:{pid} — summary fetch failed, skipping.")
            return

        # Current season GW history
        history = data.get("history", [])
        fixture_ids = []

        for match in history:
            fix_id = await save_player_gw(pid, match)
            if fix_id:
                fixture_ids.append(fix_id)

        await save_player_fixture_index(pid, fixture_ids)

        # Past seasons
        history_past = data.get("history_past", [])
        for past in history_past:
            await save_player_season(pid, past)

        LOG.info(
            f"  player:{pid} → "
            f"{len(history)} GW entries, "
            f"{len(history_past)} past seasons, "
            f"{len(fixture_ids)} fixtures indexed"
        )

        # Polite delay between requests
        await asyncio.sleep(0.05)


async def ingest_player_histories(client: FPLClient):
    """Iterate all players and concurrently fetch ``/api/element-summary/{id}/``."""
    LOG.info("========== PLAYER HISTORY INGEST ==========")
    start_histories = time.perf_counter()

    # Collect all player IDs from position indexes (built in bootstrap)
    all_pids: set[str] = set()
    for pos in range(1, 5):
        members = await DB.smembers(f"index:position_players:{pos}")
        for m in members:
            pid = m.decode() if isinstance(m, bytes) else str(m)
            all_pids.add(pid)

    if not all_pids:
        LOG.error(
            "No player IDs found in position indexes — " "skipping history ingest."
        )
        return

    LOG.info(f"Fetching histories for {len(all_pids)} players " f"(concurrency=10)...")

    semaphore = asyncio.Semaphore(10)
    tasks = [
        _fetch_one_player(client, semaphore, pid) for pid in sorted(all_pids, key=int)
    ]
    await asyncio.gather(*tasks)

    elapsed_histories = time.perf_counter() - start_histories
    LOG.info(
        f"========== PLAYER HISTORY INGEST COMPLETE "
        f"({len(all_pids)} players) in {elapsed_histories:.3f} seconds =========="
    )


# =============================================================================
# ORCHESTRATOR
# =============================================================================


async def run_fpl_ingest(full: bool = True):
    """Master orchestrator for all FPL API ingestion.

    Called by ``producer.py`` as the single entry point for FPL data.
    Runs the four endpoints in dependency order:

      1. **Bootstrap** — players, teams, GWs, state, membership indexes
      2. **Fixtures**  — match data, team/season fixture indexes
      3. **Player histories** — per-GW stats, past seasons
      4. **Set-piece notes** — taker orders

    Writes ``system:state`` fields ``producer_status`` and
    ``last_producer_run`` for pipeline observability.
    """
    LOG.info("\n" + "=" * 60)
    LOG.info("FPL INGEST PIPELINE — START")
    LOG.info("=" * 60)

    start = time.perf_counter()
    timestamp = datetime.now(timezone.utc).isoformat()

    # Mark pipeline as running
    await DB.hset_one("status", "producer_status", "running")
    await DB.hset_one("status", "last_producer_run", timestamp)

    try:
        async with FPLClient() as client:
            # Phase 1: Bootstrap (players, teams, GWs, system state)
            season = await ingest_bootstrap(client)

            # Phase 2: Fixtures (depends on season from bootstrap)
            await ingest_fixtures(client, season)

            # Phase 3: Player histories (depends on position indexes)
            if full:
                await ingest_player_histories(client)
            else:
                LOG.info("Differential mode: skipping player history summary ingest.")

        # Mark success
        await DB.hset_one("status", "producer_status", "complete")

    except Exception as e:
        LOG.error(f"Pipeline failed: {type(e).__name__} — {e}")
        await DB.hset_one("status", "producer_status", "failed")
        raise

    elapsed = time.perf_counter() - start

    LOG.info("=" * 60)
    LOG.info(f"FPL INGEST PIPELINE — COMPLETE in {elapsed:.2f}s")
    LOG.info("=" * 60 + "\n")

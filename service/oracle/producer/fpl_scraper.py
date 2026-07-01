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
import random
import time
from datetime import datetime, timezone

import httpx

from service.oracle.config.settings import (
    FIXTURES as FIXTURES_URL,
    FPL_BOOTSTRAP,
    FPL_SET_PIECE_NOTES,
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
from service.oracle.db.set_pieces import build_name_to_pid, save_set_pieces
from service.oracle.db.teams import save_team
from service.oracle.utils.log import Logger

LOG = Logger("FPL_Scraper", "producer")
DB = RedisDB()


# =============================================================================
# USER-AGENT ROTATION POOL
# =============================================================================

_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) "
    "Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:126.0) "
    "Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.5 Safari/605.1.15",
]


# =============================================================================
# HTTP CLIENT WITH RETRY & BACKOFF
# =============================================================================


class FPLClient:
    """Async HTTP client with exponential backoff, retries, and UA rotation.

    Usage::

        async with FPLClient() as client:
            data = await client.fetch("https://...")
    """

    def __init__(
        self,
        max_retries: int = 5,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            follow_redirects=True,
            headers={
                "Accept": "application/json",
                "Accept-Language": "en-GB,en;q=0.9",
            },
        )
        return self

    async def __aexit__(self, *exc):
        if self._client:
            await self._client.aclose()

    async def fetch(self, url: str):
        """GET *url* and return parsed JSON, or ``None`` on failure.

        Retries on 429 (rate-limit) and 5xx responses with exponential
        backoff + random jitter.  4xx errors (except 429) are terminal.
        """
        for attempt in range(1, self.max_retries + 1):
            ua = random.choice(_USER_AGENTS)
            try:
                LOG.info(f"[Attempt {attempt}/{self.max_retries}] GET {url}")
                resp = await self._client.get(
                    url, headers={"User-Agent": ua}
                )

                if resp.status_code == 200:
                    LOG.info(f"200 OK — {url}")
                    return resp.json()

                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 5))
                    LOG.error(f"429 Rate Limited — waiting {wait}s")
                    await asyncio.sleep(wait)
                    continue

                if resp.status_code >= 500:
                    LOG.error(
                        f"{resp.status_code} Server Error — retrying"
                    )
                else:
                    LOG.error(
                        f"{resp.status_code} Client Error — {url} (no retry)"
                    )
                    return None

            except (
                httpx.ConnectError,
                httpx.ReadTimeout,
                httpx.PoolTimeout,
            ) as e:
                LOG.error(f"Connection error: {type(e).__name__} — {e}")

            except Exception as e:
                LOG.error(f"Unexpected error: {type(e).__name__} — {e}")
                return None

            # Exponential backoff with jitter
            delay = min(
                self.base_delay * (2 ** (attempt - 1)), self.max_delay
            )
            jitter = random.uniform(0, delay * 0.5)
            wait = delay + jitter
            LOG.info(f"Backing off {wait:.1f}s before retry...")
            await asyncio.sleep(wait)

        LOG.error(f"All {self.max_retries} attempts failed — {url}")
        return None


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
    LOG.info("\n========== BOOTSTRAP INGEST ==========")

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
    LOG.info(f"Inserting {len(teams)} teams...")
    for team in teams:
        await save_team(team)

    LOG.info(f"Processing {len(events)} gameweeks...")
    for event in events:
        await save_gameweek(event)
    await save_system_state(events, season)

    LOG.info(f"Inserting {len(elements)} players...")
    for element in elements:
        await save_player(element)

    # Season-wide player index
    all_pids = [str(e["id"]) for e in elements]
    if all_pids:
        await DB.sadd_all(f"index:season_players:{season}", all_pids)
        LOG.info(f"index:season_players:{season} → {len(all_pids)} players")

    LOG.info("========== BOOTSTRAP INGEST COMPLETE ==========\n")
    return season


# =============================================================================
# PHASE 2 — FIXTURES INGEST
# =============================================================================


async def ingest_fixtures(client: FPLClient, season: str | None = None):
    """Fetch ``/api/fixtures/`` and delegate writes."""
    LOG.info("\n========== FIXTURES INGEST ==========")

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

    LOG.info(
        f"========== FIXTURES INGEST COMPLETE "
        f"({len(data)} fixtures) ==========\n"
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
    LOG.info("\n========== PLAYER HISTORY INGEST ==========")

    # Collect all player IDs from position indexes (built in bootstrap)
    all_pids: set[str] = set()
    for pos in range(1, 5):
        members = await DB.smembers(f"index:position_players:{pos}")
        for m in members:
            pid = m.decode() if isinstance(m, bytes) else str(m)
            all_pids.add(pid)

    if not all_pids:
        LOG.error(
            "No player IDs found in position indexes — "
            "skipping history ingest."
        )
        return

    LOG.info(
        f"Fetching histories for {len(all_pids)} players "
        f"(concurrency=10)..."
    )

    semaphore = asyncio.Semaphore(10)
    tasks = [
        _fetch_one_player(client, semaphore, pid)
        for pid in sorted(all_pids, key=int)
    ]
    await asyncio.gather(*tasks)

    LOG.info(
        f"========== PLAYER HISTORY INGEST COMPLETE "
        f"({len(all_pids)} players) ==========\n"
    )


# =============================================================================
# PHASE 4 — SET-PIECE INGEST
# =============================================================================


async def ingest_set_pieces(client: FPLClient):
    """Fetch ``/api/team/set-piece-notes/`` and delegate parsing + writes."""
    LOG.info("\n========== SET-PIECE INGEST ==========")

    data = await client.fetch(FPL_SET_PIECE_NOTES)
    if not data:
        LOG.error("Set-piece notes fetch failed — skipping.")
        return

    # Build player name lookup (needs bootstrap data)
    name_to_pid = await build_name_to_pid()
    LOG.info(f"Name lookup built: {len(name_to_pid)} players")

    update_count = await save_set_pieces(data, name_to_pid)

    LOG.info(
        f"========== SET-PIECE INGEST COMPLETE "
        f"({update_count} updates) ==========\n"
    )


# =============================================================================
# ORCHESTRATOR
# =============================================================================


async def run_fpl_ingest():
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
            await ingest_player_histories(client)

            # Phase 4: Set-piece notes (depends on player name data)
            await ingest_set_pieces(client)

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

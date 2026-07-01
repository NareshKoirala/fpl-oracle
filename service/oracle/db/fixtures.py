"""
DB Writer — Fixtures
=====================
Writes ``fixture:{id}`` and fixture index sets from FPL ``/api/fixtures/``.
"""

from service.oracle.config.data_struct import FIXTURE
from service.oracle.db.helpers import map_fields, FIXTURE_FIELD_MAP
from service.oracle.db.db_redis import RedisDB
from service.oracle.utils.log import Logger

LOG = Logger("Fixtures_DB", "db")
DB = RedisDB()


async def save_fixture(raw_data: dict) -> str:
    """Write a single ``fixture:{id}`` hash and team fixture indexes.

    Writes:
      - ``fixture:{id}``
      - ``SADD index:team_fixtures:{home_id}``
      - ``SADD index:team_fixtures:{away_id}``

    Returns:
        The fixture ID as a string.
    """
    fid = raw_data["id"]

    fixture_data = map_fields(FIXTURE, raw_data, FIXTURE_FIELD_MAP)

    # Scores are None for unplayed matches — store as empty string
    if raw_data.get("team_h_score") is None:
        fixture_data["home_score"] = ""
    if raw_data.get("team_a_score") is None:
        fixture_data["away_score"] = ""

    await DB.hset_all(f"fixture:{fid}", fixture_data)

    # Team → fixture indexes
    home_id = raw_data.get("team_h")
    away_id = raw_data.get("team_a")
    if home_id:
        await DB.sadd_one(f"index:team_fixtures:{home_id}", str(fid))
    if away_id:
        await DB.sadd_one(f"index:team_fixtures:{away_id}", str(fid))

    return str(fid)


async def save_season_fixture_index(season: str, fixture_ids: list[str]):
    """Bulk-write ``index:season_fixtures:{year}``."""
    if season and fixture_ids:
        await DB.sadd_all(f"index:season_fixtures:{season}", fixture_ids)
        LOG.info(
            f"index:season_fixtures:{season} → {len(fixture_ids)} fixtures"
        )

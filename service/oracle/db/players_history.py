"""
DB Writer — Player History
===========================
Writes per-gameweek and past-season data from
``/api/element-summary/{id}/`` responses.
"""

from service.oracle.config.data_struct import PLAYER_GW, PLAYER_SEASON
from service.oracle.db.helpers import (
    map_fields,
    normalize_season,
    PLAYER_GW_FIELD_MAP,
)
from service.oracle.db.db_redis import RedisDB
from service.oracle.utils.log import Logger

LOG = Logger("Player_History", "db")
DB = RedisDB()


async def save_player_gw(pid: str, match_data: dict) -> str | None:
    """Write ``player:{pid}:gw:{gw}`` from one ``history[]`` entry.

    Returns:
        The fixture ID as a string, or ``None`` if the entry had no round.
    """
    gw = match_data.get("round")
    if gw is None:
        return None

    gw_data = map_fields(PLAYER_GW, match_data, PLAYER_GW_FIELD_MAP)
    await DB.hset_all(f"player:{pid}:gw:{gw}", gw_data)

    fix_id = match_data.get("fixture")
    return str(fix_id) if fix_id else None


async def save_player_season(pid: str, past_data: dict):
    """Write ``player:{pid}:season:{year}`` from one ``history_past[]`` entry."""
    season_name = past_data.get("season_name", "")
    year = normalize_season(season_name)
    if not year:
        return

    season_data = map_fields(PLAYER_SEASON, past_data)
    await DB.hset_all(f"player:{pid}:season:{year}", season_data)


async def save_player_fixture_index(pid: str, fixture_ids: list[str]):
    """Bulk-write ``index:player_fixtures:{pid}``."""
    if fixture_ids:
        await DB.sadd_all(f"index:player_fixtures:{pid}", fixture_ids)

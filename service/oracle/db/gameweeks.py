"""
DB Writer — Gameweeks
======================
Writes ``gw:{gw}`` and ``system:state`` from FPL bootstrap ``events[]``.
Also maintains backward-compat ``current_gw`` key for modules that
haven't migrated to ``system:state`` yet.
"""

from datetime import datetime, timezone

from service.oracle.config.data_struct import GW
from service.oracle.db.helpers import map_fields
from service.oracle.db.db_redis import RedisDB
from service.oracle.utils.log import Logger

LOG = Logger("Gameweeks_DB", "db")
DB = RedisDB()


async def save_gameweek(raw_data: dict):
    """Write a single ``gw:{gw}`` hash from one ``events[]`` entry."""
    gw_id = raw_data["id"]
    gw_data = map_fields(GW, raw_data)
    await DB.hset_all(f"gw:{gw_id}", gw_data)


async def save_system_state(events: list, season: str):
    """Extract current/next/last GW flags from *events* and write system status.

    Writes:
      - ``status`` — Combined pipeline state and current gameweek details.
    """
    current_gw = None
    next_gw = None
    last_gw = None

    status_data = {
        "season": season,
        "current_season": season,
        "last_fetch": datetime.now(timezone.utc).isoformat(),
    }

    for raw in events:
        gw_id = raw["id"]
        deadline = raw.get("deadline_time", "")
        date_part = deadline.split("T")[0] if deadline else ""

        if raw.get("is_current"):
            current_gw = str(gw_id)
            status_data["current"] = current_gw
            status_data["current_gw"] = current_gw
            status_data["current_in"] = date_part

        if raw.get("is_next"):
            next_gw = str(gw_id)
            status_data["next"] = next_gw
            status_data["next_in"] = date_part

        if raw.get("is_previous"):
            last_gw = str(gw_id)
            status_data["last"] = last_gw
            status_data["last_in"] = date_part

    await DB.hset_all("status", status_data)

    LOG.info(
        f"Status updated → current={current_gw}, next={next_gw}, "
        f"last={last_gw}, season={season}"
    )

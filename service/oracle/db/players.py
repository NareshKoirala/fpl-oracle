"""
DB Writer — Players
====================
Writes ``player:{id}``, ``player:{id}:meta``, and membership indexes
from a single FPL bootstrap ``elements[]`` entry.
"""

from service.oracle.config.data_struct import PLAYER, PLAYER_META
from service.oracle.db.helpers import map_fields, PLAYER_FIELD_MAP
from service.oracle.db.db_redis import RedisDB
from service.oracle.utils.log import Logger

LOG = Logger("Players_DB", "db")
DB = RedisDB()


async def save_player(raw_data: dict):
    """Process one ``elements[]`` entry into Redis.

    Writes:
      - ``player:{id}``  — core identity, pricing, season stats
      - ``player:{id}:meta`` — ownership, transfers, set-piece orders, ranks
      - ``SADD index:team_players:{tid}``
      - ``SADD index:position_players:{pos}``
    """
    pid = raw_data["id"]
    tid = raw_data.get("team", 0)
    pos = raw_data.get("element_type", 0)

    # ── player:{id} ─────────────────────────────────────────────
    player_data = map_fields(PLAYER, raw_data, PLAYER_FIELD_MAP)

    # chance_of_playing defaults to 100 when the API returns None
    if raw_data.get("chance_of_playing_this_round") is None:
        player_data["chance_of_playing"] = "100"

    # now_cost is in tenths (e.g. 85 = £8.5m)
    raw_cost = raw_data.get("now_cost")
    if raw_cost is not None:
        player_data["cost"] = str(float(raw_cost) / 10.0)

    await DB.hset_all(f"player:{pid}", player_data)

    # ── player:{id}:meta ────────────────────────────────────────
    meta_data = map_fields(PLAYER_META, raw_data)
    await DB.hset_all(f"player:{pid}:meta", meta_data)

    # ── Indexes (SET) ───────────────────────────────────────────
    await DB.sadd_one(f"index:team_players:{tid}", str(pid))
    await DB.sadd_one(f"index:position_players:{pos}", str(pid))

    LOG.info(
        f"player:{pid} ({raw_data.get('web_name', '?')}) "
        f"→ team={tid} pos={pos}"
    )

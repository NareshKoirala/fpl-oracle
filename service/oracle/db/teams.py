"""
DB Writer — Teams
==================
Writes ``team:{id}`` and the name→ID reverse index
from a single FPL bootstrap ``teams[]`` entry.
"""

from service.oracle.config.data_struct import TEAM
from service.oracle.db.helpers import map_fields
from service.oracle.db.db_redis import RedisDB
from service.oracle.utils.log import Logger

LOG = Logger("Teams_DB", "db")
DB = RedisDB()


async def save_team(raw_data: dict):
    """Process one ``teams[]`` entry into Redis.

    Writes:
      - ``team:{id}`` — core identity, FPL strength ratings
      - ``HSET index:team_name:{name} tid {id}`` — reverse lookup
    """
    tid = raw_data["id"]
    name = raw_data["name"]

    team_data = map_fields(TEAM, raw_data)
    await DB.hset_all(f"team:{tid}", team_data)

    # Reverse lookup index: team name → tid
    await DB.hset_one(f"index:team:{name}", "tid", str(tid))

    LOG.info(f"team:{tid} → {name}")

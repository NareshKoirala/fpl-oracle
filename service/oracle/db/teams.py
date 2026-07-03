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
    
    # Normalize strength ratings by dividing by 1000
    strength_fields = [
        "strength_overall_home",
        "strength_overall_away",
        "strength_attack_home",
        "strength_attack_away",
        "strength_defence_home",
        "strength_defence_away",
    ]
    for field in strength_fields:
        val = raw_data.get(field)
        if val is not None:
            team_data[field] = str(float(val) / 1000.0)

    await DB.hset_all(f"team:{tid}", team_data)

    # Reverse lookup index: team name → tid
    await DB.hset_one(f"index:team:{name}", "tid", str(tid))
    await DB.hset_one(f"index:team_name:{name}", "tid", str(tid))

    LOG.info(f"team:{tid} → {name}")

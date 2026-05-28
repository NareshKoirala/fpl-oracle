from db.db_redis import RedisDB
from utils.log import Logger
from cook.team_math.strength import cal_teams_strength
from utils.export_redis import export_db1_to_json


LOG = Logger("Team_Cook", "cook")
DB = RedisDB()


async def teams_cook():
    LOG.info("Started cal_fix_diff()")

    
    await cal_teams_strength()
    gw = await DB.hget_one(f"current_gw", "current")
    await export_db1_to_json(DB, gw, "teams_strength")


from db.db_redis import RedisDB
from utils.log import Logger
from cook.team_math.strength import cal_teams_strength


LOG = Logger("Team_Cook", "cook")
DB = RedisDB()


async def teams_cook():
    LOG.info("Started cal_fix_diff()")
    await cal_teams_strength()

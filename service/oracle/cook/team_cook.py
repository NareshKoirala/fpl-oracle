from service.oracle.utils.log import Logger
from service.oracle.db.db_redis import RedisDB
from service.oracle.cook.team_math.strength import cal_teams_strength

LOG = Logger("Team_Cook", "cook")
DB = RedisDB()


async def teams_cook():
    LOG.info("\n========== START teams_cook() ==========")

    LOG.info("Calculating team strengths...")
    await cal_teams_strength()
    LOG.info("Team strength calculation complete.")

    LOG.info("========== END teams_cook() ==========\n")

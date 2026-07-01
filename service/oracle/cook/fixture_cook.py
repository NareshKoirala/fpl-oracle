from service.oracle.utils.log import Logger
from service.oracle.db.db_redis import RedisDB

LOG = Logger("Fixture_cook", "cook")
DB = RedisDB()


async def fixture_cook(gw=None):
    pass

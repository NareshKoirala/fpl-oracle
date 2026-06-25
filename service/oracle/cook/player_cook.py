from service.oracle.utils.log import Logger
from service.oracle.db.db_redis import RedisDB

LOG = Logger("Player_Cook", "cook")
DB = RedisDB()


async def players_cook():
    pass
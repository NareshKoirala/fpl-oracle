from cook.team_cook import teams_cook
from cook.fixture_cook import fixture_cook
from utils.log import Logger
from db.db_redis import RedisDB
import asyncio


LOG = Logger("Cook", "cook")
DB = RedisDB()


async def run_cook():
    raw_data = await DB.db_size()
    while raw_data < 33000:
        raw_data = await DB.db_size()
        LOG.info(f"Currently producer fetching Raw Data: {raw_data}")
        await asyncio.sleep(10)

    LOG.info(f"Enough data to start cook - Raw Data: {raw_data}")
    LOG.info("Cook Started...")
    await teams_cook()
    await fixture_cook(38)
    LOG.info("Cooking Finished...")

from cook.team_cook import teams_cook
from cook.fixture_cook import fixture_cook
from cook.playing_cook import playing_cook

from utils.log import Logger
from db.db_redis import RedisDB

import asyncio
from datetime import datetime

from utils.export_redis import export_db1_to_json


LOG = Logger("Cook", "cook")
DB = RedisDB()


async def run_cook():
    raw_data = await DB.db_size("raw")
    while raw_data < 42000:
        raw_data = await DB.db_size("raw")
        LOG.info(f"Currently producer fetching Raw Data: {raw_data}")
        await asyncio.sleep(10)

    LOG.info(f"Enough data to start cook - Raw Data: {raw_data}")
    if await valid_gw_day():
        LOG.info("Cook Started...")
        await teams_cook()
        await fixture_cook()
        await playing_cook()
        await DB.dump_raw()  # Test process only delete this line on prod
        await export_db1_to_json(DB)
        LOG.info("Cooking Finished...")
    else:
        LOG.error("Deadline has already started")


async def valid_gw_day():
    date_gw = await DB.hget_one("current_gw", "current_in")
    today = datetime.now()
    gw = datetime.fromisoformat(date_gw)

    return (gw - today).days < 0  # for testing i put < but change it to >

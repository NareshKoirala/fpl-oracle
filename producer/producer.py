from utils.log import Logger
from producer.fpl_scraper import fpl_data_to_db
from producer.fotmob_scraper import (
    table_scrap,
    xg_scrap,
    home_table_scrap,
    away_table_scrap,
    form_table_scrap,
)
from db.db_redis import RedisDB
from db.all_fixtures import get_fixtures
from db.players_history import get_player_history
import asyncio
import time

LOG = Logger("Producer", "producer")
DB = RedisDB()


async def run_producer():
    if not await DB.db_size("raw"):
        LOG.info("Starting scrapers...")
        start = time.perf_counter()
        await fpl_data_to_db()
        await get_fixtures()
        await table_scrap()
        await xg_scrap()
        await home_table_scrap()
        await away_table_scrap()
        await form_table_scrap()
        await get_player_history()
        await DB.dump_raw()
        end = time.perf_counter()
        total = end - start
        LOG.info(f"Finished scrapers in {total:.3f} seconds")

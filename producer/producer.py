from utils.log import Logger
from producer.fpl_scraper import fpl_data_to_db
from producer.fotmob_scraper import table_scrap, xg_scrap
from db.db_redis import RedisDB
from db.all_fixtures import get_fixtures
import asyncio

LOG = Logger("Producer")
DB = RedisDB()

async def run_scrapers():
    while True:
        print(DB.db_size())
        if not DB.db_size():
            LOG.info("Starting scrapers...")
            fpl_data_to_db()
            get_fixtures()
            await table_scrap()
            await xg_scrap()
            LOG.info("Finished scrapers.")
        await asyncio.sleep(60)

from utils.log import Logger
from producer.fpl_scraper import fpl_data_to_db
from producer.fotmob_scraper import table_scrap, xg_scrap
from utils.data_to_txt import get_players_txt, get_teams_txt
from db.db_redis import RedisDB
import asyncio

LOG = Logger("Producer")
DB = RedisDB()

async def run_scrapers():
    while True:
        print(DB.db_size())
        if not DB.db_size():
            LOG.info("Starting scrapers...")
            fpl_data_to_db()
            await table_scrap()
            await xg_scrap()
            # get_players_txt()
            # get_teams_txt()
            LOG.info("Finished scrapers.")
        await asyncio.sleep(60)

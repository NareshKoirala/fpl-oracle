from utils.log import Logger
from producer.fpl_scraper import fpl_data_to_db
from producer.fotmob_scraper import table_scrap, xg_scrap
from utils.data_to_txt import get_players_txt, get_teams_txt

LOG = Logger("Producer")


async def run_scrapers():
    while True:
        if input("") == "fetch":
            LOG.info("Starting scrapers...")
            fpl_data_to_db()
            await table_scrap()
            await xg_scrap()
            # get_players_txt()
            # get_teams_txt()
        LOG.info("Finished scrapers.")

import asyncio
from utils.log import Logger
from producer.fpl_scraper import fpl_data_to_db, yahoo_data_to_db
from producer.fotmob_scraper import table_scrap, xg_scrap
from producer.epl_scraper import team_stats_scrap
from db.teams import Team

LOG = Logger("Producer")


async def run_scrapers():
    while True:
        LOG.info("Starting scrapers...")
        fpl_data_to_db()
        await table_scrap()
        await xg_scrap()
        await team_stats_scrap()
        for team in Team.teams:
            print(f"Team: {team.name}, Raw Data: {team.raw_data}")
            print()
        LOG.info("Finished scrapers.")
        LOG.info("Sleeping for 1 min...")
        await asyncio.sleep(60)

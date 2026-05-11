import asyncio
from utils.log import Logger
from producer.fpl_scraper import fpl_data_to_db, yahoo_data_to_db
from producer.fotmob_scraper import table_scrap, xg_scrap
from producer.epl_scraper import team_stats_scrap
from db.teams import Team
from db.players import Player

LOG = Logger("Producer")


async def run_scrapers():
    while True:
        LOG.info("Starting scrapers...")
        fpl_data_to_db()
        # await table_scrap()
        # await xg_scrap()
        # await team_stats_scrap()
        for team in Team.teams[:3]:
            print(
                team.tid,
                team.name,
                team.short_name,
                "\n",
                team.table,
                "\n",
                team.expected,
                "\n",
                team.strength,
                "\n",
            )
            
        for player in Player.players[:3]:
            print(
                player.id,
                player.team_code,
                player.web_name,
                player.now_cost,
                player.total_points,
                player.status,
                player.form,
                player.element_type,
                "\n",
                player.stats,
                "\n",
                player.fpl_stats,
                "\n",
                player.rank,
                "\n",
                player.expected,
                "\n",
                player.stats_per_90,
                "\n",
            )
            
        print("Waiting")
        LOG.info("Finished scrapers.")
        LOG.info("Sleeping for 1 min...")
        await asyncio.sleep(60)

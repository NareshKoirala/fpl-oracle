import asyncio
from utils.log import Logger
from producer.fpl_scraper import fpl_data_to_db, yahoo_data_to_db
from producer.fotmob_scraper import table_scrap, xg_scrap
from db.teams import Team
from db.players import Player
from utils.dataIntxt import write_data_to_txt

LOG = Logger("Producer")


async def run_scrapers():
    while True:
        if input("") == "loop":
            LOG.info("Starting scrapers...")
            fpl_data_to_db()
            await table_scrap()
            await xg_scrap()


            for team in Team.teams:
                holder = f"""
{team.tid}: {team.name} ({team.short_name})
Table:  {team.table},
Expect: {team.expected},
Streng: {team.strength},
"""
                write_data_to_txt(holder, "Teams")

            for player in Player.players:
                holder = f"""
{player.id}: {player.team_code} -> {player.web_name}
Cost:   {player.now_cost}
TPoints:{player.total_points}
Status: {player.status}
Form:   {player.form}
Element:{player.element_type}
Stats:  {player.stats}
fpl_s:  {player.fpl_stats}
Rank:   {player.rank}
Expext: {player.expected}
SP90:   {player.stats_per_90}
"""
                write_data_to_txt(holder, "Players")
        
        print("Done")
        LOG.info("Finished scrapers.")
        LOG.info("Sleeping for 1 min...")
        await asyncio.sleep(60)

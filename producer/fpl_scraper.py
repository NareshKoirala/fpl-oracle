from utils.log import Logger
from utils.scraper import Scraper
from db.teams import get_teams
from db.players import get_players
from db.gw_fixtures import get_fixtures
from config.settings import FPL_BOOTSTRAP, YAHOO_SPORTS
import asyncio

LOG = Logger("Fpl_Scraper")

async def api_fetch()-> dict:
    LOG.info("api_fetch() running.")
    
    data = await Scraper().fetch_request(FPL_BOOTSTRAP)
    
    if data:
        LOG.info("API data fetched successfully.")
        return data["teams"], data["elements"], data["events"]
    else:
        LOG.error("Failed to fetch API data.")
        return None
    

async def fpl_data_to_db():
    LOG.info("Starting fpl_data_to_db()")
    
    teams, players, fixtures = await api_fetch()

    for team in teams: await get_teams(team)
    for player in players: await get_players(player)
    for fixtures in fixtures: await get_fixtures(fixtures)
    
    LOG.info("Finished fpl_data_to_db()")

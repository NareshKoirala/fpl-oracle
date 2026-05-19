from utils.log import Logger
from utils.scraper import Scraper
from db.teams import Team
from db.players import Player
from config.settings import FPL_BOOTSTRAP, YAHOO_SPORTS

LOG = Logger("Fpl_scraper")

def api_fetch()-> dict:
    LOG.info("api_fetch() running.")
    
    data = Scraper().fetch_request(FPL_BOOTSTRAP).json()
    
    if data:
        LOG.info("API data fetched successfully.")
        return data["teams"], data["elements"], ["events"]
    else:
        LOG.error("Failed to fetch API data.")
        return None
    

def fpl_data_to_db():
    LOG.info("Starting fpl_data_to_db()")
    
    teams, players = api_fetch()
    for team in teams: Team(team)
    for player in players: Player(player)
    
    LOG.info("Finished fpl_data_to_db()")

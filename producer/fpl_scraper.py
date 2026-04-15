from utils.log import Logger
from utils.scraper import Scraper
from db.teams import Team
from utils.settings import FPL_BOOTSTRAP

LOG = Logger("Fpl_scraper")

def api_fetch()-> dict:
    
    data = Scraper(FPL_BOOTSTRAP, False).fetch_request()
    
    if data:
        LOG.info("API data fetched successfully.")
        return data["teams"], data["elements"]
    else:
        LOG.error("Failed to fetch API data.")
        return None
    

def fpl_data_to_db():
    teams, players = api_fetch()
    
    for team in teams: Team(team)

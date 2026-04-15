from utils.log import Logger
from utils.scraper import Scraper
from db.teams import Team

LOG = Logger("fpl_scraper")
URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

def api_fetch()-> dict:
    
    data = Scraper(URL, False).fetch_request()
    
    if data:
        LOG.info("API data fetched successfully.")
        return data["teams"], data["elements"]
    else:
        LOG.error("Failed to fetch API data.")
        return None
    

teams, players = api_fetch()

for team in teams:
    Team(team)


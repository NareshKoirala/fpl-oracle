from utils.log import Logger
from utils.scraper import Scraper

LOG = Logger("fpl_scraper")

def api_fetch()-> dict:
    # The 'bootstrap-static' endpoint from your MS link
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    
    data = Scraper(url).fetch_request()
    
    if data:
        LOG.info("API data fetched successfully.")
        return data
    else:
        LOG.error("Failed to fetch API data.")
        return None
    

api_fetch()

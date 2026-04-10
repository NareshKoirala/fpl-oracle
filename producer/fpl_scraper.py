import requests
from utils.log import Logger

LOG = Logger("fpl_scraper")

def api_fetch()-> dict:
    # The 'bootstrap-static' endpoint from your MS link
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    
    response = requests.get(url)
    
    if response.status_code == 200:
    
        final_data = {}
        raw_data = response.json()
        
        final_data['teams'] = raw_data['teams'][:1]
        final_data['players'] = raw_data['elements'][:1]

        return final_data
    else:
        LOG.error(f"❌ Error: {response.status_code}")
        return None


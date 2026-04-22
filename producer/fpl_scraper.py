from utils.log import Logger
from utils.scraper import Scraper
from db.teams import Team
from utils.settings import FPL_BOOTSTRAP, YAHOO_SPORTS

LOG = Logger("Fpl_scraper")

def api_fetch()-> dict:
    
    data = Scraper(FPL_BOOTSTRAP, False).fetch_request().json()
    
    if data:
        LOG.info("API data fetched successfully.")
        return data["teams"], data["elements"]
    else:
        LOG.error("Failed to fetch API data.")
        return None
    

def fpl_data_to_db():
    teams, players = api_fetch()
    
    for team in teams: Team(team)

def testing():
    data = Scraper(YAHOO_SPORTS, False).fetch_request()
    soup = Scraper.BeautifulSoup_Parse(data.text,  "html.parser")
    table_row = soup.find_all("tr")
    
    teams = []
    title = []
    
    for row in table_row:
        team = []
        for cell in row.find_all("th"):
            title.append(cell.text)
        for cell in row.find_all("td"):
            team.append(cell.text)
        teams.append(team)
        
    print(title)
    
    for t in teams:
        print(t)
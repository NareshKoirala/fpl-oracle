from utils.scraper import Scraper
from utils.log import Logger
from utils.settings import FOTMOB_PLAYER_STATS, FOTMOB_TEAM_STATS, FOTMOB_TABLE

LOG = Logger("Fotmob_scraper")


def table_scrap():
    s = Scraper(FOTMOB_TABLE, True)
    data = s.fetch_playwright(".flipmove")
    table = data.find_all("div", class_="flipmove")
    
    """
    run the loop:- for row in table[1:]:
    team name :- row.span.text
    position :- row.div.div.text
    """
    
    print(table[1].div.div.text)
    
    #for team in table[1:]:
    #    pass


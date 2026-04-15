from utils.scraper import Scraper
from utils.log import Logger
from utils.settings import FOTMOB_PLAYER_STATS, FOTMOB_TEAM_STATS, FOTMOB_TABLE

LOG = Logger("Fotmob_scraper")


def table_scrap():
    s = Scraper(FOTMOB_TABLE, True)
    data = s.fetch_playwright(".flipmove")
    table = data.find_all("div", class_="flipmove")
    
    for team in table[1:]:
        name = team.find(class_="TeamShortname").text
        div_data = [d.text.strip() for d in team.find_all("div")[1:-8] if d.text.strip()]
        LOG.info(div_data)

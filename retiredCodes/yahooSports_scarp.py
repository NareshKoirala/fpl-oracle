from config.settings import YAHOO_SPORTS
from utils.scraper import Scraper


def yahoo_data_to_db():
    LOG.info("Starting yahoo_data_to_db()")

    data = Scraper().fetch_request(YAHOO_SPORTS)
    soup = Scraper.BeautifulSoup_Parse(data.text, "html.parser")
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

    LOG.info("Finished yahoo_data_to_db()")

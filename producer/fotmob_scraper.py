from utils.scraper import Scraper
from utils.log import Logger
from utils.settings import (
    FOTMOB_PLAYER_STATS,
    FOTMOB_BASE,
    FOTMOB_TEAM_STATS,
    FOTMOB_TABLE,
    TEAM_STATS_CLASS,
    TABLE_CLASS,
)
from db.teams import Team

LOG = Logger("Fotmob_scraper")


def team_stats_scrap():
    LOG.info("Started team_stats_scrap")
    
    s = Scraper(FOTMOB_TEAM_STATS, True)
    data = s.fetch_playwright(f".{TEAM_STATS_CLASS}")
    section = data.find_all("div", class_=TEAM_STATS_CLASS)

    for box in section[1:3]:
        key = (
            box.h3.find(string=True)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
        )
        url = f"{FOTMOB_BASE}{box.a["href"]}"
        
        s1 = Scraper(url, True)
        data = s1.fetch_playwright(".e1ef5uu60")
        
        print(data.find("div", class_="e1ef5uu60"))
        
        s1.close()
        
        #for a in data:
        #    print(a)
        
        

    LOG.info("Finished team_stats_scrap")


def table_scrap():
    LOG.info("Started table_scrap()")
    
    s = Scraper(FOTMOB_TABLE, True)
    data = s.fetch_playwright(f".{TABLE_CLASS}")
    table = data.find_all("div", class_=TABLE_CLASS)
    teams = []

    for row in table[1:]:
        div_data = [d.text.strip() for d in row.find_all("div")[1:-8] if d.text.strip()]
        form = [3 if c == "W" else 1 if c == "D" else 0 for c in div_data[10]]
        team = {
            "name": row.find(class_="TeamShortname").text,
            "data": {
                "position": div_data[0],
                "played": div_data[3],
                "win": div_data[4],
                "draw": div_data[5],
                "loss": div_data[6],
                "points": div_data[9],
                "form": form,
            },
        }
        teams.append(team)

    for team in teams:
        name = team["name"]
        for key, value in team["data"].items():
            Team.update_raw_data(key, value, name)

    LOG.info("Finished table_scrap()")

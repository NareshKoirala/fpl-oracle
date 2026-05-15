from utils.scraper import Scraper
from utils.log import Logger
from config.settings import (
    FOTMOB_TABLE,
    TABLE_CLASS,
    FOTMOB_xG,
)
from db.teams import Team

LOG = Logger("Fotmob_scraper")

async def table_scrap():
    LOG.info("Started table_scrap()")

    s = Scraper()
    await s.enable_playwright()  # Ensure Playwright is enabled for this scraper instance
    await s.page_load(FOTMOB_TABLE)
    data = await s.fetch_playwright(f".{TABLE_CLASS}")
    table = data.find_all("div", class_=TABLE_CLASS)

    for row in table[1:]:
        div_data = [d.text.strip() for d in row.find_all("div")[1:-8] if d.text.strip()]
        form = ["3" if c == "W" else "1" if c == "D" else "0" for c in div_data[10]]
        name = row.find(class_="TeamShortname").text.strip()
        goal = div_data[7].split("-")

        Team.update_table("goals", goal[0], name)
        Team.update_table("conceded", goal[1], name)
        Team.update_table("position", div_data[0], name)
        Team.update_table("played", div_data[3], name)
        Team.update_table("win", div_data[4], name)
        Team.update_table("draw", div_data[5], name)
        Team.update_table("loss", div_data[6], name)
        Team.update_table("points", div_data[9], name)
        Team.update_table("form", "".join(form), name)

    await s.close_page()  # Close the Playwright page after scraping is done

    LOG.info("Finished table_scrap()")


async def xg_scrap():
    LOG.info("Started xg_scrap()")

    s = Scraper()
    await s.enable_playwright()
    await s.page_load(FOTMOB_xG)
    data = await s.fetch_playwright(f".{TABLE_CLASS}")
    table = data.find_all("div", class_=TABLE_CLASS)
    
    for row in table[1:]:
        x_data = [d.text.strip() for d in row.find_all("span")[2:] if d.text.strip()]
        name = x_data[0]
        data = [d.text.strip() for d in row.find_all("td")[-3:]]
        
        Team.update_expected("xg", data[0][:4], name)
        Team.update_expected("xga", data[1][:4], name)
        Team.update_expected("xpts", data[2][:2], name)

        Team.update_expected("xg_difference", data[0][4:] if len(data[0]) != 1 else 0.0, name)
        Team.update_expected("xga_difference", data[1][4:] if len(data[1]) != 1 else 0.0, name)
        Team.update_expected("xpts_difference", data[2][2:] if len(data[2]) != 1 else 0.0, name)

    await s.close_page()  # Close the Playwright page after scraping is done

    LOG.info("Finished xg_scrap()")

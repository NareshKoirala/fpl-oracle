from utils.scraper import Scraper
from utils.log import Logger
from config.settings import (
    FOTMOB_TABLE,
    TABLE_CLASS,
    FOTMOB_xG,
    FOTMOB_AWAY,
    FOTMOB_HOME,
    FOTMOB_FORM,
)
from db.db_redis import RedisDB

LOG = Logger("Fotmob_Scraper")
DB = RedisDB()


async def home_table_scrap():
    LOG.info("Started home_table_scrap()")

    s = Scraper()
    await s.enable_playwright()  # Ensure Playwright is enabled for this scraper instance
    await s.page_load(FOTMOB_HOME)

    await fetch_table(s, "home")

    LOG.info("Finished home_table_scrap()")


async def away_table_scrap():
    LOG.info("Started away_table_scrap()")

    s = Scraper()
    await s.enable_playwright()  # Ensure Playwright is enabled for this scraper instance
    await s.page_load(FOTMOB_AWAY)

    await fetch_table(s, "away")

    LOG.info("Finished away_table_scrap()")


async def form_table_scrap():
    LOG.info("Started form_table_scrap()")

    s = Scraper()
    await s.enable_playwright()  # Ensure Playwright is enabled for this scraper instance
    await s.page_load(FOTMOB_FORM)

    await fetch_table(s, "last_five")

    LOG.info("Finished form_table_scrap()")


async def table_scrap():
    LOG.info("Started table_scrap()")

    s = Scraper()
    await s.enable_playwright()  # Ensure Playwright is enabled for this scraper instance
    await s.page_load(FOTMOB_TABLE)

    await fetch_table(s, "table")

    LOG.info("Finished table_scrap()")


async def fetch_table(s, feild):
    data = await s.fetch_playwright(f".{TABLE_CLASS}")
    table = data.find_all("div", class_=TABLE_CLASS)

    for row in table[1:]:
        div_data = [d.text.strip() for d in row.find_all("div")[1:] if d.text.strip()]
        form = ["3" if c == "W" else "1" if c == "D" else "0" for c in div_data[10]]
        name = row.find(class_="TeamShortname").text.strip()
        goal = div_data[7].split("-")
        tid = await DB.hget_one(f"index:team:{name}", "tid")
        place_json = {
            "goals": goal[0],
            "conceded": goal[1],
            "position": div_data[0],
            "played": div_data[3],
            "win": div_data[4],
            "draw": div_data[5],
            "loss": div_data[6],
            "points": div_data[9],
            "form": "".join(form),
        }
        await DB.hset_dict(f"raw_teams:{tid}:{feild}", place_json)

    await s.close_page()  # Close the Playwright page after scraping is done


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

        tid = await DB.hget_one(f"index:team:{name}", "tid")
        place_json = {
            "xg": data[0][:4],
            "xga": data[1][:4],
            "xpts": data[2][:2],
            "xg_difference": data[0][4:] if len(data[0]) != 1 else "0.0",
            "xga_difference": data[1][4:] if len(data[1]) != 1 else "0.0",
            "xpts_difference": data[2][2:] if len(data[2]) != 1 else "0.0",
        }
        await DB.hset_dict(f"raw_teams:{tid}:expected", place_json)

    await s.close_page()  # Close the Playwright page after scraping is done

    await s.close_browser()

    LOG.info("Finished xg_scrap()")

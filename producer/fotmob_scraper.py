from utils.scraper import Scraper
from utils.log import Logger
from config.settings import (
    FOTMOB_BASE,
    FOTMOB_TEAM_STATS,
    FOTMOB_TABLE,
    TEAM_STATS_SECTION_CLASS,
    TEAM_STATS_DIV_CLASS,
    TABLE_CLASS,
    FOTMOB_xG,
)
from db.teams import Team

LOG = Logger("Fotmob_scraper")
team_stats_dic = {}


async def team_stats_links_scrap():
    LOG.info("Started team_stats_links_scrap()")

    s = Scraper()
    await s.enable_playwright()
    await s.page_load(FOTMOB_TEAM_STATS)

    for key, value in team_stats_dic.items():

        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                data = await s.fetch_playwright(
                    f".{TEAM_STATS_SECTION_CLASS}", value[0]
                )
                section = data.find("section", class_=TEAM_STATS_SECTION_CLASS)
                div = section.find_all("div", class_=TEAM_STATS_DIV_CLASS)
                team_stats_dic[key] = (value[0], div)
                print(
                    f"Stats for {key}: {div}"
                )  # Debug print to check the scraped data
                LOG.info(f"Successfully scraped stats for {key}")
                break  # Exit the retry loop on success
            except Exception as e:
                retry_count += 1
                LOG.error(
                    f"Error scraping stats for {key} (Attempt {retry_count}/{max_retries}): {e}"
                )
                if retry_count == max_retries:
                    LOG.error(
                        f"Failed to scrape stats for {key} after {max_retries} attempts."
                    )


async def team_stats_links():
    LOG.info("Started team_stats_links()")

    s = Scraper()
    await s.enable_playwright()
    await s.page_load(FOTMOB_TEAM_STATS)
    data = await s.fetch_playwright(f".{TEAM_STATS_SECTION_CLASS}")
    section = data.find("section", class_=TEAM_STATS_SECTION_CLASS)
    div = section.find_all("div", class_=TEAM_STATS_DIV_CLASS)

    for box in div:
        key = (
            box.a.h3.text.strip()
            .lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("see_all", "")
        )

        value = box.a.get("href")

        team_stats_dic[key] = (FOTMOB_BASE + value, False)

    await s.close_page()  # Close the Playwright page after scraping is done

    LOG.info("Finished team_stats_links()")


async def table_scrap():
    LOG.info("Started table_scrap()")

    s = Scraper()
    await s.enable_playwright()  # Ensure Playwright is enabled for this scraper instance
    await s.page_load(FOTMOB_TABLE)
    data = await s.fetch_playwright(f".{TABLE_CLASS}")
    table = data.find_all("div", class_=TABLE_CLASS)

    for row in table[1:]:
        div_data = [d.text.strip() for d in row.find_all("div")[1:-8] if d.text.strip()]
        form = [3 if c == "W" else 1 if c == "D" else 0 for c in div_data[10]]
        name = row.find(class_="TeamShortname").text.strip()

        Team.update_raw_data("position", div_data[0], name)
        Team.update_raw_data("played", div_data[3], name)
        Team.update_raw_data("win", div_data[4], name)
        Team.update_raw_data("draw", div_data[5], name)
        Team.update_raw_data("loss", div_data[6], name)
        Team.update_raw_data("points", div_data[9], name)
        Team.update_raw_data("form", form, name)

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
        x_diff_data = [d.text.strip() for d in row.find_all("sup") if d.text.strip()]
        name = x_data[0]
        
        Team.update_raw_data("xg", x_data[1], name)
        Team.update_raw_data("xga", x_data[2], name)
        Team.update_raw_data("xpts", x_data[3], name)
        Team.update_raw_data("xg_difference", x_diff_data[0], name)
        Team.update_raw_data("xga_difference", x_diff_data[1], name)
        Team.update_raw_data("xpts_difference", x_diff_data[2], name)

    await s.close_page()  # Close the Playwright page after scraping is done

    LOG.info("Finished xg_scrap()")

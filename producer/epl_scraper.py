from utils.log import Logger
from utils.scraper import Scraper
from db.teams import Team
import asyncio
from config.settings import EPL_STATS, EPL_SEASON, EPL_FILTER_CLASS, SLOW_MOTION
from config.data_struct import EPL_STAT_NAME_MAP, EPL_NAME_MAP

LOG = Logger("EPL_Scraper")


async def epl_stats_scrap():
    LOG.info("Started epl_stats_scrap()")

    url_dic = {}

    s = Scraper()
    await s.enable_playwright()
    await s.page_load(EPL_STATS)
    await s.click_element('button:has-text("Goals")')
    raw_data = await s.fetch_playwright(f".{EPL_FILTER_CLASS}")

    div = raw_data.find("div", class_=EPL_FILTER_CLASS)
    url_stats_lst = [key.text.lower().replace(" ", "-") for key in div.find_all("li")]

    for item in url_stats_lst:
        key = item

        if item in EPL_STAT_NAME_MAP:
            key = EPL_STAT_NAME_MAP[item]

        url = f"{EPL_STATS}{key}/{EPL_SEASON}"
        key = item.replace("-", "_")

        if key == "expected_goals":
            key = "xg"

        url_dic[key] = url

    await s.close_page()

    LOG.info("Finished epl_stats_scrap()")
    return url_dic


async def team_stats_scrap():
    LOG.info("Started team_stats_scrap()")

    url_dic = await epl_stats_scrap()
    url_lst = list(url_dic.items())

    midpoint = len(url_lst) // 6
    first_half = dict(url_lst[:midpoint])
    second_half = dict(url_lst[midpoint : 2 * midpoint])
    third_half = dict(url_lst[2 * midpoint : 3 * midpoint])
    fourth_half = dict(url_lst[3 * midpoint : 4 * midpoint])
    fifth_half = dict(url_lst[4 * midpoint : 5 * midpoint])
    sixth_half = dict(url_lst[5 * midpoint :])
    
    for run in range(0, midpoint):
        key_1 = list(first_half.keys())[run]
        key_2 = list(second_half.keys())[run]
        key_3 = list(third_half.keys())[run]
        key_4 = list(fourth_half.keys())[run]
        key_5 = list(fifth_half.keys())[run]
        key_6 = list(sixth_half.keys())[run]

        await asyncio.gather(
            scrap_url(key_1, first_half[key_1]),
            scrap_url(key_2, second_half[key_2]),
            scrap_url(key_3, third_half[key_3]),
            scrap_url(key_4, fourth_half[key_4]),
            scrap_url(key_5, fifth_half[key_5]),
            scrap_url(key_6, sixth_half[key_6]),
        )
        
        await asyncio.sleep(SLOW_MOTION)  # Sleep between batches to avoid overwhelming the server

    LOG.info("Finished team_stats_scrap()")


async def scrap_url(key, url):

    s = Scraper()
    await s.enable_playwright()

    LOG.info(f"Scraping team stats for: {key} from URL: {url}")

    await s.page_load(url)
    raw_data = await s.fetch_playwright(f".{EPL_FILTER_CLASS}")
    table = raw_data.find("table")
    tr = table.find_all("tr")[3:]

    for row in tr:
        span = [s.text for s in row.find_all("span")[1:]]
        team_name = span[0]

        if span[0] in EPL_NAME_MAP:
            team_name = EPL_NAME_MAP[span[0]]

        Team.update_raw_data(key, span[1] if len(span[1]) != 0 else 0.0, team_name)

    await s.click_element('button:has(svg use[href$="icn-chevron-right"])')
    raw_data = await s.fetch_playwright(f".{EPL_FILTER_CLASS}")
    table = raw_data.find("table")
    tr = table.find_all("tr")[3:]

    for row in tr:
        span = [s.text for s in row.find_all("span")[1:]]
        team_name = span[0]

        if span[0] in EPL_NAME_MAP:
            team_name = EPL_NAME_MAP[span[0]]

        Team.update_raw_data(key, span[1] if len(span[1]) != 0 else 0.0, team_name)

    await s.close_page()

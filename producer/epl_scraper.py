from utils.log import Logger
from utils.scraper import Scraper
from db.teams import Team
import asyncio
from config.settings import EPL_STATS, EPL_SEASON, EPL_FILTER_CLASS
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
    
    midpoint = len(url_lst) // 2
    first_half = dict(url_lst[:midpoint])
    second_half = dict(url_lst[midpoint:])

    await asyncio.gather(scrap_url(first_half), scrap_url(second_half))

    LOG.info("Finished team_stats_scrap()")


async def scrap_url(urls):

    s = Scraper()
    await s.enable_playwright()
    
    for key, url in urls.items():
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
                
            Team.update_raw_data(key, span[1], team_name)
            

        await s.click_element('button:has(svg use[href$="icn-chevron-right"])')
        raw_data = await s.fetch_playwright(f".{EPL_FILTER_CLASS}")
        table = raw_data.find("table")
        tr = table.find_all("tr")[3:]

        for row in tr:
            span = [s.text for s in row.find_all("span")[1:]]
            team_name = span[0]

            if span[0] in EPL_NAME_MAP:
                team_name = EPL_NAME_MAP[span[0]]

            Team.update_raw_data(key, span[1], team_name)

        await s.close_page()
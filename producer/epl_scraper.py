from utils.log import Logger
from utils.scraper import Scraper
from config.settings import EPL_STATS, EPL_SEASON, EPL_FILTER_CLASS
from config.data_struct import EPL_STAT_NAME_MAP,EPL_NAME_MAP

LOG = Logger("EPL_Scraper")


async def epl_stats_scrap():
    LOG.info("Started epl_stats_scrap()")

    url_dic = {}

    s = Scraper(EPL_STATS, True)
    raw_data = await s.fetch_playwright(
        f".{EPL_FILTER_CLASS}", label="Filter By: Goals "
    )
    div = raw_data.find("div", class_=EPL_FILTER_CLASS)
    url_stats_lst = [key.text.lower().replace(" ", "-") for key in div.find_all("li")]

    for item in url_stats_lst:
        key = item

        if item in EPL_STAT_NAME_MAP:
            key = EPL_STAT_NAME_MAP[item]

        url = f"{EPL_STATS}{key}/{EPL_SEASON}"
        key = item.replace("-", "_")

        if key == "expected-goals":
            key = "xg"

        url_dic[key] = url

    LOG.info("Finished epl_stats_scrap()")
    return url_dic


async def team_stats_scrap():
    LOG.info("Started team_stats_scrap()")

    url_dic = await epl_stats_scrap()

    for key, url in url_dic.items():
        
        LOG.info(f"Scraping team stats for: {key} from URL: {url}")
        
        s = Scraper(url, True)
        
        raw_data = await s.fetch_playwright(f".{EPL_FILTER_CLASS}")
        table = raw_data.find("table")
        tr = table.find_all("tr")[3:]
        
        with open(f"epl_stats/{key}.txt", "w") as f:
            f.write(f"Team Stats for {key} in EPL Season {EPL_SEASON}\n\n")
        
        for row in tr:
            span = [s.text for s in row.find_all("span")[1:]]
            team_name = span[0]
            
            if span[0] in EPL_NAME_MAP:
                team_name = EPL_NAME_MAP[span[0]]
                
            with open(f"epl_stats/{key}.txt", "a") as f:
                f.write(f"Team: {team_name}, Stat: {key}, Value: {span[1]}\n")
                
        raw_data = await s.fetch_playwright(f".{EPL_FILTER_CLASS}", click=True)
        table = raw_data.find("table")
        tr = table.find_all("tr")[3:]
        
        for row in tr:
            span = [s.text for s in row.find_all("span")[1:]]
            team_name = span[0]
            
            if span[0] in EPL_NAME_MAP:
                team_name = EPL_NAME_MAP[span[0]]
                
            with open(f"epl_stats/{key}.txt", "a") as f:
                f.write(f"Team: {team_name}, Stat: {key}, Value: {span[1]}\n")

        await s.close_page()

    LOG.info("Finished team_stats_scrap()")

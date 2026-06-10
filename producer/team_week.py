from db.db_redis import RedisDB
from config.settings import TEAM_OF_WEEK
from utils.scraper import Scraper

DB = RedisDB()


async def get_team_of_week():
    l_week = await DB.hget_one("current_gw", "last")
    c_week = await DB.hget_one("current_gw", "current")

    url = TEAM_OF_WEEK + l_week + "/"

    data = await Scraper().fetch_request(url)

    await formats(data, "l_team_of_week")

    url = TEAM_OF_WEEK + c_week + "/"

    data = await Scraper().fetch_request(url)

    await formats(data, "c_team_of_week")


async def formats(data, key):

    if len(data) <= 1:
        return

    p_data = {}

    for k, v in data.items():
        if type(v) == list:
            for d in v:
                await DB.hset_dict(
                    f"{key}:{k}:{d["position"]}",
                    {
                        "element": d["element"],
                        "points": d["points"],
                    },
                )
        else:
            await DB.hset_dict(f"{key}:{k}", v)
            p_data[k] = {}

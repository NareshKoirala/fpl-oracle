from db.db_redis import RedisDB
from utils.log import Logger
from config.data_struct import FIXTURES
from config.settings import FIXTURES as url
from utils.scraper import Scraper


LOG = Logger("All Fixtures")
DB = RedisDB()


async def get_fixtures():
    await init_fixture_indexes()
    data = await Scraper().fetch_request(url)

    if data:
        await fixture_to_db(data)
    else:
        LOG("Data couldn't be fetch, Empty data")


async def fixture_to_db(raw_data):
    place_json = {}

    for data in raw_data:
        for key in FIXTURES.copy():

            if key != "stats":
                place_json[key] = str(data[key])
            else:
                await fix_stats_to_db(key, data[key], f"raw_fixtures:{data["id"]}")

        await DB.rpush(f"index:fixtures:{data["team_h"]}:home", data["id"])
        await DB.rpush(f"index:fixtures:{data["team_a"]}:away", data["id"])

        await DB.hset_dict(f"raw_fixtures:{data["id"]}", place_json)


async def init_fixture_indexes():
    tid_keys = await DB.get_keys(f"index:team:*")
    tids = []
    for key in tid_keys:
        tids.append(await DB.hget_one(key, "tid"))

    for tid in tids:  # EPL teams 1–20
        await DB.delete(f"index:fixtures:{tid}:home")
        await DB.delete(f"index:fixtures:{tid}:away")



async def fix_stats_to_db(field, value, db):
    place_json = {}

    for data in value:
        key = data["identifier"]

        for val in data["a"]:
            await DB.hset_one(db + ":stats", f"{key}.a.{val['element']}", val["value"])

        for val in data["h"]:
            await DB.hset_one(db + ":stats", f"{key}.h.{val['element']}", val["value"])

from db.db_redis import RedisDB
from utils.log import Logger
from config.data_struct import FIXTURES
from config.settings import FIXTURES as url
from utils.scraper import Scraper


LOG = Logger("All Fixtures")
DB = RedisDB()


def get_fixtures():
    data = Scraper().fetch_request(url).json()

    if data:
        fixture_to_db(data)
    else:
        LOG("Data couldn't be fetch, Empty data")


def fixture_to_db(raw_data):
    place_json = {}

    for data in raw_data:
        for key in FIXTURES.copy():

            if key != "stats":
                place_json[key] = str(data[key])
            else:
                fix_stats_to_db(key, data[key], f"fixtures:{data["id"]}")

        DB.hset_dict(f"fixtures:{data["id"]}", place_json)


def fix_stats_to_db(field, value, db):
    place_json = {}

    for data in value:
        key = data["identifier"]

        for val in data["a"]:
            DB.hset_one(db, f"{key}.a.{val['element']}", val["value"])

        for val in data["h"]:
            DB.hset_one(db, f"{key}.h.{val['element']}", val["value"])

from utils.log import Logger
from config.data_struct import FPL_FIXTURES
from db.db_redis import RedisDB

LOG = Logger("FPL_Fixtures")
DB = RedisDB()


async def get_fixtures(raw_data):
    place_json = {}
    db = f"gw:{raw_data["id"]}"
    for key in FPL_FIXTURES.keys():
        if key == "top_element_info":
            await validate_top_element_info(db, raw_data)
        else:
            place_json[key] = str(raw_data[key])
    await DB.hset_dict(db, place_json)


async def validate_top_element_info(db, raw_data):

    if raw_data["top_element_info"] == None:
        return

    for k, v in raw_data["top_element_info"].items():
        await DB.hset_one(db, f"top_element_info.{k}", str(v))


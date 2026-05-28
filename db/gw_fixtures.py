from utils.log import Logger
from config.data_struct import FPL_FIXTURES
from db.db_redis import RedisDB
from datetime import datetime

LOG = Logger("FPL_Fixtures", "db")
DB = RedisDB()


async def get_fixtures(raw_data):
    place_json = {}
    db = f"raw_gw:{raw_data["id"]}"
    for key in FPL_FIXTURES.keys():
        if key == "top_element_info":
            await validate_top_element_info(db, raw_data)
        else:
            place_json[key] = str(raw_data[key])

    LOG.info(f"{raw_data["id"]} - C: {raw_data["is_current"]}, N: {raw_data["is_next"]}, L: {raw_data["is_previous"]}")

    if raw_data["id"] == 1:
        await DB.hset_one("current_gw", "season", f"{raw_data["deadline_time"].split('-')[0]}")

    if raw_data["is_current"]:
        date = raw_data["deadline_time"].split("T")[0]
        await DB.hset_dict(
            f"current_gw", {"current": raw_data["id"], "current_in": date}
        )

    if raw_data["is_next"]:
        date = raw_data["deadline_time"].split("T")[0]
        await DB.hset_dict(f"current_gw", {"next": raw_data["id"], "next_in": date})

    if raw_data["is_previous"]:
        date = raw_data["deadline_time"].split("T")[0]
        await DB.hset_dict(f"current_gw", {"last": raw_data["id"], "last_in": date})

    await DB.hset_dict(db, place_json)


async def validate_top_element_info(db, raw_data):

    if raw_data["top_element_info"] == None:
        return

    for k, v in raw_data["top_element_info"].items():
        await DB.hset_one(db + ":top_element_info", f"{k}", str(v))

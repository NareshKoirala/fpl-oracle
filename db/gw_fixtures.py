from db.db_redis import RedisDB
from utils.log import Logger
from config.data_struct import FPL_FIXTURES
from datetime import datetime

LOG = Logger("FPL_Fixtures", "db")
DB = RedisDB()


async def get_fixtures(raw_data):
    place_json = {}
    db = f"raw_gw:{raw_data['id']}"

    for key in FPL_FIXTURES.keys():
        if key == "top_element_info":
            await validate_top_element_info(db, raw_data)
        else:
            place_json[key] = str(raw_data[key])

    LOG.info(
        f"{raw_data['id']} - C:{raw_data['is_current']}, "
        f"N:{raw_data['is_next']}, L:{raw_data['is_previous']}"
    )

    # Set season on first fixture
    if raw_data["id"] == 1:
        season = raw_data["deadline_time"].split("-")[0]
        await DB.hset_one("current_gw", "season", season)

    # Current GW
    if raw_data["is_current"]:
        date = raw_data["deadline_time"].split("T")[0]
        await DB.hset_dict(
            "current_gw", {"current": raw_data["id"], "current_in": date}
        )

    # Next GW
    if raw_data["is_next"]:
        date = raw_data["deadline_time"].split("T")[0]
        await DB.hset_dict("current_gw", {"next": raw_data["id"], "next_in": date})

    # Last GW
    if raw_data["is_previous"]:
        date = raw_data["deadline_time"].split("T")[0]
        await DB.hset_dict("current_gw", {"last": raw_data["id"], "last_in": date})

    # Save fixture
    await DB.hset_dict(db, place_json)

    # Update last fetch timestamp
    await DB.hset_dict("current_gw", {"last_fetch": str(datetime.now())})


async def validate_top_element_info(db, raw_data):
    info = raw_data.get("top_element_info")

    if info is None:
        LOG.info(f"No top_element_info for {db}")
        return

    LOG.info(f"Saving top_element_info for {db}")

    for k, v in info.items():
        await DB.hset_one(f"{db}:top_element_info", k, str(v))

    LOG.info(f"Saved top_element_info for {db}")

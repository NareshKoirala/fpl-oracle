from config.data_struct import PLAYERS
from utils.log import Logger
from db.db_redis import RedisDB

LOG = Logger("Players_DB", "db")
DB = RedisDB()


async def get_players(raw_data):
    db = f"raw_players:{raw_data["element_type"]}:{raw_data['id']}"

    for key in PLAYERS.keys():
        await validate(db, raw_data, key)

    place_json = {
        "id": raw_data["id"],
        "name": raw_data["web_name"],
        "tid": raw_data["team"],
    }
    await DB.hset_dict(
        f'index:player:{raw_data["element_type"]}:{raw_data["id"]}', place_json
    )


async def valid_check(db, dict_copy, section, raw_data):
    for key, value in dict_copy.items():
        if key in raw_data:
            data = raw_data[key]

            if key == "chance_of_playing_this_round":
                if data == None:
                    data = 100

            if data == "" or data == None:
                data = 0

            dict_copy[key] = str(data)
            await DB.hset_one(db + f":{section}", f"{key}", dict_copy[key])

    return dict_copy


async def validate(db, raw_data, key):
    return await valid_check(db, PLAYERS[key].copy(), key, raw_data)

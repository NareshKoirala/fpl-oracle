from config.data_struct import PLAYERS
from utils.log import Logger
from db.db_redis import RedisDB

LOG = Logger("Players_DB")
DB = RedisDB()


async def get_players(raw_data):
    place_json = {}
    db = f"players:{raw_data['id']}"
    sep_lst = ["stats", "fpl_stats", "rank", "expected", "stats_per_90"]

    for key in PLAYERS.keys():
        if key in sep_lst:
            await validate(db, raw_data, key)
        else:
            place_json[key] = key

    await DB.hset_dict(db, place_json)
    place_json = {
        "id": raw_data["id"],
        "name": raw_data["web_name"],
        "tid": raw_data["team_code"],
    }
    await DB.hset_dict(f'player_name:{raw_data["id"]}', place_json)


async def valid_check(db, dict_copy, section, raw_data):

    for key, value in dict_copy.items():
        if key in raw_data:
            data = raw_data[key]
            if data == "" or data == None:
                data = 0
            dict_copy[key] = float(data) if isinstance(value, int) else data
            await DB.hset_one(db, f"{section}.{key}", dict_copy[key])

    return dict_copy


async def validate(db, raw_data, key):
    return await valid_check(db, PLAYERS[key].copy(), key, raw_data)

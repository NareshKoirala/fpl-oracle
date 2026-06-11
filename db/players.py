from config.data_struct import PLAYERS
from utils.log import Logger
from db.db_redis import RedisDB

LOG = Logger("Players_DB", "db")
DB = RedisDB()


async def get_players(raw_data):
    db = f"raw_players:{raw_data['element_type']}:{raw_data['id']}"

    LOG.info(
        f"Saving player → ID={raw_data['id']} | Name={raw_data['web_name']} | TID={raw_data['team']}"
    )

    # Validate all sections
    for key in PLAYERS.keys():
        await validate(db, raw_data, key)

    # Index player
    place_json = {
        "id": raw_data["id"],
        "name": raw_data["web_name"],
        "tid": raw_data["team"],
    }

    index_key = f"index:player:{raw_data['element_type']}:{raw_data['id']}"
    await DB.hset_dict(index_key, place_json)

    LOG.info(f"Indexed player → {index_key}")


async def valid_check(db, dict_copy, section, raw_data):
    LOG.info(f"Validating section '{section}' for player DB={db}")

    for key, value in dict_copy.items():
        if key in raw_data:
            data = raw_data[key]

            # Fix chance_of_playing_this_round
            if key == "chance_of_playing_this_round" and data is None:
                LOG.info(f"chance_of_playing_this_round missing → defaulting to 100")
                data = 100

            # Fix empty or None values
            if data == "" or data is None:
                LOG.info(f"Field '{key}' missing → defaulting to 0")
                data = 0

            dict_copy[key] = str(data)
            await DB.hset_one(f"{db}:{section}", key, dict_copy[key])

    return dict_copy


async def validate(db, raw_data, key):
    return await valid_check(db, PLAYERS[key].copy(), key, raw_data)

from service.oracle.config.data_struct import PLAYER, PLAYER_META
from service.oracle.config.data_maps import PLAYERS_KEY_MAP
from service.oracle.utils.log import Logger
from service.oracle.db.db_redis import RedisDB

LOG = Logger("Players_DB", "db")
DB = RedisDB()


async def get_players(raw_data):
    db = f"players:{raw_data['id']}"

    LOG.info(
        f"Saving player → ID={raw_data['id']} | Name={raw_data['web_name']} | TID={raw_data['team_code']}"
    )

    t_p = {}
    t_ps = {}

    for k, v in raw_data.items():

        if type(v) == list or type(v) == dict:
            v = "0"     

        if k in PLAYER or PLAYERS_KEY_MAP.get(k):
            key = PLAYERS_KEY_MAP.get(k) or k

            if key == "chance_of_playing" and v == None:
                v = 100

            if key == "cost":
                v = float(v) / 10.0

            t_p[key] = str(v or 0)

        if k in PLAYER_META:
            t_ps[k] = str(v or 0)
            

    await DB.hset_dict(db, t_p)
    await DB.hset_dict(f"{db}:meta", t_ps)

    # Index player
    index_key = f"index:position_players"

    await DB.hset_one(index_key, {raw_data['element_type']}, )

    LOG.info(f"Indexed player → {index_key}")


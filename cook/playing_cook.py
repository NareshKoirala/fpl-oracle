from utils.log import Logger
from db.db_redis import RedisDB

LOG = Logger("Playing_Cook", "cook")
DB = RedisDB()


async def fetch_pids(db, type):
    keys = await db.get_keys(f"index:player:{type}:*")
    return [await db.hget_one(key, "id") for key in keys]


async def playing_cook():
    for element_t in range(1, 5):
        pids = await fetch_pids(DB, element_t)
        await save_player(pids, element_t)


def valid(can_t, status, can_s, rm):
    return can_t and status in ["a", "d"] and not can_s and not rm


def safe_bool(value):
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        return value


async def save_player(pids, element_t):

    for pid in pids:
        data = await DB.hget_all(f"raw_players:{element_t}:{pid}:selection")
        if valid(
            safe_bool(data["can_transact"]),
            data["status"],
            safe_bool(data["can_select"]),
            safe_bool(data["removed"]),
        ):
            await DB.hset_dict(
                f"proc_player:{element_t}:{pid}",
                {"playing": data["chance_of_playing_this_round"]},
            )

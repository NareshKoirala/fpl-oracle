from utils.log import Logger

LOG = Logger("Player_Cook", "cook")


async def past_season_stats(db: RedisDB):

    await goalkeeper_cal(fetch_pids(db, 1))
    await defence_cal(fetch_pids(db, 2))
    await midfeild_cal(fetch_pids(db, 3))
    await attacker_cal(fetch_pids(db, 4))


async def fetch_pids(db, type):
    keys = await db.get_keys(f"index:player:{type}:*")
    return [await db.hget_one(key, "id") for key in keys]


async def goalkeeper_cal(pids):
    for pid in pids:
        data = a


async def defence_cal(pids):
    pass


async def midfeild_cal(pids):
    pass


async def attacker_cal(pids):
    pass

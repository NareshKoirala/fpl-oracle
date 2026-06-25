from service.oracle.utils.log import Logger
from service.oracle.db.db_redis import RedisDB

LOG = Logger("Player_Cook", "cook/player_math")
DB = RedisDB()


async def past_season_stats(db: RedisDB):
    LOG.info("\n========== START past_season_stats() ==========")

    gk_pids = await fetch_pids(db, 1)
    df_pids = await fetch_pids(db, 2)
    mf_pids = await fetch_pids(db, 3)
    fw_pids = await fetch_pids(db, 4)

    LOG.info(
        f"Goalkeepers: {len(gk_pids)}, Defenders: {len(df_pids)}, "
        f"Midfielders: {len(mf_pids)}, Attackers: {len(fw_pids)}"
    )

    await goalkeeper_cal(gk_pids)
    await defence_cal(df_pids)
    await midfeild_cal(mf_pids)
    await attacker_cal(fw_pids)

    LOG.info("========== END past_season_stats() ==========\n")


async def fetch_pids(db, type):
    keys = await db.get_keys(f"index:player:{type}:*")
    return [await db.hget_one(key, "id") for key in keys]


# ---------------------------------------------------------
# GOALKEEPER
# ---------------------------------------------------------


async def goalkeeper_cal(pids):
    LOG.info("\n--- Calculating GK past-season stats ---")

    for pid in pids:
        try:
            data = await DB.hget_all(f"raw_player_past_season:{pid}:2023/24")
            LOG.info(f"GK PID={pid} → Loaded {len(data)} fields")
            # TODO: Add your GK math here
        except Exception as e:
            LOG.error(f"Error processing GK PID={pid}: {e}")


# ---------------------------------------------------------
# DEFENDER
# ---------------------------------------------------------


async def defence_cal(pids):
    LOG.info("\n--- Calculating DEF past-season stats ---")

    for pid in pids:
        try:
            data = await DB.hget_all(f"raw_player_past_season:{pid}:2023/24")
            LOG.info(f"DEF PID={pid} → Loaded {len(data)} fields")
            # TODO: Add your DEF math here
        except Exception as e:
            LOG.error(f"Error processing DEF PID={pid}: {e}")


# ---------------------------------------------------------
# MIDFIELDER
# ---------------------------------------------------------


async def midfeild_cal(pids):
    LOG.info("\n--- Calculating MID past-season stats ---")

    for pid in pids:
        try:
            data = await DB.hget_all(f"raw_player_past_season:{pid}:2023/24")
            LOG.info(f"MID PID={pid} → Loaded {len(data)} fields")
            # TODO: Add your MID math here
        except Exception as e:
            LOG.error(f"Error processing MID PID={pid}: {e}")


# ---------------------------------------------------------
# ATTACKER
# ---------------------------------------------------------


async def attacker_cal(pids):
    LOG.info("\n--- Calculating FWD past-season stats ---")

    for pid in pids:
        try:
            data = await DB.hget_all(f"raw_player_past_season:{pid}:2023/24")
            LOG.info(f"FWD PID={pid} → Loaded {len(data)} fields")
            # TODO: Add your FWD math here
        except Exception as e:
            LOG.error(f"Error processing FWD PID={pid}: {e}")

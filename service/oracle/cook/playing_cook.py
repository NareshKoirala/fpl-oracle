from service.oracle.utils.log import Logger
from service.oracle.db.db_redis import RedisDB

LOG = Logger("Playing_Cook", "cook")
DB = RedisDB()


async def fetch_pids(db, type):
    keys = await db.get_keys(f"index:player:{type}:*")
    return [await db.hget_one(key, "id") for key in keys]


async def playing_cook():
    LOG.info("\n========== START playing_cook() ==========")

    for element_t in range(1, 5):
        LOG.info(f"\n--- Processing element type {element_t} ---")

        pids = await fetch_pids(DB, element_t)
        LOG.info(f"Found {len(pids)} players for element type {element_t}")

        await save_player(pids, element_t)

    LOG.info("\n========== END playing_cook() ==========\n")


def valid(can_t, status, can_s, rm):
    return can_t and status in ["a", "d"] and not can_s and not rm


def safe_bool(value):
    if value == "True":
        return True
    elif value == "False":
        return False
    return value


async def save_player(pids, element_t):
    saved_count = 0

    for pid in pids:
        try:
            data = await DB.hget_all(f"raw_players:{element_t}:{pid}:selection")

            if not data:
                LOG.error(f"Missing selection data for PID={pid}")
                continue

            if valid(
                safe_bool(data.get("can_transact")),
                data.get("status"),
                safe_bool(data.get("can_select")),
                safe_bool(data.get("removed")),
            ):
                await DB.hset_dict(
                    f"proc_player:{element_t}:{pid}",
                    {"playing": data["chance_of_playing_this_round"]},
                )
                saved_count += 1

        except Exception as e:
            LOG.error(f"Error processing PID={pid}: {e}")

    LOG.info(f"Saved {saved_count}/{len(pids)} players for element type {element_t}")

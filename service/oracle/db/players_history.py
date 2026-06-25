import redis.asyncio as redis
from service.oracle.utils.log import Logger
from service.oracle.config.settings import PLAYER_HISTORY
from service.oracle.db.db_redis import RedisDB
import asyncio
import httpx

LOG = Logger("Player_History", "db")
DB = RedisDB()


async def fetch_and_save(client, semaphore, pid):
    async with semaphore:
        url = PLAYER_HISTORY + f"{pid}"
        LOG.info(f"Fetching history for PID={pid}")

        try:
            response = await client.get(url)
        except Exception as e:
            LOG.error(f"Request failed for PID={pid}: {e}")
            return

        if response.status_code == 200:
            data = response.json()
            history = data["history"]
            history_past = data["history_past"]

            # Current season fixtures
            for fixture in history:
                redis_key = f"raw_player_fixtures:{pid}:{fixture['fixture']}"
                await DB.hset_dict(redis_key, fixture)

            # Past seasons
            for past in history_past:
                redis_key = f"raw_player_past_season:{pid}:{past['season_name']}"
                await DB.hset_dict(redis_key, past)

            LOG.info(
                f"Saved history for PID={pid} "
                f"(fixtures={len(history)}, past={len(history_past)})"
            )

        else:
            LOG.error(f"Status {response.status_code} for PID={pid} → {url}")

        await asyncio.sleep(0.05)


async def fetch_history(pids):
    LOG.info(f"Starting fetch for {len(pids)} players...")
    semaphore = asyncio.Semaphore(10)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [fetch_and_save(client, semaphore, pid) for pid in pids]
        await asyncio.gather(*tasks)

    LOG.info("Finished fetching all player histories.")


async def get_player_history():
    cursor = 0
    pids = []

    LOG.info("Collecting player IDs...")

    while True:
        cursor, data = await DB.scan("index:player:*", cursor=cursor)
        for key in data:
            pid = await DB.hget_one(key, "id")
            pids.append(pid)

        if cursor == 0:
            break

    LOG.info(f"Total player IDs collected: {len(pids)}")

    await fetch_history(pids)

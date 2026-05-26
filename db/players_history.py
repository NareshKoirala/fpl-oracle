from utils.log import Logger
from config.settings import PLAYER_HISTORY
from db.db_redis import RedisDB
import asyncio
import httpx

LOG = Logger("Player_History")
DB = RedisDB()


async def fetch_and_save(client, semaphore, pid):
    # This limits how many requests can be active at once
    async with semaphore:
        url = PLAYER_HISTORY + f"{pid}"
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            history = data["history"]
            history_past = data["history_past"]
            for fixture in history:
                await DB.hset_dict(
                    f"raw_player_fixtures:{pid}:{fixture["fixture"]}", fixture
                )
            for past in history_past:
                await DB.hset_dict(
                    f"raw_player_past_season:{pid}:{past["season_name"]}", past
                )
        else:
            LOG.error(f"Status: {response.status_code}, For: {url}")
        
        await asyncio.sleep(0.05)



async def fetch_history(pids):
    semaphore = asyncio.Semaphore(10)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [fetch_and_save(client, semaphore, pid) for pid in pids]
        await asyncio.gather(*tasks)


async def get_player_history():
    cursor = 0
    pids = []
    LOG.info("Started to get the pids.")
    while True:
        cursor, data = await DB.scan("index:player:*", cursor=cursor)
        for key in data:
            pids.append(await DB.hget_one(key, "id"))

        if cursor == 0:
            break
    LOG.info(f"Total pids got: {len(pids)}")
    await fetch_history(pids)

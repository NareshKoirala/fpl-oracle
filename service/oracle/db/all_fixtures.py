from db.db_redis import RedisDB
from utils.log import Logger
from config.data_struct import FIXTURES
from config.settings import FIXTURES as url
from utils.scraper import Scraper

LOG = Logger("All Fixtures", "db")
DB = RedisDB()


async def get_fixtures():
    LOG.info("\n========== START get_fixtures() ==========")

    await init_fixture_indexes()
    LOG.info("Fixture indexes cleared.")

    data = await Scraper().fetch_request(url)

    if data:
        LOG.info(f"Fetched {len(data)} fixtures from API.")
        await fixture_to_db(data)
        LOG.info("All fixtures saved to Redis.")
    else:
        LOG.error("Data couldn't be fetched — empty response.")

    LOG.info("========== END get_fixtures() ==========\n")


async def fixture_to_db(raw_data):
    LOG.info("Processing fixture data...")

    for idx, data in enumerate(raw_data, start=1):
        LOG.info(f"Processing fixture {idx}/{len(raw_data)} (ID={data['id']})")

        place_json = {}

        for key in FIXTURES.copy():
            if key != "stats":
                place_json[key] = str(data[key])
            else:
                stats_key = f"raw_fixtures:{data['id']}"
                await fix_stats_to_db(key, data[key], stats_key)

        # Index by home/away
        await DB.rpush(f"index:fixtures:{data['team_h']}:home", data["id"])
        await DB.rpush(f"index:fixtures:{data['team_a']}:away", data["id"])

        # Index by gameweek
        await DB.hset_dict(
            f"index:gw_fixture:{data['event']}",
            {data["id"]: f"{data['team_h']}:{data['team_a']}"},
        )

        # Raw fixture
        await DB.hset_dict(f"raw_fixtures:{data['id']}", place_json)

    LOG.info("Finished processing all fixtures.")


async def init_fixture_indexes():
    LOG.info("Clearing old fixture indexes...")

    tid_keys = await DB.get_keys("index:team:*")
    tids = [await DB.hget_one(key, "tid") for key in tid_keys]

    for tid in tids:
        await DB.delete(f"index:fixtures:{tid}:home")
        await DB.delete(f"index:fixtures:{tid}:away")

    LOG.info(f"Cleared fixture indexes for {len(tids)} teams.")


async def fix_stats_to_db(field, value, db):
    LOG.info(f"Saving stats for fixture key: {db}")

    for data in value:
        key = data["identifier"]

        # Away stats
        for val in data["a"]:
            stat_key = f"{key}.a.{val['element']}"
            await DB.hset_one(f"{db}:stats", stat_key, val["value"])

        # Home stats
        for val in data["h"]:
            stat_key = f"{key}.h.{val['element']}"
            await DB.hset_one(f"{db}:stats", stat_key, val["value"])

    LOG.info(f"Stats saved for fixture key: {db}")

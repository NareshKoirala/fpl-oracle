from utils.log import Logger
from producer.fpl_scraper import fpl_data_to_db
from producer.team_week import get_team_of_week
from producer.fotmob_scraper import (
    table_scrap,
    xg_scrap,
    home_table_scrap,
    away_table_scrap,
    form_table_scrap,
)
from db.db_redis import RedisDB
from db.all_fixtures import get_fixtures
from db.players_history import get_player_history
import asyncio
import time

LOG = Logger("Producer", "producer")
DB = RedisDB()


async def run_producer():
    LOG.info("\n========== START run_producer() ==========")

    # Only run if RAW DB is empty
    if not await DB.db_size("raw"):
        LOG.info("Redis RAW DB is empty → running full producer pipeline.")
        start = time.perf_counter()

        # -----------------------------
        # FPL API
        # -----------------------------
        LOG.info("\n--- Fetching FPL API Data ---")
        await fpl_data_to_db()

        # -----------------------------
        # Team of the Week
        # -----------------------------
        LOG.info("\n--- Fetching Team of the Week ---")
        await get_team_of_week()

        # -----------------------------
        # Fixtures
        # -----------------------------
        LOG.info("\n--- Fetching All Fixtures ---")
        await get_fixtures()

        # -----------------------------
        # FotMob Scrapers
        # -----------------------------
        LOG.info("\n--- Fetching FotMob Table ---")
        await table_scrap()

        LOG.info("\n--- Fetching FotMob xG Data ---")
        await xg_scrap()

        LOG.info("\n--- Fetching FotMob Home Table ---")
        await home_table_scrap()

        LOG.info("\n--- Fetching FotMob Away Table ---")
        await away_table_scrap()

        LOG.info("\n--- Fetching FotMob Form Table ---")
        await form_table_scrap()

        # -----------------------------
        # Player History
        # -----------------------------
        LOG.info("\n--- Fetching Player History ---")
        await get_player_history()

        # -----------------------------
        # Dump RAW Snapshot
        # -----------------------------
        LOG.info("\n--- Dumping RAW Redis Snapshot ---")
        await DB.dump_raw()

        end = time.perf_counter()
        total = end - start

        LOG.info(
            f"\n========== FINISHED run_producer() in {total:.3f} seconds ==========\n"
        )

    else:
        LOG.info("Redis RAW DB already populated → skipping producer run.")
        LOG.info("========== END run_producer() ==========\n")

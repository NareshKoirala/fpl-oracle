from service.oracle.utils.log import Logger
from service.oracle.producer.fpl_scraper import run_fpl_ingest
from service.oracle.producer.team_week import get_team_of_week
from service.oracle.producer.fotmob_scraper import (
    table_scrap,
    xg_scrap,
    home_table_scrap,
    away_table_scrap,
    form_table_scrap,
)
from service.oracle.db.db_redis import RedisDB
from service.oracle.utils.export_redis import export_db0
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
        # FPL API (all 4 endpoints)
        # -----------------------------
        LOG.info("\n--- FPL API Ingest (bootstrap, fixtures, history, set-pieces) ---")
        await run_fpl_ingest()

        # -----------------------------
        # Team of the Week (Dream Team API — separate endpoint)
        # -----------------------------
        LOG.info("\n--- Fetching Team of the Week ---")
        await get_team_of_week()

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
        # Set status to completed before saving the dump
        # -----------------------------
        await DB.hset_one("status", "completed", "True")

        # -----------------------------
        # Dump RAW Snapshot
        # -----------------------------
        LOG.info("\n--- Dumping RAW Redis Snapshot ---")
        await DB.dump_raw()

        # -----------------------------
        # Pretty Export DB 0
        # -----------------------------
        await export_db0()

        end = time.perf_counter()
        total = end - start

        LOG.info(
            f"\n========== FINISHED run_producer() in {total:.3f} seconds ==========\n"
        )

    else:
        LOG.info("Redis RAW DB already populated → skipping producer run.")
        await DB.hset_one("status", "completed", "True")
        LOG.info("========== END run_producer() ==========\n")

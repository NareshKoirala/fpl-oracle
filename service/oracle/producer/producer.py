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


async def run_producer(force_full: bool = False):
    LOG.info("========== START run_producer() ==========")

    db_populated = await DB.db_size("raw") > 0
    full_run = force_full or not db_populated

    if full_run:
        LOG.info(
            "Running FULL producer pipeline (bootstrap, fixtures, histories, Dream Team, FotMob)."
        )
    else:

        # TODO
        # This is for the test purpose so remove on production
        LOG.debug("Redis RAW DB already populated")
        return
        #

        LOG.info(
            "Redis RAW DB already populated → running DIFFERENTIAL refresh pipeline."
        )

    start = time.perf_counter()

    # -----------------------------
    # FPL API (all 4 endpoints)
    # -----------------------------
    LOG.info("--- FPL API Ingest (bootstrap, fixtures, history, set-pieces) ---")
    start_fpl = time.perf_counter()
    await run_fpl_ingest(full=full_run)
    elapsed_fpl = time.perf_counter() - start_fpl
    LOG.info(f"FPL API Ingest complete in {elapsed_fpl:.3f} seconds")

    # -----------------------------
    # Team of the Week (Dream Team API — separate endpoint)
    # -----------------------------
    LOG.info("--- Fetching Team of the Week ---")
    start_totw = time.perf_counter()
    await get_team_of_week()
    elapsed_totw = time.perf_counter() - start_totw
    LOG.info(f"Team of the Week fetch complete in {elapsed_totw:.3f} seconds")

    # -----------------------------
    # FotMob Scrapers
    # -----------------------------
    LOG.info("--- Fetching FotMob Table ---")
    start_table = time.perf_counter()
    await table_scrap()
    elapsed_table = time.perf_counter() - start_table
    LOG.info(f"FotMob Table fetch complete in {elapsed_table:.3f} seconds")

    LOG.info("--- Fetching FotMob xG Data ---")
    start_xg = time.perf_counter()
    await xg_scrap()
    elapsed_xg = time.perf_counter() - start_xg
    LOG.info(f"FotMob xG fetch complete in {elapsed_xg:.3f} seconds")

    LOG.info("--- Fetching FotMob Home Table ---")
    start_home = time.perf_counter()
    await home_table_scrap()
    elapsed_home = time.perf_counter() - start_home
    LOG.info(f"FotMob Home Table fetch complete in {elapsed_home:.3f} seconds")

    LOG.info("--- Fetching FotMob Away Table ---")
    start_away = time.perf_counter()
    await away_table_scrap()
    elapsed_away = time.perf_counter() - start_away
    LOG.info(f"FotMob Away Table fetch complete in {elapsed_away:.3f} seconds")

    LOG.info("--- Fetching FotMob Form Table ---")
    start_form = time.perf_counter()
    await form_table_scrap()
    elapsed_form = time.perf_counter() - start_form
    LOG.info(f"FotMob Form Table fetch complete in {elapsed_form:.3f} seconds")

    # -----------------------------
    # Set status to completed before saving the dump
    # -----------------------------
    await DB.hset_one("status", "completed", "True")

    # -----------------------------
    # Dump RAW Snapshot
    # -----------------------------
    LOG.info("--- Dumping RAW Redis Snapshot ---")
    start_dump = time.perf_counter()
    await DB.dump_raw()
    elapsed_dump = time.perf_counter() - start_dump
    LOG.info(f"Dumping RAW Redis Snapshot complete in {elapsed_dump:.3f} seconds")

    # -----------------------------
    # Pretty Export DB 0
    # -----------------------------
    LOG.info("--- Pretty Export DB 0 ---")
    start_export = time.perf_counter()
    await export_db0()
    elapsed_export = time.perf_counter() - start_export
    LOG.info(f"Pretty Export DB 0 complete in {elapsed_export:.3f} seconds")

    end = time.perf_counter()
    total = end - start

    LOG.info(f"========== FINISHED run_producer() in {total:.3f} seconds ==========")

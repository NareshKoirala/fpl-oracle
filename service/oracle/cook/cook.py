from service.oracle.cook.team_cook import teams_cook
from service.oracle.cook.fixture_cook import fixture_cook
from service.oracle.cook.playing_cook import playing_cook

from service.oracle.utils.log import Logger
from service.oracle.db.db_redis import RedisDB

import asyncio
from datetime import datetime

from service.oracle.utils.export_redis import export_db1_to_json


LOG = Logger("Cook", "cook")
DB = RedisDB()


async def run_cook():
    LOG.info("\n========== START run_cook() ==========")

    # Wait until producer finishes
    while (await DB.hget_one("status:producer", "completed")) != "True":
        LOG.info("Waiting for producer to finish...")
        await asyncio.sleep(10)

    raw_data = await DB.db_size("raw")
    LOG.info(f"Enough data to start cook → Raw Data: {raw_data}")

    # Validate GW timing
    if await valid_gw_day():
        LOG.info("Cook Started...")

        # -----------------------------
        # TEAM COOK
        # -----------------------------
        LOG.info("\n--- Running teams_cook() ---")
        await teams_cook()

        # -----------------------------
        # FIXTURE COOK
        # -----------------------------
        LOG.info("\n--- Running fixture_cook() ---")
        await fixture_cook()

        # -----------------------------
        # PLAYING COOK
        # -----------------------------
        LOG.info("\n--- Running playing_cook() ---")
        await playing_cook()

        # -----------------------------
        # RAW SNAPSHOT (TEST ONLY)
        # -----------------------------
        LOG.info("\n--- Dumping RAW snapshot (TEST MODE) ---")
        await DB.dump_raw()

        # -----------------------------
        # EXPORT JSON SNAPSHOTS
        # -----------------------------
        LOG.info("\n--- Exporting DB to JSON ---")
        await export_db1_to_json(DB)

        LOG.info("\n========== FINISHED run_cook() ==========\n")

    else:
        LOG.error("Cook aborted → Deadline has already started.")
        LOG.info("========== END run_cook() ==========\n")


async def valid_gw_day():
    date_gw = await DB.hget_one("current_gw", "current_in")
    today = datetime.now()
    gw = datetime.fromisoformat(date_gw)

    # NOTE: For testing you set < 0. Change back to > 0 for production.
    return (gw - today).days < 0

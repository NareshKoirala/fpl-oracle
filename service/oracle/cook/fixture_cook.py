from service.oracle.cook.team_cook import teams_cook
from service.oracle.cook.playing_cook import playing_cook
from service.oracle.cook.fixture_math.fixture_diff import fixture_difficulty
from service.oracle.cook.fixture_math.fixture_xg import cal_fix_xg

from service.oracle.utils.log import Logger
from service.oracle.db.db_redis import RedisDB

import asyncio
from datetime import datetime

LOG = Logger("Fixture_cook", "cook")
DB = RedisDB()


async def fixture_cook(gw=None):
    LOG.info("========== START fixture_cook() ==========")

    # Determine gameweek
    if not gw:
        gw = await DB.hget_one("status", "current")
        LOG.info(f"Using current GW → {gw}")

    # Load fixtures for this GW
    fix_dict = await DB.hget_all(f"index:gw_fixture:{gw}")
    LOG.info(f"Found {len(fix_dict)} fixtures for GW {gw}")

    # Process each fixture
    for fx_id, fix in fix_dict.items():
        try:
            h, a = fix.split(":")
            LOG.info(f"Processing fixture {fx_id}: {h} vs {a}")

            await fixture_difficulty(h, a, gw, fx_id)
            await cal_fix_xg(gw, fx_id)

            LOG.info(f"Finished fixture {fx_id}")

        except Exception as e:
            LOG.error(f"Error processing fixture {fx_id}: {e}")

    LOG.info("========== END fixture_cook() ==========")

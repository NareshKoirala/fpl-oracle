from db.db_redis import RedisDB
from utils.log import Logger
from cook.fixture_math.fixture_diff import fixture_difficulty
from cook.fixture_math.fixture_xg import cal_fix_xg


LOG = Logger("Team_Cook", "cook")
DB = RedisDB()


async def fixture_cook(gw):
    LOG.info("Started fixture_cook()")

    fix_dict = await DB.hget_all(f"index:gw_fixture:{gw}")

    for fx_id, fix in fix_dict.items():
        h, a = fix.split(":")
        await fixture_difficulty(h, a, gw, fx_id)
        await cal_fix_xg(gw, fx_id)


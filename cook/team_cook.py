from db.db_redis import RedisDB
from utils.log import Logger
from cook.team_math.strength import cal_teams_strength
from cook.team_math.fixture_diff import fixture_difficulty
from cook.team_math.fixture_xg import cal_fix_xg


LOG = Logger("Team_Cook", "cook")
DB = RedisDB()


async def team_fixture(gw):
    LOG.info(f"Started cal_fix_diff({gw})")
    fix_dict = await DB.hget_all(f"index:gw_fixture:{gw}")
    await cal_teams_strength()

    for fx_id, fix in fix_dict.items():
        h, a = fix.split(":")
        await fixture_difficulty(h, a, gw, fx_id)
        await cal_fix_xg(gw, fx_id)

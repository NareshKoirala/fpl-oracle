from utils.log import Logger
from db.db_redis import RedisDB


LOG = Logger("Fixture_xG", "cook/team_math")
DB = RedisDB()


def safe_float(v):
    try:
        return float(v)
    except:
        return 0.0


async def cal_fix_xg(gw, fx_id):
    LOG.info(f"Started cal_fix_xg(GW: {gw}, FID: {fx_id})")

    key = f"proc_fixture:{gw}:{fx_id}"

    diff_h = safe_float(await DB.hget_one(key, "diff_h"))
    diff_a = safe_float(await DB.hget_one(key, "diff_a"))

    await DB.hset_dict(
        key,
        {
            "xg_h": round(1.5 / diff_h, 2),
            "xg_a": round(1.5 / diff_a, 2),
        },
    )

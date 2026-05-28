from utils.log import Logger
from db.db_redis import RedisDB
from scipy.stats import poisson


LOG = Logger("Fixture_xG", "cook/fixture_math")
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

    xg_h = round(1.5 / diff_h, 2)
    xg_a = round(1.5 / diff_a, 2)

    goal_a = []
    goal_h = []

    for k in range(6):
        goal_h.append(float(poisson.pmf(k, xg_h)))
        goal_a.append(float(poisson.pmf(k, xg_a)))

        await DB.hset_one(
            key + ":goal_poisson_h", f"{k}", str(round(goal_h[k] * 100, 3))
        )
        await DB.hset_one(
            key + ":goal_poisson_a", f"{k}", str(round(goal_a[k] * 100, 3))
        )

    home = draw = away = 0.0
    total_s = 6 * 6
    clean_h = clean_a = 0.0
    over = under = 0.0

    for h in range(6):
        for a in range(6):
            p_score = (goal_h[h] * goal_a[a]) * 100

            if h > a:
                home += p_score
            elif h == a:
                draw += p_score
            else:
                away += p_score

            if h == 0:
                clean_h += p_score

            if a == 0:
                clean_a += p_score

            if a + h > 2:
                over += p_score
            else:
                under += p_score

            await DB.hset_one(key + ":score_line", f"{h}-{a}", f"{p_score:.3f}")

    await DB.hset_dict(
        key,
        {
            "win_h": round(home, 3),
            "draw": round(draw, 3),
            "win_a": round(away, 3),
            "clean_h": round(clean_h, 3),
            "clean_a": round(clean_a, 3),
            "over_2": round(over, 3),
            "under_2": round(under, 3),
            "xg_h": xg_h,
            "xg_a": xg_a,
        },
    )

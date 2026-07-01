from service.oracle.utils.log import Logger
from service.oracle.db.db_redis import RedisDB
from scipy.stats import poisson

LOG = Logger("Fixture_xG", "cook/fixture_math")
DB = RedisDB()


def safe_float(v):
    try:
        return float(v)
    except:
        return 0.0


async def cal_fix_xg(gw, fx_id):
    LOG.info(f"--- cal_fix_xg(GW={gw}, FID={fx_id}) ---")

    key = f"proc_fixture:{fx_id}"

    # -------------------------------
    # Load difficulty values
    # -------------------------------
    diff_h = safe_float(await DB.hget_one(key, "diff_h"))
    diff_a = safe_float(await DB.hget_one(key, "diff_a"))

    if diff_h == 0 or diff_a == 0:
        LOG.error(
            f"Invalid diff values for FID={fx_id} → diff_h={diff_h}, diff_a={diff_a}"
        )
        return

    # -------------------------------
    # Compute expected goals
    # -------------------------------
    xg_h = round(1.5 / diff_h, 2)
    xg_a = round(1.5 / diff_a, 2)

    LOG.info(f"xG → Home={xg_h}, Away={xg_a}")

    # -------------------------------
    # Poisson goal probabilities
    # -------------------------------
    goal_h = []
    goal_a = []

    for k in range(6):
        ph = float(poisson.pmf(k, xg_h))
        pa = float(poisson.pmf(k, xg_a))

        goal_h.append(ph)
        goal_a.append(pa)

        await DB.hset_one(f"{key}:goal_poisson_h", f"{k}", f"{ph * 100:.3f}")
        await DB.hset_one(f"{key}:goal_poisson_a", f"{k}", f"{pa * 100:.3f}")

    # -------------------------------
    # Scoreline matrix + match metrics
    # -------------------------------
    home = draw = away = 0.0
    clean_h = clean_a = 0.0
    over = under = 0.0

    for h in range(6):
        for a in range(6):
            p_score = (goal_h[h] * goal_a[a]) * 100

            # Win/draw/loss
            if h > a:
                home += p_score
            elif h == a:
                draw += p_score
            else:
                away += p_score

            # Clean sheets
            if a == 0:
                clean_h += p_score
            if h == 0:
                clean_a += p_score

            # Over/under 2.5
            if h + a > 2:
                over += p_score
            else:
                under += p_score

            await DB.hset_one(f"{key}:score_line", f"{h}-{a}", f"{p_score:.3f}")

    # -------------------------------
    # Save final metrics
    # -------------------------------
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

    LOG.info(
        f"Saved xG + probabilities for FID={fx_id} → "
        f"HW:{home:.2f}, D:{draw:.2f}, AW:{away:.2f}, "
        f"CS_H:{clean_h:.2f}, CS_A:{clean_a:.2f}, "
        f"O2.5:{over:.2f}, U2.5:{under:.2f}"
    )

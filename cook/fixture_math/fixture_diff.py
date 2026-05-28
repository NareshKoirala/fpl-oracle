from db.db_redis import RedisDB
from utils.log import Logger

LOG = Logger("Fixture_Diff", "cook/fixture_math")
DB = RedisDB()


async def team_data(tid, field):
    return await DB.hget_all(f"raw_teams:{tid}:{field}")


def safe_float(v):
    try:
        return float(v)
    except:
        return 0.0


async def fixture_difficulty(team_h, team_a, gw, fx_id):
    LOG.info(
        f"Started fixture_difficulty(H:{team_h}, A:{team_a}, GW:{gw}, FID: {fx_id})"
    )

    ratio_fpl = 0.25
    ratio_cook = 0.25
    ratio_form = 0.40
    ratio_expect = 0.025
    ration_real = 0.075

    cook_data_h = await DB.hget_all(f"proc_strength:{team_h}")
    cook_data_a = await DB.hget_all(f"proc_strength:{team_a}")

    fpl_data_h = await team_data(team_h, "strength")
    fpl_data_a = await team_data(team_a, "strength")

    strength_h = safe_float(fpl_data_h["strength"])
    strength_a = safe_float(fpl_data_a["strength"])

    atk_diff_h = strength_a * (
        (ratio_fpl * safe_float(fpl_data_a["strength_defence_away"]))
        + (ratio_cook * safe_float(cook_data_a["defence_away"]))
        + (ratio_form * safe_float(cook_data_a["defence_last5"]))
        + (ratio_expect * safe_float(cook_data_a["defence_overall_expected"]))
        + (ration_real * safe_float(cook_data_a["defence_overall_real"]))
    )
    atk_diff_a = strength_h * (
        (ratio_fpl * safe_float(fpl_data_h["strength_defence_home"]))
        + (ratio_cook * safe_float(cook_data_h["defence_home"]))
        + (ratio_form * safe_float(cook_data_h["defence_last5"]))
        + (ratio_expect * safe_float(cook_data_h["defence_overall_expected"]))
        + (ration_real * safe_float(cook_data_h["defence_overall_real"]))
    )

    def_diff_h = strength_a * (
        (ratio_fpl * safe_float(fpl_data_a["strength_attack_away"]))
        + (ratio_cook * safe_float(cook_data_a["attack_away"]))
        + (ratio_form * safe_float(cook_data_a["attack_last5"]))
        + (ratio_expect * safe_float(cook_data_a["attack_overall_expected"]))
        + (ration_real * safe_float(cook_data_a["attack_overall_real"]))
    )
    def_diff_a = strength_h * (
        (ratio_fpl * safe_float(fpl_data_h["strength_attack_home"]))
        + (ratio_cook * safe_float(cook_data_h["attack_home"]))
        + (ratio_form * safe_float(cook_data_h["attack_last5"]))
        + (ratio_expect * safe_float(cook_data_h["attack_overall_expected"]))
        + (ration_real * safe_float(cook_data_h["attack_overall_real"]))
    )

    final_diff_h = round((atk_diff_h + def_diff_h) / 2, 2)
    final_diff_a = round((atk_diff_a + def_diff_a) / 2, 2)

    await DB.hset_dict(
        f"proc_fixture:{gw}:{fx_id}",
        {
            "home": team_h,
            "away": team_a,
            "diff_h": final_diff_h,
            "diff_a": final_diff_a,
        },
    )

from db.db_redis import RedisDB
from utils.log import Logger


LOG = Logger("Team_Cook")
DB = RedisDB()


async def p_teams():
    teams_key_map = await DB.get_keys("index:team:*")
    team_ids = [await DB.hget_all(db) for db in teams_key_map]

    avg = await league_avg_xg(team_ids)

    for team in team_ids:
        tid = team["tid"]
        data_ex = await team_data(tid, "expected")
        data_st = await team_data(tid, "strength")
        data_ta = await team_data(tid, "table")
        last5_home, last5_away = await team_fixtures(tid)




        await DB.hset_dict(f"proc_strength_overall:{tid}", cal_overall_strength(avg, data_ex))

async def cal_home

def safe_float(v):
    try:
        return float(v)
    except:
        return 0.0


def cal_overall_strength(avg, data):

    xg = safe_float(data.get("xg"))
    xga = safe_float(data.get("xga"))
    xpts = safe_float(data.get("xpts"))

    xg_diff = safe_float(data.get("xg_difference"))
    xga_diff = safe_float(data.get("xga_difference"))
    xpts_diff = safe_float(data.get("xpts_difference"))

    rg = xg + xg_diff
    rga = xga + xga_diff
    rpts = xpts + xpts_diff

    return {
        "attack_x": f"{(xg / avg[0]):.2f}",
        "defence_x": f"{(xga / avg[1]):.2f}",
        "point_x": f"{(xpts / avg[2]):.2f}",
        "attack_r": f"{(rg / avg[3]):.2f}",
        "defence_r": f"{(rga / avg[4]):.2f}",
        "point_r": f"{(rpts / avg[5]):.2f}",
    }


async def league_avg_xg(ids):
    total_xg = total_xga = total_xpts = 0
    total_rg = total_rga = total_rpts = 0

    size = len(ids)

    for tid in ids:
        data = await team_data(tid["tid"], "expected")

        xg = safe_float(data.get("xg"))
        xga = safe_float(data.get("xga"))
        xpts = safe_float(data.get("xpts"))

        xg_diff = safe_float(data.get("xg_difference"))
        xga_diff = safe_float(data.get("xga_difference"))
        xpts_diff = safe_float(data.get("xpts_difference"))

        total_xg += xg
        total_xga += xga
        total_xpts += xpts

        total_rg += xg + xg_diff
        total_rga += xga + xga_diff
        total_rpts += xpts + xpts_diff

    return (
        total_xg / size,
        total_xga / size,
        total_xpts / size,
        total_rg / size,
        total_rga / size,
        total_rpts / size,
    )


async def team_fixtures(tid):
    home = await DB.lrange(f"index:fixtures:{tid}:home", -5, -1)
    away = await DB.lrange(f"index:fixtures:{tid}:away", -5, -1)
    return (home, away)


async def team_data(tid, field):
    return await DB.hget_all(f"raw_teams:{tid}:{field}")

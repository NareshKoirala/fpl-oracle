from pathlib import Path
from datetime import datetime
from utils.log import Logger


LOG = Logger("Export Redis", "utils")


async def create_folders(db):
    season = await db.hget_one(f"current_gw", "season")
    gw = await db.hget_one(f"current_gw", "current")
    path_dir = Path.cwd() / f"snapshots/{season}/{gw}"
    path_dir.mkdir(parents=True, exist_ok=True)
    return path_dir


TOPICS = [
    "dream_team",
    "fixture",
    "player",
]


async def export_fixture(db):
    r_key = "fixture"
    path = await create_folders(db) / f"{r_key}.json"

    f_keys = await db.get_keys("proc_fixture:*")
    rt_keys = await db.get_keys("index:team:*")

    td_name = {}

    for key in rt_keys:
        t_name = key.decode().split(":")[-1]
        tid = await db.hget_one(key, "tid")

        td_name[tid] = t_name

    data = {}
    for key in f_keys:
        rk_data = await db.hget_all(key)
        
        print(rk_data)

        if key.decode().count(":") == 1:
            fid = key.decode().split(":")[-1]
            data[fid] = {
                **data.get(fid, {}),
                "fixture": fid,
                "home_name": td_name[rk_data["home"]],
                "away_name": td_name[rk_data["away"]],
                **rk_data
            }
        else:
            fid = key.decode().split(":")[-2]
        



async def export_dream_team(db):
    r_data = await db.hget_all("proc_dream_team:")
    rp_keys = await db.get_keys("index:player:*")

    for k, v in r_data.items():
        LOG.info(f"{k}: {v}")
        LOG.info(f"")


async def export_teams_strength(DB):
    data = {}

    r_key = "teams_strength"
    path = await create_folders(DB) / f"{r_key}.json"

    teams = await DB.get_keys(f"index:team:*")

    for team in teams:
        name = team.decode().split(":")[-1]
        tid = await DB.hget_one(team, "tid")

        r_data = await DB.hget_all(f"proc_{r_key}:{tid}")
        m_data = await DB.get_keys(f"raw_teams:{tid}:*")

        temp = {}

        for k, v in r_data.items():
            key = k.split("_")[0]
            title = k.split("_")[-1]

            if title in temp:
                temp[title].update({key: safe_float(v)})
            else:
                temp[title] = {key: safe_float(v)}

        data[name] = temp

        temp = {}

        for m_key in m_data:
            key = m_key.decode().split(":")[-1]

            val = await DB.hget_all(m_key)

            temp[key] = val

        data[name]["meta"] = temp

    write(path, data)


def safe_float(v):
    try:
        return float(v)
    except:
        return v


def write(url, data):
    import json

    with open(url, "w") as f:
        json.dump(data, f, indent=4)


async def export_db1_to_json(DB):

    await export_teams_strength(DB)

    # await export_dream_team(DB)

    await export_fixture(DB)

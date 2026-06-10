from pathlib import Path
from datetime import datetime
from utils.log import Logger


LOG = Logger("Export Redis", "utils")


async def create_folders(db, extra=None):
    season = await db.hget_one(f"current_gw", "season")
    gw = await db.hget_one(f"current_gw", "current")
    if extra:
        path_dir = Path.cwd() / f"snapshots/{season}/{gw}/{extra}"
    else:
        path_dir = Path.cwd() / f"snapshots/{season}/{gw}"
    path_dir.mkdir(parents=True, exist_ok=True)
    return path_dir


TOPICS = [
    "player",
]


async def export_fixture(db):
    r_key = "fixture"

    f_path = await create_folders(db, r_key) / f"{r_key}.json"
    sl_path = await create_folders(db, r_key) / f"{r_key}_scoreline.json"
    gpa_path = await create_folders(db, r_key) / f"{r_key}_gpa.json"
    gph_path = await create_folders(db, r_key) / f"{r_key}_gph.json"

    f_keys = await db.get_keys("proc_fixture:*")
    rt_keys = await db.get_keys("index:team:*")

    td_name = {}

    for key in rt_keys:
        t_name = key.decode().split(":")[-1]
        tid = await db.hget_one(key, "tid")

        td_name[tid] = t_name

    f_data = {}
    sl_data = {}
    gpa_data = {}
    gph_data = {}
    for key in f_keys:
        rk_data = await db.hget_all(key.decode())

        if key.decode().count(":") == 1:
            fid = key.decode().split(":")[-1]
            f_data[fid] = {
                "fixture": fid,
                "home_name": td_name[rk_data["home"]],
                "away_name": td_name[rk_data["away"]],
                **rk_data,
            }
        else:
            fid = key.decode().split(":")[-2]
            name = key.decode().split(":")[-1]

            if name[-1] == "a":
                gpa_data[fid] = rk_data
            elif name[-1] == "h":
                gph_data[fid] = rk_data
            else:
                sl_data[fid] = rk_data

    write(f_path, f_data)
    write(sl_path, sl_data)
    write(gpa_path, gpa_data)
    write(gph_path, gph_data)


async def export_team_of_week(DB):

    keys = [f"index:player:{i}" for i in range(1, 5)]

    players = {}

    for key in keys:
        p_keys = await DB.get_keys(f"{key}:*")

        for p_key in p_keys:
            data = await DB.hget_all(p_key)

            players[data["id"]] = data["name"]

    season = await DB.hget_one("current_gw", "season")
    l_week = await DB.hget_one("current_gw", "last")

    l_path = Path.cwd() / f"snapshots/{season}/{l_week}"
    l_path.mkdir(parents=True, exist_ok=True)
    l_path = l_path / f"team_week.json"

    place_json = {}

    place_json["team"] = {}

    keys = await DB.get_keys("l_team_of_week:*")

    for key in keys:
        data = await DB.hget_all(key.decode())

        if key.decode().count(":") > 1:
            position = key.decode().split(":")[-1]
            place_json["team"] = {
                **place_json["team"],
                players[data["element"]]: {
                    "points": safe_float(data["points"]),
                    "position": safe_float(position),
                    "id": safe_float(data["element"]),
                },
            }
        else:
            place_json["top_player"] = {
                players[data["id"]]: safe_float(data["points"]),
            }

    write(l_path, place_json)

    m_path = await create_folders(DB) / f"team_week.json"

    place_json = {}

    place_json["team"] = {}

    keys = await DB.get_keys("c_team_of_week:*")

    for key in keys:
        data = await DB.hget_all(key.decode())

        if key.decode().count(":") > 1:
            position = key.decode().split(":")[-1]
            place_json["team"] = {
                **place_json["team"],
                players[data["element"]]: {
                    "points": safe_float(data["points"]),
                    "position": safe_float(position),
                    "id": safe_float(data["element"]),
                },
            }
        else:
            place_json["top_player"] = {
                players[data["id"]]: safe_float(data["points"]),
            }

    write(m_path, place_json)


async def export_teams_strength(DB):
    data = {}

    r_key = "teams"
    m_path = await create_folders(DB, r_key) / f"{r_key}_raw.json"
    sp_path = await create_folders(DB, r_key) / f"{r_key}_strength.json"

    teams = await DB.get_keys(f"index:team:*")

    mp_data = {}
    sp_data = {}

    for team in teams:
        name = team.decode().split(":")[-1]
        tid = await DB.hget_one(team, "tid")

        r_data = await DB.hget_all(f"proc_{r_key}_strength:{tid}")
        m_data = await DB.get_keys(f"raw_teams:{tid}:*")

        temp = {}

        for k, v in r_data.items():
            key = k.split("_")[0]
            title = k.split("_")[-1]

            if title in temp:
                temp[title].update({key: safe_float(v)})
            else:
                temp[title] = {key: safe_float(v)}

        sp_data[name] = {**temp}

        temp = {}

        for m_key in m_data:
            key = m_key.decode().split(":")[-1]

            val = await DB.hget_all(m_key)

            temp[key] = val

        mp_data[name] = {**temp}

    write(m_path, mp_data)
    write(sp_path, sp_data)


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

    await export_team_of_week(DB)

    await export_fixture(DB)

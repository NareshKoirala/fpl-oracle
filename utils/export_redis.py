from pathlib import Path
from utils.log import Logger

LOG = Logger("Export Redis", "utils")


# ---------------------------------------------------------
# MASTER HELPERS
# ---------------------------------------------------------


async def create_folders(db, extra=None):
    season = await db.hget_one("current_gw", "season")
    gw = await db.hget_one("current_gw", "current")

    base = Path.cwd() / f"snapshots/{season}/{gw}"
    if extra:
        base = base / extra

    base.mkdir(parents=True, exist_ok=True)
    LOG.info(f"Created folder: {base}")
    return base


def write_json(path, data):
    import json

    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    LOG.info(f"Wrote file: {path}")


def safe_float(v):
    try:
        return float(v)
    except:
        return v


async def collect_team_names(db):
    """Collect tid → team_name mapping."""
    td_name = {}
    rt_keys = await db.get_keys("index:team:*")

    for key in rt_keys:
        key = key.decode()
        t_name = key.split(":")[-1]
        tid = await db.hget_one(key, "tid")
        td_name[tid] = t_name

    LOG.info(f"Collected {len(td_name)} team names")
    return td_name


async def collect_player_names(db):
    """Collect element_id → player_name mapping."""
    players = {}
    index_keys = [f"index:player:{i}" for i in range(1, 5)]

    for key in index_keys:
        p_keys = await db.get_keys(f"{key}:*")
        for p_key in p_keys:
            data = await db.hget_all(p_key)
            players[data["id"]] = data["name"]

    LOG.info(f"Collected {len(players)} player names")
    return players


# ---------------------------------------------------------
# EXPORT: FIXTURES
# ---------------------------------------------------------


async def export_fixture(db):
    LOG.info("=== Exporting Fixtures ===")

    td_name = await collect_team_names(db)
    folder = await create_folders(db, "fixture")

    f_path = folder / "fixture.json"
    sl_path = folder / "fixture_scoreline.json"
    gpa_path = folder / "fixture_gpa.json"
    gph_path = folder / "fixture_gph.json"

    f_keys = await db.get_keys("proc_fixture:*")
    LOG.info(f"Found {len(f_keys)} fixture keys")

    f_data, sl_data, gpa_data, gph_data = {}, {}, {}, {}

    for key in f_keys:
        key = key.decode()
        rk_data = await db.hget_all(key)

        parts = key.split(":")
        if len(parts) == 2:
            # Base fixture
            fid = parts[-1]
            f_data[fid] = {
                "fixture": fid,
                "home_name": td_name[rk_data["home"]],
                "away_name": td_name[rk_data["away"]],
                **rk_data,
            }
        else:
            # Scoreline / GPA / GPH
            fid = parts[-2]
            name = parts[-1]

            if name.endswith("a"):
                gpa_data[fid] = rk_data
            elif name.endswith("h"):
                gph_data[fid] = rk_data
            else:
                sl_data[fid] = rk_data

    write_json(f_path, f_data)
    write_json(sl_path, sl_data)
    write_json(gpa_path, gpa_data)
    write_json(gph_path, gph_data)

    LOG.info("=== Finished Exporting Fixtures ===")


# ---------------------------------------------------------
# EXPORT: TEAM OF THE WEEK
# ---------------------------------------------------------


async def export_team_of_week(db):
    LOG.info("=== Exporting Team of the Week ===")

    players = await collect_player_names(db)

    # LAST WEEK
    season = await db.hget_one("current_gw", "season")
    last_week = await db.hget_one("current_gw", "last")

    last_path = Path.cwd() / f"snapshots/{season}/{last_week}"
    last_path.mkdir(parents=True, exist_ok=True)
    last_path = last_path / "team_week.json"

    place_json = {"team": {}}

    keys = await db.get_keys("l_team_of_week:*")
    LOG.info(f"Found {len(keys)} last-week keys")

    for key in keys:
        key = key.decode()
        data = await db.hget_all(key)

        element_id = data.get("element") or data.get("id")
        if not element_id:
            LOG.error(f"Missing element/id in key: {key} → data={data}")
            continue

        if key.count(":") > 1:
            position = key.split(":")[-1]
            place_json["team"][players[element_id]] = {
                "points": safe_float(data["points"]),
                "position": safe_float(position),
                "id": safe_float(element_id),
            }
        else:
            place_json["top_player"] = {
                players[element_id]: safe_float(data["points"]),
            }

    write_json(last_path, place_json)

    # CURRENT WEEK
    curr_path = await create_folders(db) / "team_week.json"
    place_json = {"team": {}}

    keys = await db.get_keys("c_team_of_week:*")
    LOG.info(f"Found {len(keys)} current-week keys")

    for key in keys:
        key = key.decode()
        data = await db.hget_all(key)

        element_id = data.get("element") or data.get("id")
        if not element_id:
            LOG.error(f"Missing element/id in key: {key} → data={data}")
            continue

        if key.count(":") > 1:
            position = key.split(":")[-1]
            place_json["team"][players[element_id]] = {
                "points": safe_float(data["points"]),
                "position": safe_float(position),
                "id": safe_float(element_id),
            }
        else:
            place_json["top_player"] = {
                players[element_id]: safe_float(data["points"]),
            }

    write_json(curr_path, place_json)

    LOG.info("=== Finished Exporting Team of the Week ===")


# ---------------------------------------------------------
# EXPORT: TEAM STRENGTH
# ---------------------------------------------------------


async def export_teams_strength(db):
    LOG.info("=== Exporting Team Strength ===")

    folder = await create_folders(db, "teams")
    raw_path = folder / "teams_raw.json"
    sp_path = folder / "teams_strength.json"

    teams = await db.get_keys("index:team:*")
    LOG.info(f"Found {len(teams)} teams")

    mp_data, sp_data = {}, {}

    for team in teams:
        team = team.decode()
        name = team.split(":")[-1]
        tid = await db.hget_one(team, "tid")

        r_data = await db.hget_all(f"proc_teams_strength:{tid}")
        m_data = await db.get_keys(f"raw_teams:{tid}:*")

        LOG.info(f"Processing team: {name} ({len(m_data)} raw keys)")

        # Strength data
        temp = {}
        for k, v in r_data.items():
            key = k.split("_")[0]
            title = k.split("_")[-1]
            temp.setdefault(title, {})[key] = safe_float(v)

        sp_data[name] = temp

        # Raw data
        raw_temp = {}
        for m_key in m_data:
            m_key = m_key.decode()
            key = m_key.split(":")[-1]
            raw_temp[key] = await db.hget_all(m_key)

        mp_data[name] = raw_temp

    data = {}
    for k, v in mp_data.items():
        for k1, v1 in v.items():
            data[k1] = {**data.get(k1, {}), k: v1}

    for k, v in data.items():
        path = folder / f"t_{k}.json"

        write_json(path, v)

    write_json(sp_path, sp_data)

    LOG.info("=== Finished Exporting Team Strength ===")


# ---------------------------------------------------------
# MASTER EXPORT
# ---------------------------------------------------------


async def export_db1_to_json(db):
    LOG.info("=== Starting Full DB1 Export ===")

    await export_teams_strength(db)
    await export_team_of_week(db)
    await export_fixture(db)

    LOG.info("=== Finished Full DB1 Export ===")

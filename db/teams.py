from config.data_struct import TEAMS
from config.data_maps import FOTMOB_NAME_MAP
from utils.log import Logger
from db.db_redis import RedisDB

LOG = Logger("Teams_DB", "db")
DB = RedisDB()


def validate_table():
    return TEAMS["table"].copy()


def validate_expected():
    return TEAMS["expected"].copy()


def validate_strength(raw_data):

    dict_copy = TEAMS["strength"].copy()

    for key in dict_copy:
        if key in raw_data:
            value = float(raw_data[key])
            dict_copy[key] = value if value <= 5 else value / 1000

    return dict_copy


def validate_name(raw_data):
    if "name" in raw_data and isinstance(raw_data["name"], str):
        name = raw_data["name"]
        if name in FOTMOB_NAME_MAP:
            name = FOTMOB_NAME_MAP[name]
        return name
    else:
        LOG.error("Invalid or missing 'name' field in team data.")


def validate_short_name(raw_data):
    if "short_name" in raw_data and isinstance(raw_data["short_name"], str):
        return raw_data["short_name"]
    else:
        LOG.error("Invalid or missing 'short_name' field in team data.")


async def get_teams(raw_data):
    tid = raw_data["id"]
    db = f"raw_teams:{tid}"
    table = validate_table()
    expected = validate_expected()
    strength = validate_strength(raw_data)
    name = validate_name(raw_data)
    short_name = validate_short_name(raw_data)

    LOG.info(f"Creating team: {name} with tid: {tid}")
    await DB.hset_one(f"index:team:{name}", "tid", tid)
    await DB.hset_one(f"index:p_team", f"{raw_data["code"]}", tid)
    await DB.hset_dict(db + ":table", table)
    await DB.hset_dict(db + ":strength", strength)
    await DB.hset_dict(db + ":expected", expected)

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
            # Normalize if fpl gives 5000 instead of 5.0
            dict_copy[key] = value if value <= 5 else value / 1000

    return dict_copy


def validate_name(raw_data):
    if "name" in raw_data and isinstance(raw_data["name"], str):
        name = raw_data["name"]
        if name in FOTMOB_NAME_MAP:
            mapped = FOTMOB_NAME_MAP[name]
            LOG.info(f"Mapping team name: {name} → {mapped}")
            name = mapped
        return name

    LOG.error("Invalid or missing 'name' field in team data.")
    return None


def validate_short_name(raw_data):
    if "short_name" in raw_data and isinstance(raw_data["short_name"], str):
        return raw_data["short_name"]

    LOG.error("Invalid or missing 'short_name' field in team data.")
    return None


async def get_teams(raw_data):
    tid = raw_data["id"]
    db = f"raw_teams:{tid}"

    name = validate_name(raw_data)
    short_name = validate_short_name(raw_data)
    table = validate_table()
    expected = validate_expected()
    strength = validate_strength(raw_data)

    LOG.info(f"Saving team → {name} (short={short_name}, tid={tid})")

    # Index team by name
    await DB.hset_one(f"index:team:{name}", "tid", tid)

    # Save raw sections
    await DB.hset_dict(f"{db}:table", table)
    await DB.hset_dict(f"{db}:strength", strength)
    await DB.hset_dict(f"{db}:expected", expected)

    LOG.info(f"Team saved → {name} (tid={tid})")

from service.oracle.config.data_struct import TEAM
from service.oracle.config.data_maps import FOTMOB_NAME_MAP
from service.oracle.utils.log import Logger
from service.oracle.db.db_redis import RedisDB

LOG = Logger("Teams_DB", "db")
DB = RedisDB()


async def get_teams(raw_data):
    tid = raw_data["id"]
    name = (
        raw_data["name"] in FOTMOB_NAME_MAP
        if FOTMOB_NAME_MAP["name"]
        else raw_data["name"]
    )
    short_name = raw_data["short_name"]

    db = f"team:{tid}"

    temp = {}

    for k in TEAM:

        if k == "name":
            temp[k] = name
            continue

        temp[k] = raw_data.get(k)

    LOG.info(f"Saving team → {name} (short={short_name}, tid={tid})")

    # Index team by name
    await DB.hset_one(f"index:team_name:{name}", "tid", tid)

    # Save raw sections
    await DB.hset_dict(f"{db}", temp)

    LOG.info(f"Team saved → {name} (tid={tid})")

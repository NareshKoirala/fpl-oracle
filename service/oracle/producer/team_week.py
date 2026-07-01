from service.oracle.db.db_redis import RedisDB
from service.oracle.config.settings import TEAM_OF_WEEK
from service.oracle.utils.scraper import Scraper
from service.oracle.utils.log import Logger

DB = RedisDB()
LOG = Logger("Team_Of_Week", "producer")


async def get_team_of_week():
    LOG.info("========== START get_team_of_week() ==========")

    l_week = await DB.hget_one("status", "last")
    c_week = await DB.hget_one("status", "current")

    # -----------------------------
    # LAST WEEK
    # -----------------------------
    url = TEAM_OF_WEEK + l_week + "/"
    LOG.info(f"Fetching LAST week team of the week → GW {l_week}")
    data = await Scraper().fetch_request(url)

    if not data:
        LOG.error(f"Failed to fetch last-week team of the week for GW {l_week}")
    else:
        await formats(data, "l_team_of_week")

    # -----------------------------
    # CURRENT WEEK
    # -----------------------------
    url = TEAM_OF_WEEK + c_week + "/"
    LOG.info(f"Fetching CURRENT week team of the week → GW {c_week}")
    data = await Scraper().fetch_request(url)

    if not data:
        LOG.error(f"Failed to fetch current-week team of the week for GW {c_week}")
    else:
        await formats(data, "c_team_of_week")

    LOG.info("========== END get_team_of_week() ==========")


async def formats(data, key):
    LOG.info(f"Formatting team of the week data for key: {key}")

    if len(data) <= 1:
        LOG.error(f"No valid data found for {key}. Skipping.")
        return

    for k, v in data.items():
        # LIST = players in positions
        if isinstance(v, list):
            LOG.info(f"Processing list for: {key}:{k} ({len(v)} entries)")

            for d in v:
                position = d["position"]
                element = d["element"]
                points = d["points"]

                redis_key = f"{key}:{k}:{position}"

                await DB.hset_dict(
                    redis_key,
                    {
                        "element": element,
                        "points": points,
                    },
                )

                LOG.info(f"Saved → {redis_key} (element={element}, points={points})")

        # DICT = top player
        else:
            redis_key = f"{key}:{k}"
            await DB.hset_dict(redis_key, v)

            LOG.info(f"Saved top player → {redis_key}: {v}")

import json
from pathlib import Path
import redis.asyncio as redis
from service.oracle.config.settings import LIVE_HOST, LIVE_PORT, SNAPSHOTS_DIR
from service.oracle.utils.log import Logger

LOG = Logger("Export Redis Pretty", "utils")


async def get_season_gw():
    """Helper to query the current season and gameweek from status hash in DB 0."""
    r = redis.Redis(host=LIVE_HOST, port=LIVE_PORT, db=0, decode_responses=True)
    try:
        status = await r.hgetall("status")
        season = status.get("season", "unknown_season")
        gw = status.get("current", "unknown_gw")
        return season, gw
    finally:
        await r.aclose()


async def export_db0():
    """Loops DB 0 (raw) and exports all data with crisp, pretty formatting to a JSON file in snapshots."""
    LOG.info("Starting pretty export of DB 0 (Raw data)...")
    season, gw = await get_season_gw()
    folder = SNAPSHOTS_DIR / str(season) / str(gw)
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / "raw_database.json"

    r = redis.Redis(host=LIVE_HOST, port=LIVE_PORT, db=0, decode_responses=True)
    formatted_data = {}
    try:
        async for key in r.scan_iter("*"):
            key_type = await r.type(key)

            if key_type == "string":
                formatted_data[key] = await r.get(key)
            elif key_type == "hash":
                formatted_data[key] = await r.hgetall(key)
            elif key_type == "set":
                formatted_data[key] = sorted(list(await r.smembers(key)))
            elif key_type == "list":
                formatted_data[key] = await r.lrange(key, 0, -1)
            elif key_type == "zset":
                pairs = await r.zrange(key, 0, -1, withscores=True)
                formatted_data[key] = {member: score for member, score in pairs}

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(formatted_data, file, indent=4)
        LOG.info(f"✨ DB 0 data exported with crisp, human-readable formatting to {filepath}")
    finally:
        await r.aclose()


async def export_db1():
    """Loops DB 1 (proc) and exports all data with crisp, pretty formatting to a JSON file in snapshots."""
    LOG.info("Starting pretty export of DB 1 (Processed data)...")
    season, gw = await get_season_gw()
    folder = SNAPSHOTS_DIR / str(season) / str(gw)
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / "processed_database.json"

    r = redis.Redis(host=LIVE_HOST, port=LIVE_PORT, db=1, decode_responses=True)
    formatted_data = {}
    try:
        async for key in r.scan_iter("*"):
            key_type = await r.type(key)

            if key_type == "string":
                formatted_data[key] = await r.get(key)
            elif key_type == "hash":
                formatted_data[key] = await r.hgetall(key)
            elif key_type == "set":
                formatted_data[key] = sorted(list(await r.smembers(key)))
            elif key_type == "list":
                formatted_data[key] = await r.lrange(key, 0, -1)
            elif key_type == "zset":
                pairs = await r.zrange(key, 0, -1, withscores=True)
                formatted_data[key] = {member: score for member, score in pairs}

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(formatted_data, file, indent=4)
        LOG.info(f"✨ DB 1 data exported with crisp, human-readable formatting to {filepath}")
    finally:
        await r.aclose()

from service.oracle.config.settings import SNAPSHOTS_DIR
import os
from fastapi import APIRouter, Depends
from service.oracle.utils.redis_server import start_past_server
from service.oracle.utils.log import Logger
import json

router = APIRouter(prefix="/history-path", tags=["history_path"])
LOG = Logger("History Path Waiter", "waiter/endpoints")

SNAPSHOT_ROOT = str(SNAPSHOTS_DIR)


@router.get("/", response_model=dict)
async def get_history_paths():
    LOG.info("Fetching history paths from snapshots root")
    seasons = {}

    # Loop through season folders
    for season_folder in os.listdir(SNAPSHOT_ROOT):
        season_path = os.path.join(SNAPSHOT_ROOT, season_folder)

        if not os.path.isdir(season_path):
            continue

        # Collect valid gameweeks
        weeks = []
        for gw_folder in os.listdir(season_path):
            gw_path = os.path.join(season_path, gw_folder)

            if os.path.isdir(gw_path):
                # Only include if dump.rdb exists
                dump_file = os.path.join(gw_path, "raw.rdb")
                if os.path.exists(dump_file):
                    weeks.append(int(gw_folder))

        if weeks:
            seasons[int(season_folder)] = sorted(weeks, reverse=True)

    data = dict(sorted(seasons.items(), reverse=True))
    LOG.info(f"Loaded {len(data)} seasons of history paths")

    return data

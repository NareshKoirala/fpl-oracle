import os
from fastapi import APIRouter, Depends
from models.history_path import Season, HistorySeasonResponse
from utils.redis_server import start_past_server

router = APIRouter(prefix="/history-path", tags=["history_path"])

SNAPSHOT_ROOT = os.path.join(os.getcwd(), "snapshots")


@router.get("/history/seasons", response_model=HistorySeasonResponse)
async def get_history_paths():
    seasons = []

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
            seasons.append(Season(season=int(season_folder), weeks=sorted(weeks)))

    return HistorySeasonResponse(data=seasons)


@router.post("/cold-start?path")
async def check_redis(path):
    if path != "current":
        s, w = path.split(":")
        start_past_server(s, w)

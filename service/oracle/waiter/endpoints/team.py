from service.oracle.config.settings import SNAPSHOTS_DIR
from fastapi import APIRouter
import json
from pathlib import Path
from service.oracle.utils.log import Logger

router = APIRouter(prefix="/team", tags=["team"])
LOG = Logger("Team Waiter", "waiter/endpoints")


def get_json(filepath):
    cwd = SNAPSHOTS_DIR / f"{filepath}.json"

    if not cwd.exists():
        LOG.error(f"File not found: {cwd}")
        return {}

    try:
        with open(cwd, "r") as f:
            data = json.load(f)
            LOG.info(f"Data loaded for {filepath}: {len(data)} entries found.")
            return data
    except json.JSONDecodeError:
        LOG.error(f"Invalid JSON in: {cwd}")
        return {}


@router.get("/{season}/{gw}")
def get_table(season: str, gw: str):
    return get_json(f"{season}/{gw}/teams/t_table")


@router.get("/away/{season}/{gw}")
def get_away(season: str, gw: str):
    return get_json(f"{season}/{gw}/teams/t_away")


@router.get("/home/{season}/{gw}")
def get_home(season: str, gw: str):
    return get_json(f"{season}/{gw}/teams/t_home")


@router.get("/expected/{season}/{gw}")
def get_expected(season: str, gw: str):
    return get_json(f"{season}/{gw}/teams/t_expected")


@router.get("/last_five/{season}/{gw}")
def get_last_five(season: str, gw: str):
    return get_json(f"{season}/{gw}/teams/t_last_five")


@router.get("/strength/{season}/{gw}")
def get_strength(season: str, gw: str):
    return get_json(f"{season}/{gw}/teams/t_strength")


@router.get("/team_of_week/{season}/{gw}")
def get_team_of_week(season: str, gw: str):
    return get_json(f"{season}/{gw}/team_week")


@router.get("/proc_strength/{season}/{gw}")
def get_proc_strength(season: str, gw: str):
    return get_json(f"{season}/{gw}/teams/teams_strength")

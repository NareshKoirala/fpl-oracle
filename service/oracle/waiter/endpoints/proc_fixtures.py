from fastapi import APIRouter, Depends
from utils.log import Logger
from pathlib import Path
import json

router = APIRouter(prefix="/proc_fixtures", tags=["proc_fixtures"])
LOG = Logger("Proc Fixture Waiter", "waiter/endpoints")


def get_json(filepath):
    cwd = Path.cwd() / "snapshots" / f"{filepath}.json"

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
    return get_json(f"{season}/{gw}/proc_fixture/fixture")


@router.get("/gpa/{season}/{gw}")
def get_away(season: str, gw: str):
    return get_json(f"{season}/{gw}/proc_fixture/fixture_gpa")


@router.get("/gph/{season}/{gw}")
def get_home(season: str, gw: str):
    return get_json(f"{season}/{gw}/proc_fixture/fixture_gph")


@router.get("/scoreline/{season}/{gw}")
def get_expected(season: str, gw: str):
    return get_json(f"{season}/{gw}/proc_fixture/fixture_scoreline")

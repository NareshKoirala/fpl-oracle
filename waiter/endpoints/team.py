from fastapi import APIRouter, Depends
import json
from pathlib import Path

router = APIRouter(prefix="/team", tags=["team"])


def get_json(filepath):
    cwd = Path.cwd() / filepath + ".json"
    data = {}

    with open(cwd, "r") as f:
        data = json.load(f)

    return data


@router.get("/table/{season}/{gw}")
def get_table(season, gw):
    print(season, gw)

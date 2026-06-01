from pathlib import Path


async def create_folders(db):
    season = await db.hget_one(f"current_gw", "season")
    gw = await db.hget_one(f"current_gw", "current")
    path_dir = Path.cwd() / f"snapshots/{season}/{gw}"
    path_dir.mkdir(parents=True, exist_ok=True)
    return path_dir


async def export_db1_to_json(DB, key):

    keys = await DB.get_keys(f"proc_{key}:*")
    data = {}

    filename = f"{key}.json"

    url = await create_folders(DB) / filename

    for key in keys:
        key = key.decode()
        data[key] = await DB.hget_all(key)

    import json

    with open(url, "w") as f:
        json.dump(data, f, indent=4)

from pathlib import Path


async def create_folders(db):
    path_dir = Path.cwd() / "snapshots"
    path_dir.mkdir(parents=True, exist_ok=True)
    season = await db.hget_one(f"current_gw", "season")
    path_dir = path_dir / f"proc/{season}"
    path_dir.mkdir(parents=True, exist_ok=True)
    return path_dir


async def export_db1_to_json(DB, gw, key):

    keys = await DB.get_keys(f"proc_{key}:*")
    data = {}

    filename = f"{key}_{gw}.json"

    url = await create_folders(DB) / filename

    for key in keys:
        key = key.decode()
        data[key] = await DB.hget_all(key)

    import json

    with open(url, "w") as f:
        json.dump(data, f, indent=4)


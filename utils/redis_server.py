import subprocess
import os
from config.settings import LIVE_PORT, PAST_PORT
from utils.log import Logger


LOG = Logger("Redis Server", "utils")


def start_past_server(season, gw):
    c_path = os.path.join(os.getcwd(), f"snapshots/{season}/{gw}/")
    os.makedirs(c_path, exist_ok=True)

    cmd = [
        "redis-server",
        "--port",
        str(PAST_PORT),
        "--dir",
        c_path,
        "--dbfilename",
        "raw.rdb",
    ]

    subprocess.Popen(cmd)


def start_live_server():
    download_req()
    download_chrome()
    enable_redis()


def download_chrome():

    cmd = ["python", "-m", "playwright", "install", "chromium"]

    process = subprocess.Popen(cmd)

    process.wait()


def download_req():
    n_path = os.path.join(os.getcwd(), f"requirements.txt")

    if not os.path.exists(n_path):
        with open(n_path, "w") as f:
            pass

    cmd = ["python", "-m", "pip", "install", "-r", "requirements.txt"]

    process = subprocess.Popen(cmd)

    process.wait()


def enable_redis():

    n_path = os.path.join(os.getcwd(), f"snapshots/")
    os.makedirs(n_path, exist_ok=True)

    cmd = [
        "redis-server",
        "--port",
        f"{LIVE_PORT}",
        "--dir",
        n_path,
        "--dbfilename",
        "raw.rdb",
    ]

    subprocess.Popen(cmd)

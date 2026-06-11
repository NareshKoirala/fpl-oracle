import subprocess
import threading
import os
import socket
import time

from config.settings import LIVE_PORT, PAST_PORT, LIVE_HOST, PAST_HOST
from utils.log import Logger

LOG = Logger("Launcher", "utils")


# ---------------------------------------------------------
# REAL-TIME LOG STREAMING
# ---------------------------------------------------------


def stream_output(pipe, logger_method):
    for line in pipe:
        logger_method(line.rstrip())


def log_process_header(cmd):
    LOG.info("=" * 80)
    LOG.info(f"Starting process: {' '.join(cmd)}")
    LOG.info("=" * 80)


def run_with_logs(cmd, logger, wait=False):
    log_process_header(cmd)

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # <— enables text mode
        bufsize=1,  # <— line buffering now allowed
    )

    threading.Thread(
        target=stream_output, args=(process.stdout, logger.info), daemon=True
    ).start()
    threading.Thread(
        target=stream_output, args=(process.stderr, logger.error), daemon=True
    ).start()

    if wait:
        process.wait()

    return process


# ---------------------------------------------------------
# PORT WAITING
# ---------------------------------------------------------


def wait_for_port(port, host="127.0.0.1", timeout=30):
    LOG.info(f"Waiting for port {port} to open...")
    start = time.time()

    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                LOG.info(f"Port {port} is ready.")
                return True
        except OSError:
            time.sleep(0.2)

    raise TimeoutError(f"Port {port} not ready after {timeout} seconds")


# ---------------------------------------------------------
# PACKAGE INSTALLATION
# ---------------------------------------------------------


def download_chrome():
    cmd = ["python", "-m", "playwright", "install", "chromium"]
    run_with_logs(cmd, LOG, wait=True)


def download_req():
    n_path = os.path.join(os.getcwd(), "requirements.txt")

    if not os.path.exists(n_path):
        with open(n_path, "w") as f:
            pass

    cmd = ["python", "-m", "pip", "install", "-r", "requirements.txt"]
    run_with_logs(cmd, LOG, wait=True)


# ---------------------------------------------------------
# REDIS SERVERS
# ---------------------------------------------------------


def enable_redis():
    kill_if_enable(LIVE_HOST, LIVE_PORT)

    n_path = os.path.join(os.getcwd(), "snapshots/")
    os.makedirs(n_path, exist_ok=True)

    cmd = [
        "redis-server",
        "--port",
        str(LIVE_PORT),
        "--dir",
        n_path,
        "--dbfilename",
        "raw.rdb",
    ]

    run_with_logs(cmd, LOG)


def kill_if_enable(host, port):
    import socket
    import psutil

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.close()

        LOG.info(f"Redis detected on port {port}. Killing...")

        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            if "redis-server" in proc.info["name"]:
                proc.kill()
                LOG.info(f"Killed Redis PID {proc.info['pid']}")

    except Exception:
        LOG.info(f"No Redis running on port {port}.")


def start_past_server(season, gw):
    kill_if_enable(PAST_HOST, PAST_PORT)

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

    run_with_logs(cmd, LOG)


# ---------------------------------------------------------
# FASTAPI + NPM DASHBOARD
# ---------------------------------------------------------


def start_uvicorn():
    cmd = [
        "uvicorn",
        "waiter.waiter:app",
        "--reload",
    ]

    run_with_logs(cmd, LOG)


def run_npm():
    # Install packages first
    run_with_logs(["npm", "install", "--prefix", "dashboard"], LOG, wait=True)

    # Start dev server (non-blocking)
    run_with_logs(["npm", "run", "dev", "--prefix", "dashboard"], LOG)


# ---------------------------------------------------------
# MAIN LIVE SERVER STARTUP
# ---------------------------------------------------------


def start_live_server():
    LOG.info("Starting Live Server Pipeline...")

    download_req()
    download_chrome()

    enable_redis()
    wait_for_port(LIVE_PORT)

    start_uvicorn()
    wait_for_port(8000)

    run_npm()

    LOG.info("Live Server Pipeline fully started.")

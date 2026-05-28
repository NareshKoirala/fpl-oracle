import datetime
from pathlib import Path


class Logger:
    def __init__(self, fileName, subRepo=None):
        # Modern path handling
        log_dir = Path.cwd() / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        if subRepo:
            log_dir = log_dir / subRepo
            log_dir.mkdir(parents=True, exist_ok=True)

        fileName = f"{fileName}.log"
        self.log_path = log_dir / fileName

    def log(self, level, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {level}: {message}"

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

    def info(self, message):
        self.log("INFO", message)

    def error(self, message):
        self.log("ERROR", message)

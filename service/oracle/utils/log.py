import datetime
from service.oracle.config.settings import LOGS_DIR


class Logger:
    COLORS = {
        "INFO": "\033[96m",  # cyan
        "ERROR": "\033[91m",  # red
        "DEBUG": "\033[93m",  # yellow
        "RESET": "\033[0m",
    }

    def __init__(self, fileName, subRepo=None):
        log_dir = LOGS_DIR
        log_dir.mkdir(parents=True, exist_ok=True)

        self.fileName = fileName

        if subRepo:
            log_dir = log_dir / subRepo
            log_dir.mkdir(parents=True, exist_ok=True)

        self.log_path = log_dir / f"{fileName}.log"

    def log(self, level, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {level}: {message}"

        # Write to file
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

        # Pretty console output
        color = self.COLORS.get(level, "")
        reset = self.COLORS["RESET"]
        print(f"{color}({self.fileName}) {log_entry}{reset}")

    def info(self, message):
        self.log("INFO", message)

    def error(self, message):
        self.log("ERROR", message)

    def debug(self, message):
        self.log("DEBUG", message)

# API Endpoints
SEASON = "2025/2026"

FPL_BOOTSTRAP = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIXTURES = "https://fantasy.premierleague.com/api/fixtures/"
PLAYER_HISTORY = f"https://fantasy.premierleague.com/api/element-summary/"
TEAM_OF_WEEK = "https://fantasy.premierleague.com/api/dream-team/"
FPL_SET_PIECE_NOTES = "https://fantasy.premierleague.com/api/team/set-piece-notes/"

FOTMOB_BASE = "https://www.fotmob.com/leagues/47/"
# FOTMOB_TABLE = f"{FOTMOB_BASE}table/premier-league?"
FOTMOB_TABLE = f"{FOTMOB_BASE}table/premier-league?season={SEASON}&"
FOTMOB_xG = f"{FOTMOB_TABLE}filter=xg"
FOTMOB_HOME = f"{FOTMOB_TABLE}filter=home"
FOTMOB_AWAY = f"{FOTMOB_TABLE}filter=away"
FOTMOB_FORM = f"{FOTMOB_TABLE}filter=form"

# Key Classes for FotMob
TABLE_CLASS = "flipmove"
TEAM_STATS_SECTION_CLASS = "e1uxaz290"
TEAM_STATS_DIV_CLASS = "e1m5w55z1"

# Key Classes for EPL
EPL_FILTER_CLASS = "filters"

# Scraper Settings
AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
HEAD = True  # Set to False for headless mode
BROWSER_WAIT_TIME = 8000  # Time to wait for page elements to load (in milliseconds)
SLOW_MOTION = 3  # Slow down Playwright actions for more human-like

# Redis
LIVE_HOST = "localhost"
LIVE_PORT = 6379

PAST_HOST = "localhost"
PAST_PORT = 6380

# Paths relative to fpl-oracle/service/
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # service/
SNAPSHOTS_DIR = BASE_DIR / "snapshots"
LOGS_DIR = BASE_DIR / ".cache/logs"
PW_SESSION_DIR = BASE_DIR / ".cache/pw_session"

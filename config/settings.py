 # API Endpoints
YAHOO_SPORTS = "https://sports.yahoo.com/soccer/premier-league/stats/team/?_rsc=k9461"

FPL_BOOTSTRAP = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIXTURES = "https://fantasy.premierleague.com/api/fixtures/"
PLAYER_HISTORY = f"https://fantasy.premierleague.com/api/element-summary/"

FOTMOB_BASE = "https://www.fotmob.com"
FOTMOB_TABLE = f"{FOTMOB_BASE}/leagues/47/table/premier-league/teams"
FOTMOB_xG = f"{FOTMOB_TABLE}?filter=xg"
FOTMOB_HOME = f"{FOTMOB_TABLE}?filter=home"
FOTMOB_AWAY = f"{FOTMOB_TABLE}?filter=away"
FOTMOB_FORM = f"{FOTMOB_TABLE}?filter=form"
FOTMOB_TEAM_STATS = f"{FOTMOB_BASE}/leagues/47/stats/premier-league/teams"
FOTMOB_PLAYER_STATS = f"{FOTMOB_BASE}/leagues/47/stats/premier-league/players"

EPL_STATS = "https://www.premierleague.com/en/stats/top/goals/2025-26"
EPL_SEASON = "2025-26"

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

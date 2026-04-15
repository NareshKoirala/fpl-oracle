# API Endpoints
FPL_BOOTSTRAP = "https://fantasy.premierleague.com/api/bootstrap-static/"
FOTMOB_BASE = "https://www.fotmob.com"
FOTMOB_TABLE = f"{FOTMOB_BASE}/leagues/47/table/premier-league/teams"
FOTMOB_TEAM_STATS = f"{FOTMOB_BASE}/leagues/47/stats/premier-league/teams"
FOTMOB_PLAYER_STATS = f"{FOTMOB_BASE}/leagues/47/stats/premier-league/players"

# Key Classes for FotMob



# Scraper Settings
AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
HEAD = True  
BROWSER_WAIT_TIME = 10000

# The Translator
NAME_MAP = {
    "Man Utd": "Man United",
    "Nott'm Forest": "Nottm Forest",
    "Spurs": "Tottenham",
}
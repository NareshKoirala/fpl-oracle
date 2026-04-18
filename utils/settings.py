# API Endpoints
YAHOO_SPORTS = "https://sports.yahoo.com/soccer/premier-league/stats/team/?_rsc=k9461"
FPL_BOOTSTRAP = "https://fantasy.premierleague.com/api/bootstrap-static/"
FOTMOB_BASE = "https://www.fotmob.com"
FOTMOB_TABLE = f"{FOTMOB_BASE}/leagues/47/table/premier-league/teams"
FOTMOB_TEAM_STATS = f"{FOTMOB_BASE}/leagues/47/stats/premier-league/teams"
FOTMOB_PLAYER_STATS = f"{FOTMOB_BASE}/leagues/47/stats/premier-league/players"

# Key Classes for FotMob
TABLE_CLASS = "flipmove"
TEAM_STATS_CLASS = "e1m5w55z1"

# Scraper Settings
AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
HEAD = False
BROWSER_WAIT_TIME = 20000

# The Translator
NAME_MAP = {
    "Man Utd": "Man United",
    "Nott'm Forest": "Nottm Forest",
    "Spurs": "Tottenham",
}

# Teams & Players keys
TEAMS_KEYS = [
    "strength_overall_home",
    "strength_overall_away",
    "strength_attack_home",
    "strength_attack_away",
    "strength_defence_home",
    "strength_defence_away",
    "strength",
    "win",
    "draw",
    "loss",
    "played",
    "points",
    "position",
    "form",
    "fotmob_rating",
    "goals_per_match",
    "goals_conceded_per_match",
    "average_possession",
    "clean_sheets",
    "expected_goals_xg",
    "xg_difference",
    "shots_on_target_per_match",
    "big_chances",
    "big_chances_missed",
    "accurate_passes_per_match",
    "accurate_long_balls_per_match",
    "accurate_crosses_per_match",
    "penalties_awarded",
    "touches_in_opposition_box",
    "corners",
    "set_piece_goals",
    "xg_conceded",
    "interceptions_per_match",
    "tackles_per_match",
    "clearances_per_match",
    "possession_won_final_3rd_per_match",
    "set_piece_goals_conceded",
    "penalties_conceded",
    "saves_per_match",
    "fouls_per_match",
    "yellow_cards",
    "red_cards",
]
PLAYERS_KEYS = []
# The Translator
FOTMOB_NAME_MAP = {
    "Man Utd": "Man United",
    "Nott'm Forest": "Nottm Forest",
    "Spurs": "Tottenham",
}

EPL_STAT_NAME_MAP = {
    "direct-free-kick-goals": "set-pieces-goals",
    "assists": "goal-assists",
    "red-cards": "total-red-cards",
    "corners-taken": "corners-taken-incl-short-corners",
    "fouls-conceded": "total-fouls-conceded",
    "clearances": "total-clearances",
    "penalties": "penalty-goals",
}

EPL_NAME_MAP = {
    "Leeds United": "Leeds",
    "Manchester City": "Man City",
    "Manchester United": "Man United",
    "Newcastle United": "Newcastle",
    "Tottenham Hotspur": "Tottenham",
    "Brighton and Hove Albion": "Brighton",
    "Wolverhampton Wanderers": "Wolves",
    "West Ham United": "West Ham",
    "Nottingham Forest": "Nottm Forest",
}

PLAYERS_KEY_MAP = {
    "web_name": "name",
    "team_code": "team_id",
    "element_type": "position",
    "chance_of_playing_this_round": "chance_of_playing",
    "now_cost": "cost",
}

PLAYER_GW_KEY_MAP = {
    "fixture_id": "fixture",
    "opponent_team_id": "opponent_team",
}

FIXTURE_MAP = {
    "gw": "event",
    "home_id": "team_h",
    "away_id": "team_a",
    "home_score": "team_h_score",
    "away_score": "team_a_score",
}

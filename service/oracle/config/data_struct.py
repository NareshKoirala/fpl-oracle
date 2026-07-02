"""
FPL-Oracle Redis Schema — Data Structures
==========================================
Defines the flat field templates for every Redis HASH key used in the system.

Each dict represents exactly one Redis HASH key:
    - Keys are field names stored inside that hash.
    - Values are the default/zero value for that field.

DB Routing Rule (enforced in RedisDB._select):
    key.startswith("proc_") → DB 1 (processed)
    everything else          → DB 0 (raw)

Usage pattern in writers:
    template = PLAYER.copy()
    for field in template:
        if field in raw_api_data:
            template[field] = str(raw_api_data[field])
    await db.hset_dict(f"player:{pid}", template)
"""


# =============================================================================
# DB 0 — RAW DATA
# =============================================================================


# -----------------------------------------------------------------------------
# player:{id} — HASH
# Core identity + current FPL season stats.
# Source: FPL bootstrap-static API → elements[]
# -----------------------------------------------------------------------------
PLAYER = {
    # Identity
    "id": "0",
    "first_name": "",
    "second_name": "",
    "name": "",             # (web_name) — the display name used everywhere
    "code": "0",            # FPL photo/asset code
    # Relationships (normalized IDs)
    "team_id": "0",         # FK → team:{id} (team_code)
    "position": "0",        # 1=GK  2=DEF  3=MID  4=FWD (element_type)
    # Availability
    "status": "a",          # a=available  d=doubtful  i=injured  s=suspended  u=unavailable
    "chance_of_playing": "100", # (chance_of_playing_this_round)
    "news": "",
    # Pricing
    "cost": "0",            # (now_cost) / 10 (stored as float string e.g. "8.5")
    "cost_change_start": "0", 
    "cost_change_event": "0",
    # Current season totals (summary — full history in player:{id}:season:{year})
    "total_points": "0",
    "points_per_game": "0",
    "form": "0",
    "minutes": "0",
    "goals_scored": "0",
    "assists": "0",
    "clean_sheets": "0",
    "goals_conceded": "0",
    "own_goals": "0",
    "penalties_saved": "0",
    "penalties_missed": "0",
    "yellow_cards": "0",
    "red_cards": "0",
    "saves": "0",
    "bonus": "0",
    "bps": "0",
    "starts": "0",
    # ICT Index
    "influence": "0",
    "creativity": "0",
    "threat": "0",
    "ict_index": "0",
    # Expected stats (current season)
    "expected_goals": "0",
    "expected_assists": "0",
    "expected_goal_involvements": "0",
    "expected_goals_conceded": "0",
    # Per-90 expected stats
    "expected_goals_per_90": "0",
    "expected_assists_per_90": "0",
    "expected_goal_involvements_per_90": "0",
    "expected_goals_conceded_per_90": "0",
    "goals_conceded_per_90": "0",
    "clean_sheets_per_90": "0",
    "saves_per_90": "0",
    "starts_per_90": "0",
    # FPL projected points
    "ep_this": "0",
    "ep_next": "0",
}


# -----------------------------------------------------------------------------
# player:{id}:meta — HASH
# FPL metadata: ownership, transfers, set-piece roles, ranks.
# Source: FPL bootstrap-static API → elements[]
# -----------------------------------------------------------------------------
PLAYER_META = {
    # Ownership & transfers
    "selected_by_percent": "0",
    "transfers_in": "0",
    "transfers_in_event": "0",
    "transfers_out": "0",
    "transfers_out_event": "0",
    "value_form": "0",
    "value_season": "0",
    # Dream Team
    "event_points": "0",
    "in_dreamteam": "False",
    "dreamteam_count": "0",
    # Set pieces (order = 1 means first taker, "" = not a taker)
    "corners_and_indirect_freekicks_order": "",
    "direct_freekicks_order": "",
    "penalties_order": "",
    # Ranks (within position group)
    "selected_rank": "0",
    "selected_rank_type": "0",
    "influence_rank": "0",
    "influence_rank_type": "0",
    "creativity_rank": "0",
    "creativity_rank_type": "0",
    "threat_rank": "0",
    "threat_rank_type": "0",
    "ict_index_rank": "0",
    "ict_index_rank_type": "0",
    "now_cost_rank": "0",
    "now_cost_rank_type": "0",
    "form_rank": "0",
    "form_rank_type": "0",
    "points_per_game_rank": "0",
    "points_per_game_rank_type": "0",
}


# -----------------------------------------------------------------------------
# player:{id}:season:{year} — HASH
# Full career season totals per year (year = end year, e.g. 2025 for 2024/25).
# Source: FPL player-summary API → history_past[]
# Note: year key is normalized via normalize_season() in the writer.
# -----------------------------------------------------------------------------
PLAYER_SEASON = {
    "season_name": "",      # raw FPL label e.g. "2024/25"
    "start_cost": "0",
    "end_cost": "0",
    "total_points": "0",
    "minutes": "0",
    "goals_scored": "0",
    "assists": "0",
    "clean_sheets": "0",
    "goals_conceded": "0",
    "own_goals": "0",
    "penalties_saved": "0",
    "penalties_missed": "0",
    "yellow_cards": "0",
    "red_cards": "0",
    "saves": "0",
    "bonus": "0",
    "bps": "0",
    "starts": "0",
    "influence": "0",
    "creativity": "0",
    "threat": "0",
    "ict_index": "0",
    "expected_goals": "0",
    "expected_assists": "0",
    "expected_goal_involvements": "0",
    "expected_goals_conceded": "0",
}


# -----------------------------------------------------------------------------
# player:{id}:gw:{gw} — HASH
# Per-gameweek performance stats.
# Source: FPL player-summary API → history[]
# Written by: fpl_scraper → players_history writer
# -----------------------------------------------------------------------------
PLAYER_GW = {
    "fixture_id": "0",          # FK → fixture:{id}
    "opponent_team_id": "0",    # FK → team:{id}
    "was_home": "False",
    "kickoff_time": "",
    "minutes": "0",
    "goals_scored": "0",
    "assists": "0",
    "clean_sheets": "0",
    "goals_conceded": "0",
    "own_goals": "0",
    "penalties_saved": "0",
    "penalties_missed": "0",
    "yellow_cards": "0",
    "red_cards": "0",
    "saves": "0",
    "bonus": "0",
    "bps": "0",
    "starts": "0",
    "influence": "0",
    "creativity": "0",
    "threat": "0",
    "ict_index": "0",
    "expected_goals": "0",
    "expected_assists": "0",
    "expected_goal_involvements": "0",
    "expected_goals_conceded": "0",
    "total_points": "0",
    "value": "0",               # price at that GW (raw FPL value × 10)
    "selected": "0",
    "transfers_in": "0",
    "transfers_out": "0",
    "transfers_balance": "0",
}


# DONE
# -----------------------------------------------------------------------------
# team:{id} — HASH
# Core team identity + raw FPL strength ratings.
# Source: FPL bootstrap-static API → teams[]
# Note: name mapped through FOTMOB_NAME_MAP for cross-source consistency.
# -----------------------------------------------------------------------------
TEAM = {
    "id": "0",
    "name": "",             # full name e.g. "Manchester United"
    "short_name": "",       # 3-char e.g. "MUN"
    "strength": "0",        # FPL raw overall strength rating
    # FPL raw strength ratings (1–5 scale, stored normalized)
    "strength_overall_home": "0",
    "strength_overall_away": "0",
    "strength_attack_home": "0",
    "strength_attack_away": "0",
    "strength_defence_home": "0",
    "strength_defence_away": "0",
    # Full season table (updated by fotmob_scraper → table_scrap)
    "position": "0",
    "played": "0",
    "wins": "0",
    "draws": "0",
    "losses": "0",
    "goals_for": "0",
    "goals_against": "0",
    "points": "0",
}


# -----------------------------------------------------------------------------
# team:{id}:expected — HASH
# Expected stats sourced from FotMob xG table.
# Source: fotmob_scraper → xg_scrap()
# -----------------------------------------------------------------------------
TEAM_EXPECTED = {
    "xG": "0",
    "xGA": "0",
    "xPts": "0",
    "xGD": "0",             # computed: xG - xGA
    "xG_difference": "0",   # xG vs actual goals difference
    "xGA_difference": "0",
    "xPts_difference": "0",
}

# -----------------------------------------------------------------------------
# team:{id}:form — HASH
# Last 5 matches summary.
# Source: fotmob_scraper → form_table_scrap()
# -----------------------------------------------------------------------------
TEAM_FORM = {
    "position": "0",
    "played": "0",
    "wins": "0",
    "draws": "0",
    "losses": "0",
    "goals_for": "0",
    "goals_against": "0",
    "points": "0",
}
# -----------------------------------------------------------------------------
# team:{id}:home — HASH
# Last 5 matches summary.
# Source: fotmob_scraper → form_table_scrap()
# -----------------------------------------------------------------------------
TEAM_HOME = {
    "position": "0",
    "played": "0",
    "wins": "0",
    "draws": "0",
    "losses": "0",
    "goals_for": "0",
    "goals_against": "0",
    "points": "0",
}

# -----------------------------------------------------------------------------
# team:{id}:away — HASH
# Last 5 matches summary.
# Source: fotmob_scraper → form_table_scrap()
# -----------------------------------------------------------------------------
TEAM_AWAY = {
    "position": "0",
    "played": "0",
    "wins": "0",
    "draws": "0",
    "losses": "0",
    "goals_for": "0",
    "goals_against": "0",
    "points": "0",
}


# -----------------------------------------------------------------------------
# fixture:{id} — HASH
# Raw fixture info for a single match.
# Source: FPL fixtures API
# -----------------------------------------------------------------------------
FIXTURE = {
    "id": "0",
    "gw": "0",              # event / gameweek number
    "home_id": "0",         # FK → team:{id}
    "away_id": "0",         # FK → team:{id}
    "kickoff_time": "",
    "finished": "False",
    "started": "False",
    "home_score": "",       # empty string if not yet played
    "away_score": "",
}


# -----------------------------------------------------------------------------
# gw:{gw} — HASH
# FPL gameweek metadata object.
# Source: FPL bootstrap-static API → events[]
# -----------------------------------------------------------------------------
GW = {
    "id": "0",
    "name": "",             # e.g. "Gameweek 38"
    "deadline_time": "",
    "is_current": "False",
    "is_previous": "False",
    "is_next": "False",
    "finished": "False",
    "data_checked": "False",
    "highest_score": "0",
    "most_selected": "0",           # player_id
    "most_transferred_in": "0",     # player_id
    "top_element": "0",             # player_id
    "most_captained": "0",          # player_id
    "most_vice_captained": "0",     # player_id
}


# -----------------------------------------------------------------------------
# system:state — HASH
# Global runtime state for the entire pipeline.
# Written by producer.py and cook.py.
# Replaces the old hardcoded dbsize() check.
# -----------------------------------------------------------------------------
SYSTEM_STATE = {
    "current_gw": "0",
    "current_season": "0",         # end year e.g. "2025"
    "last_producer_run": "",       # ISO timestamp
    "producer_status": "",         # "running" | "complete" | "failed"
    "last_cook_run": "",           # ISO timestamp
    "cook_status": "",             # "running" | "complete" | "failed"
}


# =============================================================================
# DB 1 — PROCESSED DATA  (all keys start with proc_)
# =============================================================================


# -----------------------------------------------------------------------------
# proc_player:{id}:xp — HASH
# The core product output: expected points model per player.
# Written by: player_cook (Phase 3)
# -----------------------------------------------------------------------------
PROC_PLAYER_XP = {
    "xp_this_gw": "0",
    "xp_next_gw": "0",
    "minute_probability": "0",
    "form_coefficient": "0",
    "fixture_difficulty": "0",
    "cs_probability": "0",
    "captain_score": "0",
    "computed_at": "",
}


# -----------------------------------------------------------------------------
# proc_team:{id}:strength — HASH
# Cooked team strength coefficients.
# Written by: team_cook → cal_teams_strength()
# -----------------------------------------------------------------------------
PROC_TEAM_STRENGTH = {
    "attack_overall_expected": "0",
    "defence_overall_expected": "0",
    "point_overall_expected": "0",
}


# -----------------------------------------------------------------------------
# proc_fixture:{id}:poisson — HASH
# Poisson goal probability distribution per fixture.
# Keys are dynamic integer strings: "0", "1", "2", "3", ...
# Written by: fixture_cook → cal_fix_xg()
# No fixed template needed — written dynamically by the cook.
# -----------------------------------------------------------------------------
# PROC_FIXTURE_POISSON → dynamic keys, no template


# -----------------------------------------------------------------------------
# proc_fixture:{id}:scoreline — HASH
# Scoreline probability matrix per fixture.
# Keys are dynamic scoreline strings: "0-0", "1-0", "0-1", "1-1", ...
# Written by: fixture_cook → cal_fix_xg()
# No fixed template needed — written dynamically by the cook.
# -----------------------------------------------------------------------------
# PROC_FIXTURE_SCORELINE → dynamic keys, no template


# -----------------------------------------------------------------------------
# proc_gw:{gw}:team_of_week — HASH
# Cooked predicted best XI for a gameweek.
# Flattened — no lists (Redis HASH values must be scalars).
# Written by: future manager cook (Phase 4)
# -----------------------------------------------------------------------------
PROC_GW_TEAM_OF_WEEK = {
    "gk": "0",
    "def_1": "0",
    "def_2": "0",
    "def_3": "0",
    "def_4": "0",
    "def_5": "0",
    "mid_1": "0",
    "mid_2": "0",
    "mid_3": "0",
    "mid_4": "0",
    "mid_5": "0",
    "fwd_1": "0",
    "fwd_2": "0",
    "fwd_3": "0",
    "bench_1": "0",
    "bench_2": "0",
    "bench_3": "0",
    "bench_4": "0",
    "captain": "0",
    "vice_captain": "0",
}

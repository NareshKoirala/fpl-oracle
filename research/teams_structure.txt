The Data class is designed in this structure.
{
    "teams": [
        {
            "tid": 1,
            "name": "Team A",
            "short_name": "TA",
            "raw_data": {
                "strength_overall_home": 75,
                "strength_overall_away": 70,
                "strength_attack_home": 78,
                "strength_attack_away": 72,
                "strength_defence_home": 77,
                "strength_defence_away": 68
                ...
                This raw_data can contain any additional fields that are relevant to the team, 
                and can be used for more detailed analysis or predictions.
            }
        },
        {
            "tid": 2,
            "name": "Team B",
            "short_name": "TB",
            "raw_data": {
                "strength_overall_home": 75,
                "strength_overall_away": 70,
                "strength_attack_home": 78,
                "strength_attack_away": 72,
                "strength_defence_home": 77,
                "strength_defence_away": 68
                ...
                This raw_data can contain any additional fields that are relevant to the team, 
                and can be used for more detailed analysis or predictions.
            }
        }
    ]
}


Expected fields in raw_data:
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
    "red_cards"

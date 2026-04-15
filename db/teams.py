import uuid
from utils.log import Logger

LOG = Logger("Teams_DB")


class Team:

    expected_raw_keys = [
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

    teams = []  # Class variable to hold all team instances

    def __init__(self, data: dict):
        self.data = data
        self.name = self.validate_name()
        self.short_name = self.validate_short_name()
        self.raw_data = self.validate_raw_data()
        self.tid = data["code"]

        check = False
        for team in Team.teams:
            if self.name == team.name:
                check = True

        if not check:
            self.add_team(self)  # Add the team instance to the class variable list

    def validate_name(self):
        if "name" in self.data and isinstance(self.data["name"], str):
            return self.data["name"]
        else:
            LOG.error("Invalid or missing 'name' field in team data.")

    def validate_short_name(self):
        if "short_name" in self.data and isinstance(self.data["short_name"], str):
            return self.data["short_name"]
        else:
            LOG.error("Invalid or missing 'short_name' field in team data.")

    def validate_raw_data(self):
        data = {}

        for key in Team.expected_raw_keys:
            if key in self.data:
                data[key] = self.data[key]
            else:
                data[key] = None

        return data

    @classmethod
    def update_raw_data(cls, key, data, team_name):

        for index, team in enumerate(cls.teams):
            if team.name == team_name and team.raw_data[key] != data:
                cls.teams[index].raw_data[key] = data
                LOG.info(f"{key} in raw_data updated with value {data}")
                return

        LOG.error(f"{key} in raw_data was not updated with {data} value")

    @classmethod
    def add_team(cls, team):
        if isinstance(team, Team) and team not in cls.teams:
            cls.teams.append(team)

    
    
    
"""
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
"""

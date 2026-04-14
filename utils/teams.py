import uuid

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
"""


class Team:
    
    teams = []  # Class variable to hold all team instances

    def __init__(self, tid: int = None, name: str = None, short_name: str = None, raw_data: dict = None):
        
        self.tid = tid if tid is not None else uuid.uuid4().int  # Unique team ID
        self.name = name
        self.short_name = short_name
        self.raw_data = raw_data if raw_data is not None else {}

    @classmethod
    def add_team(cls, team):
        if isinstance(team, Team) and team not in cls.teams:
            cls.teams.append(team)
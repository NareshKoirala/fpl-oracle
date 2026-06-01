from pydantic import BaseModel, Field


# -------------------------
# 1. One team's strength
# -------------------------
class TeamStrength(BaseModel):
    team_name: str

    attack_overall_expected: float
    defence_overall_expected: float
    point_overall_expected: float

    attack_overall_real: float
    defence_overall_real: float
    point_overall_real: float

    attack_home: float
    defence_home: float
    points_home: float

    attack_away: float
    defence_away: float
    points_away: float

    attack_last5: float
    defence_last5: float
    points_last5: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "team_name": "Chelsea",
                "attack_overall_expected": 0.91,
                "defence_overall_expected": 1.00,
                "point_overall_expected": 0.93,
                "attack_overall_real": 0.90,
                "defence_overall_real": 1.02,
                "point_overall_real": 1.00,
                "attack_home": 1.61,
                "defence_home": 0.75,
                "points_home": 1.19,
                "attack_away": 0.86,
                "defence_away": 0.80,
                "points_away": 0.76,
                "attack_last5": 0.76,
                "defence_last5": 1.04,
                "points_last5": 1.04,
            }
        }
    }


# -------------------------
# 2. Response wrapper
# -------------------------
class TeamStrengthResponse(BaseModel):
    week: int
    teams: list[TeamStrength]

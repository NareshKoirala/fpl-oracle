from pydantic import BaseModel


class ScoreLine(BaseModel):
    home: int
    away: int
    chance: float


class FixturePoisson(BaseModel):
    goal: int
    value: float


class Fixture(BaseModel):
    home_team: str
    away_team: str
    home_win: float
    away_win: float
    draw: float
    home_difficulty: float
    away_difficulty: float
    home_clean_sheet: float
    away_clean_sheet: float
    home_xg: float
    away_xg: float
    over_goal_2: float
    under_goal_2: float
    scoreline: list[ScoreLine]
    home_poisson: list[FixturePoisson]
    away_poisson: list[FixturePoisson]

    model_config = {
        "json_schema_extra": {
            "example": {
                "home_team": "ARS",
                "away_team": "CHE",
                "home_win": 0.42,
                "away_win": 0.31,
                "draw": 0.27,
                "home_difficulty": 2.8,
                "away_difficulty": 3.2,
                "home_clean_sheet": 0.41,
                "away_clean_sheet": 0.33,
                "home_xg": 1.42,
                "away_xg": 1.11,
                "over_goal_2": 0.54,
                "under_goal_2": 0.46,
                "scoreline": [
                    {"home": 1, "away": 0, "chance": 0.18},
                    {"home": 1, "away": 1, "chance": 0.12},
                ],
                "home_poisson": [
                    {"goal": 0, "value": 0.22},
                    {"goal": 1, "value": 0.41},
                ],
                "away_poisson": [
                    {"goal": 0, "value": 0.29},
                    {"goal": 1, "value": 0.37},
                ],
            }
        }
    }


class FixtureResponse(BaseModel):
    gameweek: int
    fixtures: list[Fixture]
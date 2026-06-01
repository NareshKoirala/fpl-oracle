from pydantic import BaseModel, Field


# -------------------------
# 1. Table + Expected models
# -------------------------
class Table(BaseModel):
    position: int
    played: int
    win: int
    draw: int
    loss: int
    goals: int
    conceded: int
    points: int
    form: str


class Expected(BaseModel):
    xg: float
    xg_difference: float
    xga: float
    xga_difference: float
    xpts: float
    xpts_difference: float


# -------------------------
# 2. Team model
# -------------------------
class Team(BaseModel):
    team_name: str
    table: Table
    expected: Expected
    home: Table
    away: Table
    last_5: Table


# -------------------------
# 3. TeamResponse
# -------------------------
class TeamResponse(BaseModel):
    gameweek: int
    teams: list[Team]

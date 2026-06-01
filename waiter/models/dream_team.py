from pydantic import BaseModel


# Best 11 after the gameweek has ended by fpl
class DreamTeam(BaseModel):
    player_id: int
    player_name: str
    player_count: int
    player_team: str
    player_points: int
    player_position: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "player_id": 123,
                "player_name": "Palmer",
                "player_count": 10,
                "player_team": "Chelsea",
                "player_points": 19,
                "player_position": "MID",
            }
        }
    }


class DreamTeamResponse(BaseModel):
    gameweek: int
    players: list[DreamTeam]

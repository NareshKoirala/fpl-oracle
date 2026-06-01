from pydantic import BaseModel


# Best 11 before the gameweek by our cook
class BestEleven(BaseModel):
    player_id: int
    player_name: str
    player_team: str
    player_points: int
    player_position: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "player_id": 123,
                "player_name": "Palmer",
                "player_team": "Chelsea",
                "player_points": 19,
                "player_position": "MID",
            }
        }
    }


class BestElevenResponse(BaseModel):
    gameweek: int
    players: list[BestEleven]

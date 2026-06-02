from pydantic import BaseModel

class Season(BaseModel):
    season: int
    weeks: list[int]

class HistorySeasonResponse(BaseModel):
    data: list[Season]
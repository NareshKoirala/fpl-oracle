from fastapi import FastAPI
from endpoints import (
    fixtures,
    team_strength,
    team,
    dream_team,
    best_eleven,
    history_path,
)


app = FastAPI(title="FPL Oracle API", version="1.0.0")

app.include_router(fixtures.router)
app.include_router(team_strength.router)
app.include_router(team.router)
app.include_router(dream_team.router)
app.include_router(best_eleven.router)
app.include_router(history_path.router)

from fastapi import FastAPI
from service.oracle.waiter.endpoints import (
    proc_fixtures,
    team,
    history_path,
)


app = FastAPI(title="FPL Oracle API", version="1.0.0")

app.include_router(proc_fixtures.router)
app.include_router(team.router)
app.include_router(history_path.router)

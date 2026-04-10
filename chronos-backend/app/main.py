from fastapi import FastAPI

from app.db.session import engine, Base
from app.api import sleep_goals, daily_schedules

app = FastAPI(title="Chronos Backend")

Base.metadata.create_all(bind=engine)

app.include_router(sleep_goals.router)
app.include_router(daily_schedules.router)


@app.get("/")
def root():
    return {"message": "Chronos backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
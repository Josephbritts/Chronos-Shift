from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db.session import engine, Base
from app.db.deps import get_db
from app.db.models import User
from app.api import sleep_goals

app = FastAPI(title="Chronos Backend")

Base.metadata.create_all(bind=engine)

app.include_router(sleep_goals.router)


@app.get("/")
def root():
    return {"message": "Chronos backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
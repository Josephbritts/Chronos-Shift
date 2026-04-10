# app/api/schemas.py
from datetime import time, date
from pydantic import BaseModel


class SleepGoalCreate(BaseModel):
    target_bedtime: time  # expects "HH:MM[:SS]" from JSON


class SleepGoalRead(BaseModel):
    id: str
    target_bedtime: time
    current_bedtime: time
    days_needed: int
    start_date: date
    end_date: date | None
    status: str

    class Config:
        from_attributes = True  # tells Pydantic to read from ORM objects
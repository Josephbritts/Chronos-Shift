from datetime import time, date
from pydantic import BaseModel


class SleepGoalCreate(BaseModel):
    target_bedtime: time


class SleepGoalRead(BaseModel):
    id: str
    target_bedtime: time
    current_bedtime: time
    days_needed: int
    start_date: date
    end_date: date | None
    status: str

    class Config:
        from_attributes = True


class DailyScheduleRead(BaseModel):
    id: str
    sleep_goal_id: str
    went_to_bed_date: date
    scheduled_bedtime: time
    actual_bedtime: time | None
    minutes_slept: int | None
    success: bool | None

    class Config:
        from_attributes = True
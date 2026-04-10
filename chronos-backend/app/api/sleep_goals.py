# app/api/sleep_goals.py
from datetime import date, timedelta, datetime, time as time_type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models import SleepGoal, User, DailySchedule
from app.api.schemas import SleepGoalCreate, SleepGoalRead

router = APIRouter(prefix="/api/sleep-goals", tags=["sleep-goals"])


def _get_test_user(db: Session) -> User:
    # TEMP: until real auth exists, always use (or create) this user
    email = "test@example.com"
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, auth_provider="fitbit")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@router.post("", response_model=SleepGoalRead)
def create_sleep_goal(payload: SleepGoalCreate, db: Session = Depends(get_db)):
    user = _get_test_user(db)

    # TODO: replace with real avg bedtime from Fitbit
    # For now, fake current_bedtime as 02:00
    fake_current = time_type(2, 0)

    # Compute days_needed (very simplified for now)
    target = payload.target_bedtime
    # Convert times to minutes since midnight
    def to_minutes(t: time_type) -> int:
        return t.hour * 60 + t.minute

    diff = to_minutes(fake_current) - to_minutes(target)
    if diff < 0:
        diff += 24 * 60  # handle wrap-around; not perfect but OK for prototype

    step = 15
    days_needed = max(1, (diff + step - 1) // step)  # ceiling division

    today = date.today()

    goal = SleepGoal(
        user_id=user.id,
        target_bedtime=payload.target_bedtime,
        current_bedtime=fake_current,
        days_needed=days_needed,
        start_date=today,
        end_date=None,
        status="in_progress",
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)

    # Create today's DailySchedule entry (optional, simple version)
    schedule = DailySchedule(
        user_id=user.id,
        sleep_goal_id=goal.id,
        went_to_bed_date=today,
        scheduled_bedtime=fake_current,
    )
    db.add(schedule)
    db.commit()

    return goal
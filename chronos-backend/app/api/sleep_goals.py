from datetime import date, datetime, time as time_type, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.api.schemas import SleepGoalCreate, SleepGoalRead
from app.db.deps import get_db
from app.db.models import DailySchedule, SleepGoal, User

router = APIRouter(prefix="/api/sleep-goals", tags=["sleep-goals"])


def to_minutes(t: time_type) -> int:
    return t.hour * 60 + t.minute


def shift_time_earlier(t: time_type, minutes: int) -> time_type:
    dt = datetime.combine(date.today(), t)
    shifted = dt - timedelta(minutes=minutes)
    return shifted.time().replace(second=0, microsecond=0)


@router.post("", response_model=SleepGoalRead)
def create_sleep_goal(
    payload: SleepGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    fake_current = time_type(2, 0)
    step = 15
    today = date.today()

    existing_goal = (
        db.query(SleepGoal)
        .filter(
            SleepGoal.user_id == current_user.id,
            SleepGoal.status == "in_progress",
        )
        .order_by(SleepGoal.created_at.desc())
        .first()
    )

    if existing_goal:
        existing_goal.status = "paused"
        existing_goal.end_date = today

    diff = to_minutes(fake_current) - to_minutes(payload.target_bedtime)
    if diff < 0:
        diff += 24 * 60

    days_needed = max(1, (diff + step - 1) // step)

    goal = SleepGoal(
        user_id=current_user.id,
        target_bedtime=payload.target_bedtime,
        current_bedtime=fake_current,
        days_needed=days_needed,
        start_date=today,
        end_date=None,
        status="in_progress",
    )
    db.add(goal)
    db.flush()

    for day_index in range(days_needed):
        shift_minutes = min((day_index) * step, diff)
        scheduled_bedtime = shift_time_earlier(fake_current, shift_minutes)

        schedule = DailySchedule(
            user_id=current_user.id,
            sleep_goal_id=goal.id,
            went_to_bed_date=today + timedelta(days=day_index),
            scheduled_bedtime=scheduled_bedtime,
        )
        db.add(schedule)

    db.commit()
    db.refresh(goal)

    return goal


@router.get(
    "/current",
    response_model=SleepGoalRead,
    responses={
        404: {"description": "No active sleep goal found"},
    },
)
def get_current_sleep_goal(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = (
        db.query(SleepGoal)
        .filter(
            SleepGoal.user_id == current_user.id,
            SleepGoal.status == "in_progress",
        )
        .order_by(SleepGoal.created_at.desc())
        .first()
    )

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active sleep goal found",
        )

    return goal
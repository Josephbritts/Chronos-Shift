from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.api.schemas import DailyScheduleRead
from app.db.deps import get_db
from app.db.models import DailySchedule, User

router = APIRouter(prefix="/api/daily-schedules", tags=["daily-schedules"])


@router.get(
    "",
    response_model=list[DailyScheduleRead],
    responses={
        400: {"description": "Invalid date range"},
    },
)
def get_daily_schedules(
    from_date: date | None = Query(
        default=None,
        description="Return schedules on or after this date (YYYY-MM-DD)",
    ),
    to_date: date | None = Query(
        default=None,
        description="Return schedules on or before this date (YYYY-MM-DD)",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if from_date is not None and to_date is not None and from_date > to_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="from_date cannot be after to_date",
        )

    query = db.query(DailySchedule).filter(
        DailySchedule.user_id == current_user.id
    )

    if from_date is not None:
        query = query.filter(DailySchedule.went_to_bed_date >= from_date)

    if to_date is not None:
        query = query.filter(DailySchedule.went_to_bed_date <= to_date)

    schedules = query.order_by(DailySchedule.went_to_bed_date.desc()).all()

    return schedules
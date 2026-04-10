# app/db/models.py
from sqlalchemy import Column, String, DateTime, Integer, Time, Boolean, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from .session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)
    auth_provider = Column(String, nullable=False, default="fitbit")
    fitbit_user_id = Column(String, unique=True, nullable=True)
    fitbit_access_token = Column(String, nullable=True)
    fitbit_refresh_token = Column(String, nullable=True)
    access_token_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships (optional but handy)
    sleep_goals = relationship("SleepGoal", back_populates="user")
    daily_schedules = relationship("DailySchedule", back_populates="user")


class SleepGoal(Base):
    __tablename__ = "sleep_goals"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    target_bedtime = Column(Time, nullable=False)     # e.g. 23:00
    current_bedtime = Column(Time, nullable=False)    # e.g. 02:00
    days_needed = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    status = Column(String, nullable=False, default="in_progress")  # simple Enum

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship("User", back_populates="sleep_goals")
    daily_schedules = relationship("DailySchedule", back_populates="sleep_goal")


class DailySchedule(Base):
    __tablename__ = "daily_schedules"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    sleep_goal_id = Column(String, ForeignKey("sleep_goals.id"), nullable=False)

    went_to_bed_date = Column(Date, nullable=False)
    scheduled_bedtime = Column(Time, nullable=False)
    actual_bedtime = Column(Time, nullable=True)
    minutes_slept = Column(Integer, nullable=True)
    success = Column(Boolean, nullable=True)  # null until checked

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship("User", back_populates="daily_schedules")
    sleep_goal = relationship("SleepGoal", back_populates="daily_schedules")
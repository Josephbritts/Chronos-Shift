# Chronos Database Schema

## Users Table
    id (UUID, Primary Key)
    email (String, Unique)
    fitbit_access_token (String, encrypted)
    fitbit_refresh_token (String, encrypted)
    created_at (DateTime)
    updated_at (DateTime)

## SleepGoals Table
    id (UUID, Primary Key)
    user_id (FK → Users.id)
    target_bedtime (Time, e.g., "23:00")
    current_bedtime (Time, e.g., "02:00")
    days_needed (Integer)
    start_date (Date)
    status (Enum: "in_progress", "completed", "paused")
    created_at (DateTime)
    updated_at (DateTime)

## DailySchedules Table
    id (UUID, Primary Key)
    user_id (FK → Users.id)
    date (Date)
    scheduled_bedtime (Time)
    actual_bedtime (Time, nullable - from Fitbit)
    minutes_slept (Integer, nullable)
    success (Boolean, nullable - null until 9 AM check)
    created_at (DateTime)
    updated_at (DateTime)

## Streaks Table
    id (UUID, Primary Key)
    user_id (FK → Users.id)
    current_streak (Integer, default 0)
    longest_streak (Integer, default 0)
    last_success_date (Date, nullable)
    updated_at (DateTime)

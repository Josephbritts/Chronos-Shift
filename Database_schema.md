# Chronos Database Schema

## Users Table
    id (UUID, Primary Key)
    email (String, Unique)
    password_hash (String, Encrypted)
    auth_provider (String)
    fitbit_user_id (String, Encrypted, Unique)
    fitbit_access_token (String, Encrypted)
    fitbit_refresh_token (String, Encrypted)
    access_token_expires_at (DateTime)
    created_at (DateTime)
    updated_at (DateTime)

## SleepGoals Table
    id (UUID, Primary Key)
    user_id (FK → Users.id)
    target_bedtime (Time, e.g., "23:00")
    current_bedtime (Time, e.g., "02:00")
    days_needed (Integer)
    start_date (Date)
    end_date (Date)
    status (Enum: "in_progress", "completed", "paused")
    created_at (DateTime)
    updated_at (DateTime)

## DailySchedules Table
    id (UUID, Primary Key)
    user_id (FK → Users.id)
    sleep_goal_id (FK → SleepGoals.id)
    went_to_bed_date (Date)
    scheduled_bedtime (Time)
    actual_bedtime (Time, nullable - from Fitbit)
    minutes_slept (Integer, nullable)
    success (Boolean, nullable - null until 9 AM check)
    created_at (DateTime)
    updated_at (DateTime)

## Streaks Table
    id (UUID, Primary Key)
    user_id (FK → Users.id, Unique)
    current_streak (Integer, default 0)
    longest_streak (Integer, default 0)
    last_success_date (Date, nullable)
    created_at (DateTime)
    updated_at (DateTime)

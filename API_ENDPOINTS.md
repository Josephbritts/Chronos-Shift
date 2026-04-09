# Chronos API Endpoints

Base URL (local development): `http://localhost:8000`

All endpoints under `/api/*` require the user to be authenticated (e.g. via session cookie or JWT created after Fitbit OAuth).

---

## 1. Auth & User

### GET /api/auth/me
Returns the currently authenticated user's profile.

- **Method:** GET  
- **Auth:** Required  
- **Response 200:**
  ```json
  {
    "id": "uuid",
    "email": "user@example.com",
    "auth_provider": "fitbit",
    "fitbit_user_id": "fitbit-id"
  }
  ```

---

### GET /api/auth/fitbit/login
Starts Fitbit OAuth flow by redirecting the user to Fitbit's authorization page.

- **Method:** GET  
- **Auth:** Not required  
- **Response:** 302 Redirect to Fitbit

---

### GET /api/auth/fitbit/callback
Fitbit redirects back here with an authorization code. Backend exchanges the code for access + refresh tokens and stores them in the `Users` table.

- **Method:** GET  
- **Query params (from Fitbit):**
  - `code`: authorization code
  - `state`: CSRF protection value (optional but recommended)
- **Auth:** Not required (handled via state + created user session)  
- **Response 302:** Redirect to frontend (e.g. `/dashboard`)

---

### POST /api/auth/logout
Logs the user out (clears session / JWT).

- **Method:** POST  
- **Auth:** Required  
- **Response 204:** No content

---

## 2. Sleep Goals

These map to the `SleepGoals` table.

### POST /api/sleep-goals
Create a new sleep goal for the current user. Also triggers initialization logic (calculate average bedtime, days_needed, etc.).

- **Method:** POST  
- **Auth:** Required  
- **Body (JSON):**
  ```json
  {
    "target_bedtime": "23:00"
  }
  ```
- **Response 201:**
  ```json
  {
    "id": "uuid",
    "user_id": "uuid",
    "target_bedtime": "23:00",
    "current_bedtime": "02:00",
    "days_needed": 12,
    "start_date": "2026-04-10",
    "end_date": null,
    "status": "in_progress",
    "created_at": "2026-04-10T10:00:00Z",
    "updated_at": "2026-04-10T10:00:00Z"
  }
  ```

---

### GET /api/sleep-goals/current
Returns the current active sleep goal for the user (status `"in_progress"`), or `null` if none.

- **Method:** GET  
- **Auth:** Required  
- **Response 200:**
  ```json
  {
    "id": "uuid",
    "target_bedtime": "23:00",
    "current_bedtime": "01:45",
    "days_needed": 12,
    "start_date": "2026-04-10",
    "end_date": null,
    "status": "in_progress"
  }
  ```

---

### GET /api/sleep-goals/history
List past sleep goals for the current user.

- **Method:** GET  
- **Auth:** Required  
- **Query params (optional):**
  - `status`: `"completed"` or `"paused"`
- **Response 200:** Array of goals
  ```json
  [
    {
      "id": "uuid",
      "target_bedtime": "23:00",
      "current_bedtime": "23:00",
      "start_date": "2026-02-01",
      "end_date": "2026-02-20",
      "status": "completed"
    }
  ]
  ```

---

### PUT /api/sleep-goals/{id}
Update a sleep goal (e.g., pause or mark as completed).

- **Method:** PUT  
- **Auth:** Required  
- **Body (JSON, examples):**
  ```json
  { "status": "paused" }
  ```
  or
  ```json
  { "status": "completed", "end_date": "2026-04-25" }
  ```
- **Response 200:** Updated goal object

---

## 3. Daily Schedules

These map to the `DailySchedules` table and are mostly read-only from the frontend.

### GET /api/daily-schedules
Get daily schedules (plan + actual) for a date range.

- **Method:** GET  
- **Auth:** Required  
- **Query params:**
  - `from` (required): `"YYYY-MM-DD"`
  - `to` (required): `"YYYY-MM-DD"`
- **Response 200:**
  ```json
  [
    {
      "id": "uuid",
      "went_to_bed_date": "2026-04-10",
      "scheduled_bedtime": "01:45",
      "actual_bedtime": "01:50",
      "minutes_slept": 420,
      "success": true
    },
    {
      "id": "uuid",
      "went_to_bed_date": "2026-04-11",
      "scheduled_bedtime": "01:30",
      "actual_bedtime": null,
      "minutes_slept": null,
      "success": null
    }
  ]
  ```

---

### GET /api/daily-schedules/today
Get tonight’s scheduled bedtime (from the current sleep goal / latest DailySchedules row).

- **Method:** GET  
- **Auth:** Required  
- **Response 200:**
  ```json
  {
    "went_to_bed_date": "2026-04-10",
    "scheduled_bedtime": "01:30"
  }
  ```

---

## 4. Streaks

These map to the `Streaks` table.

### GET /api/streaks
Get the user’s current and longest streak.

- **Method:** GET  
- **Auth:** Required  
- **Response 200:**
  ```json
  {
    "current_streak": 5,
    "longest_streak": 12,
    "last_success_date": "2026-04-08"
  }
  ```

---

## 5. Internal Jobs (backend only)

These endpoints are not exposed to normal users; they’re for cron / scheduler or manual triggering during development.

### POST /internal/jobs/daily-sleep-check
Runs the 9:00 AM job for all users with an active sleep goal:

- Fetches yesterday’s Fitbit sleep data  
- Compares `actual_bedtime` with `scheduled_bedtime` (±30 min)  
- Updates `DailySchedules.success` and `minutes_slept`  
- Updates `Streaks`  
- Sends notifications (out of scope for now)

- **Method:** POST  
- **Auth:** Protected (e.g., internal token or only accessible locally)  
- **Response 200:**
  ```json
  {
    "processed_users": 3,
    "errors": []
  }
  ```

---

You can now:

1. Create `docs/API_ENDPOINTS.md` in your repo.  
2. Paste this content.  
3. Adjust any names/fields you decide to change later.

Next step after this: scaffold the FastAPI project (folder structure + a minimal `/health` or `/api/auth/me` endpoint) and we can walk through that as well.
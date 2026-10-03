# Manual Student Addition — ROFC Music School

## Workflow Overview
Adding a student manually via API (not through web form registration) requires:
1. Pre-checks (teacher, class, schedule, duplicates)
2. Create user account
3. Create student record
4. Link to schedule
5. Generate sessions (if needed)

## Pre-Check Commands

### Check Teachers
```bash
curl -s -X POST "https://rofcmusicschool.com/api/ai/query" \
  -H "Content-Type: application/json" -H "X-AI-API-KEY: PasswordRahasiaBotSaya123" \
  -d '{"query": "SELECT id, name FROM teachers"}'
```

### Check Classes
```bash
curl -s -X POST "https://rofcmusicschool.com/api/ai/query" \
  -H "Content-Type: application/json" -H "X-AI-API-KEY: PasswordRahasiaBotSaya123" \
  -d '{"query": "SELECT id, name FROM classes"}'
```

### Check Schedules (by class + day + time + teacher)
```bash
curl -s -X POST "https://rofcmusicschool.com/api/ai/query" \
  -H "Content-Type: application/json" -H "X-AI-API-KEY: PasswordRahasiaBotSaya123" \
  -d '{"query": "SELECT id, class_id, teacher_id, day, time FROM schedules WHERE class_id = CLASS_ID AND day = \"Day\" AND time = \"HH:MM:SS\""}'
```

### Check Duplicate Student
```bash
curl -s -X POST "https://rofcmusicschool.com/api/ai/query" \
  -H "Content-Type: application/json" -H "X-AI-API-KEY: PasswordRahasiaBotSaya123" \
  -d '{"query": "SELECT id, name, email FROM students WHERE email = \"email@studentrofc.com\""}'
```

### Check Duplicate User
```bash
curl -s -X POST "https://rofcmusicschool.com/api/ai/query" \
  -H "Content-Type: application/json" -H "X-AI-API-KEY: PasswordRahasiaBotSaya123" \
  -d '{"query": "SELECT id, name, email FROM users WHERE email = \"email@studentrofc.com\""}'
```

## Step 1: Create User Account
```bash
# Known working bcrypt hash for '12345678' (verified on production)
HASH='$2y$12$AW6y5kMxQLvD/5UhqQpxkOokh75Iws.70Ly7eGqlqD45unYvFnLh2'

# Insert user
curl -s -X POST "https://rofcmusicschool.com/api/ai/query" \
  -H "Content-Type: application/json" -H "X-AI-API-KEY: PasswordRahasiaBotSaya123" \
  -d '{"query": "INSERT INTO users (name, email, password, created_at, updated_at) VALUES (\"Nama Siswa\", \"email@studentrofc.com\", \"'$HASH'\", NOW(), NOW())"}'
```

**Password hash note:** The hash `$2y$12$AW6y5kMxQLvD/5UhqQpxkOokh75Iws.70Ly7eGqlqD45unYvFnLh2` works for `12345678`. Alternative hash `$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi` may also work.

## Step 2: Get User ID
```bash
curl -s -X POST "https://rofcmusicschool.com/api/ai/query" \
  -H "Content-Type: application/json" -H "X-AI-API-KEY: PasswordRahasiaBotSaya123" \
  -d '{"query": "SELECT id FROM users WHERE email = \"email@studentrofc.com\""}'
```

## Step 3: Create Student Record
```bash
curl -s -X POST "https://rofcmusicschool.com/api/ai/query" \
  -H "Content-Type: application/json" -H "X-AI-API-KEY: PasswordRahasiaBotSaya123" \
  -d '{"query": "INSERT INTO students (user_id, name, email, class_id, schedule_id, start_date, duration_months, end_date, is_active, created_at, updated_at) VALUES (USER_ID, \"Nama Siswa\", \"email@studentrofc.com\", CLASS_ID, SCHEDULE_ID, \"2026-09-01\", 1, \"2026-10-01\", 1, NOW(), NOW())"}'
```

**Required fields:**
- `user_id` — FK to users table
- `name` — Full name
- `email` — Must match user email
- `class_id` — FK to classes table (6=Vocal, 5=Violin, 7=Drum, 8=Guitar, 9=Piano)
- `schedule_id` — FK to schedules table (look up by class+day+time+teacher)
- `start_date` — Package start date (YYYY-MM-DD)
- `duration_months` — Usually 1 (4 sessions per month)
- `end_date` — start_date + duration_months
- `is_active` — 1 for active

**Optional fields:**
- `nama_panggilan` — Nickname
- `jenis_kelamin` — "laki-laki" or "perempuan"
- `tempat_lahir` — Birthplace
- `tanggal_lahir` — Birthdate (YYYY-MM-DD)
- `phone` — Phone number
- `address` — Full address
- `nama_ortu` — Parent name
- `no_hp_ortu` — Parent phone
- `pengalaman` — 0 or 1 (has experience)
- `deskripsi_pengalaman` — Experience description
- `favorite_song` — Favorite song

## Step 4: Generate Sessions (CRITICAL)

**⚠️ Without sessions, teacher dashboard shows NOTHING.**

Sessions require these columns (not just schedule_id + student_id):

```sql
schedule_id, student_id, teacher_id, class_id, session_date, time, status, is_reminder_sent, created_at, updated_at
```

### Common Pitfall: Missing Columns
The `schedule_sessions` table requires `teacher_id`, `class_id`, and `time` — INSERT will fail or sessions won't appear without these.

### Generate 4 Sessions (1 Month Package)
```bash
# Variables
SCHEDULE_ID=675
STUDENT_ID=42
TEACHER_ID=15
CLASS_ID=6
TIME='14:00:00'

# Selasa (Tuesday) in September 2026: 1st, 8th, 15th, 22nd
for DATE in "2026-09-01" "2026-09-08" "2026-09-15" "2026-09-22"; do
  curl -s -X POST "https://rofcmusicschool.com/api/ai/query" \
    -H "Content-Type: application/json" -H "X-AI-API-KEY: PasswordRahasiaBotSaya123" \
    -d "{\"query\": \"INSERT INTO schedule_sessions (schedule_id, student_id, teacher_id, class_id, session_date, time, status, is_reminder_sent, created_at, updated_at) VALUES ($SCHEDULE_ID, $STUDENT_ID, $TEACHER_ID, $CLASS_ID, '$DATE', '$TIME', 'booked', 0, NOW(), NOW())\"}"
done
```

### Session Date Rules
- Dates must be actual class day (Selasa=Tuesday, Rabu=Wednesday, etc.)
- September 2026 Tuesdays: 1, 8, 15, 22
- September 2026 Wednesdays: 2, 9, 16, 23
- September 2026 Thursdays: 3, 10, 17, 24
- September 2026 Fridays: 4, 11, 18, 25
- September 2026 Saturdays: 5, 12, 19, 26
- September 2026 Sundays: 6, 13, 20, 27
- September 2026 Mondays: 7, 14, 21, 28

### Verify Sessions Created
```bash
curl -s -X POST "https://rofcmusicschool.com/api/ai/query" \
  -H "Content-Type: application/json" -H "X-AI-API-KEY: PasswordRahasiaBotSaya123" \
  -d '{"query": "SELECT ss.id, ss.session_date, ss.time, ss.status, s.name FROM schedule_sessions ss JOIN students s ON ss.student_id = s.id WHERE ss.student_id = STUDENT_ID ORDER BY ss.session_date"}'
```

## Reference IDs (as of 2026-09)

### Teachers
| ID | Name |
|----|------|
| 8 | MUHAMMAD AZZAM |
| 9 | ABDUL HAMID |
| 10 | IDA BAGUS AHLAN ZEN |
| 11 | ROBY LAMBERTUS HADINATA |
| 12 | DEWI HANDAYANI |
| 14 | ZAMZAM KAMIL |
| 15 | SHYAKIRA FATIHA (Shakira) |
| 16 | TRI SUTRISNO |

### Classes
| ID | Name |
|----|------|
| 5 | Violin |
| 6 | Vocal |
| 7 | Drum |
| 8 | Guitar |
| 9 | Piano |

### Schedule Lookup Pattern
```sql
SELECT id, class_id, teacher_id, day, time 
FROM schedules 
WHERE class_id = [CLASS_ID] 
  AND teacher_id = [TEACHER_ID] 
  AND day = '[Day]'  -- Selasa, Rabu, Kamis, Jumat, Sabtu, Minggu, Senin
  AND time = '[HH:MM:SS]'  -- e.g., '14:00:00'
```

## Common Pitfalls
1. **Password hash** — Must be bcrypt format, use verified hash: `$2y$12$AW6y5kMxQLvD/5UhqQpxkOokh75Iws.70Ly7eGqlqD45unYvFnLh2`
2. **email must match** — students.email should equal users.email
3. **schedule_id required** — Cannot create student without linking to a schedule
4. **⚠️ Session generation MISSING columns** — schedule_sessions INSERT must include `teacher_id`, `class_id`, and `time` — NOT just schedule_id + student_id. Without these, teacher dashboard shows nothing.
5. **Session dates must be actual class day** — Selasa=Tuesday (1,8,15,22), NOT sequential (1,2,3,4)
6. **start_date format** — Must be YYYY-MM-DD, not DD/MM/YYYY
7. **end_date calculation** — start_date + duration_months (1 month = ~30 days)
# ROFC Scheduling System — Deep Dive

## Session Generation Flow

### Entry Points (all have dedup checks)
1. `AcademicManagementController::approveRegistration()` — when admin approves registration
2. `RegistrationController::generateInitialSessions()` — alternative registration approval
3. `AiAgentController::handleAddSchedule()` — via API action
4. `RescheduleRequest::approveReschedule()` — when reschedule is approved
5. `scripts/sync_sessions.php` — standalone sync script

### Dedup Pattern (applied to all entry points)
```php
$sessionDate = $currentDate->toDateString();
$existing = ScheduleSession::where('student_id', $student->id)
    ->where('session_date', $sessionDate)
    ->where('time', $time)
    ->exists();

if (!$existing) {
    ScheduleSession::create([...]);
}
```

### Session Count Formula
```
totalSessions = duration_months × 4
```
Sessions are weekly, starting from `start_date`. **No auto-renewal.**

### Session Numbering (in teacher schedule view)
- Grouped by `effective_month` (month of first session in the 4-session block)
- Session number = `(index % 4) + 1` within the block
- Even if session 4 falls in next calendar month, it stays in the original month's tab

## Schedule Checkbox Mapping
- `input[name="schedule_ids[]"]` — values are schedule table IDs
- Each day × time × teacher = one checkbox

### TRI SUTRISNO @ 17:00 (Guitar) ID Pattern
| Day | Schedule ID |
|-----|-------------|
| Senin | 768 |
| Selasa | 783 |
| Rabu | 798 |
| Kamis | 813 |
| Jumat | 828 |
| Sabtu | 843 |
| Minggu | 858 |

## Common Issues & Fixes

### Duplicate Sessions
**Root cause:** Multiple code paths create sessions without checking for existing records.
**Fix:** All entry points now have dedup `exists()` check before `create()`.
**Production cleanup:** `DELETE FROM schedule_sessions WHERE id IN (...)` to remove duplicates, keeping earliest ID per (student_id, session_date, time).

### add_schedule Action — Wrong Teacher ID Bug
**Root cause:** `handleAddSchedule()` does `$schedule = Schedule::where('student_id', $student->id)->first()`. If the student's schedule has `student_id=null` (available slot), it finds nothing and falls back to `Teacher::first()->id` — which is often the WRONG teacher.
**Workaround:** Bypass `add_schedule` action. Insert sessions directly via SQL:
```sql
INSERT INTO schedule_sessions (schedule_id, student_id, teacher_id, class_id, session_date, time, status, created_at, updated_at)
VALUES (851, 19, 16, 8, '2026-09-06', '10:00:00', 'booked', NOW(), NOW()), ...;
```
Always verify `teacher_id` in the INSERT matches the intended teacher.

### Teacher Attendance Prerequisite for ABSENSI Button
**Rule:** The student ABSENSI button in teacher portal only appears if the **teacher has a `teacher_attendances` record for that date**. Without it, all student sessions show without action buttons.
**Check:** `SELECT * FROM teacher_attendances WHERE teacher_id = X AND attendance_date = 'YYYY-MM-DD'`
**Fix:** Create teacher attendance first via Dashboard Admin or SQL INSERT.

### Schedule Unique Constraint
The `schedules` table has a **unique index** on `(teacher_id, day, time)`. You CANNOT update a schedule's teacher_id if another schedule already exists with the same teacher/day/time. Must delete the wrong schedule and reassign sessions to the correct one.

### No Auto-Renewal
Sessions generated only at registration/edit. Admin must manually re-edit student to regenerate.

### Form Performance
Student edit form loads ~5600 checkboxes. Use `delegate_task` or direct POST, not browser automation.

## Adding New Student Schedule via API — Quick Reference
```sql
-- 1. Find student
SELECT id, name, is_active, class_id, schedule_id FROM students WHERE name LIKE '%name%';

-- 2. Find available schedule (day + time + teacher)
SELECT id, day, time, teacher_id, class_id, status FROM schedules
WHERE day = 'Minggu' AND time = '10:00:00' AND teacher_id = 16 AND class_id = 8 AND status = 'available';

-- 3. Insert 4 sessions (adjust IDs and dates)
INSERT INTO schedule_sessions (schedule_id, student_id, teacher_id, class_id, session_date, time, status, created_at, updated_at)
VALUES
  (SCHED_ID, STUDENT_ID, TEACHER_ID, CLASS_ID, '2026-09-06', '10:00:00', 'booked', NOW(), NOW()),
  (SCHED_ID, STUDENT_ID, TEACHER_ID, CLASS_ID, '2026-09-13', '10:00:00', 'booked', NOW(), NOW()),
  (SCHED_ID, STUDENT_ID, TEACHER_ID, CLASS_ID, '2026-09-20', '10:00:00', 'booked', NOW(), NOW()),
  (SCHED_ID, STUDENT_ID, TEACHER_ID, CLASS_ID, '2026-09-27', '10:00:00', 'booked', NOW(), NOW());

-- 4. Verify
SELECT ss.id, ss.session_date, ss.time, ss.teacher_id, s.name
FROM schedule_sessions ss JOIN students s ON ss.student_id = s.id
WHERE ss.teacher_id = TEACHER_ID AND ss.session_date >= '2026-09-01' ORDER BY ss.session_date;
```

## Debugging
```
GET /debug-student-schedules
```
Check: `schedules_table` (should have entries), `sessions` (should have dated entries)

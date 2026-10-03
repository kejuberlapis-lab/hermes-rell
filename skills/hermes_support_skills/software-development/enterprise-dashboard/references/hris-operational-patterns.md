# HRIS Operational Patterns & Edge Cases Reference

This reference documents real production patterns and pitfalls discovered during HRIS development and operations.

---

### 1. Multi-Tier Approval Workflows & Action Gating Matrix
- **Approval Actions by Status**:
  - `pending_manager`: Approve/Reject/Revise buttons rendered strictly for Division Managers (`role == 'manager'` or `super_admin`) where `current_user.id != requester_id`.
  - `pending_director`: Approve/Reject/Revise buttons rendered strictly for Executive Directors (`role == 'director'` or executive super admin). Requester managers see read-only `View Detail`.
  - `draft` / `revision_required`: Edit, Submit, and Resubmit buttons restricted to the request owner (`current_user.id == requester_id`).
  - `approved` / `completed`: Finance processing restricted to Finance/Accounting roles and `super_admin`.

---

### 1b. Manager-Tier Travel Request (SPPD) Lifecycles & Subordinate Document Access
- **Manager Self-Service SPPD Modification & Resubmission**:
  - In hierarchical approval models, requests submitted by Division Managers bypass `pending_manager` and jump straight to `pending_director`.
  - *Pitfall*: If the update endpoint (`PUT /api/travel/{id}`) or UI edit button restricts modifications strictly to `draft` and `revision_required`, a Manager cannot edit their request while awaiting Director review (`pending_director`) or after receiving revision notes.
  - *Fix*:
    1. In backend `update_travel`: Allow request updates when status is `draft`, `revision_required`, OR `pending_director` (if requester is the owner).
    2. In frontend action matrix: Expose `btnEdit` and `btnResubmit` (`/api/travel/{id}/submit`) for the request owner when status is `pending_director` or `revision_required`.
- **Subordinate SPPD Print & Document Transparency**:
  - Division Managers require instant visual transparency to inspect and print official SPPD documents of their direct subordinates (`WHERE manager_id = user_id`).
  - Always render the `Print / View SPPD` button (`btnPrint`) for managers across all approved, pending, and completed records of their team members so they can audit the generated 2-TTD or 3-TTD official letters without requiring administrative privilege elevation.

---

### 2. Fingerprint Machine Excel Bulk Import (`/api/attendance/import-excel`)
- **Centralized GA Workflow**:
  - Centralized in General Affair (GA) Manager (`andreas`) and `super_admin`.
  - Disable self-service manual clock in/out buttons on dashboards and ledger pages.
- **Biometric Name Fuzzy Resolution Strategy**:
  1. *Synonym / Override Dictionary*: Exact mapping for abbreviated names (e.g. `"Lim Mei Ie"` -> Mei, `"Auw Septiawati Keristin"` -> Kristin).
  2. *Substring Containment*: Check if database full name is substring of Excel cell or vice-versa.
  3. *Alphanumeric Token Intersection*: `len(set(re.findall(r'\w+', excel_name)).intersection(set(re.findall(r'\w+', db_name)))) > 0`.
- **Status Classification Logic**:
  - Scan In exists -> `present` (or `late` if late minutes > 0).
  - Note indicates `S` -> `sick`, `C` -> `leave`, `Penugasan` / `Dinas` -> `duty`.
  - Missing scan in/out without note -> `absent`.

---

### 3. SQLite CHECK Constraint Migration in Production
- When adding new enum states (e.g., adding `'sick'`, `'leave'`, `'duty'` to an attendance table with `CHECK(status IN ('present', 'absent', 'late', 'half_day'))`), SQLite requires a table rebuild:
```python
conn.execute('PRAGMA foreign_keys=OFF;')
conn.execute('BEGIN TRANSACTION;')
conn.execute('''
CREATE TABLE table_new (
    ...
    status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late', 'half_day', 'sick', 'leave', 'duty', 'holiday')),
    ...
);
''')
conn.execute('INSERT INTO table_new SELECT * FROM table_old;')
conn.execute('DROP TABLE table_old;')
conn.execute('ALTER TABLE table_new RENAME TO table_old;')
conn.commit()
```

---

### 4. Client-Side Overwrite vs Server-Side Rendered (SSR) Stat Cards
- When Jinja2 server-side rendering computes card statistics (e.g. `att_stats`), ensure background client JS (such as `loadAttendanceSummary()`) does not blindly fetch an empty/dummy API summary and overwrite DOM elements on window load.

---

### 5. Organizational Hierarchy & Performance Evaluation Cascading
- When transferring employees from one manager to another:
  1. Update `employees.manager_id = new_mgr_id`.
  2. Cascade active performance evaluations: `performance_reviews.reviewer_id = new_mgr_id`.
  3. Cascade KPI reviews: `employee_kpis.reviewed_by = new_mgr_id`.
- Maintain clean isolation between operational managers (`role == 'manager'`) and master system administrators (`role == 'super_admin'`).

---

### 6. Live Polling Notifications & Realtime Topbar Updates
- For multi-tier web applications without WebSockets:
  1. Trigger event entries into `notifications` table on critical status changes (submission, manager approval, director revision).
  2. Implement client-side periodic polling (e.g. `setInterval(() => App.initNotifications(), 30000)`) in `app.js`.
  3. Wire dynamic badge counts (`#notifBadge`) and "Mark All Read" endpoint (`PUT /api/notifications/read-all`).

---

### 7. End-to-End Payroll Batch Execution vs UI Stubs
- Do not leave batch processing buttons as cosmetic toast stubs (`App.processPayroll()`).
- The button must prompt with period confirmation (Month/Year), invoke `POST /api/payroll/process`, compute salary line-items in the database, and trigger automatic UI table reloads.

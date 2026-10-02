---
name: enterprise-workflow-and-role-governance-v3
description: "Use when managing approval workflows or attendance rules."
version: 3.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [workflow, approvals, hierarchy, rbac, lifecycle, state-machine, hris, erp, attendance, geofencing, transitions, notifications]
    related_skills: [production-environment-operations-v2, systematic-debugging, reverify]
---

# Enterprise Workflow, Role Governance & Attendance Architecture

A class-level operational guide for designing, debugging, auditing, and maintaining enterprise role hierarchies, approval workflows (SPPD/Travel, Leave, Overtime, Reimbursement), automated lifecycle state machines, and centralized attendance geofencing systems.

## When to Use

- When subordinate submissions (e.g. travel requests, leave, reimbursement) fail to appear in supervisor/manager dashboards.
- When designing or debugging multi-tier approval chains (e.g., Staff $\rightarrow$ Manager $\rightarrow$ Director $\rightarrow$ Finance).
- When state transition validators throw transition errors on resubmit/double-click (e.g., `Cannot transition from 'pending_manager' to 'pending_manager'`).
- When implementing self-registration, user onboarding, or account approval pipelines in HRIS/ERP systems.
- When configuring centralized attendance geofencing, GPS radius validation, punctuality grace periods, or attendance policy enforcement.
- When diagnosing automated lifecycle schedulers (e.g., membership freeze/unfreeze, contract expirations, quota extensions).
- When packaging full application source code and database dumps for export or chat delivery.

## Procedure

1. **Hierarchy Linkage & Foreign Key Verification:**
   - **Audit User-to-Employee Mapping:** Confirm that each authenticated user record (`users.employee_id`) links to the canonical record in the organizational directory (`employees.id`).
   - **Inspect Structural Foreign Keys:** Verify that the employee record has valid non-null values for:
     * `department_id`: Department assignment for divisional scoping.
     * `manager_id`: Immediate supervisor's `employee_id` for approval routing.
     * `position_id`: Job title/role for signature authority.
   - **Detect Orphan Records:** Query for active employees with missing structural linkages:
     ```sql
     SELECT id, full_name, email FROM employees WHERE status = 'active' AND (manager_id IS NULL OR department_id IS NULL);
     ```

2. **Approval Scope, Transition State Machines & Idempotency:**
   - **Idempotent Status Transitions:** State transition validation matrices must permit idempotent transitions (e.g., `pending_manager -> pending_manager` and `pending_director -> pending_director`). When an already submitted item receives a submit command (due to double-clicks, UI retries, or edit resubmissions), the backend must update metadata (`updated_at`), refresh supervisor notifications, and return a clean success response without throwing a 400 transition error.
   - **Auto-Submit on Creation (Form Modal Handshake):** When modal submission forms present a "Submit Request" CTA, do not leave records silently stranded in `draft` state unless an explicit "Save as Draft" button was clicked. Programmatic creation (`POST /api/travel`) should immediately transition/submit the record into the proper role queue:
     * **Executive / Director (1 Signature):** Directly `approved`.
     * **Manager (2 Signatures):** Bypasses manager level directly to `pending_director`.
     * **Staff (3 Signatures):** Directly into `pending_manager` linked to their immediate supervisor.
   - **SQL Column Shadowing in Joins (Supervisor Notification Bug):** In join queries between transaction records and employees (`SELECT tr.*, e.full_name, e.manager_id FROM travel_requests tr JOIN employees e ...`), if both tables contain a `manager_id` column, `tr.*` shadows `e.manager_id` (which is `NULL` prior to supervisor approval). Always alias supervisor references explicitly:
     ```sql
     SELECT tr.*, e.full_name as emp_name, e.manager_id as direct_manager_id
     FROM travel_requests tr
     JOIN employees e ON tr.employee_id = e.id
     ```
   - **Trace Manager Scope Logic:** Enterprise approval tables filter actionable items by supervisor scope:
     ```sql
     WHERE req.employee_id = :manager_emp_id 
        OR req.employee_id IN (SELECT id FROM employees WHERE manager_id = :manager_emp_id)
     ```
   - **Simulate Authenticated Role Query:** Test API endpoints directly using the supervisor's bearer token or session cookie to verify exact list visibility before confirming resolution.
   - **Relink Orphaned Submissions:** When an employee submitted requests while unlinked, update both the employee profile (`employees.manager_id = :target_manager`) and the existing submission records (`travel_requests.employee_id = :canonical_emp_id`).

3. **System-Wide Multi-User Audit & Credential Verification:**
   - When auditing directory health, execute automated login tests (`/api/auth/login`) against *all* registered user accounts in the system rather than sampling only admin accounts.
   - Verify that bcrypt password hashes in both `users` and `employees` match canonical format and resolve successfully.
   - Test key operational endpoints (`/attendance/today-status`, `/dashboard`, `/travel`, `/leave`, `/overtime`, `/reimbursements`) across representative accounts from every organizational tier (Executive, Divisional Manager, Staf).

4. **Safe Registration & Onboarding Pipeline Guardrail:**
   - **Prevent Duplicate / Split Employee Entities:** When approving public user registrations, never unconditionally execute `INSERT INTO employees` with placeholder/random IDs if an employee record already exists for that person.
   - **Link to Existing Directory:** First search for matching email/phone in `employees`. If found, link `users.employee_id = existing_employee.id`. If new, enforce mandatory selection of `department_id`, `manager_id`, and `position_id` upon administrative approval.

5. **Automated Lifecycle State Machine & Scheduler Sizing:**
   - **Audit State Machine Exclusions:** Ensure daily maintenance commands do not unconditionally skip records in temporary states (e.g. `STATUS_FREEZE`, `SUSPENDED`).
   - **Implement Active State Resumption:** Construct dedicated scheduler commands (`members:auto-unfreeze`) that query expired status periods (`end_date < today`), calculate duration adjustments, restore status to active/expired, and mark transition records as `finished`.
   - **Order Scheduler Execution:** Place resumption/unfreeze commands *before* general status recalculation commands in the console kernel (`00:00` vs `00:05`).

6. **GPS Geofencing, Centralized Settings & Attendance Policy Architecture:**
   - **Centralized Reference Coordinates & Superadmin Locks:** Store office GPS coordinates (`office_lat`, `office_lng`, `office_radius`, `wfo_strict_mode`) in centralized database tables (`company_settings`) accessible only to Superadmin/Director roles. Never allow client-side or employee-level modification of reference coordinates. All user GPS calculations query these centralized server settings dynamically.
   - **Live GPS & Distance Calculation (Haversine Formula):** Use HTML5 Geolocation API (`getCurrentPosition` with `enableHighAccuracy: true`) and calculate geodesic distance in meters on the backend using the Haversine formula against the central office coordinates to prevent client-side distance tampering.
   - **Humanized Distance Unit Formatting:** Always format distance values conditionally across all UI components (status badges, modal camera previews, history tables, photo viewer metadata, and API validation messages):
     * If distance $\ge 1,000\text{ meters}$: format as **Kilometers** (`X.X km`, e.g. `14.2 km`).
     * If distance $< 1,000\text{ meters}$: format as **Meters** (`X meter` or `X m`, e.g. `150 meter`).
     Never display unformatted large integers like `14174 meter` in user-facing views.
   - **Attendance Type Policy Alignment:** Strictly align attendance types with organizational policy (e.g. `WFO` enforcing radius tolerance $\le 200\text{m}$ vs `Duty/Dinas Luar` requiring activity notes and client coordinates; explicitly purge/reject unsupported modes such as `WFH` across frontend selectors and backend schema validation when prohibited by company governance).
   - **Dynamic Grace Period & Punctuality Calculation:** Use dynamic start time and grace period threshold (`work_start_time` + `grace_period_mins`) to distinguish between on-time (`present`) and late (`late`) arrivals accurately.
   - **Anti-Cheat Live Face Capture & Dual-Mode Camera:** Use WebRTC `navigator.mediaDevices.getUserMedia` with `facingMode: 'user'`, mirrored display (`scaleX(-1)`), and an SVG/CSS oval face guidance frame. Provide an explicit fallback native camera capture input (`<input type="file" accept="image/*" capture="user">`) for full device compatibility on HTTP development IPs and HTTPS production domains. Capture directly to `<canvas>`/base64 payload to server; reject file picker / gallery uploads to prevent spoofing.
   - **Multi-Service Host Port Architecture:** On servers running multiple web applications (e.g. HRIS on port `8082`, SIMRS on `8089`), check systemd service unit definitions (`/etc/systemd/system/*.service`) and process working directories (`/proc/<pid>/cwd`) before binding ports or executing diagnostic curls.

7. **Compact Project & Database Packaging for Delivery:**
   - **Gzip Database Dump:** Always compress database SQL dumps (`.sql.gz`) prior to bundling (reduces 50 MB raw SQL to ~4.8 MB).
   - **Prune Heavy Run-Time Assets:** Exclude runtime upload folders (`public/media/`, `public/uploads/`), temporary test archives, and storage log files to ensure zip archives stay safely below platform upload thresholds (< 50 MB).

## Pitfalls

- **Rigid Transition State Matrices Crashing on Resubmit:** Rejecting `state -> state` transitions causes application crashes when users double-click submit buttons or save revisions; allow idempotent transitions and refresh notifications gracefully.
- **SQL Wildcard Column Shadowing in Joins:** Using `SELECT tr.*, e.manager_id` shadows the employee's supervisor ID with the transaction table's `manager_id` (NULL until approved), preventing submission notifications from reaching the supervisor.
- **Modal Creation Disconnected from Submission:** Creating records as `draft` when the user clicks "Submit Request" leaves items invisible in approval queues ("0 Draft Not Submitted") and confuses end users.
- **Unlinked Registration Dropping Workflow Visibility:** Creating new employee rows without `manager_id` upon user registration drops all subsequent submissions from manager dashboard queues silently, without throwing application runtime errors.
- **Hardcoding Company Geofence Coordinates in Code:** Hardcoding office coordinates in route source files rather than centralized database settings forces code redeployments whenever office boundaries shift and prevents non-developer superadmins from managing branches.
- **Mismatch Between Attendance Modes and Corporate Policy:** Offering unauthorized attendance options (e.g., WFH in strictly on-site or client-duty companies) confuses employees and breaks HR compliance auditing.
- **Unformatted Raw Distances in UI:** Showing raw meter counts for large distances (e.g. `14174 meter`) degrades mobile readability; always convert $\ge 1,000\text{m}$ to `km`.
- **Geodesic vs Driving Distance Discrepancies:** Attendance geofencing calculates straight-line spherical distance (Haversine formula), which is shorter than Google Maps / GPS navigation driving distances that follow street curves and highways. Explain this clear distinction to end users when addressing reported distance differences.
- **Passive vs Active State Transitions:** Relying on user interactions (such as check-in taps or visiting profile pages) to trigger state transitions leaves accounts in stale frozen/suspended states if the user remains inactive; always deploy automated cron schedulers.
- **Split User Identity:** Creating multiple user or employee entries for the same physical person fragments attendance, points, leave balances, and payroll calculations; maintain a single canonical `employee_id`.

---
name: enterprise-workflow-and-role-governance-v2
description: "Use when managing approval workflows or attendance rules."
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [workflow, approvals, hierarchy, rbac, lifecycle, state-machine, hris, erp, attendance, geofencing]
    related_skills: [production-environment-operations-v2, systematic-debugging, reverify]
---

# Enterprise Workflow, Role Governance & Attendance Architecture

A class-level operational guide for designing, debugging, auditing, and maintaining enterprise role hierarchies, approval workflows (SPPD/Travel, Leave, Overtime, Reimbursement), automated lifecycle state machines, and centralized attendance geofencing systems.

## When to Use

- When subordinate submissions (e.g. travel requests, leave, reimbursement) fail to appear in supervisor/manager dashboards.
- When designing or debugging multi-tier approval chains (e.g., Staff $\rightarrow$ Manager $\rightarrow$ Director $\rightarrow$ Finance).
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

2. **Approval Scope & Query Diagnosis:**
   - **Trace Manager Scope Logic:** Enterprise approval tables typically filter actionable items by supervisor scope:
     ```sql
     WHERE req.employee_id = :manager_emp_id 
        OR req.employee_id IN (SELECT id FROM employees WHERE manager_id = :manager_emp_id)
     ```
   - **Simulate Authenticated Role Query:** Test the API endpoint directly using the supervisor's bearer token or session cookie to verify exact list visibility before confirming resolution.
   - **Relink Orphaned Submissions:** When an employee submitted requests while unlinked, update both the employee profile (`employees.manager_id = :target_manager`) and the existing submission records (`travel_requests.employee_id = :canonical_emp_id`).

3. **Safe Registration & Onboarding Pipeline Guardrail:**
   - **Prevent Duplicate / Split Employee Entities:** When approving public user registrations, never unconditionally execute `INSERT INTO employees` with placeholder/random IDs if an employee record already exists for that person.
   - **Link to Existing Directory:** First search for matching email/phone in `employees`. If found, link `users.employee_id = existing_employee.id`. If new, enforce mandatory selection of `department_id`, `manager_id`, and `position_id` upon administrative approval.

4. **Automated Lifecycle State Machine & Scheduler Sizing:**
   - **Audit State Machine Exclusions:** Ensure daily maintenance commands do not unconditionally skip records in temporary states (e.g. `STATUS_FREEZE`, `SUSPENDED`).
   - **Implement Active State Resumption:** Construct dedicated scheduler commands (`members:auto-unfreeze`) that query expired status periods (`end_date < today`), calculate duration adjustments, restore status to active/expired, and mark transition records as `finished`.
   - **Order Scheduler Execution:** Place resumption/unfreeze commands *before* general status recalculation commands in the console kernel (`00:00` vs `00:05`).

5. **GPS Geofencing, Centralized Settings & Attendance Policy Architecture:**
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

6. **Compact Project & Database Packaging for Delivery:**
   - **Gzip Database Dump:** Always compress database SQL dumps (`.sql.gz`) prior to bundling (reduces 50 MB raw SQL to ~4.8 MB).
   - **Prune Heavy Run-Time Assets:** Exclude runtime upload folders (`public/media/`, `public/uploads/`), temporary test archives, and storage log files to ensure zip archives stay safely below platform upload thresholds (< 50 MB).

## Pitfalls

- **Unlinked Registration Dropping Workflow Visibility:** Creating new employee rows without `manager_id` upon user registration drops all subsequent submissions from manager dashboard queues silently, without throwing application runtime errors.
- **Hardcoding Company Geofence Coordinates in Code:** Hardcoding office coordinates in route source files rather than centralized database settings forces code redeployments whenever office boundaries shift and prevents non-developer superadmins from managing branches.
- **Mismatch Between Attendance Modes and Corporate Policy:** Offering unauthorized attendance options (e.g., WFH in strictly on-site or client-duty companies) confuses employees and breaks HR compliance auditing.
- **Unformatted Raw Distances in UI:** Showing raw meter counts for large distances (e.g. `14174 meter`) degrades mobile readability; always convert $\ge 1,000\text{m}$ to `km`.
- **Geodesic vs Driving Distance Discrepancies:** Attendance geofencing calculates straight-line spherical distance (Haversine formula), which is shorter than Google Maps / GPS navigation driving distances that follow street curves and highways. Explain this clear distinction to end users when addressing reported distance differences.
- **Passive vs Active State Transitions:** Relying on user interactions (such as check-in taps or visiting profile pages) to trigger state transitions leaves accounts in stale frozen/suspended states if the user remains inactive; always deploy automated cron schedulers.
- **Split User Identity:** Creating multiple user or employee entries for the same physical person fragments attendance, points, leave balances, and payroll calculations; maintain a single canonical `employee_id`.
- **Uncompressed Chat Payloads:** Bundling uncompressed raw SQL and runtime media directories into delivery zip files causes immediate upload rejections on messaging platforms like Telegram.

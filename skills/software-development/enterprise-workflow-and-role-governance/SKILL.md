---
name: enterprise-workflow-and-role-governance
description: "Use when debugging approval workflows or role hierarchy."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [workflow, approvals, hierarchy, rbac, lifecycle, state-machine, hris, erp]
    related_skills: [production-environment-operations-v2, systematic-debugging, reverify]
---

# Enterprise Workflow & Role Governance

A class-level operational guide for designing, debugging, auditing, and maintaining enterprise role hierarchies, approval workflows (SPPD/Travel, Leave, Overtime, Reimbursement), and automated lifecycle state machines.

## When to Use

- When subordinate submissions (e.g. travel requests, leave, reimbursement) fail to appear in supervisor/manager dashboards.
- When designing or debugging multi-tier approval chains (e.g., Staff $\rightarrow$ Manager $\rightarrow$ Director $\rightarrow$ Finance).
- When implementing self-registration, user onboarding, or account approval pipelines in HRIS/ERP systems.
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

5. **GPS Geofencing & Live Face Verification Attendance Architecture:**
   - **Live GPS & Distance Calculation:** Use HTML5 Geolocation API (`getCurrentPosition` with `enableHighAccuracy: true`) and the Haversine formula to compute distance in meters against configured office coordinates (`OFFICE_LAT`, `OFFICE_LNG`).
   - **Attendance Type Routing:** Route validation based on work mode: `WFO` (enforce radius tolerance, e.g. $\le 200\text{m}$), `WFH` (log coordinates with home tag), `Duty/Dinas Luar` (require activity notes + client location pin).
   - **Anti-Cheat Live Face Capture:** Use WebRTC `navigator.mediaDevices.getUserMedia` with `facingMode: 'user'`, mirrored display (`scaleX(-1)`), and an SVG/CSS oval face guidance frame. Capture directly to `<canvas>` and transmit base64 payload to server; reject file picker / gallery uploads to prevent spoofing.
   - **Multi-Service Host Port Architecture:** On servers running multiple web applications (e.g. HRIS on port `8082`, SIMRS on `8089`), check systemd service unit definitions (`/etc/systemd/system/*.service`) and process working directories (`/proc/<pid>/cwd`) before binding ports or executing diagnostic curls.

6. **Compact Project & Database Packaging for Delivery:**
   - **Gzip Database Dump:** Always compress database SQL dumps (`.sql.gz`) prior to bundling (reduces 50 MB raw SQL to ~4.8 MB).
   - **Prune Heavy Run-Time Assets:** Exclude runtime upload folders (`public/media/`, `public/uploads/`), temporary test archives, and storage log files to ensure zip archives stay safely below platform upload thresholds (< 50 MB).

## Pitfalls

- **Unlinked Registration Dropping Workflow Visibility:** Creating new employee rows without `manager_id` upon user registration drops all subsequent submissions from manager dashboard queues silently, without throwing application runtime errors.
- **Passive vs Active State Transitions:** Relying on user interactions (such as check-in taps or visiting profile pages) to trigger state transitions leaves accounts in stale frozen/suspended states if the user remains inactive; always deploy automated cron schedulers.
- **Split User Identity:** Creating multiple user or employee entries for the same physical person fragments attendance, points, leave balances, and payroll calculations; maintain a single canonical `employee_id`.
- **Uncompressed Chat Payloads:** Bundling uncompressed raw SQL and runtime media directories into delivery zip files causes immediate upload rejections on messaging platforms like Telegram.

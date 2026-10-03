---
name: fastapi-ssr-fullstack
description: "FastAPI+Jinja2 SSR pitfalls and parallel multi-agent builds."
version: 1.1.0
author: Hermes Agent (curator-managed)
---

# FastAPI SSR Full-Stack Development

## Overview

Building server-rendered full-stack apps with FastAPI + Jinja2 templates + Bootstrap 5 CDN.
Covers pitfalls, integration patterns, and multi-agent parallel build workflow.

## FastAPI + Jinja2 Template Pitfalls

### 1. `url_for('static')` BROKEN with `app.mount()`

**Symptom:** `starlette.routing.NoMatchFound: No route exists for name "static"`

**Root cause:** `app.mount("/static", StaticFiles(...), name="static")` creates a sub-application, NOT a named route. `url_for("static", filename="...")` in Jinja2 cannot resolve it.

**Fix:** Use literal paths in templates:
```html
<!-- BROKEN with app.mount -->
<link href="{{ url_for('static', filename='css/style.css') }}">

<!-- WORKS -->
<link href="/static/css/style.css">
```

### 2. HTML Form Access by Name Requires `name` Attribute

**Symptom:** `form.username.value` returns empty string even though `id="username"` exists.

**Root cause:** `form.username` accesses by `name` attribute, NOT `id`.

**Fix:** Always add `name` attribute: `<input id="username" name="username">`

Same applies to checkboxes: `<input type="checkbox" id="rememberMe" name="remember">`

### 3. Server-Rendered Pages + Cookie Auth

**Symptom:** Login succeeds, but redirect to `/dashboard` bounces back to login.

**Root cause:** JS stores token in `localStorage`, but server-side auth reads from HTTP cookies.

**Fix:** On login success, set BOTH localStorage AND cookie:
```javascript
localStorage.setItem('hris_token', result.token);
document.cookie = 'token=' + result.token + '; path=/; max-age=' + (60*60*24);
window.location.href = '/dashboard';
```

### 4. DB Seed Password Mismatch

**Symptom:** Login returns "Invalid credentials" even though hash is valid.

**Root cause:** Seed hashed `password123` but UI expects `admin123`.

**Fix:** After seeding, re-hash with canonical password or document the correct one.

### 5. Import Name Mismatch Between Multi-Agent Outputs

**Symptom:** `ImportError: cannot import name 'export_leaves_excel' from 'app.services.export_service'`

**Root cause:** Agent A names function `export_leave_excel` (singular), Agent B imports `export_leaves_excel` (plural). Common when agents work independently on service vs route files.

**Fix:** After agents complete, verify all cross-file imports match actual function definitions:
```bash
# List all function defs in services
grep -rn "^def \|^async def " app/services/
# List all imports from services in routes
grep -rn "from app.services" app/routes/
```

### 6. Router Prefix Missing `api_prefix`

**Symptom:** New API endpoints return 404 even though server starts without errors.

**Root cause:** `app.include_router(new_router)` without `prefix=api_prefix`. All other routers have the prefix.

**Fix:** Always register with consistent prefix:
```python
# In main.py
app.include_router(exports_router, prefix=api_prefix)  # ← DON'T FORGET
```

### 7. Function Signature Mismatch (Routes vs Services)

**Symptom:** `TypeError: export_payroll_pdf() got an unexpected keyword argument 'period'`

**Root cause:** Routes pass individual kwargs (`period=period`), but service functions accept a filters dict (`filters=None`).

**Fix:** Routes must aggregate filters into a dict:
```python
# WRONG
data = export_payroll_pdf(conn, period=period)
# RIGHT
data = export_payroll_pdf(conn, filters={"period": period})
```

## Multi-Agent Parallel Build Pattern

Dispatch 3 subagents simultaneously for non-overlapping file paths:
1. **Agent 1 (Database):** Schema, models, auth, seed data
2. **Agent 2 (Backend):** API routes, main.py
3. **Agent 3 (Frontend):** Templates, CSS, JS

**Post-merge parent must:** verify imports, fix naming mismatches, align auth flow, test end-to-end.

## Post-Merge Integration Checklist

After multi-agent build completes, run these checks:

```bash
# 1. Verify all imports resolve
cd /path/to/project && source venv/bin/activate
python3 -c "from app.routes.<module> import router" 2>&1 | grep ImportError

# 2. Check router registration
grep "include_router" main.py

# 3. Verify DB tables exist
python3 -c "import sqlite3; print([r[0] for r in sqlite3.connect('app.db').execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()])"

# 4. Test page routes return 200
TOKEN=$(curl -s -X POST http://localhost:PORT/api/auth/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
for page in dashboard employees departments; do
    curl -s -o /dev/null -w "$page: %{http_code}\n" -H "Authorization: Bearer $TOKEN" http://localhost:PORT/$page
done

# 5. Test API CRUD endpoints
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:PORT/api/employees | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Employees: {len(d.get(\"employees\", d))} records')"
```

### 8. Bootstrap Modal Overflow (BUTTONS HIDDEN)

**Symptom:** Modals with many form fields push Cancel/Submit buttons off-screen.

**Root cause:** Default Bootstrap modal doesn't scroll internally; content overflows viewport.

**Fix:** Always add `modal-dialog-scrollable`:
```html
<div class="modal-dialog modal-lg modal-dialog-scrollable">
```

### 9. Sidebar Links vs Routes vs Templates Mismatch

**Symptom:** Sidebar shows menu items, clicking them shows 404 or wrong page content.

**Root cause:** `base.html` sidebar has links, but matching `@app.get()` route in `main.py` or matching template in `templates/pages/` is missing. Subagents often reuse existing templates for new routes instead of creating dedicated ones.

**Fix:** After adding any sidebar link, immediately add ALL THREE:
1. `base.html` sidebar link (href + active_page)
2. `main.py` page route (renders correct template with matching active_page)
3. `templates/pages/<name>.html` (dedicated template, not reused from another page)

Verify with:
```bash
# Check all sidebar links have routes
grep 'href="/' templates/base.html | grep -o 'href="/[^"]*"' | while read link; do
    route=$(echo $link | tr -d 'href="')
    grep -q "\"$route\"" main.py && echo "✓ $route" || echo "✗ $ROUTE MISSING"
done
```

### 10. Export Service: PDF/Excel with openpyxl + reportlab

**Pattern:** Use sync `sqlite3.connect()` directly in export routes (don't mix async aiosqlite with sync libraries).

```python
import sqlite3, io
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table

def export_to_excel(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    wb = Workbook()
    ws = wb.active
    # Style: header fill #003366, white text, alternating rows #F2F2F2
    # ... populate rows from query ...
    buffer = io.BytesIO()
    wb.save(buffer)
    conn.close()
    return buffer.getvalue()

# In route:
@router.get("/export")
def export(format: str = "excel"):
    data = export_to_excel(DB_PATH)
    return StreamingResponse(io.BytesIO(data), media_type="...", 
        headers={"Content-Disposition": f'attachment; filename="export.xlsx"'})
```

### 11. Multi-Level Approval Workflow

**Pattern:** Travel requests, procurement, leave — all follow the same state machine.

```python
# Status flow: draft → pending_manager → pending_director → approved → completed
#                                                     ↘ rejected
#                                         ↘ rejected

@router.post("/{id}/submit")        # draft → pending_manager
@router.post("/{id}/approve-manager")  # pending_manager → pending_director  
@router.post("/{id}/reject-manager")   # pending_manager → rejected
@router.post("/{id}/approve-director") # pending_director → approved
@router.post("/{id}/reject-director")  # pending_director → rejected
@router.post("/{id}/finance-submit")   # approved → finance processing
@router.post("/{id}/finance-complete") # finance done → completed
```

Separate `finance_status` field tracks payment state independently from approval.

### 12. JWT `user_id` vs `employee_id` Disambiguation in RBAC

**Symptom:** Role filtering or queries return 0 results or 401/404 for valid logged-in users.

**Root cause:** `JWT` payload contains `user_id` (from `users.id`), but employee routes query `employees.id` (or `employee_id`). Using `users.id` in `employees.id` queries (or vice versa) breaks relational joins.

**Fix:** Standardize `_resolve_emp_id(db, user)` helper across all routes:
```python
async def _resolve_emp_id(db, user):
    # 1. Prefer explicit emp_id in JWT payload
    if user.get("emp_id") or user.get("employee_id"):
        return user.get("emp_id") or user.get("employee_id")
    # 2. Fallback query users.id -> employee_id
    uid = user.get("user_id") or user.get("id")
    cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (uid,))
    row = await cursor.fetchone()
    return row["employee_id"] if row and row["employee_id"] else uid
```

### 13. Dynamic Topbar User Hydration vs Hardcoded Profile HTML

**Symptom:** Logged in as `staf` (e.g. Ahmad Fauzi), but header topbar displays static hardcoded template user (e.g. "Andi Saputra Admin").

**Root cause:** HTML base template has hardcoded user text, and JS login/checkAuth fails to update header DOM elements on page load.

**Fix:** In `checkAuth()` or page initialization, read stored user profile from `localStorage` or `/api/auth/me` and update DOM:
```javascript
const userStr = localStorage.getItem('hris_user');
if (userStr) {
    const u = JSON.parse(userStr);
    const nameEl = document.getElementById('userName');
    const roleEl = document.getElementById('userRole');
    const avatarEl = document.querySelector('.user-avatar span');
    if (nameEl && u.full_name) nameEl.textContent = u.full_name;
    if (roleEl && u.role) roleEl.textContent = u.role.toUpperCase();
    if (avatarEl && u.full_name) {
        const parts = u.full_name.split(' ');
        avatarEl.textContent = parts.length > 1 ? (parts[0][0] + parts[1][0]).toUpperCase() : parts[0][0].toUpperCase();
    }
}
```

### 14. Role Nomenklatur Harmonization (DB vs JS Frontend)

**Symptom:** RBAC menu hiding/showing fails or hides all items when logging in as non-admin role.

**Root cause:** Database stores Indonesian role strings (e.g. `staf`, `direktur`), but JS frontend checks English role keys (e.g. `staff`, `director`).

**Fix:** Normalize role strings immediately upon reading user profile or login response:
```javascript
const normalizedRole = userRole === 'staf' ? 'staff' : (userRole === 'direktur' ? 'director' : userRole);
```

### 15. Disable Demo Mode Fallback in Authentication Scripts

**Symptom:** Invalid or expired logins unexpectedly redirect to dashboard as a hardcoded admin user (e.g. "Andi Saputra Admin").

**Root cause:** Client-side JS `checkAuth()` or `.catch()` block falls back to a hardcoded demo token/user instead of enforcing login redirect.

**Fix:** Remove demo-mode fallback in `checkAuth()` and API `.catch()` blocks; redirect strictly to `/`:
```javascript
if (!this.token && !window.location.pathname.includes('login') && window.location.pathname !== '/') {
    window.location.href = '/';
}
```

### 16. Role-Adaptive Page Headers & Self-Service UI Adaptation

**Symptom:** Non-admin roles (e.g. `staff`) view admin-oriented management pages (e.g., `Employees`, `Documents`) with bulk actions, import/export buttons, and admin headers ("Manage your organization's workforce").

**Root cause:** Single shared HTML template used for all roles without adapting titles, subtitles, search filters, or control buttons dynamically based on user role.

**Fix:** Add `data-role` attributes to admin-only buttons/filters, and update page header titles/subtitles in JS for self-service contexts:
```javascript
// In page load JS handler:
if (normalizedRole === 'staff') {
    const pageTitle = document.getElementById('empPageTitle');
    const pageSub = document.getElementById('empPageSubtitle');
    if (pageTitle) pageTitle.textContent = 'My Profile';
    if (pageSub) pageSub.textContent = 'View your employee profile information';
}
```
And wrap admin-only management elements with role attributes in Jinja2 templates:
```html
<button class="btn btn-primary btn-sm" data-role="super_admin"><i class="fas fa-plus me-1"></i>Add Employee</button>
<div class="card border-0 shadow-sm mb-3" data-role="super_admin,director,manager">
```

### 17. Google Drive Archive / Large File Deployment Workflow

**Symptom:** User needs to deploy or sync a large project archive (e.g. zip file >20MB) hosted on Google Drive or external file host.

**Pattern:** 
1. Install `gdown` or direct downloader CLI via Python/venv if needed: `python3 -m pip install gdown`.
2. Download archive directly to an isolated staging directory (`/tmp/uploaded_file.zip`).
3. Extract archive to a temporary inspection folder (`/tmp/extracted_hris`).
4. Perform structural inspection & sanity checks (`ls -la`, `diff -rq`) before touching production directories.
5. Create a clean backup of the existing project directory (`cp -r /home/ubuntu/hris /home/ubuntu/hris_backup_<timestamp>`).
6. Apply deployment using `rsync -av --exclude='venv' --exclude='__MACOSX' /tmp/extracted_hris/ /home/ubuntu/hris/` to maintain clean permissions and preserve system virtualenv.
7. Verify DB credentials/seed passwords in the newly deployed environment (e.g., check `users` table for password hashes vs expected UI passwords).
8. Nuclear restart background process (`fuser -k -9 <port>/tcp`, start daemon) and verify port status.

### 18. CSS-Only Theme Adaptation (Zero Logic Mutation Rule)

**Symptom:** User requests a complete visual theme redesign (e.g., AdminKit, Tabler, soft-minimalist) without touching backend routes, API contracts, Jinja2 template bindings, or interactive JS handlers.

**Pattern:**
1. **Isolate Changes to CSS:** Focus purely on `/static/css/style.css` (or override CSS file) using clean CSS Custom Properties (`:root` design tokens for primary palette, neutral backgrounds, border radiuses, and layered tinted shadows).
2. **Preserve Semantic HTML Classes & IDs:** Never rename or remove existing class hooks (`.sidebar`, `.main-content`, `.topbar`, `.stat-card`, `.nav-tabs-custom`, `.table-responsive`) that JavaScript listeners or Jinja2 templates depend upon.
3. **Verify Interactive Elements Post-Restyle:** Check in browser that dropdowns, collapse accordions, active navigation pills, and responsive mobile drawers still trigger smoothly.
4. **Enforce Tabular Numbers on Data:** Apply `font-variant-numeric: tabular-nums` to stat values, employee IDs, currency/salary fields, and digital clocks for clean alignment.

### 19. Menu / Feature Deletion Regression Post-Archive Restore

**Symptom:** Previously deprecated or removed navigation menu items (e.g. `Shifts` under `Time & Attendance`) unexpectedly reappear after extracting an older project archive or snapshot.

**Root cause:** Archive zip files from external sources or previous checkpoints contain older versions of `templates/base.html` or navigation components that still contain deprecated links.

**Fix:**
1. After restoring/unzipping an archive, audit all navigation links against active functional requirements:
```bash
grep -rn 'href="/' templates/
```
2. Strip deprecated menu anchor tags from `base.html` immediately.
3. Check in browser via accessibility snapshot or vision to verify exact menu composition matches current state.

### 20. Self-Service Profile Editing with Selective RBAC Field Protection

**Symptom:** Employee self-service requires allowing users to update their own contact/personal/payroll info (e.g. phone, address, bank account, tax numbers), but standard employee endpoints block updates or allow standard users to dangerously overwrite organizational fields (department, position, manager, salary, status).

**Pattern:**
1. **API Route Dual Access:** In `PUT /api/employees/{emp_id}`, allow updates if `caller_emp_id == emp_id` OR `user["role"] in ("super_admin", "director", "manager")`.
2. **Field Sanitization for Self-Service:** If user role is `employee` editing self, strip structural/organizational fields before database update:
```python
if user["role"] == "employee" and caller_emp_id == emp_id:
    protected_fields = ["department_id", "position_id", "manager_id", "hire_date", "status", "role"]
    for pf in protected_fields:
        fields.pop(pf, None)
```
3. **Modal UI & JWT Injection:** Attach an "Edit Data Diri" modal with `modal-dialog-scrollable`, and ensure client-side AJAX fetch explicitly attaches `Authorization: Bearer <token>` retrieved from `localStorage` or session cookie.
4. **Token Resolution in Dependency:** Ensure `get_current_user` dependency resolves and populates `employee_id` in the user dict so `caller_emp_id` accurately matches `employees.id`.

### 21. Corporate Naming Conventions & Entity Identifier Prefix Migration

**Symptom:** Organization standardizes employee IDs/NIK from generic prefixes (e.g. `EMP0001`) to company-specific codes (e.g. `MVP0001`).

**Pattern:**
1. **Database String Replacement:**
```sql
UPDATE employees SET employee_id_str = REPLACE(employee_id_str, 'EMP', 'MVP');
```
2. **Auto-Numbering Prefix Realignment:** Update all backend route generators (`auth.py`, `employees.py`, `export_service.py`) from `f"EMP{...}"` to `f"MVP{...}"`.
3. **Template & Org Chart Sync:** Update hardcoded reference mockups, PDF generation headers, and interactive org-chart tree components to render the new prefix uniformly.

### 22. Production Handover Sanitization: Removing Demo UI Artifacts

**Symptom:** Demo helpers (quick-login buttons, dummy account selectors, "Demo Accounts: password123" boxes) left in `login.html` or dashboard after migration to real company structure.

**Pattern:**
1. **Clean Login View:** Remove all quick-fill buttons and demo boxes from `templates/login.html` to prevent security leakage and present a clean enterprise appearance.
2. **Visual Verification:** Inspect login page via headless browser snapshot/vision to ensure form container stays centered, clean, and properly balanced without the demo widget.
3. **Keep Documented Accounts in Dev Notes:** Keep real role test credentials in developer documentation / deployment handover notes, not in public-facing template DOM.

### 23. Mandatory First-Login Password Change Enforcement

**Symptom:** Default passwords provisioned during mass employee onboarding (e.g. `password123`) create security vulnerabilities if employees do not update them upon initial access.

**Pattern:**
1. **DB Column:** Add `must_change_password INTEGER DEFAULT 1` to the `users` table.
2. **Backend Auth Route:** Expose `POST /api/auth/change-password` requiring `old_password` and `new_password`. On success, update `password_hash` and set `must_change_password = 0`.
3. **Frontend Interceptor Modal:** In `base.html` or main app layout, inject an unclosable backdrop modal if `user.must_change_password == 1`:
```html
<div class="modal fade" id="firstLoginModal" data-bs-backdrop="static" data-bs-keyboard="false">
```
4. **Instant Unlock:** Upon successful password change, dismiss the modal and update session state without requiring a full re-login.

### 24. Document & PDF Financial Alignment Standards (Strict Right-Alignment)

**Symptom:** Financial values, currency headers, empty dashes (`—`), and grand totals in generated PDFs (ReportLab) or HTML print templates have staggered or misaligned right margins.

**Pattern:**
1. **ReportLab Alignment:**
   * Text descriptions: `alignment=0` (Left).
   * Headers and numeric cells under currency columns: create dedicated `ParagraphStyle("RightVal", alignment=2)`.
   * Never leave raw numbers as plain unstyled strings if headers use Paragraphs — wrap both headers and numeric cells in `Paragraph` with `alignment=2` so bounding boxes match.
   * Total and Take Home Pay rows: ensure the numerical amount cell is right-aligned and flush with table column right margin.
2. **HTML Print & Table Alignment:**
   * Use CSS: `.cost-tbl td.num, .cost-tbl th.th-r { text-align: right; font-variant-numeric: tabular-nums; }`.
   * For empty/zero deduction entries, place a centered or right-aligned dash `—` so columns do not look broken.

### 25. High-Fidelity Logo Alpha Masking for Dark/Light UI Surfaces

**Symptom:** Company logo uploaded as a square JPEG with white background looks boxy, pixelated, or distorted when rendered in dark theme sidebars (`#222e3c`).

**Pattern:**
1. **Automated Circular Alpha Masking (PIL):**
```python
from PIL import Image, ImageDraw

img = Image.open(src_path).convert("RGBA")
# Crop tightly to emblem bounding box
cropped = img.crop((left, top, right, bottom))
cw, ch = cropped.size

# High-res anti-aliased circular mask
scale = 4
big_mask = Image.new("L", (cw * scale, ch * scale), 0)
big_draw = ImageDraw.Draw(big_mask)
big_draw.ellipse((0, 0, cw * scale - 1, ch * scale - 1), fill=255)
mask = big_mask.resize((cw, ch), Image.Resampling.LANCZOS)

output = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
output.paste(cropped, (0, 0), mask=mask)
output.save("/path/to/static/img/logo.png", format="PNG")
```
2. **CSS Integration:** Use `object-fit: contain;` and explicit 1:1 width/height (e.g. `38px × 38px`) so the logo maintains exact proportions in navbar and sidebar headers.

### 26. Executive & Board of Commissioners (BOC) Approval Exemption & Multi-Tier Signature Layout

**Symptom:** Travel orders (SPPD) or operational requests submitted by Board of Commissioners (Dewan Komisaris) or Department Managers render incorrect signature blocks on printed documents (e.g. Manager submission rendering 3 signature blocks with an empty supervisor slot instead of 2 signatures, or BOC prompting for supervisor approval).

**Root Cause:** The template/renderer lacked employee position and direct manager relations in the view query (`SELECT tr.* ... LEFT JOIN positions p ... LEFT JOIN employees m`), causing the client-side JavaScript signature resolver to default to standard staff layout (3 signatures).

**Pattern:**
1. **Backend Query Enrichment:** Always JOIN `positions` and self-referential `employees` (manager) when preparing travel/SPPD data lists:
```sql
SELECT tr.*, e.full_name as employee_name, e.employee_id_str, d.name as department_name, 
       p.title as position_title, m.full_name as manager_name
FROM travel_requests tr
JOIN employees e ON tr.employee_id = e.id
LEFT JOIN departments d ON e.department_id = d.id
LEFT JOIN positions p ON e.position_id = p.id
LEFT JOIN employees m ON e.manager_id = m.id
```
2. **Dynamic Signature Block Adaptation in Document Templates:**
   * **BOC / Direksi (1 Tanda Tangan Tunggal):** Auto-approved, single centered signature block representing *Pimpinan / Direksi*.
   * **Manajer Divisi (2 Tanda Tangan):** Applicant is a Manager (`posTitle.includes('manager') || emp.manager_name == 'William Hosea Eko Putro'`) -> left signature is *Pemohon (Manajer Divisi)*, right signature is *Disetujui oleh (Direktur Utama)*.
   * **Staf Biasa (3 Tanda Tangan):** Standard employee -> left is *Yang Melaksanakan (Staf)*, center is *Mengetahui (Manajer Divisi / Atasan)*, right is *Disetujui oleh (Direktur Utama)*.

### 27. Pydantic Form Body Schema vs Dynamic Calculation Fallbacks

**Symptom:** Submitting multi-field operational forms (e.g. Travel, Reimbursement) triggers a 500 error: `'ModelCreate' object has no attribute 'estimated_cost'` or overwrites calculated totals with `0`.

**Root Cause:** The Pydantic model definition omitted an optional/derived field that the route handler logic tried to access directly (`body.grand_total or body.estimated_cost`), or default `0` fell through when client form inputs calculated totals under an alternative field name.

**Pattern:**
1. **Always Declare Optional Cost & Total Fields in Pydantic Schema:**
```python
class TravelCreate(BaseModel):
    employee_id: int
    destination: str
    transport_type: str
    estimated_cost: Optional[float] = 0
    grand_total: Optional[float] = 0
    # ... all subtotal components
```
2. **Prioritize Explicit Non-Zero Totals Over Fallback Defaults:**
```python
# In route handler, ensure calculated form total is preserved:
effective_cost = body.grand_total if (body.grand_total and body.grand_total > 0) else (getattr(body, 'estimated_cost', 0) or 0)
```

### 28. Event-Driven Workflow Notifications to Role Hierarchies

**Symptom:** When an employee or manager submits an operational request (SPPD travel, leave, reimbursement), approving authorities (Directors/Managers) see no notifications in their topbar dropdown.

**Pattern:**
1. **Insert Notification on State Transition:** In route handlers (`POST /submit`, `POST /approve-manager`), query user IDs for the target approver roles and insert records into `notifications`:
```python
# Notify Director(s)
dir_users = conn.execute("SELECT id FROM users WHERE role IN ('director', 'super_admin')").fetchall()
for u in dir_users:
    conn.execute(
        "INSERT INTO notifications (user_id, title, message, link) VALUES (?, ?, ?, ?)",
        (u[0], "Persetujuan Perjalanan Dinas", f"Pengajuan baru ke {body.destination} membutuhkan persetujuan Direktur.", "/travel")
    )
```
2. **Hydrate Topbar Notifications Dynamically:** Ensure client-side JS (`app.js`) queries `/api/notifications` on page load to replace static mockup items with real user notification records, updating the badge count and mark-as-read handlers.

### 29. Centralized Fingerprint Excel Import & Check-In Only Policy

**Symptom:** Client app provides manual Clock In / Clock Out buttons, but office operations rely on central RFID/biometric fingerprint machines where employees do not check out upon leaving.

**Pattern:**
1. **Disable Manual Self-Clocking:** Remove client-side Clock In / Out action buttons from Dashboard & Attendance pages to prevent arbitrary attendance manipulation.
2. **Role-Restricted Excel Import Endpoint:** Allow GA Manager / Super Admin to upload raw fingerprint `.xlsx` sheets (mapping `No ID`, `Nama`, `Tanggal`, `Scan Masuk`, `Terlambat`, `Keterangan`).
3. **Smart Fuzzy & Token Name Matching:** Use a dictionary lookup plus token-intersection fallback to match raw fingerprint export names to internal `employees` table records.
4. **Single Check-In Presence Rule:** If `scan_in` exists without `scan_out`, treat status as `present` (or `late` if scan exceeds shift start) rather than flagging as incomplete/absent.

### 30. SSR Stat Card Value Overwrite by Asynchronous Background API Polling

**Symptom:** Server-rendered Jinja2 metric cards display accurate historical/filtered statistics on initial page load, but flash to `0` or `-` a second later.

**Root Cause:** Generic background JavaScript (e.g. `loadAttendanceSummary()`) triggered on page load fetches a company-wide today endpoint (`/api/attendance/summary` returning today's zeros) and overwrites the server-rendered DOM elements (`#attPresent`, `#attLate`).

**Fix:** Remove or guard client-side JS pollers on server-rendered SSR pages, allowing Jinja2-rendered personal and period-filtered metrics to persist accurately without async overwrite.

### 31. Dedicated Printable Document Route & Compact Stamp Watermarks

**Symptom:** Client-side print modals or popup JS scripts fail to render complete signature hierarchies, or print popups get blocked/truncated before dynamic status watermarks render. Large approval watermark stamps dwarf the signature space.

**Pattern:**
1. **Dedicated SSR Route (`/module/{id}/print`):** Avoid client-side DOM scrapers or messy popup windows. Serve an independent clean HTML template styled for standard A4 (`@page { size: A4 portrait; margin: 15mm; }`) with print utilities (`.no-print-bar { display: none !important; }`).
2. **Compact & Proportional Approval Watermark Stamps:**
   * Do NOT use oversized stamps that obscure signatory names.
   * Standard compact watermark badge CSS:
```css
.stamp-badge {
  display: inline-block;
  padding: 2px 8px;
  border: 1.5px solid #16a34a;
  color: #16a34a;
  font-family: 'Arial Black', sans-serif;
  font-size: 7pt;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  border-radius: 3px;
  transform: rotate(-7deg);
  opacity: 0.82;
  background: rgba(240, 253, 244, 0.75);
}
.stamp-badge small {
  display: block;
  font-size: 4.8pt;
  font-family: 'Arial', sans-serif;
  font-weight: 700;
  letter-spacing: 0.3px;
  margin-top: -1px;
}
```
3. **Hierarchy-Aware Stamp Display:**
   * Employee / Applicant: Blue `SUBMITTED` stamp with creation date.
   * Manager / Supervisor: Green `APPROVED` stamp rendered only when `manager_approved_at` or status is approved.
   * Director / BOC: Green `APPROVED` stamp rendered upon final executive sign-off.

### 32. Custom Document Auto-Increment Sequence (e.g. `SPPD-001`)

**Symptom:** Database table `id` primary key does not match company official document numbering sequence (e.g. initial paper records started earlier, or numbering must be zero-padded and continuous from an official starting request).

**Pattern:**
1. **Dedicated Sequence Column:** Add `sppd_number INTEGER` (or `doc_number`) distinct from the auto-increment DB row `id`.
2. **Atomic Next Sequence Resolver on Creation:**
```python
cur_seq = conn.execute("SELECT COALESCE(MAX(sppd_number), 0) + 1 FROM travel_requests WHERE sppd_number IS NOT NULL")
next_sppd_num = cur_seq.fetchone()[0]
```
3. **Formatted Display Code:**
   * Badge format: `SPPD-001` via `f"SPPD-{str(num).zfill(3)}"` or JS `String(num).padStart(3, '0')`.
   * Formal Document Number format: `Nomor: SPPD/001/HRIS/2026`.

### 33. cPanel Shared Hosting to VPS FastAPI High-Speed Reverse Proxy Bridge

**Symptom:** Company domain/subdomain is hosted on cPanel shared hosting (PHP 8.x only, no Python Passenger / root access), while the backend application runs as a FastAPI service on a VPS.

**Pattern:**
1. Point subdomain document root (e.g. `/hris.mitsindo.co.id/`) to an `index.php` bridge script using cURL with full header/method forwarding (`$_SERVER['REQUEST_METHOD']`, `file_get_contents('php://input')`, `X-Forwarded-Proto: https`, `X-Forwarded-For`).
2. Forward requests internally or via an open VPS port (e.g. `http://<VPS_IP>:8082`).
3. Ensure the VPS listener runs on `0.0.0.0:<port>` with firewall reachability verified from the cPanel host.

## Tiered Role Testing Workflow

When testing multi-role apps, test in strict hierarchical order without bloating dummy data:
1. **Staff Tier:** Log in as Staff -> fill all form actions (Clock in, Overtime, Leave, Reimbursement, Travel) -> verify self-only isolation.
2. **Manager Tier:** Log in as Manager -> verify pending queue -> approve/reject items submitted by subordinates -> verify team-only visibility.
3. **Director / Exec Tier:** Log in as Director -> execute final approval (Tier 2) -> verify executive company-wide dashboard metrics.

## Checklist

- [ ] Templates use `/static/` not `url_for('static')`
- [ ] All form inputs have `name` attributes
- [ ] Login JS sets localStorage AND cookie
- [ ] Server-side auth reads from cookies
- [ ] DB seed password matches documented user password
- [ ] All cross-file imports verified (service ↔ route)
- [ ] All routers registered with `prefix=api_prefix`
- [ ] Service function signatures match route call patterns
- [ ] All modals with forms use `modal-dialog-scrollable`
- [ ] Every sidebar link has matching route + template
- [ ] Export routes use sync sqlite3 (not async aiosqlite)

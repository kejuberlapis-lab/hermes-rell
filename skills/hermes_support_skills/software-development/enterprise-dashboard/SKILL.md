---
name: enterprise-dashboard
description: FastAPI + Bootstrap 5 admin panel with JWT auth and RBAC. Full enterprise SaaS patterns including export (Excel/PDF), multi-agent build, and production pitfalls.
version: 1.2.0
author: Hermes Agent
---

# Enterprise Dashboard Builder

Build enterprise-grade admin panels and internal tools with Python backend + Bootstrap 5 CDN frontend.

## Tech Stack
- **Backend**: FastAPI + aiosqlite (async SQLite) or asyncpg (Postgres)
- **Frontend**: Bootstrap 5.3 CDN + Font Awesome 6 + Chart.js + Inter font
- **Auth**: JWT (python-jose) + bcrypt (passlib) with RBAC
- **Templates**: Jinja2 with base.html layout + page templates
- **Database**: SQLite for MVP/internal, Postgres for production
- **Export**: openpyxl (Excel) + reportlab (PDF) via StreamingResponse

## Architecture

### Project Structure
```
project/
├── main.py                    # FastAPI entry + page routes + lifespan
├── requirements.txt
├── app/
│   ├── database.py            # Async DB, schema, init_db(), seed
│   ├── models/schemas.py      # Pydantic models
│   ├── services/
│   │   ├── auth_service.py    # JWT + bcrypt + get_current_user
│   │   └── export_service.py  # Excel/PDF generation (openpyxl + reportlab)
│   └── routes/
│       ├── auth.py            # /api/auth/login, /logout, /me
│       ├── <module>.py        # One file per module
│       ├── dashboard.py       # Aggregated stats
│       └── exports.py         # /api/exports/<module> download endpoints
├── templates/
│   ├── base.html              # Sidebar + topbar layout
│   ├── login.html             # Standalone (no extends)
│   └── pages/*.html           # One per module page
└── static/
    ├── css/style.css          # Extends Bootstrap
    └── js/app.js              # API calls, Chart.js, sidebar
```

### main.py Pattern
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

api_prefix = "/api"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

for router in [auth_router, employees_router, exports_router]:
    app.include_router(router, prefix=api_prefix)  # ← MUST include prefix
```

### Auth Flow
1. JS POST `/api/auth/login` → gets JWT → stores in localStorage AND sets cookie
2. Server reads JWT from cookie for page routes
3. JS reads JWT from localStorage for API calls
4. RBAC: `get_current_user` dependency → `require_role("super_admin")` factory

## ⚠️ Critical Pitfalls

### 1. Static Files + url_for
`url_for('static')` **BREAKS** with `app.mount()`. Use `/static/css/style.css` directly.

### 2. HTML Input name Attributes
JS `form.username.value` requires `name` attribute, not just `id`.

### 3. JWT Cookie vs localStorage
Server reads cookie, JS uses localStorage. Login must set BOTH.

### 4. Table Name Mismatch (Multi-Agent)
Verify actual DB table names match route queries.

### 5. Password Seed Mismatch (Multi-Agent)
Standardize password in seed function across all agents.

### 6. Server Restart
Kill old process before restarting: `fuser -k PORT/tcp; sleep 1`

### 7. Import Name Mismatch (Multi-Agent)
**Symptom**: `ImportError: cannot import name 'export_leaves_excel' from ...`
**Root cause**: Agent A names function `export_leave_excel` (no 's'), Agent B imports `export_leaves_excel` (with 's').
**Fix**: After all agents complete, grep all imports vs actual function defs:
```bash
# Check all function definitions
grep -rn "^def " app/services/
grep -rn "^async def " app/routes/
# Check all imports
grep -rn "from app" app/routes/
```

### 8. Router prefix=api_prefix Mismatch
**Symptom**: New API endpoints return 404 even though server starts fine.
**Root cause**: `app.include_router(new_router)` without `prefix=api_prefix`. Other routers use `prefix=api_prefix`.
**Fix**: Always add `prefix=api_prefix`:
```python
app.include_router(new_router, prefix=api_prefix)  # ← DON'T FORGET
```

### 9. Function Signature Mismatch (Routes vs Services)
**Symptom**: `TypeError: export_payroll_pdf() got an unexpected keyword argument 'period'`
**Root cause**: Route passes `period=period` as kwarg, but service function signature is `def export_payroll_pdf(db=None, filters=None)`.
**Fix**: Routes must pass filters as dict:
```python
# WRONG
data = export_payroll_pdf(conn, period=period)
# RIGHT
data = export_payroll_pdf(conn, filters={"period": period})
```

### 10. sync sqlite3 for Export Routes
Export routes use sync `sqlite3.connect()` directly, not async aiosqlite. This avoids async compatibility issues in reportlab/openpyxl.

### 11. Sidebar Links Without Page Routes
**Symptom**: Sidebar navigation shows links but pages return 404 or "Not Found".
**Root cause**: Multi-agent build creates sidebar HTML (base.html) with links like `/documents`, `/shifts`, `/reimbursement`, but API agent only creates routes for major modules. Sub-pages (shifts, payslips, reimbursement, reviews, requisitions, interviews, documents, org-chart) often missing.
**Fix**: After multi-agent build, verify EVERY sidebar href has a corresponding `@app.get` route:
```bash
grep -oP 'href="/\K[a-z-]+' templates/base.html | sort -u > /tmp/sidebar.txt
grep -oP '@app.get\("/\K[a-z-]+' main.py | sort -u > /tmp/routes.txt
diff /tmp/sidebar.txt /tmp/routes.txt
```
Sub-pages can reuse existing templates: `/shifts` → `attendance.html`, `/payslips` → `payroll.html`, etc.

### 12. Route Template Path Mismatch
**Symptom**: Route exists but renders wrong page content (e.g., `/reimbursement` shows Payroll page).
**Root cause**: When reusing templates for sub-pages, route may point to wrong template file: `"pages/payroll.html"` instead of `"pages/reimbursement.html"`.
**Fix**: After adding routes, verify each route's template path:
```bash
grep -A5 'def.*_page' main.py | grep 'TemplateResponse'
```
Ensure `/reimbursement` → `pages/reimbursement.html`, not `pages/payroll.html`.

### 13. Multi-Level Approval Workflow Pattern
**Use for**: Travel requests, leave approvals, procurement sign-offs — any flow requiring 2+ approval levels.
**Database schema**: Add status column with states: `draft → pending_manager → pending_director → approved → completed`. Include `manager_id/approved_at/notes` and `director_id/approved_at/notes` pairs. Add finance fields for disbursement: `finance_status (not_submitted/submitted/processing/completed)`, `finance_amount`, `finance_processed_by`, `finance_processed_at`.
**API pattern**: Separate endpoints for each transition:
```
POST /api/{module}/submit         # draft → pending_manager
POST /api/{module}/approve-manager  # pending_manager → pending_director
POST /api/{module}/reject-manager   # pending_manager → rejected
POST /api/{module}/approve-director # pending_director → approved
POST /api/{module}/reject-director  # pending_director → rejected
POST /api/{module}/finance-submit   # not_submitted → submitted
POST /api/{module}/finance-process  # submitted → processing
POST /api/{module}/finance-complete # processing → completed
```
**Frontend**: Horizontal workflow step indicator (Bootstrap badges/numbered steps). Context-sensitive action buttons per row (draft shows Edit/Submit/Delete; pending shows Approve/Reject; approved shows Submit to Finance).

### 14. Dynamic Custom Fields in Forms
**Pattern**: "Tambah Field" button adds label+value input pairs. Store as JSON array column.
```python
# DB: ALTER TABLE travel_requests ADD COLUMN custom_fields TEXT DEFAULT '[]'
# JS: Collect from document.querySelectorAll('.custom-field-row')
# API: Accept custom_fields as array of {label, value} objects
```
**HTML**:
```html
<div id="customFieldsContainer"></div>
<button type="button" class="btn btn-outline-primary btn-sm" onclick="addCustomField()">
  <i class="fas fa-plus me-1"></i> Tambah Field
</button>
```
**JS**: `addCustomField()` creates flex row with 2 inputs + remove button. `removeCustomField(btn)` removes the row. Submit handler collects all pairs into array.

### 15. Full System QA Test Matrix Pattern
**When user asks for QA, test EVERYTHING — not just the feature under discussion.**
**Components to cover**: All sidebar pages (HTTP 200), all API endpoints (GET/POST/PUT/DELETE), all export endpoints (Excel + PDF), auth validation (valid/invalid), form validation (empty required fields), edge cases (non-existent IDs, delete non-draft), full CRUD workflows E2E.
**Output format**: Structured markdown table with columns: `# | Component | Location | Test Action | Expected | Actual | Status (PASS/FAIL) | Severity`.
**Automation**: Use `execute_code` with subprocess curl for API tests, browser tools for UI visual checks. Binary responses (Excel/PDF) use `-o /dev/null -w '%{http_code}'` to avoid UTF-8 decode errors. Login via API once, reuse token for all subsequent calls.
**Common false FAILs**: HTTP 201 (Created) is valid for POST create — test expects 200. Clock-in "already clocked in" returning 400 is correct behavior, not a bug. Required query params returning 422 is validation working correctly.

### 15b. Export Buttons Can Also Be JS Stubs
**Symptom**: User clicks Export dropdown, selects Excel/PDF, nothing happens (no download).
**Root cause**: Subagent created `App.exportTable()` that only calls `showToast()`. The `<a href="/api/exports/...">` download links exist in a separate dropdown but the main Export button uses the broken JS stub.
**Fix**: Replace JS-export buttons with direct `<a href>` links inside a Bootstrap split dropdown. Never use JS to trigger file downloads when the server already has a download endpoint — just link to it:
```html
<div class="btn-group">
  <a href="/api/exports/employees?format=excel" class="btn btn-success btn-sm">
    <i class="fas fa-file-excel me-1"></i> Export Excel
  </a>
  <button type="button" class="btn btn-success btn-sm dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown">
    <span class="visually-hidden">Toggle Dropdown</span>
  </button>
  <ul class="dropdown-menu">
    <li><a class="dropdown-item" href="/api/exports/employees?format=excel"><i class="fas fa-file-excel me-2 text-success"></i>Excel</a></li>
    <li><a class="dropdown-item" href="/api/exports/employees?format=pdf"><i class="fas fa-file-pdf me-2 text-danger"></i>PDF</a></li>
  </ul>
</div>
```
**Note**: Export routes should NOT require auth (no `Depends(get_current_user)`) since `<a href>` browser navigation doesn't send Bearer tokens. If auth is needed, use JS `fetch()` with Blob download instead.

### 15c. Import / Bulk Upload Feature Pattern
**When user asks for CSV/Excel import**, add these three components:
1. **Backend endpoint** (`POST /api/{module}/import`): Accept `UploadFile`, parse CSV via `csv.DictReader` or XLSX via `openpyxl`, validate required fields, insert with duplicate checking, return `{imported, errors[], total_rows}`.
2. **Frontend modal**: File upload with drag-and-drop zone, file name preview, progress bar, result display with error list.
3. **JS handler**: `FormData` → `fetch()` with auth header → show progress → display results.

**Backend pattern**:
```python
from fastapi import UploadFile, File

@router.post("/import")
async def import_employees(file: UploadFile = File(...), user=Depends(get_current_user), db=Depends(get_db)):
    content = await file.read()
    if file.filename.endswith('.csv'):
        import csv, io
        rows = list(csv.DictReader(io.StringIO(content.decode('utf-8'))))
    elif file.filename.endswith(('.xlsx', '.xls')):
        import openpyxl, io
        wb = openpyxl.load_workbook(io.BytesIO(content))
        ws = wb.active
        headers = [cell.value for cell in ws[1]]
        rows = [dict(zip(headers, row)) for row in ws.iter_rows(min_row=2, values_only=True)]
    else:
        raise HTTPException(400, "Only CSV and XLSX supported")
    imported, errors = 0, []
    for i, row in enumerate(rows):
        try:
            # Extract fields with flexible column name matching
            full_name = row.get('full_name') or row.get('Full Name') or row.get('name', '')
            email = row.get('email') or row.get('Email', '')
            if not full_name or not email:
                errors.append(f"Row {i+2}: missing name or email")
                continue
            # Check duplicate
            cur = await db.execute("SELECT id FROM employees WHERE email = ?", (email,))
            if await cur.fetchone():
                errors.append(f"Row {i+2}: email {email} already exists")
                continue
            await db.execute("INSERT INTO employees (...) VALUES (...)")
            imported += 1
        except Exception as e:
            errors.append(f"Row {i+2}: {str(e)[:100]}")
    await db.commit()
    return {"imported": imported, "errors": errors, "total_rows": len(rows)}
```

### 15d. Toast Notifications Are Invisible to Users
**Symptom**: `showToast()` runs without error, toast container exists, but user sees nothing happen when clicking buttons.
**Root cause**: Bootstrap toasts auto-hide in 3 seconds and auto-remove from DOM. Users don't notice them — especially if the click also triggers a confirm() dialog or network delay.
**Fix**: For action buttons (edit, view, delete, approve), use **modals** instead of toasts. Toasts are fine for background notifications (export started, sync complete). For buttons the user clicks and expects feedback:
- **Edit buttons** → Open a dynamic Bootstrap modal with form fields pre-filled via API fetch
- **View buttons** → Open a detail modal with key-value table
- **Delete** → `confirm()` dialog → API call → row removal + success toast is OK (confirm provides the feedback moment)
**Pattern — Generic dynamic modals in app.js**:
```javascript
showEditModal(title, id, fields) {
    const modalId = 'editModal_' + Date.now();
    // fields = [{name, label, value, type: 'text|select|number', options?}]
    // Create modal HTML, insert into DOM, show via bootstrap.Modal
    // Auto-remove on hidden.bs.modal
}
showDetailModal(title, rows) {
    // rows = [['Label', 'Value'], ...]
    // Same pattern, read-only table layout
}
saveEdit(modalId, type, id) {
    // Collect FormData → PUT /api/{type}/{id} → hide modal → toast + reload
}
```

### 15e. FK Constraint on DELETE Returns 500
**Symptom**: DELETE /api/employees/5 returns 500 Internal Server Error.
**Root cause**: SQLite foreign key constraints — employee has related records in attendance, payroll, leave, etc. Unhandled exception becomes 500.
**Fix**: Wrap DELETE in try/except and return 400 with message:
```python
try:
    await db.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    await db.commit()
except Exception as e:
    raise HTTPException(status_code=400, detail=f"Cannot delete: has related records. ({str(e)[:100]})")
```

### 15f. Logout Must Clear BOTH Cookie AND localStorage
**Symptom**: User clicks Logout but stays logged in (page refreshes to dashboard, not login).
**Root cause**: Auth check reads token from cookie (server-side) AND localStorage (JS). Clearing only one leaves the other active.
**Fix**: Logout function must clear all three:
```javascript
logout() {
    localStorage.removeItem('hris_token');
    localStorage.removeItem('hris_role');
    localStorage.removeItem('hris_user');
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/';
}
```
Also ensure redirect goes to actual login route (often `/` not `/login`).

### 15g. Multi-Agent Button Handler Bug — Dead onclick on Non-First Rows
**Symptom**: First row's edit/delete buttons work, but all other rows' buttons do nothing.
**Root cause**: When subagents patch HTML tables row-by-row, they often add `onclick` only to the first `<tr>` and miss subsequent rows. Each row's button must have its own `onclick` with the correct entity ID.
**Fix**: After multi-agent build, scan ALL rows for dead buttons:
```javascript
document.querySelectorAll('table tbody tr').forEach((row, i) => {
    row.querySelectorAll('td:last-child button').forEach(btn => {
        if (!btn.getAttribute('onclick')) console.log(`Row ${i+1}: DEAD BUTTON`, btn.innerHTML);
    });
});
```

### 15h. CRITICAL: API Tests ≠ UI Button Tests — Test Actual Button Interactivity
**NEVER claim "zero defects" based solely on HTTP status code testing.** API returning 200 does NOT mean the UI button that calls it actually works.
**What to actually test** (browser console + visual):
1. **Every action button (eye/edit/trash) must have an onclick handler or href**: `document.querySelectorAll('table tbody button').forEach(b => console.log(b.getAttribute('onclick') || 'NO HANDLER'))`
2. **Every href must point to an existing route**: Check that `/employees/1` has a corresponding `@app.get('/employees/{emp_id}')` in main.py
3. **Every onclick function must exist in JS**: `typeof App.confirmDelete` must be `function`, not `undefined`
4. **Every JS handler must actually call an API**: Inspect function body — if it only shows `confirm()` + `showToast()` without `fetch()`, it's a stub
5. **Every delete handler must have onclick on ALL rows**, not just the first row (multi-agent bug: only first row gets onclick, rest are dead)

**User's exact complaint**: "aneh kamu bilang tidak ada eror saya coba klik lambang mata atau edit atau hapus tombol tidak berfungsi" — they found all buttons broken after I declared zero defects.

**Verification script** (add to QA test suite):
```javascript
// Run in browser console on each table page
(function(){
  const rows = document.querySelectorAll('table tbody tr');
  let issues = [];
  rows.forEach((row, i) => {
    const btns = row.querySelectorAll('td:last-child button, td:last-child a');
    btns.forEach(b => {
      const handler = b.getAttribute('onclick') || b.getAttribute('href');
      if (!handler) issues.push(`Row ${i+1}: ${b.innerHTML.trim()} has NO handler`);
      if (handler && handler.startsWith('/employees/') && !window.location.pathname.includes('employees')) {
        issues.push(`Row ${i+1}: href ${handler} may not have a route`);
      }
    });
  });
  return issues.length ? issues : 'All buttons have handlers ✓';
})()
```

### 15i. Complete CRUD Button Lifecycle — Every Button Must Do Something Visible
**NEVER leave any button as a dead stub.** Users click buttons expecting visible action. Here's the complete lifecycle every table row should implement:

**View (eye icon) — Two patterns:**
1. Navigate to detail page: `onclick` → `window.location.href = '/employees/' + id` (requires `@app.get('/employees/{emp_id}')` route)
2. Show modal: `onclick` → `App.viewEntity(id)` → fetch GET `/api/entities/{id}` → `App.showDetailModal('Title', [['Key', value], ...])`

**Edit (pencil icon):**
1. Fetch entity from API: `fetch('/api/employees/' + id)`
2. Show dynamic modal with form fields pre-filled
3. Save button: PUT `/api/employees/{id}` → close modal → success toast → page reload
```javascript
editEmployee(id) {
    fetch(`${this.API_BASE}/employees/${id}`, {headers: {'Authorization': `Bearer ${this.token}`}})
    .then(r => r.json())
    .then(emp => {
        const e = emp.data || emp;
        this.showEditModal('Edit Employee', id, [
            {name: 'full_name', label: 'Full Name', value: e.full_name, type: 'text'},
            {name: 'email', label: 'Email', value: e.email, type: 'text'},
            {name: 'status', label: 'Status', value: e.status, type: 'select', options: ['active','inactive','on_leave']}
        ]);
    })
    .catch(err => this.showToast('Failed to load: ' + err.message, 'danger'));
}
```

**Delete (trash icon):**
1. `confirm('Are you sure?')` dialog
2. `fetch('/api/employees/' + id, {method: 'DELETE'})`
3. On success: remove table row from DOM + show success toast
4. On error (FK constraint): show error toast with message (NOT 500 — see pitfall 15e)

**Approve/Reject:**
1. `confirm('Approve this request?')` dialog
2. POST `/api/module/{id}/approve` or `/reject`
3. On success: reload page (status changes, buttons change)

**Generic helpers for app.js:**
```javascript
showEditModal(title, id, fields) {
    const modalId = 'editModal_' + Date.now();
    const fieldsHtml = fields.map(f => {
        if (f.type === 'select') {
            const opts = f.options.map(o => `<option value="${o}" ${o === f.value ? 'selected' : ''}>${o}</option>`).join('');
            return `<div class="mb-3"><label class="form-label fw-semibold">${f.label}</label><select class="form-select" name="${f.name}">${opts}</select></div>`;
        }
        return `<div class="mb-3"><label class="form-label fw-semibold">${f.label}</label><input type="${f.type || 'text'}" class="form-control" name="${f.name}" value="${f.value || ''}"></div>`;
    }).join('');
    // ... create modal, insert into DOM, show via bootstrap.Modal, auto-remove on hidden
}
showDetailModal(title, rows) {
    // rows = [['Label', 'Value'], ...]
    // Read-only table in a Bootstrap modal
}
saveEdit(modalId, type, id) {
    const form = document.getElementById(modalId + '_form');
    const data = Object.fromEntries(new FormData(form));
    fetch(`${this.API_BASE}/${type}/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${this.token}`},
        body: JSON.stringify(data)
    })
    .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
    .then(() => { bootstrap.Modal.getInstance(document.getElementById(modalId)).hide(); this.showToast('Updated', 'success'); setTimeout(() => location.reload(), 1000); })
    .catch(err => this.showToast('Failed: ' + err.message, 'danger'));
}
```

### 15j. Audit Trail — Scan for Dead Buttons BEFORE User Does
**After ANY multi-agent or subagent build, run this browser console audit on EVERY table page:**
```javascript
(function(){
    let issues = [];
    // Check ALL onclick handlers exist
    document.querySelectorAll('[onclick]').forEach(el => {
        const match = el.getAttribute('onclick').match(/App\.(\w+)\(/);
        if (match && typeof App[match[1]] !== 'function') {
            issues.push('Dead handler: App.' + match[1] + '() not defined');
        }
    });
    // Check ALL table rows have handlers on ALL buttons
    document.querySelectorAll('table tbody tr').forEach((row, i) => {
        row.querySelectorAll('td:last-child button, td:last-child a').forEach(b => {
            if (!b.getAttribute('onclick') && !b.getAttribute('href')) {
                issues.push(`Row ${i+1}: button "${b.textContent.trim()}" has no handler`);
            }
        });
    });
    // Check all <a href> links resolve to existing page routes
    document.querySelectorAll('a[href^="/"]').forEach(a => {
        const path = new URL(a.href).pathname;
        // Can't verify server routes from client-side, but flag common issues
        if (path.match(/^\/\w+\/\d+$/) && !document.body.dataset.entityRoutes) {
            issues.push(`Link ${path} may need a detail route`);
        }
    });
    return issues.length ? 'ISSUES:\n' + issues.join('\n') : '✓ All buttons audited — no dead handlers';
})()
```

### 16. Adding New Modules to Existing HRIS
**Pattern**: When adding a new feature (e.g., KPI, Travel, Procurement) to an existing HRIS:

**Step 1: Extract Requirements from Documents**
```bash
# For PDF files
pdftotext input.pdf -  # Output to stdout

# For DOCX files
python3 -c "
from docx import Document
doc = Document('input.docx')
for para in doc.paragraphs:
    print(para.text)
for table in doc.tables:
    for row in table.rows:
        print(' | '.join([cell.text for cell in row.cells]))
"
```
**Pitfall**: If `ocr-and-documents` skill is pruned/unavailable, use `pdftotext` or `python-docx` directly.

**Step 2: Design Database Schema**
```python
# Create new tables with proper foreign keys
cursor.execute("""
CREATE TABLE IF NOT EXISTS kpi_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name TEXT NOT NULL,
    department TEXT,
    position TEXT,
    kpi_name TEXT NOT NULL,
    formula_id INTEGER,
    target_standard TEXT,
    weight_percentage REAL,
    scoring_scale TEXT,  -- JSON format
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (formula_id) REFERENCES kpi_formulas(id)
)
""")

# Insert template data from extracted document
templates = [
    ("Revenue Growth", "Executive", "Director", "Revenue Growth", 1, 
     "Sesuai RUPS", 40.0, '{"1": "<50%", "2": "50-69%", "3": "70-85%", "4": "86-100%", "5": ">100%"}'),
    # ... more templates
]
cursor.executemany("INSERT INTO kpi_templates (...) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", templates)
```

**Step 3: Create API Routes**
```python
# app/routes/kpi_dashboard.py
from fastapi import APIRouter, Depends
from app.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/kpi-dashboard", tags=["kpi-dashboard"])

@router.get("/summary")
async def get_summary(user=Depends(get_current_user), db=Depends(get_db)):
    # ... implementation
```

**Step 4: Register Router in main.py**
```python
from app.routes.kpi_dashboard import router as kpi_dashboard_router
app.include_router(kpi_dashboard_router, prefix=api_prefix)  # ← MUST include prefix
```

**Step 5: Create Dashboard UI**
```html
<!-- templates/pages/kpi_dashboard.html -->
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KPI Dashboard - HRIS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Dashboard content -->
</head>
```

**Step 6: Create Export Files**
```python
# Export in multiple formats
import csv
import json

# CSV
with open('kpi_formulas.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Template', 'Department', ...])
    for template in templates:
        writer.writerow(template)

# JSON
with open('kpi_formulas.json', 'w') as f:
    json.dump(kpi_data, f, indent=2, ensure_ascii=False)

# SQL INSERT
with open('kpi_formulas.sql', 'w') as f:
    f.write("INSERT INTO kpi_templates (...) VALUES (...);\n")
```

**Step 7: Test and Verify**
```bash
# Test database
python3 -c "import sqlite3; conn = sqlite3.connect('hris.db'); print(conn.execute('SELECT COUNT(*) FROM kpi_templates').fetchone()[0])"

# Test API endpoints
curl -H "Authorization: Bearer $TOKEN" http://localhost:8090/api/kpi-dashboard/summary

# Test dashboard page
curl -H "Authorization: Bearer $TOKEN" http://localhost:8090/kpi-dashboard
```

### 17. Missing Dependencies Checklist
**Symptom**: Server starts but API endpoints return 404 or import errors occur.
**Root cause**: Dependencies not installed in the environment.
**Required packages for HRIS**:
```bash
pip install aiosqlite python-jose[cryptography] passlib[bcrypt] reportlab openpyxl python-docx
```
**Verification**:
```python
import aiosqlite
from jose import jwt
from passlib.context import CryptContext
from reportlab.lib import colors
import openpyxl
from docx import Document
print("All dependencies installed ✓")
```

### 17b. Server Running from venv — Check Startup Method
**Symptom**: You modified main.py, restarted the server, but changes don't appear. New routes return 404.
**Root cause**: Server was originally started via `./venv/bin/uvicorn main:app` (from a previous session or systemd), not `python main.py`. Different Python environments = different installed packages.
**Detection**: `ps aux | grep -E "uvicorn|main.py" | grep -v grep`
**Fix**: Kill ALL existing processes on the port, then start with the SAME command:
```bash
# Find what's using the port
lsof -ti:PORT | xargs kill -9
# Check how it was originally started
ps aux | grep uvicorn
# Start with same method — if venv uvicorn:
cd /path/to/project && ./venv/bin/uvicorn main:app --host 0.0.0.0 --port PORT --reload
# OR if plain python:
cd /path/to/project && python3 main.py
```
**Critical**: When adding new routes (router + page route + sidebar link), the server MUST be restarted after each change. With `--reload` flag, uvicorn auto-reloads on file changes.

### 17c. Testing with Public IP vs Localhost
**When user accesses HRIS via public IP (e.g. 43.134.179.61:8090), always test URLs with that IP — not localhost.**
**Why**: Some server configurations, firewalls, or proxy setups behave differently on localhost vs public IP. User explicitly reminded: "ingat kita pakai ip itu" (remember we use that IP).
**Pattern**:
```bash
# Test main page
curl -s -o /dev/null -w "%{http_code}" http://PUBLIC_IP:PORT/
# Test new page route
curl -s -o /dev/null -w "%{http_code}" http://PUBLIC_IP:PORT/kpi-dashboard
# Test API endpoint
curl -s -H "Authorization: Bearer $TOKEN" http://PUBLIC_IP:PORT/api/kpi-dashboard/summary
```

### 17d. Adding Sidebar Link for New Module
**After creating page route + API routes + template, ALWAYS add sidebar navigation link.**
**File**: `templates/base.html` — find the relevant section (e.g. "Performance") and add:
```html
<a href="/new-module" class="sidebar-link {% if active_page == 'new-module' %}active{% endif %}">
    <i class="fas fa-icon-name"></i><span>New Module</span>
</a>
```
**Verification**: After restart, login and check sidebar shows the new link. Test the link navigates correctly.

### 18b. Sidebar Redundancy & Historical Ghost Links on Restore
**Symptom**: Previously deleted or deprecated sidebar links (e.g. `/shifts` under Attendance) reappear after unzipping/restoring an older code archive or backup.
**Root cause**: Unzipping older code archives overwrites `templates/base.html` back to an earlier revision containing deprecated navigation menus.
**Fix**:
1. Scan `templates/base.html` for deprecated routes after any restore/unzip operation.
2. Cross-check active routes in `main.py` vs sidebar entries:
```bash
grep -oP 'href="/\K[a-z-]+' templates/base.html | sort -u
```
3. Remove unneeded items (e.g., removing `Shifts` so Time & Attendance only shows `Attendance` and `Overtime`).
4. Re-verify rendered output via browser tool snapshot/vision.

### 18c. Organizational Structure Account Provisioning & RBAC Mapping
**Pattern**: When provisioning accounts from an organizational structure chart (e.g., PT Mitsindo):
1. **Hierarchical Mapping**:
   - Extract Board of Commissioners, Executive Director, Department Heads/Managers, and Staff.
   - Establish explicit `manager_id` parent relations (e.g., Staff $\rightarrow$ Manager $\rightarrow$ Director).
2. **Role Mapping in HRIS**:
   - `super_admin`: IT Admin / System Administrator, Commissioners (if requested for system-wide access)
   - `director`: Managing Director (Executive oversight & final SPPD/Leave approval, distinct from super_admin)
   - `manager`: Department Heads (1st tier approval for team requests)
   - `finance`: Finance & Accounting Heads (Payroll batch processing & disbursement settlement)
   - `employee`: Regular staff, technical specialists, drivers, sales officers
3. **Database Schema Constraints Check**:
   - Note `CHECK (role IN ('super_admin', 'director', 'manager', 'employee'))` on SQLite `users` table. If `finance` is not a discrete ENUM role, assign `manager` or `employee` role and grant operational menu permissions accordingly.
4. **Clarification Protocol**:
   - Always confirm dual-role duplicate names (e.g. same name in two divisions).
   - Clarify whether legacy/dummy records should be purged or preserved.
   - Confirm default credentials policy before database insertion.

### 18d. Org Chart Interactive Template Synchronization
**Symptom**: Database has new corporate hierarchy, but `/org-chart` displays hardcoded old dummy names (e.g. "Dr. Surya Pratama").
**Root cause**: `orgchart.html` had a static mock HTML tree rather than reading from database or matching current company structure.
**Fix**:
1. When company hierarchy is updated, update `templates/pages/orgchart.html` to reflect the exact tiered node structure (Komisaris $\rightarrow$ Direktur & Sekretaris $\rightarrow$ Department Grid).
2. Use distinct CSS classes per hierarchy level (`.commissioner`, `.director`, `.secretary`, `.manager`, `.staff`) with color-coded top borders for visual clarity.

### 13b. Export Filter `_where_clause` with Date Ranges
**Symptom**: Attendance/Payroll export fails with date filter kwargs.
**Root cause**: `_where_clause(filters)` does `key = ?` for all filters, but `start_date`, `end_date`, and `period` need special SQL handling (not simple equality).
**Fix**: Build `_where_clause` with special cases:
```python
def _where_clause(filters, extra_wheres=None):
    wheres, params = list(extra_wheres or []), []
    for key, val in (filters or {}).items():
        if val is None or val == "": continue
        if key == "start_date":
            wheres.append("a.date >= ?"); params.append(val)
        elif key == "end_date":
            wheres.append("a.date <= ?"); params.append(val)
        elif key == "period":
            parts = val.split("-")
            if len(parts) == 2:
                wheres.append("p.period_year = ? AND p.period_month = ?")
                params.extend([int(parts[0]), int(parts[1])])
        else:
            wheres.append(f"{key} = ?"); params.append(val)
    return f"WHERE {' AND '.join(wheres)}" if wheres else "", params
```
Routes must pass filters as dict: `export_payroll_pdf(conn, filters={"period": period})`.

### 18e. Corporate NIK / Employee ID Customization
**Pattern**: When migrating or customizing HRIS for a specific company (e.g., PT Mitsindo Solution Integration):
1. **Prefix Alignment**: Check and adjust employee ID string generation from default (`EMP0001`) to company-specific format (e.g., `MVP0001` or `MVP-YYYYMMDD-XXXX`).
2. **Global Sync**: Update prefix in:
   - `employees` table `employee_id_str` column (`UPDATE employees SET employee_id_str = REPLACE(employee_id_str, 'EMP', 'MVP')`)
   - `app/routes/auth.py` auto-registration generator
   - `app/routes/employees.py` employee creation fallback
   - `app/services/export_service.py` PDF payslip and Excel generator default fallbacks
   - `templates/pages/orgchart.html` and any static mock nodes.

### 18f. Self-Service Employee Profile Editing with Field-Level RBAC
**Pattern**: Allow employees to update personal & financial details while locking organizational fields.
1. **RBAC Boundary in Route (`PUT /api/employees/{emp_id}`)**:
   - Regular employee (`role == 'employee'`) can only update their own record (`user['employee_id'] == emp_id`).
   - If not `super_admin` / `manager`, filter update payload: allow only `phone`, `date_of_birth`, `gender`, `marital_status`, `religion`, `address`, `bank_name`, `bank_account`, `npwp`, `bpjs_ketenagakerjaan`, `bpjs_kesehatan`.
   - Strip structural/organizational fields (`department_id`, `position_id`, `employee_id_str`, `status`, `hire_date`, `manager_id`) from regular employee requests to prevent privilege escalation.
2. **UI Implementation**:
   - Add modal `#editProfileModal` in `templates/pages/employee_detail.html` pre-populated with employee data.
   - Attach Bearer token from localStorage/cookie to the `fetch` request header: `Authorization: Bearer ${token}`.

### 18g. Mandatory First-Login Password Change Workflow
**Pattern**: Enforce password change on initial login for newly provisioned accounts.
1. **Database Flag**: `ALTER TABLE users ADD COLUMN must_change_password INTEGER DEFAULT 1;`
2. **Session / Token Extraction**: In `get_user_from_request()`, query DB or inject `must_change_password` into user context object.
3. **Frontend Blocking Modal**:
   - In `templates/base.html`, include `#changePasswordModal`.
   - If `user.must_change_password == 1`, initialize modal with static backdrop (`data-bs-backdrop="static" data-bs-keyboard="false"`) so it cannot be dismissed until password is updated.
   - Show warning alert explaining account security requirement.
4. **API Endpoint (`POST /api/auth/change-password`)**:
   - Validate `old_password` against DB `password_hash`.
   - Validate `new_password` length ($\ge 6$ chars).
   - On success, hash new password, set `must_change_password = 0`, and return success message.

### 18h. Production Readiness: Stripping Demo Login Artifacts
**Checklist before production handover**:
1. Remove "Quick Demo Accounts" boxes, auto-fill buttons, and sample credentials from `templates/login.html`.
2. Ensure clean input focus with standard username/password placeholders and password visibility toggle.
3. Remove unused/stale menu links (e.g. static org chart) from `templates/base.html` so users only access functional modules.

### 18i. Corporate Entity Rebranding & Multi-Surface Term Replacement
**Pattern**: When rebranding an existing dashboard/HRIS to a new corporate identity (e.g., PT Mitsindo):
1. **Search All Occurrences**: Run case-insensitive grep across templates, services, routes, and static JS:
```bash
grep -rn "Previous Company Name" app/ templates/ static/
```
2. **Surfaces to Update**:
   - **Page Titles & Meta**: `<title>` tags in `base.html`, `login.html`, and `register.html`.
   - **Footer & Copyright**: All copyright notices and year spans (e.g. `© 2026 PT Mitsindo. All rights reserved.`).
   - **Document Headers & Footers**: Letterheads and auto-generation disclaimers in `travel.html` (SPPD print layout) and `export_service.py` (ReportLab PDF payslips/exports).
   - **Settings & Config**: Default company name, tax ID (NPWP), email domains (`hr@domain.co.id`), and address in `settings.html` and DB system config tables.
   - **Client JS Dynamic Views**: `app.js` print templates and dynamic popups (e.g. `document.title = 'Payslip - PT Mitsindo'`).
3. **Verification**: Verify visual rendering via browser tools on Login, Dashboard, SPPD, Settings, and PDF download endpoints.

### 18j. Corporate Logo Integration, Alpha Masking & Print Asset Optimization
**Pattern**: Integrating custom client logos across auth cards, navigation sidebars, and document prints (PDF/HTML).
1. **Asset Processing & High-Fidelity Anti-Aliased Alpha Masking**:
   - Avoid raw pixel thresholding alone, which produces jagged edges or leaves white halos against dark sidebars.
   - Compute tight non-white bounding box to remove asymmetric margins.
   - Generate a 4x supersampled circular mask with LANCZOS downsampling for smooth anti-aliased transparency:
```python
from PIL import Image, ImageDraw

def process_logo_to_alpha_circle(src_path, out_path):
    img = Image.open(src_path).convert("RGBA")
    w, h = img.size
    # Detect non-white bounds
    left = min(x for x in range(w) if sum(1 for y in range(h) if any(c < 240 for c in img.getpixel((x,y))[:3])) > 5)
    right = max(x for x in range(w) if sum(1 for y in range(h) if any(c < 240 for c in img.getpixel((x,y))[:3])) > 5)
    top = min(y for y in range(h) if sum(1 for x in range(w) if any(c < 240 for c in img.getpixel((x,y))[:3])) > 5)
    bottom = max(y for y in range(h) if sum(1 for x in range(w) if any(c < 240 for c in img.getpixel((x,y))[:3])) > 5)
    cropped = img.crop((left, top, right, bottom))
    cw, ch = cropped.size
    # 4x Supersampled mask for crisp edge
    scale = 4
    mask = Image.new("L", (cw * scale, ch * scale), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, cw * scale - 1, ch * scale - 1), fill=255)
    mask = mask.resize((cw, ch), Image.Resampling.LANCZOS)
    output = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    output.paste(cropped, (0, 0), mask=mask)
    output.save(out_path, format="PNG")
```
2. **Surfaces to Wire**:
   - **Login & Register**: Center above form card (`<img src="/static/img/logo.png?v=2" class="mb-3" style="width: 80px; height: 80px; object-fit: contain;">`).
   - **Sidebar Header**: Replace icon with `<img src="/static/img/logo.png?v=2" style="width: 38px; height: 38px; object-fit: contain;">` paired with brand text.
   - **Letterheads (SPPD & Payslip HTML)**: Place logo next to company name with flexbox:
     `<div class="letterhead" style="display:flex;align-items:center;justify-content:center;gap:15px;border-bottom:2px solid #1e3a5f;padding-bottom:10px;">`
3. **ReportLab PDF Embedding & Tag Formatting Gotchas**:
   - In ReportLab table cells, raw strings containing `<b>...</b>` or `<font>...</font>` are NOT automatically parsed and will print raw XML tags unless wrapped in `Paragraph("<b>...</b>", style)`.
   - Embed logo in PDF header:
```python
import os
from reportlab.platypus import Image as RLImage, Spacer, Paragraph
logo_path = "/path/to/static/img/logo.png"
if os.path.exists(logo_path):
    elements.append(RLImage(logo_path, width=45, height=45))
    elements.append(Spacer(1, 4))
elements.append(Paragraph("<b>COMPANY NAME</b>", title_style))
```

### 18k. Strict Right-Alignment for Financial Tables & ReportLab Paragraph Gotchas
**Pattern**: Financial figures in payslips, invoices, and travel expense breakdowns must follow strict accounting standards.
1. **Right Alignment Standard**:
   - Header labels (e.g. `Earnings (Rp)`, `Satuan (Rp)`, `Jumlah (Rp)`) AND numeric data rows must both have `alignment=2` (ReportLab) or `text-align: right` (CSS).
   - In ReportLab `Table`, if wrapping text in `Paragraph`, the paragraph style's `alignment=2` overrides the `TableStyle`'s `('ALIGN', (x,y), (-1,-1), 'RIGHT')`. Define dedicated `right_style = ParagraphStyle(..., alignment=2)`.
   - Use `tabular-nums` in CSS (`font-variant-numeric: tabular-nums`) so numbers line up vertically without proportional font jitter.
   - Empty/dash cells (`—`) must also be right-aligned with the currency column.

### 18l. Hierarchical Multi-Tier SPPD Approval & Dynamic Signature Block Rendering
**Pattern**: Travel orders (SPPD) require dynamic approval routing and printed signature blocks based on employee hierarchy:
1. **Approval Routing Logic (`POST /api/travel/{id}/submit`)**:
   - **Board of Commissioners / Managing Director (Tier 3)**: Highest corporate authority. Request is immediately auto-approved (`status = 'approved'`, `director_approved_at = now`) directly to Finance without requiring permission from anyone.
   - **Department Managers / Division Heads (Tier 2)**: Submits directly to the Managing Director (`status = 'pending_director'`, `manager_approved_at = now`), bypassing peer manager review.
   - **Staff / Operational Employees (Tier 1)**: Follows standard 2-tier review (`status = 'pending_manager'`).
2. **Pydantic Schema & Attribute Matching in Travel/Expense Modals (`TravelCreate`)**:
   - When modal form sends cost breakdown (`estimated_cost`, `grand_total`, `transport_cost`, etc.), ensure Pydantic request body explicitly defines all optional cost attributes (`estimated_cost: Optional[float] = 0`).
   - Route logic accessing `body.grand_total or body.estimated_cost` will throw `'TravelCreate' object has no attribute 'estimated_cost'` (HTTP 500) if any referenced attribute is omitted from the Pydantic model definition.
3. **Dynamic Signature Block Rendering (Print / PDF)**:
   - **1 Signatory (Director / Commissioner)**: Single centered column spanning 100% width with label *"Pimpinan / Direksi / Dewan Komisaris"*.
   - **2 Signatories (Division Manager)**: Two equal columns (50% each) — Left: *"Pemohon (Manajer Divisi)"*, Right: *"Disetujui oleh (Direktur Utama)"*.
   - **3 Signatories (Staff)**: Three equal columns (33.3% each) — Left: *"Yang Melaksanakan (Staf Pemohon)"*, Center: *"Mengetahui / Atasan (Manajer Divisi)"*, Right: *"Disetujui oleh (Direktur Utama)"*.

### 18m. Role-Based Dashboard KPI Overview & Aggregation Architecture
**Pattern**: Delivering contextualized performance/KPI overviews tailored to user organizational tiers on the main dashboard:
1. **Backend Aggregation in Route (`@app.get('/dashboard')`)**:
   - **Executive / Director (`director` / `super_admin`)**: Group KPI achievements across all company departments/divisions. Query `departments` $\bowtie$ `employees` $\bowtie$ `employee_kpis` to aggregate headcount, average achievement %, and average score (4.0 scale).
   - **Manager (`manager`)**: Aggregate performance metrics of direct subordinates (`employees WHERE manager_id = ? OR id = ?`). Include indicator count, average achievement, and latest performance review comments.
   - **Staff (`employee`)**: Retrieve personal individual KPI records (`employee_kpis` joined with `kpi_templates`) and recent formal review summary (`performance_reviews`).
2. **Frontend UI Rendering (`dashboard.html`)**:
   - **Director View**: Full-width Executive Summary table showing all divisions, division heads, member counts, progress bars, scores, and status badges.
   - **Manager View**: Subordinate Team KPI Table with per-member achievement progress bars and evaluation notes.
   - **Staff View**: Split 2-column layout — Left: Summary Review Card (Score %, Grade, Reviewer Name, Approval Status); Right: Detailed KPI table (Weight %, Target, Actual, Achievement %, Score /4.0).

### 18n. Live Notification Engine & Topbar Badge Integration for Multi-Tier Workflows
**Pattern**: Ensuring real-time notifications are delivered to designated roles (Manager, Director, Staff) across request lifecycles (Travel/SPPD, Leave, Overtime, Reimbursement):
1. **Database Triggers & Event Notification (`_notify_travel_target`)**:
   - On request submission: query manager/director user IDs and insert record into `notifications` (`user_id`, `title`, `message`, `is_read=0`, `link`).
   - On manager forward/director approval/revision: notify target employee and approvers with clear action summaries and nominal cost amounts.
2. **Topbar Dynamic Dropdown Integration (`app.js` & `base.html`)**:
   - Replace static mock notification items with dynamic API fetch: `App.apiCall('/notifications?limit=10')`.
   - Update unread counter badge (`#notifBadge`) dynamically and toggle display.
   - Wire "Mark all read" header link to `PUT /api/notifications/read-all`.
3. **Form Cost Synchronization**:
   - Ensure backend route logic stores `grand_total` and `estimated_cost` with calculated form values rather than allowing zero-defaults to overwrite computed expenses.

### 18o. Strict RBAC Decision-Maker Action Button Gating on Dynamic Tables
**Pattern**: In multi-tier workflows (Travel/SPPD, Overtime, Reimbursement, Leave), approval and rejection/revision action buttons must be strictly gated in the UI based on user role, hierarchy, and request ownership:
1. **Frontend Action Button Matrix**:
   - `pending_manager`: Approve/Revise buttons (`btnApproveMgr`) must **ONLY** render for users with role `manager` or `super_admin` who are **NOT the owner** of the request (`!isOwner`). The requesting employee must only see `View Detail` (`btnView`).
   - `pending_director`: Approve/Revise buttons (`btnApproveDir`) must **ONLY** render for Director accounts (`role === 'director'` or executive super_admin like `william` / `direktur`). Requesting managers or staff must only see `btnView`.
   - `draft` & `revision_required`: Edit, Submit, Resubmit, and Delete buttons are restricted to `isOwner || isSuperAdmin`.
   - `approved` & `completed`: Print/Download receipt (`btnPrint`) is accessible to owners and approvers; Finance disbursement modal (`btnFinance`) is restricted to Finance department users and `super_admin`.
2. **Backend Guarding**:
   - Every approval/revision route (`/api/{module}/{id}/approve-manager`, `/approve-director`) must verify `approver_id` against database role and forbid self-approval unless explicit executive auto-approval rules apply.

### 18p. Query Hydration for Dynamic Template & Print Rendering (Join Integrity)
**Pattern**: When rendering client-side print templates, PDF exports, or dynamic UI cards (such as SPPD travel orders or payslips), route queries in `main.py` and API endpoints MUST hydrate all organizational relation fields:
1. **Prerequisite Joins**:
   - Always `LEFT JOIN positions p ON e.position_id = p.id` to expose `position_title`.
   - Always `LEFT JOIN employees m ON e.manager_id = m.id` to expose `manager_name`.
2. **Pitfall**: If route queries return only the raw foreign key (`position_id`, `manager_id`), client-side JavaScript conditionals cannot evaluate employee titles or reporting chains accurately, falling back to default rules (e.g., classifying a Division Manager as regular staff and rendering 3 signatures instead of 2).

### 18q. Separation of Personal Operational Accounts vs Master IT Super Admin
**Pattern**: Avoid binding an active Manager or Director's personal employee profile directly to a generic `super_admin` master role.
1. **Isolation Principle**:
   - **Personal Account (`andisaputra`, etc.)**: Assigned their actual organizational role (`manager` or `director`) linked to their personal `employee_id`. This ensures normal organizational workflows, correct SPPD signature counts (2 signatures), and standard team approvals.
   - **Master IT Account (`admin` / `system`)**: Dedicated solely for IT maintenance, user provisioning, system debugging, and database migrations.
2. **Benefit**: Prevents privilege leakage, self-approval bypasses, and hierarchy confusion in multi-tier audit trails.

### 18r. Manager-Tier SPPD Lifecycle & Subordinate Document Transparency
**Pattern**: When managing travel requests (SPPD) in multi-tier corporate hierarchies:
1. **Manager Self-Edit & Resubmit**: In approval models where Division Manager requests route directly to the Managing Director (`pending_director`), allow managers to edit and resubmit their requests (`PUT /api/travel/{id}` and `POST /api/travel/{id}/submit`) while in `pending_director` or `revision_required` status.
2. **Subordinate Document Visibility**: Always provide the `Print / View SPPD` action button (`btnPrint`) for managers on their subordinates' travel records across all active statuses, allowing managers to inspect the generated official letter and cost breakdowns on demand.
3. **Detail Modal Quick Print**: Embed a direct `Cetak / Lihat Dokumen SPPD` action button inside the generic `#detailModal` footer wired to `downloadReceipt(req.id)` so managers can preview official printable letters directly from the detail view.

### 18r. Date-Duration Auto-Calculation on Form Submission (Quantity vs Grand Total Sync)
**Pattern**: In expense and travel reimbursement forms where daily allowance/meals have a duration quantity (e.g. `daily_allowance_days`, `meal_days`):
1. **Symptom**: Form displays correct grand total (e.g., Rp 3,300,000 for 6 days), but printed SPPD/receipt displays Qty `1 hr` or `1 paket` with nominal Rp 550,000.
2. **Root Cause**: If the duration input is left blank (relying on UI placeholder "Auto"), naive `parseInt(input.value) || 0` on form submit sends 0 or 1 to the backend instead of computing the real date difference.
3. **Fix**: In the submit handler, always calculate fallback auto-days from date inputs before building the payload:
```javascript
const depVal = fd.get('departure_date');
const retVal = fd.get('return_date');
let autoDays = 1;
if (depVal && retVal) {
    autoDays = Math.max(1, Math.ceil((new Date(retVal) - new Date(depVal)) / (1000 * 60 * 60 * 24)) + 1);
}
const dailyAllowDays = dailyAllowDaysInput ? (parseInt(dailyAllowDaysInput) || autoDays) : autoDays;
```

### 18s. Fingerprint Machine Excel Import Architecture & Smart Employee Fuzzy Matching
**Pattern**: Transitioning from employee self-service clock-in/out to centralized GA/HR import of biometric/RFID fingerprint machine export files:
1. **Workflow Architecture**:
   - Disable/remove manual `Clock In` and `Clock Out` buttons from regular user views to eliminate phantom self-reporting.
   - Provide a dedicated **"Import Excel Fingerprint"** modal restricted to General Affair (GA) managers and `super_admin`.
   - Regular employees and division managers retain read-only transparency over their attendance logs, late flags, and monthly summaries.
2. **Robust Multi-Strategy Employee Matching Algorithm**:
   - Biometric machines often store nickname variants (e.g., `"Lim Mei Ie"` for Mei, `"Auw Septiawati Keristin"` for Kristin, `"Joko Agus Widodo"` for Joko).
   - Implement a 3-tier resolution engine:
     1. *Explicit Synonym / Nickname Map*: Static lookup table for known alias overrides (`CUSTOM_NAME_MAP`).
     2. *Case-Insensitive Exact & Substring Match*: Match if database name is contained in Excel cell or vice versa.
     3. *Token Set Intersection*: Tokenize alphanumeric words with `re.findall(r'\w+', name)` and check if word sets overlap.
3. **Batch Parse & Upsert Engine (`POST /api/attendance/import-excel`)**:
   - Use `openpyxl` with `data_only=True` to evaluate cell formulas.
   - Scan rows dynamically to detect header start row (handling variable metadata banners).
   - Parse diverse date representations (`datetime` object, `date` object, or strings like `27-Jul-26`, `2026-07-27`).
   - Extract raw scan times (`08:23`, `17:30`), late duration, and status notes (sakit `S`, cuti `C`, penugasan/dinas luar, alpa `A`).
   - Perform atomic UPSERT against `(employee_id, date)`: update scan times and status if record exists, or insert new record.
   - Return detailed operational counters: `{imported: N, updated: N, skipped: N, errors: [...]}`.

### 18t. Personal Scoping & Flexible Date/Period Filtering on Ledger Views
**Pattern**: On sensitive employee modules (Attendance logs, Payslips, Personal Overtime logs):
1. **Strict Personal Scoping**:
   - By default, even division managers should only see their personal history on their own ledger page (`WHERE a.employee_id = ?`) to maintain individual privacy.
   - Team summaries should be separated into dedicated manager reports or executive dashboards.
2. **Flexible Period/Month/Year Filtering Pattern**:
   - In FastAPI routes, accept `period: Optional[str] = Query("all")`, `month: Optional[str] = Query(None)`, `year: Optional[str] = Query(None)`, `limit_count: Optional[int] = Query(200)`.
   - Build dynamic SQL clauses using `strftime('%Y-%m', date) = ?` or `strftime('%Y', date) = ?`.
   - In Jinja2 template, provide a unified filter bar with quick buttons (*All, This Month, This Year*), plus dynamic month/year pickers and line-limit selectors.

### 18u. SQLite CHECK Constraint Migration in Live Production
**Symptom**: `sqlite3.IntegrityError: CHECK constraint failed: status IN ('present', 'absent', 'late', 'half_day')` when inserting valid new business states (e.g. `'sick'`, `'leave'`, `'duty'`).
**Root Cause**: SQLite `CHECK` constraints are immutable and cannot be modified with `ALTER TABLE MODIFY COLUMN`.
**Fix**: Execute safe SQLite atomic table replacement:
```python
conn.execute('PRAGMA foreign_keys=OFF;')
conn.execute('BEGIN TRANSACTION;')
conn.execute('''
CREATE TABLE attendance_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    date DATE NOT NULL,
    clock_in TEXT,
    clock_out TEXT,
    status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late', 'half_day', 'sick', 'leave', 'duty', 'holiday')),
    location_lat REAL,
    location_lng REAL,
    notes TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
)
''')
conn.execute('INSERT INTO attendance_new SELECT * FROM attendance;')
conn.execute('DROP TABLE attendance;')
conn.execute('ALTER TABLE attendance_new RENAME TO attendance;')
conn.commit()
```

### 18v. Background Client-Side JS Overwriting Server-Rendered (SSR) Stat Cards
**Symptom**: Server correctly renders filtered stat cards via Jinja2 (`att_stats`), but milliseconds after page load, card numbers suddenly revert to `0` or `-`.
**Root Cause**: Client-side JavaScript (e.g. in `app.js` `loadAttendanceSummary()`) fires asynchronously on page load, fetches an unfiltered or dummy API summary, and directly overwrites DOM elements by ID (`#attPresent`, `#attLate`, `#attAbsent`).
**Fix**: Remove or comment out redundant client-side summary fetchers if stats are already computed server-side via SQL in `main.py`, or ensure the JS fetch passes matching period/filter parameters.

### 18w. Check-In-Only Attendance Workflows & Table Simplification
**Pattern**: In companies where biometric/RFID clock-in is tracked without a mandatory clock-out/checkout policy:
1. **Attendance Classification**: Any valid check-in scan (`clock_in != None`) marks the employee as `present` (or `late` if beyond threshold).
2. **Table UI Simplification**: Remove the "Jam Scan Pulang" (Clock Out) column entirely from ledger tables to eliminate visual clutter and misleading empty cells.

### 18x. Centralized Payroll Batch Processing & Employee Payslip Scoping
**Pattern**:
1. **Admin/GA Batch Process**: GA Manager/Super Admin triggers `/api/payroll/process` for selected month/year. The backend calculates base salary + allowances - deductions for all active employees and inserts records into `payroll` table with `status='processed'`.
2. **Strict Payslip Scoping**: Non-admin employees navigating to `/payroll` or requesting `/api/payroll/payslip/{emp_id}` are strictly restricted to their own `employee_id`. Provide instant ReportLab PDF download via `/api/payroll/payslip/{emp_id}/pdf`.

### 18y. Live Notifications Polling & Payroll Batch Execution
**Pattern**:
1. **Live Notification Polling**: Implement client-side periodic polling (e.g. `setInterval(() => App.initNotifications(), 30000)`) in `app.js` with unread badge updates and category icons.
2. **Real End-to-End Batch Execution**: Never leave batch processing actions (e.g. `processPayroll`) as cosmetic `showToast()` stubs. Always prompt for period (Month/Year), invoke the backend endpoint (`POST /api/payroll/process`), write rows to database, and reload view.

### 18z. Physical File vs Dynamic Official PDF Generation for Document Downloads
**Pattern**: When building employee file/document management modules (`/documents`, `/employees/{id}`):
1. **Symptom**: User clicks "Download" button on a document row and gets a broken link, missing file error, or a dead `alert('Mengunduh...')` stub.
2. **Dual-Resolution Download Route (`/api/documents/download/{doc_id}`)**:
   - Query document metadata joined with `employees`, `positions`, and `departments`.
   - Verify RBAC: regular employee can only access their own documents; managers/admins can access assigned team documents.
   - **Path A (Physical File Exists)**: If `doc.file_path` exists on the server filesystem, return `FileResponse(path=file_path, filename=doc.file_name, media_type="application/octet-stream")`.
   - **Path B (Dynamic Fallback Generation)**: If the document record exists in DB but no physical file was uploaded (e.g. demo data, digitized records, or migrated archives), dynamically generate an official PDF document via ReportLab with company letterhead, employee identity, validity status, and HR GA validation stamp on the fly.
3. **Frontend Wiring**: Always use `<a href="/api/documents/download/{{ d.id }}" target="_blank">` instead of JS click alerts so the browser naturally triggers download/preview.

### 18aa. Sequential Business Document Numbering (SPPD / Invoices / Letters)
**Pattern**: In enterprise workflows where official reference numbers must start from a specific sequence (e.g., SPPD-001) independent of internal primary keys (`id`):
1. **Database Schema**: Add dedicated `doc_number` / `sppd_number INTEGER DEFAULT NULL` column to preserve historical records while numbering official business runs.
2. **Atomic Sequence Generation**:
   ```python
   cur_seq = conn.execute("SELECT COALESCE(MAX(sppd_number), 0) + 1 FROM travel_requests WHERE sppd_number IS NOT NULL")
   next_num = cur_seq.fetchone()[0]
   ```
3. **Format Formatting**: Display padded strings like `SPPD-001` or `Nomor: SPPD/001/HRIS/2026` across table views, detail cards, and print templates (`SPPD-${String(sppd_number).padStart(3, '0')}`).

### 18ab. Subdomain Deployment via cPanel Reverse-Proxy Bridge to VPS Backend
**Pattern**: Connecting a live corporate subdomain (e.g., `hris.domain.co.id`) hosted on shared cPanel to a FastAPI / Node backend running on a VPS:
1. **cPanel UAPI Setup**: Add subdomain via cPanel API / Jupiter theme (`SubDomain/addsubdomain`) pointing to an isolated document root.
2. **High-Performance PHP Bridge (`index.php`)**: When shared hosting disables Apache `mod_proxy` / `RewriteRule [P]`, deploy a transparent streaming cURL forwarder in `index.php` with `.htaccess` rewriting `RewriteRule ^(.*)$ index.php [QSA,L]`.
3. **Headers & Protocol Passing**: Forward `$_SERVER['REQUEST_METHOD']`, raw body (`php://input`), and inject `X-Forwarded-Host: $_SERVER['HTTP_HOST']` and `X-Forwarded-Proto: https` to preserve JWT cookies and SSL state.

See `references/hris-operational-patterns.md` for extended production examples and edge cases.

## Export Feature Pattern (Excel + PDF)

### export_service.py
```python
import sqlite3
import io
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

DB_PATH = "/path/to/app.db"

def _get_db(db=None):
    if db:
        return db, False
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn, True

def _build_workbook(headers, rows):
    wb = Workbook()
    ws = wb.active
    # Header styling: #003366 fill, white text, bold
    # Alternating row colors: #F2F2F2
    # Auto-width columns
    # Freeze panes on header
    # Thin borders
    return wb.save(io.BytesIO()).getvalue()  # Return bytes

def export_employees_excel(db=None, filters=None):
    conn, opened = _get_db(db)
    # JOIN employees, departments, positions
    # Build rows, return _build_workbook(headers, rows)
```

### exports.py (Route)
```python
import io, sqlite3
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.services.export_service import export_employees_excel, export_employees_pdf

router = APIRouter(prefix="/exports", tags=["exports"])

@router.get("/employees")
async def export_employees(format: str = Query("excel")):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        if format == "pdf":
            data = export_employees_pdf(conn)
            return StreamingResponse(io.BytesIO(data),
                media_type="application/pdf",
                headers={"Content-Disposition": f'inline; filename="employees.pdf"'})
        data = export_employees_excel(conn)
        return StreamingResponse(io.BytesIO(data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="employees.xlsx"'})
    finally:
        conn.close()
```

### HTML Export Button (Dropdown)
```html
<div class="btn-group">
  <a href="/api/exports/employees?format=excel" class="btn btn-success btn-sm">
    <i class="fas fa-file-excel me-1"></i> Export Excel
  </a>
  <button type="button" class="btn btn-success btn-sm dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown">
    <span class="visually-hidden">Toggle Dropdown</span>
  </button>
  <ul class="dropdown-menu">
    <li><a class="dropdown-item" href="/api/exports/employees?format=excel"><i class="fas fa-file-excel me-2 text-success"></i>Excel</a></li>
    <li><a class="dropdown-item" href="/api/exports/employees?format=pdf"><i class="fas fa-file-pdf me-2 text-danger"></i>PDF</a></li>
  </ul>
</div>
```

## Multi-Agent Build Pattern

| Agent | Output |
|-------|--------|
| DB Agent | database.py, schemas.py, auth_service.py, seed |
| API Agent | All route files + main.py |
| Frontend Agent | All templates + CSS + JS |

After agents finish: manual integration pass for mismatches.

### Post-Merge Verification Checklist
```bash
# 1. Check import mismatches
grep -rn "from app" app/routes/ | while read line; do
    func=$(echo "$line" | grep -oP 'import \K\w+')
    grep -rn "def $func" app/ || echo "MISSING: $func"
done

# 2. Check router prefixes
grep "include_router" main.py

# 3. Check table names in routes vs DB
sqlite3 app.db ".tables"
grep -rn "FROM " app/routes/

# 4. Verify ALL sidebar links have routes (CRITICAL)
grep -oP 'href="/\K[a-z-]+' templates/base.html | sort -u | while read page; do
    curl -s -o /dev/null -w "$page: %{http_code}\n" -H "Cookie: token=$TOKEN" http://localhost:PORT/$page
done

# 5. Verify template paths match routes
grep -A5 'def.*_page' main.py | grep 'TemplateResponse'
```

## Design Guidelines
- Bootstrap 5 CDN only, Corporate Blue palette, Inter font
- Status badges: green=active, yellow=on_leave, red=inactive
- Data tables with alternating rows, pagination, bulk actions
- NO glassmorphism, NO AI-purple, NO centered-3-cards
- Export buttons: green (btn-success) with Excel/PDF dropdown
- **UI/UX Refinement Workflows (AdminKit / Enterprise standard)**:
  - Integrate rules from `taste-skill`, `redesign-existing-projects`, and AdminKit design system.
  - Eliminate overly busy AI gradients or synthetic card designs; keep surfaces flat with subtle borders (`1px solid #e9ecef`), soft layered shadows (`0 0 0.875rem 0 rgba(33, 37, 41, 0.05)`), 500/600 font weights, and `tabular-nums` on NIK/dates/amounts.
  - **Zero Backend Disruption Constraint**: When adapting themes/templates (like AdminKit, Tabler), customize solely via CSS custom properties and theme overrides in `style.css` without modifying existing route endpoints, Jinja2 template bindings, or API payload contracts.
  - When updating stylesheets, bust browser caches via base.html versioning (`/static/css/style.css?v=YYYYMMDD_N`).

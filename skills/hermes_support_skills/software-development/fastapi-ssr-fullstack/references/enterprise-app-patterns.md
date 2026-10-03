# FastAPI + Jinja2 + Bootstrap 5 Enterprise App Reference

## Project Structure (HRIS-style)
```
project/
├── main.py                    # FastAPI app, page routes, auth middleware, router registration
├── app/
│   ├── database.py            # SQLite schema (CREATE TABLE), init_db(), seed_data()
│   ├── models/schemas.py      # Pydantic Create/Out/Base variants
│   ├── services/
│   │   ├── auth_service.py    # JWT create/decode, bcrypt hash, get_current_user
│   │   └── export_service.py  # openpyxl + reportlab export functions
│   └── routes/
│       ├── auth.py            # POST /login, /logout, GET /me
│       ├── employees.py       # CRUD with RBAC
│       ├── travel.py          # Multi-level approval workflow
│       ├── exports.py         # PDF/Excel download endpoints
│       └── ...                # One router per domain module
├── templates/
│   ├── base.html              # Sidebar nav (22+ items) + topbar + block content
│   ├── login.html
│   └── pages/                 # One template per page
├── static/
│   ├── css/style.css
│   └── js/app.js
└── project.db
```

## Router Registration Pattern (main.py)
```python
api_prefix = "/api"

# Import all routers
from app.routes.auth import router as auth_router
from app.routes.employees import router as employees_router
# ... more routers ...

# Register with api_prefix — NEVER forget prefix
app.include_router(auth_router, prefix=api_prefix)
app.include_router(employees_router, prefix=api_prefix)
# ...

# Page routes (Jinja2 templates)
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("pages/dashboard.html", 
        {"request": request, "user": user, "active_page": "dashboard"})
```

## Sidebar → Route → Template Verification
Every sidebar link needs all three:
1. `base.html`: `<a href="/travel" class="sidebar-link {% if active_page == 'travel' %}active{% endif %}">`
2. `main.py`: `@app.get("/travel", response_class=HTMLResponse)` with matching template
3. `templates/pages/travel.html`: dedicated template

## RBAC Pattern (3 roles)
```python
def get_user_from_request(request):
    token = request.cookies.get("token") or request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        return payload  # {id, username, role, employee_id}
    except:
        return None

# In route
user = get_user_from_request(request)
if not user:
    return RedirectResponse(url="/", status_code=302)

# Role-based filtering
if user["role"] == "employee":
    query += " WHERE employee_id = ?"
    params.append(user["employee_id"])
```

## Multi-Level Approval Workflow (Travel/Procurement)
State machine: `draft → pending_manager → pending_director → approved → completed`
Reject branches: `pending_manager → rejected`, `pending_director → rejected`
Finance: separate `finance_status` field (not_submitted → submitted → processing → completed)

## Export Service Pattern
- Excel: openpyxl Workbook, style header #003366 white text, alternating #F2F2F2, auto-width
- PDF: reportlab SimpleDocTemplate, landscape A4, Table with TableStyle
- Always use sync `sqlite3.connect()` (not async aiosqlite)
- Return `StreamingResponse(io.BytesIO(bytes), media_type=..., headers={Content-Disposition: ...})`

## Color Palette
- Primary: `#1e3a5f`, Secondary: `#2c5282`, Background: `#f8f9fa`
- Success: `#28a745`, Warning: `#ffc107`, Danger: `#dc3545`

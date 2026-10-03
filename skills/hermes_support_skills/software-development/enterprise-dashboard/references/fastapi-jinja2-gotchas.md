# FastAPI + Jinja2 Common Gotchas

## 1. Static Files + url_for (CRITICAL)

`url_for('static', filename='...')` **BREAKS** when static files are mounted with `app.mount()`.

**Symptom**: `starlette.routing.NoMatchFound: No route exists for name "static"`

**Cause**: `app.mount("/static", ...)` creates a sub-application, not a named route. `url_for()` can't resolve it.

**Fix**: Use direct paths in templates:
```html
<!-- ❌ BROKEN -->
<link href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/app.js') }}"></script>

<!-- ✅ WORKS -->
<link href="/static/css/style.css">
<script src="/static/js/app.js"></script>
```

**Note**: `url_for()` works fine with FastAPI's `StaticFiles` when using `add_route` pattern instead of `mount`, but `mount` is the standard approach.

---

## 2. HTML Input name Attributes (CRITICAL)

JS form access via `form.fieldName.value` requires the `name` HTML attribute, not just `id`.

**Symptom**: `form.username` returns empty object `{}`, `form.username.value` returns `""`

**Cause**: `form.username` uses the `name` attribute for lookup, not `id`.

**Fix**:
```html
<!-- ❌ BROKEN -->
<input type="text" id="username" placeholder="Enter username">

<!-- ✅ WORKS -->
<input type="text" id="username" name="username" placeholder="Enter username">
```

---

## 3. JWT Cookie vs localStorage (CRITICAL for Server-Rendered Apps)

FastAPI Jinja2 templates are server-rendered. The server reads JWT from **cookies**, but JS typically stores tokens in **localStorage**. You must set BOTH.

**Symptom**: Login succeeds (API returns 200), but redirect to `/dashboard` sends you back to login.

**Cause**: Server can't find JWT cookie, so `get_user_from_request()` returns None, triggering redirect to `/`.

**Fix in JS login handler**:
```javascript
// After successful login API call
if (result.token) {
    localStorage.setItem('hris_token', result.token);        // For API calls
    document.cookie = 'token=' + result.token + '; path=/; max-age=' + (60*60*24);  // For page routes
    window.location.href = '/dashboard';
}
```

**Server reads cookie**:
```python
def get_user_from_request(request: Request):
    token = request.cookies.get("token")  # ← reads from cookie
    if not token:
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
    # ... decode and return user
```

---

## 4. Table Name Mismatch (Multi-Agent Projects)

When multiple agents write routes and DB schema independently, they often use different table names.

**Symptom**: `sqlite3.OperationalError: no such table: employee_documents`

**Common mismatches**:
- Route uses `employee_documents` but DB has `documents`
- Route uses `users` but DB has `accounts`
- Route uses `departments` but DB has `dept`

**Fix**: Always verify actual DB table names after schema creation:
```python
import sqlite3
conn = sqlite3.connect('app.db')
tables = [r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()]
print(tables)  # Check actual names
conn.close()
```

---

## 5. Password Seed Mismatch (Multi-Agent Projects)

Different agents may seed different default passwords.

**Symptom**: Login returns "Invalid username or password" even with correct credentials.

**Cause**: Agent 1 seeded with `password123`, Agent 2 expects `admin123`.

**Fix**: Standardize in database.py seed function:
```python
from app.services.auth_service import get_password_hash

async def seed_users(db):
    pwd_hash = get_password_hash("admin123")  # ← standardized
    await db.execute(
        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        ("admin", pwd_hash, "super_admin")
    )
```

---

## 6. Server Process Management

Uvicorn in background mode doesn't auto-reload on file changes.

**Fix**: Always kill old process before restarting:
```bash
# Find and kill process on port
fuser -k 8090/tcp
sleep 1

# Start fresh
cd /path/to/project
source venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8090 &
```

**Check if server is running**:
```bash
ss -tlnp | grep 8090
curl -s -o /dev/null -w "%{http_code}" http://localhost:8090/
```

---

## 7. aiosqlite Row Factory

To access columns by name (not just index), set row_factory:
```python
import aiosqlite

db = await aiosqlite.connect("app.db")
db.row_factory = aiosqlite.Row  # ← enables dict-like access

cursor = await db.execute("SELECT * FROM users WHERE id = ?", (1,))
row = await cursor.fetchone()
print(row["username"])  # Works with Row factory
# print(row[1])         # Also works (index-based)
```

---

## 8. Template Rendering Without Auth Context

When a template expects `user` variable but route doesn't pass it:

**Symptom**: `jinja2.exceptions.UndefinedError: 'user' is undefined`

**Fix**: Always pass user context to templates:
```python
@app.get("/dashboard")
async def dashboard_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse(
        "pages/dashboard.html",
        {"request": request, "user": user}  # ← always include user
    )
```

---

## 9. CORS Issues (API from Different Origin)

If frontend and backend run on different ports during development:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ← specify origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 10. SQLite Async Concurrency

SQLite has limited concurrent write support. For multi-user apps:
- Use WAL mode: `PRAGMA journal_mode=WAL`
- Use connection pooling or per-request connections
- For production, consider PostgreSQL with asyncpg

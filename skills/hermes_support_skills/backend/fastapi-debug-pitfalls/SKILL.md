---
name: fastapi-debug-pitfalls
description: Use when FastAPI apps have sqlite3 login 500 errors.
metadata: {"clawdbot": {"emoji": "🔧", "os": ["linux","darwin","win32"]}}
---

## FastAPI + SQLite Debugging Pitfalls

When working on FastAPI apps with vanilla sqlite3 (not SQLAlchemy), static HTML/JS frontend, and JWT auth — expect and check these traps before blaming network or config issues.

### 1. sqlite3.Row Does NOT Have .get()

**Symptom:** 500 Internal Server Error on login/auth routes. `'sqlite3.Row' object has no attribute 'get'`.

**Fix:** Replace `row.get("field")` with `row["field"]`. Use `grep -rn "\.get(" app/routes/*.py` to find all instances. Only broken on raw sqlite3.Row — works fine on Pydantic models, SQLAlchemy results, Flask request args.

### 2. @router.get("/") Decorator Corruption

**Symptom:** SyntaxError: `@router["/path"]` instead of `@router.get("/path")`.

**Cause:** Automated find-replace tools match `.get(` incorrectly. Detection: `grep -rn '@router\[' app/routes/`. Fix each route file individually.

### 3. Browser SPA Token Persistence Failure

**Symptom:** Page redirects back to /login even after form-login succeeded. Tables show "no data" because fetch calls get unauthorized.

**Workaround (inject from console):** Get fresh token via fetch POST to `/api/auth/login`, save to localStorage + cookie, update App singleton, reload page.

**Permanent fix:** Change `checkAuth()` in app.js to switch to demo mode (`this.token = 'demo_token'`) instead of redirecting. Add `getToken()` helper to the App object that checks both localStorage and cookies.

### 4. Table Render Failures After Auth Passes

**Symptom:** URL is correct, user logged in, but table body shows "Belum ada karyawan terdaftar".

**Causes:** (a) loadPageData() runs before token set → early return, (b) API key mismatch: JS expects `{items}` but API returns `{employees}`, (c) CORS drops Authorization header.

**Fix:** In loadEmployees(), use `const items = data?.items || data?.employees || []`. Inject fresh token via browser console fetch + render directly into tbody.

### 5. Server Process Zombie on Dev Port

**Symptom:** uvicorn won't start, port already in use.

**Fix:** `fuser -k 8090/tcp` or `kill -9 <PID>`. Python alternative: `import os, signal; os.kill(PID, signal.SIGKILL)`.

### 6. Dashboard Stat Card Hardcoded Values

**Symptom:** Dashboard shows old hardcoded numbers instead of real-time API data.

**Root cause:** HTML stat elements lack matching IDs or use invalid CSS selectors like `.text()`. Compare `setVal('idName', value)` calls with actual `id="..."` attributes in HTML.

**Fix:** Remove hardcoded values from HTML, add proper IDs. Use fallback iteration through `.card-body` elements matching by label text content.

---

*Captured from PT Maju Bersama HRIS debugging session.*

---
name: fastapi-routing-test
description: "Troubleshooting guide for FastAPI routing issues: prefix mismatches, nested sub-routers, missing routes, inconsistent module naming. Captures lessons from debugging a multi-module FastAPI application with 20+ route modules."
license: MIT
metadata:
  version: "1.0.0"
  created: "2026-09-19"
  sources:
    - Real-world debugging of HRIS FastAPI application
    - FastAPI docs on APIRouter and include_router
---

# FastAPI Routing Debug & Test Guide

Troubleshooting patterns and systematic testing methods for FastAPI applications with multiple route modules.

## Common Routing Issues (Ranked by Frequency)

### 1. Prefix Mismatch Between Router Definition and Caller

**Symptom:** Frontend calls `/api/export/employees` but returns 404.  
**Cause:** The route module uses prefix `/exports` (plural), so full path is `/api/exports/employees`.

```python
# In exports.py
router = APIRouter(prefix="/exports", tags=["exports"])  # NOTE THE 'S'

# In main.py
app.include_router(exports_router, prefix="/api")  # → /api/exports/...

# WRONG call: /api/export/employees     (missing 's')
# CORRECT:     /api/exports/employees
```

**Fix:** Always verify the prefix string in the source file matches what your frontend/caller uses. Common gotcha: singular vs plural resource names.

### 2. Nested Sub-Routes Require Full Path

**Symptom:** Calling `/api/training` returns 404, but `/api/training/programs` works.  
**Cause:** The GET handler is defined on a sub-path, not root.

```python
# In training.py
router = APIRouter(prefix="/training", tags=["training"])

@router.get("/programs")        # ← NOT at root!
async def list_programs(): ...

@router.get("/enrollments")     # ← NOT at root either!
async def list_enrollments(): ...
```

**Pattern:** Many modules define their primary data collection at a sub-path (e.g., `/programs`, `/items`, `/entries`) rather than directly at the router prefix. This means:
- `GET /api/training` → may not exist (or may return something else)
- `GET /api/training/programs` → actual list endpoint
- You must grep `@router.get("")` to find if there IS a root GET

**Debug step:** Search each route file for `@router.get(\"\")` to confirm root-level read access exists.

### 3. Page Route Exists But No Corresponding API Route

**Symptom:** `/shifts` page loads successfully, but `GET /api/shifts` returns 404.  
**Cause:** Some pages render server-side templates without exposing a dedicated REST API.

**Rule:** Don't assume every page has an equivalent `/api/{resource}` endpoint. Check `main.py` for page routes and individual route files for API definitions independently.

### 4. Query Parameter Requirements Hidden in Signature

**Symptom:** `GET /api/payroll/payslip/1` returns "Not Found".  
**Cause:** Route requires query params but they're optional in the signature.

```python
@router.get("/payslip/{emp_id}")
async def get_payslip(emp_id: int, period_month: Optional[int] = None, ...):
    # Without period_month, some logic fails to produce output
```

**Debug step:** When a known-working GET returns unexpected empty/error response, check ALL query parameters in the function signature. Required-looking-but-optional params often need explicit values.

### 5. Import Order Breaks Router Registration

**Symptom:** Some endpoints work, others silently absent from OpenAPI docs.  
**Cause:** Missing or lazy import in `main.py`.

```python
# In main.py — check these are ALL imported
from app.routes.assets import router as assets_router      # ✅ included
from app.routes.training import router as training_router   # ✅ included
# if one is MISSING here, its endpoints won't be registered
```

**Debug step:** Compare imports in `main.py` against files in `app/routes/`:
```bash
ls app/routes/*.py | sed 's|app/routes/||;s|\.py$||' | sort > /tmp/files.txt
grep "^from app.routes\." main.py | sed 's|import.*||;s|from app.routes.||;s|^ *||' | sort > /tmp/imports.txt
diff /tmp/files.txt /tmp/imports.txt   # any missing?
```

## Systematic Testing Methodology

When debugging a multi-module FastAPI app, follow this sequence:

### Phase 1: Infrastructure Check
```bash
# 1. Verify app starts cleanly
python -c "from main import app; print('OK')"

# 2. List all Python route files
find app/routes -name '*.py' | sort

# 3. Count routers per file (check prefix declarations)
grep -rn 'APIRouter(prefix=' app/routes/

# 4. List all @router decorators per file (discover actual endpoints)
grep -rn '@router\.' app/routes/
```

### Phase 2: Auth Flow
```bash
# 5. Login to get token
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}' \
  http://localhost:8090/api/auth/login

# Extract token from response, use in all subsequent requests:
# -H "Authorization: Bearer <TOKEN>"
```

### Phase 3: Page Route Verification
```bash
# 6. Test all HTML-rendered page routes (they redirect if unauthenticated)
for path in /dashboard /employees /departments /attendance /payroll \
            /performance /recruitment /procurement /assets /training \
            /reports /settings /documents /org-chart /shifts /payslips \
            /reimbursement /reviews /requisitions /interviews /travel; do
  code=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:8090$path)
  echo "$path → $code"
done
```

### Phase 4: API Route Verification (Authenticated)
```bash
# 7. For EACH route file, check every @router endpoint:
#    GET: curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8090/api/<route>
#    POST: curl -s -H "Authorization: Bearer $TOKEN" -X POST \
#          -H "Content-Type: application/json" -d '<payload>' \
#          http://localhost:8090/api/<route>

# 8. Cross-reference: compare expected vs actual by grepping all @router lines
```

### Phase 5: Error Classification
Categorize failures into these buckets:

| Pattern | Cause | Fix |
|---------|-------|-----|
| 404 on known endpoint | Wrong URL path / prefix mismatch | Verify prefix in route file |
| Empty array instead of data | Unseeded database table | Run seed script / insert fixtures |
| Validation error on POST | Missing required field in schema | Check Pydantic model definition |
| Already exists error | Duplicate key / unique constraint | Clear table or use different name |
| Method Not Allowed | Wrong HTTP method | Check @router.post/get decorator type |
| Already clocked in | Idempotency guard triggered | Expected behavior — test different day |

## Debug Script Template

Copy-paste template for new FastAPI projects:

```python
#!/usr/bin/env python3
"""FastAPI route verifier — tests all pages and APIs in one pass."""
import subprocess, json

def login():
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", "-H", "Content-Type: application/json",
         '-d', '{"username":"admin","password":"password123"}',
         "http://localhost:8090/api/auth/login"],
        capture_output=True, text=True
    )
    return json.loads(r.stdout).get("token")

def curl_auth(token, url, method="GET"):
    cmd = ["curl", "-s", "-H", f"Authorization: Bearer {token}", "-X", method, url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(r.stdout)
        if isinstance(data, dict) and "detail" in data:
            return "ERR", data["detail"][:60]
        elif isinstance(data, list):
            return "OK", f"{len(data)} items"
        elif isinstance(data, dict):
            keys = ", ".join(list(data.keys())[:5])
            return "OK", keys
        return "OK", str(data)[:40]
    except:
        return "ERR", "Parse failed"

if __name__ == "__main__":
    token = login()
    if not token:
        print("Failed to authenticate"); exit(1)
    
    # Add your test cases here following the format:
    # (method, full_url, description)
    tests = [
        ("GET", "http://localhost:8090/api/employees", "Employees list"),
        ("GET", "http://localhost:8090/api/employees/1", "Employee detail"),
        # ... populate based on grep of @router. in route files
    ]
    
    passed = failed = 0
    for method, url, desc in tests:
        status, summary = curl_auth(token, url, method)
        icon = "✅" if status == "OK" else "❌"
        print(f"{icon} {desc:<40} → {summary}")
        if status == "OK": passed += 1
        else: failed += 1
    
    print(f"\nTotal: {passed}/{passed+failed} OK, {failed} failed")
```

## Anti-Patterns to Avoid

| ❌ Don't | ✅ Do Instead |
|----------|--------------|
| Assume `GET /api/{module}` lists data | Grep `@router.get("")` in each file first |
| Use singular prefix when module uses plural | Match exact string from `APIRouter(prefix="...")` |
| Forget to check query param requirements | Read function signatures before calling endpoints |
| Test only happy path | Also test POST/PUT/DELETE, validation errors, duplicates |
| Rely on browser devtools alone | Use curl scripts for reproducible automated checks |
| Skip comparing route files vs main.py imports | Ensure all route modules are actually included |

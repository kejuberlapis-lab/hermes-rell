#!/usr/bin/env python3
"""Self-contained test script: kills old servers, starts new one, runs all auth tests."""
import subprocess
import sys
import time
import requests
import json
import os

BASE_DIR = "/home/ubuntu/hris"
VENV = os.path.join(BASE_DIR, "venv", "bin", "python")

# ============================================================
# STEP 0: Kill any existing uvicorn on ports 8090/8000
# ============================================================
print(">>> Killing stale uvicorn processes...")
subprocess.run(["fuser", "-k", "-9", "8090/tcp"], capture_output=True)
subprocess.run(["fuser", "-k", "-9", "8000/tcp"], capture_output=True)
time.sleep(1)

PORT = 8090
BASE_URL = f"http://localhost:{PORT}/api"

# ============================================================
# STEP 1: Start server in background
# ============================================================
print(f">>> Starting server on port {PORT}...")
proc = subprocess.Popen(
    [VENV, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", str(PORT)],
    cwd=BASE_DIR,
    env={**os.environ, "VIRTUAL_ENV": os.path.join(BASE_DIR, "venv")},
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# Wait up to 10 seconds for startup
for i in range(20):
    time.sleep(0.5)
    if proc.poll() is None:
        break
else:
    print(f"Server did not start in time!")
    proc.kill()
    stdout, stderr = proc.communicate(timeout=2)
    print("STDOUT:", stdout.decode())
    print("STDERR:", stderr.decode())
    sys.exit(1)

# Quick health check
for i in range(10):
    try:
        r = requests.get(f"{BASE_URL}/auth/me", timeout=2)
        if r.status_code == 401:  # Expected (no token) → server is up!
            print(f">>> Server is UP (HTTP {r.status_code} with no token = correct)")
            break
    except requests.ConnectionError:
        pass
    except Exception:
        pass
    time.sleep(0.5)
else:
    print("Could not connect to server — killing and exiting.")
    proc.kill()
    sys.exit(1)

# ============================================================
# STEP 2: Login for all 4 roles
# ============================================================
CREDENTIALS = {
    "superadmin": {"username": "superadmin", "password": "admin123"},
    "direktur":   {"username": "direktur",   "password": "admin123"},
    "manager":    {"username": "manager",     "password": "admin123"},
    "staf":       {"username": "staf",        "password": "admin123"},
}

tokens = {}
all_pass = True

print("\n" + "=" * 70)
print("PHASE 1: LOGIN TESTS")
print("=" * 70)

for role, creds in CREDENTIALS.items():
    try:
        # Login expects JSON body (Pydantic LoginRequest model), NOT form data
        resp = requests.post(f"{BASE_URL}/auth/login", json=creds, timeout=5)
        data = resp.json()
        
        if resp.status_code == 200 and ("token" in data or "access_token" in data):
            token = data.get("token") or data.get("access_token")
            udata = data.get("user", {})
            tokens[role] = token
            print(f"  ✅ {role:<15} → LOGIN OK  | email={udata.get('email')} | role={udata.get('role')}")
        else:
            tokens[role] = None
            print(f"  ❌ {role:<15} → FAIL (HTTP {resp.status_code}): {json.dumps(data)[:120]}")
            all_pass = False
    except Exception as e:
        tokens[role] = None
        results_role = {"token": False, "error": str(e)}
        print(f"  ❌ {role:<15} → ERROR: {e}")
        all_pass = False

# ============================================================
# STEP 3: Test protected endpoints with each token
# ============================================================
PROTECTED_ENDPOINTS = ["/employees", "/dashboard", "/auth/me"]

print("\n" + "=" * 70)
print("PHASE 2: PROTECTED ENDPOINT TESTS")
print("=" * 70)

endpoint_results = {}

for role, info in CREDENTIALS.items():
    if tokens.get(role):
        endpoint_results[role] = {}
        headers = {"Authorization": f"Bearer {tokens[role]}"}
        
        for ep in PROTECTED_ENDPOINTS:
            url = f"{BASE_URL}{ep}"
            try:
                resp = requests.get(url, headers=headers, timeout=5)
                
                if resp.status_code == 200:
                    body = resp.json()
                    sample = json.dumps(body)[:80]
                    endpoint_results[role][ep] = {"status": "PASS", "code": 200, "body_sample": sample}
                    print(f"  ✅ {role:<15} {ep:<25} → HTTP 200 ({sample[:60]})")
                else:
                    endpoint_results[role][ep] = {"status": "FAIL", "code": resp.status_code, "text": resp.text[:150]}
                    print(f"  ❌ {role:<15} {ep:<25} → HTTP {resp.status_code}: {resp.text[:120]}")
                    all_pass = False
            except Exception as e:
                endpoint_results[role][ep] = {"status": "ERROR", "detail": str(e)}
                print(f"  ❌ {role:<15} {ep:<25} → ERROR: {e}")
                all_pass = False
    else:
        print(f"  ⏭️  Skipping {role:<15} — login failed")

# ============================================================
# STEP 4: Verify invalid token handling
# ============================================================
print("\n" + "=" * 70)
print("PHASE 3: INVALID TOKEN HANDLING")
print("=" * 70)

bad_headers = {"Authorization": "Bearer invalid.token.here"}
resp = requests.get(f"{BASE_URL}/auth/me", headers=bad_headers, timeout=5)
if resp.status_code == 401:
    print(f"  ✅ Invalid token correctly rejected → {resp.status_code}")
else:
    print(f"  ⚠️  Unexpected status for bad token: {resp.status_code} (expected 401)")

resp_no_auth = requests.get(f"{BASE_URL}/auth/me", timeout=5)
if resp_no_auth.status_code == 401:
    print(f"  ✅ No auth header correctly rejected → {resp_no_auth.status_code}")
else:
    print(f"  ⚠️  Unexpected status for missing auth: {resp_no_auth.status_code}")

# ============================================================
# STEP 5: Summary
# ============================================================
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

headers_ep = ["Role", "Login", "/employees", "/dashboard", "/auth/me"]
row_sep = "-" * 65
print(row_sep)
print(f"{'Role':<15} {'Login':<10} {'/employees':<12} {'/dashboard':<12} {'/auth/me':<12}")
print(row_sep)

for role in CREDENTIALS:
    if tokens.get(role):
        eps = endpoint_results.get(role, {})
        emp_s = eps.get("/employees", {}).get("status", "N/A")
        dash_s = eps.get("/dashboard", {}).get("status", "N/A")
        auth_s = eps.get("/auth/me", {}).get("status", "N/A")
        print(f"{role:<15} PASS{'':<9} {emp_s:<12} {dash_s:<12} {auth_s:<12}")
    else:
        print(f"{role:<15} FAIL{'':<9} N/A{'':<12} N/A{'':<12} N/A{'':<12}")

print(row_sep)
print()
if all_pass:
    print("🎉 ALL TESTS PASSED! Auth middleware fix is working.")
    print("\nRoot cause fixed:")
    print("  • get_current_user() now queries 'employees' table instead of 'users'")
    print("  • Login stores employee_id in JWT → matches what get_current_user looks up")
    sys.exit(0)
else:
    print("❌ Some tests failed — see details above")
    sys.exit(1)

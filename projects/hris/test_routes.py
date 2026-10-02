"""Smoke test for HRIS API routes."""
import requests
import sys

BASE = 'http://localhost:8090'
passed = 0
failed = 0

def check(name, r, expected_status=None, check_func=None):
    global passed, failed
    ok = True
    if expected_status and r.status_code != expected_status:
        ok = False
    if check_func and not check_func(r):
        ok = False
    status = "PASS" if ok else "FAIL"
    if not ok:
        failed += 1
        print(f"  {status} {name}: got {r.status_code}, expected {expected_status}")
        try:
            print(f"    body: {r.json()}")
        except:
            print(f"    body: {r.text[:200]}")
    else:
        passed += 1
        print(f"  {status} {name}")

# Login
r = requests.post(f'{BASE}/api/auth/login', json={"username": "admin", "password": "password123"})
check("POST /api/auth/login", r, 200, lambda r: "token" in r.json())
token = r.json()["token"]
H = {"Authorization": f"Bearer {token}"}

# Me
r = requests.get(f'{BASE}/api/auth/me', headers=H)
check("GET /api/auth/me", r, 200)

# Departments
r = requests.post(f'{BASE}/api/departments', headers=H, json={"name": "QA", "code": "QA", "description": "Quality Assurance"})
check("POST /api/departments", r, 201)
r = requests.get(f'{BASE}/api/departments', headers=H)
check("GET /api/departments", r, 200)
r = requests.get(f'{BASE}/api/departments/1', headers=H)
check("GET /api/departments/1", r, 200)
r = requests.put(f'{BASE}/api/departments/1', headers=H, json={"description": "Updated"})
check("PUT /api/departments/1", r, 200)

# Employees
r = requests.post(f'{BASE}/api/employees', headers=H, json={
    "employee_id_str": "EMP-NEW", "full_name": "Test User",
    "email": "test@co.com", "department_id": 1, "position_id": 4, "hire_date": "2026-01-01"
})
check("POST /api/employees", r, 201)
r = requests.get(f'{BASE}/api/employees', headers=H)
check("GET /api/employees", r, 200)
r = requests.get(f'{BASE}/api/employees/1', headers=H)
check("GET /api/employees/1", r, 200)
r = requests.put(f'{BASE}/api/employees/1', headers=H, json={"phone": "12345"})
check("PUT /api/employees/1", r, 200)

# Attendance
r = requests.post(f'{BASE}/api/attendance/clock-in', headers=H)
check("POST /api/attendance/clock-in", r, 200)
r = requests.post(f'{BASE}/api/attendance/clock-out', headers=H)
check("POST /api/attendance/clock-out", r, 200)
r = requests.get(f'{BASE}/api/attendance', headers=H)
check("GET /api/attendance", r, 200)
r = requests.get(f'{BASE}/api/attendance/summary/1', headers=H)
check("GET /api/attendance/summary/1", r, 200)

# Overtime
r = requests.post(f'{BASE}/api/overtime', headers=H, json={"date": "2026-09-07", "hours": 2, "reason": "Deadline"})
check("POST /api/overtime", r, 201)
r = requests.get(f'{BASE}/api/overtime', headers=H)
check("GET /api/overtime", r, 200)
r = requests.put(f'{BASE}/api/overtime/1', headers=H, json={"status": "approved"})
check("PUT /api/overtime/1", r, 200)

# Leave
r = requests.post(f'{BASE}/api/leave', headers=H, json={
    "leave_type_id": 1, "start_date": "2026-09-10", "end_date": "2026-09-12", "reason": "Vacation"
})
check("POST /api/leave", r, 201)
r = requests.get(f'{BASE}/api/leave', headers=H)
check("GET /api/leave", r, 200)
r = requests.get(f'{BASE}/api/leave/balances', headers=H)
check("GET /api/leave/balances", r, 200)
r = requests.put(f'{BASE}/api/leave/1', headers=H, json={"status": "approved"})
check("PUT /api/leave/1", r, 200)

# Payroll
r = requests.post(f'{BASE}/api/payroll/process', headers=H, json={"period_month": 9, "period_year": 2026})
check("POST /api/payroll/process", r, 200)
r = requests.get(f'{BASE}/api/payroll', headers=H)
check("GET /api/payroll", r, 200)
r = requests.get(f'{BASE}/api/payroll/payslip/1?period_month=9&period_year=2026', headers=H)
check("GET /api/payroll/payslip/1", r, 200)
r = requests.post(f'{BASE}/api/payroll/payslip/1/pdf?period_month=9&period_year=2026', headers=H)
check("POST /api/payroll/payslip/1/pdf", r, 200)

# Performance
r = requests.post(f'{BASE}/api/performance/kpis', headers=H, json={
    "employee_id": 1, "period": "2026-Q3", "target": "100", "actual": "85", "score": 85
})
check("POST /api/performance/kpis", r, 201)
r = requests.get(f'{BASE}/api/performance/kpis', headers=H)
check("GET /api/performance/kpis", r, 200)
r = requests.post(f'{BASE}/api/performance/okrs', headers=H, json={
    "employee_id": 1, "objective": "Ship features", "key_result": "Ship 5 features", "progress": 60
})
check("POST /api/performance/okrs", r, 201)
r = requests.get(f'{BASE}/api/performance/okrs', headers=H)
check("GET /api/performance/okrs", r, 200)
r = requests.post(f'{BASE}/api/performance/reviews', headers=H, json={
    "employee_id": 1, "reviewer_id": 1, "period": "2026-Q3", "score": 4.2, "review_type": "manager"
})
check("POST /api/performance/reviews", r, 201)
r = requests.get(f'{BASE}/api/performance/reviews', headers=H)
check("GET /api/performance/reviews", r, 200)

# Recruitment
r = requests.post(f'{BASE}/api/recruitment/requisitions', headers=H, json={"title": "Senior Dev", "department_id": 1})
check("POST /api/recruitment/requisitions", r, 201)
r = requests.get(f'{BASE}/api/recruitment/requisitions', headers=H)
check("GET /api/recruitment/requisitions", r, 200)
r = requests.post(f'{BASE}/api/recruitment/applicants', headers=H, json={
    "requisition_id": 1, "full_name": "Jane", "email": "jane@co.com"
})
check("POST /api/recruitment/applicants", r, 201)
r = requests.get(f'{BASE}/api/recruitment/applicants', headers=H)
check("GET /api/recruitment/applicants", r, 200)
r = requests.post(f'{BASE}/api/recruitment/interviews', headers=H, json={
    "applicant_id": 1, "interviewer_id": 1, "scheduled_at": "2026-09-15T10:00:00"
})
check("POST /api/recruitment/interviews", r, 201)
r = requests.get(f'{BASE}/api/recruitment/interviews', headers=H)
check("GET /api/recruitment/interviews", r, 200)

# Procurement
r = requests.post(f'{BASE}/api/procurement', headers=H, json={"title": "Laptops", "estimated_cost": 5000})
check("POST /api/procurement", r, 201)
r = requests.get(f'{BASE}/api/procurement', headers=H)
check("GET /api/procurement", r, 200)
r = requests.put(f'{BASE}/api/procurement/1', headers=H, json={"status": "approved"})
check("PUT /api/procurement/1", r, 200)

# Assets
r = requests.post(f'{BASE}/api/assets', headers=H, json={
    "name": "MacBook Pro", "category": "IT Equipment", "serial_number": "SN001"
})
check("POST /api/assets", r, 201)
r = requests.get(f'{BASE}/api/assets', headers=H)
check("GET /api/assets", r, 200)
r = requests.post(f'{BASE}/api/assets/1/assign', headers=H, json={"employee_id": 1})
check("POST /api/assets/1/assign", r, 200)
r = requests.post(f'{BASE}/api/assets/1/unassign', headers=H)
check("POST /api/assets/1/unassign", r, 200)

# Notifications
r = requests.get(f'{BASE}/api/notifications', headers=H)
check("GET /api/notifications", r, 200)

# Training
r = requests.post(f'{BASE}/api/training/programs', headers=H, json={
    "title": "Python Basics", "trainer": "John", "start_date": "2026-09-15", "end_date": "2026-09-20"
})
check("POST /api/training/programs", r, 201)
r = requests.get(f'{BASE}/api/training/programs', headers=H)
check("GET /api/training/programs", r, 200)
r = requests.post(f'{BASE}/api/training/enrollments', headers=H, json={"training_id": 1, "employee_id": 1})
check("POST /api/training/enrollments", r, 201)
r = requests.get(f'{BASE}/api/training/enrollments', headers=H)
check("GET /api/training/enrollments", r, 200)

# Reimbursement
r = requests.post(f'{BASE}/api/reimbursements', headers=H, json={"category": "travel", "amount": 150, "description": "Taxi"})
check("POST /api/reimbursements", r, 201)
r = requests.get(f'{BASE}/api/reimbursements', headers=H)
check("GET /api/reimbursements", r, 200)
r = requests.put(f'{BASE}/api/reimbursements/1', headers=H, json={"status": "approved"})
check("PUT /api/reimbursements/1", r, 200)

# Dashboard
r = requests.get(f'{BASE}/api/dashboard', headers=H)
check("GET /api/dashboard", r, 200)

# Pages
for page in ["/", "/dashboard", "/employees", "/departments", "/attendance", "/overtime", "/leave", "/payroll", "/performance", "/recruitment", "/procurement", "/assets", "/training", "/reports", "/settings"]:
    r = requests.get(f'{BASE}{page}')
    check(f"GET {page}", r, 200)

print(f"\n{'='*50}")
print(f"Results: {passed} passed, {failed} failed out of {passed+failed}")
if failed:
    sys.exit(1)

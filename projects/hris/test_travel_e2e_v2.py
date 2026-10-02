#!/usr/bin/env python3
"""End-to-end Travel Request workflow tester - corrected."""
import subprocess
import json
import sqlite3
import os
from datetime import datetime

DB_PATH = "/home/ubuntu/hris/hris.db"
BASE_URL = "http://localhost:8090/api"

def run_cmd(cmd):
    """Run a shell command list and return (stdout_str, exit_code)."""
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout.strip(), r.returncode

def json_parse(text):
    """Parse JSON, return dict or empty dict on failure."""
    try:
        return json.loads(text)
    except Exception:
        return {"_raw": text[:500]}

# ===========================================================================
# STEP 1: CREATE travel request with cost breakdown
# ===========================================================================
print("\n=== STEP 1: CREATE TRAVEL REQUEST ===\n")

create_payload = {
    "employee_id": 1,
    "destination": "Surabaya",
    "purpose": "Meeting client kontrak Q4",
    "departure_date": "2026-10-15",
    "return_date": "2026-10-18",
    "transport_type": "plane",
    "accommodation_needed": 1,
    "transport_cost": 1500000,
    "accommodation_rate_per_night": 450000,
    "accommodation_nights": 3,
    "daily_allowance_per_day": 200000,
    "daily_allowance_days": 4,
    "meals_per_day": 150000,
    "meal_days": 4,
    "additional_items": "",
    "notes": "Perlu approval cepat",
    "grand_total": 4250000,
    "accommodation_total": 1350000,
    "daily_allowance_total": 800000,
    "meal_total": 600000
}

cmd_create = [
    "curl", "-s", "-X", "POST", f"{BASE_URL}/travel",
    "-H", "Content-Type: application/json",
    "-d", json.dumps(create_payload)
]
stdout, _ = run_cmd(cmd_create)
resp_create = json_parse(stdout)
print(f"Response: {json.dumps(resp_create, indent=2)}")

if "id" in resp_create and isinstance(resp_create["id"], int):
    travel_id = resp_create["id"]
    print(f"[PASS] Created travel_id={travel_id}")
else:
    print("[FAIL] Could not create travel request")
    # Write minimal report and exit
    os.makedirs("/home/ubuntu/hris", exist_ok=True)
    with open("/home/ubuntu/hris/test_travel_results.txt", "w") as f:
        f.write("TRAVEL REQUEST E2E TEST REPORT\nGenerated: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        f.write("\n[FAIL] Step 1: POST /api/travel failed\n{}\n".format(stdout))
    exit(1)

# ===========================================================================
# STEP 2: GET detail right after creation (verify cost breakdown)
# ===========================================================================
print("\n=== STEP 2: VERIFY COST BREAKDOWN IN RESPONSE ===\n")

cmd_get1 = ["curl", "-s", f"{BASE_URL}/travel/{travel_id}"]
stdout, _ = run_cmd(cmd_get1)
detail1 = json_parse(stdout)

cost_fields = {
    "transport_cost": detail1.get("transport_cost"),
    "accommodation_rate_per_night": detail1.get("accommodation_rate_per_night"),
    "accommodation_nights": detail1.get("accommodation_nights"),
    "accommodation_total": detail1.get("accommodation_total"),
    "daily_allowance_per_day": detail1.get("daily_allowance_per_day"),
    "daily_allowance_days": detail1.get("daily_allowance_days"),
    "daily_allowance_total": detail1.get("daily_allowance_total"),
    "meals_per_day": detail1.get("meals_per_day"),
    "meal_days": detail1.get("meal_days"),
    "meal_total": detail1.get("meal_total"),
    "grand_total": detail1.get("grand_total"),
}

print("Cost breakdown after creation:")
for k, v in cost_fields.items():
    print(f"  {k}: {v}")

cost_intact = all(cost_fields[k] == create_payload.get(k.replace('_', ' ') if ' ' in k else k.split('_')[0]) 
                  for k in cost_fields if isinstance(cost_fields.get(k), (int, float)))
# More precise checks
checks_pass = True
expected = {
    "transport_cost": 1500000,
    "accommodation_rate_per_night": 450000,
    "accommodation_nights": 3,
    "accommodation_total": 1350000,
    "daily_allowance_per_day": 200000,
    "daily_allowance_days": 4,
    "daily_allowance_total": 800000,
    "meals_per_day": 150000,
    "meal_days": 4,
    "meal_total": 600000,
    "grand_total": 4250000,
}
for field, exp_val in expected.items():
    actual_val = detail1.get(field)
    status = "OK" if actual_val == exp_val else "MISMATCH"
    if status == "MISMATCH":
        checks_pass = False
    print(f"  [{status}] {field}: expected={exp_val}, got={actual_val}")

# ===========================================================================
# STEP 3: SUBMIT for manager approval
# ===========================================================================
print("\n=== STEP 3: SUBMIT FOR MANAGER APPROVAL ===\n")

cmd_submit = ["curl", "-s", "-X", "POST", f"{BASE_URL}/travel/{travel_id}/submit"]
stdout, _ = run_cmd(cmd_submit)
resp_submit = json_parse(stdout)
print(f"Response: {resp_submit}")

cmd_get_after_submit = ["curl", "-s", f"{BASE_URL}/travel/{travel_id}"]
stdout, _ = run_cmd(cmd_get_after_submit)
detail_submit = json_parse(stdout)
print(f"Status after submit: {detail_submit.get('status')}")

# ===========================================================================
# STEP 4: MANAGER APPROVE
# ===========================================================================
print("\n=== STEP 4: MANAGER APPROVE ===\n")

cmd_mgr = [
    "curl", "-s", "-X", "POST", f"{BASE_URL}/travel/{travel_id}/approve-manager",
    "-H", "Content-Type: application/json",
    "-d", json.dumps({"manager_id": 1, "notes": "Approved untuk meeting klien penting."})
]
stdout, _ = run_cmd(cmd_mgr)
resp_mgr = json_parse(stdout)
print(f"Response: {resp_mgr}")

cmd_get_mgr = ["curl", "-s", f"{BASE_URL}/travel/{travel_id}"]
stdout, _ = run_cmd(cmd_get_mgr)
detail_mgr = json_parse(stdout)
print(f"Status: {detail_mgr.get('status')}, manager_approved_at: {detail_mgr.get('manager_approved_at')}")

# ===========================================================================
# STEP 5: DIRECTOR APPROVE
# ===========================================================================
print("\n=== STEP 5: DIRECTOR APPROVE ===\n")

cmd_dir = [
    "curl", "-s", "-X", "POST", f"{BASE_URL}/travel/{travel_id}/approve-director",
    "-H", "Content-Type: application/json",
    "-d", json.dumps({"director_id": 1, "notes": "Disetujui, budget ada."})
]
stdout, _ = run_cmd(cmd_dir)
resp_dir = json_parse(stdout)
print(f"Response: {resp_dir}")

cmd_get_dir = ["curl", "-s", f"{BASE_URL}/travel/{travel_id}"]
stdout, _ = run_cmd(cmd_get_dir)
detail_dir = json_parse(stdout)
print(f"Status: {detail_dir.get('status')}, director_approved_at: {detail_dir.get('director_approved_at')}")

# ===========================================================================
# STEP 6: FINANCE SUBMIT
# ===========================================================================
print("\n=== STEP 6: FINANCE SUBMIT ===\n")

cmd_fsub = [
    "curl", "-s", "-X", "POST", f"{BASE_URL}/travel/{travel_id}/finance-submit",
    "-H", "Content-Type: application/json",
    "-d", json.dumps({"amount": 4250000, "notes": "Submit biaya ke finance"})
]
stdout, _ = run_cmd(cmd_fsub)
resp_fsub = json_parse(stdout)
print(f"Response: {resp_fsub}")

cmd_get_fsub = ["curl", "-s", f"{BASE_URL}/travel/{travel_id}"]
stdout, _ = run_cmd(cmd_get_fsub)
detail_fsub = json_parse(stdout)
print(f"Finance status: {detail_fsub.get('finance_status')}")

# ===========================================================================
# STEP 7: FINANCE PROCESS
# ===========================================================================
print("\n=== STEP 7: FINANCE PROCESS ===\n")

cmd_fproc = [
    "curl", "-s", "-X", "POST", f"{BASE_URL}/travel/{travel_id}/finance-process",
    "-H", "Content-Type: application/json",
    "-d", json.dumps({"actual_cost": 4500000, "advance_payment": 2000000, "notes": "Advance payment Rp 2jt"})
]
stdout, _ = run_cmd(cmd_fproc)
resp_fproc = json_parse(stdout)
print(f"Response: {resp_fproc}")

cmd_get_fproc = ["curl", "-s", f"{BASE_URL}/travel/{travel_id}"]
stdout, _ = run_cmd(cmd_get_fproc)
detail_fproc = json_parse(stdout)
print(f"Finance status: {detail_fproc.get('finance_status')}, actual_cost: {detail_fproc.get('actual_cost')}")

# ===========================================================================
# STEP 8: FINANCE COMPLETE
# ===========================================================================
print("\n=== STEP 8: FINANCE COMPLETE ===\n")

cmd_fcomp = [
    "curl", "-s", "-X", "POST", f"{BASE_URL}/travel/{travel_id}/finance-complete",
    "-H", "Content-Type: application/json",
    "-d", json.dumps({"finance_processed_by": 1, "notes": "All settled. Net payment after advance: Rp 2.5jt"})
]
stdout, _ = run_cmd(cmd_fcomp)
resp_fcomp = json_parse(stdout)
print(f"Response: {resp_fcomp}")

# ===========================================================================
# STEP 9: FINAL VERIFICATION via GET
# ===========================================================================
print("\n=== STEP 9: FINAL VERIFICATION (GET) ===\n")

cmd_final = ["curl", "-s", f"{BASE_URL}/travel/{travel_id}"]
stdout, _ = run_cmd(cmd_final)
detail_final = json_parse(stdout)

print(f"Final status: {detail_final.get('status')}")
print(f"Finance status: {detail_final.get('finance_status')}")
print(f"Manager approved: {bool(detail_final.get('manager_approved_at'))}")
print(f"Director approved: {bool(detail_final.get('director_approved_at'))}")
print(f"Finance processed at: {detail_final.get('finance_processed_at')}")
print(f"Actual cost: {detail_final.get('actual_cost')}")
print(f"Advance payment: {detail_final.get('advance_payment')}")

# Final cost breakdown
final_costs = {
    "transport_cost": detail_final.get("transport_cost"),
    "accommodation_total": detail_final.get("accommodation_total"),
    "daily_allowance_total": detail_final.get("daily_allowance_total"),
    "meal_total": detail_final.get("meal_total"),
    "grand_total": detail_final.get("grand_total"),
}
print("\nFinal cost breakdown:")
for k, v in final_costs.items():
    print(f"  {k}: {v}")

# Final timestamps
final_ts = {
    "created_at": detail_final.get("created_at"),
    "updated_at": detail_final.get("updated_at"),
    "manager_approved_at": detail_final.get("manager_approved_at"),
    "director_approved_at": detail_final.get("director_approved_at"),
    "finance_processed_at": detail_final.get("finance_processed_at"),
}
print("\nTimestamps:")
for k, v in final_ts.items():
    print(f"  {k}: {v}")

# ===========================================================================
# STEP 10: DATABASE VERIFICATION via sqlite3 Python module
# ===========================================================================
print("\n=== STEP 10: DATABASE VERIFICATION ===\n")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.execute("SELECT * FROM travel_requests WHERE id = ?", (travel_id,))
row = cur.fetchone()
conn.close()

db = dict(row) if row else None

if db:
    print("Database record found for travel_id={}".format(travel_id))
    
    # Verify cost breakdown in DB
    db_checks = {
        "transport_cost": db.get("transport_cost"),
        "accommodation_rate_per_night": db.get("accommodation_rate_per_night"),
        "accommodation_nights": db.get("accommodation_nights"),
        "accommodation_total": db.get("accommodation_total"),
        "daily_allowance_per_day": db.get("daily_allowance_per_day"),
        "daily_allowance_days": db.get("daily_allowance_days"),
        "daily_allowance_total": db.get("daily_allowance_total"),
        "meals_per_day": db.get("meals_per_day"),
        "meal_days": db.get("meal_days"),
        "meal_total": db.get("meal_total"),
        "grand_total": db.get("grand_total"),
        "actual_cost": db.get("actual_cost"),
        "advance_payment": db.get("advance_payment"),
        "status": db.get("status"),
        "finance_status": db.get("finance_status"),
    }
    for k, v in db_checks.items():
        print(f"  {k}: {v}")
    
    db_cost_ok = (
        db.get("transport_cost") == 1500000 and
        db.get("accommodation_total") == 1350000 and
        db.get("daily_allowance_total") == 800000 and
        db.get("meal_total") == 600000 and
        db.get("grand_total") == 4250000 and
        db.get("actual_cost") == 4500000 and
        db.get("advance_payment") == 2000000
    )
    db_status_ok = db.get("status") == "completed" and db.get("finance_status") == "completed"
    db_ts_ok = all([db.get("manager_approved_at"), db.get("director_approved_at"), db.get("finance_processed_at")])
    
    print(f"\n  DB Cost OK: {db_cost_ok}")
    print(f"  DB Status OK: {db_status_ok}")
    print(f"  DB Timestamps OK: {db_ts_ok}")
else:
    print("ERROR: No DB record found!")
    db = {}

# ===========================================================================
# GENERATE REPORT
# ===========================================================================
report_lines = []
report_lines.append("=" * 70)
report_lines.append("TRAVEL REQUEST E2E TEST REPORT")
report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append(f"Travel ID: {travel_id}")
report_lines.append("=" * 70)
report_lines.append("")

# Determine overall pass/fail for each step
overall_results = []

def add_result(label, passed, detail=""):
    marker = "PASS" if passed else "FAIL"
    line = "  [{}] {}".format(marker, label)
    if detail:
        line += "\n       -> {}".format(detail)
    report_lines.append(line)
    overall_results.append((label, passed))

# Step 1
add_result("Step 1 - CREATE travel request", 
           isinstance(resp_create.get("id"), int),
           "travel_id={}".format(travel_id))

# Step 2 - Cost breakdown integrity
add_result("Step 2 - Cost breakdown after creation",
           checks_pass,
           json.dumps({k: {"expected": expected[k], "got": detail1.get(k)} for k, v in expected.items()}))

# Step 3
add_result("Step 3 - SUBMIT for approval",
           detail_submit.get("status") == "pending_manager",
           "status={}".format(detail_submit.get("status")))

# Step 4
add_result("Step 4 - MANAGER APPROVE",
           detail_mgr.get("status") == "pending_director" and bool(detail_mgr.get("manager_approved_at")),
           "status={}, manager_approved_at={}".format(detail_mgr.get("status"), detail_mgr.get("manager_approved_at")))

# Step 5
add_result("Step 5 - DIRECTOR APPROVE",
           detail_dir.get("status") == "approved" and bool(detail_dir.get("director_approved_at")),
           "status={}, director_approved_at={}".format(detail_dir.get("status"), detail_dir.get("director_approved_at")))

# Step 6
add_result("Step 6 - FINANCE SUBMIT",
           detail_fsub.get("finance_status") == "submitted",
           "finance_status={}".format(detail_fsub.get("finance_status")))

# Step 7
add_result("Step 7 - FINANCE PROCESS",
           detail_fproc.get("finance_status") == "processing" and 
           detail_fproc.get("actual_cost") == 4500000 and
           detail_fproc.get("advance_payment") == 2000000,
           "finance_status={}, actual_cost={}, advance_payment={}".format(
               detail_fproc.get("finance_status"), detail_fproc.get("actual_cost"), detail_fproc.get("advance_payment")))

# Step 8
add_result("Step 8 - FINANCE COMPLETE",
           resp_fcomp.get("message") is not None,
           "response={}".format(resp_fcomp.get("message", "")))

# Step 9 - Final verification
final_passed = (detail_final.get("status") == "completed" and 
                detail_final.get("finance_status") == "completed" and
                bool(detail_final.get("manager_approved_at")) and
                bool(detail_final.get("director_approved_at")) and
                bool(detail_final.get("finance_processed_at")))
add_result("Step 9 - FINAL STATUS (API)",
           final_passed,
           "status={}, finance_status={}".format(detail_final.get("status"), detail_final.get("finance_status")))

# Step 10 - DB verification
db_overall = db_cost_ok and db_status_ok and db_ts_ok
add_result("Step 10 - DATABASE VERIFICATION",
           db_overall,
           "status={}, finance_status={}, cost_ok={}, ts_ok={}".format(
               db.get("status"), db.get("finance_status"), db_cost_ok, db_ts_ok))

# Summary
total = len(overall_results)
passed_count = sum(1 for _, p in overall_results if p)
failed_count = total - passed_count

report_lines.append("")
report_lines.append("-" * 70)
report_lines.append("SUMMARY: {} tests | {} PASSED | {} FAILED".format(total, passed_count, failed_count))
report_lines.append("-" * 70)

report_lines.append("")
report_lines.append("DETAILED RESULTS:")
for label, passed in overall_results:
    marker = "PASS" if passed else "FAIL"
    report_lines.append("  [{}] {}".format(marker, label))

report_lines.append("")
report_lines.append("-" * 70)
report_lines.append("WORKFLOW SUMMARY")
report_lines.append("-" * 70)
report_lines.append("")
report_lines.append("Workflow Steps Executed:")
report_lines.append("  1. CREATE travel request (draft status)")
report_lines.append("  2. VERIFY cost breakdown fields persisted correctly")
report_lines.append("  3. SUBMIT for manager approval → pending_manager")
report_lines.append("  4. MANAGER APPROVE → pending_director")
report_lines.append("  5. DIRECTOR APPROVE → approved")
report_lines.append("  6. FINANCE SUBMIT → submitted")
report_lines.append("  7. FINANCE PROCESS → processing (actual_cost=4500000, advance=2000000)")
report_lines.append("  8. FINANCE COMPLETE → completed")
report_lines.append("  9. FINAL GET verification")
report_lines.append("  10. SQLite database verification")

report_lines.append("")
report_lines.append("Cost Breakdown (tersimpan di DB):")
if db:
    report_lines.append("  Transport cost:        Rp {:,.0f}".format(db.get("transport_cost", 0)))
    report_lines.append("  Accommodation rate/night: Rp {:,.0f}".format(db.get("accommodation_rate_per_night", 0)))
    report_lines.append("  Accommodation nights:  {}".format(db.get("accommodation_nights", 0)))
    report_lines.append("  Accommodation total:   Rp {:,.0f}".format(db.get("accommodation_total", 0)))
    report_lines.append("  Daily allowance/day:   Rp {:,.0f}".format(db.get("daily_allowance_per_day", 0)))
    report_lines.append("  Daily allowance days:  {}".format(db.get("daily_allowance_days", 0)))
    report_lines.append("  Daily allowance total: Rp {:,.0f}".format(db.get("daily_allowance_total", 0)))
    report_lines.append("  Meals/day:             Rp {:,.0f}".format(db.get("meals_per_day", 0)))
    report_lines.append("  Meal days:             {}".format(db.get("meal_days", 0)))
    report_lines.append("  Meal total:            Rp {:,.0f}".format(db.get("meal_total", 0)))
    report_lines.append("  Grand total (est):     Rp {:,.0f}".format(db.get("grand_total", 0)))
    report_lines.append("  Actual cost:           Rp {:,.0f}".format(db.get("actual_cost", 0)))
    report_lines.append("  Advance payment:       Rp {:,.0f}".format(db.get("advance_payment", 0)))
    net = (db.get("actual_cost", 0) or 0) - (db.get("advance_payment", 0) or 0)
    report_lines.append("  ──────────────────────────")
    report_lines.append("  Net payment:           Rp {:,.0f}".format(net))

report_lines.append("")
report_lines.append("Approval Timestamps:")
if db:
    report_lines.append("  Created:          {}".format(db.get("created_at")))
    report_lines.append("  Manager Approved: {}".format(db.get("manager_approved_at")))
    report_lines.append("  Director Approved:{}".format(db.get("director_approved_at")))
    report_lines.append("  Finance Processed:{}".format(db.get("finance_processed_at")))
    report_lines.append("  Updated:          {}".format(db.get("updated_at")))

# Issues
issues = [(l, p) for l, p in overall_results if not p]
report_lines.append("")
if issues:
    report_lines.append("-" * 70)
    report_lines.append("ISSUES FOUND")
    report_lines.append("-" * 70)
    report_lines.append("")
    for label, _ in issues:
        report_lines.append("  - {}".format(label))
else:
    report_lines.append("")
    report_lines.append("=" * 70)
    report_lines.append("ALL TESTS PASSED — No issues found.")
    report_lines.append("=" * 70)

report_lines.append("")
report_lines.append("END OF REPORT")
report_lines.append("=" * 70)

# Write report
os.makedirs("/home/ubuntu/hris", exist_ok=True)
report_path = "/home/ubuntu/hris/test_travel_results.txt"
with open(report_path, "w") as f:
    f.write("\n".join(report_lines))

print("\n" + "=" * 60)
print("TEST COMPLETE — Report saved to: {}".format(report_path))
print("Total: {} | Passed: {} | Failed: {}".format(total, passed_count, failed_count))
print("=" * 60)

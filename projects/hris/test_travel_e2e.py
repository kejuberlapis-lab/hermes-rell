"""
End-to-end test for HRIS Travel Request workflow with full cost breakdown.
Tests: CREATE, SUBMIT, MANAGER APPROVE, DIRECTOR APPROVE, FINANCE SUBMIT/PROCESS/COMPLETE.
"""
import sqlite3
import urllib.request
import urllib.error
import json
import sys
from datetime import datetime

BASE = "http://localhost:8090/api/travel"
DB_PATH = "/home/ubuntu/hris/hris.db"

test_results = []  # Each entry: {step, status_code, response, pass_fail}

def post(url_path, data):
    """POST JSON data and return (status_code, parsed_response).
    
    url_path is relative to BASE (i.e., what comes AFTER /api/travel).
    - "" → http://localhost:8090/api/travel  (root/create)
    - "{id}/submit" → http://localhost:8090/api/travel/{id}/submit
    """
    # Strip leading slash if present to avoid double segments
    url_path = url_path.lstrip("/")
    url = f"{BASE}/{url_path}" if url_path else BASE
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode())
        return resp.getcode(), result
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            result = json.loads(raw)
        except Exception:
            result = {"raw_error": raw[:500]}
        return e.code, result


def get(url_path):
    """GET a URL and return (status_code, parsed_response)."""
    url_path = url_path.lstrip("/")
    url = f"{BASE}/{url_path}" if url_path else BASE
    try:
        resp = urllib.request.urlopen(url, timeout=10)
        return resp.getcode(), json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            result = json.loads(raw)
        except Exception:
            result = {"raw_error": raw[:500]}
        return e.code, result


def db_get_record(travel_id):
    """Fetch a single travel request from DB."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT * FROM travel_requests WHERE id = ?", (travel_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def log_step(step_name, status_code, response, expected_codes=None, detail_msg=None):
    """Record a test step result."""
    if expected_codes is None:
        expected_codes = [200, 201]
    passed = status_code in expected_codes
    label = "PASS" if passed else "FAIL"
    test_results.append({
        "step": step_name,
        "status_code": status_code,
        "response": response,
        "pass_fail": label,
        "detail": detail_msg,
    })
    print(f"[{label}] {step_name} -> HTTP {status_code}")
    if isinstance(response, dict) and "message" in response:
        print(f"       Message: {response['message']}")
    elif isinstance(response, dict):
        print(f"       Response: {json.dumps(response, indent=2)}")
    return passed


def main():
    overall_start = datetime.now()
    
    print("=" * 70)
    print("HRIS TRAVEL REQUEST END-TO-END TEST")
    print(f"Started: {overall_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Clean up any previous test records (IDs > current max)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    max_existing_id = cursor.execute("SELECT COALESCE(MAX(id), 0) FROM travel_requests").fetchone()[0]
    conn.close()
    clean_start_id = max_existing_id + 1
    
    # ======================== STEP A: CREATE ========================
    print("\n--- STEP A: CREATE travel request ---")
    travel_data = {
        "employee_id": 1,
        "destination": "Surabaya",
        "purpose": "Meeting client PT Sentosa kontrak Q4",
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
        "notes": "Perlu approval cepat karena tanggal fixed",
        "grand_total": 4250000,
        "accommodation_total": 1350000,
        "daily_allowance_total": 800000,
        "meal_total": 600000
    }
    
    expected_grand = 1500000 + 1350000 + 800000 + 600000  # 4,250,000
    print(f"Expected grand_total: {expected_grand}")
    
    sc, resp = post("/travel", travel_data)
    create_passed = log_step("CREATE /api/travel", sc, resp, [201])
    
    if not create_passed:
        print("\n*** CREATE failed — cannot proceed with rest of workflow ***")
        print("*** Trying to find last record in DB instead... ***")
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute("SELECT MAX(id) FROM travel_requests").fetchone()
        conn.close()
        travel_id = row[0]
    else:
        travel_id = resp["id"]
    
    print(f"\n>>> Travel request created with ID: {travel_id}\n")
    
    # ======================== Read raw DB after CREATE ========================
    print("--- Database read immediately after CREATE ---")
    record = db_get_record(travel_id)
    if record:
        cost_fields = [
            "estimated_cost", "transport_cost", "accommodation_rate_per_night",
            "accommodation_nights", "accommodation_total",
            "daily_allowance_per_day", "daily_allowance_days", "daily_allowance_total",
            "meals_per_day", "meal_days", "meal_total",
            "additional_items", "grand_total"
        ]
        for field in cost_fields:
            val = record.get(field, "N/A")
            sent_val = travel_data.get(field, "N/A")
            match_marker = " ✓" if str(val) == str(sent_val) or \
                (sent_val in (0, '') and (val in (0, '', 0.0))) else " ✗ MISMATCH"
            print(f"  {field:35s}: db={val:<15} sent={sent_val:<15}{match_marker}")
    else:
        print("  Record NOT found in DB!")
    
    # ======================== STEP B: SUBMIT ========================
    print("\n--- STEP B: Submit for manager approval ---")
    sc, resp = post(f"/{travel_id}/submit", {})
    log_step("SUBMIT", sc, resp)
    
    # Verify status changed
    rec = db_get_record(travel_id)
    if rec:
        print(f"  DB status: {rec['status']}")
    
    # ======================== STEP C: MANAGER APPROVE ========================
    print("\n--- STEP C: Manager approve ---")
    sc, resp = post(f"/{travel_id}/approve-manager", {
        "manager_id": 1,
        "notes": "Approved meeting klien penting"
    })
    log_step("MANAGER_APPROVE", sc, resp)
    
    # ======================== STEP D: DIRECTOR APPROVE ========================
    print("\n--- STEP D: Director approve ---")
    sc, resp = post(f"/{travel_id}/approve-director", {
        "director_id": 1,
        "notes": "Disetujui budget ada"
    })
    log_step("DIRECTOR_APPROVE", sc, resp)
    
    # ======================== STEP E: FINANCE SUBMIT ========================
    print("\n--- STEP E: Finance submit ---")
    sc, resp = post(f"/{travel_id}/finance-submit", {
        "amount": 4250000,
        "notes": "Submit ke finance"
    })
    log_step("FINANCE_SUBMIT", sc, resp)
    
    # ======================== STEP F: FINANCE PROCESS ========================
    print("\n--- STEP F: Finance process ---")
    sc, resp = post(f"/{travel_id}/finance-process", {
        "actual_cost": 4500000,
        "advance_payment": 2000000,
        "notes": "Advance payment 2jt"
    })
    log_step("FINANCE_PROCESS", sc, resp)
    
    # ======================== STEP G: FINANCE COMPLETE ========================
    print("\n--- STEP G: Finance complete ---")
    sc, resp = post(f"/{travel_id}/finance-complete", {
        "finance_processed_by": 1,
        "notes": "All settled net payment 2.5jt"
    })
    log_step("FINANCE_COMPLETE", sc, resp)
    
    # ======================== VERIFICATION QUERY ========================
    print("\n" + "=" * 70)
    print("VERIFICATION QUERY — Final DB State")
    print("=" * 70)
    final_rec = db_get_record(travel_id)
    if final_rec:
        display_cols = [
            ("id", "ID"),
            ("employee_id", "Employee ID"),
            ("destination", "Destination"),
            ("status", "Travel Status"),
            ("finance_status", "Finance Status"),
            ("transport_cost", "Transport Cost"),
            ("accommodation_rate_per_night", "Accommodation Rate/Night"),
            ("accommodation_nights", "Accommodation Nights"),
            ("accommodation_total", "Accommodation Total"),
            ("daily_allowance_per_day", "Daily Allowance/Day"),
            ("daily_allowance_days", "Daily Allowance Days"),
            ("daily_allowance_total", "Daily Allowance Total"),
            ("meals_per_day", "Meals Per Day"),
            ("meal_days", "Meal Days"),
            ("meal_total", "Meal Total"),
            ("additional_items", "Additional Items"),
            ("grand_total", "Grand Total"),
            ("estimated_cost", "Estimated Cost"),
            ("actual_cost", "Actual Cost"),
            ("advance_payment", "Advance Payment"),
            ("manager_approved_at", "Manager Approved At"),
            ("director_approved_at", "Director Approved At"),
            ("finance_processed_at", "Finance Processed At"),
        ]
        for col, label in display_cols:
            val = final_rec.get(col, "N/A")
            print(f"  {label:35s}: {val}")
        
        # Verify calculation accuracy
        print("\n--- Calculation Verification ---")
        tc = float(final_rec.get('transport_cost', 0) or 0)
        ac = float(final_rec.get('accommodation_total', 0) or 0)
        dl = float(final_rec.get('daily_allowance_total', 0) or 0)
        ml = float(final_rec.get('meal_total', 0) or 0)
        gt_db = float(final_rec.get('grand_total', 0) or 0)
        calc_gt = tc + ac + dl + ml
        
        print(f"  Transport:     {tc:,.0f}")
        print(f"  Accommodation: {ac:,.0f}")
        print(f"  Daily Allow.:  {dl:,.0f}")
        print(f"  Meals:         {ml:,.0f}")
        print(f"  Sum of parts:   {calc_gt:,.0f}")
        print(f"  Grand total:    {gt_db:,.0f}")
        calc_ok = abs(calc_gt - expected_grand) < 1 and abs(gt_db - expected_grand) < 1
        print(f"  Calculations: {'✓ ACCURATE' if calc_ok else '✗ INACCURATE'}")
        
        # Check timestamps
        print("\n--- Timestamp Checks ---")
        for ts_col, ts_label in [("manager_approved_at", "Manager"), 
                                   ("director_approved_at", "Director"),
                                   ("finance_processed_at", "Finance")]:
            ts = final_rec.get(ts_col)
            print(f"  {ts_label}: {'✓ Has timestamp' if ts else '✗ No timestamp'}")
    else:
        print("Final record NOT found in DB!")
    
    # ======================== SUMMARY ========================
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    total = len(test_results)
    passed = sum(1 for r in test_results if r['pass_fail'] == 'PASS')
    failed = total - passed
    
    for r in test_results:
        icon = "✓" if r['pass_fail'] == 'PASS' else "✗"
        print(f"  {icon} {r['step']:25s} HTTP {r['status_code']}  {r['pass_fail']}")
    
    print(f"\nTotal Steps: {total} | PASSED: {passed} | FAILED: {failed}")
    
    if failed > 0:
        print("\n--- Issues Found ---")
        for r in test_results:
            if r['pass_fail'] == 'FAIL':
                print(f"  FAIL: {r['step']} -> {r['response']}")
    
    # Save report data for file generation
    report = {
        "started_at": overall_start.strftime("%Y-%m-%d %H:%M:%S"),
        "travel_id": travel_id,
        "expected_grand_total": expected_grand,
        "steps": test_results,
        "final_record": final_rec,
        "total": total,
        "passed": passed,
        "failed": failed,
    }
    
    # Write report data as JSON to a temp file for the report generator
    with open('/tmp/test_travel_report_data.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

import subprocess
import json
import sys

BASE = "http://localhost:8090/api"
headers = {"Content-Type": "application/json"}

results = []

# Step 1: CREATE travel request with new cost breakdown structure
print("=== STEP 1: CREATE TRAVEL REQUEST ===")
create_payload = {
    "employee_id": 1,
    "destination": "Surabaya",
    "purpose": "Meeting dengan client PT Sentosa untuk kontrak Q4",
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
    "notes": "Perlu approval cepat karena tanggal fixed"
}

acc_total = 450000 * 3
daily_total = 200000 * 4
meal_total = 150000 * 4
grand_total = 1500000 + acc_total + daily_total + meal_total

create_payload["grand_total"] = grand_total
create_payload["accommodation_total"] = acc_total
create_payload["daily_allowance_total"] = daily_total
create_payload["meal_total"] = meal_total

print(f"Payload: employee={create_payload['employee_id']}, dest={create_payload['destination']}")
print(f"Cost breakdown:")
print(f"  Transport: {create_payload['transport_cost']:,.0f}")
print(f"  Akomodasi: {acc_total:,} ({create_payload['accommodation_nights']} malam x {create_payload['accommodation_rate_per_night']:,.0f})")
print(f"  Uang Harian: {daily_total:,} ({create_payload['daily_allowance_days']} hari x {create_payload['daily_allowance_per_day']:,.0f})")
print(f"  Makan/Minum: {meal_total:,} ({create_payload['meal_days']} hari x {create_payload['meals_per_day']:,.0f})")
print(f"  GRAND TOTAL: {grand_total:,}")

resp = subprocess.run(
    ["curl", "-s", "-X", "POST", f"{BASE}/travel", "-H", headers[0], "-d", json.dumps(create_payload)],
    capture_output=True, text=True
)
result = json.loads(resp.stdout)
print(f"\nResponse: {json.dumps(result, indent=2)}")

if "id" in result:
    travel_id = result["id"]
    results.append({"step": "CREATE", "status": "OK", "id": travel_id})
else:
    print("ERROR creating travel request!")
    sys.exit(1)

# Step 2: SUBMIT for manager approval
print("\n=== STEP 2: SUBMIT FOR MANAGER APPROVAL ===")
resp = subprocess.run(
    ["curl", "-s", "-X", "POST", f"{BASE}/travel/{travel_id}/submit"],
    capture_output=True, text=True
)
result = json.loads(resp.stdout)
print(f"Response: {result}")
results.append({"step": "SUBMIT", "status": "OK"})

# Step 3: GET detail before approval
print("\n=== STEP 3: CHECK DETAIL BEFORE APPROVAL ===")
resp = subprocess.run(
    ["curl", "-s", f"{BASE}/travel/{travel_id}"],
    capture_output=True, text=True
)
detail_before = json.loads(resp.stdout)
print(f"Status: {detail_before.get('status')}")
print(f"Estimated Cost: {detail_before.get('estimated_cost'):,.0f}")
print(f"Grand Total: {detail_before.get('grand_total'):,.0f}")
print(f"Transport Cost: {detail_before.get('transport_cost'):,.0f}")
print(f"Akomodasi Rate: {detail_before.get('accommodation_rate_per_night'):,.0f}")
print(f"Akomodasi Nights: {detail_before.get('accommodation_nights')}")
print(f"Daily Allowance Days: {detail_before.get('daily_allowance_days')}")
print(f"Meal Days: {detail_before.get('meal_days')}")
results.append({"step": "DETAIL_BEFORE", "status": "OK"})

# Step 4: MANAGER APPROVE
print("\n=== STEP 4: MANAGER APPROVE ===")
resp = subprocess.run(
    ["curl", "-s", "-X", "POST", f"{BASE}/travel/{travel_id}/approve-manager",
     "-H", "Content-Type: application/json",
     '-d', json.dumps({"manager_id": 1, "notes": "Approved untuk meeting klien penting."})],
    capture_output=True, text=True
)
result = json.loads(resp.stdout)
print(f"Response: {result}")
results.append({"step": "MANAGER_APPROVE", "status": "OK"})

# Step 5: DIRECTOR APPROVE
print("\n=== STEP 5: DIRECTOR APPROVE ===")
resp = subprocess.run(
    ["curl", "-s", "-X", "POST", f"{BASE}/travel/{travel_id}/approve-director",
     "-H", "Content-Type: application/json",
     '-d', json.dumps({"director_id": 1, "notes": "Disetujui, budget ada."})],
    capture_output=True, text=True
)
result = json.loads(resp.stdout)
print(f"Response: {result}")
results.append({"step": "DIRECTOR_APPROVE", "status": "OK"})

# Step 6: FINANCE SUBMIT
print("\n=== STEP 6: FINANCE SUBMIT ===")
resp = subprocess.run(
    ["curl", "-s", "-X", "POST", f"{BASE}/travel/{travel_id}/finance-submit",
     "-H", "Content-Type: application/json",
     '-d', json.dumps({"amount": grand_total, "notes": "Submit biaya ke finance"})],
    capture_output=True, text=True
)
result = json.loads(resp.stdout)
print(f"Response: {result}")
results.append({"step": "FINANCE_SUBMIT", "status": "OK"})

# Step 7: FINANCE PROCESS
print("\n=== STEP 7: FINANCE PROCESS ===")
proc_data = {"actual_cost": 4500000, "advance_payment": 2000000, "notes": "Advance payment Rp 2jt"}
resp = subprocess.run(
    ["curl", "-s", "-X", "POST", f"{BASE}/travel/{travel_id}/finance-process",
     "-H", "Content-Type: application/json",
     '-d', json.dumps(proc_data)],
    capture_output=True, text=True
)
result = json.loads(resp.stdout)
print(f"Response: {result}")
results.append({"step": "FINANCE_PROCESS", "status": "OK"})

# Step 8: FINANCE COMPLETE
print("\n=== STEP 8: FINANCE COMPLETE ===")
comp_data = {"finance_processed_by": 1, "notes": "All settled. Net payment after advance: Rp 2.5jt"}
resp = subprocess.run(
    ["curl", "-s", "-X", "POST", f"{BASE}/travel/{travel_id}/finance-complete",
     "-H", "Content-Type: application/json",
     '-d', json.dumps(comp_data)],
    capture_output=True, text=True
)
result = json.loads(resp.stdout)
print(f"Response: {result}")
results.append({"step": "FINANCE_COMPLETE", "status": "OK"})

# FINAL CHECK
print("\n=== FINAL VERIFICATION ===")
resp = subprocess.run(
    ["curl", "-s", f"{BASE}/travel/{travel_id}"],
    capture_output=True, text=True
)
final_detail = json.loads(resp.stdout)
print(f"Final Status: {final_detail.get('status')}")
print(f"Finance Status: {final_detail.get('finance_status')}")
print(f"Manager Approved: {bool(final_detail.get('manager_approved_at'))}")
print(f"Director Approved: {bool(final_detail.get('director_approved_at'))}")
print(f"Finance Processed At: {final_detail.get('finance_processed_at')}")
print(f"Aktual Cost tersimpan: {final_detail.get('actual_cost')}")
print(f"Advance Payment tersimpan: {final_detail.get('advance_payment')}")
print(f"Transport Cost: {final_detail.get('transport_cost')}")
print(f"Grand Total: {final_detail.get('grand_total')}")

# Summary table
print("\n" + "="*60)
print("WORKFLOW SUMMARY")
print("="*60)
for r in results:
    marker = "OK" if r["status"] == "OK" else "FAIL"
    status_str = "[ PASS ]" if marker == "OK" else "[ FAIL ]"
    print(f"  {status_str} {r['step']:25s} → {marker}")
print("="*60)
print("COST BREAKDOWN (tersimpan di DB):")
print(f"  Transport:       Rp {final_detail.get('transport_cost', 0):,.0f}")
print(f"  Akomodasi:       Rp {final_detail.get('accommodation_total', 0):,.0f}")
print(f"  Uang Harian:     Rp {final_detail.get('daily_allowance_total', 0):,.0f}")
print(f"  Makan/Minum:     Rp {final_detail.get('meal_total', 0):,.0f}")
print(f"  ──────────────────────────")
print(f"  GRAND TOTAL:     Rp {final_detail.get('grand_total', 0):,.0f}")
print(f"  Actual Cost:     Rp {final_detail.get('actual_cost', 0):,.0f}")
print(f"  Advance Pay:     Rp {final_detail.get('advance_payment', 0):,.0f}")
print(f"  Net Payment:     Rp {(final_detail.get('actual_cost', 0) - final_detail.get('advance_payment', 0)):,.0f}")
print("="*60)

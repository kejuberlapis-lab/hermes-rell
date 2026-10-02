import requests, json

BASE_URL = 'http://localhost:8090/api'

# 1. Login Staf
res = requests.post(f'{BASE_URL}/auth/login', json={'username': 'staf', 'password': 'staff123'})
staf_data = res.json()
staf_token = staf_data['token']
staf_headers = {'Authorization': f'Bearer {staf_token}'}
staf_emp_id = staf_data['user']['employee_id']

print('=== 1. STAF FLOW ===')
print(f'Logged in as Staf: emp_id={staf_emp_id}')

# Travel Submit by Staf
res_travel = requests.post(f'{BASE_URL}/travel', headers=staf_headers, json={
    'employee_id': staf_emp_id,
    'destination': 'Bandung',
    'purpose': 'Kunjungan Cabang',
    'departure_date': '2026-10-01',
    'return_date': '2026-10-03',
    'transport_type': 'car',
    'grand_total': 1200000
})
print(f'Submit Travel: Status {res_travel.status_code}, Resp: {res_travel.json()}')
travel_id = res_travel.json().get('id')

# Submit Travel for Manager Approval
if travel_id:
    res_sub = requests.post(f'{BASE_URL}/travel/{travel_id}/submit', headers=staf_headers)
    print(f'Submit Travel to Manager: Status {res_sub.status_code}, Resp: {res_sub.json()}')

# Get Staf's Own Data
res_my_leave = requests.get(f'{BASE_URL}/leave', headers=staf_headers)
print(f'Staf Leave List: Count = {len(res_my_leave.json().get("leaves", []))}')

res_my_ot = requests.get(f'{BASE_URL}/overtime', headers=staf_headers)
print(f'Staf Overtime List: Count = {len(res_my_ot.json().get("overtime", []))}')

res_my_reimb = requests.get(f'{BASE_URL}/reimbursements', headers=staf_headers)
print(f'Staf Reimbursement List: Count = {len(res_my_reimb.json().get("reimbursements", []))}')


# 2. Login Manager
res_mgr = requests.post(f'{BASE_URL}/auth/login', json={'username': 'manager', 'password': 'manager123'})
mgr_data = res_mgr.json()
mgr_token = mgr_data['token']
mgr_headers = {'Authorization': f'Bearer {mgr_token}'}

print('\n=== 2. MANAGER APPROVAL FLOW ===')
print(f'Logged in as Manager: {mgr_data["user"]["full_name"]}')

# Cek daftar permohonan yang perlu diapprove
res_mgr_leave = requests.get(f'{BASE_URL}/leave', headers=mgr_headers)
pending_leaves = [l for l in res_mgr_leave.json().get('leaves', []) if l.get('status') == 'pending']
print(f'Pending Leaves for Manager: {len(pending_leaves)}')

for l in pending_leaves:
    res_app = requests.put(f'{BASE_URL}/leave/{l["id"]}', headers=mgr_headers, json={'status': 'approved'})
    print(f'  Approve Leave ID {l["id"]}: Status {res_app.status_code}, Resp: {res_app.json()}')

res_mgr_ot = requests.get(f'{BASE_URL}/overtime', headers=mgr_headers)
pending_ot = [o for o in res_mgr_ot.json().get('overtime', []) if o.get('status') == 'pending']
print(f'Pending Overtime for Manager: {len(pending_ot)}')

for o in pending_ot:
    res_app = requests.put(f'{BASE_URL}/overtime/{o["id"]}', headers=mgr_headers, json={'status': 'approved'})
    print(f'  Approve Overtime ID {o["id"]}: Status {res_app.status_code}, Resp: {res_app.json()}')

res_mgr_reimb = requests.get(f'{BASE_URL}/reimbursements', headers=mgr_headers)
pending_reimb = [r for r in res_mgr_reimb.json().get('reimbursements', []) if r.get('status') == 'pending']
print(f'Pending Reimbursement for Manager: {len(pending_reimb)}')

for r in pending_reimb:
    res_app = requests.put(f'{BASE_URL}/reimbursements/{r["id"]}', headers=mgr_headers, json={'status': 'approved'})
    print(f'  Approve Reimbursement ID {r["id"]}: Status {res_app.status_code}, Resp: {res_app.json()}')

if travel_id:
    res_app_trv = requests.post(f'{BASE_URL}/travel/{travel_id}/approve-manager', headers=mgr_headers)
    print(f'Approve Travel ID {travel_id} by Manager: Status {res_app_trv.status_code}, Resp: {res_app_trv.json()}')


# 3. Login Direktur
res_dir = requests.post(f'{BASE_URL}/auth/login', json={'username': 'direktur', 'password': 'director123'})
dir_data = res_dir.json()
dir_token = dir_data['token']
dir_headers = {'Authorization': f'Bearer {dir_token}'}

print('\n=== 3. DIREKTUR APPROVAL & OVERVIEW ===')
print(f'Logged in as Direktur: {dir_data["user"]["full_name"]}')

if travel_id:
    res_dir_trv = requests.post(f'{BASE_URL}/travel/{travel_id}/approve-director', headers=dir_headers)
    print(f'Approve Travel ID {travel_id} by Direktur: Status {res_dir_trv.status_code}, Resp: {res_dir_trv.json()}')

# Overview Dashboard oleh Direktur
res_dir_dash = requests.get(f'{BASE_URL}/dashboard', headers=dir_headers)
print(f'Direktur Dashboard Overview: {res_dir_dash.json()}')

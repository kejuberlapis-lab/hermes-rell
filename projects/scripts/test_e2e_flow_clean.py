import requests, json

BASE_URL = 'http://localhost:8090/api'

# ---------------------------------------------------------
# 1. PERCOBAAN STAF (Ahmad Fauzi - Emp ID: 4)
# ---------------------------------------------------------
res = requests.post(f'{BASE_URL}/auth/login', json={'username': 'staf', 'password': 'staff123'})
staf_data = res.json()
staf_token = staf_data['token']
staf_headers = {'Authorization': f'Bearer {staf_token}'}
staf_emp_id = staf_data['user']['employee_id']

print('=== 1. PERCOBAAN STAF (Ahmad Fauzi) ===')
print(f'Logged in as Staf: emp_id={staf_emp_id}')

# Clock In & Clock Out
res_clockin = requests.post(f'{BASE_URL}/attendance/clock-in', headers=staf_headers, json={'notes': 'Masuk pagi staf'})
print(f'[Attendance] Clock In: Status {res_clockin.status_code}, Resp: {res_clockin.json()}')

res_clockout = requests.post(f'{BASE_URL}/attendance/clock-out', headers=staf_headers, json={'notes': 'Pulang staf'})
print(f'[Attendance] Clock Out: Status {res_clockout.status_code}, Resp: {res_clockout.json()}')

# Overtime Submit
res_ot = requests.post(f'{BASE_URL}/overtime', headers=staf_headers, json={
    'date': '2026-09-20',
    'hours': 2.5,
    'reason': 'Lembur pengerjaan fitur HRIS'
})
ot_id = res_ot.json().get('id')
print(f'[Overtime] Submit: Status {res_ot.status_code}, ID={ot_id}')

# Leave Submit
res_leave = requests.post(f'{BASE_URL}/leave', headers=staf_headers, json={
    'leave_type_id': 1,
    'start_date': '2026-09-25',
    'end_date': '2026-09-26',
    'reason': 'Izin acara keluarga'
})
leave_id = res_leave.json().get('id')
print(f'[Leave] Submit: Status {res_leave.status_code}, ID={leave_id}')

# Reimbursement Submit
res_reimb = requests.post(f'{BASE_URL}/reimbursements', headers=staf_headers, json={
    'category': 'Transport',
    'amount': 150000,
    'description': 'Bensin dinas lapangan'
})
reimb_id = res_reimb.json().get('id')
print(f'[Reimbursement] Submit: Status {res_reimb.status_code}, ID={reimb_id}')

# Travel Submit & Submit to Manager
res_travel = requests.post(f'{BASE_URL}/travel', headers=staf_headers, json={
    'employee_id': staf_emp_id,
    'destination': 'Bandung',
    'purpose': 'Kunjungan Cabang',
    'departure_date': '2026-10-01',
    'return_date': '2026-10-03',
    'transport_type': 'car',
    'grand_total': 1200000
})
travel_id = res_travel.json().get('id')
print(f'[Travel] Create: Status {res_travel.status_code}, ID={travel_id}')

if travel_id:
    res_sub = requests.post(f'{BASE_URL}/travel/{travel_id}/submit', headers=staf_headers)
    print(f'[Travel] Submit to Manager: Status {res_sub.status_code}')

# Cek Data Sendiri oleh Staf
res_my_leave = requests.get(f'{BASE_URL}/leave', headers=staf_headers)
print(f'[Staf Check] Daftar Leave Sendiri: {len(res_my_leave.json().get("leaves", []))} item')

res_my_ot = requests.get(f'{BASE_URL}/overtime', headers=staf_headers)
print(f'[Staf Check] Daftar Overtime Sendiri: {len(res_my_ot.json().get("overtime", []))} item')

res_my_reimb = requests.get(f'{BASE_URL}/reimbursements', headers=staf_headers)
print(f'[Staf Check] Daftar Reimbursement Sendiri: {len(res_my_reimb.json().get("reimbursements", []))} item')


# ---------------------------------------------------------
# 2. PERCOBAAN MANAGER & APPROVAL (Siti Rahayu - Emp ID: 2)
# ---------------------------------------------------------
res_mgr = requests.post(f'{BASE_URL}/auth/login', json={'username': 'manager', 'password': 'manager123'})
mgr_data = res_mgr.json()
mgr_token = mgr_data['token']
mgr_headers = {'Authorization': f'Bearer {mgr_token}'}
mgr_emp_id = mgr_data['user']['employee_id']

print('\n=== 2. PERCOBAAN MANAGER & APPROVAL (Siti Rahayu) ===')
print(f'Logged in as Manager: {mgr_data["user"]["full_name"]} (emp_id={mgr_emp_id})')

# Cek & Approve Leave
res_mgr_leave = requests.get(f'{BASE_URL}/leave', headers=mgr_headers)
pending_leaves = [l for l in res_mgr_leave.json().get('leaves', []) if l.get('status') == 'pending']
print(f'[Manager Check] Pending Leaves: {len(pending_leaves)}')
for l in pending_leaves:
    res_app = requests.put(f'{BASE_URL}/leave/{l["id"]}', headers=mgr_headers, json={'status': 'approved'})
    print(f'  -> Approve Leave ID {l["id"]}: Status {res_app.status_code}, Resp: {res_app.json()}')

# Cek & Approve Overtime
res_mgr_ot = requests.get(f'{BASE_URL}/overtime', headers=mgr_headers)
pending_ot = [o for o in res_mgr_ot.json().get('overtime', []) if o.get('status') == 'pending']
print(f'[Manager Check] Pending Overtime: {len(pending_ot)}')
for o in pending_ot:
    res_app = requests.put(f'{BASE_URL}/overtime/{o["id"]}', headers=mgr_headers, json={'status': 'approved'})
    print(f'  -> Approve Overtime ID {o["id"]}: Status {res_app.status_code}, Resp: {res_app.json()}')

# Cek & Approve Reimbursement
res_mgr_reimb = requests.get(f'{BASE_URL}/reimbursements', headers=mgr_headers)
pending_reimb = [r for r in res_mgr_reimb.json().get('reimbursements', []) if r.get('status') == 'pending']
print(f'[Manager Check] Pending Reimbursement: {len(pending_reimb)}')
for r in pending_reimb:
    res_app = requests.put(f'{BASE_URL}/reimbursements/{r["id"]}', headers=mgr_headers, json={'status': 'approved'})
    print(f'  -> Approve Reimbursement ID {r["id"]}: Status {res_app.status_code}, Resp: {res_app.json()}')

# Approve Travel oleh Manager
if travel_id:
    res_app_trv = requests.post(f'{BASE_URL}/travel/{travel_id}/approve-manager', headers=mgr_headers, json={
        'manager_id': mgr_emp_id,
        'notes': 'Disetujui Manager'
    })
    print(f'[Manager Check] Approve Travel ID {travel_id}: Status {res_app_trv.status_code}, Resp: {res_app_trv.json()}')


# ---------------------------------------------------------
# 3. PERCOBAAN DIREKTUR & OVERVIEW (Budi Santoso - Emp ID: 3)
# ---------------------------------------------------------
res_dir = requests.post(f'{BASE_URL}/auth/login', json={'username': 'direktur', 'password': 'director123'})
dir_data = res_dir.json()
dir_token = dir_data['token']
dir_headers = {'Authorization': f'Bearer {dir_token}'}
dir_emp_id = dir_data['user']['employee_id']

print('\n=== 3. PERCOBAAN DIREKTUR & OVERVIEW (Budi Santoso) ===')
print(f'Logged in as Direktur: {dir_data["user"]["full_name"]} (emp_id={dir_emp_id})')

# Approve Travel oleh Direktur
if travel_id:
    res_dir_trv = requests.post(f'{BASE_URL}/travel/{travel_id}/approve-director', headers=dir_headers, json={
        'director_id': dir_emp_id,
        'notes': 'Disetujui Direktur'
    })
    print(f'[Direktur Check] Approve Travel ID {travel_id}: Status {res_dir_trv.status_code}, Resp: {res_dir_trv.json()}')

# Dashboard Overview oleh Direktur
res_dir_dash = requests.get(f'{BASE_URL}/dashboard', headers=dir_headers)
dash_json = res_dir_dash.json()
print(f'[Direktur Check] Dashboard Summary Overview:')
print(f'  - Total Employees: {dash_json.get("employees")}')
print(f'  - Attendance Today: {dash_json.get("attendance_today")}')
print(f'  - Pending Approvals: {dash_json.get("pending_approvals")}')

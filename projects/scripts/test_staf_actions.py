import requests, json

BASE_URL = 'http://localhost:8090/api'

res = requests.post(f'{BASE_URL}/auth/login', json={'username': 'staf', 'password': 'staff123'})
staf_data = res.json()

print('1. LOGIN STAF:')
print(f'Status: {res.status_code}')
print(f'User info: {staf_data.get("user")}')

headers = {'Authorization': f'Bearer {staf_data["token"]}'}

# Clock In
res_clockin = requests.post(f'{BASE_URL}/attendance/clock-in', headers=headers, json={'notes': 'Masuk pagi staf'})
print('\n2. CLOCK IN STAF:')
print(f'Status: {res_clockin.status_code}, Body: {res_clockin.json()}')

# Overtime
res_ot = requests.post(f'{BASE_URL}/overtime', headers=headers, json={
    'date': '2026-09-20',
    'hours': 2.5,
    'reason': 'Lembur pengerjaan fitur HRIS'
})
print('\n3. AJUKAN OVERTIME STAF:')
print(f'Status: {res_ot.status_code}, Body: {res_ot.json()}')

# Leave
res_leave = requests.post(f'{BASE_URL}/leave', headers=headers, json={
    'leave_type_id': 1,
    'start_date': '2026-09-25',
    'end_date': '2026-09-26',
    'reason': 'Izin acara keluarga'
})
print('\n4. AJUKAN LEAVE STAF:')
print(f'Status: {res_leave.status_code}, Body: {res_leave.json()}')

# Reimbursement
res_reimb = requests.post(f'{BASE_URL}/reimbursements', headers=headers, json={
    'category': 'Transport',
    'amount': 150000,
    'description': 'Bensin dinas lapangan'
})
print('\n5. AJUKAN REIMBURSEMENT STAF:')
print(f'Status: {res_reimb.status_code}, Body: {res_reimb.json()}')

# Travel
res_travel = requests.post(f'{BASE_URL}/travel', headers=headers, json={
    'destination': 'Bandung',
    'purpose': 'Kunjungan Cabang',
    'start_date': '2026-10-01',
    'end_date': '2026-10-03',
    'estimated_cost': 1200000
})
print('\n6. AJUKAN TRAVEL STAF:')
print(f'Status: {res_travel.status_code}, Body: {res_travel.json()}')

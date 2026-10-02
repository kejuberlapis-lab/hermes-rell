import requests

BASE_URL = 'http://localhost:8090/api'

roles = [
    ('staf', 'staff123', 'staff', 'Ahmad Fauzi'),
    ('manager', 'manager123', 'manager', 'Siti Rahayu'),
    ('direktur', 'director123', 'director', 'Budi Santoso'),
    ('superadmin', 'admin123', 'super_admin', 'Rizky Pratama')
]

print("=== VERIFIKASI AKUN & PROFILE DATA ===")
for username, password, expected_role, expected_name in roles:
    res = requests.post(f'{BASE_URL}/auth/login', json={'username': username, 'password': password})
    data = res.json()
    token = data.get('token')
    user = data.get('user', {})
    
    print(f"\n[Login {username.upper()}]")
    print(f"  - HTTP Status: {res.status_code}")
    print(f"  - Full Name: {user.get('full_name')} (Expected: {expected_name})")
    print(f"  - Role: {user.get('role')} (Expected: {expected_role})")
    print(f"  - Employee ID: {user.get('employee_id')}")
    
    # Test /auth/me
    headers = {'Authorization': f'Bearer {token}'}
    me_res = requests.get(f'{BASE_URL}/auth/me', headers=headers)
    print(f"  - GET /auth/me Status: {me_res.status_code}")

import requests, json

BASE_URL = 'http://localhost:8090/api'

# 1. Staf (Ahmad Fauzi) - Cek KPI miliknya sendiri
res_staf = requests.post(f'{BASE_URL}/auth/login', json={'username': 'staf', 'password': 'staff123'})
staf_headers = {'Authorization': f'Bearer {res_staf.json()["token"]}'}

print("=== 1. UJI KPI STAF (Ahmad Fauzi) ===")
res_kpi_staf = requests.get(f'{BASE_URL}/performance/kpis', headers=staf_headers)
print(f"[Staf] GET /performance/kpis Status: {res_kpi_staf.status_code}")
print(f"[Staf] Jumlah KPI milik staf: {len(res_kpi_staf.json().get('kpis', []))}")

res_assign_staf = requests.get(f'{BASE_URL}/kpi-dashboard/assignments', headers=staf_headers)
print(f"[Staf] GET /kpi-dashboard/assignments Status: {res_assign_staf.status_code}")


# 2. Manager (Siti Rahayu) - Buat KPI / Evaluasi KPI Bawahan
res_mgr = requests.post(f'{BASE_URL}/auth/login', json={'username': 'manager', 'password': 'manager123'})
mgr_headers = {'Authorization': f'Bearer {res_mgr.json()["token"]}'}

print("\n=== 2. UJI KPI MANAGER (Siti Rahayu) ===")
# Manager membuatkan KPI untuk Staf (Ahmad Fauzi - Emp ID 4)
res_create_kpi = requests.post(f'{BASE_URL}/performance/kpis', headers=mgr_headers, json={
    'employee_id': 4,
    'period': '2026-Q3',
    'target': 'Menyelesaikan 10 Tiket HRIS',
    'actual': '8 Tiket',
    'score': 85.0,
    'description': 'Target pencapaian kuartal 3'
})
print(f"[Manager] Create KPI untuk Staf: Status {res_create_kpi.status_code}, Resp: {res_create_kpi.json()}")

kpi_id = res_create_kpi.json().get('id')
if kpi_id:
    # Manager meng-update skor KPI setelah evaluasi
    res_update_kpi = requests.put(f'{BASE_URL}/performance/kpis/{kpi_id}', headers=mgr_headers, json={
        'actual': '10 Tiket',
        'score': 100.0,
        'description': 'Target selesai 100%'
    })
    print(f"[Manager] Update Score KPI Staf: Status {res_update_kpi.status_code}, Resp: {res_update_kpi.json()}")


# 3. Direktur (Budi Santoso) - Melihat Semua KPI Perusahaan
res_dir = requests.post(f'{BASE_URL}/auth/login', json={'username': 'direktur', 'password': 'director123'})
dir_headers = {'Authorization': f'Bearer {res_dir.json()["token"]}'}

print("\n=== 3. UJI KPI DIREKTUR (Budi Santoso) ===")
res_dir_kpis = requests.get(f'{BASE_URL}/performance/kpis', headers=dir_headers)
print(f"[Direktur] GET /performance/kpis Total KPI Perusahaan: {len(res_dir_kpis.json().get('kpis', []))}")

res_dir_kpi_dash = requests.get(f'{BASE_URL}/kpi-dashboard/summary', headers=dir_headers)
print(f"[Direktur] Summary KPI Dashboard: {res_dir_kpi_dash.json()}")

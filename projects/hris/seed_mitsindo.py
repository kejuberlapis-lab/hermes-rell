import sqlite3
import os
import sys

# Ensure app path is in python path
sys.path.insert(0, "/home/ubuntu/hris")
from app.services.auth_service import get_password_hash

DB_PATH = "/home/ubuntu/hris/hris.db"

def setup_mitsindo_structure():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Backup current DB first
    os.system(f"cp {DB_PATH} {DB_PATH}.bak_before_mitsindo")
    print(f"Backup created at {DB_PATH}.bak_before_mitsindo")

    # 1. Clear existing operational/employee data
    print("Clearing old data...")
    tables_to_clear = [
        "attendance", "overtime", "leaves", "payroll", "reimbursement", 
        "travel_requests", "assets", "procurement_requests", "training_enrollments",
        "employee_kpis", "performance_reviews", "users", "employees", "positions", "departments"
    ]
    for table in tables_to_clear:
        try:
            cursor.execute(f"DELETE FROM {table};")
        except Exception as e:
            print(f"Error clearing {table}: {e}")

    # Reset sqlite_sequence for clean IDs
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('departments', 'positions', 'employees', 'users');")

    # 2. Insert Departments
    # IDs:
    # 1: Dewan Komisaris (BOD/BOC)
    # 2: Executive Management (Direksi)
    # 3: General Affairs (GA)
    # 4: Accounting & Finance
    # 5: Government Sales
    # 6: Corporate Sales
    # 7: Development & Technical
    # 8: Warehouse & Logistics
    departments = [
        (1, 'Dewan Komisaris', 'BOC', 'Dewan Pengawas & Komisaris Perusahaan', None),
        (2, 'Direksi & Sekretaris', 'DIR', 'Executive Management & Corporate Secretary', None),
        (3, 'General Affairs', 'GA', 'General Affairs, Fasilitas & Operasional Umum', None),
        (4, 'Accounting & Finance', 'FIN', 'Keuangan, Akuntansi, Kasir & Perpajakan', None),
        (5, 'Government Sales', 'GS', 'Penjualan & Relasi Sektor Pemerintahan', None),
        (6, 'Corporate Sales', 'CS', 'Penjualan & Kemitraan Sektor Korporasi & Swasta', None),
        (7, 'Development & Technical', 'DEV', 'Pengembangan Sistem, Presales, Digital Marketing & Teknis', None),
        (8, 'Warehouse & Logistics', 'WHS', 'Manajemen Pergudangan, Aset & Distribusi', None),
    ]
    cursor.executemany(
        "INSERT INTO departments (id, name, code, description, manager_id) VALUES (?, ?, ?, ?, ?);",
        departments
    )
    print(f"Inserted {len(departments)} departments.")

    # 3. Insert Positions
    positions = [
        # BOC
        (1, 'Komisaris', 'Executive', 1, 'Komisaris Perusahaan', 20000000.0, 50000000.0),
        # DIR
        (2, 'Direktur Utama', 'Director', 2, 'Managing Director / Direktur Utama', 20000000.0, 45000000.0),
        (3, 'Sekretaris Direksi', 'Staff', 2, 'Executive Secretary & Administrasi Direksi', 6000000.0, 10000000.0),
        # GA
        (4, 'Head of General Affairs', 'Manager', 3, 'Kepala Bagian General Affairs', 10000000.0, 18000000.0),
        (5, 'Staf General Affairs', 'Staff', 3, 'Staf Operasional & Perlengkapan GA', 5000000.0, 8000000.0),
        # FIN
        (6, 'Head of Accounting & Finance', 'Manager', 4, 'Kepala Departemen Accounting & Finance', 12000000.0, 22000000.0),
        (7, 'Head of Finance', 'Manager', 4, 'Kepala Divisi Keuangan', 10000000.0, 18000000.0),
        (8, 'Staf Penjualan & Billing', 'Staff', 4, 'Staf Penagihan & Finansial Penjualan', 5500000.0, 9000000.0),
        (9, 'Staf Kasir', 'Staff', 4, 'Kasir & Pengelolaan Kas Harian', 5000000.0, 8500000.0),
        (10, 'Staf Purchasing & Accounting', 'Staff', 4, 'Staf Pengadaan & Akuntansi', 6000000.0, 9500000.0),
        (11, 'Supir & Logistik', 'Staff', 4, 'Supir Operasional & Ekspedisi', 4500000.0, 7000000.0),
        # GS
        (12, 'Government Sales Manager', 'Manager', 5, 'Manajer Penjualan Sektor Pemerintahan', 12000000.0, 22000000.0),
        (13, 'Government Sales Executive', 'Staff', 5, 'Sales Executive Sektor Pemerintah', 6000000.0, 12000000.0),
        (14, 'Sales Support', 'Staff', 5, 'Sales Support & Administrasi Tender', 5500000.0, 9000000.0),
        # CS
        (15, 'Corporate Sales Manager', 'Manager', 6, 'Manajer Penjualan Sektor Korporasi', 12000000.0, 22000000.0),
        (16, 'Corporate Sales Executive', 'Staff', 6, 'Sales Executive Sektor Korporasi', 6000000.0, 12000000.0),
        # DEV
        (17, 'Manager Development', 'Manager', 7, 'Manajer Pengembangan Solusi & TI', 15000000.0, 25000000.0),
        (18, 'Presales Specialist', 'Staff', 7, 'Presales & Solution Architect', 8000000.0, 15000000.0),
        (19, 'Digital Marketing Specialist', 'Staff', 7, 'Digital Marketing, Media & Branding', 6000000.0, 11000000.0),
        (20, 'Teknisi / Technical Engineer', 'Staff', 7, 'Teknisi Lapangan, Implementasi & Hardware/Network', 5500000.0, 10000000.0),
        # WHS
        (21, 'Head of Warehouse', 'Manager', 8, 'Kepala Gudang & Manajemen Inventaris', 10000000.0, 16000000.0),
        (22, 'Staf Gudang', 'Staff', 8, 'Staf Pergudangan & Stock Keeper', 4800000.0, 7500000.0),
    ]
    cursor.executemany(
        "INSERT INTO positions (id, title, level, department_id, description, salary_min, salary_max) VALUES (?, ?, ?, ?, ?, ?, ?);",
        positions
    )
    print(f"Inserted {len(positions)} positions.")

    # 4. Define Employees & Hierarchy
    # ID mapping:
    # 1: Slamet (Komisaris) -> Mgr: None
    # 2: Willung (Komisaris) -> Mgr: None
    # 3: William Hosea Eko Putro (Direktur) -> Mgr: None / 1 (Reports to Komisaris)
    # 4: Annisa (Sekretaris) -> Mgr: 3
    # 5: Andreas (GA Head) -> Mgr: 3
    # 6: Alwan (GA Staf) -> Mgr: 5
    # 7: Wina (Head Accounting & Finance) -> Mgr: 3
    # 8: Mei (Head Finance) -> Mgr: 7
    # 9: Ravena (Staf Penjualan) -> Mgr: 8
    # 10: Kristin (Staf Kasir) -> Mgr: 8
    # 11: Agnes (Staf Purchasing & Accounting - Merangkap) -> Mgr: 8
    # 12: Iwan (Supir) -> Mgr: 7
    # 13: Jeni (Supir) -> Mgr: 7
    # 14: Furqon (Supir) -> Mgr: 7
    # 15: Lina (Government Sales Manager) -> Mgr: 3
    # 16: Arief (Sales GS) -> Mgr: 15
    # 17: Jefferson (Sales GS) -> Mgr: 15
    # 18: Bagus Juono (Sales GS) -> Mgr: 15
    # 19: Arvina (Sales Support) -> Mgr: 15
    # 20: Meytilien (Corporate Sales Manager) -> Mgr: 3
    # 21: Edwin Yahya (Sales CS) -> Mgr: 20
    # 22: Ekky Muhammad (Sales CS) -> Mgr: 20
    # 23: Rendy Mahardika (Sales CS) -> Mgr: 20
    # 24: Andi Saputra (Manager Development) -> Mgr: 3
    # 25: Gilang Ramadhan (Presales) -> Mgr: 24
    # 26: Sedni (Digital Marketing) -> Mgr: 24
    # 27: Rahman (Teknis) -> Mgr: 24
    # 28: Willy (Teknis) -> Mgr: 24
    # 29: Irvan (Teknis) -> Mgr: 24
    # 30: Sugeng (Head Warehouse) -> Mgr: 3
    # 31: Joko (Staf Warehouse) -> Mgr: 30
    # 32: Yusuf (Staf Warehouse) -> Mgr: 30
    # 33: Sureha (Staf Warehouse) -> Mgr: 30

    employees_data = [
        # ID, NIK, Full Name, Email, Phone, DeptID, PosID, MgrID, Role
        (1, 'EMP0001', 'Slamet', 'slamet@mitsindo.co.id', '08121111001', 1, 1, None, 'employee'),
        (2, 'EMP0002', 'Willung', 'willung@mitsindo.co.id', '08121111002', 1, 1, None, 'employee'),
        (3, 'EMP0003', 'William Hosea Eko Putro', 'william@mitsindo.co.id', '08121111003', 2, 2, None, 'employee'),
        (4, 'EMP0004', 'Annisa', 'annisa@mitsindo.co.id', '08121111004', 2, 3, 3, 'employee'),
        (5, 'EMP0005', 'Andreas', 'andreas@mitsindo.co.id', '08121111005', 3, 4, 3, 'employee'),
        (6, 'EMP0006', 'Alwan', 'alwan@mitsindo.co.id', '08121111006', 3, 5, 5, 'employee'),
        (7, 'EMP0007', 'Wina', 'wina@mitsindo.co.id', '08121111007', 4, 6, 3, 'employee'),
        (8, 'EMP0008', 'Mei', 'mei@mitsindo.co.id', '08121111008', 4, 7, 7, 'employee'),
        (9, 'EMP0009', 'Ravena', 'ravena@mitsindo.co.id', '08121111009', 4, 8, 8, 'employee'),
        (10, 'EMP0010', 'Kristin', 'kristin@mitsindo.co.id', '08121111010', 4, 9, 8, 'employee'),
        (11, 'EMP0011', 'Agnes', 'agnes@mitsindo.co.id', '08121111011', 4, 10, 8, 'employee'),
        (12, 'EMP0012', 'Iwan', 'iwan@mitsindo.co.id', '08121111012', 4, 11, 7, 'employee'),
        (13, 'EMP0013', 'Jeni', 'jeni@mitsindo.co.id', '08121111013', 4, 11, 7, 'employee'),
        (14, 'EMP0014', 'Furqon', 'furqon@mitsindo.co.id', '08121111014', 4, 11, 7, 'employee'),
        (15, 'EMP0015', 'Lina', 'lina@mitsindo.co.id', '08121111015', 5, 12, 3, 'employee'),
        (16, 'EMP0016', 'Arief', 'arief@mitsindo.co.id', '08121111016', 5, 13, 15, 'employee'),
        (17, 'EMP0017', 'Jefferson', 'jefferson@mitsindo.co.id', '08121111017', 5, 13, 15, 'employee'),
        (18, 'EMP0018', 'Bagus Juono', 'bagus.juono@mitsindo.co.id', '08121111018', 5, 13, 15, 'employee'),
        (19, 'EMP0019', 'Arvina', 'arvina@mitsindo.co.id', '08121111019', 5, 14, 15, 'employee'),
        (20, 'EMP0020', 'Meytilien', 'meytilien@mitsindo.co.id', '08121111020', 6, 15, 3, 'employee'),
        (21, 'EMP0021', 'Edwin Yahya', 'edwin.yahya@mitsindo.co.id', '08121111021', 6, 16, 20, 'employee'),
        (22, 'EMP0022', 'Ekky Muhammad', 'ekky.muhammad@mitsindo.co.id', '08121111022', 6, 16, 20, 'employee'),
        (23, 'EMP0023', 'Rendy Mahardika', 'rendy.mahardika@mitsindo.co.id', '08121111023', 6, 16, 20, 'employee'),
        (24, 'EMP0024', 'Andi Saputra', 'andi.saputra@mitsindo.co.id', '08121111024', 7, 17, 3, 'employee'),
        (25, 'EMP0025', 'Gilang Ramadhan', 'gilang.ramadhan@mitsindo.co.id', '08121111025', 7, 18, 24, 'employee'),
        (26, 'EMP0026', 'Sedni', 'sedni@mitsindo.co.id', '08121111026', 7, 19, 24, 'employee'),
        (27, 'EMP0027', 'Rahman', 'rahman@mitsindo.co.id', '08121111027', 7, 20, 24, 'employee'),
        (28, 'EMP0028', 'Willy', 'willy@mitsindo.co.id', '08121111028', 7, 20, 24, 'employee'),
        (29, 'EMP0029', 'Irvan', 'irvan@mitsindo.co.id', '08121111029', 7, 20, 24, 'employee'),
        (30, 'EMP0030', 'Sugeng', 'sugeng@mitsindo.co.id', '08121111030', 8, 21, 3, 'employee'),
        (31, 'EMP0031', 'Joko', 'joko@mitsindo.co.id', '08121111031', 8, 22, 30, 'employee'),
        (32, 'EMP0032', 'Yusuf', 'yusuf@mitsindo.co.id', '08121111032', 8, 22, 30, 'employee'),
        (33, 'EMP0033', 'Sureha', 'sureha@mitsindo.co.id', '08121111033', 8, 22, 30, 'employee'),
    ]

    for emp in employees_data:
        cursor.execute(
            """INSERT INTO employees (
                id, employee_id_str, full_name, email, phone, department_id, position_id, manager_id, 
                hire_date, status, role
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, '2026-01-01', 'active', ?);""",
            emp
        )
    print(f"Inserted {len(employees_data)} employees.")

    # Update department manager_id
    dept_managers = {
        1: 1,   # BOC: Slamet
        2: 3,   # DIR: William
        3: 5,   # GA: Andreas
        4: 7,   # FIN: Wina
        5: 15,  # GS: Lina
        6: 20,  # CS: Meytilien
        7: 24,  # DEV: Andi Saputra
        8: 30,  # WHS: Sugeng
    }
    for d_id, m_id in dept_managers.items():
        cursor.execute("UPDATE departments SET manager_id = ? WHERE id = ?;", (m_id, d_id))

    # 5. Insert Users & Passwords (All default: password123)
    default_hash = get_password_hash("password123")

    users_data = [
        # ID, username, email, password_hash, role, employee_id, is_active
        # Super Admins: Slamet, Willung, Andi Saputra, and default 'admin'
        (1, 'slamet', 'slamet@mitsindo.co.id', default_hash, 'super_admin', 1, 1),
        (2, 'willung', 'willung@mitsindo.co.id', default_hash, 'super_admin', 2, 1),
        (3, 'andisaputra', 'andi.saputra@mitsindo.co.id', default_hash, 'super_admin', 24, 1),
        (4, 'admin', 'admin@mitsindo.co.id', default_hash, 'super_admin', 24, 1), # Alias for quick admin access
        
        # Director (Final Approval SPPD/Leave): William Hosea Eko Putro
        (5, 'william', 'william@mitsindo.co.id', default_hash, 'director', 3, 1),
        (6, 'direktur', 'direktur@mitsindo.co.id', default_hash, 'director', 3, 1), # Alias
        
        # Managers:
        (7, 'andreas', 'andreas@mitsindo.co.id', default_hash, 'manager', 5, 1),
        (8, 'wina', 'wina@mitsindo.co.id', default_hash, 'manager', 7, 1),
        (9, 'mei', 'mei@mitsindo.co.id', default_hash, 'manager', 8, 1), # Head Finance -> manager role
        (10, 'lina', 'lina@mitsindo.co.id', default_hash, 'manager', 15, 1),
        (11, 'meytilien', 'meytilien@mitsindo.co.id', default_hash, 'manager', 20, 1),
        (12, 'sugeng', 'sugeng@mitsindo.co.id', default_hash, 'manager', 30, 1),
        
        # Staff:
        (13, 'annisa', 'annisa@mitsindo.co.id', default_hash, 'employee', 4, 1),
        (14, 'alwan', 'alwan@mitsindo.co.id', default_hash, 'employee', 6, 1),
        (15, 'ravena', 'ravena@mitsindo.co.id', default_hash, 'employee', 9, 1),
        (16, 'kristin', 'kristin@mitsindo.co.id', default_hash, 'employee', 10, 1),
        (17, 'agnes', 'agnes@mitsindo.co.id', default_hash, 'employee', 11, 1),
        (18, 'iwan', 'iwan@mitsindo.co.id', default_hash, 'employee', 12, 1),
        (19, 'jeni', 'jeni@mitsindo.co.id', default_hash, 'employee', 13, 1),
        (20, 'furqon', 'furqon@mitsindo.co.id', default_hash, 'employee', 14, 1),
        (21, 'arief', 'arief@mitsindo.co.id', default_hash, 'employee', 16, 1),
        (22, 'jefferson', 'jefferson@mitsindo.co.id', default_hash, 'employee', 17, 1),
        (23, 'bagus', 'bagus.juono@mitsindo.co.id', default_hash, 'employee', 18, 1),
        (24, 'arvina', 'arvina@mitsindo.co.id', default_hash, 'employee', 19, 1),
        (25, 'edwin', 'edwin.yahya@mitsindo.co.id', default_hash, 'employee', 21, 1),
        (26, 'ekky', 'ekky.muhammad@mitsindo.co.id', default_hash, 'employee', 22, 1),
        (27, 'rendy', 'rendy.mahardika@mitsindo.co.id', default_hash, 'employee', 23, 1),
        (28, 'gilang', 'gilang.ramadhan@mitsindo.co.id', default_hash, 'employee', 25, 1),
        (29, 'sedni', 'sedni@mitsindo.co.id', default_hash, 'employee', 26, 1),
        (30, 'rahman', 'rahman@mitsindo.co.id', default_hash, 'employee', 27, 1),
        (31, 'willy', 'willy@mitsindo.co.id', default_hash, 'employee', 28, 1),
        (32, 'irvan', 'irvan@mitsindo.co.id', default_hash, 'employee', 29, 1),
        (33, 'joko', 'joko@mitsindo.co.id', default_hash, 'employee', 31, 1),
        (34, 'yusuf', 'yusuf@mitsindo.co.id', default_hash, 'employee', 32, 1),
        (35, 'sureha', 'sureha@mitsindo.co.id', default_hash, 'employee', 33, 1),
    ]

    cursor.executemany(
        """INSERT INTO users (id, username, email, password_hash, role, employee_id, is_active)
           VALUES (?, ?, ?, ?, ?, ?, ?);""",
        users_data
    )
    print(f"Inserted {len(users_data)} users.")

    conn.commit()
    conn.close()
    print("PT Mitsindo structure successfully initialized in DB!")

if __name__ == "__main__":
    setup_mitsindo_structure()

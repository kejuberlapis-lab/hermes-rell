"""
HRIS Database - SQLite with aiosqlite
Creates all tables and seeds demo data.
"""
import aiosqlite
import os
import random
from datetime import datetime, date, timedelta

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hris.db")

# ---------------------------------------------------------------------------
# Table creation SQL
# ---------------------------------------------------------------------------

CREATE_TABLES_SQL = """
-- Departments (manager_id is INTEGER without FK to avoid circular dep)
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    manager_id INTEGER,
    parent_dept_id INTEGER,
    description TEXT,
    FOREIGN KEY (parent_dept_id) REFERENCES departments(id)
);

-- Positions
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    level TEXT NOT NULL,
    department_id INTEGER,
    description TEXT,
    salary_min REAL,
    salary_max REAL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Employees
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id_str TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    department_id INTEGER,
    position_id INTEGER,
    manager_id INTEGER,
    hire_date DATE NOT NULL,
    contract_end_date DATE,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'on_leave')),
    avatar_url TEXT,
    address TEXT,
    date_of_birth DATE,
    gender TEXT,
    marital_status TEXT,
    religion TEXT,
    bank_account TEXT,
    bank_name TEXT,
    npwp TEXT,
    bpjs_ketenagakerjaan TEXT,
    bpjs_kesehatan TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (position_id) REFERENCES positions(id),
    FOREIGN KEY (manager_id) REFERENCES employees(id)
);

-- Users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'employee' CHECK(role IN ('super_admin', 'director', 'manager', 'employee')),
    employee_id INTEGER,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_verified INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Registration requests for approval
CREATE TABLE IF NOT EXISTS registration_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    department TEXT,
    position TEXT,
    password_hash TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
    rejected_by INTEGER,
    rejection_reason TEXT,
    approved_by INTEGER,
    approved_at TIMESTAMP,
    rejected_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Documents
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    doc_type TEXT NOT NULL CHECK(doc_type IN ('ktp', 'kontrak', 'sertifikat', 'other')),
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATE,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Attendance
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    date DATE NOT NULL,
    clock_in TEXT,
    clock_out TEXT,
    status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late', 'half_day')),
    location_lat REAL,
    location_lng REAL,
    notes TEXT,
    photo_in TEXT,
    photo_out TEXT,
    address TEXT,
    distance_meters REAL,
    attendance_type TEXT DEFAULT 'wfo',
    location_lat_out REAL,
    location_lng_out REAL,
    address_out TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Shifts
CREATE TABLE IF NOT EXISTS shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    description TEXT
);

-- Employee Shifts
CREATE TABLE IF NOT EXISTS employee_shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    shift_id INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (shift_id) REFERENCES shifts(id)
);

-- Overtime
CREATE TABLE IF NOT EXISTS overtime (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    date DATE NOT NULL,
    hours REAL NOT NULL,
    reason TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
    approved_by INTEGER,
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (approved_by) REFERENCES employees(id)
);

-- Leave Types
CREATE TABLE IF NOT EXISTS leave_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    days_allowed INTEGER NOT NULL DEFAULT 0,
    description TEXT
);

-- Leaves
CREATE TABLE IF NOT EXISTS leaves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    leave_type_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
    approved_by INTEGER,
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (leave_type_id) REFERENCES leave_types(id),
    FOREIGN KEY (approved_by) REFERENCES employees(id)
);

-- Payroll
CREATE TABLE IF NOT EXISTS payroll (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_month INTEGER NOT NULL,
    period_year INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    base_salary REAL NOT NULL DEFAULT 0,
    allowance REAL NOT NULL DEFAULT 0,
    overtime_pay REAL NOT NULL DEFAULT 0,
    bonus REAL NOT NULL DEFAULT 0,
    deduction REAL NOT NULL DEFAULT 0,
    tax_pph21 REAL NOT NULL DEFAULT 0,
    bpjs_ketenagakerjaan REAL NOT NULL DEFAULT 0,
    bpjs_kesehatan REAL NOT NULL DEFAULT 0,
    net_salary REAL NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'draft' CHECK(status IN ('draft', 'processed', 'paid')),
    processed_at TIMESTAMP,
    paid_at TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Reimbursement
CREATE TABLE IF NOT EXISTS reimbursement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    receipt_path TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
    approved_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (approved_by) REFERENCES employees(id)
);

-- KPIs
CREATE TABLE IF NOT EXISTS kpis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    period TEXT NOT NULL,
    target TEXT,
    actual TEXT,
    score REAL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- OKRs
CREATE TABLE IF NOT EXISTS okrs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    objective TEXT NOT NULL,
    key_result TEXT NOT NULL,
    progress REAL DEFAULT 0,
    period TEXT,
    status TEXT DEFAULT 'in_progress',
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Performance Reviews
CREATE TABLE IF NOT EXISTS performance_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    reviewer_id INTEGER NOT NULL,
    period TEXT NOT NULL,
    score REAL,
    comments TEXT,
    review_type TEXT NOT NULL CHECK(review_type IN ('self', 'manager', 'director', '360', 'quarterly', 'annual')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (reviewer_id) REFERENCES employees(id)
);

-- Training
CREATE TABLE IF NOT EXISTS training (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    trainer TEXT,
    capacity INTEGER DEFAULT 30,
    status TEXT DEFAULT 'active'
);

-- Training Enrollments
CREATE TABLE IF NOT EXISTS training_enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    training_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'enrolled' CHECK(status IN ('enrolled', 'completed', 'cancelled')),
    score REAL,
    completed_at TIMESTAMP,
    FOREIGN KEY (training_id) REFERENCES training(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Job Requisitions
CREATE TABLE IF NOT EXISTS job_requisitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    department_id INTEGER,
    position_id INTEGER,
    headcount INTEGER NOT NULL DEFAULT 1,
    salary_range TEXT,
    status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'closed', 'cancelled')),
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (position_id) REFERENCES positions(id),
    FOREIGN KEY (created_by) REFERENCES employees(id)
);

-- Applicants
CREATE TABLE IF NOT EXISTS applicants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requisition_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    resume_path TEXT,
    source TEXT,
    status TEXT NOT NULL DEFAULT 'new' CHECK(status IN ('new', 'screening', 'interview', 'offer', 'hired', 'rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (requisition_id) REFERENCES job_requisitions(id)
);

-- Interviews
CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    applicant_id INTEGER NOT NULL,
    interviewer_id INTEGER NOT NULL,
    scheduled_at TIMESTAMP NOT NULL,
    notes TEXT,
    rating REAL,
    status TEXT NOT NULL DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'completed', 'cancelled')),
    FOREIGN KEY (applicant_id) REFERENCES applicants(id),
    FOREIGN KEY (interviewer_id) REFERENCES employees(id)
);

-- Procurement Requests
CREATE TABLE IF NOT EXISTS procurement_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requester_id INTEGER NOT NULL,
    department_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    estimated_cost REAL NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'purchased', 'rejected')),
    approved_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (requester_id) REFERENCES employees(id),
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (approved_by) REFERENCES employees(id)
);

-- Assets
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    serial_number TEXT,
    purchase_date DATE,
    purchase_price REAL,
    condition TEXT NOT NULL DEFAULT 'good' CHECK(condition IN ('good', 'fair', 'poor')),
    assigned_to INTEGER,
    department_id INTEGER,
    status TEXT NOT NULL DEFAULT 'available' CHECK(status IN ('available', 'assigned', 'maintenance', 'retired')),
    location TEXT,
    FOREIGN KEY (assigned_to) REFERENCES employees(id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read INTEGER NOT NULL DEFAULT 0,
    link TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Travel Requests (Perjalanan Dinas)
CREATE TABLE IF NOT EXISTS travel_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    destination TEXT NOT NULL,
    purpose TEXT,
    departure_date DATE NOT NULL,
    return_date DATE,
    transport_type TEXT NOT NULL CHECK(transport_type IN ('car', 'bus', 'train', 'plane', 'ship', 'other')),
    accommodation_needed INTEGER NOT NULL DEFAULT 0,
    
    -- Cost breakdown fields
    estimated_cost REAL DEFAULT 0,
    transport_cost REAL DEFAULT 0,
    accommodation_rate_per_night REAL DEFAULT 0,
    accommodation_nights INTEGER DEFAULT 0,
    accommodation_total REAL DEFAULT 0,
    daily_allowance_per_day REAL DEFAULT 0,
    daily_allowance_days INTEGER DEFAULT 0,
    daily_allowance_total REAL DEFAULT 0,
    meals_per_day REAL DEFAULT 0,
    meal_days INTEGER DEFAULT 0,
    meal_total REAL DEFAULT 0,
    additional_items TEXT,
    grand_total REAL DEFAULT 0,
    
    actual_cost REAL DEFAULT 0,
    advance_payment REAL DEFAULT 0,
    
    status TEXT NOT NULL DEFAULT 'draft' CHECK(status IN (
        'draft', 'pending_manager', 'pending_director', 
        'approved', 'rejected', 'completed'
    )),
    finance_status TEXT NOT NULL DEFAULT 'not_submitted' CHECK(finance_status IN (
        'not_submitted', 'submitted', 'processing', 'completed'
    )),
    manager_id INTEGER,
    manager_approved_at TIMESTAMP,
    manager_notes TEXT,
    director_id INTEGER,
    director_approved_at TIMESTAMP,
    director_notes TEXT,
    finance_processed_by INTEGER,
    finance_processed_at TIMESTAMP,
    finance_amount REAL,
    finance_notes TEXT,
    receipt_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (manager_id) REFERENCES employees(id),
    FOREIGN KEY (director_id) REFERENCES employees(id),
    FOREIGN KEY (finance_processed_by) REFERENCES employees(id)
);

-- KPI Templates
CREATE TABLE IF NOT EXISTS kpi_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT NOT NULL,
    position TEXT NOT NULL,
    template_name TEXT NOT NULL,
    kpi_name TEXT NOT NULL,
    description TEXT,
    formula TEXT,
    target_standard TEXT,
    weight_percentage REAL NOT NULL DEFAULT 100.0,
    scoring_scale TEXT DEFAULT '1-5',
    category TEXT DEFAULT 'performance',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- KPI Formulas
CREATE TABLE IF NOT EXISTS kpi_formulas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    formula TEXT NOT NULL,
    variable_help TEXT
);

-- Employee KPIs
CREATE TABLE IF NOT EXISTS employee_kpis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    template_id INTEGER NOT NULL,
    period TEXT NOT NULL,
    target_value TEXT,
    actual_value TEXT,
    score REAL,
    achievement_percentage REAL,
    comments TEXT,
    reviewed_by INTEGER,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (template_id) REFERENCES kpi_templates(id)
);
"""

# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

SEED_DEPARTMENTS = """
INSERT OR IGNORE INTO departments (id, name, code, description) VALUES
    (1, 'Human Resources', 'HR', 'People operations and talent management'),
    (2, 'Engineering', 'ENG', 'Software development and infrastructure'),
    (3, 'Marketing', 'MKT', 'Brand, digital marketing, and communications'),
    (4, 'Finance', 'FIN', 'Accounting, budgeting, and financial planning'),
    (5, 'Operations', 'OPS', 'Business operations and logistics');
"""

SEED_POSITIONS = """
INSERT OR IGNORE INTO positions (id, title, level, department_id, description, salary_min, salary_max) VALUES
    (1,  'Director of HR',        'Director', 1, 'Head of human resources department',         15000000, 25000000),
    (2,  'HR Manager',           'Manager',  1, 'Manages HR day-to-day operations',           10000000, 18000000),
    (3,  'HR Specialist',        'Staff',    1, 'Handles recruitment and employee relations',  6000000, 10000000),
    (4,  'Software Engineer',    'Staff',    2, 'Develops and maintains software',             8000000, 18000000),
    (5,  'Senior Software Eng',  'Senior',   2, 'Leads technical projects and mentors juniors',12000000, 25000000),
    (6,  'Marketing Manager',    'Manager',  3, 'Oversees marketing strategy',                 10000000, 18000000),
    (7,  'Marketing Specialist', 'Staff',    3, 'Executes marketing campaigns',                5000000,  9000000),
    (8,  'Finance Manager',      'Manager',  4, 'Manages financial operations',                10000000, 18000000),
    (9,  'Accountant',           'Staff',    4, 'Handles bookkeeping and reporting',           6000000, 11000000),
    (10, 'Operations Manager',   'Manager',  5, 'Manages daily operations',                    10000000, 18000000);
"""

SEED_EMPLOYEES = """
INSERT OR IGNORE INTO employees (id, employee_id_str, full_name, email, phone, department_id, position_id, manager_id, hire_date, status, address, date_of_birth, gender, marital_status, religion, bank_account, bank_name, npwp, bpjs_ketenagakerjaan, bpjs_kesehatan) VALUES
    (1,  'EMP-001', 'Andi Pratama',    'andi.pratama@company.com',   '081234560001', 1, 1, NULL, '2020-01-15', 'active', 'Jl. Sudirman No. 10, Jakarta',  '1985-03-10', 'Male',   'Married', 'Islam',   '1234567890', 'Bank Mandiri', '123.456.789-001', 'BPJS-TK-001', 'BPJS-KS-001'),
    (2,  'EMP-002', 'Siti Rahayu',     'siti.rahayu@company.com',    '081234560002', 1, 2, 1,     '2020-06-01', 'active', 'Jl. Gatot Subroto No. 20, Jakarta', '1988-07-22', 'Female', 'Married', 'Islam',   '2345678901', 'Bank BCA',    '123.456.789-002', 'BPJS-TK-002', 'BPJS-KS-002'),
    (3,  'EMP-003', 'Rudi Hartono',    'rudi.hartono@company.com',   '081234560003', 2, 5, NULL, '2020-03-01', 'active', 'Jl. Rasuna Said No. 30, Jakarta',  '1986-11-05', 'Male',   'Single',  'Kristen', '3456789012', 'Bank Mandiri', '123.456.789-003', 'BPJS-TK-003', 'BPJS-KS-003'),
    (4,  'EMP-004', 'Dewi Lestari',    'dewi.lestari@company.com',   '081234560004', 2, 4, 3,     '2021-01-10', 'active', 'Jl. Kuningan No. 40, Jakarta',     '1992-02-14', 'Female', 'Single',  'Hindu',   '4567890123', 'Bank BRI',    '123.456.789-004', 'BPJS-TK-004', 'BPJS-KS-004'),
    (5,  'EMP-005', 'Budi Santoso',    'budi.santoso@company.com',   '081234560005', 2, 4, 3,     '2021-06-15', 'active', 'Jl. Setiabudi No. 50, Jakarta',    '1993-09-30', 'Male',   'Married', 'Islam',   '5678901234', 'Bank Mandiri', '123.456.789-005', 'BPJS-TK-005', 'BPJS-KS-005'),
    (6,  'EMP-006', 'Maya Putri',      'maya.putri@company.com',     '081234560006', 3, 6, NULL, '2020-04-01', 'active', 'Jl. Permata No. 60, Jakarta',      '1987-12-18', 'Female', 'Married', 'Islam',   '6789012345', 'Bank BCA',    '123.456.789-006', 'BPJS-TK-006', 'BPJS-KS-006'),
    (7,  'EMP-007', 'Fajar Nugroho',   'fajar.nugroho@company.com',  '081234560007', 3, 7, 6,     '2022-03-01', 'active', 'Jl. Tebet No. 70, Jakarta',        '1995-05-25', 'Male',   'Single',  'Islam',   '7890123456', 'Bank Mandiri', '123.456.789-007', 'BPJS-TK-007', 'BPJS-KS-007'),
    (8,  'EMP-008', 'Lina Wijaya',     'lina.wijaya@company.com',    '081234560008', 4, 8, NULL, '2020-02-01', 'active', 'Jl. SCBD No. 80, Jakarta',         '1984-08-12', 'Female', 'Married', 'Buddha',  '8901234567', 'Bank BRI',    '123.456.789-008', 'BPJS-TK-008', 'BPJS-KS-008'),
    (9,  'EMP-009', 'Hendra Kusuma',   'hendra.kusuma@company.com',  '081234560009', 4, 9, 8,     '2022-07-01', 'active', 'Jl. Senopati No. 90, Jakarta',     '1994-01-07', 'Male',   'Single',  'Islam',   '9012345678', 'Bank Mandiri', '123.456.789-009', 'BPJS-TK-009', 'BPJS-KS-009'),
    (10, 'EMP-010', 'Rina Sari',       'rina.sari@company.com',      '081234560010', 5, 10, NULL, '2020-05-01', 'active', 'Jl. Kemang No. 100, Jakarta',      '1989-06-15', 'Female', 'Married', 'Islam',   '0123456789', 'Bank BCA',    '123.456.789-010', 'BPJS-TK-010', 'BPJS-KS-010');
"""

SEED_SHIFTS = """
INSERT OR IGNORE INTO shifts (id, name, start_time, end_time, description) VALUES
    (1, 'Morning Shift',   '07:00', '15:00', 'Standard morning working hours'),
    (2, 'Afternoon Shift', '14:00', '22:00', 'Afternoon to evening working hours'),
    (3, 'Night Shift',     '22:00', '06:00', 'Overnight working hours'),
    (4, 'Full Day',        '08:00', '17:00', 'Standard full-day office hours');
"""

SEED_LEAVE_TYPES = """
INSERT OR IGNORE INTO leave_types (id, name, code, days_allowed, description) VALUES
    (1, 'Annual Leave',       'AL',  12, 'Paid annual leave for vacation'),
    (2, 'Sick Leave',         'SL',  12, 'Medical leave when ill'),
    (3, 'Maternity Leave',    'ML',  90, 'Leave for childbirth'),
    (4, 'Paternity Leave',    'PL',  5,  'Leave for new fathers'),
    (5, 'Unpaid Leave',       'UL',  30, 'Leave without pay'),
    (6, 'Marriage Leave',     'MRL', 3,  'Leave for getting married'),
    (7, 'Bereavement Leave',  'BL',  3,  'Leave for family bereavement'),
    (8, 'Religious Holiday',  'RH',  2,  'Leave for religious observances');
"""


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

async def get_db():
    """FastAPI dependency that yields an async database connection."""
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    try:
        yield db
    finally:
        await db.close()


async def get_db_connection() -> aiosqlite.Connection:
    """Get a raw async connection (not a dependency). Caller must close."""
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    return db


async def init_db():
    """Create all tables and seed demo data."""
    db = await get_db_connection()
    try:
        await db.executescript(CREATE_TABLES_SQL)
        
        # Auto-migration for attendance columns if missing
        cols_to_ensure = [
            ("photo_in", "TEXT"),
            ("photo_out", "TEXT"),
            ("address", "TEXT"),
            ("distance_meters", "REAL"),
            ("attendance_type", "TEXT DEFAULT 'wfo'"),
            ("location_lat_out", "REAL"),
            ("location_lng_out", "REAL"),
            ("address_out", "TEXT")
        ]
        for cname, ctype in cols_to_ensure:
            try:
                await db.execute(f"ALTER TABLE attendance ADD COLUMN {cname} {ctype}")
            except Exception:
                pass
                
        await _seed_demo_data(db)
        await db.commit()
    finally:
        await db.close()


async def _seed_demo_data(db: aiosqlite.Connection):
    """Insert demo seed data if tables are empty."""
    cursor = await db.execute("SELECT COUNT(*) FROM employees")
    count = (await cursor.fetchone())[0]
    if count > 0:
        return

    # Disable FK during seeding to avoid FK ordering issues
    await db.execute("PRAGMA foreign_keys = OFF;")
    
    await db.executescript(
        SEED_DEPARTMENTS
        + SEED_POSITIONS
        + SEED_EMPLOYEES
        + SEED_SHIFTS
        + SEED_LEAVE_TYPES
    )

    # Insert users with properly hashed passwords (password123 for all demo users)
    from app.services.auth_service import get_password_hash
    demo_hash = get_password_hash("password123")
    demo_users = [
        (1, 'admin', 'admin@company.com', demo_hash, 'super_admin', 1, 1),
        (2, 'superadmin', 'superadmin@company.com', demo_hash, 'super_admin', 1, 1),
        (3, 'direktur', 'direktur@company.com', demo_hash, 'director', 2, 1),
        (4, 'manager', 'manager@company.com', demo_hash, 'manager', 3, 1),
        (5, 'staf', 'staf@company.com', demo_hash, 'employee', 4, 1),
        (6, 'employee', 'employee@company.com', demo_hash, 'employee', 4, 1),
    ]
    for u in demo_users:
        await db.execute(
            """INSERT OR REPLACE INTO users (id, username, email, password_hash, role, employee_id, is_active)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            u,
        )

    # Set department managers
    await db.execute("UPDATE departments SET manager_id = 1 WHERE code = 'HR'")
    await db.execute("UPDATE departments SET manager_id = 3 WHERE code = 'ENG'")
    await db.execute("UPDATE departments SET manager_id = 6 WHERE code = 'MKT'")
    await db.execute("UPDATE departments SET manager_id = 8 WHERE code = 'FIN'")
    await db.execute("UPDATE departments SET manager_id = 10 WHERE code = 'OPS'")

    today = date.today()

    # Employee shift assignments
    for emp_id in range(1, 11):
        await db.execute(
            "INSERT INTO employee_shifts (employee_id, shift_id, date) VALUES (?, 4, ?)",
            (emp_id, today.isoformat()),
        )

    # Attendance records (last 5 working days for employees 1-5)
    statuses = ['present', 'present', 'present', 'late', 'half_day']
    for emp_id in range(1, 6):
        for i in range(1, 6):
            d = today - timedelta(days=i)
            if d.weekday() >= 5:
                continue
            clock_in = f"0{random.randint(7, 8)}:{random.randint(0, 30):02d}"
            clock_out = f"{random.randint(16, 18)}:{random.randint(0, 59):02d}"
            status = random.choice(statuses)
            await db.execute(
                """INSERT INTO attendance
                   (employee_id, date, clock_in, clock_out, status, notes)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (emp_id, d.isoformat(), clock_in, clock_out, status, 'Demo attendance record'),
            )

    # Overtime records
    for emp_id in range(3, 6):
        await db.execute(
            """INSERT INTO overtime (employee_id, date, hours, reason, status, approved_by)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (emp_id, (today - timedelta(days=2)).isoformat(), round(random.uniform(1, 4), 1),
             'Project deadline overtime', 'approved', 2),
        )

    # Leave records
    await db.execute(
        """INSERT INTO leaves (employee_id, leave_type_id, start_date, end_date, reason, status, approved_by)
           VALUES (4, 1, ?, ?, 'Family vacation', 'approved', 2)""",
        ((today + timedelta(days=14)).isoformat(), (today + timedelta(days=18)).isoformat()),
    )
    await db.execute(
        """INSERT INTO leaves (employee_id, leave_type_id, start_date, end_date, reason, status, approved_by)
           VALUES (7, 2, ?, ?, 'Medical checkup', 'approved', 2)""",
        ((today - timedelta(days=3)).isoformat(), (today - timedelta(days=3)).isoformat()),
    )

    # Payroll records
    for emp_id in range(1, 11):
        base = random.uniform(5000000, 15000000)
        allowance = base * 0.15
        overtime_pay = random.uniform(0, 500000)
        bonus = random.uniform(0, 200000)
        deduction = random.uniform(0, 300000)
        tax = base * 0.05
        bpjs_tk = base * 0.04
        bpjs_ks = base * 0.01
        net = base + allowance + overtime_pay + bonus - deduction - tax - bpjs_tk - bpjs_ks
        await db.execute(
            """INSERT INTO payroll
               (period_month, period_year, employee_id, base_salary, allowance,
                overtime_pay, bonus, deduction, tax_pph21, bpjs_ketenagakerjaan,
                bpjs_kesehatan, net_salary, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (today.month, today.year, emp_id, round(base), round(allowance),
             round(overtime_pay), round(bonus), round(deduction), round(tax),
             round(bpjs_tk), round(bpjs_ks), round(net), 'paid'),
        )

    # Reimbursement
    await db.execute(
        """INSERT INTO reimbursement (employee_id, category, amount, description, status, approved_by)
           VALUES (3, 'Transportation', 250000, 'Travel to client meeting', 'approved', 2)"""
    )
    await db.execute(
        """INSERT INTO reimbursement (employee_id, category, amount, description, status, approved_by)
           VALUES (5, 'Meal', 150000, 'Team lunch', 'pending', NULL)"""
    )

    # KPIs
    for emp_id in range(1, 6):
        await db.execute(
            """INSERT INTO kpis (employee_id, period, target, actual, score, description)
               VALUES (?, '2025-Q1', 'Meet quarterly targets', 'Exceeded by 10%', 4.5,
                       'Strong performance in Q1 2025')""",
            (emp_id,),
        )

    # OKRs
    await db.execute(
        """INSERT INTO okrs (employee_id, objective, key_result, progress, period, status)
           VALUES (3, 'Launch new API gateway', 'Complete 80% of endpoints', 75, '2025-Q1', 'in_progress')"""
    )
    await db.execute(
        """INSERT INTO okrs (employee_id, objective, key_result, progress, period, status)
           VALUES (6, 'Increase brand awareness', 'Grow social following by 20%', 60, '2025-Q1', 'in_progress')"""
    )

    # Performance reviews
    await db.execute(
        """INSERT INTO performance_reviews (employee_id, reviewer_id, period, score, comments, review_type)
           VALUES (3, 1, '2025-Q1', 4.2, 'Excellent technical skills and team collaboration.', 'manager')"""
    )
    await db.execute(
        """INSERT INTO performance_reviews (employee_id, reviewer_id, period, score, comments, review_type)
           VALUES (3, 3, '2025-Q1', 3.8, 'Self-assessment: room for growth in mentoring.', 'self')"""
    )

    # Training
    await db.execute(
        """INSERT INTO training (id, title, description, start_date, end_date, trainer, capacity, status)
           VALUES (1, 'Python Advanced Workshop', 'Deep dive into async Python and design patterns',
                   ?, ?, 'Dr. Andi', 20, 'active')""",
        ((today + timedelta(days=7)).isoformat(), (today + timedelta(days=9)).isoformat()),
    )
    await db.execute(
        """INSERT INTO training (id, title, description, start_date, end_date, trainer, capacity, status)
           VALUES (2, 'Leadership Development', 'Building effective leaders for the future',
                   ?, ?, 'Ms. Sarah', 15, 'active')""",
        ((today + timedelta(days=14)).isoformat(), (today + timedelta(days=16)).isoformat()),
    )

    # Training enrollments
    await db.execute(
        "INSERT INTO training_enrollments (training_id, employee_id, status) VALUES (1, 3, 'enrolled')"
    )
    await db.execute(
        "INSERT INTO training_enrollments (training_id, employee_id, status) VALUES (1, 4, 'enrolled')"
    )
    await db.execute(
        "INSERT INTO training_enrollments (training_id, employee_id, status) VALUES (2, 1, 'enrolled')"
    )

    # Job requisitions
    await db.execute(
        """INSERT INTO job_requisitions (title, department_id, position_id, headcount, salary_range, status, created_by)
           VALUES ('Backend Developer', 2, 4, 2, '8-12 juta', 'open', 1)"""
    )
    await db.execute(
        """INSERT INTO job_requisitions (title, department_id, position_id, headcount, salary_range, status, created_by)
           VALUES ('Marketing Coordinator', 3, 7, 1, '5-8 juta', 'open', 1)"""
    )

    # Applicants
    await db.execute(
        """INSERT INTO applicants (requisition_id, full_name, email, phone, source, status)
           VALUES (1, 'Tono Sugiarto', 'tono@example.com', '081999000001', 'LinkedIn', 'screening')"""
    )
    await db.execute(
        """INSERT INTO applicants (requisition_id, full_name, email, phone, source, status)
           VALUES (1, 'Wati Susanti', 'wati@example.com', '081999000002', 'JobStreet', 'new')"""
    )
    await db.execute(
        """INSERT INTO applicants (requisition_id, full_name, email, phone, source, status)
           VALUES (2, 'Bambang Irawan', 'bambang@example.com', '081999000003', 'Website', 'interview')"""
    )

    # Interviews
    await db.execute(
        """INSERT INTO interviews (applicant_id, interviewer_id, scheduled_at, notes, rating, status)
           VALUES (3, 6, ?, 'First round technical interview', NULL, 'scheduled')""",
        ((today + timedelta(days=3)).isoformat() + 'T10:00:00',),
    )

    # Procurement requests
    await db.execute(
        """INSERT INTO procurement_requests (requester_id, department_id, title, description, estimated_cost, status, approved_by)
           VALUES (3, 2, 'New laptop', 'Development laptop for new hire', 15000000, 'approved', 1)"""
    )
    await db.execute(
        """INSERT INTO procurement_requests (requester_id, department_id, title, description, estimated_cost, status, approved_by)
           VALUES (6, 3, 'Marketing materials', 'Brochures and banners for event', 5000000, 'pending', NULL)"""
    )

    # Assets
    await db.execute(
        """INSERT INTO assets (name, category, serial_number, purchase_date, purchase_price, condition, assigned_to, department_id, status, location)
           VALUES ('MacBook Pro 16"', 'Laptop', 'MBP-2024-001', '2024-01-15', 28000000, 'good', 3, 2, 'assigned', 'Engineering Floor')"""
    )
    await db.execute(
        """INSERT INTO assets (name, category, serial_number, purchase_date, purchase_price, condition, assigned_to, department_id, status, location)
           VALUES ('Dell Monitor 27"', 'Monitor', 'MON-2024-001', '2024-02-01', 5000000, 'good', 4, 2, 'assigned', 'Engineering Floor')"""
    )
    await db.execute(
        """INSERT INTO assets (name, category, serial_number, purchase_date, purchase_price, condition, assigned_to, department_id, status, location)
           VALUES ('HP LaserJet Printer', 'Printer', 'PRN-2023-001', '2023-06-01', 3500000, 'fair', NULL, 5, 'available', 'Operations Room')"""
    )

    # Notifications
    await db.execute(
        """INSERT INTO notifications (user_id, title, message, is_read, link)
           VALUES (1, 'New Procurement Request', 'A new procurement request needs your approval.', 0, '/procurement')"""
    )
    await db.execute(
        """INSERT INTO notifications (user_id, title, message, is_read, link)
           VALUES (1, 'Leave Request Pending', 'Leave request from Dewi Lestari is pending approval.', 0, '/leaves')"""
    )
    await db.execute(
        """INSERT INTO notifications (user_id, title, message, is_read, link)
           VALUES (2, 'Overtime Approved', 'Your overtime request has been approved.', 1, '/overtime')"""
    )


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import asyncio

    async def _main():
        await init_db()
        print(f"Database initialized at {DATABASE_PATH}")

        db = await get_db_connection()
        try:
            tables = [
                "users", "employees", "departments", "positions", "documents",
                "attendance", "shifts", "employee_shifts", "overtime",
                "leave_types", "leaves", "payroll", "reimbursement",
                "kpis", "okrs", "performance_reviews", "training",
                "training_enrollments", "job_requisitions", "applicants",
                "interviews", "procurement_requests", "assets", "notifications",
            ]
            for table in tables:
                cursor = await db.execute(f"SELECT COUNT(*) FROM {table}")
                count = (await cursor.fetchone())[0]
                print(f"  {table:25s}: {count} rows")
        finally:
            await db.close()

    asyncio.run(_main())

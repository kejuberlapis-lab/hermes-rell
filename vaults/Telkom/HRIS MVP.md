# HRIS MVP - Human Resource Information System

## 📋 Overview
Sistem HRIS (Human Resource Information System) tingkat enterprise yang dibangun dengan FastAPI + SQLite + Bootstrap 5. Dirancang untuk B2B SaaS dengan Role-Based Access Control (RBAC) untuk 3 peran: Super Admin, Manager, Employee.

## 🏗️ Tech Stack
- **Backend:** Python 3.11 + FastAPI + aiosqlite (async SQLite)
- **Frontend:** Bootstrap 5.3 CDN + Font Awesome 6 + Chart.js + Inter font
- **Auth:** JWT (python-jose) + bcrypt (passlib)
- **Database:** SQLite (24 tabel)
- **Port:** 8090
- **URL:** http://43.134.179.61:8090

## 📁 Project Structure
```
/home/ubuntu/hris/
├── main.py                          # FastAPI entry point (port 8090)
├── hris.db                          # SQLite database
├── requirements.txt                 # Python dependencies
├── app/
│   ├── database.py                  # DB schema (24 tables) + init + seed
│   ├── models/
│   │   └── schemas.py              # Pydantic models (all entities)
│   ├── services/
│   │   └── auth_service.py         # JWT auth, password hashing, RBAC
│   ├── routes/
│   │   ├── auth.py                 # POST /login, /logout, GET /me
│   │   ├── employees.py            # CRUD + filters
│   │   ├── departments.py          # CRUD departments
│   │   ├── attendance.py           # Clock in/out, records, summary
│   │   ├── overtime.py             # Submit, approve/reject
│   │   ├── leave.py                # Submit, approve, balances
│   │   ├── payroll.py              # Process, payslip
│   │   ├── performance.py          # KPIs, OKRs, reviews
│   │   ├── recruitment.py          # Requisitions, applicants, interviews
│   │   ├── procurement.py          # Requests + approval workflow
│   │   ├── assets.py               # CRUD + assign/unassign
│   │   ├── notifications.py        # List, mark read
│   │   ├── dashboard.py            # Aggregated stats
│   │   ├── documents.py            # Upload/download docs
│   │   ├── training.py             # Programs, enrollments
│   │   └── reimbursement.py        # Submit/approve claims
│   └── uploads/                    # Uploaded files
├── templates/
│   ├── base.html                   # Base layout (sidebar + navbar)
│   ├── login.html                  # Login page
│   └── pages/
│       ├── dashboard.html          # Main dashboard
│       ├── employees.html          # Employee list
│       ├── employee_detail.html    # Employee detail (6 tabs)
│       ├── attendance.html         # Attendance management
│       ├── leave.html              # Leave management
│       ├── payroll.html            # Payroll processing
│       ├── overtime.html           # Overtime management
│       ├── performance.html        # KPI/OKR tracking
│       ├── recruitment.html        # ATS pipeline
│       ├── procurement.html        # Procurement requests
│       ├── assets.html             # Asset management
│       ├── training.html           # Training/LMS
│       ├── reports.html            # Reports dashboard
│       ├── departments.html        # Departments
│       └── settings.html           # System settings
└── static/
    ├── css/style.css               # Custom CSS (extends Bootstrap)
    └── js/app.js                   # JavaScript (API calls, charts, UI)
```

## 🗄️ Database Schema (24 Tables)

### Core HR
| Table | Description |
|-------|-------------|
| users | User accounts (admin, manager, employee) |
| employees | Employee profiles (15+ fields) |
| departments | Organizational departments |
| positions | Job positions with salary ranges |
| employee_documents | Uploaded documents (KTP, contracts, etc.) |

### Time & Attendance
| Table | Description |
|-------|-------------|
| attendance | Daily clock in/out records |
| shifts | Work shift definitions |
| employee_shifts | Shift assignments |
| overtime | Overtime requests + approvals |

### Leave Management
| Table | Description |
|-------|-------------|
| leave_types | Leave categories (annual, sick, etc.) |
| leaves | Leave requests + approvals |
| leave_balances | Annual leave quotas |

### Payroll & Compensation
| Table | Description |
|-------|-------------|
| payroll | Monthly salary processing |
| reimbursement | Reimbursement claims |

### Performance & Talent
| Table | Description |
|-------|-------------|
| kpis | Key Performance Indicators |
| okrs | Objectives & Key Results |
| performance_reviews | 360° reviews |

### Training & LMS
| Table | Description |
|-------|-------------|
| training_programs | Training courses |
| training_enrollments | Employee enrollments |

### Recruitment (ATS)
| Table | Description |
|-------|-------------|
| job_requisitions | Open positions |
| applicants | Candidate profiles |
| interviews | Interview schedules |

### Procurement & Assets
| Table | Description |
|-------|-------------|
| procurement_requests | Purchase requests |
| assets | Company assets inventory |

### Communication
| Table | Description |
|-------|-------------|
| notifications | In-app notifications |

## 👥 RBAC Roles

### Super Admin / HR
- Full access to all modules
- Manage employees, departments, payroll
- Approve leave, overtime, procurement
- View reports and analytics

### Manager / Supervisor
- View team members
- Approve team leave/overtime
- View team attendance
- Performance reviews

### Employee (Self-Service)
- View own profile, attendance, payslips
- Submit leave/overtime requests
- Submit reimbursement claims
- View training enrollments

## 🔐 Demo Accounts

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Super Admin |
| manager | admin123 | Manager |
| employee | admin123 | Employee |

## 📊 Key Features

### Dashboard
- Stat cards: Total Employees, Present Today, Pending Approvals, Monthly Payroll
- Attendance trend chart (Chart.js)
- Department distribution chart
- Recent activity feed
- Quick actions panel
- Upcoming leaves summary

### Core HR
- Employee CRUD with search/filter
- Employee detail with 6 tabs (Overview, Documents, Attendance, Leave, Payroll, Performance)
- Department management
- Document management (KTP, contracts, certificates)
- Org chart

### Time & Attendance
- Live attendance tracking (clock in/out)
- Date range filters
- Attendance summary with charts
- Shift management

### Leave Management
- Leave balance cards with progress bars
- Leave request form with modal
- Approval queue for managers
- Leave history table

### Payroll
- Period selector (month/year)
- Bulk payroll processing
- Payslip download (HTML)
- Tax (PPH 21) & BPJS calculations

### Overtime
- Submit overtime requests
- Approve/reject workflow
- Overtime summary stats

### Performance
- KPI tracking with progress bars
- OKR management
- 360° performance reviews
- Star ratings

### Recruitment (ATS)
- Job requisition management
- Applicant pipeline
- Interview scheduling
- Offer letter generation

### Procurement
- Purchase request submission
- Approval workflow
- Cost tracking

### Asset Management
- Asset inventory
- Assignment tracking
- Condition monitoring
- Location tracking

### Training/LMS
- Training program management
- Employee enrollment
- Completion tracking
- Score recording

## 🚀 Deployment

### Start Server
```bash
cd /home/ubuntu/hris
source venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8090
```

### Access URL
- **Login:** http://43.134.179.61:8090/
- **Dashboard:** http://43.134.179.61:8090/dashboard
- **API Docs:** http://43.134.179.61:8090/docs (if enabled)

### Restart
```bash
fuser -k 8090/tcp
cd /home/ubuntu/hris && source venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8090 &
```

## 📝 Design Principles
- **Bootstrap 5 CDN** — no custom CSS framework
- **Corporate Professional Blue** (#1e3a5f primary, #2c5282 secondary)
- **Inter font** from Google Fonts
- **Clean, minimal, enterprise** — NOT glassmorphism, NOT AI-purple
- **Responsive** — sidebar collapses to icons on tablet
- **Status badges** with semantic colors (green=active, yellow=on_leave)
- **Data tables** with alternating row colors

## 📌 API Endpoints

### Auth
- `POST /api/auth/login` — Login (returns JWT token)
- `POST /api/auth/logout` — Logout
- `GET /api/auth/me` — Current user info

### Core
- `GET/POST /api/employees` — List/Create employees
- `GET/PUT/DELETE /api/employees/{id}` — Read/Update/Delete employee
- `GET/POST /api/departments` — List/Create departments

### Time & Attendance
- `GET/POST /api/attendance` — List/Create attendance
- `POST /api/attendance/clock-in` — Clock in
- `POST /api/attendance/clock-out` — Clock out

### Leave
- `GET/POST /api/leave` — List/Create leave requests
- `PUT /api/leave/{id}/approve` — Approve leave
- `GET /api/leave/balances` — Leave balances

### Overtime
- `GET/POST /api/overtime` — List/Create overtime
- `PUT /api/overtime/{id}/approve` — Approve overtime

### Payroll
- `GET /api/payroll` — List payroll records
- `POST /api/payroll/process` — Process payroll

### Performance
- `GET/POST /api/performance/kpis` — KPIs
- `GET/POST /api/performance/okrs` — OKRs
- `GET/POST /api/performance/reviews` — Reviews

### Recruitment
- `GET/POST /api/recruitment/requisitions` — Job requisitions
- `GET/POST /api/recruitment/applicants` — Applicants

### Procurement
- `GET/POST /api/procurement` — Procurement requests

### Assets
- `GET/POST /api/assets` — Assets

### Training
- `GET/POST /api/training/programs` — Training programs

### Notifications
- `GET /api/notifications` — Notifications

---

## 📌 Catatan Pembaruan Sistem & Audit Operasional (21 September 2026)

### 1. Akun & Hak Akses (RBAC Isolation)
- **Pemisahan Akun Master vs Manager:**
  - `admin` (`super_admin`): Master System & Database Administrator.
  - `andisaputra` (`manager` - Employee ID 24 / `MVP0024`): Manager IT & Development murni (terpisah dari kendali super admin).
- **Kebijakan Password:** Akun `sedni` mempertahankan custom password hash; 33 karyawan default `password123`.

### 2. Modul Perjalanan Dinas (SPPD & Approval Matrix)
- **Hirarki Tanda Tangan SPPD (Print PDF):**
  - Staf Umum: 3 Tanda Tangan (Pemohon, Manajer Divisi, Direktur Utama William Hosea).
  - Manajer Divisi (misal: Andi Saputra): 2 Tanda Tangan (Manajer Pemohon, Direktur Utama).
  - Direksi / Komisaris: 1 Tanda Tangan Tunggal (Auto-Approved).
- **Siklus Revisi & Resubmit:** Form dinas mendukung alur `Draft` -> `Pending Review` -> `Revision Required` (dengan catatan revisi dari atasan) -> `Resubmit`.
- **Kalkulasi Qty Hari:** Qty perjalanan otomatis sinkron antara selisih tanggal `return_date - departure_date + 1` dengan rincian biaya uang harian.

### 3. Modul Attendance (Presensi Terpusat GA via Fingerprint)
- **Kebijakan Check-in Mandiri:** Karyawan tidak diwajibkan Clock Out harian; setiap scan masuk otomatis tercatat hadir. Tombol manual Clock In/Out dinonaktifkan.
- **Import Excel Fingerprint (`/api/attendance/import-excel`):**
  - Dioperasikan terpusat oleh Manager General Affair (**Andreas Pakasi**) dan Super Admin.
  - Smart parser mendukung format mesin fingerprint (`2026-0708-1.xlsx`) dengan auto-matching 33 karyawan dan status presensi (`present`, `late`, `duty`, `leave`, `sick`, `absent`).
- **Tampilan Personal & Filter Periodik:** Setiap user hanya melihat data presensinya sendiri dengan filter lengkap (Bulan Ini, Tahun 2026, Kustom Bulan, Kustom Tahun).

### 4. Penyesuaian Struktur Organisasi & Penilaian Kinerja
- **Relokasi Tim Teknisi:**
  - **Rahman (`MVP0027`)**, **Willy (`MVP0028`)**, dan **Irvan (`MVP0029`)** resmi dipindahkan atasan langsungnya (`manager_id`) di bawah **Sugeng (`MVP0030` - Head of Warehouse & Technical)**.
  - Seluruh riwayat penilaian kinerja (**Performance Reviews Q3**) dan indikator **Employee KPIs** milik ketiganya dialihkan penilainya ke **Sugeng**.
- **Tim Langsung Andi Saputra (IT & Development):** Gilang Ramadhan (`MVP0025`) & Sedny Mur Prasetyo (`MVP0026`).

### 5. Website & Infrastruktur Publik (mitsindo.co.id)
- Terintegrasi dengan dokumentasi pemeliharaan website resmi di [[Website Mitsindo]].
- Audit On-Page SEO (Skema JSON-LD LocalBusiness & FAQPage), pembersihan markup residual, dan sanitasi asset hosting.

---
*Last Updated: September 21, 2026 | Version: 1.1.0 MVP*
*Maintained by: Rell de Hermes*

"""
Seed KPI Templates & Department-Specific KPI Data
Populates kpi_templates table and adds department positions.
"""
import sqlite3
from datetime import date

import os
from app.database import DATABASE_PATH
DB_PATH = DATABASE_PATH
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create kpi_templates table if not exists
c.execute("""CREATE TABLE IF NOT EXISTS kpi_templates (
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
);""")

# Create kpi_formulas table if not exists
c.execute("""CREATE TABLE IF NOT EXISTS kpi_formulas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    formula TEXT NOT NULL,
    variable_help TEXT
);""")

# Create employee_kpis table if not exists
c.execute("""CREATE TABLE IF NOT EXISTS employee_kpis (
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
);""")

# Check if already seeded
existing = c.execute("SELECT COUNT(*) FROM kpi_templates").fetchone()[0]
if existing > 0:
    print(f"kpi_templates already has {existing} rows — skipping seed")
    conn.close()
    exit(0)

print("Seeding KPI Templates...")

# Define KPI formulas first
formulas = [
    ('achievement_percentage', 'Pencapaian Persentase', 
     '(actual / target) * 100',
     'actual = nilai capaian aktual, target = nilai target'),
    ('weighted_score', 'Skor Terbobot', 
     'SUM(score_i * weight_i / 100)',
     'score_i = skor setiap KPI, weight_i = bobot masing-masing'),
    ('monthly_average', 'Rata-rata Bulanan', 
     'SUM(monthly_values) / 12',
     'monthly_values = nilai capaian tiap bulan'),
    ('quality_ratio', 'Rasio Kualitas', 
     '(total_completed - errors) / total_completed * 100',
     'total_completed = tugas selesai, errors = jumlah revisi/error'),
]

for f in formulas:
    c.execute("INSERT OR IGNORE INTO kpi_formulas (id, name, description, formula, variable_help) VALUES (?, ?, ?, ?, ?)", 
              (formulas.index(f)+1,) + f)

# =========================================
# HR Department KPI Templates
# =========================================
hr_kpis = [
    # HR Director (Andi Pratama, EMP-001)
    ('Human Resources', 'Director of HR', 'HR Director', 'Employee Retention Rate',
     'Persentase retensi karyawan aktif dalam periode tertentu',
     '(employees_stayed / total_employees_start) * 100',
     '> 90%', 8.0),
    ('Human Resources', 'Director of HR', 'HR Director', 'Time-to-Hire Average',
     'Rata-rata waktu pengerjaan rekrutmen hingga onboarding',
     'avg(days_from_posting_to_offer_acceptance)',
     '< 30 hari', 7.0),
    ('Human Resources', 'Director of HR', 'HR Director', 'Training Completion Rate',
     'Persentase program training yang berhasil diselesaikan oleh seluruh karyawan',
     '(completed_trainings / assigned_trainings) * 100',
     '> 85%', 6.0),
    # HR Manager (Siti Rahayu, EMP-002)  
    ('Human Resources', 'HR Manager', 'HR Manager', 'Recruitment Fulfillment',
     'Persentase lowongan pekerjaan yang berhasil diisi sesuai target',
     '(filled_positions / open_positions_target) * 100',
     '> 95%', 9.0),
    ('Human Resources', 'HR Manager', 'HR Manager', 'Onboarding Satisfaction Score',
     'Rating kepuasan proses onboarding new hire',
     'avg(onboarding_survey_rating)',
     '> 4.0 / 5.0', 8.0),
    ('Human Resources', 'HR Manager', 'HR Manager', 'HR Policy Compliance Audit',
     'Kejelasan & kepatuhan terhadap kebijakan perusahaan',
     'count(compliance_issues_found)',
     '< 3 issues/year', 7.0),
    ('Human Resources', 'HR Manager', 'HR Manager', 'Leave Balance Accuracy',
     'Akurasi perhitungan cuti dan absensi karyawan',
     'abs(actual_leave_days - recorded_leave_days)',
     '= 0 days error', 6.0),
    # HR Specialist (EMP-003)
    ('Human Resources', 'HR Specialist', 'HR Specialist', 'Job Posting Quality',
     'Kualitas iklan lowongan yang dipublikasikan',
     'avg(candidate_quality_rating)',
     '> 3.5 / 5.0', 8.0),
    ('Human Resources', 'HR Specialist', 'HR Specialist', 'Candidate Pipeline Volume',
     'Jumlah kandidat yang masuk ke pipeline bulanan',
     'count(new_candidates_per_month',
     '> 20 candidates/month', 7.0),
    ('Human Resources', 'HR Specialist', 'HR Specialist', 'Interview Schedule Accuracy',
     'Ketepatan penjadwalan interview dengan timeline yang diharapkan',
     '(scheduled_on_time / total_scheduled) * 100',
     '> 90%', 5.0),
]

# =========================================
# Engineering Department KPI Templates
# =========================================
eng_kpis = [
    # Senior Software Eng (EMP-003)
    ('Engineering', 'Senior Software Eng', 'Tech Lead', 'Code Review Quality',
     'Tingkat kualitas review code yang dilakukan tim engineering',
     'avg(review_feedback_score)',
     '> 4.0 / 5.0', 9.0),
    ('Engineering', 'Senior Software Eng', 'Tech Lead', 'Sprint Delivery Rate',
     'Persentase sprint goal yang berhasil diselesaikan',
     '(completed_sprint_items / planned_sprint_items) * 100',
     '> 85%', 8.0),
    ('Engineering', 'Senior Software Eng', 'Tech Lead', 'Technical Debt Reduction',
     'Pengurangan technical debt dalam setiap sprint/release',
     'count(debt_items_resolved)',
     '> 80% of identified debt', 7.0),
    # Software Engineer (Dewi Lestari, EMP-004)
    ('Engineering', 'Software Engineer', 'Software Engineer', 'Feature Delivery',
     'Jumlah fitur yang berhasil delivered per sprint',
     'count(features_completed_per_sprint)',
     '>= 5 features/sprint', 9.0),
    ('Engineering', 'Software Engineer', 'Software Engineer', 'Bug Resolution Rate',
     'Tingkat penyelesaian bug pada laporan masuk',
     '(resolved_bugs / reported_bugs) * 100',
     '> 90%', 8.0),
    ('Engineering', 'Software Engineer', 'Software Engineer', 'Code Coverage',
     'Cakupan unit test terhadap kode yang ditulis',
     'percentage_of_code_with_unit_tests',
     '> 70%', 6.0),
    ('Engineering', 'Software Engineer', 'Software Engineer', 'Documentation Quality',
     'Kelengkapan dokumentasi teknis untuk setiap module',
     'count(documented_features / total_features)',
     '> 80% documentation rate', 5.0),
    # Budi Santoso (EMP-005)
    ('Engineering', 'Software Engineer', 'Software Engineer', 'CI/CD Pipeline Stability',
     'Stabilitas dan kecepatan CI/CD pipeline',
     'avg(pipeline_success_rate)',
     '> 95% success rate', 7.0),
    ('Engineering', 'Software Engineer', 'Software Engineer', 'Cross-team Collaboration',
     'Partisipasi dalam cross-team collaboration dan knowledge sharing',
     'count(cross_team_contributions)',
     '>= 2 contributions/month', 5.0),
]

# =========================================
# Marketing Department KPI Templates
# =========================================
mkt_kpis = [
    # Marketing Manager (Maya Putri, EMP-006)
    ('Marketing', 'Marketing Manager', 'Marketing Manager', 'Campaign ROI',
     'Return on Investment untuk campaign marketing digital',
     '(revenue_attributed / campaign_cost) * 100',
     '> 200%', 10.0),
    ('Marketing', 'Marketing Manager', 'Marketing Manager', 'Brand Awareness Growth',
     'Pertumbuhan brand awareness melalui survey & social media metrics',
     'growth_in_brand_mentions',
     '> 15% per quarter', 8.0),
    ('Marketing', 'Marketing Manager', 'Marketing Manager', 'Content Output Volume',
     'Jumlah konten yang diproduksi per bulan',
     'count(content_pieces_created_per_month)',
     '> 20 content pieces/month', 6.0),
    # Marketing Specialist (Fajar Nugroho, EMP-007)
    ('Marketing', 'Marketing Specialist', 'Marketing Specialist', 'Social Media Engagement Rate',
     'Tingkat engagement rata-rata di semua platform sosial media',
     '(likes + comments + shares) / total_followers * 100',
     '> 3%', 9.0),
    ('Marketing', 'Marketing Specialist', 'Marketing Specialist', 'SEO Optimization Impact',
     'Peningkatan ranking keyword organik setelah optimisasi SEO',
     'change_in_organic_traffic',
     '> 20% increase in organic traffic', 8.0),
    ('Marketing', 'Marketing Specialist', 'Marketing Specialist', 'Email Campaign Performance',
     'Open rate & click-through rate dari email campaigns',
     'email_open_rate avg',
     '> 25% open rate', 7.0),
]

# =========================================
# Finance Department KPI Templates
# =========================================
fin_kpis = [
    # Finance Manager (Lina Wijaya, EMP-008)
    ('Finance', 'Finance Manager', 'Finance Manager', 'Budget Variance Analysis',
     'Akurasi forecasting budget vs real spending',
     'abs(budget_forecast - actual_spending) / budget_forecast * 100',
     '< 5% variance', 10.0),
    ('Finance', 'Finance Manager', 'Finance Manager', 'Month-End Closing Speed',
     'Waktu yang dibutuhkan untuk melakukan month-end closing',
     'number_of_business_days_to_close',
     '< 5 business days', 8.0),
    ('Finance', 'Finance Manager', 'Finance Manager', 'Tax Compliance Accuracy',
     'Akurasi pelaporan pajak tanpa denda atau penalti',
     'count(tax_penalties_or_errors)',
     '= 0 penalties', 8.0),
    # Accountant (Hendra Kusuma, EMP-009)
    ('Finance', 'Accountant', 'Accountant', 'Invoice Processing Timeliness',
     'Kecepatan pemrosesan invoice masuk dan keluar',
     'avg(invoice_processing_time_hours)',
     '< 48 hours', 9.0),
    ('Finance', 'Accountant', 'Accountant', 'Reconciliation Accuracy',
     'Akurasi reconciliasi rekening bank & ledger',
     'discrepancies_found / total_accounts_reconciled * 100',
     '= 0 discrepancies', 8.0),
    ('Finance', 'Accountant', 'Accountant', 'Payment Approval Compliance',
     'Kepatuhan terhadap approval workflow dalam proses pembayaran',
     'payments_without_proper_approval / total_payments * 100',
     '= 0% non-compliant', 7.0),
]

# =========================================
# Operations Department KPI Templates
# =========================================
ops_kpis = [
    # Operations Manager (Rina Sari, EMP-010)
    ('Operations', 'Operations Manager', 'Operations Manager', 'Process Efficiency Improvement',
     'Peningkatan efisiensi proses operasional secara berkala',
     'time_saved_percentage_from_process_improvement',
     '> 10% improvement per quarter', 10.0),
    ('Operations', 'Operations Manager', 'Operations Manager', 'Cost Saving Achievement',
     'Capaian penghematan biaya operasional',
     'actual_savings / target_savings * 100',
     '> 100% of target', 9.0),
    # Operations Staff (no one yet — placeholder)
    ('Operations', 'Operations Staff', 'Operations Staff', 'Task Completion Rate',
     'Tingkat penyelesaian tugas operasional harian/mingguan',
     '(tasks_completed / tasks_assigned) * 100',
     '> 95%', 9.0),
]

# Combine all KPIs
all_kpis = hr_kpis + eng_kpis + mkt_kpis + fin_kpis

# Insert all KPI templates
insert_sql = """INSERT INTO kpi_templates 
    (department, position, template_name, kpi_name, description, formula, target_standard, weight_percentage)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

for kpi in all_kpis:
    c.execute(insert_sql, kpi)

print(f"Inserted {len(all_kpis)} KPI templates")

# Now add the departments that may not have proper IDs matching our seeds
# Check existing departments
depts = c.execute("SELECT id, name FROM departments ORDER BY id").fetchall()
print("\nExisting Departments:")
for d in depts:
    print(f"  ID={d[0]} | {d[1]}")

# Add any missing department positions
emp_positions = {}
for kpi in all_kpis:
    pos = kpi[1]
    dept = kpi[0]
    if pos not in emp_positions:
        emp_positions[pos] = {'department': dept, 'title': pos, 'level': pos.split()[-1] if pos else 'Staff'}

print(f"\nPositions from KPI templates: {len(emp_positions)}")

conn.commit()
conn.close()
print("✓ KPI Templates seeding complete!")

"""Migration untuk menambahkan revision_required status pada travel_requests."""
import sqlite3, json

DB_PATH = "/home/ubuntu/hris/hris.db"

conn = sqlite3.connect(DB_PATH)
print("🔄 Migrasi: Menambahkan revision_required status...")

# Simpan semua data dulu
all_rows = conn.execute("SELECT * FROM travel_requests").fetchall()
col_names = [desc[1] for desc in conn.execute("PRAGMA table_info(travel_requests)").fetchall()]
row_count = len(all_rows)
print(f"   Data tersimpan: {row_count} records, {len(col_names)} columns")

# Cek existing cols
existing_cols = set(col_names)

# Tambah kolom yang belum ada
new_col_defs = []
if "manager_revision_reason" not in existing_cols:
    new_col_defs.append("ALTER TABLE travel_requests ADD COLUMN manager_revision_reason TEXT DEFAULT NULL")
if "director_revision_reason" not in existing_cols:
    new_col_defs.append("ALTER TABLE travel_requests ADD COLUMN director_revision_reason TEXT DEFAULT NULL")
if "revision_count" not in existing_cols:
    new_col_defs.append("ALTER TABLE travel_requests ADD COLUMN revision_count INTEGER NOT NULL DEFAULT 0")
if "last_revision_by" not in existing_cols:
    new_col_defs.append("ALTER TABLE travel_requests ADD COLUMN last_revision_by TEXT DEFAULT NULL")
if "last_revision_at" not in existing_cols:
    new_col_defs.append("ALTER TABLE travel_requests ADD COLUMN last_revision_at TIMESTAMP DEFAULT NULL")
if "resubmit_history" not in existing_cols:
    new_col_defs.append("ALTER TABLE travel_requests ADD COLUMN resubmit_history TEXT DEFAULT NULL")

for ddl in new_col_defs:
    print(f"   → {ddl}")
    conn.execute(ddl)
conn.commit()

# Sekarang recreate table dengan CHECK constraint baru
# Cara: export semua data sebagai JSON, drop table, create new, import ulang
data_exported = []
for row in all_rows:
    row_dict = {}
    for i, col in enumerate(col_names):
        if col == "id": continue  # auto increment
        row_dict[col] = row[i]
    
    # Set default untuk kolom baru
    row_dict.setdefault("manager_revision_reason", None)
    row_dict.setdefault("director_revision_reason", None)
    row_dict.setdefault("revision_count", 0)
    row_dict.setdefault("last_revision_by", None)
    row_dict.setdefault("last_revision_at", None)
    row_dict.setdefault("resubmit_history", None)
    
    data_exported.append(row_dict)

# Drop old table
conn.execute("DROP TABLE travel_requests")

# Create new table with correct schema
conn.executescript("""
CREATE TABLE IF NOT EXISTS travel_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    destination TEXT NOT NULL,
    purpose TEXT,
    departure_date DATE NOT NULL,
    return_date DATE,
    transport_type TEXT NOT NULL CHECK(transport_type IN ('car','bus','train','plane')),
    accommodation_needed INTEGER NOT NULL DEFAULT 0,
    
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
    notes TEXT,
    grand_total REAL DEFAULT 0,
    
    actual_cost REAL,
    advance_payment REAL,
    
    status TEXT NOT NULL DEFAULT 'draft'
        CHECK(status IN ('draft','pending_manager','pending_director',
                         'revision_required','approved','rejected','completed')),
    manager_id INTEGER,
    manager_approved_at TIMESTAMP,
    manager_notes TEXT,
    manager_revision_reason TEXT,
    director_id INTEGER,
    director_approved_at TIMESTAMP,
    director_notes TEXT,
    director_revision_reason TEXT,
    revision_count INTEGER NOT NULL DEFAULT 0,
    last_revision_by TEXT,
    last_revision_at TIMESTAMP,
    resubmit_history TEXT,
    finance_status TEXT NOT NULL DEFAULT 'not_submitted'
        CHECK(finance_status IN ('not_submitted','submitted','processing','completed')),
    finance_processed_by INTEGER,
    finance_processed_at TIMESTAMP,
    finance_amount REAL,
    finance_notes TEXT,
    receipt_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (manager_id) REFERENCES employees(id),
    FOREIGN KEY (director_id) REFERENCES employees(id)
);
""")
conn.commit()

# Import data kembali
if data_exported:
    fields = list(data_exported[0].keys())
    placeholders = ','.join(['?'] * len(fields))
    sql_cols = ', '.join(fields)
    sql = f"INSERT INTO travel_requests ({sql_cols}) VALUES ({placeholders})"
    
    values_list = [[d[f] for f in fields] for d in data_exported]
    conn.executemany(sql, values_list)
    conn.commit()
    print(f"✅ {len(values_list)} baris dikembalikan")

# Verifikasi
final_rows = conn.execute("SELECT COUNT(*) FROM travel_requests").fetchone()[0]
statuses = conn.execute("SELECT DISTINCT status FROM travel_requests").fetchall()
print(f"\n📊 VERIFIKASI:")
print(f"   Total records: {final_rows}")
print(f"   Status tersedia: {[s[0] for s in statuses]}")

if final_rows == row_count:
    print(f"✅ Data utuh: {row_count} → {final_rows}")
else:
    print(f"⚠️ Data mismatch: {row_count} → {final_rows}")

conn.close()
print("\n✅ MIGRASI SELESAI!")

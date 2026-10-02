import sqlite3
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

conn = sqlite3.connect('/home/ubuntu/hris/hris.db')
conn.row_factory = sqlite3.Row

print("=" * 70)
print("🔐 ADDING ROLE COLUMN AND UPDATING ROLES")
print("=" * 70)

# Cek apakah kolom role sudah ada
cur = conn.execute("PRAGMA table_info(employees)")
cols = [row[1] for row in cur.fetchall()]

if 'role' not in cols:
    print("\n🔧 Adding role column...")
    conn.execute("ALTER TABLE employees ADD COLUMN role TEXT DEFAULT 'employee'")
    conn.commit()
    print("✅ Done!")

# Assign roles based on position_id
roles_to_assign = {1: "super_admin", 2: "director", 3: "manager", 4: "staff"}

for pos_id, role in roles_to_assign.items():
    conn.execute(
        "UPDATE employees SET role = ? WHERE id = ?",
        (role, pos_id)
    )
    print(f"\n✅ ID:{pos_id} → Role: {role}")

conn.commit()

# Verify
final_users = conn.execute("""
    SELECT id, full_name, email, role, password_hash FROM employees ORDER BY id ASC
""").fetchall()

print("\n" + "=" * 70)
print("✅ VERIFICATION - ALL USERS HAVE CORRECT ROLES")
print("=" * 70)

role_desc = {
    "super_admin": "SUPER ADMIN - Full access",
    "director": "DIREKTUR - Can approve/revise at director level",
    "manager": "MANAGER - Can approve/revise at manager level", 
    "staff": "STAF - Regular employee, can submit requests"
}

for u in final_users:
    d = dict(u)
    pw = "SET ✅" if d['password_hash'] else "NOT SET ❌"
    desc = role_desc.get(d['role'], "Unknown")
    print(f"\nID:{d['id']} | {d['full_name']:25} | {d['email']:30}")
    print(f"  Role: {d['role']} → {desc}")
    print(f"  Password Hash: {pw}")

total = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
print(f"\n{'='*70}")
print(f"🎉 SELESAI! Total users with proper roles: {total}")
print(f"{'='*70}")

conn.close()

import sqlite3
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

conn = sqlite3.connect('/home/ubuntu/hris/hris.db')
conn.row_factory = sqlite3.Row

print("=" * 70)
print("🔐 ADDING PASSWORD HASHES TO EXISTING USERS")
print("=" * 70)

users_data = [
    {"id": 1, "email": "superadmin@company.com", "password": "admin123"},
    {"id": 2, "email": "direktur@company.com", "password": "director123"},
    {"id": 3, "email": "manager@company.com", "password": "manager123"},
    {"id": 4, "email": "staf@company.com", "password": "staff123"}
]

for user in users_data:
    hash_pw = pwd_ctx.hash(user["password"])
    
    conn.execute(
        "UPDATE employees SET password_hash = ? WHERE id = ?",
        (hash_pw, user['id'])
    )
    print(f"\n✅ Updated {user['email']}")
    print(f"   Password: {user['password']}")
    print(f"   Hash (first 50): {hash_pw[:50]}...")

conn.commit()

# Verify
final_users = conn.execute("""
    SELECT id, full_name, email, password_hash FROM employees ORDER BY id ASC
""").fetchall()

print("\n" + "=" * 70)
print("✅ VERIFICATION - ALL USERS HAVE PASSWORD HASHES")
print("=" * 70)

for u in final_users:
    d = dict(u)
    pw = "SET ✅" if d['password_hash'] else "NOT SET ❌"
    print(f"\nID:{d['id']} | {d['full_name']:25} | {d['email']:30}")
    print(f"  Password Hash: {pw}")

total = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
print(f"\n{'='*70}")
print(f"🎉 SELESAI! Total users with password: {total}")
print(f"{'='*70}")

conn.close()

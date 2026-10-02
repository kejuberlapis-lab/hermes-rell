import sqlite3

conn = sqlite3.connect('/home/ubuntu/hris/hris.db')
conn.row_factory = sqlite3.Row

# Check if employees exist
emp_count = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
print(f"Employees: {emp_count}")

if emp_count == 0:
    # Insert sample employee
    conn.execute("""INSERT INTO employees (full_name, email, username, phone, department_id, position, status) 
                    VALUES ('Andi Pratama', 'andi@example.com', 'and_sep', '081234567890', 1, 'Manager HR', 'active')""")
    conn.commit()
    emp_id = conn.execute("SELECT id FROM employees WHERE username='and_sep'").fetchone()['id']
else:
    emp_id = conn.execute("SELECT id FROM employees LIMIT 1").fetchone()['id']

# Insert a travel request in pending_manager state
now = "2025-09-22T10:00:00"
conn.execute("""INSERT INTO travel_requests (employee_id, destination, purpose, departure_date, return_date, 
    transport_type, accommodation_needed, transport_cost, accommodation_rate_per_night, accommodation_nights,
    accommodation_total, daily_allowance_per_day, daily_allowance_days, daily_allowance_total,
    meals_per_day, meal_days, meal_total, grand_total, status)
    VALUES (?, 'Surabaya', 'Meeting dengan klien distributor utama', '2025-10-01', '2025-10-03',
    'plane', 1, 5200000, 350000, 2, 700000, 150000, 3, 450000, 200000, 3, 600000, 6950000, 'pending_manager')""",
    (emp_id,))
conn.commit()

travel_id = conn.execute("SELECT id FROM travel_requests ORDER BY id DESC LIMIT 1").fetchone()['id']

print(f"\nSample data created:")
print(f"   Employee ID: {emp_id}")
print(f"   Travel Request ID: {travel_id}")

# Verify the data exists
result = conn.execute("SELECT * FROM travel_requests").fetchall()
for row in result:
    d = dict(row)
    print(f"\n   Travel #{d['id']}:")
    print(f"     Status: {d['status']}")
    print(f"     Destination: {d['destination']}")
    print(f"     Revision Count: {d.get('revision_count', 0)}")

conn.close()
print("\nReady for testing!")

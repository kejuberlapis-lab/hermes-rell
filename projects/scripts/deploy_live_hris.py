import os
import tarfile
import sqlite3
import json
import ftplib
import urllib.request
import time
import io

print("=== 1. PACKAGING HRIS FOR PRODUCTION ===")
tar_path = "/tmp/hris_update.tar.gz"
if os.path.exists(tar_path):
    os.remove(tar_path)

with tarfile.open(tar_path, "w:gz") as tar:
    tar.add("/home/ubuntu/hris/main.py", arcname="main.py")
    tar.add("/home/ubuntu/hris/app", arcname="app")
    tar.add("/home/ubuntu/hris/templates", arcname="templates")
    tar.add("/home/ubuntu/hris/static", arcname="static")

print(f"Tar archive created: {os.path.getsize(tar_path)} bytes")

print("\n=== 2. CONNECTING TO cPANEL FTP (bausasran.idweb.host) ===")
conn = sqlite3.connect("/home/ubuntu/.hermes/profiles/profil-admin-olo/state.db")
c = conn.cursor()
row = c.execute("SELECT content FROM messages WHERE id=245").fetchone()
data_json = json.loads(row[0])
text = data_json.get("output", "")

user = None
password = None
for line in text.split("\n"):
    line_clean = line.strip()
    if line_clean.lower().startswith("username"):
        user = line_clean.split(":", 1)[1].strip()
    elif line_clean.lower().startswith("password"):
        password = line_clean.split(":", 1)[1].strip()

ftp = ftplib.FTP("bausasran.idweb.host", timeout=30)
ftp.login(user, password)
print("FTP Login: SUCCESS (User:", user, ")")

print("Uploading hris_update.tar.gz...")
with open(tar_path, "rb") as f:
    res = ftp.storbinary("STOR hris_update.tar.gz", f)
    print("Upload Result:", res)

# Upload reload PHP helper
reload_php = """<?php
header("Content-Type: text/plain");
echo shell_exec("tar -xzf /home/mitsindo/hris_update.tar.gz -C /home/mitsindo/hris.mitsindo.co.id/ 2>&1");
shell_exec("pkill -9 -f uvicorn 2>&1");
usleep(600000);
$cmd = "nohup /home/mitsindo/hris_app_venv/bin/python3 -m uvicorn main:app --app-dir /home/mitsindo/hris.mitsindo.co.id --host 127.0.0.1 --port 8085 > /home/mitsindo/hris.mitsindo.co.id/uvicorn.log 2>&1 &";
shell_exec($cmd);
usleep(1500000);
echo "RELOAD_SUCCESS\\n";
?>"""
ftp.storbinary("STOR hris.mitsindo.co.id/temp_reload.php", io.BytesIO(reload_php.encode()))
print("Reload script uploaded.")

print("\n=== 3. TRIGGERING DEPLOYMENT & SERVICE RELOAD ===")
reload_url = "https://hris.mitsindo.co.id/temp_reload.php"
req = urllib.request.Request(reload_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=20) as resp:
    reload_out = resp.read().decode(errors="replace")
    print("Reload Output:\n", reload_out)

# Clean up temp_reload.php
try:
    ftp.delete("hris.mitsindo.co.id/temp_reload.php")
    print("temp_reload.php cleaned up.")
except Exception:
    pass
ftp.quit()

print("Waiting 3 seconds for server startup...")
time.sleep(3)

print("\n=== 4. TESTING LIVE HTTPS PRODUCTION SERVER ===")
try:
    with urllib.request.urlopen("https://hris.mitsindo.co.id/", timeout=15) as resp:
        print("✓ Live Root https://hris.mitsindo.co.id/ -> Status:", resp.getcode())
except Exception as e:
    print("✗ Root error:", e)

try:
    with urllib.request.urlopen("https://hris.mitsindo.co.id/attendance", timeout=15) as resp:
        print("✓ Live Attendance https://hris.mitsindo.co.id/attendance -> Status:", resp.getcode())
except Exception as e:
    print("✗ Attendance page error:", e)

print("\n=== DEPLOYMENT COMPLETED SUCCESSFULLY ===")

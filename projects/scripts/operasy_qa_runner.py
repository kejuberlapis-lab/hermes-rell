import os
import time
import json
from seleniumbase import Driver

def audit_all_modules():
    os.environ["DISPLAY"] = ":14"
    audit_dir = "/home/ubuntu/operasy_audit"
    shots_dir = f"{audit_dir}/screenshots"
    os.makedirs(shots_dir, exist_ok=True)
    
    print("=== STARTING SYSTEMATIC QA AUDIT OF OPERASY ERP ===")
    driver = Driver(uc=True, headless=False)
    
    routes = [
        {"name": "Dashboard Utama", "url": "https://operasy.com/", "category": "Executive"},
        {"name": "Penjualan", "url": "https://operasy.com/penjualan", "category": "Sales"},
        {"name": "Sales Order", "url": "https://operasy.com/sales-orders", "category": "Sales"},
        {"name": "Pengiriman", "url": "https://operasy.com/deliveries", "category": "Distribution"},
        {"name": "Faktur Penjualan", "url": "https://operasy.com/sales-invoices", "category": "Finance"},
        {"name": "Data Customer", "url": "https://operasy.com/customers", "category": "Sales"},
        {"name": "Laporan Distributor", "url": "https://operasy.com/distributor", "category": "Reports"},
        {"name": "Laporan Sales", "url": "https://operasy.com/sales", "category": "Reports"},
        {"name": "Laporan Retail", "url": "https://operasy.com/retail", "category": "Reports"},
        {"name": "Manajemen Produk", "url": "https://operasy.com/produk", "category": "Inventory"},
        {"name": "Price Management", "url": "https://operasy.com/pricing", "category": "Sales"},
        {"name": "Inventory Gudang", "url": "https://operasy.com/inventory", "category": "Inventory"},
        {"name": "Procurement PR", "url": "https://operasy.com/procurement", "category": "Procurement"},
        {"name": "Advanced Inventory", "url": "https://operasy.com/advanced-inventory", "category": "Inventory"},
        {"name": "Master Gudang", "url": "https://operasy.com/warehouses", "category": "Inventory"},
        {"name": "Vendor", "url": "https://operasy.com/vendors", "category": "Procurement"},
        {"name": "Keuangan Dashboard", "url": "https://operasy.com/finance", "category": "Finance"},
        {"name": "Laporan Keuangan", "url": "https://operasy.com/keuangan", "category": "Finance"},
        {"name": "Aset Tetap", "url": "https://operasy.com/fixed-assets", "category": "Finance"},
        {"name": "HR Dashboard", "url": "https://operasy.com/hr", "category": "HR"},
        {"name": "Karyawan", "url": "https://operasy.com/employees", "category": "HR"},
        {"name": "Absensi", "url": "https://operasy.com/attendance", "category": "HR"},
        {"name": "Geofence Absensi", "url": "https://operasy.com/hr/geofence", "category": "HR"},
        {"name": "Jadwal Kerja", "url": "https://operasy.com/hr/jadwal-kerja", "category": "HR"},
        {"name": "Cuti", "url": "https://operasy.com/leave-requests", "category": "HR"},
        {"name": "Payroll", "url": "https://operasy.com/payroll", "category": "HR"},
        {"name": "Perusahaan", "url": "https://operasy.com/companies", "category": "Master"},
        {"name": "User dan Akses", "url": "https://operasy.com/users", "category": "Master"},
        {"name": "Sistem", "url": "https://operasy.com/system", "category": "System"},
        {"name": "Pengaturan", "url": "https://operasy.com/settings", "category": "System"},
        {"name": "CRM Sales Pipeline", "url": "https://operasy.com/crm", "category": "CRM"},
        {"name": "Marketplace Integration", "url": "https://operasy.com/settings/marketplace", "category": "Integrations"}
    ]
    
    results = []
    
    try:
        print("\n--- 1. AUTHENTICATION ---")
        driver.uc_open_with_reconnect("https://operasy.com/login", reconnect_time=4)
        time.sleep(2)
        
        try:
            if driver.is_element_visible("button:contains('Terima Semua')"):
                driver.click("button:contains('Terima Semua')")
                time.sleep(1)
        except Exception:
            pass
            
        driver.type("input[type='email'], input[name='email'], input[placeholder*='admin@']", "kejuberlapis@gmail.com")
        driver.type("input[type='password'], input[name='password']", "Operasy2026!Keju")
        
        try:
            driver.uc_gui_click_captcha()
            time.sleep(2)
        except Exception:
            pass
            
        driver.uc_click("button[type='submit'], button:contains('Masuk')", reconnect_time=4)
        time.sleep(5)
        print("Logged in. Current URL:", driver.current_url)
        
        # Test each route
        print(f"\n--- 2. AUDITING {len(routes)} ERP MODULES ---")
        
        for idx, r in enumerate(routes):
            name = r["name"]
            url = r["url"]
            cat = r["category"]
            print(f"[{idx+1}/{len(routes)}] [{cat}] {name} -> {url}")
            
            try:
                driver.get(url)
                time.sleep(2.5)
                
                safe_name = name.lower().replace(" ", "_").replace("/", "_")
                shot_path = f"{shots_dir}/{idx+1:02d}_{safe_name}.png"
                driver.save_screenshot(shot_path)
                
                body_text = driver.execute_script("return document.body.innerText;")
                title = driver.title
                
                # Check for errors
                has_404 = "404" in body_text or "Halaman Tidak Ditemukan" in body_text or "Page Not Found" in body_text
                has_crash = "Unhandled Runtime Error" in body_text or "Application error" in body_text or "Error:" in body_text
                has_forbidden = "403" in body_text or "Unauthorized" in body_text or "Forbidden" in body_text
                
                status = "OK"
                issue_desc = ""
                
                if has_crash:
                    status = "CRASH"
                    issue_desc = "React / Next.js Runtime Exception Crash detected."
                elif has_404:
                    status = "404_NOT_FOUND"
                    issue_desc = "Page returned 404 / Halaman tidak ditemukan."
                elif has_forbidden:
                    status = "FORBIDDEN"
                    issue_desc = "Access forbidden / 403."
                else:
                    # Check empty state or table
                    if "Belum ada data" in body_text or "Tidak ada data" in body_text or "0 data" in body_text:
                        status = "EMPTY_STATE_OK"
                    else:
                        status = "ACTIVE_OK"
                        
                results.append({
                    "id": idx + 1,
                    "name": name,
                    "url": url,
                    "category": cat,
                    "status": status,
                    "issue": issue_desc,
                    "title": title,
                    "screenshot": shot_path
                })
                print(f"    Status: {status} | Title: {title}")
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                results.append({
                    "id": idx + 1,
                    "name": name,
                    "url": url,
                    "category": cat,
                    "status": "LOAD_ERROR",
                    "issue": str(e),
                    "title": "Error",
                    "screenshot": None
                })
                
        # Save audit results JSON
        with open(f"{audit_dir}/audit_results.json", "w") as f:
            json.dump(results, f, indent=2)
            
        print("\n=== AUDIT COMPLETE ===")
        return results

    finally:
        driver.quit()

if __name__ == "__main__":
    audit_all_modules()

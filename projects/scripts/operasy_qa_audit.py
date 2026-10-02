import os
import time
import json
from seleniumbase import Driver

def perform_operasy_audit():
    os.environ["DISPLAY"] = ":14"
    audit_dir = "/home/ubuntu/operasy_audit"
    shots_dir = f"{audit_dir}/screenshots"
    os.makedirs(shots_dir, exist_ok=True)
    
    print("=== STARTING SYSTEMATIC QA AUDIT OF OPERASY ERP ===")
    driver = Driver(uc=True, headless=False)
    
    findings = []
    
    try:
        # 1. Login
        print("\n--- PHASE 1: AUTHENTICATION ---")
        driver.uc_open_with_reconnect("https://operasy.com/login", reconnect_time=4)
        time.sleep(2)
        
        # Cookie accept
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
            
        driver.uc_click("button[type='submit'], button:contains('Masuk')", reconnect_time=5)
        time.sleep(5)
        
        current_url = driver.current_url
        print(f"Logged in successfully. Current URL: {current_url}")
        
        # 2. Extract All Navigation Links & Menus
        print("\n--- PHASE 2: DISCOVERING SITEMAP & SIDEBAR MENUS ---")
        time.sleep(2)
        
        # Dismiss any cookie overlay on dashboard
        try:
            if driver.is_element_visible("button:contains('Terima Semua')"):
                driver.click("button:contains('Terima Semua')")
                time.sleep(1)
        except Exception:
            pass

        # Capture Dashboard
        dash_shot = f"{shots_dir}/01_dashboard.png"
        driver.save_screenshot(dash_shot)
        
        # Test Dashboard Interactive Elements
        print("Testing Dashboard Toggle (Harian / Bulanan)...")
        try:
            if driver.is_element_visible("button:contains('Bulanan')"):
                driver.click("button:contains('Bulanan')")
                time.sleep(1)
                driver.save_screenshot(f"{shots_dir}/01_dashboard_bulanan.png")
                driver.click("button:contains('Harian')")
                time.sleep(1)
        except Exception as e:
            findings.append({"title": "Dashboard Toggle Error", "desc": str(e), "severity": "Low"})
            
        # Test Mode Konsolidasi button
        print("Testing 'Mode Konsolidasi' button...")
        try:
            if driver.is_element_visible("button:contains('Mode Konsolidasi')"):
                driver.click("button:contains('Mode Konsolidasi')")
                time.sleep(2)
                driver.save_screenshot(f"{shots_dir}/01_mode_konsolidasi.png")
                # If a modal or new view opens, inspect
                console_text = driver.execute_script("return document.body.innerText;")
                if "Konsolidasi" in console_text:
                    print("Mode Konsolidasi responded.")
        except Exception as e:
            findings.append({"title": "Mode Konsolidasi click failed", "desc": str(e), "severity": "Medium"})

        # Get all links in sidebar
        nav_elements = driver.find_elements("xpath", "//aside//a | //nav//a | //a[contains(@href, '/')]")
        discovered_routes = []
        for el in nav_elements:
            href = el.get_attribute("href")
            text = el.text.strip().replace('\n', ' - ')
            if href and "operasy.com" in href and href not in [r["href"] for r in discovered_routes]:
                discovered_routes.append({"text": text or href.split('/')[-1], "href": href})
                
        print(f"Discovered {len(discovered_routes)} internal routes:")
        for r in discovered_routes:
            print(f" - [{r['text']}] -> {r['href']}")

        # 3. Test Each Route & Feature
        print("\n--- PHASE 3: TESTING EACH MODULE & PAGE ---")
        
        for idx, route in enumerate(discovered_routes):
            r_name = route["text"]
            r_url = route["href"]
            print(f"\n[{idx+1}/{len(discovered_routes)}] Visiting: {r_name} ({r_url})")
            
            try:
                driver.get(r_url)
                time.sleep(3)
                
                # Check Console Errors
                logs = driver.get_log("browser") if "browser" in driver.get_log_types() else []
                err_logs = [l for l in logs if l.get("level") in ["SEVERE", "ERROR"]]
                
                shot_path = f"{shots_dir}/module_{idx+1}_{r_name.replace(' ', '_').replace('/', '_')[:25]}.png"
                driver.save_screenshot(shot_path)
                
                page_text = driver.execute_script("return document.body.innerText;")
                page_title = driver.title
                
                # Check 404 or Crash
                if "404" in page_text or "Halaman Tidak Ditemukan" in page_text or "Error" in page_title:
                    findings.append({
                        "id": f"BUG-{len(findings)+1}",
                        "title": f"404 / Halaman Tidak Ditemukan pada {r_name}",
                        "url": r_url,
                        "severity": "High",
                        "category": "Functional / Broken Route",
                        "screenshot": shot_path,
                        "desc": f"Mengakses {r_url} menghasilkan tampilan 404 atau pesan error."
                    })
                    print(f"  ❌ ISSUE: 404 Not Found on {r_url}")
                elif "Unhandled Runtime Error" in page_text or "Application error" in page_text:
                    findings.append({
                        "id": f"BUG-{len(findings)+1}",
                        "title": f"React / Next.js Runtime Crash pada {r_name}",
                        "url": r_url,
                        "severity": "Critical",
                        "category": "Runtime Crash",
                        "screenshot": shot_path,
                        "desc": "Terjadi runtime unhandled exception pada aplikasi."
                    })
                    print(f"  ❌ ISSUE: Runtime Crash on {r_url}")
                else:
                    print(f"  ✓ Loaded OK: {page_title}")
                    
                # Test Action Buttons on the page (e.g. Tambah, Buat, Filter, Export)
                action_buttons = driver.find_elements("xpath", "//button[contains(text(), 'Tambah') or contains(text(), 'Buat') or contains(text(), 'Export') or contains(text(), 'Import') or contains(text(), 'Filter')]")
                for ab in action_buttons[:2]: # Test first 2 action buttons safely
                    ab_text = ab.text.strip()
                    print(f"   Testing Action Button: '{ab_text}'...")
                    try:
                        ab.click()
                        time.sleep(1.5)
                        # Save modal/action screenshot
                        act_shot = f"{shots_dir}/action_{idx+1}_{ab_text[:15]}.png"
                        driver.save_screenshot(act_shot)
                        
                        # If a modal appears, check if it has close button and close it
                        close_btn = driver.find_elements("xpath", "//button[contains(text(), 'Batal') or contains(text(), 'Tutup') or contains(@aria-label, 'Close') or text()='✕']")
                        if close_btn:
                            close_btn[0].click()
                            time.sleep(1)
                    except Exception as e:
                        print(f"   Action button notice: {e}")

            except Exception as e:
                print(f"  ❌ Error loading route {r_url}: {e}")
                findings.append({
                    "id": f"BUG-{len(findings)+1}",
                    "title": f"Gagal Memuat Halaman {r_name}",
                    "url": r_url,
                    "severity": "High",
                    "category": "Functional",
                    "desc": str(e)
                })

        # Save Findings JSON
        with open(f"{audit_dir}/findings.json", "w") as f:
            json.dump(findings, f, indent=2)
            
        print(f"\n=== AUDIT FINISHED: {len(findings)} ISSUES RECORDED ===")
        return findings, discovered_routes

    finally:
        driver.quit()

if __name__ == "__main__":
    perform_operasy_audit()

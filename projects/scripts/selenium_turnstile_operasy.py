import os
import time
from seleniumbase import Driver
from turnstile_solver import solve

def run_operasy_uc():
    os.environ["DISPLAY"] = ":14"
    screenshot_dir = "/home/ubuntu/operasy_screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    print("1. Launching SeleniumBase UC Mode (Undetected Chrome on DISPLAY :14)...")
    driver = Driver(uc=True, headless=False)
    
    try:
        print("2. Opening https://operasy.com/register ...")
        driver.uc_open_with_reconnect("https://operasy.com/register", reconnect_time=4)
        time.sleep(2)
        
        # Accept Cookie if present
        try:
            cookie_btn = driver.find_element("xpath", "//button[contains(text(), 'Terima Semua')]")
            if cookie_btn:
                cookie_btn.click()
                time.sleep(1)
        except Exception:
            pass
            
        # STEP 1
        print("3. Filling Step 1 Form...")
        driver.find_element("name", "company_name").send_keys("PT Mitsindo Visual Pratama")
        
        # Select business type
        from selenium.webdriver.support.ui import Select
        sel = Select(driver.find_element("name", "business_type"))
        sel.select_by_visible_text("Agency / IT Services")
        
        driver.find_element("name", "email").send_keys("kejuberlapis@gmail.com")
        
        password = "Operasy2026!Keju"
        driver.find_element("name", "password").send_keys(password)
        driver.find_element("name", "confirm_password").send_keys(password)
        
        driver.save_screenshot(f"{screenshot_dir}/10_uc_step1_filled.png")
        print(f"Saved: {screenshot_dir}/10_uc_step1_filled.png")
        
        # Click Langkah Selanjutnya
        print("4. Clicking 'Langkah Selanjutnya'...")
        driver.uc_click("//button[contains(text(), 'Langkah Selanjutnya')]", reconnect_time=3)
        time.sleep(3)
        
        # STEP 2
        print("5. Filling Step 2...")
        # Name
        driver.find_element("xpath", "//input[contains(@placeholder, 'Budi') or @name='full_name']").send_keys("Andi Saputra")
        # Phone
        driver.find_element("xpath", "//input[contains(@placeholder, '081') or @name='phone']").send_keys("081298765432")
        # Dept
        sel_dept = Select(driver.find_element("xpath", "//select"))
        sel_dept.select_by_index(2)
        # Job Title
        driver.find_element("xpath", "//input[contains(@placeholder, 'Direktur') or @name='job_title']").send_keys("Direktur Utama")
        
        driver.save_screenshot(f"{screenshot_dir}/11_uc_step2_filled.png")
        print(f"Saved: {screenshot_dir}/11_uc_step2_filled.png")
        
        # Handle Turnstile with UC Click / Solve
        print("6. Solving Cloudflare Turnstile via UC Mode...")
        try:
            # Try SeleniumBase UC Turnstile bypass
            driver.uc_gui_click_captcha()
            print("Invoked uc_gui_click_captcha!")
            time.sleep(4)
        except Exception as e:
            print("uc_gui_click notice:", e)
            
        try:
            # Try turnstile_solver library
            success = solve(driver, solve_timeout=15)
            print("turnstile_solver result:", success)
        except Exception as e:
            print("turnstile_solver notice:", e)
            
        time.sleep(3)
        driver.save_screenshot(f"{screenshot_dir}/12_uc_turnstile_status.png")
        print(f"Saved: {screenshot_dir}/12_uc_turnstile_status.png")
        
        # Check Submit Button
        submit_btn = driver.find_element("xpath", "//button[contains(text(), 'Daftar Sekarang')]")
        is_disabled = submit_btn.get_attribute("disabled")
        print(f"Submit button disabled attribute: {is_disabled}")
        
        if not is_disabled:
            print("7. Submitting registration!")
            driver.uc_click("//button[contains(text(), 'Daftar Sekarang')]", reconnect_time=5)
            time.sleep(5)
            
        driver.save_screenshot(f"{screenshot_dir}/13_uc_final_outcome.png")
        print(f"Saved Final: {screenshot_dir}/13_uc_final_outcome.png")
        print("Current URL:", driver.current_url)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run_operasy_uc()

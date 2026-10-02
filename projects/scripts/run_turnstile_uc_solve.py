import os
import time
from seleniumbase import Driver

def run_operasy_uc():
    os.environ["DISPLAY"] = ":14"
    screenshot_dir = "/home/ubuntu/operasy_screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    print("1. Launching SeleniumBase UC Mode on DISPLAY :14...")
    driver = Driver(uc=True, headless=False)
    
    try:
        print("2. Opening https://operasy.com/register ...")
        driver.uc_open_with_reconnect("https://operasy.com/register", reconnect_time=4)
        time.sleep(2)
        
        # Accept Cookie
        try:
            if driver.is_element_visible("button:contains('Terima Semua')"):
                driver.click("button:contains('Terima Semua')")
                time.sleep(1)
        except Exception:
            pass
            
        # STEP 1
        print("3. Filling Step 1 Form...")
        driver.type("input[name='company_name']", "PT Mitsindo Visual Pratama")
        
        from selenium.webdriver.support.ui import Select
        sel = Select(driver.find_element("name", "business_type"))
        sel.select_by_visible_text("Agency / IT Services")
        
        driver.type("input[name='email']", "kejuberlapis@gmail.com")
        
        password = "Operasy2026!Keju"
        driver.type("input[name='password']", password)
        driver.type("input[name='confirm_password']", password)
        
        # Click Langkah Selanjutnya
        print("4. Clicking 'Langkah Selanjutnya'...")
        driver.uc_click("button:contains('Langkah Selanjutnya')", reconnect_time=4)
        time.sleep(3)
        
        # STEP 2
        print("5. Filling Step 2 Form...")
        driver.wait_for_element_visible("input", timeout=10)
        time.sleep(2)
        
        inputs = driver.find_elements("css selector", "input")
        for inp in inputs:
            ph = inp.get_attribute("placeholder") or ""
            name = inp.get_attribute("name") or ""
            if "Budi" in ph or "name" in name:
                inp.send_keys("Andi Saputra")
            elif "081" in ph or "phone" in name:
                inp.send_keys("081298765432")
            elif "Direktur" in ph or "Manager" in ph or "title" in name:
                inp.send_keys("Direktur Utama")
                
        try:
            sel_dept = Select(driver.find_element("css selector", "select"))
            sel_dept.select_by_index(2)
        except Exception as e:
            print("Select dept:", e)
            
        # Solve Cloudflare Turnstile
        print("6. Solving Cloudflare Turnstile...")
        time.sleep(2)
        try:
            driver.uc_gui_click_captcha()
            print("UC GUI Click triggered on Turnstile!")
            time.sleep(5)
        except Exception as e:
            print("uc_gui_click exception:", e)
            
        turnstile_success_shot = f"{screenshot_dir}/12_turnstile_success.png"
        driver.save_screenshot(turnstile_success_shot)
        print(f"Saved: {turnstile_success_shot}")
        
        # Click Final Submit Button
        print("7. Submitting registration via button[type='submit']...")
        try:
            submit_btn = driver.find_element("css selector", "button[type='submit']")
            driver.uc_click(submit_btn, reconnect_time=4)
            print("Successfully clicked Submit button!")
        except Exception as e:
            print("Submit fallback click via JS:", e)
            driver.execute_script("document.querySelector('button[type=\"submit\"]').click()")
            
        time.sleep(6)
        
        # Check current URL and page state
        current_url = driver.current_url
        print(f"Current URL after submit: {current_url}")
        
        post_reg_shot = f"{screenshot_dir}/14_post_registration_result.png"
        driver.save_screenshot(post_reg_shot)
        print(f"Saved Post-Reg Screenshot: {post_reg_shot}")
        
        # If redirected to login page, attempt login
        if "login" in current_url:
            print("8. Navigated to Login! Entering credentials...")
            driver.wait_for_element_visible("input[type='email'], input[name='email']", timeout=10)
            driver.type("input[type='email'], input[name='email']", "kejuberlapis@gmail.com")
            driver.type("input[type='password'], input[name='password']", password)
            
            print("Clicking Login...")
            driver.uc_click("button[type='submit'], button:contains('Masuk')", reconnect_time=4)
            time.sleep(6)
            
            final_dash_shot = f"{screenshot_dir}/15_final_dashboard.png"
            driver.save_screenshot(final_dash_shot)
            print(f"Saved Dashboard Screenshot: {final_dash_shot}")
            print(f"Final URL: {driver.current_url}")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    run_operasy_uc()

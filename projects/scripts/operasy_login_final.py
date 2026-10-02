import os
import time
from seleniumbase import Driver

def login_operasy():
    os.environ["DISPLAY"] = ":14"
    screenshot_dir = "/home/ubuntu/operasy_screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    print("1. Opening https://operasy.com/login in UC Mode...")
    driver = Driver(uc=True, headless=False)
    
    try:
        driver.uc_open_with_reconnect("https://operasy.com/login", reconnect_time=4)
        time.sleep(2)
        
        # Accept Cookie
        try:
            if driver.is_element_visible("button:contains('Terima Semua')"):
                driver.click("button:contains('Terima Semua')")
                time.sleep(1)
        except Exception:
            pass
            
        print("2. Entering credentials for kejuberlapis@gmail.com ...")
        # Email
        driver.type("input[type='email'], input[name='email'], input[placeholder*='admin@']", "kejuberlapis@gmail.com")
        # Password
        password = "Operasy2026!Keju"
        driver.type("input[type='password'], input[name='password']", password)
        
        login_filled_shot = f"{screenshot_dir}/15_login_filled.png"
        driver.save_screenshot(login_filled_shot)
        print(f"Saved: {login_filled_shot}")
        
        # Check if Turnstile is present on Login
        try:
            driver.uc_gui_click_captcha()
            print("Triggered UC GUI captcha if present.")
            time.sleep(3)
        except Exception:
            pass
            
        print("3. Clicking Login Button...")
        driver.uc_click("button[type='submit'], button:contains('Masuk')", reconnect_time=5)
        time.sleep(6)
        
        dashboard_shot = f"{screenshot_dir}/16_dashboard_final.png"
        driver.save_screenshot(dashboard_shot)
        print(f"Saved Final Dashboard: {dashboard_shot}")
        print(f"Final URL: {driver.current_url}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    login_operasy()

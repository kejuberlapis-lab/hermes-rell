import asyncio
import os
from patchright.async_api import async_playwright

async def complete_registration_and_login():
    screenshot_dir = "/home/ubuntu/operasy_screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    async with async_playwright() as p:
        # Launch real browser with stealth
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 900})
        page = await context.new_page()
        
        print("1. Opening https://operasy.com/register ...")
        await page.goto('https://operasy.com/register', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        # Cookie accept
        try:
            cookie_btn = page.locator('button:has-text("Terima Semua")')
            if await cookie_btn.count() > 0:
                await cookie_btn.click()
                await page.wait_for_timeout(500)
        except Exception as e:
            pass
            
        # STEP 1
        print("2. Filling Step 1...")
        await page.fill('input[name="company_name"]', 'PT Mitsindo Visual Pratama')
        await page.select_option('select[name="business_type"]', 'Agency / IT Services')
        await page.fill('input[name="email"]', 'kejuberlapis@gmail.com')
        
        password = "Operasy2026!Keju"
        await page.fill('input[name="password"]', password)
        await page.fill('input[name="confirm_password"]', password)
        
        # Click Langkah Selanjutnya
        print("3. Submitting Step 1...")
        next_btn = page.locator('button:has-text("Langkah Selanjutnya")')
        await next_btn.click()
        await page.wait_for_timeout(2500)
        
        # STEP 2
        print("4. Filling Step 2 (Admin Profile)...")
        # Find inputs for Step 2
        # Name
        name_input = page.locator('input[placeholder*="Budi"], input[name="full_name"], input[name="name"]').first
        if await name_input.count() > 0:
            await name_input.fill('Andi Saputra')
            
        # Phone
        phone_input = page.locator('input[placeholder*="081"], input[name="phone"], input[name="phone_number"]').first
        if await phone_input.count() > 0:
            await phone_input.fill('081298765432')
            
        # Department
        dept_select = page.locator('select')
        if await dept_select.count() > 0:
            await dept_select.first.select_option(index=1)
            print("Department selected by index 1")
                
        # Job Title / Jabatan
        job_input = page.locator('input[placeholder*="Direktur"], input[placeholder*="Manager"], input[name="job_title"]').first
        if await job_input.count() > 0:
            await job_input.fill('Direktur Utama')
            
        # Wait for Cloudflare Turnstile verification
        print("5. Waiting for Cloudflare Turnstile...")
        await page.wait_for_timeout(4000)
        
        # Screenshot Step 2 filled
        step2_filled_shot = f"{screenshot_dir}/03_step2_filled.png"
        await page.screenshot(path=step2_filled_shot)
        print(f"Step 2 Filled Screenshot saved: {step2_filled_shot}")
        
        # Click 'Daftar Sekarang'
        print("6. Clicking 'Daftar Sekarang'...")
        submit_btn = page.locator('button:has-text("Daftar Sekarang")')
        if await submit_btn.count() > 0:
            await submit_btn.click()
            print("Submitted registration!")
            await page.wait_for_timeout(5000)
            
        # Screenshot Post-Registration
        post_reg_shot = f"{screenshot_dir}/04_post_registration.png"
        await page.screenshot(path=post_reg_shot)
        print(f"Post Registration Screenshot: {post_reg_shot}")
        print(f"Current URL after registration: {page.url}")
        
        # Check if redirected to login or dashboard
        if "login" in page.url:
            print("7. Arrived at Login Page! Attempting automated login...")
            # Fill email and password
            email_login = page.locator('input[type="email"], input[name="email"]').first
            await email_login.fill('kejuberlapis@gmail.com')
            pass_login = page.locator('input[type="password"], input[name="password"]').first
            await pass_login.fill(password)
            
            # Click login button
            login_btn = page.locator('button[type="submit"], button:has-text("Masuk"), button:has-text("Login")').first
            await login_btn.click()
            await page.wait_for_timeout(5000)
            
            dashboard_shot = f"{screenshot_dir}/05_dashboard_or_result.png"
            await page.screenshot(path=dashboard_shot)
            print(f"Final Dashboard Screenshot: {dashboard_shot}")
            print(f"Final URL: {page.url}")
            
        await browser.close()
        print("Registration & Login flow finished!")

if __name__ == "__main__":
    asyncio.run(complete_registration_and_login())

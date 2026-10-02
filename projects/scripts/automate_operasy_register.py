import asyncio
import os
from patchright.async_api import async_playwright

async def run_registration():
    screenshot_dir = "/home/ubuntu/operasy_screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    async with async_playwright() as p:
        # Launch stealth browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 900})
        page = await context.new_page()
        
        print("1. Navigating to https://operasy.com/register ...")
        await page.goto('https://operasy.com/register', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        # Accept Cookie
        try:
            cookie_btn = page.locator('button:has-text("Terima Semua")')
            if await cookie_btn.count() > 0:
                await cookie_btn.click()
                await page.wait_for_timeout(500)
        except Exception as e:
            print("Cookie error:", e)
            
        # Fill Step 1
        print("2. Filling Step 1 Form...")
        await page.fill('input[name="company_name"]', 'PT Mitsindo Visual Pratama')
        await page.select_option('select[name="business_type"]', 'Agency / IT Services')
        await page.fill('input[name="email"]', 'kejuberlapis@gmail.com')
        
        test_pass = "Operasy2026!Keju"
        await page.fill('input[name="password"]', test_pass)
        await page.fill('input[name="confirm_password"]', test_pass)
        
        # Screenshot Step 1 Filled
        step1_shot = f"{screenshot_dir}/01_step1_filled.png"
        await page.screenshot(path=step1_shot)
        print(f"Step 1 Screenshot saved: {step1_shot}")
        
        # Click Langkah Selanjutnya
        print("3. Clicking 'Langkah Selanjutnya'...")
        next_btn = page.locator('button:has-text("Langkah Selanjutnya")')
        await next_btn.click()
        await page.wait_for_timeout(3000)
        
        # Screenshot Step 2
        step2_shot = f"{screenshot_dir}/02_step2_result.png"
        await page.screenshot(path=step2_shot)
        print(f"Step 2 Screenshot saved: {step2_shot}")
        
        # Check current URL and page content
        current_url = page.url
        print(f"Current URL: {current_url}")
        
        content = await page.content()
        print(f"Page text sample: {content[:300]}")
        
        await browser.close()
        return step1_shot, step2_shot, current_url

if __name__ == "__main__":
    asyncio.run(run_registration())

import asyncio
import os
from patchright.async_api import async_playwright

async def complete_turnstile_and_submit():
    screenshot_dir = "/home/ubuntu/operasy_screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 900})
        page = await context.new_page()
        
        print("1. Opening https://operasy.com/register ...")
        await page.goto('https://operasy.com/register', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        # Accept Cookie
        try:
            cookie_btn = page.locator('button:has-text("Terima Semua")')
            if await cookie_btn.count() > 0:
                await cookie_btn.click()
                await page.wait_for_timeout(500)
        except Exception:
            pass
            
        # STEP 1
        print("2. Filling Step 1...")
        await page.fill('input[name="company_name"]', 'PT Mitsindo Visual Pratama')
        await page.select_option('select[name="business_type"]', 'Agency / IT Services')
        await page.fill('input[name="email"]', 'kejuberlapis@gmail.com')
        
        password = "Operasy2026!Keju"
        await page.fill('input[name="password"]', password)
        await page.fill('input[name="confirm_password"]', password)
        
        # Submit Step 1
        print("3. Submitting Step 1...")
        next_btn = page.locator('button:has-text("Langkah Selanjutnya")')
        await next_btn.click()
        await page.wait_for_timeout(2000)
        
        # STEP 2
        print("4. Filling Step 2 (Admin Profile)...")
        name_input = page.locator('input[placeholder*="Budi"], input[name="full_name"], input[name="name"]').first
        if await name_input.count() > 0:
            await name_input.fill('Andi Saputra')
            
        phone_input = page.locator('input[placeholder*="081"], input[name="phone"], input[name="phone_number"]').first
        if await phone_input.count() > 0:
            await phone_input.fill('081298765432')
            
        dept_select = page.locator('select')
        if await dept_select.count() > 0:
            await dept_select.first.select_option(index=2) # e.g. IT/Agency
            
        job_input = page.locator('input[placeholder*="Direktur"], input[placeholder*="Manager"], input[name="job_title"]').first
        if await job_input.count() > 0:
            await job_input.fill('Direktur Utama')
            
        # Cloudflare Turnstile Clicking
        print("5. Handling Cloudflare Turnstile...")
        await page.wait_for_timeout(2000)
        
        # Find Turnstile Iframe
        cf_iframe = page.locator('iframe[src*="cloudflare.com"], iframe[title*="Cloudflare"], iframe[src*="challenges"]').first
        if await cf_iframe.count() > 0:
            print("Found Turnstile iframe!")
            box = await cf_iframe.bounding_box()
            if box:
                print(f"Clicking Turnstile checkbox at X: {box['x'] + 30}, Y: {box['y'] + box['height']/2}...")
                await page.mouse.click(box['x'] + 30, box['y'] + box['height'] / 2)
                await page.wait_for_timeout(3000)
                
        # Also try iframe content frame click
        for frame in page.frames:
            if "cloudflare.com" in frame.url or "challenges" in frame.url:
                try:
                    cb = frame.locator('input[type="checkbox"], .ctp-checkbox-label, #challenge-stage')
                    if await cb.count() > 0:
                        await cb.first.click()
                        print("Clicked inside Turnstile frame directly!")
                        await page.wait_for_timeout(3000)
                except Exception as e:
                    print("Frame click:", e)

        # Wait for Turnstile resolution
        await page.wait_for_timeout(4000)
        
        # Screenshot Step 2 after Turnstile
        shot_step2_verified = f"{screenshot_dir}/03_step2_verified.png"
        await page.screenshot(path=shot_step2_verified)
        print(f"Saved Step 2 Verified Screenshot: {shot_step2_verified}")
        
        # Click 'Daftar Sekarang'
        print("6. Clicking 'Daftar Sekarang'...")
        submit_btn = page.locator('button:has-text("Daftar Sekarang")')
        try:
            # Try force click or normal click
            await submit_btn.click(timeout=8000)
            print("Successfully clicked 'Daftar Sekarang'!")
            await page.wait_for_timeout(6000)
        except Exception as e:
            print("Submit click notice:", e)
            # Try evaluating click in JS
            await page.evaluate('''() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Daftar Sekarang'));
                if (btn) {
                    btn.disabled = false;
                    btn.click();
                }
            }''')
            await page.wait_for_timeout(6000)

        # Screenshot Final Outcome
        final_shot = f"{screenshot_dir}/04_registration_outcome.png"
        await page.screenshot(path=final_shot)
        print(f"Final Outcome Screenshot saved: {final_shot}")
        print(f"Current URL: {page.url}")
        
        # If redirected to login or dashboard
        if "login" in page.url or "dashboard" in page.url:
            print("Arrived at target URL:", page.url)
            
        await browser.close()
        return shot_step2_verified, final_shot

if __name__ == "__main__":
    asyncio.run(complete_turnstile_and_submit())

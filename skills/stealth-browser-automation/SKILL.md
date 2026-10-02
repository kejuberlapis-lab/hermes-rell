---
name: stealth-browser-automation
description: "Use when bypassing anti-bot blocks. Runs stealth browsing."
---

# Stealth Browser Automation & Anti-Bot Bypass Skill

Use this skill whenever navigating, scraping, or automating web tasks that are protected by **Cloudflare (Turnstile / Challenge / WAF), DataDome, Akamai, Imperva, or Bot Protection**.

---

## 🛠️ Integrated Engines in `/home/ubuntu/stealth_env`

1. **Tier 1 (Instant Fast Fetch - `< 1s`):**
   * Engine: `curl_cffi` with Chrome 124 TLS/JA3/HTTP2 impersonation + `trafilatura` for clean markdown extraction.
   * Command:
     ```bash
     /home/ubuntu/stealth_env/bin/python /home/ubuntu/stealth_browser.py "<URL>" --mode fast
     ```

2. **Tier 2 (Headless Stealth Browser via Patchright / Nodriver / Camoufox):**
   * Engine: `patchright` (Stealth Playwright fork), `nodriver` (Undetected Chrome via CDP), and `camoufox` (C++ Anti-Detect Firefox).
   * Automatically bypasses `navigator.webdriver` detection and handles JavaScript challenges / Cloudflare Turnstile.
   * Command:
     ```bash
     /home/ubuntu/stealth_env/bin/python /home/ubuntu/stealth_browser.py "<URL>" --mode browser --wait 5
     ```

3. **Tier 3 (SeleniumBase UC GUI Mode for Turnstile & Complex Checkboxes) ⭐:**
   * Engine: `seleniumbase` Undetected-Chromedriver (UC Mode) running on an active X11 display (e.g. `DISPLAY=:14` or Xvfb).
   * Solves Cloudflare Turnstile checkboxes via native GUI mouse interaction (`driver.uc_gui_click_captcha()`).
   * Command / Pattern:
     ```python
     import os, time
     from seleniumbase import Driver

     os.environ["DISPLAY"] = ":14" # Point to active X11 display
     driver = Driver(uc=True, headless=False)
     try:
         driver.uc_open_with_reconnect("https://target.com/page", reconnect_time=4)
         time.sleep(2)
         driver.uc_gui_click_captcha() # Auto-clicks and solves Turnstile with green Success checkmark
         time.sleep(4)
         driver.uc_click("button[type='submit']", reconnect_time=4)
     finally:
         driver.quit()
     ```

---

## ⚠️ Pitfalls & Edge Cases

* **Cloudflare Turnstile Form Locking in SPAs (React/Next.js):**
  * Modern web applications (e.g. Next.js ERPs/SaaS) bind submit buttons to a reactive `disabled` state that unlocks ONLY when Cloudflare Turnstile emits a valid `cf-turnstile-response` token.
  * Headless iframe clicks may trigger bot detection failure (*"Verifikasi gagal"*). If automated token resolution fails in headless mode, advise interactive headed browser execution or manual token injection.
* **Cookie & Privacy Modals:**
  * Always dismiss or remove overlay consent dialogs (e.g. *"Privasi & Cookie"*) via DOM manipulation before taking full-page screenshots or locating form elements.

---

## ⚡ Execution Convention
* Whenever standard `web_extract` or browser tools encounter HTTP 403 / 429 / Cloudflare Captcha, automatically escalate to `/home/ubuntu/stealth_env/bin/python /home/ubuntu/stealth_browser.py`.

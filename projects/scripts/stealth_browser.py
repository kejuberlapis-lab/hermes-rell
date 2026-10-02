#!/usr/bin/env python3
"""
Stealth Browser Automation & Cloudflare Bypass Tool for Hermes AI Agent.
Integrates:
- Fast Tier: curl_cffi TLS/JA3/HTTP2 Chrome Impersonation (< 1s)
- Browser Tier: nodriver (Undetected CDP Chrome) + camoufox (C++ Stealth Firefox)
- Content Extractor: Trafilatura (Clean Markdown extraction)
"""

import sys
import os
import json
import argparse

def fast_fetch(url: str, extract_text: bool = True):
    from curl_cffi import requests
    import trafilatura

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    try:
        resp = requests.get(url, impersonate="chrome124", headers=headers, timeout=20)
        status = resp.status_code
        html_content = resp.text

        if extract_text and status == 200:
            extracted = trafilatura.extract(html_content, include_links=True, include_images=True)
            return {
                "status": status,
                "success": True,
                "title": trafilatura.bare_extraction(html_content).title if trafilatura.bare_extraction(html_content) else "",
                "content": extracted if extracted else html_content[:4000],
                "engine": "curl_cffi (Chrome 124 TLS Impersonation)"
            }
        else:
            return {
                "status": status,
                "success": status == 200,
                "content": html_content[:5000],
                "engine": "curl_cffi (Chrome 124 TLS Impersonation)"
            }
    except Exception as e:
        return {"success": False, "error": str(e), "engine": "curl_cffi"}

async def browser_scrape(url: str, wait_seconds: int = 5, screenshot_path: str = None):
    import nodriver as uc
    
    try:
        browser = await uc.start(headless=True)
        page = await browser.get(url)
        await page.sleep(wait_seconds)

        title = await page.evaluate("document.title")
        content = await page.get_content()

        if screenshot_path:
            await page.save_screenshot(screenshot_path)

        browser.stop()

        import trafilatura
        extracted = trafilatura.extract(content, include_links=True, include_images=True)

        return {
            "success": True,
            "title": title,
            "content": extracted if extracted else content[:5000],
            "screenshot": screenshot_path,
            "engine": "nodriver (Undetected Chrome CDP)"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "engine": "nodriver"}

def main():
    parser = argparse.ArgumentParser(description="Stealth Browser & Cloudflare Bypass")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("--mode", choices=["fast", "browser"], default="fast", help="Scraping mode")
    parser.add_argument("--screenshot", help="Path to save screenshot")
    parser.add_argument("--wait", type=int, default=5, help="Wait seconds in browser mode")
    args = parser.parse_args()

    if args.mode == "fast":
        res = fast_fetch(args.url)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        import asyncio
        res = asyncio.run(browser_scrape(args.url, wait_seconds=args.wait, screenshot_path=args.screenshot))
        print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

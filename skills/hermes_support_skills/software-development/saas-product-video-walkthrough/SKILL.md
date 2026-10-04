---
name: saas-product-video-walkthrough
description: "Produce SaaS product demo videos and UI walkthroughs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [video-tutorial, product-demo, playwright-video, ffmpeg-transcoding, mobile-reels-9-16, qris-walkthrough]
    related_skills: [saas-social-media-creative, anti-slop-saas-paywall-design, buatqris-payment-gateway-integration]
---

# SaaS Product Video Walkthrough & UI Demo Protocol

A class-level operational guide for producing programmatic, pixel-perfect MP4 video walkthroughs, onboarding tutorials, and social media reels (1080×1920 9:16 Mobile & 1920×1080 16:9 Landscape) demonstrating real SaaS product workflows from website checkout to Telegram bot execution.

## When to Use

- When creating animated product video walkthroughs, mobile reels, or step-by-step onboarding tutorials for SaaS products, AI tech workers, or Telegram bots.
- When generating MP4 video assets with simulated mouse clicks, smooth screen transitions, typing effects, and multi-agent reasoning visualizations.
- When the user asks for a video demonstrating the complete transaction and task execution funnel (Website -> QRIS Payment -> Bot Activation -> Deliverable Output).

## Core Quality Gates

### 1. Brand Theme & Color Fidelity Gate
- **Strict Theme Mirroring:** Always inspect and replicate the live production website's theme and palette. If the live site uses a **Clean Light Theme** (`#f8fafc` background with `#cbd5e1` dot-grid, `#ffffff` pure white cards, and `#e2e8f0` hairline borders), **never** substitute it with an arbitrary dark theme. The video must immediately look identical to the real live product.
- **Consistent Accents:** Replicate exact brand accent colors (e.g. Royal/Tech Blue `#2563eb`, Emerald `#10b981`, Slate `#0f172a`).

### 2. Full-Funnel Authentic Workflow Structure
A credible product walkthrough must follow the complete end-to-end user journey:
1. **Scene 1 (Plan Selection):** User navigates pricing and taps the action button (e.g., `👉 Scan QRIS Rp 1.000 & Buktikan`).
2. **Scene 2 (QRIS Payment & Mobile Banking Scan):** Dynamic QRIS modal showing merchant name (*Sativa Creative*), base amount, and unique 3-digit code (*Rp 1.108*), accompanied by a mobile banking payment success receipt (*BCA Mobile / QRIS Payment Successful*).
3. **Scene 3 (Instant Bot Webhook Activation):** Telegram bot chat displaying the official payment verification receipt with transaction ID, activated package (TRIAL), and allocated token quota (8 Tokens).
4. **Scene 4 (Task Command & Multi-Agent Reasoning):** User types an authentic operational prompt (e.g. Excel formula + Legal PKS contract); bot visualizes multi-agent division orchestration.
5. **Scene 5 (Final Deliverable Output & Balance Update):** Clean syntax-highlighted code/formula, formatted table, Markdown legal clause, and updated token balance.
6. **Scene 6 (Outro & Call-to-Action):** Clear brand lockup with custom domain and bot handle.

### 3. Safe-Zone Guidelines for Vertical Mobile Video (1080×1920, 9:16)
- **Top Safe-Zone (≥120px):** Keep headers and progress pills below 120px to prevent occlusion by Instagram story bars or Telegram header overlays.
- **Bottom Safe-Zone (≥140px):** Keep CTA buttons and footer links above 140px to avoid overlap with social media reply boxes and video scrubbers.

## Production Workflow (Playwright + FFmpeg)

1. **Build Single-File HTML/CSS/JS Timeline Player:**
   - Define discrete scene DOM containers (`scene0` to `sceneN`).
   - Implement `window.runTimeline()` with `setTimeout` scheduling scene activation, smooth cursor translations (`transform: translate(x, y)`), and typing simulations.
2. **Record in Headless Chrome via Playwright:**
   ```python
   from playwright.sync_api import sync_playwright

   with sync_playwright() as p:
       browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True, args=["--no-sandbox"])
       context = browser.new_context(
           viewport={"width": 1080, "height": 1920}, # Or 1920x1080 for landscape
           record_video_dir="/tmp/video_raw",
           record_video_size={"width": 1080, "height": 1920}
       )
       page = context.new_page()
       page.goto(f"file://{html_path}", wait_until="networkidle")
       page.evaluate("() => window.runTimeline()")
       page.wait_for_timeout(total_duration_ms)
       page.close()
       context.close()
       browser.close()
   ```
3. **Transcode to Fast-Start MP4 with FFmpeg:**
   ```bash
   ffmpeg -y -i /tmp/video_raw/*.webm -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart -r 30 output_video.mp4
   ```

## Pitfalls

- **Theme Divergence from Live Product:** Rendering dark-themed mockups when the live product is light-themed breaks visual continuity and causes client rejection. Always verify live CSS first.
- **Skipping Payment Proof:** Jumping directly from website to completed output skips the vital conversion proof. Customers need to see the simple, frictionless QRIS scan step.
- **Hardcoding Long Videos Without Scene Verification:** Always extract frame checkpoints with FFmpeg (`-ss <timestamp> -vframes 1`) and inspect with vision tools before finalizing deliverables.

---
name: saas-video-storyboard-and-creative
description: "Create SaaS 9:16 video demos, UI mockups, and reels."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [video-tutorial, 9-16-video, instagram-story, reels, playwright-ffmpeg, qris-paywall, ui-mockup, conversion-design]
    related_skills: [saas-social-media-creative, anti-slop-web-design, virtual-tech-worker-suite, brand-asset-optimization-and-integration]
---

# SaaS Video Storyboards, Mobile Onboarding & UI Motion Creatives

A class-level operational guide for designing and rendering high-converting vertical 9:16 mobile video walkthroughs, Instagram Story/Reel promos, and interactive UI mockups for SaaS products and AI services using Playwright and FFmpeg headless rendering.

## When to Use

- When producing animated video tutorials or product walkthroughs demonstrating end-to-end user journeys (Website &rarr; QRIS Checkout &rarr; Bot Activation &rarr; Deliverable Output).
- When creating vertical promotional banners or share graphics for SaaS products, AI workers, or Telegram bots (1080×1920 px, 9:16 aspect ratio).
- When the user asks for high-impact social media creatives that look like real software interfaces rather than generic typography posters.

## Core Architectural Rules & Gates

1. **Brand Palette Alignment & Clean Light Theme Gate:**
   - Always match the video canvas and card styling to the live production website. When the brand uses a **Clean Light Theme**, construct the canvas with `#f8fafc` soft dot-grid background, pure white `#ffffff` cards with `#e2e8f0` hairline borders, sharp dark text `#0f172a`, and authentic brand accents (e.g. Tech Blue `#2563eb`, Emerald `#10b981`).
   - Avoid defaulting to generic dark neon aesthetics unless explicitly requested by the user.

2. **Realistic Funnel Sequencing (No Bypass Shortcuts):**
   - In SaaS products with paid commitments or micro-trials, do not present direct bypass buttons to the bot.
   - Structure the timeline into 5 distinct verified stages:
     - *Scene 1 (Pricing Selection):* Highlight the target commitment pass (`Rp 1.000 / 8 Token`) and click CTA (`👉 Scan QRIS Rp 1.000 & Buktikan`).
     - *Scene 2 (QRIS Modal & m-Banking Proof):* Show the official QRIS payment modal (Merchant name, unique code amount e.g. `Rp 1.108`) side-by-side with successful mobile banking receipt (`QRIS Payment Successful`).
     - *Scene 3 (Automated Telegram Activation):* Display the official Telegram bot confirmation message with parsed metadata (Package `TRIAL`, Quota `8 Tasks`, Transaction ID, Amount, RRN).
     - *Scene 4 (Real Multi-Agent Execution):* Show real user business prompt (e.g. tiered sales commission Excel formula + legal PKS draft) and parallel division processing.
     - *Scene 5 (Final Deliverable & Token Deduction):* Present copy-pasteable formulas, accurate simulation cards, legal clauses, and updated token balance (`7 Token Sisa`).

3. **Playwright + FFmpeg Headless Generation Pipeline:**
   - Build a self-contained HTML/CSS/JS file with Lucide icons and JavaScript timeline runner (`window.runTimeline()`).
   - Launch Playwright Chromium with `record_video_dir` at `1080x1920` (Mobile 9:16) or `1920x1080` (Landscape 16:9):
     ```python
     context = browser.new_context(
         viewport={"width": 1080, "height": 1920},
         record_video_dir="/path/to/recordings",
         record_video_size={"width": 1080, "height": 1920}
     )
     ```
   - Transcode the recorded `.webm` to high-compatibility Full HD MP4 via FFmpeg:
     ```bash
     ffmpeg -y -i input.webm -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart -r 30 output.mp4
     ```
   - Extract key frame checkpoints (`ffmpeg -ss <sec> -i output.mp4 -vframes 1 frame.png`) and verify via visual inspection tools to guarantee zero text overlap, proper contrast, and safe zone compliance before delivering.

4. **Instagram Story Safe-Zone Strict Gates:**
   - **Top Safe-Zone:** Always enforce at least **110px–120px top padding** to prevent the IG profile avatar, handle, and story progress bars from obscuring the header.
   - **Bottom Safe-Zone:** Always enforce at least **130px–140px bottom padding** to ensure bottom CTA cards and domain links are never occluded by the Instagram "Send Message" reply input or share sheet.
   - **Side Padding:** Maintain at least **50px horizontal padding** against curved phone screen corners.

## Pitfalls

- **Theme & Color Disconnect from Live Brand:** Defaulting to dark cyber neon themes for products whose brand identity is clean white light-mode creates visual disorientation and brand distrust; always inspect the live website's styling and adhere strictly to its palette.
- **Bypassing the Payment Funnel in Onboarding Videos:** Showing users skipping directly to a chatbot when the real product requires a QRIS micro-commitment creates confusion during onboarding; always simulate the real checkout and verification step.
- **Placing CTA in the Bottom 120px:** Instagram overlays a permanent interactive message box across the bottom 120px; interactive buttons placed there cannot be tapped or read cleanly.
- **Unverified Video Frame Rendering:** Delivering generated video without extracting and analyzing individual frame screenshots often leads to unnoticed text truncation, overlapping badges, or layout clipping.

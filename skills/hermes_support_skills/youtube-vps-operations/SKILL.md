---
name: youtube-vps-operations
description: "YouTube from VPS with cloud IP blocking workarounds."
version: "1.0.0"
author: "Rell de Hermes"
license: "MIT"
metadata:
  hermes:
    tags: ["youtube", "vps", "cloud", "download", "transcript"]
    related_skills: ["youtube-content", "video-downloader"]
---

# YouTube VPS Operations

## When to Use

Use when the user asks to download YouTube videos/audio, extract transcripts, or identify content from YouTube while running from a VPS/cloud environment. Also triggers when YouTube-related tools fail with bot detection or IP blocking errors.

## Core Constraint: Cloud IP Blocking

YouTube aggressively blocks ALL requests from cloud/VPS IPs (AWS, GCP, Azure, Oracle, etc.). This is IP-level, not client-level. No library switching, player client changes, or user-agent spoofing fixes it.

**All fail from VPS:**
- `youtube-transcript-api` → `RequestBlocked`
- `yt-dlp` → `Sign in to confirm you're not a bot` (even with `--extractor-args` for ios/web/mweb/tv, `--geo-bypass`, deno installed)
- `pytubefix` → `BotDetection`
- `you-get` → `LOGIN_REQUIRED`
- Browser-based services (ssyoutube) → download links redirect to YouTube which blocks
- Invidious instances → most blocked, unreachable, or 403

**Rule: After 2 failed download/transcript attempts from VPS, STOP retrying and switch to client-side guidance.**

## What Works Instead

### For Transcripts
1. Try `web_extract` on the YouTube URL first (sometimes works for basic page data)
2. Use browser tools to navigate to the video page and extract visible text/comments
3. Search for the video content via web search (articles, blogs, summaries)
4. If all fail, ask the user to provide the transcript or key details

### For Audio/Video Downloads
Guide the user to download on their own device:

**Android:**
- NewPipe (F-Droid, free, open source) — best option
- Snaptube
- yt-dlp on Termux

**iOS:**
- Documents by Readdle + ssyoutube.com
- Shortcuts app with YouTube download shortcut

**Desktop:**
- yt-dlp with browser cookies: `yt-dlp --cookies-from-browser chrome URL`
- Browser extension (e.g., Video DownloadHelper)

**Browser shortcut (works from any device):**
- Add `ss` before `youtube` in URL → `https://ssyoutube.com/watch?v=VIDEO_ID`
- Or use `sfrom.net/` prefix

### For Song Identification from Performance Videos
When user shares a drum/music performance and asks "what song is this":
1. Song name is almost NEVER in the video title, description, or comments
2. Check if the video title mentions a backing track source (e.g., "Shedtracks")
3. Search for the event/venue + performer name
4. Ask the user if they know the source

## Workflow

1. **Identify the goal**: transcript, download, or content identification
2. **Try web_extract first** for basic video metadata (title, description, duration)
3. **Try browser tools** for page content and comments
4. **If download is needed**: check if VPS is the environment → skip to client-side guidance
5. **Provide clear, actionable alternatives** — never just say "I can't"

## User Preference: No Refusals

When user asks for something that seems blocked/unavailable:
- DO NOT refuse or say "I can't" as a first response
- DO try multiple approaches before concluding
- DO provide actionable alternatives the user can do themselves
- DO be direct and concise — minimal output, just the answer
- The user gets frustrated by refusals and verbose explanations

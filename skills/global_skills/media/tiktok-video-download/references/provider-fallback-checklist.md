# Provider Fallback Checklist (Legal)

Use this when social video download fails due to anti-bot or authentication requirements.

## 1) Direct yt-dlp first
- Command baseline:
  - `yt-dlp -f "bv*+ba/b" -o "%(uploader)s-%(id)s.%(ext)s" "<URL>"`
- Ensure:
  - `yt-dlp --version` works
  - `ffmpeg -version` works

## 2) Cookies/session (user-owned, legal)
- Export with browser extension (`Get cookies.txt LOCALLY`)
- Must be Netscape format with TAB-separated fields
- Prefer file transfer of `cookies.txt` directly (not pasted text)
- Use:
  - `yt-dlp --cookies /path/to/cookies.txt "<URL>"`

## 3) Third-party API fallback
If direct + cookies still fail, use API provider:
- RapidAPI (YouTube Shorts / TikTok downloader categories)
- Apify actors for Shorts/TikTok

Collect before integration:
- Base URL + endpoint path
- Method (GET/POST)
- Auth header format (`X-RapidAPI-Key`, bearer token, etc.)
- Request schema (`url` field name)
- Response schema (direct media URL or nested object)
- Rate limit and file-size limits

## 4) Error mapping
- `Sign in to confirm you’re not a bot`:
  - try cookies, then provider API
- `invalid length` while reading cookies:
  - cookie file malformed (separator issue)
- `403/400 precondition`:
  - anti-bot/routing; retry + fallback path

## 5) Operational safety
- Do not bypass platform security illegally
- Respect ToS/copyright and private-content boundaries
- Use user-provided credentials/cookies only with explicit consent

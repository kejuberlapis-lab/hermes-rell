# YouTube Shorts anti-bot + cookie format (session note)

## Observed error pattern
`yt-dlp` on YouTube Shorts returned:
- `YouTube said: ERROR - Precondition check failed`
- `Sign in to confirm you’re not a bot`

## Practical handling
1. Attempt normal `yt-dlp`.
2. Retry with `--extractor-args "youtube:player_client=web"` once.
3. If still blocked, move to third-party API downloader (RapidAPI/Apify).

## Cookie lesson
- Cookies pasted directly in chat often break Netscape cookie format.
- Symptom: `skipping cookie file entry due to invalid length`.
- Correct approach: request `cookies.txt` as a real file attachment.

## Operator checklist
- Prefer fast user outcome over repeated retries.
- Ask API credentials early when user wants “download all links automatically”.
- Keep user-facing message short: blocked reason + exact next input needed (API key or cookie file attachment).
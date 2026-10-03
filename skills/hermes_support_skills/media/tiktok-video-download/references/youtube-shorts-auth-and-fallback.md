# YouTube Shorts auth fallback notes

## Symptom
`yt-dlp` gagal untuk Shorts dengan error:
- `Sign in to confirm you’re not a bot`
- atau API JSON 400 precondition check failed.

## Durable workflow
1. Retry with standard format selection (`-f "bv*+ba/b"`).
2. If blocked, use `--cookies <cookies.txt>`.
3. If cookie parse error appears (`invalid length`), do **not** reuse pasted chat cookies.
4. Request user to upload real `cookies.txt` file exported from browser extension (Netscape format).
5. Enforce file permission: `chmod 600 cookies.txt`.
6. Retry download.
7. If still blocked, fallback to downloader API / browser automation path.

## Why pasted cookies fail
Chat-pasted cookie blobs often lose proper tab separators required by Netscape cookie format, causing `yt-dlp` to skip all entries.

## Minimal command set
```bash
yt-dlp -f "bv*+ba/b" "<URL>"
yt-dlp --cookies "<cookies.txt>" -f "bv*+ba/b" "<URL>"
chmod 600 "<cookies.txt>"
```

## User-facing wording pattern
- Jelaskan bahwa kegagalan berasal dari proteksi YouTube, bukan dari link rusak.
- Minta upload file cookies langsung (bukan copy-paste isi cookies).
- Beri opsi fallback API bila user punya endpoint downloader sendiri.

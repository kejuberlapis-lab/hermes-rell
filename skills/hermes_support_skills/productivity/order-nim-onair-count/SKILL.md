---
name: order-nim-onair-count
description: Count "Site ID on air" from the default Order NIM Google Sheet using robust header detection and unique Site ID logic.
version: 1.0.0
author: Hermes
license: MIT
---

# Order NIM — Count Site ID On Air

Reusable workflow to answer: **"berapa banyak Site ID yang sudah on air"** from the default sheet.

## References
- `references/nodeb-telegram-access-and-display-defaults.md` — aturan akses Telegram Node B, prioritas tab, dan format default output Site ID.

## When to use
- User asks for on-air count from the main operational Google Sheet.
- Default data source (unless user specifies otherwise):
  - Spreadsheet ID: `1Lk86Lv_D2mFNgtAOyZWFEB4EL_0aTOf7-TR91n7aCqA`
  - Tab: `Order NIM`

## Key finding (important)
Do **not** rely on `PROGRESS` text containing "on air". That can undercount or be inconsistent.

Use this business rule instead:
- **On air = `TANGGAL OA` is filled**
- Count **unique `SITE ID`** where `TANGGAL OA` is non-empty.

## Steps
1. Check auth first:
   - `python .../setup.py --check`
   - If `REFRESH_FAILED invalid_grant`, re-auth is required (`--auth-url` then `--auth-code`).
2. Read a wide range from `Order NIM` (e.g. `A1:AZ3000` or larger as needed).
3. Normalize headers before matching:
   - trim spaces
   - lowercase
   - collapse repeated whitespace/newlines
4. Locate columns by semantic matching:
   - `SITE ID` column: header containing both `site` and `id`
   - `TANGGAL OA` column: header containing both `tanggal` and `oa`
5. Iterate data rows and count unique Site IDs where TANGGAL OA is non-empty.
6. Report final integer clearly.

## Robust Python snippet
```python
import json, re, subprocess
api='python /home/ubuntu/.hermes/profiles/profil-admin-node-b/skills/productivity/google-workspace/scripts/google_api.py'
sheet='1Lk86Lv_D2mFNgtAOyZWFEB4EL_0aTOf7-TR91n7aCqA'
out=subprocess.check_output(f"{api} sheets get {sheet} \"'Order NIM'!A1:AZ3000\"", shell=True, text=True)
rows=json.loads(out)

def norm(s):
    s=str(s).lower().strip()
    return re.sub(r'\s+', ' ', s)

header=[norm(h) for h in rows[0]]
site_i=next(i for i,h in enumerate(header) if 'site' in h and 'id' in h)
oa_i=next(i for i,h in enumerate(header) if 'tanggal' in h and 'oa' in h)

uniq=set()
for r in rows[1:]:
    sid=str(r[site_i]).strip() if site_i < len(r) else ''
    oa=str(r[oa_i]).strip() if oa_i < len(r) else ''
    if sid and oa:
        uniq.add(sid)

print(len(uniq))
```

## Pitfalls
- Header cells may include leading spaces (`" PROGRESS"`) or line breaks; exact string matches can fail.
- If range is too short (e.g., only first ~2000 rows), count may be outdated/too low.
- OAuth can be partially authenticated (limited scopes). Sheets-only operations still work if Drive+Sheets scopes are present.

## Operational routing rules (Site ID queries)
For this workspace, apply these defaults consistently:

1. If user sends **Site ID only** (e.g., `TBH236`) or asks general site status, query tab **`Order NIM`** first.
2. If user explicitly asks about **billing** (keyword: billing/tagihan/bw pada konteks billing), query tab **`Billing `** (note the trailing space in tab title).
3. After finishing a billing-specific lookup, revert default focus back to **`Order NIM`** for subsequent Site ID-only queries.

## Freshness / update policy
- `Order NIM` is operational field data and may change frequently.
- Treat **Wednesday 15:00 WIB** as the routine update checkpoint.
- When reporting data to stakeholders, include or be ready to provide a **"tanggal update terakhir"** marker for transparency.

## Performance pattern for high-frequency Site ID lookups
When many Site ID lookups are expected:
1. Build local index cache file (JSON) keyed by uppercase Site ID.
2. Use `Order NIM` column C as primary Site ID index; `Billing ` column B for billing index.
3. Store lightweight fields for fast reply (row number, site name, status/BW).
4. Refresh cache periodically (e.g., every 10–30 minutes) or after known sheet updates.
5. If lookup misses in cache, fallback to direct Sheets read then optionally repair cache.

## Output format
- `Site ID on air: <number>`
- Mention rule used: `SITE ID unik dengan TANGGAL OA terisi`.

### Default (Order NIM, non-detail request)
Return this concise field set only:
- `SOW`
- `SITEID`
- `SITE NAME`
- `NOMOR ORDER TSEL`
- `STATUS BILLING`
- `WITEL`
- `TSEL REG`
- `BW ORDER`
- `PLAN DEPLOYMENT`
- `PLAN TRANSPORT`
- `TANGGAL OA`
- `TANGGAL QC PASSED`
- `PROGRESS`

### Detail mode (when user asks lengkap/detail)
- Return full row context up to kolom `PROGRESS`.
- Preserve original sheet values; normalize only for display readability (e.g., trim extra spaces in header labels).

### Billing context
- For billing-specific Site ID requests, include `BW` from tab `Billing ` and state that source tab explicitly.

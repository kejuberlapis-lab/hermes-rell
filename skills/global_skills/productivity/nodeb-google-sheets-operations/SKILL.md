---
name: nodeb-google-sheets-operations
description: Standard operating workflow for Node B Telegram assistant when reading/updating Google Sheets (Order NIM, Billing, and BAUT tracking sheets), including default output format and safe update rules.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Node B Google Sheets Operations

Class-level workflow for handling Node B operational sheet requests from Telegram users with consistent defaults, strict safety, and predictable output.

## References
- `references/nodeb-field-mappings.md` — canonical field list, parsing examples, and write/skip policy.

## When to use

Use this skill when tasks involve:
- Site ID lookup in Node B sheets
- Billing lookups tied to Site ID
- Structured output from `Order NIM`
- Updating BAUT fields in external tracking sheets (e.g., `TRACKING BAUT SUMATERA`)

## Canonical data sources

1. **Primary**: Spreadsheet `1Lk86Lv_D2mFNgtAOyZWFEB4EL_0aTOf7-TR91n7aCqA`
   - Default tab for Site ID queries: `Order NIM`
   - Billing tab: `Billing ` (**note trailing space**)
2. Secondary source can be explicitly provided by user (e.g., `TRACKING BAUT SUMATERA`)

## Routing rules

1. If user sends only Site ID / generic site query → route to **Order NIM**.
2. If user asks billing-specific question (BW billing, billing status/context) → route to **Billing **.
3. After billing task, revert default lookup context to **Order NIM**.

## Billing tab retrieval pitfalls (important)

`Billing ` can contain decorative/pivot rows above the real header, so row 1 is not guaranteed to be field names. In observed layout, semantic header starts at row 3 (`No`, `Site ID`, `Site Name`, ...).

Practical retrieval pattern for Site ID checks:
1. Query a narrow range first (`'Billing '!B:B`) to locate `Site ID` quickly.
2. Avoid fetching full `'Billing '!A:AZ` unless needed; outputs are very large and may be truncated by tool output limits.
3. After locating the match, fetch only the target row span (or minimal column slice) for concise reporting.

## Default Order NIM output format

Unless user asks for full detail, return only:
- SOW
- SITEID
- SITE NAME
- NOMOR ORDER TSEL
- STATUS BILLING
- WITEL
- TSEL REG
- BW ORDER
- PLAN DEPLOYMENT
- PLAN TRANSPORT
- TANGGAL OA
- TANGGAL QC PASSED
- PROGRESS

If user requests detail, provide full row up to `PROGRESS`.

## BAUT update workflow (Newlink tab)

Target columns to fill:
- `Nomor BAUT`
- `TGL BAUT`
- `Status BAUT`
- `TGL Submit ke PM Tsel`

Rules:
1. Parse user line into components (Nomor BAUT, UNIQ/Site token, Status BAUT, Date).
2. Locate row by `UNIQ` (or exact agreed key) in target tab.
3. If row not found: **skip**, report "not found", do not force update.
4. Set `TGL Submit ke PM Tsel` = `TGL BAUT` when user requested this mapping.
5. `Status BAUT` must follow each incoming line (do not hardcode globally).

## Parsing pitfall (important)

For free-form lines like:
`Tel.674/... BTM388-2164/... sirkulir PD ENOM 17 Mei 2026`
- Do **not** assume token-1/token-2 split by whitespace is always correct.
- Prefer extracting `UNIQ` using pattern similar to `AAA999-...` and date from tail.
- Everything before UNIQ is `Nomor BAUT`; between UNIQ and date is `Status BAUT`.

## Safety and permission guardrails

- Do not perform edit/update without explicit user instruction.
- For unmatched IDs, no write side effects.
- Keep responses concise and operational.

## Operational reminder pattern

For recurring maintenance requests, create cron reminders (e.g., weekly Wednesday 15:00 WIB for Order NIM updates) and report job ID back to user.

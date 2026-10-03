---
name: nodeb-sheets-workflow
description: "Standard operating workflow for Node B Google Sheets tasks: default tab routing, output format, and safe update rules for Newlink BAUT fields."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Node B Sheets Workflow

Use this skill when handling Node B operational queries in Google Sheets, especially Site ID lookups and BAUT updates.

## Triggers

- User sends only a Site ID (e.g., `TBH236`)
- User asks billing-related checks by Site ID
- User asks to update BAUT fields in `Newlink`
- User provides compact BAUT line format mixing nomor + `SITEID-NIM` + status + date

## Routing Rules (Tab Selection)

1. **Default** for Site ID query (no billing context): use tab **`Order NIM`**.
2. If user explicitly asks billing context, use tab **`Billing `** (note trailing space in tab title).
3. After billing-specific tasks, revert default back to **`Order NIM`**.

## Default Output Format for `Order NIM`

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

If user asks detail, expand to full row up to PROGRESS.

## Newlink BAUT Update Rules (Strict)

Target sheet/tab: `TRACKING BAUT SUMATERA` → **`Newlink`**.

Update columns:
- `Nomor BAUT`
- `TGL BAUT`
- `Status BAUT`
- `TGL Submit ke PM Tsel`

Matching policy:
1. Parse `Site ID` and `NIM` from `SITEID-NIM` token.
2. Match row by **both** fields simultaneously:
   - `Actual Site ID` == Site ID
   - `NIM` == NIM
3. If both do not match on the same row: **SKIP** (do not force insert).

Date policy:
- `TGL Submit ke PM Tsel` must be set equal to `TGL BAUT` unless user says otherwise.

Status policy:
- `Status BAUT` is dynamic and must follow the exact status phrase provided by user for each line.

## Batch-Check First, Then Write

For multiple lines:
1. Run a pre-check and report `MATCH` / `SKIP_NO_MATCH` per line.
2. Only write updates for `MATCH` rows.
3. If permission is read-only (403), stop writes and report access requirement clearly.

## Pitfalls

- Tab name can be visually "Billing" but actual title is `Billing ` with trailing space.
- Site ID alone may exist, but must still require Site ID + NIM match for Newlink updates.
- Compact BAUT lines can be misparsed if using naive token positions; prefer pattern extraction around `SITEID-NIM` and trailing date.

## References

- `references/newlink-baut-line-format.md` — parsing patterns and examples for compact BAUT lines.

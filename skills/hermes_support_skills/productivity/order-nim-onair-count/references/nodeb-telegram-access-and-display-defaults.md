# Node B Telegram — Access & Display Defaults

## Scope
Operational defaults for Telegram-based Site ID lookup on Sheet `Order NIM` / `Billing `.

## Access policy (current)
- Primary owner / boss ID: `661471478`.
- Full operational access should be restricted to owner ID unless owner explicitly changes policy.
- For non-owner access requests, prefer **read-only** and require owner confirmation before broader enablement.

## Routing rules
1. Input is only Site ID (example: `TBH236`) → query tab `Order NIM` first.
2. Billing context explicitly requested (billing/tagihan/BW billing) → query tab `Billing ` (tab has trailing space).
3. After billing lookup, default focus returns to `Order NIM`.

## Default response fields for Order NIM
When user does NOT ask for full detail, return ONLY:
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

## Detail mode
- If user asks for "detail/lengkap", return data through full column set up to `PROGRESS`.

## Freshness reminder
- `Order NIM` routine update checkpoint: **Wednesday 15:00 WIB**.
- Include or provide "tanggal update terakhir" when communicating operational data to stakeholders.

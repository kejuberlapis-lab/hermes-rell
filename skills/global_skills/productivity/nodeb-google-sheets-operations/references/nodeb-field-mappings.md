# Node B Field Mappings & Examples

## Order NIM (default concise response fields)
Return these fields by default:
1. SOW
2. SITEID
3. SITE NAME
4. NOMOR ORDER TSEL
5. STATUS BILLING
6. WITEL
7. TSEL REG
8. BW ORDER
9. PLAN DEPLOYMENT
10. PLAN TRANSPORT
11. TANGGAL OA
12. TANGGAL QC PASSED
13. PROGRESS

## Billing tab naming caveat
Billing tab title in the primary sheet is `Billing ` (with trailing space). If range parsing fails for `Billing`, retry with exact title including trailing whitespace.

## BAUT update input pattern (free-form)
Example input:
`Tel.674/YN 140/JIFC-R1D0000/V/2026 BTM388-2164/TC.01/VS-01/III/2025 sirkulir PD ENOM 17 Mei 2026`

Recommended extraction:
- Nomor BAUT: `Tel.674/YN 140/JIFC-R1D0000/V/2026`
- UNIQ/key: `BTM388-2164/TC.01/VS-01/III/2025`
- Status BAUT: `sirkulir PD ENOM`
- TGL BAUT: `17 Mei 2026` (normalize as needed)
- TGL Submit ke PM Tsel: same as TGL BAUT (when user requested)

## Write policy
- If key is not found in target tab: do not write; report skipped.
- Status BAUT comes from each row's text; do not enforce a constant value unless requested.

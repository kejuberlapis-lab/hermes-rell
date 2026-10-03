# Newlink BAUT Line Format (Node B)

## Expected Compact Pattern

`<Nomor BAUT> <SITEID-NIM> <Status BAUT> <Tanggal Indonesia>`

Example:

`Tel.679/YN 140/JIFC-R1D0000/V/2026 PBR568-0259/TC.01/VS-01/II/2026 Sirkulir PD ENOM 17 Mei 2026`

## Extraction Rules

1. Find `SITEID-NIM` via regex-like token: `AAA999-...` (e.g., `PBR568-0259/...`).
2. `Site ID` = part before first `-` (e.g., `PBR568`).
3. `NIM` = part after first `-` (e.g., `0259/TC.01/VS-01/II/2026`).
4. `Nomor BAUT` = text before `SITEID-NIM` token.
5. `Tanggal` = trailing date phrase (e.g., `17 Mei 2026`).
6. `Status BAUT` = text between `SITEID-NIM` token and trailing date.

## Update Mapping

- `Nomor BAUT` ← extracted nomor
- `TGL BAUT` ← extracted date
- `Status BAUT` ← extracted status
- `TGL Submit ke PM Tsel` ← same as `TGL BAUT` (default user rule)

## Match Gate (Mandatory)

Only update row when BOTH are true in tab `Newlink`:

- `Actual Site ID` == extracted Site ID
- `NIM` == extracted NIM

If mismatch, return `SKIP_NO_MATCH` and do not write.

## Real Session Note

A case with `BTM388-2164/...` was skipped even though `BTM388` existed, because row NIM in sheet was different (`5009/...`). This validates the strict dual-key gate.

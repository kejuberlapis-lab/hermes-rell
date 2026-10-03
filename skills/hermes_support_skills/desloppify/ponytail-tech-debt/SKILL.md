---
name: ponytail-tech-debt
description: Use when auditing codebases. Audits tech debt ledgers.
---

# Ponytail Technical Debt & Anti-Overengineering Audit

Sistem audit repositori untuk membersihkan over-engineering, mengumpulkan komentar jalan pintas (TODO/FIXME/HACK), dan mengelola buku besar utang teknis (*tech debt ledger*).

## Prosedur Audit
1. **Harvesting Shortcut Comments:** Memindai seluruh codebase untuk mendeteksi marker `TODO`, `FIXME`, `HACK`, `WORKAROUND`, `XXX`.
2. **Over-Engineering Scan:** Mendeteksi boilerplate yang tidak perlu, lapisan abstraksi berlebih, dan ketergantungan paket yang membengkak.
3. **Tech Debt Ledger:** Menyusun laporan utang teknis terstruktur dengan tingkat keparahan (High/Med/Low) dan rencana pelunasan bertahap.

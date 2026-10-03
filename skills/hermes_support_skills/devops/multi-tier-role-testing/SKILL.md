---
name: multi-tier-role-testing
description: "Use when testing multi-role workflows sequentially."
version: 1.0.0
author: Hermes Agent
created_by: agent
---

# Multi-Tier Role Workflow & E2E Testing

## Kapan Dipakai
- Digunakan saat menguji aplikasi dengan hirarki multi-role (seperti HRIS, ERP, atau sistem approval bertingkat: Staf, Manager, Direktur, Super Admin).
- Ketika user menginstruksikan untuk memvalidasi alur pengajuan dan persetujuan bertahap tanpa membuat/mengacak data dummy baru.

## Aturan Utama
1. **Jangan Menambah Data Dummy Karyawan**: Jaga entitas tetap pada data yang sudah ada (locked entities).
2. **Pengujian Berurutan (Sequential Testing)**:
   - **Tahap 1 (Staf)**: Login staf -> Uji seluruh form pengajuan/action (Clock In/Out, Overtime, Leave, Reimbursement, Travel) -> Pastikan terisolasi hanya data sendiri.
   - **Tahap 2 (Manager)**: Login manager -> Cek antrean pending milik tim/bawahan -> Eksekusi approval tier-1 (Leave, Overtime, Reimbursement, Travel).
   - **Tahap 3 (Direktur)**: Login direktur -> Eksekusi approval tier-2/final (Travel) -> Verifikasi ringkasan agregat di Dashboard.
3. **Penanganan JWT Mapping**: Pastikan JWT payload `user_id` dan `emp_id` terpetakan secara benar tanpa bentrok antara tabel `users` dan `employees`.

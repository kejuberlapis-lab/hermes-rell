---
name: crypto-exchange-api-onboarding-and-safety
description: "Onboard exchange APIs (spot) for automation safely: key provisioning, signature verification, fallback decisions, and go-live gates for low-balance users."
version: 1.0.0
author: Hermes Agent
---

# Crypto Exchange API Onboarding and Safety

Gunakan skill ini saat user ingin setup API exchange untuk analisa market otomatis dan/atau auto-trading spot.

## Trigger
- "setup API exchange"
- "tes koneksi trading API"
- "pindah exchange"
- "hapus semua data exchange"
- "modal kecil ($10)"

## Prinsip Operasional
1. **Keamanan dulu**: jangan minta/menampilkan credential sensitif di chat.
2. **Mode ketat**: hanya eksekusi aksi saat user memberi instruksi eksplisit.
3. **Read-only dulu**: validasi akun/API sebelum izin transaksi live.
4. **Hapus jejak lama saat migrasi exchange** (env vars, key files, script lama).
5. **Untuk modal kecil, cek minimum order per pair**, bukan asumsi per-exchange.

## Playbook Step-by-step
1. Konfirmasi exchange target + mode (paper/live).
2. Instruksikan permission API minimum:
   - ✅ Read
   - ✅ Spot Trade (jika live diminta)
   - ❌ Withdraw
3. Jalankan test koneksi **read-only** dengan endpoint signed yang tepat.
4. Jika gagal signature/auth:
   - cek pasangan key (public/private) atau format signing,
   - cek passphrase (jika exchange memerlukan),
   - cek timestamp/recvWindow.
5. Jika user memutuskan pindah exchange:
   - hapus variabel env lama,
   - hapus file key lama,
   - verifikasi tidak ada sisa konfigurasi lama.
6. Setelah koneksi OK, baru lanjut cek market rules (min notional/qty) pair target.

## Pitfalls
- Endpoint `models/list` sukses (provider LLM) **tidak** membuktikan inferensi/chat sukses. Tetap uji endpoint chat.
- Public key saja tidak cukup untuk signed request; butuh private key pasangan yang benar.
- Error signature invalid biasanya mismatch key-pair atau mekanisme signing, bukan semata API key salah.
- User sering kirim credential di chat: wajib ingatkan rotate/revoke dan minimal aktifkan guardrail (no-withdraw, IP whitelist).

## Checklist Go-Live (Spot, modal kecil)
- [ ] Read-only test lulus
- [ ] Rule minimum order pair target tervalidasi
- [ ] Risk limit aktif (max loss harian, max posisi)
- [ ] Notifikasi transaksi/error aktif
- [ ] Permission withdraw NONAKTIF

## Referensi
- `references/openrouter-fallback-and-exchange-migration-notes.md`

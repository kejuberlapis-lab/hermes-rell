---
name: hermes-plugin-activation-and-validation
description: Prosedur class-level untuk memilih, mengaktifkan, dan memverifikasi plugin Hermes secara aman, terutama skenario tanpa API key.
version: 1.0.0
---

# Hermes Plugin Activation and Validation

## Kapan skill ini dipakai
- User meminta install/enable plugin Hermes.
- User ingin "install semuanya" tapi ada batasan keamanan/biaya/API key.
- User ingin plugin tertentu dipakai otomatis saat relevan.

## Prinsip kerja
1. **Jangan asal aktifkan semua plugin.** Pilih berdasarkan use-case user.
2. **Prioritaskan plugin tanpa API** bila user minta hemat/zero-key.
3. **Pisahkan status plugin vs dependency runtime**:
   - plugin bisa `enabled`
   - dependency Python bisa belum terpasang
4. **Verifikasi dengan uji nyata**, bukan hanya status enable.

## Langkah operasional standar
1. Muat konteks Hermes (skill `hermes-agent`) untuk command resmi.
2. Tampilkan inventaris plugin:
   - `hermes plugins list`
3. Jika user ambigu (contoh: "instal semuanya"), minta pilihan yang jelas:
   - semua tanpa API
   - semua termasuk berbayar/API
   - subset tertentu
4. Enable plugin target:
   - `hermes plugins enable <name>`
5. Pasang dependency yang diminta plugin (jika ada).
   - Untuk host PEP 668, **pakai venv proyek Hermes** (`./venv/bin/pip ...`) alih-alih pip global.
6. Verifikasi:
   - cek status plugin via `hermes plugins list`
   - lakukan smoke test kecil sesuai plugin.
7. Ingatkan user bahwa perubahan plugin biasanya efektif penuh setelah `/reset` atau restart gateway/service.

## Playbook khusus `web/ddgs` (tanpa API key)
1. Enable plugin:
   - `hermes plugins enable web/ddgs`
2. Install dependency `ddgs` di venv Hermes:
   - `./venv/bin/pip install ddgs`
3. Smoke test:
   - jalankan query singkat via Python dan pastikan hasil > 0.
4. Jika user bertanya "apa hasilnya", tampilkan ringkas: title + link teratas.

## Install skill komunitas (GitHub/tap) — pola aman
1. Tambah tap:
   - `hermes skills tap add <owner/repo>`
2. **Jangan asumsi skill langsung bisa dicari** (`skills search` bisa kosong walau tap berhasil).
3. Install dengan identifier penuh bila perlu:
   - `hermes skills install <owner/repo>/<path-skill>`
4. Untuk non-interaktif, gunakan `--yes` agar tidak berhenti di prompt konfirmasi.
5. Jika scanner memberi verdict **CAUTION/BLOCKED**:
   - default: **jangan force**
   - hanya pakai `--force` jika user memberi approval eksplisit + jelaskan risikonya.
6. Setelah terpasang, verifikasi via `skills_list`/`skill_view` dan lakukan audit cepat SKILL.md.

Lihat juga: `references/community-skill-install-safety.md`.

## Pitfalls
- **False sense of done**: plugin sudah enabled tapi dependency belum ada.
- **PEP 668**: install global `pip` gagal pada distro tertentu; jangan pakai `--break-system-packages` sebagai default.
- **Over-enabling**: mengaktifkan plugin massal tanpa kebutuhan meningkatkan risiko konfigurasi kacau.
- **Tap ≠ searchable skill**: beberapa repo berhasil ditambah sebagai tap tetapi tidak muncul di `skills search`; pakai install by full identifier.
- **Prompt blocking**: `hermes skills install` dapat berhenti di prompt `Confirm [y/N]`; gunakan `--yes` untuk otomatisasi.
- **Safety scan bypass risk**: `--force` hanya boleh setelah persetujuan user yang eksplisit.

## Preferensi pengguna (workflow)
- Jika user meminta tool tertentu (contoh `ddgs`), prioritaskan tool itu saat tugas memang membutuhkan pencarian web ringan.
- Tetap lakukan seleksi skill/plugin berbasis konteks; jangan auto-pakai semua plugin untuk tiap tugas.

## Output yang diharapkan ke user
- Status enable/disable yang jelas.
- Status dependency (terpasang/belum).
- Bukti verifikasi singkat (hasil smoke test).
- Next step (`/reset` atau restart) bila perlu.
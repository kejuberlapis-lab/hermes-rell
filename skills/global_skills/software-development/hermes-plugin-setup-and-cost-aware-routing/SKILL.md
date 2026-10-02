---
name: hermes-plugin-setup-and-cost-aware-routing
description: Konfigurasi plugin Hermes secara aman dan hemat biaya (tanpa API bila memungkinkan), plus routing model 3-tier (primary/secondary/tertiary) dengan fallback gratis.
version: 1.0.0
author: Hermes
license: MIT
---

# Hermes Plugin Setup & Cost-Aware Routing

## Kapan skill ini dipakai
Gunakan saat user meminta:
- Instal/aktifkan plugin Hermes (terutama yang minim API key)
- Setup agent agar hemat biaya dan tetap responsif saat kuota/saldo habis
- Rekomendasi model murah-berkualitas + fallback gratis

## Prinsip kerja
1. **Jangan asal aktifkan plugin**: sesuaikan dengan use-case user.
2. **Prioritaskan no-API / low-cost dulu** untuk start cepat.
3. **Pisahkan status plugin vs readiness runtime**:
   - `enabled` = plugin aktif secara konfigurasi
   - `ready` = dependensi/env sudah terpenuhi
4. **Selalu verifikasi** setelah instalasi (bukan asumsi sukses).

## Langkah operasional standar
1. Muat daftar plugin:
   - `hermes plugins list`
2. Aktifkan plugin target satu per satu:
   - `hermes plugins enable <name>`
3. Jika plugin butuh dependensi Python dan pip global gagal (PEP 668), **pasang di venv proyek Hermes**:
   - Gunakan `./venv/bin/pip install <package>` (atau `venv/bin/pip` jika itu yang ada)
4. Verifikasi fungsi plugin/dependensi dengan uji kecil yang deterministik.
5. Informasikan bahwa perubahan plugin berlaku di sesi baru (`/reset` atau restart gateway/service).

## Pola troubleshooting yang terbukti
### Kasus: `pip install --user` gagal karena externally-managed-environment (PEP 668)
- Jangan pakai `--break-system-packages` sebagai default.
- Gunakan virtualenv Hermes:
  - `./venv/bin/pip install ddgs`
- Verifikasi cepat:
  - import paket + query kecil (mis. DDGS max_results=3).

### Kasus: Setup Composio di server/headless (tanpa browser lokal)
- Gejala umum: CLI menampilkan error `xdg-open not found` saat `composio link ...`.
- Ini bukan kegagalan koneksi; hanya auto-open browser yang tidak tersedia.
- Alur stabil:
  1. Install CLI: `curl -fsSL https://composio.dev/install | bash`
  2. Login headless: `~/.composio/composio login --no-wait --no-skill-install`
  3. Kirim `login_url` ke user untuk dibuka manual.
  4. Finalisasi sesi via CLI key: `~/.composio/composio login --key <cli_key> --no-skill-install`
  5. Verifikasi: `~/.composio/composio whoami`
  6. Link app target headless: `~/.composio/composio link <toolkit> --no-wait`
  7. Jika muncul URL + error `xdg-open`, abaikan error tersebut dan minta user buka URL manual.
- Untuk X/Twitter, gunakan toolkit slug `twitter`.

## Routing model 3-tier (hemat + tahan gangguan)
- **Primary**: model murah-cepat untuk mayoritas tugas.
- **Secondary**: model murah alternatif saat primary gagal/lambat.
- **Tertiary (emergency)**: `openrouter/auto` sebagai jalur survival paling stabil (biarkan OpenRouter memilih endpoint yang tersedia saat itu).
- Gunakan model fixed hanya jika user minta deterministik spesifik. Untuk operasi harian, `openrouter/auto` umumnya lebih tahan terhadap endpoint model free yang naik-turun.

### Verifikasi OpenRouter yang benar (2 tahap)
> Jangan berhenti di `models` endpoint saja; wajib uji `chat/completions` juga.

1. **Connectivity test** (list model):
   - `GET /api/v1/models` dengan header Bearer key.
   - Lulus jika JSON valid dan ada `data[]`.
2. **Inference test** (real chat):
   - `POST /api/v1/chat/completions` dengan payload minimal.
   - Pakai model `openrouter/auto` untuk smoke test awal.
   - Lulus jika ada `choices[]` dan request tidak error.

### Pitfall penting saat uji chat
- Beberapa model free bisa mengembalikan `message.content = null` (mis. respons reasoning-only atau `finish_reason=length`).
- Saat parsing hasil, **jangan asumsi `content` selalu string**; tangani `null`/array dengan aman.
- Jika model fixed gagal dengan `No endpoints found`, ulangi tes dengan `openrouter/auto` sebelum menyimpulkan koneksi bermasalah.

## Komunikasi ke user (wajib jelas)
- Jelaskan bahwa biaya OpenRouter **bergantung model + token**.
- Sampaikan bahwa saldo habis tidak selalu “agent mati”, tapi panggilan model bisa gagal.
- Beri solusi: fallback provider/model, budget guardrail, dan monitoring.

## Kurasi repo komunitas sebelum install (wajib saat user minta "shortlist")
Lihat contoh ringkas & checklist metadata di `references/community-repo-shortlist-and-validation.md`.
Untuk flow instal skill komunitas yang sering kena scanner/prompt interaktif, lihat `references/community-skill-install-safety.md`.
Untuk setup Composio di environment headless + koneksi Twitter/X, lihat `references/composio-headless-login-and-twitter-link.md`.

1. **Jangan langsung install massal**. Mulai dari shortlist repo dulu.
2. Prioritaskan sumber dalam urutan ini:
   - Daftar resmi/dokumentasi Hermes (skills/tap)
   - Repo kurasi komunitas (contoh: awesome list)
   - Repo spesifik tool (MCP servers, plugin source)
3. Verifikasi sinyal kualitas minimum per repo:
   - update terbaru (`updated_at`),
   - adopsi komunitas (`stargazers_count`),
   - relevansi use-case user (no-API, low-cost, operasional).
4. Jika backend extract aktif adalah **ddgs (search-only)**, jangan paksa `web_extract` untuk URL:
   - gunakan endpoint metadata resmi (mis. GitHub REST API) untuk cek cepat,
   - atau arahkan user mengganti `web.extract_backend` ke penyedia yang mendukung extract.
5. Hasil akhir harus berupa **opsi bertahap**: pilih 1–2 repo → coba 1 use-case → validasi → lanjut.

### Instal skill komunitas dari tap/repo (pola aman yang terverifikasi)
1. **Tambahkan tap dulu**:
   - `hermes skills tap add <owner/repo>`
2. Jika `hermes skills search <query>` tidak menemukan skill, **jangan asumsi tap rusak**:
   - coba install dengan identifier penuh dari repo/community index:
   - `hermes skills install <owner/repo>/<path-skill>`
3. Untuk otomasi/non-interaktif, gunakan `--yes` agar tidak berhenti di prompt konfirmasi.
4. Jika scanner memberi `Decision: BLOCKED` karena `CAUTION`, default-nya **jangan lanjut**.
   - Lanjut `--force` hanya jika user memberi approval eksplisit.
   - Setelah force install, tandai skill sebagai "perlu audit manual" sebelum dipakai di task sensitif.
5. `hermes skills install` menerima **satu identifier per eksekusi**. Jangan kirim banyak identifier dalam satu command.

## Pitfalls
- Menganggap plugin `enabled` berarti langsung bisa dipakai tanpa dependensi/env.
- Memaksakan instalasi global Python di sistem yang menerapkan PEP 668.
- Memberi rekomendasi satu model untuk semua task tanpa routing.
- Langsung "instal semuanya" tanpa kurasi risiko, relevansi, dan readiness.

## Checklist selesai
- [ ] Plugin target enabled
- [ ] Dependensi terpasang di env yang benar
- [ ] Uji fungsi lulus
- [ ] User diberi instruksi `/reset`/restart
- [ ] Rencana 3-tier fallback dijelaskan
- [ ] (Jika topik komunitas) shortlist repo + validasi metadata + rencana instal bertahap

---
name: x-account-integration-and-automation-on-hermes
description: Setup dan troubleshooting integrasi akun X (Twitter) di Hermes dengan jalur Composio dulu, lalu fallback langsung ke OAuth 1.0a API untuk memastikan akses posting/interaksi benar-benar aktif.
---

# X account integration and automation on Hermes

## Kapan skill ini dipakai
- User ingin Hermes bisa posting dan interaksi di X menggunakan akun user.
- Flow Composio/OAuth UI bikin user mentok dan butuh jalur alternatif yang pasti jalan.
- Perlu verifikasi koneksi **berbasis bukti** (status API 200 + username terdeteksi), bukan asumsi.

## Prinsip inti
1. **Prioritaskan jalur resmi terstruktur**: Composio link `twitter`.
2. Jika user tetap mentok di UI auth, gunakan **fallback direct API OAuth 1.0a**.
3. Pisahkan status:
   - `AUTH_OK` (koneksi kredensial valid)
   - `ACTION_OK` (posting/engagement berhasil)
4. Setelah user memberi approval eksplisit untuk rangkaian setup, jalankan end-to-end tanpa minta konfirmasi kecil berulang.

## Langkah eksekusi
1. **Cek baseline tooling**
   - Pastikan binary Composio tersedia: `~/.composio/composio --help`
   - Jika perlu, install: `curl -fsSL https://composio.dev/install | bash`

2. **Login Composio (headless-friendly)**
   - Generate link: `composio login --no-wait --no-skill-install`
   - Setelah user selesai di browser, finalisasi deterministic:
     - `composio login --key <cli_key> --no-skill-install`
   - Verifikasi: `composio whoami` harus menampilkan akun/org.

3. **Link toolkit X di Composio**
   - `composio link twitter --no-wait` (ambil URL koneksi)
   - Setelah user authorize, cek:
     - `composio link twitter --list`
   - Sukses jika `total > 0`.

4. **Jika Composio tetap gagal, fallback ke direct X API (OAuth1.0a)**
   - Simpan kredensial ke file env profile terpisah (permission ketat 600), contoh:
     - `.env.x_api`
   - Verifikasi akun pakai endpoint:
     - `GET https://api.x.com/1.1/account/verify_credentials.json`
   - Sukses jika status 200 dan `screen_name` terbaca.

5. **Validasi operasi minimum**
   - Lakukan tes non-destruktif dulu (verify credentials).
   - Baru lanjut test post/engagement setelah user meminta eksplisit.

6. **Diagnosis cepat error posting (wajib dibedakan)**
   - Jika `POST /2/tweets` mengembalikan `403` + pesan `oauth1 app permissions`, artinya permission app belum `Read and write` atau access token belum diregenerate.
   - Tindakan: ubah permission di X Developer Portal ke `Read and write`, lalu **regenerate** `Access Token` + `Access Token Secret`, kemudian tes ulang.
   - Jika `POST /2/tweets` mengembalikan `402 CreditsDepleted`, auth sebenarnya sudah valid tetapi kuota/plan developer habis.
   - Jika fallback `v1.1 statuses/update` juga `404`, perlakukan sebagai keterbatasan plan/endpoint availability, bukan bug script lokal.
   - Setelah itu arahkan user ke opsi praktis: top-up/upgrade plan X atau pindah sementara ke platform lain untuk automasi konten.

## Pitfalls penting
- `composio login` bisa terlihat selesai di browser tapi sesi CLI belum terkunci; gunakan `--key` untuk finalisasi eksplisit.
- Di server headless, `xdg-open` bisa tidak ada; tetap pakai URL manual dari output `--no-wait`.
- Jangan menyimpulkan gagal auth hanya karena aksi lain terblokir (mis. guardrail/izin post).
- Hindari asumsi "connected" tanpa cek `link --list` / verify endpoint.

## Keamanan wajib
- Jangan tampilkan token/secret penuh di balasan.
- Jika user terlanjur kirim kredensial di chat, minta **rotate/revoke** setelah setup selesai.
- Simpan secret hanya di file env lokal profile dengan izin minimum (`chmod 600`).

## Referensi
- Lihat `references/composio-x-and-direct-oauth-fallback.md` untuk resep komando ringkas dan pola verifikasi.
# Composio headless login + Twitter link (Hermes)

## Kapan dipakai
- Hermes berjalan di server/headless (tanpa desktop GUI).
- `composio link` gagal auto-open browser (`xdg-open` tidak ada).

## Prosedur ringkas
1. Install Composio CLI:
   - `curl -fsSL https://composio.dev/install | bash`
2. Generate login URL + CLI key:
   - `~/.composio/composio login --no-wait --no-skill-install`
3. User buka `login_url` secara manual di browser.
4. Finalisasi login via key:
   - `~/.composio/composio login --key <cli_key> --no-skill-install`
5. Verifikasi identitas:
   - `~/.composio/composio whoami`
6. Hubungkan toolkit Twitter:
   - `~/.composio/composio link twitter --no-wait`
7. Jika keluar URL + error `xdg-open not found`, perlakukan sebagai expected di headless. Gunakan URL itu untuk auth manual.

## Pitfall yang perlu diingat
- `whoami` bisa kosong jika user hanya membuka URL tapi sesi CLI belum di-finalize dengan `--key`.
- Jangan menyimpulkan gagal hanya karena `xdg-open` error; cek dulu apakah URL auth sudah diberikan.
- Simpan komunikasi ke user: jelaskan langkah manual yang tersisa secara eksplisit (buka URL, authorize, konfirmasi selesai).

# Pola error: Exchange API OK, tapi bot tetap "authentication failed"

## Gejala
- Script read-only exchange sukses (contoh: Bybit connection OK).
- Gateway/cron bot trading tetap gagal auth saat menjawab chat atau saat job jalan.
- Log menunjukkan error auth provider model (mis. Codex access token missing), bukan error exchange.

## Akar masalah yang sering
Profile bot trading masih memakai provider/model default lama (atau fallback mengarah ke provider yang belum login), sehingga runtime LLM gagal sebelum logic trading dijalankan.

## Fix stabil (profile bot terpisah)
1. Ubah config profile bot:
   - `model.provider: openrouter`
   - `model.default: openrouter/auto`
   - `fallback_providers: ["openrouter"]`
2. Restart gateway dengan mode replace untuk menghindari instance lama tetap aktif.
3. Validasi dari Telegram dengan pesan teks biasa (bukan slash command).
4. Pantau log gateway + errors untuk memastikan tidak ada auth provider error berulang.

## Catatan verifikasi
- `/start` bisa tampil sebagai unknown command di beberapa setup Hermes gateway, jadi bukan indikator koneksi rusak.
- Health check yang lebih akurat: bot membalas pesan teks normal + cron jalan tanpa auth error provider.

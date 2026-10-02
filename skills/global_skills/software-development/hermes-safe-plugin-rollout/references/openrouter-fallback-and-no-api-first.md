# OpenRouter Fallback + No-API-First (Ringkas)

## Kapan dipakai
- User ingin setup Hermes bertahap, aman, dan hemat biaya.
- Prioritas awal: tool/plugin tanpa API.

## Pola implementasi yang terbukti
1. Aktifkan plugin no-API dulu (contoh: `web/ddgs`) untuk quick win.
2. Jika dependency Python gagal global karena PEP 668, pindah ke virtualenv agent/proyek.
3. Aktifkan provider fallback (OpenRouter) setelah secret tersimpan aman di `.env`.
4. Set fallback provider + default model budget (`openrouter/free` atau model murah lain).
5. Verifikasi lewat `hermes config check` dan `hermes config show`.

## Guardrail keamanan
- API key diperlakukan sensitif; jangan tampilkan penuh di chat/output.
- Jika key pernah terpapar di chat, rekomendasikan rotate/revoke.
- Untuk skill komunitas yang bisa write, tambahkan safety gate: read-only default, write butuh approval eksplisit.

## Catatan operasional
- Backend search tertentu bisa bersifat search-only; jangan asumsi bisa extract URL konten.
- Untuk validasi perintah CLI, gunakan subcommand resmi yang tersedia (hindari asumsi `get` jika tidak ada).

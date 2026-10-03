# OpenRouter Fallback Validation (Hermes)

Tujuan: memastikan fallback provider `openrouter` benar-benar bekerja saat provider utama gagal, bukan sekadar key terdeteksi.

## Checklist konfigurasi inti

1. Set fallback provider:
   - `fallback_providers: ["openrouter"]`
2. Set default model OpenRouter untuk jalur fallback yang stabil:
   - `providers.openrouter.default_model: "openrouter/auto"`
3. Verifikasi key ter-load (masked) via `hermes config check`.

## Pola uji konektivitas yang lebih stabil

Gunakan pola **curl -> simpan file -> parse JSON**. Hindari pipe langsung `curl | python` untuk mencegah error output/pipe yang flaky.

### Uji endpoint models
- Request: `GET /api/v1/models`
- Lulus jika:
  - JSON valid
  - field `data` berupa array non-kosong

### Uji endpoint chat/completions
- Request minimal ke `/api/v1/chat/completions`
- Gunakan model `openrouter/auto` untuk menghindari kegagalan model free tertentu yang unavailable sementara.

## Pitfall penting dari lapangan

1. **JSON parse gagal** sering bukan karena key invalid, tapi karena pola pipe output tidak stabil.
   - Solusi: simpan respons ke file dulu, parse terpisah.

2. **`message.content` bisa null** pada beberapa model/reasoning mode.
   - Jangan asumsi `content` selalu string.
   - Parser harus defensif: cek `content`, fallback ke field lain bila perlu.

3. **Model free spesifik bisa 404 endpoint unavailable** walau OpenRouter sehat.
   - Solusi: tes awal pakai `openrouter/auto`.

## Kriteria "siap operasional"

OpenRouter dianggap siap dipakai fallback bila semua benar:
1. `OPENROUTER_API_KEY` terbaca di config check
2. `GET /models` sukses dan mengembalikan daftar model
3. `POST /chat/completions` sukses minimal 1 respons valid
4. Fallback chain tetap menunjuk `openrouter`

## Catatan keamanan

- Jangan tampilkan secret utuh di chat/log.
- Jika key pernah terkirim di chat, sarankan rotate (keputusan final tetap di user).

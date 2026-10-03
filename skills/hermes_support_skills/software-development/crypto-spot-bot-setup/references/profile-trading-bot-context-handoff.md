# Trading Profile Context Handoff (Hermes)

Gunakan saat user bilang bot trading terpisah "tidak paham konteks" atau "tidak bisa akses exchange" padahal setup sudah pernah dibahas di chat utama.

## Tujuan
Membuat profile trading bot punya konteks operasional permanen, bukan hanya bergantung history chat profile utama.

## Langkah praktis
1. Simpan ringkasan konteks trading ke file profile trading (contoh: `TRADING_HANDOFF_CONTEXT.md`).
2. Patch `SOUL.md` profile trading agar eksplisit menunjuk:
   - file `.env` profile trading,
   - file guardrail trading,
   - script analisa dan eksekutor.
3. Tambahkan instruksi wajib: saat user minta cek koneksi exchange, bot harus jalankan probe private endpoint (mis. `fetch_balance`) sebelum menjawab.
4. Uji langsung dari profile trading dengan `hermes chat -q` untuk verifikasi bot benar-benar menggunakan konteks profile tersebut.

## Indikator sukses
- Bot trading menjawab status koneksi berdasarkan hasil probe aktual (bukan asumsi).
- Bot tidak lagi mengandalkan profile utama untuk keputusan trading.
- Guardrail tetap berlaku (analyze-only default, no live order tanpa instruksi eksplisit user).

## Pitfall
- Menganggap "clone profile" otomatis memindahkan seluruh konteks percakapan. Tidak selalu.
- Menyimpan konteks hanya di chat, tanpa jejak permanen di file profile trading.

# Telegram Gateway Recovery — VPS Primary Runner

Gunakan referensi ini saat Hermes Telegram menerima pesan tapi tidak membalas normal, atau log menunjukkan polling conflict antara lokal/WSL dan VPS.

## Pola gejala

- Log berulang:
  `Conflict: terminated by other getUpdates request; make sure that only one bot instance is running`
- Dua runner menggunakan token bot yang sama, misalnya lokal/WSL dan VPS-Zeus.
- Setelah conflict hilang, Telegram bisa inbound tapi agent error:
  `Auxiliary compression model ... has a context window of 8,192 tokens, below the minimum 64,000 required by Hermes Agent`.

## Recovery aman

1. Tentukan runner utama Telegram.
   - Untuk bot yang harus selalu hidup, prioritaskan VPS always-on.
2. Stop runner duplikat.
   - Jika VPS jadi utama, stop gateway lokal/WSL.
   - Jangan jalankan dua gateway polling dengan token sama.
3. **Disable gateway service** untuk mencegah auto-restart:
   ```bash
   systemctl --user disable hermes-gateway.service
   ```
   Tanpa `disable`, systemd bisa menghidupkan kembali gateway dalam hitungan menit (lingering, auto-restart on-failure, atau preset enable). Verifikasi dengan `systemctl --user is-enabled hermes-gateway.service` → harus `disabled`.
4. Di VPS/profile utama, cek proses dan status:
   - `hermes profile list`
   - `ps -ef | grep -E 'hermes.*gateway|gateway.*hermes|hermes_cli.*gateway' | grep -v grep`
   - `hermes --profile <profile> gateway status`
4. Cek log profile utama:
   - `~/.hermes/profiles/<profile>/logs/gateway.log`
   - Cari `Connected to Telegram`, `inbound message`, `response ready`, `Sending response`, dan error terbaru.
5. Jika auxiliary compression context error:
   - backup config profile: `config.yaml.bak_<timestamp>`.
   - update hanya `auxiliary.compression` ke model 64K+ context atau set `context_length` jika deteksi model salah.
   - jangan sentuh token/API key/provider secret.
6. Restart profile gateway:
   - `hermes --profile <profile> gateway restart`
7. Verifikasi:
   - log menunjukkan `Connected to Telegram (polling mode)`.
   - tidak ada conflict baru setelah restart window.
   - Bot API `sendMessage` boleh dipakai untuk chat yang eksplisit diinstruksikan/terlibat, dengan token dibaca dari env tanpa dicetak.
   - Jika user mengirim pesan, log harus menunjukkan inbound, `response ready`, lalu `Sending response`.
8. Catat ringkasan aman ke operational log lokal dan/atau profile VPS.

## Benign artifact: `NoneType updater` error

Saat gateway shutdown karena conflict, log bisa menunjukkan:

```
WARNING — Telegram polling retry 1/5 failed: 'NoneType' object has no attribute 'updater'
WARNING — Telegram polling conflict (2/5) — previous session still held open ...
Error: 'NoneType' object has no attribute 'updater'
```

**Interpretasi:** Ini BUKAN error serius. Ini terjadi karena ada retry polling tersisa yang mencoba akses `updater` setelah gateway sudah shutdown. Objek gateway sudah `None`, retry gagal, lalu gateway restart normal.

**Ciri-ciri harmless:**
- Muncul PERSIS setelah log `Shutdown phase` / `Gateway stopped`.
- Hanya 1-2 baris, tidak berulang.
- Diikuti log `Starting Hermes Gateway` + `Connected to Telegram` dalam beberapa detik.
- Setelah restart, tidak ada error serupa.

**Kapan curiga serius:** Jika error ini muncul tanpa log shutdown sebelumnya, atau berulang terus setelah restart, maka ada masalah lain (bukan artifact restart).

## Guardrail detail

- Jangan menampilkan token/password/API key.
- Password SSH dari user dipakai hanya untuk sesi itu; jangan simpan ke memory/log.
- Historical conflict lines di log tidak berarti masalah masih terjadi; cek timestamp setelah stop/restart.
- Jangan restart semua profile sekaligus; scope ke profile Telegram yang benar.

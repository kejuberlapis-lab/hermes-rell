---
name: yanshee-embodiment-bridge
description: "Use when deploying embodiment bridges on Yanshee robots."
---

# UBTECH Yanshee Embodiment Bridge

Prosedur operasional untuk menghubungkan robot humanoid UBTECH Yanshee (Raspberry Pi / Linux) ke Hermes AI Agent / Cloud LLM melalui pola *Outbound Hybrid Bridge*, Edge-TTS, dan kontrol motor servo fisik.

---

## 1. Arsitektur Komunikasi (Outbound Hybrid Bridge)

Karena robot fisik Yanshee berada di jaringan Wi-Fi lokal (private IP di balik NAT/firewall router), sedangkan otak AI berada di VPS Cloud:
* **Edge Client (Yanshee):** Menjalankan script Python (`yanshee_agent.py`) di Raspberry Pi internal. Melakukan *outbound polling* atau *WebSocket* ke VPS, memutar audio streaming, dan mengontrol servo gerak via `YanAPI` / REST API port 9090.
* **Cloud Server (VPS):** Menerima registrasi robot, menghasilkan audio Text-to-Speech (Edge-TTS `id-ID-ArdiNeural` / `id-ID-GadisNeural`), mengelola antrian tugas (*task queue*), dan mengoordinasikan respon percakapan.

```
+------------------------------------+          +-----------------------------------------+
|      UBTECH Yanshee Robot (Client) |          |        Hermes VPS Cloud (Brain)         |
|  - Raspberry Pi (Linux / Raspbian) |  ======> |  - FastAPI / Hermes Brain (Port 8088)   |
|  - Microsemi DSP Mic Array         |  (HTTP)  |  - Edge-TTS Generator (id-ID Neural)    |
|  - 17x Servos via YanAPI / REST    |  <====== |  - Motion & Speech Task Queue           |
|  - Speaker (mpg123 / ffplay)       | (Audio)  |  - Telegram / WhatsApp Remote Triggers  |
+------------------------------------+          +-----------------------------------------+
```

---

## 2. Prosedur Pemasangan Klien (One-Line Bootstrapper)

Jalankan perintah ini di dalam terminal Raspberry Pi Yanshee (via SSH atau terminal lokal):
```bash
curl -sL http://<SERVER_IP>:8088/static/yanshee_agent.py -o yanshee_agent.py && python3 yanshee_agent.py
```

### Alur Kerja Agent Klien (`yanshee_agent.py`):
1. **Pendaftaran (`POST /api/yanshee/register`):** Mengirimkan IP lokal, hostname, dan kapabilitas audio player ke VPS.
2. **Handshake Sapaan Otomatis:** Saat pertama kali terhubung, robot otomatis berdiri (`stand`), melambaikan tangan (`wave`), dan menyapa pemilik via speaker.
3. **Loop Polling (`GET /api/yanshee/poll`):** Mengambil instruksi suara (URL MP3) dan aksi gerakan yang siap dieksekusi setiap 1-2 detik.
4. **Laporan Status (`POST /api/yanshee/report`):** Mengonfirmasi status penyelesaian tugas ke server.

---

## 3. Konfigurasi Audio & Hardware DSP (Mikrofon & Speaker)

Hardware audio Yanshee menggunakan chip DSP **Microsemi DAC zl380xx** (`card 0: sndmicrosemidac`).

### Aturan Rekam & Playback Audio:
* **Wajib Stereo (`-c 2`):** Chip DSP Microsemi mic array menolak format mono (`-c 1`) dengan error `Channels count non available`.
* **Gunakan ALSA Plugin Converter (`plughw:0,0`):** Hindari direct raw `hw:0,0` agar rate dan konversi channel ditangani otomatis oleh ALSA.
* **Audio Playback:** Gunakan `mpg123`, `ffplay`, atau `cvlc` untuk pemutaran streaming MP3 tanpa lag.

**Perintah Rekam & Uji Audio:**
```bash
arecord -D plughw:0,0 -f S16_LE -r 16000 -c 2 -d 3 /tmp/mic_test.wav && aplay -D plughw:0,0 /tmp/mic_test.wav
```

---

## 4. Kontrol Gerakan Fisik (YanAPI & REST API)

1. **Python YanAPI SDK:**
   ```python
   import YanAPI
   YanAPI.yan_api_init('127.0.0.1')
   YanAPI.start_play_motion(name='wave') # atau 'bow', 'stand', 'walk_forward'
   ```
2. **Local REST API Fallback (Port 9090):**
   ```bash
   curl -X PUT "http://127.0.0.1:9090/v1/motions/play?name=wave"
   ```

---

## 5. Pitfalls & Rules

* **Private LAN IP Isolation:** Server cloud tidak boleh mencoba melakukan koneksi SSH inbound langsung ke IP privat `192.168.x.x`. Selalu gunakan pola *outbound polling* dari robot ke VPS atau pasang VPN mesh (Tailscale).
* **`play motion failed error code = 106 (This Motion set wrong direction!)`:** Terjadi jika parameter arah gerakan pada `YanAPI.sync_play_motion()` tidak valid. Gunakan nama gerakan dasar (`wave`, `bow`, `stand`, `nod`) tanpa parameter tambahan yang tidak terdokumentasi.
* **Low-Power Audio Output Distortion:** Jika suara robot pecah, pastikan volume ALSA di Raspberry Pi tidak melebihi 85% (`alsamixer` atau `amixer set Master 85%`).

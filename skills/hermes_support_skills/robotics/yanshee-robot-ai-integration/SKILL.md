---
name: yanshee-robot-ai-integration
description: "Use when connecting AI models to UBTECH Yanshee robots."
---

# UBTECH Yanshee AI Agent Integration

Panduan operasional dan prosedur teknis untuk menghubungkan robot humanoid UBTECH Yanshee (Raspberry Pi based) dengan model AI / Hermes Agent untuk komunikasi dua arah dan kontrol gerakan fisik.

---

## 1. Arsitektur Komunikasi

Yanshee beroperasi dengan arsitektur **Client-Server (Hybrid Edge-Cloud)**:
* **Edge / Yanshee (Body):** Menjalankan Linux Raspbian di Raspberry Pi internal, menangani penangkapan audio mikrofon, playback speaker, pembacaan sensor, dan motor servo via `YanAPI`.
* **Server / LLM (Brain):** Hermes Agent / LLM API (Groq, OpenAI, Gemini, dll.) memproses pemahaman bahasa, reasoning, dan mengembalikan teks respon beserta JSON aksi gerakan (*tool calling*).

---

## 2. Prosedur Setup & Konektivitas

### A. Deteksi IP & Akses SSH
1. **Deteksi IP:**
   * Tekan tombol dada (Chest Button) Yanshee 1-2 kali saat bot aktif untuk menyuarakan IP lokalnya (Voice Broadcast).
   * Atau gunakan hostname mDNS: `ping yanshee.local`.
2. **Koneksi SSH:**
   * User default: `pi`
   * Password default resmi: `raspberry` (bukan `yanapi` atau kosong).
   * Lakukan pergantian password segera via `passwd`.
3. **Catatan SSH Timeout:**
   * Jangan biarkan prompt password menganggur terlalu lama karena daemon SSH Yanshee akan otomatis memutus sesi (`Connection closed by host port 22`).

### B. Inisialisasi SDK YanAPI
Verifikasi instalasi Python 3 dan YanAPI di dalam Raspberry Pi Yanshee:
```python
import YanAPI
YanAPI.yan_api_init('127.0.0.1')
YanAPI.sync_do_tts('Halo sir, sistem Yanshee terhubung.')
```

---

## 3. Konfigurasi Audio & Hardware DSP (Mikrofon & Speaker)

Hardware audio Yanshee menggunakan chip DSP **Microsemi DAC zl380xx** (`card 0: sndmicrosemidac`).

### Aturan Rekam & Playback Audio:
* **Wajib Stereo (`-c 2`):** Chip DSP Microsemi mic array menolak format mono (`-c 1`) dengan error `Channels count non available`.
* **Gunakan ALSA Plugin Converter (`plughw:0,0`):** Hindari akses direct raw `hw:0,0` agar konversi format rate dan channel ditangani otomatis oleh ALSA.

**Perintah Rekam Uji Coba Audio:**
```bash
arecord -D plughw:0,0 -f S16_LE -r 16000 -c 2 -d 3 /tmp/mic_test.wav && aplay -D plughw:0,0 /tmp/mic_test.wav
```

---

## 4. Pipeline Komunikasi Dua Arah (Voice-to-Voice)

1. **Audio In (Hearing):**
   * Rekam buffer suara dari mic array (`plughw:0,0`, stereo 16kHz).
   * Konversi audio ke teks menggunakan Speech-to-Text (STT) berlatensi rendah (misal: Groq Whisper API / local Whisper).
2. **AI Reasoning (Brain):**
   * Kirim prompt teks ke endpoint LLM dengan persona Hermes Agent (Bahasa Indonesia, sapaan "sir", ringkas).
3. **Audio Out & Action (Speaking & Motion):**
   * Output teks disuarakan via `YanAPI.sync_do_tts(text)` atau Edge-TTS playback via `aplay`.
   * Jika respon memuat aksi fisik, panggil fungsi motion yang valid.

---

## 5. Pitfalls & Troubleshooting

* **`play motion failed error code = 106 (This Motion set wrong direction!)`:**
  * Terjadi jika parameter arah gerakan pada `YanAPI.sync_play_motion(name=..., direction=...)` tidak sesuai dengan kamus aksi bawaan. Validasi nama gerakan sebelum dieksekusi.
* **Network Isolation (Private LAN IP):**
  * IP `192.168.1.x` adalah jaringan lokal. Server cloud tidak bisa melakukan inbound connection secara langsung. Gunakan pola outbound client (Yanshee yang melakukan request HTTP/WebSocket ke server) atau gunakan VPN mesh seperti Tailscale untuk kontrol langsung.

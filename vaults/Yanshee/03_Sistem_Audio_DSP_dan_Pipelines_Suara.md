# 🎙️ 03. Sistem Audio DSP, Rekaman & Pipeline Suara 2 Arah

---

## 📌 1. Arsitektur Pipeline Suara 2 Arah (STT & TTS)
Interaksi suara pada Hermes Yanshee menggabungkan hardware audio DSP di kepala robot dengan cloud speech engine dan offline text-to-speech synthesizer.

```text
[Sir Bicara di Ruangan]
          │ (Gelombang Akustik)
          ▼
[Microphone Array di Kepala]
          │
[Microsemi DSP Codec (ZL380xx)]  <── Unmute via ALSA Control numid=2
          │ (Digital 48kHz Stereo S16_LE)
          ▼
[arecord -D plughw:0,0 /tmp/wake.wav]
          │ (Raw WAV Format)
          ▼
[FLAC Audio Encoder Utility]
          │ (Compressed Stream)
          ▼
[Google Speech Recognition API (id-ID)]
          │ (Teks Bahasa Indonesia)
          ▼
[Intent Engine / Wakeword Filter]
          │
      ┌───┴────────────────────────┐
      ▼ (Pertanyaan / Chat)        ▼ (Perintah Musik / Volume)
[Hermes LLM di 9Router VPS]   [Hardware Exec: mpg123 / amixer]
      │ (Jawaban Kalimat)
      ▼
[YanAPI.sync_do_tts() Synthesizer]
      │ (PCM Waveform)
      ▼
[Stereo Speaker Fisik Yanshee]
```

---

## ⚙️ 2. Konfigurasi Mixer Hardware ALSA (`amixer`)

Robot Yanshee memiliki 3 kontrol mixer hardware utama pada `card 0` (`snd_microsemi_dac`):

| Kontrol ALSA | Nama ID | Tipe | Nilai / Rentang | Konfigurasi Optimal | Fungsi & Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `numid=2` | `MIC SOUT MUTE` | Boolean | `on` / `off` | **`off`** | Sakelar Mute Mic hardware. Jika `on`, sinyal mic 0 (hening). |
| `numid=3` | `MIC SOUT GAIN` | Integer | `0` – `15` | **`15`** (Maksimal) | Penguatan sensitivitas gain mikrofon array. |
| `numid=1` | `DAC` (Master Vol) | Integer | `0` – `20` | **`14`** (70%) | Volume speaker fisik DAC. Naik/turun dengan step `4` (20%). |

### Perintah Konfigurasi Otomatis saat Startup:
```bash
amixer -c 0 cset numid=2 off    # Unmute mikrofon
amixer -c 0 cset numid=3 15     # Sensitivitas maksimal
amixer -c 0 sset DAC 14         # Default volume 70%
```

---

## 🗣️ 3. Speech-to-Text (STT) Engine & Dependensi FLAC
* **Library:** `SpeechRecognition` (Python 3)
* **Kebutuhan Sistem:** Paket binary `flac` (`/usr/bin/flac`) wajib terpasang di OS Raspbian. Tanpa binary ini, `SpeechRecognition` akan gagal mengirim data audio ke server STT dengan error `OSError: FLAC conversion utility not available`.
* **Bahasa:** `id-ID` (Bahasa Indonesia) dengan toleransi dialek santai.

---

## 🔊 4. Text-to-Speech (TTS) Synthesizer & Natural Pacing
Untuk menghasilkan suara yang ramah, jelas, dan tidak tergesa-gesa:
1. **YanAPI Offline TTS:** Menggunakan modul speech synthesis internal robot (`YanAPI.sync_do_tts`).
2. **Punctuation Formatting:** Kalimat yang dikembalikan oleh LLM diformat ulang secara dinamis:
   * Tanda titik (`. `) dan tanda seru (`! `) diganti dengan tanda koma (`, `).
   * Format ini memaksa mesin TTS memberikan jeda nafas pendek antar frasa sehingga intonasi terdengar rileks dan santun.
3. **Chime Sound Cue:** File audio `/opt/yanshee/lib/voice/audio/tips/ding.wav` diputar setiap kali giliran mikrofon siap mendengarkan sir.

# 🤖 Index Vault: Hermes AI Avatar — Robot Humanoid Yanshee

---

## 📌 1. Ringkasan Eksekutif & Filosofi Integrasi
Proyek **Hermes Yanshee** adalah manifestasi fisik (Hardware Avatar) dari **Hermes AI Agent** ke dalam robot humanoid **UBTECH Yanshee**.

Sesuai filosofi operasional utama Hermes:
> *"Lokal, VPS-Zeus, Telegram, dan Robot Yanshee adalah SATU: 1 Otak, 1 Proses, 1 Tempat Operasional."*

Robot Yanshee di ruangan fisik sir bukan merupakan entitas yang terpisah, melainkan bertindak sebagai tubuh fisik robotik cerdas yang terhubung langsung ke otak utama Hermes di VPS melalui jaringan mesh aman Tailscale dan gateway AI 9Router.

---

## 🧭 2. Peta Dokumen Vault Yanshee

| File | Topik / Lingkup Dokumentasi | Deskripsi Utama |
| :--- | :--- | :--- |
| **[[01_Arsitektur_Hardware_dan_Spesifikasi]]** | Hardware & Spesifikasi Robot | Detail Raspberry Pi 3B, 17 DOF Servo, Chip DSP Microsemi, Sensor, Baterai |
| **[[02_Infrastruktur_Jaringan_dan_Tailscale]]** | Jaringan Mesh & Keamanan SSH | Topologi Tailscale, IP 100.125.105.97, Port Routing, Autentikasi Ed25519 |
| **[[03_Sistem_Audio_DSP_dan_Pipelines_Suara]]** | Pipeline Suara 2 Arah (STT & TTS) | Chip ZL380xx DSP, ALSA `plughw:0,0`, Google STT FLAC, iFlytek TTS, Mixer DAC |
| **[[04_Integrasi_Otak_Hermes_dan_9Router_LLM]]** | Integrasi AI & Prompt Persona | Endpoint 9Router port 20128, Gemini Flash, Multi-turn Context Memory |
| **[[05_Sistem_Multimedia_dan_Music_Player]]** | Pemutar Musik & Streaming Hardware | Engine `mpg123`, Katalog Pop Indo & Barat, Kontrol Volume Hardware, Playback Guard |
| **[[06_Sistem_Kontrol_Fisik_dan_ROS_Bridge]]** | ROS Kinetic & Tombol Dada Hardware | Topic `/hal_button_info`, Push-to-Talk / Stop, YanAPI Motion & Servo Control |
| **[[07_SOP_Operasional_Maintenance_dan_Troubleshooting]]** | Standard Operating Procedure | Systemd services, log debugging, recovery command, maintenance runbook |
| **[[08_Artikulasi_Suara_Jelas_dan_Anti_Slop_Voice_Engine]]** | Standar Artikulasi Suara & Anti-Slop | Panduan pelafalan kata, intonasi lisan, sanitasi TTS, irama bicara natural |

---

## ⚡ 3. Identitas Perangkat & Quick Reference
* **Nama Perangkat:** Robot Humanoid Yanshee (UBTECH Edu)
* **OS:** Raspbian GNU/Linux 9.4 (Stretch) — Kernel 4.1.19-v7+ (ARMv7 32-bit)
* **IP Tailscale Yanshee:** `100.125.105.97`
* **IP Tailscale VPS Brain:** `100.114.89.30`
* **SSH Key Auth:** `~/.ssh/id_ed25519_yanshee` (User: `pi`)
* **Service Utama:** `hermes-yanshee.service` & `hermes-button.service`
* **Lokasi Script Utama:** `/home/pi/hermes_yanshee.py`
* **Direktori Musik:** `/home/pi/Music/`

---

## 🎯 4. Logika Alur Interaksi Fisik
```text
[Sir Bicara di Ruangan: "Halo Hermes"]
                   │
                   ▼
       [Mic DSP Microsemi ZL380xx] (48kHz Stereo)
                   │
                   ▼
         [Google STT Engine] (FLAC Transcoder)
                   │
                   ▼ (Teks Terdeteksi)
       [Robot Nyahut: "Ya, Sir?"] + [Bunyi Chime DING!]
                   │
                   ▼
[Sir Memberikan Perintah / Pertanyaan / Minta Lagu]
        ├── Pertanyaan / Diskusi ──► [9Router VPS LLM: Gemini Flash] ──► [TTS Yanshee Bersuara]
        ├── Putar Lagu ───────────► [Engine mpg123 Hardware DAC] ───► [Lagu Berputar di Speaker]
        └── Atur Volume / Kontrol ──► [ALSA Mixer DAC 4-/4+] ──────────► [Volume Berubah Instan]
```

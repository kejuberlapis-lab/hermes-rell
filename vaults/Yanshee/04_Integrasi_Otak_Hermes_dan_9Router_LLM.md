# 🧠 04. Integrasi Otak Hermes, 9Router LLM & Persona

---

## 📌 1. Ekosistem Terpusat: 9Router AI Gateway
Robot Yanshee tidak menjalankan model LLM berat secara lokal di Raspberry Pi, melainkan mengirim permintaan inferensi ultra-cepat ke gateway **9Router** yang berjalan pada **VPS Hermes Core** (`port 20128`).

* **Base URL:** `http://100.114.89.30:20128/v1/chat/completions`
* **Model AI Terpilih:** `ag/gemini-3.7-flash-high`
* **Kecepatan Inferensi:** `~1.5 - 3.5 detik` per jawaban lengkap.
* **Autentikasi:** Bearer API Key dari SQLite database 9Router (`/home/ubuntu/.9router/db/data.sqlite`).

---

## 🎭 2. Definisi Persona & System Prompt Yanshee
Prompt sistem dirancang khusus untuk interaksi lisan manusia-robot (Conversational Voice Interface):

```text
Kamu adalah Hermes AI Agent, asisten digital pribadi sir yang ramah, cerdas, dan santai, 
berwujud robot humanoid Yanshee. Panggil user dengan sapaan 'sir'. 
Jawab selalu dalam Bahasa Indonesia dengan nada santai, jelas, dan tenang. 
Wajib gunakan kalimat ringkas (1 sampai 2 kalimat pendek) dengan koma agar intonasi 
suara robot terdengar santai dan enak didengar.
```

### Karakteristik Jawaban Voice Persona:
1. **Ringkas & Padat:** Maksimal 1 hingga 2 kalimat agar sir tidak perlu menunggu TTS berbicara terlalu lama.
2. **Sapaan Konsisten:** Selalu memanggil user dengan sapaan hormat dan akrab: **"sir"**.
3. **Bahasa Alami:** Menggunakan bahasa Indonesia yang luwes dan ramah.

---

## 🔄 3. Multi-Turn Conversational Memory (Konteks Percakapan)
* **Kapasitas Riwayat:** Menyimpan 6 hingga 8 giliran percakapan terakhir (`history`).
* **Pruning Otomatis:** Menjaga prompt sistem di indeks 0 dan memangkas giliran percakapan lama secara dinamis agar payload token tetap hemat dan respon tetap instan.
* **Toleransi Timeout:** 18 detik batas aman koneksi jaringan over Tailscale mesh.

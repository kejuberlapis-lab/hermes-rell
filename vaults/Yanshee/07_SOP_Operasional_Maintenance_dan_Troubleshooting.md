# 📋 07. SOP Operasional, Maintenance & Troubleshooting

---

## 📌 1. Manajemen Service Systemd
Semua proses Hermes di robot Yanshee berjalan sebagai background service otomatis di bawah systemd:

| Nama Unit Service | Deskripsi Layanan | Status Auto-Start |
| :--- | :--- | :--- |
| **`hermes-yanshee.service`** | Engine Suara 2 Arah, Wakeword, AI 9Router & Music Player | `enabled` (Otomatis nyala saat boot) |
| **`hermes-button.service`** | Jembatan ROS Topik Tombol Dada (`/hal_button_info`) | `enabled` (Otomatis nyala saat boot) |

---

## 💻 2. Perintah Operasional Cepat (dari VPS atau Terminal)

### A. Cek Status Live Kedua Service:
```bash
ssh -i ~/.ssh/id_ed25519_yanshee pi@100.125.105.97 "systemctl status hermes-yanshee.service hermes-button.service"
```

### B. Monitor Log Suara & Percakapan Real-Time:
```bash
ssh -i ~/.ssh/id_ed25519_yanshee pi@100.125.105.97 "journalctl -u hermes-yanshee.service -f"
```

### C. Restart Service Suara:
```bash
ssh -i ~/.ssh/id_ed25519_yanshee pi@100.125.105.97 "sudo systemctl restart hermes-yanshee.service"
```

### D. Cek Level Volume & Sensitivitas Mic:
```bash
ssh -i ~/.ssh/id_ed25519_yanshee pi@100.125.105.97 "amixer -c 0 sget DAC; amixer -c 0 cget numid=2; amixer -c 0 cget numid=3"
```

---

## 🔧 3. Troubleshooting & Penanganan Kendala Umum

### 1. Robot Tidak Merespon Suara "Halo Hermes"
* **Penyebab:** Mic hardware mungkin terkunci (*muted*) oleh sistem ROS.
* **Solusi:** Jalankan perintah unmute paksa:
  ```bash
  ssh -i ~/.ssh/id_ed25519_yanshee pi@100.125.105.97 "amixer -c 0 cset numid=2 off; amixer -c 0 cset numid=3 15; sudo systemctl restart hermes-yanshee.service"
  ```

### 2. Robot Menjawab "Koneksi ke Otak Lambat"
* **Penyebab:** Koneksi internet di lokasi robot atau latensi Tailscale sedang tinggi.
* **Solusi:** Cek ping koneksi dari robot ke VPS:
  ```bash
  ssh -i ~/.ssh/id_ed25519_yanshee pi@100.125.105.97 "ping -c 4 100.114.89.30"
  ```

### 3. Musik Berhenti Mendadak saat Diputar
* **Penyebab:** Terjadi benturan ALSA jika proses perekam mic dibuka saat lagu aktif.
* **Solusi:** Pastikan service menggunakan script V9 / V9-MusicLib terbaru yang memisahkan channel rekaman saat status pemutaran lagu berlangsung.

---

## 🔋 4. Tips Pemeliharaan Daya & Baterai
* Jika baterai Yanshee berada di bawah 15%, LED dada robot akan berkedip merah.
* Selalu gunakan adaptor charger 9.5V bawaan UBTECH saat sesi interaksi panjang.

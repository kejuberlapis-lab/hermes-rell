# 🌐 02. Infrastruktur Jaringan, VPN Tailscale & Keamanan SSH

---

## 📌 1. Topologi Jaringan Mesh Terdistribusi
Untuk mewujudkan konsep **"1 Otak, 1 Proses, 1 Ekosistem Tersinkronisasi"**, Robot Yanshee tidak menggunakan port-forwarding publik yang rentan, melainkan dihubungkan langsung ke **VPS-Zeus** melalui jaringan mesh **Tailscale WireGuard Zero-Trust Network**.

```text
[VPS-Zeus Hermes Core] (Tailscale IP: 100.114.89.30)
         │  Port 20128: 9Router OpenAI-Compatible API
         │  Port 22: Dedicated SSH Control
         │
    WireGuard Mesh Tunnel (Encrypted Tailscale Network)
         │
         ▼
[Robot Yanshee Physical Avatar] (Tailscale IP: 100.125.105.97)
         │  User: pi
         │  Auth: SSH Ed25519 Key (~/.ssh/id_ed25519_yanshee)
         │  Port 9099: Local Voice Webhook
         │  Port 11311: ROS Core Master
```

---

## 🔑 2. Konfigurasi Autentikasi SSH Key
Akses dari VPS Hermes ke robot Yanshee diamankan dengan pasangan kunci kriptografi **Ed25519**:

* **Private Key di VPS:** `/home/ubuntu/.ssh/id_ed25519_yanshee`
* **Public Key di Yanshee:** Terdaftar pada `/home/pi/.ssh/authorized_keys`
* **Perintah Akses Cepat:**
  ```bash
  ssh -i ~/.ssh/id_ed25519_yanshee pi@100.125.105.97
  ```
* **Konfigurasi SSH Client (`~/.ssh/config`):**
  ```sshconfig
  Host yanshee
      HostName 100.125.105.97
      User pi
      IdentityFile ~/.ssh/id_ed25519_yanshee
      StrictHostKeyChecking no
      ServerAliveInterval 30
      ServerAliveCountMax 3
  ```

---

## 🛡️ 3. Port Binding & Service Network Map

| Port | Protokol | Layanan / Endpoint | Arah Komunikasi | Fungsi Utama |
| :--- | :--- | :--- | :--- | :--- |
| **20128** | HTTP | `http://100.114.89.30:20128/v1/chat/completions` | Outbound (Yanshee $\rightarrow$ VPS) | Permintaan LLM ke gateway 9Router VPS |
| **9099** | HTTP | `http://127.0.0.1:9099` | Localhost (Internal Yanshee) | Webhook audio & event dispatcher |
| **11311** | TCP/XML-RPC | `http://localhost:11311` | Localhost (Internal Yanshee) | ROS Master Kinetic Core |
| **22** | SSH | Port 22 (Tailscale 100.125.105.97) | Inbound (VPS $\rightarrow$ Yanshee) | Remote management, deploy script, monitoring |
| **41641** | UDP | WireGuard Tailscale Encrypted Daemon | In/Out Peer-to-Peer | Tunneling zero-latency enkripsi |

---

## 🚀 4. Uji Latensi & Keandalan Koneksi
Jaringan Tailscale menghubungkan Raspberry Pi robot langsung ke server VPS dengan latensi rata-rata:
* **Ping Latency (VPS $\leftrightarrow$ Yanshee):** `~30 - 45 ms` (Sangat ideal untuk streaming audio dan instruksi real-time).
* **Throughput:** `~15 - 25 Mbps` (Mendukung transfer file audio, stream video kamera, dan payload teks).

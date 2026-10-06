# 🛠️ 01. Arsitektur Hardware & Spesifikasi Robot Yanshee

---

## 📌 1. Ikhtisar Hardware UBTECH Yanshee
Robot Yanshee adalah platform robot humanoid edukasi canggih dengan tinggi sekitar 37 cm dan berat 2.1 kg, ditenagai oleh single-board computer Raspberry Pi 3B yang terintegrasi dengan motherboard STM32 controller dan serangkaian sensor cerdas.

```text
+-------------------------------------------------------------------+
|                        KEPALA ROBOT                               |
|   - 8MP HD Camera                                                 |
|   - Dual MEMS Microphone Array                                    |
|   - Microsemi ZL380xx DSP Audio Processor                         |
|   - LED Expressive Eyes (RGB Matrix)                              |
+---------------------------------+---------------------------------+
                                  |
+---------------------------------v---------------------------------+
|                        DADA & BADAN UTAMA                         |
|   - Raspberry Pi 3 Model B (Quad Core ARM Cortex-A53 1.2GHz, 1GB) |
|   - STM32 Secondary Motion Controller MCU                         |
|   - Power / Multi-function Chest Center Button                    |
|   - High-Fidelity Stereo Loudspeaker (Dual Channel)               |
|   - Li-ion Battery Pack 7.4V 3000mAh                              |
+---------------------------------+---------------------------------+
                                  | (RS485/UART Bus)
+---------------------------------v---------------------------------+
|                        ANGGOTA GERAK (17 DOF)                     |
|   - Leher: 1 Servo (Yaw)                                          |
|   - Lengan Kiri & Kanan: Masing-masing 3 Servo (Bahu, Lengan, Siku)|
|   - Tangan Kiri & Kanan: Masing-masing 1 Servo (Gripper/Jari)     |
|   - Kaki Kiri & Kanan: Masing-masing 4 Servo (Panggul, Paha, Lutut, Telapak) |
|   - Total: 17 High-Precision Digital Coreless Servos              |
+-------------------------------------------------------------------+
```

---

## 📋 2. Spesifikasi Teknis Lengkap

| Komponen | Spesifikasi Teknis | Keterangan & Catatan Sistem |
| :--- | :--- | :--- |
| **Main Processing Unit** | Broadcom BCM2837, Quad Core Cortex-A53 @ 1.2 GHz | Raspberry Pi 3 Model B |
| **RAM** | 1GB LPDDR2 | RAM sistem untuk Linux Raspbian |
| **Storage** | 16GB / 32GB MicroSD Card | Root filesystem `/` |
| **Sub-Controller MCU** | STM32F4xx ARM Cortex-M4 | Khusus manajemen bus servo 1Mbps & low-level sensor |
| **Sistem Operasi** | Raspbian GNU/Linux 9.4 (Stretch) | Kernel: `4.1.19-v7+` (armv7l 32-bit) |
| **Kamera** | 8 Megapixel Fixed Focus | Terhubung via interface CSI |
| **Audio DSP** | Microsemi Timberwolf ZL380xx Hardware Codec | Dedicated Acoustic Echo Cancellation (AEC) & Beamforming |
| **Speaker** | 2x 2.5W Stereo Speaker | Terhubung ke DAC amplifier internal |
| **Mikrofon** | Dual Far-field Microphone Array | Terletak di mahkota kepala robot |
| **Servomotor** | 17x UBTECH Digital Bus Servo | Torsi 12kg.cm, resolusi 360-derajat magnetik feedback |
| **Konektivitas** | Wi-Fi 802.11 b/g/n (2.4GHz), Bluetooth 4.1 LE | Terhubung ke LAN & Tailscale Mesh |
| **Port Eksternal** | USB 2.0 (x2), Micro USB Debug, DC Jack 9.5V, GPIO Header | Ekspansi sensor & debugging |
| **Baterai** | 7.4V 3000mAh Rechargeable Lithium-ion | Daya tahan standby ~2-3 jam, gerak ~1 jam |

---

## ⚡ 3. Karakteristik Komponen Audio & Bus Servo

### A. Chip DSP Audio Microsemi ZL380xx
Chip Microsemi mengelola konversi ADC mikrofon dan DAC amplifier stereo speaker. 
* **Nama Perangkat ALSA:** `snd_microsemi_dac` (`card 0, device 0`)
* **Format Native Rekaman:** 48.000 Hz, 16-bit Signed Little Endian (`S16_LE`), Stereo (2 Channel).
* **Hardware Mute Switch:** Kontrol nomor 2 (`numid=2`). Harus selalu dalam posisi `off` agar mikrofon menangkap gelombang suara.
* **Volume DAC:** Kontrol nomor 1 (`DAC`), skala integer `0` sampai `20` (Level ideal: `14` / 70%).

### B. Bus Servo 17 Derajat Kebebasan (DOF)
Semua 17 servo terhubung dalam satu jalur UART serial kecepatan tinggi (1 Mbps). Sub-controller STM32 bertindak sebagai master bus yang mengirim perintah sudut, kecepatan, dan membaca telemetri suhu/arus setiap servo.

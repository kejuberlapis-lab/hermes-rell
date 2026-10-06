# 🕹️ 06. Sistem Kontrol Fisik, ROS Bridge & Tombol Dada

---

## 📌 1. Ekosistem ROS Kinetic & Interaksi Hardware
Robot Yanshee menggunakan framework **Robot Operating System (ROS Kinetic Kame)** untuk menjembatani komunikasi antar driver hardware tingkat rendah (HAL), sensor, mikrofon, dan motor servo.

* **ROS Master URI:** `http://localhost:11311`
* **Node Utama:**
  * `/hal`: Mengontrol aktuator servo, tombol dada, sensor gyro, dan LED.
  * `/voice`: Mengelola subsystem MSC iFlytek.
  * `/sysconfig`: Manajemen konfigurasi sistem dan baterai.

---

## 🔘 2. Tombol Dada Hardware (*Push-to-Talk / Push-to-Stop*)
Tombol fisik di tengah dada Yanshee terhubung ke interrupt GPIO yang dipublikasikan oleh ROS pada topik:

* **Topik ROS:** `/hal_button_info` (Message Type: `std_msgs/Int32`)
* **Kode Event Tombol:**
  * `1` = Single Click (Tekan 1x)
  * `2` = Double Click (Tekan 2x)
  * `3` = Long Press (Tekan Tahan)

### Jembatan Tombol (`hermes-button.service`):
Script `/home/pi/button_listener.py` berjalan secara independen di background untuk memantau topik ROS tersebut:
```python
def button_callback(data):
    with open('/tmp/button_pressed.flag', 'w') as f:
        f.write(str(data.data))
```
Ketika sir menekan tombol dada:
1. File penanda `/tmp/button_pressed.flag` dibuat secara instan.
2. Engine suara `hermes_yanshee.py` membaca penanda tersebut dan langsung:
   * Menghentikan musik yang sedang berjalan seketika.
   * Mengaktifkan mode mendengarkan mikrofon dengan bunyi *"DING!"*.

---

## 🦾 3. Kontrol Gerak & Servo via YanAPI
Selain suara, Hermes dapat menggerakkan tubuh Yanshee menggunakan API gerak bawaan:
* `YanAPI.start_play_motion(name='wave')`: Melambaikan tangan.
* `YanAPI.start_play_motion(name='bow')`: Membungkuk memberi hormat.
* `YanAPI.set_servos_angles(angles_dict)`: Mengatur sudut spesifik 17 servo.

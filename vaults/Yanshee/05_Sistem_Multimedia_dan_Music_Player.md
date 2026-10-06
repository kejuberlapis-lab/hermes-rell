# 🎵 05. Sistem Multimedia, Pemutar Musik & Audio Conflict Guard

---

## 📌 1. Arsitektur Pemutar Musik Hardware
Robot Yanshee dilengkapi kemampuan memutar file audio MP3 berkualitas tinggi secara lokal serta radio streaming online menggunakan engine **`mpg123`** yang dialihkan langsung ke amplifier DAC hardware (`plughw:0,0`).

```text
[Sir: "Putar lagu Peterpan" / "Putar lagu Coldplay"]
                     │
                     ▼
      [Intent Matching Song Catalog]
                     │
      ┌──────────────┴──────────────┐
      ▼ (Lokal Terdaftar)           ▼ (Online Stream)
[File MP3 di /home/pi/Music/]  [Zeno.fm Top Pop Stream]
      │                             │
      └──────────────┬──────────────┘
                     ▼
  [mpg123 -a plughw:0,0 -q <target>] ──► [Speaker Fisik Stereo]
```

---

## 📂 2. Katalog Lagu Lokal (`/home/pi/Music/`)

| Kata Kunci Trigger | Judul Lagu & Artis | File Audio Lokal | Ukuran |
| :--- | :--- | :--- | :--- |
| `peterpan`, `noah`, `jejak` | **Peterpan — Menghapus Jejakmu** | `peterpan_menghapus_jejakmu.mp3` | 4.3 MB |
| `mungkin nanti` | **Peterpan — Mungkin Nanti** | `peterpan_mungkin_nanti.mp3` | 4.2 MB |
| `sheeran`, `thinking`, `ed` | **Ed Sheeran — Thinking Out Loud** | `ed_sheeran.mp3` | 5.7 MB |
| `coldplay`, `viva` | **Coldplay — Viva La Vida** | `coldplay.mp3` | 7.5 MB |
| `john legend`, `all of me` | **John Legend — All of Me** | `john_legend_all_of_me.mp3` | 4.7 MB |
| `justin`, `bieber` | **DJ Snake ft. Justin Bieber — Let Me Love You** | `justin_bieber.mp3` | 3.2 MB |
| `jason mraz`, `mraz` | **Jason Mraz — I Won't Give Up** | `jason_mraz.mp3` | 5.6 MB |
| `maroon`, `adam` | **Maroon 5 / Adam Levine — Stereo Hearts** | `adam_levine_maroon5.mp3` | 4.2 MB |
| `radio`, genre umum | **Top Hits Pop Radio Stream** | `https://stream.zeno.fm/f3wvbbqmdg8uv` | Live Stream |

---

## 🛡️ 3. Audio Conflict Guard & ALSA Buffer Safety
Pada hardware chip Microsemi ZL380xx:
1. **Pemisahan Jalur Suara & Musik:** Saat robot berbicara (TTS), proses musik dihentikan terlebih dahulu (`stop_music()`) agar tidak terjadi tabrakan frekuensi suara di hardware DAC.
2. **Kestabilan Parameter `mpg123`:** Jangan menggunakan parameter skala `-f` pada build ARMv7 32-bit di Raspbian Stretch untuk mencegah *Segmentation Fault*. Pengaturan volume dilakukan secara murni melalui ALSA DAC mixer (`amixer DAC 4-/4+`).
3. **Konfirmasi Judul:** Setiap pemutaran lagu diawali dengan notifikasi lisan: *"Memutarkan lagu [Judul] untuk sir."*

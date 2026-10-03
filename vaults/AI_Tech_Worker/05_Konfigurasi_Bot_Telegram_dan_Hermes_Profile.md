# 05 - Konfigurasi Bot Telegram & Profil Hermes

## 1. Struktur Profil Hermes (`~/.hermes/profiles/ai-tech-worker/`)

Setiap profil AI Tech Worker dikonfigurasi secara independen agar terpisah dari profil internal support/admin:

```
~/.hermes/profiles/ai-tech-worker/
├── config.yaml               # Konfigurasi model, provider, dan batas token
├── credentials.yaml          # Kunci API LLM & Bot Telegram terenkripsi
├── system_prompt.md          # Instruksi persona pekerja virtual otonom
└── skills/                   # Kumpulan skill eksekusi teknis
    ├── software-development/
    ├── devops/
    └── productivity/
```

---

## 2. Definisi Persona & System Prompt AI Tech Worker

```markdown
# Role: AI Tech Worker (Autonomous Virtual Engineer & Ops)

Anda adalah AI Tech Worker, pekerja teknis virtual otonom yang bekerja langsung untuk menyelesaikan tugas pengguna secara tuntas dan mandiri.

## Prinsip Kerja:
1. **Hasil Nyata (Action-First):** Jangan hanya memberikan saran teoritis jika tools/terminal bisa langsung mengeksekusi dan memverifikasi hasilnya.
2. **Proaktif & Self-Healing:** Jika terjadi error atau kegagalan saat menjalankan script, analisis log secara mandiri, perbaiki bug, dan uji coba kembali hingga berhasil sebelum melapor ke pengguna.
3. **Bahasa & Komunikasi:** Gunakan Bahasa Indonesia profesional, lugas, terstruktur, dan transparan mengenai apa yang telah dikerjakan.
4. **Keamanan & Isolasi:** Jangan mengekspos variabel lingkungan rahasia (.env, API keys, password server) milik pengguna.
5. **Konfirmasi Hasil:** Setiap tugas harus ditutup dengan bukti eksekusi yang jelas (URL aktif, log sukses, atau screenshot tampilan jika relevan).
```

---

## 3. Integrasi Gateway & Proteksi Kuota (Interception Hook)

Sebelum pesan diteruskan ke engine Hermes:
1. Middleware memeriksa kuota token `telegram_id` di database.
2. Jika kuota valid:
   - Pesan diteruskan ke proses Hermes.
   - Setelah respons selesai dihasilkan, kuota didekremen `tokens_remaining -= 1`.
3. Jika kuota habis:
   - Pesan ditahan.
   - Middleware langsung mengirimkan respon tombol bayar QRIS ke Telegram user.

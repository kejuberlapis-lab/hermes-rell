# Community Skill Install Safety (Hermes)

Ringkasan pola dari sesi real-world saat memasang skill komunitas.

## Temuan operasional
- `hermes skills tap add <owner/repo>` bisa sukses, tetapi `hermes skills search <query>` tetap tidak menemukan skill.
- Solusi praktis: install pakai identifier penuh (`owner/repo/path-skill`) dari index komunitas.
- `hermes skills install` hanya menerima satu identifier per command.
- Installer bersifat interaktif; gunakan `--yes` untuk automation/headless run.
- Skill komunitas dapat diblok scanner (`Decision: BLOCKED`, verdict `CAUTION`).
  - Lanjut `--force` hanya dengan approval eksplisit user.

## Command pattern yang direkomendasikan
```bash
# 1) Tambah sumber
hermes skills tap add <owner/repo>

# 2) Install satu skill secara eksplisit (non-interaktif)
hermes skills install --yes <owner/repo>/<path-skill>

# 3) Hanya jika user approve override scanner
hermes skills install --yes --force <owner/repo>/<path-skill>
```

## Guardrail
- Jangan force install default.
- Setelah force install, labelkan sebagai "audit manual required" sebelum dipakai pada tugas sensitif (write/delete/credential-flow).
- Hindari instal borongan; lakukan batch kecil + verifikasi tiap skill.

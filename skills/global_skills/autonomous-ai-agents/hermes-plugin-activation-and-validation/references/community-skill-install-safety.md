# Community Skill Install Safety Notes

## Ringkasan pola yang terbukti
- `hermes skills tap add <owner/repo>` bisa sukses, tetapi skill belum tentu muncul di `hermes skills search`.
- Untuk kompatibilitas maksimum, gunakan identifier penuh saat install:
  - `hermes skills install <owner/repo>/<skill-or-path>`
- Tambahkan `--yes` untuk menghindari prompt interaktif `Confirm [y/N]`.

## Alur aman yang direkomendasikan
1. Tambah tap.
2. Coba `skills search` seperlunya.
3. Jika tidak ketemu, install dengan full identifier.
4. Perhatikan hasil security scan:
   - SAFE/ALLOWED: lanjut.
   - CAUTION/BLOCKED: minta approval user sebelum `--force`.
5. Setelah install: cek skill muncul (`skills_list`) lalu audit cepat isi `SKILL.md` sebelum dipakai.

## Command snippets
```bash
hermes skills tap add <owner/repo>
hermes skills install --yes <owner/repo>/<skill>
hermes skills install --yes --force <owner/repo>/<skill>   # hanya dengan approval user
```

## Guardrail komunikasi ke user
- Jelaskan perbedaan: "terpasang" vs "aman dipakai otomatis".
- Labelkan hasil audit:
  - Aman dipakai
  - Aman terbatas (perlu approval per aksi write/change)
  - Jangan dipakai

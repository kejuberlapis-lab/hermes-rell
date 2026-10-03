---
name: generate-word-docx-on-ubuntu-hermes
description: Membuat file .docx (Word) secara otomatis di environment Hermes Ubuntu saat modul python-docx tidak tersedia di interpreter default.
version: 1.0.0
author: Hermes
---

# generate-word-docx-on-ubuntu-hermes

## Kapan dipakai
Gunakan saat user minta output dokumen Word (.docx) dan environment Hermes gagal import `docx` pada `python` default.

## Gejala umum
- `ModuleNotFoundError: No module named 'docx'`
- `pip install python-docx` gagal dengan pesan `externally-managed-environment` (PEP 668)
- `execute_code` tidak melihat paket yang baru diinstall via apt

## Pendekatan yang terbukti
1. **Cek dulu interpreter yang aktif**
   - `python -V`
   - `which python`
2. **Jika pip diblokir PEP 668, jangan paksa --break-system-packages** untuk workflow standar.
3. **Install paket Debian**
   - `apt-get update -qq && apt-get install -y -qq python3-docx`
4. **Verifikasi pada system Python**
   - `/usr/bin/python3 -c "import docx; print(docx.__version__)"`
5. **Generate dokumen dengan `/usr/bin/python3` (bukan `python`/`execute_code`)**
   - Jalankan script python-docx via terminal heredoc memakai `/usr/bin/python3`.
6. **Simpan file ke path absolut** (contoh `/root/NAMA_FILE.docx`) dan kirim ke user sebagai media path.

## Template command
```bash
/usr/bin/python3 - << 'PY'
from docx import Document

doc = Document()
doc.add_heading('Judul Dokumen', 0)
doc.add_paragraph('Isi dokumen...')
out='/root/output.docx'
doc.save(out)
print(out)
PY
```

## Pitfalls
- `execute_code` bisa memakai interpreter sandbox/venv berbeda yang tidak membaca paket dari apt.
- `python` symlink dapat berbeda dari `/usr/bin/python3`.
- Hindari `pip install` system-wide di Ubuntu modern kecuali benar-benar diperlukan.

## Verifikasi akhir
- Pastikan command mengembalikan path file `.docx`.
- Jika platform mendukung, kirim dengan format `MEDIA:/absolute/path/file.docx`.

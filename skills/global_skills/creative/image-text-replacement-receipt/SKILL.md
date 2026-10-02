---
name: image-text-replacement-receipt
description: Ganti nominal/teks pada screenshot struk menggunakan PIL + OCR, dengan fallback koordinat manual untuk gambar kecil/blur.
---

# Kapan dipakai
- User minta mengganti angka/nominal pada gambar struk/screenshot (contoh: `160.000` jadi `188.000`).
- Kasus OCR tidak sempurna dan butuh trial-and-error pada area teks.

# Pendekatan yang terbukti
1. **Deteksi environment Python dulu**
   - `execute_code` bisa gagal import PIL karena pakai interpreter sandbox berbeda.
   - Gunakan `/usr/bin/python3` untuk akses paket sistem.

2. **Pasang dependensi OS-level jika perlu**
   - PIL: `apt-get install -y python3-pil`
   - OCR: `apt-get install -y tesseract-ocr`
   - Wrapper OCR Python: `/usr/bin/python3 -m pip install --break-system-packages pytesseract`

3. **Lakukan OCR kandidat teks target**
   - Pakai `pytesseract.image_to_data(..., output_type=DICT)`.
   - Cari token yang mengandung angka target (mis. `160`, `160.000`, `160000`).

4. **Replace berbasis bounding box**
   - Untuk setiap token cocok: tutup area dengan rectangle putih lalu tulis nominal baru.
   - Gunakan font `DejaVuSans-Bold` agar hasil terbaca.

5. **Fallback manual coordinates (penting)**
   - Pada screenshot kecil/kompres, OCR bisa hanya menangkap sebagian kemunculan.
   - Tambah daftar area manual untuk nominal yang pasti muncul (headline amount, subtotal, total, cash).
   - Ini yang menyelesaikan kasus ketika OCR hanya menemukan 1 instance.

6. **Simpan ke file output baru**
   - Jangan overwrite file asli jika belum diminta.

# Pitfalls
- Jangan mengandalkan OCR saja untuk gambar resolusi rendah.
- Interpreter `python3` aktif bisa bukan sistem Python; cek dengan cepat jika import PIL gagal.
- Hindari menampilkan data sensitif dari struk di respons akhir.

# Template command cepat
```bash
/usr/bin/python3 - <<'PY'
from PIL import Image, ImageDraw, ImageFont
import pytesseract

src='input.jpg'
out='output.jpg'
img=Image.open(src).convert('RGB')
d=ImageDraw.Draw(img)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

data=pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config='--psm 6')
for i,t in enumerate(data['text']):
    t=(t or '').strip().replace(' ','')
    if '160.000' in t or t=='160000' or t=='160.000':
        x,y,w,h=data['left'][i],data['top'][i],data['width'][i],data['height'][i]
        d.rectangle([x-1,y-1,x+w+1,y+h+1], fill='white')
        f=ImageFont.truetype(font, max(9,int(h*0.95)))
        d.text((x,y-1),'188.000',fill='black',font=f)

# fallback koordinat manual bila perlu
manual=[(106,200,236,227,'Rp. 188.000',14)]
for x1,y1,x2,y2,txt,fs in manual:
    d.rectangle([x1,y1,x2,y2], fill='white')
    f=ImageFont.truetype(font,fs)
    d.text((x1+1,y1-1),txt,fill='black',font=f)

img.save(out, quality=95)
print(out)
PY
```

# Verifikasi
- Buka output dan cek semua kemunculan nominal target sudah berubah.
- Jika ada yang terlewat, tambahkan koordinat manual area tersebut.

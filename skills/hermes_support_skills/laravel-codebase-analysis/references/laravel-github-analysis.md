# Laravel Codebase Analysis via GitHub Raw URLs

## Teknik Analisa Tanpa SSH/VPS

Ketika hanya punya akses GitHub repo (bukan server langsung), gunakan `web_extract` dengan URL raw GitHub untuk analisa kode:

### URL Pattern
```
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path/to/file.php}
```

### Contoh
```
https://raw.githubusercontent.com/anonim-sen10/rofc-schoolmusic/main/app/Models/Schedule.php
https://raw.githubusercontent.com/anonim-sen10/rofc-schoolmusic/main/routes/web.php
https://raw.githubusercontent.com/anonim-sen10/rofc-schoolmusic/main/database/migrations/xxx.php
```

### Urutan Analisa yang Efektif

1. **routes/web.php** — Pahami semua rute dan controller yang terpakai
2. **app/Models/*.php** — Struktur tabel, relasi, fillable fields
3. **app/Http/Controllers/*.php** — Logic bisnis, query, validasi
4. **database/migrations/*.php** — Struktur database lengkap
5. **resources/views/**/*.blade.php** — Tampilan frontend (opsional)

### Tips

- Gunakan `char_limit=50000` untuk file controller besar
- Cari pattern dengan Python regex di `execute_code` untuk analisa cepat
- Identifikasi method dengan `public function xxx` pattern
- Cari model relasi: `belongsTo`, `hasMany`, `belongsToMany`
- Jika web_extract timeout, coba dengan char_limit lebih kecil

### Studi Kasus: ROFC Scheduling Issue

**Masalah:** Siswa hanya punya 1 sesi di bulan September (seharusnya 4x/bulan)

**Root Cause ditemukan di:** `ManagesStudents.php` line 290:
```php
$totalSessions = (int) (($student->duration_months ?: 1) * 4);
for ($i = 0; $i < $totalSessions; $i++) {
    // generate sesi 1x per minggu
    $currentDate->addWeek();
}
```

**Penjelasan:** Sesi di-generate SEKALI saat registrasi berdasarkan `duration_months × 4`, bukan auto-renew tiap bulan.

**Solusi:** Tambah logic auto-generate sesi per bulan + cron job tiap tanggal 1.

---
name: laravel-codebase-analysis
description: Analyze Laravel codebases via GitHub raw URLs.
---

# Laravel Codebase Analysis

## When to Use
User wants to analyze a Laravel project but only has GitHub repo access.

## Teknik via GitHub Raw URLs

### URL Pattern
```
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}
```

### Urutan Analisa

1. **routes/web.php** — Rute dan controller
2. **app/Models/*.php** — Struktur tabel, relasi
3. **app/Http/Controllers/*.php** — Logic bisnis
4. **database/migrations/*.php** — Struktur database

### Tool Usage
- `web_extract` dengan `char_limit=50000` untuk file besar
- `execute_code` dengan Python regex untuk analisa cepat

### Pitfall
- File controller besar perlu `char_limit` tinggi
- Cek `routes/web.php` dulu untuk mapping controller

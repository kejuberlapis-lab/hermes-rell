---
name: sql-database-architect
description: Use when designing SQL DBs. Handles schema & indexing.
---

# Production SQL Database Architect & Optimizer

Standar rekayasa database relasional (PostgreSQL, MySQL, SQLite) untuk layanan web komersial.

### Standar Rekayasa Database:
1. **Perancangan Skema & Normalisasi:**
   - Gunakan tipe data eksplisit (Integer, BigInt, VARCHAR dengan batas, DateTime UTC).
   - Tentukan Primary Key, Foreign Key berelasi (`ON DELETE CASCADE / SET NULL`), dan constraint unik secara ketat.

2. **Strategi Indexing & Optimasi Query:**
   - Pasang index pada kolom yang sering dicari (`WHERE`), difilter, atau di-join (misal `user_id`, `created_at`, `status`).
   - Hindari query N+1 dengan `JOIN` atau eager loading pada ORM.

3. **Backup & Migrasi Aman:**
   - Buat file migrasi berkala dan selalu lakukan snapshot data sebelum migrasi skema tabel produksi.

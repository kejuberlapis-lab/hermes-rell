# Telegram Access Control: TELEGRAM_ALLOWED_USERS

## Konsep
- `TELEGRAM_ALLOWED_USERS` di `.env` mengontrol **siapa yang bisa chat** dengan bot
- Setiap profile punya `.env` sendiri (`~/.hermes/profiles/<profile>/.env`) yang override global `.env` (`~/.hermes/.env`)
- Default (tidak ada setting): semua user bisa chat
- Jika diset: hanya user ID di daftar yang bisa chat

## Konfigurasi untuk multi-role access

### Setup: Semua user chat, hanya supermaster approve

**1. Buka akses chat (semua user bisa chat):**
```bash
# Comment out TELEGRAM_ALLOWED_USERS di .env profile
sed -i 's/^TELEGRAM_ALLOWED_USERS=/# TELEGRAM_ALLOWED_USERS=/' ~/.hermes/profiles/<profile>/.env
```

**2. Set approvals untuk system changes only (config.yaml):**
```yaml
approvals:
  mode: auto                        # destructive commands butuh approval
  destructive_slash_confirm: true   # konfirmasi sebelum destructive action
  cron_mode: deny                   # cron butuh approval
```

**3. Supermaster approval:**
- User dengan ID yang diizinkan bisa pakai `/approve`
- User biasa bisa chat tapi tidak bisa approve system changes

## Pitfall

### Multiple TELEGRAM_ALLOWED_USERS entries
Jika `.env` punya 2 baris `TELEGRAM_ALLOWED_USERS=`, yang kedua override yang pertama. Pastikan hanya ada satu entry aktif.

### Per-profile .env vs global .env
- Per-profile `.env` (`~/.hermes/profiles/<profile>/.env`) override global `.env` (`~/.hermes/.env`)
- Cek keduanya saat diagnose access issues

### Commented vs empty
- `# TELEGRAM_ALLOWED_USERS=` (commented) = tidak ada restriction, semua bisa chat
- `TELEGRAM_ALLOWED_USERS=` (empty, no comment) = tidak ada user yang diizinkan, SEMUA DIBLOKIR!
- `TELEGRAM_ALLOWED_USERS=123,456` = hanya user 123 dan 456 yang bisa chat

## Contoh: hermes-support VPS

```bash
# Global .env
TELEGRAM_ALLOWED_USERS=298964291,661471478

# Per-profile .env (hermes-support)
TELEGRAM_ALLOWED_USERS=661471478,5955713269  # duplicate entry!
TELEGRAM_ALLOWED_USERS=661471478,5955713269  # second one wins
```

**Fix:** Comment out atau hapus salah satu entry, pastikan hanya satu yang aktif.

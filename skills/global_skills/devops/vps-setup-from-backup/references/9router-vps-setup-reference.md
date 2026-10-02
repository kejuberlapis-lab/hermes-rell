# 9Router VPS Setup — Detailed Reference

## Overview
9Router adalah LLM gateway/proxy yang menjalankan dashboard di port 20128. Setiap VPS harus punya 9Router sendiri jika ingin independen dari local.

## Key Learnings from VPS Setup (2026-08-25)

### 0. 9Router Native Dependencies Compilation
**Problem:** Pertama kali running 9Router, ia auto-compile sqlite3 dan better-sqlite3 via node-gyp. Proses ini bisa butuh 2-5 menit dan memakan CPU ~65%.

**Observation:** Proses compilation terlihat dari `ps aux | grep -E "node-gyp|cc1"` yang aktif. Port 20128 belum open sampai compilation selesai.

**Fix:** Tunggu compilation selesai. Jangan restart service selama compilation berjalan. Setelah selesai, port 20128 akan listen otomatis.

**Cara cek apakah sudah selesai:**
```bash
# Tunggu sampai tidak ada lagi proses node-gyp/cc1
while pgrep -f "node-gyp" > /dev/null; do sleep 5; done
# Lalu cek port
ss -tlnp | grep 20128
```

### 1. Profile .env not read by gateway
**Problem:** `~/.hermes/profiles/<profile>/.env` TIDAK dibaca oleh gateway process. Gateway hanya membaca `~/.hermes/.env` (utama).

**Proof:** `cat /proc/$(pgrep -f 'profile <name>.*gateway')/environ | tr '\0' '\n' | grep TELEGRAM` — tidak ada output jika token hanya di profile .env.

**Fix:** Token HARUS di `~/.hermes/.env` utama.

### 2. yaml.dump() truncates API keys
**Problem:** Python `yaml.dump()` menulis API key panjang terpotong (misal `sk-b57d3d2b9b1aa5a6-kkn0rm-8e7e9a1d` jadi `sk-b57...9a1d`).

**Detection:** `cat -A config.yaml | grep "sk-"` — jika ada `...` di tengah key.

**Fix:** 
- Jangan pakai `yaml.dump()` untuk rewrite config dengan API key
- Gunakan `sed` untuk edit targeted
- Atau backup dulu, lalu restore key manual

### 3. 9Router API key creation
**Problem:** API key yang dibuat langsung di sqlite (`INSERT INTO apiKeys`) TIDAK dikenali oleh 9Router server. 9Router punya auth layer sendiri.

**Fix:** API key HARUS dibuat dari dashboard:
1. Login ke http://<VPS_IP>:20128
2. Buka menu API Keys
3. Klik Create API Key
4. Copy key yang dihasilkan

### 4. 9Router INITIAL_PASSWORD
**Problem:** "Default password must be changed before remote access" saat pertama kali diakses dari browser.

**Fix:** Set `INITIAL_PASSWORD` di systemd service:
```bash
sed -i '/Environment=SHELL=/a Environment=INITIAL_PASSWORD=<password>' ~/.config/systemd/user/9router.service
systemctl --user daemon-reload && systemctl --user restart 9router.service
```

### 5. Multiple gateways + same token = conflict
**Problem:** Menjalankan 6+ gateway service dengan token Telegram yang sama = polling conflict.

**Fix:** Jalankan HANYA 1 gateway per token. Stop semua gateway lain.

### 6. 9Router bind address
**Problem:** Default bind `127.0.0.1` — dashboard tidak bisa diakses dari browser luar.

**Fix:** Ganti ke `0.0.0.0` di systemd service.

## Profile Config Structure
Profile config harus punya:
```yaml
model:
  base_url: http://localhost:20128/v1
  default: <model-name>
  provider: custom
  api_mode: chat_completions
custom_providers:
  - name: 9Router
    base_url: http://localhost:20128/v1
    api_key: <valid-key-from-dashboard>
    model: <model-name>
```

## Verification Steps
1. `curl -s http://localhost:20128/v1/models -H 'Authorization: Bearer <key>'` — harus return model list
2. `curl -s -X POST http://localhost:20128/v1/chat/completions -H 'Content-Type: application/json' -H 'Authorization: Bearer <key>' -d '{"model":"<model>","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}'` — harus return response
3. `systemctl --user is-active hermes-gateway-<profile>.service` — harus `active`
4. `journalctl --user -u hermes-gateway-<profile>.service -n 10 --no-pager | grep -i error` — tidak ada error

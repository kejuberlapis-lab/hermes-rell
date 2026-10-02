---
name: model-override-cleanup
description: "Clean up stuck model overrides across all storage locations (sessions.json, state.db gateway_routing, state.db sessions table) when a Hermes profile uses wrong model/provider despite correct config.yaml."
version: 1.0.0
author: Hermes
created_by: agent
tags: [devops, hermes, model, override, troubleshooting, multi-profile]
triggers:
  - bot pakai model/provider SALAH meskipun config sudah benar
  - model override stuck / tertinggal
  - error 429 karena provider salah
  - custom:custom provider bug
  - ganti model tapi tidak berubah di Telegram
---

# Model Override Cleanup

## Kapan dipakai
- Bot Telegram pakai model/provider yang salah meskipun `config.yaml` sudah benar
- User mengubah model via `/model` di Telegram tapi perubahan tidak konsisten
- Error 429/401 karena provider di override salah (misal `custom:custom` bukan `custom:9router`)
- Setelah migrasi profile, model lama masih nempel

## 4 Lokasi Model Override

Override tersimpan di **4 tempat** secara terpisah. Semua harus di-check dan di-clear:

| # | Lokasi | Path | Tipe | Impact |
|---|--------|------|------|--------|
| 1 | Sessions routing | `sessions/sessions.json` | `model_override` dict | Routing gateway ke model/provider |
| 2 | Gateway routing DB | `state.db` → `gateway_routing` | `entry_json` JSON | Primary routing source (gateway reads ini) |
| 3 | Sessions DB | `state.db` → `sessions` | `model` + `billing_provider` + `billing_base_url` kolom | Runtime model/provider saat API call — **jangan lupa clear ini juga!** |
| 4 | Config default | `config.yaml` → `model.default` | String | Default untuk chat baru |

**PITFALL #2:** `gateway_routing.entry_json` bisa menyimpan `model_override` sebagai nested JSON dict (bukan kolom terpisah). Cek dengan:
```python
import json
c.execute('SELECT session_key, entry_json FROM gateway_routing')
for row in c.fetchall():
    entry = json.loads(row[1])
    if 'model_override' in entry:
        print(f'Still has override: {row[0]}: {entry["model_override"]}')
```

**PITFALL #3:** `sessions` table punya kolom `model`, `billing_provider`, `billing_base_url` yang TIDAK NULL berarti model lama masih aktif. Clear dengan:
```python
c.execute('UPDATE sessions SET model=NULL, billing_provider=NULL, billing_base_url=NULL WHERE model IS NOT NULL')
```

**PITFALL KRITIS:** Gateway **meregenerasi** `sessions.json` dari memory/cache jika masih running. Override yang di-clear saat gateway running akan muncul lagi.

**PITFALL BARU (2026-08):** `sessions` table juga punya kolom `model`, `billing_provider`, `billing_base_url` yang bisa override config.yaml. Ini sering terlewat karena fokus ke `gateway_routing` saja. **SELALU clear kedua-duanya:**
```python
# Clear gateway_routing
c.execute('SELECT session_key, entry_json FROM gateway_routing')
for row in c.fetchall():
    entry = json.loads(row[1])
    if 'model_override' in entry:
        del entry['model_override']
        c.execute('UPDATE gateway_routing SET entry_json=? WHERE session_key=?',
                  (json.dumps(entry), row[0]))
# Clear sessions (INI YANG SERING TERLEWAT!)
c.execute('UPDATE sessions SET model=NULL, billing_provider=NULL, billing_base_url=NULL WHERE model IS NOT NULL OR billing_provider IS NOT NULL')
```

## Prosedur Cleanup

### Langkah 1: STOP Gateway

```bash
systemctl --user stop hermes-gateway.service
sleep 3
# Verify stopped
ps aux | grep 'hermes.*gateway' | grep -v grep | wc -l  # harus 0
```

### Langkah 2: Clear dari Semua Lokasi

```python
import json, sqlite3, os, glob

profiles_dir = os.path.expanduser('~/.hermes/profiles')

for profile_dir in sorted(glob.glob(os.path.join(profiles_dir, '*'))):
    if not os.path.isdir(profile_dir):
        continue
    name = os.path.basename(profile_dir)

    # 1. Clear sessions.json
    sj_path = os.path.join(profile_dir, 'sessions', 'sessions.json')
    if os.path.exists(sj_path):
        with open(sj_path) as f:
            data = json.load(f)
        changed = False
        for k, v in data.items():
            if isinstance(v, dict) and 'model_override' in v:
                chat = v.get('display_name', k)
                print(f'Clearing {name}/{chat}: {v["model_override"]}')
                del v['model_override']
                changed = True
        if changed:
            with open(sj_path, 'w') as f:
                json.dump(data, f, indent=2)

    # 2. Clear state.db gateway_routing
    db_path = os.path.join(profile_dir, 'state.db')
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT session_key, entry_json FROM gateway_routing')
        changed = False
        for row in cur.fetchall():
            entry = json.loads(row[1])
            if 'model_override' in entry:
                chat = entry.get('display_name', row[0])
                print(f'Clearing DB {name}/{chat}: {entry["model_override"]}')
                del entry['model_override']
                cur.execute('UPDATE gateway_routing SET entry_json=? WHERE session_key=?',
                            (json.dumps(entry), row[0]))
                changed = True
        if changed:
            conn.commit()
        conn.close()

# 3. Fix session model/provider (jika perlu)
# conn = sqlite3.connect('state.db')
# cur = conn.cursor()
# cur.execute('UPDATE sessions SET model=?, billing_provider=? WHERE user_id=? AND id=?',
#             ('<correct_model>', 'custom', '<telegram_user_id>', '<session_id>'))
# conn.commit()
# conn.close()
```

### Langkah 3: RESTART & Verify

```bash
systemctl --user start hermes-gateway.service
sleep 5
ps aux | grep 'hermes.*gateway' | grep -v grep | wc -l  # harus 9
```

## `custom:custom` Provider Bug

**Symptom:** Error 429 meskipun model tersedia di provider.

**Cause:** Override punya `provider: "custom:custom"` — prefix `custom:` diikuti nama provider di `custom_providers` list. Jika nama salah, request ke provider yang tidak ada.

**Fix:** Clear override (lihat prosedur di atas), lalu restart gateway.

## Multi-Profile Access Control

Untuk setup: semua user bisa chat, hanya supermaster bisa approve/system changes:

```bash
# 1. Buka akses chat (comment TELEGRAM_ALLOWED_USERS di .env)
sed -i 's/^TELEGRAM_ALLOWED_USERS=/# TELEGRAM_ALLOWED_USERS=/' ~/.hermes/profiles/<profile>/.env

# 2. Set approvals
python3 -c "
import yaml
path = '~/.hermes/profiles/<profile>/config.yaml'
with open(path) as f:
    c = yaml.safe_load(f) or {}
c.setdefault('approvals', {})['mode'] = 'auto'
c['approvals']['destructive_slash_confirm'] = True
c.setdefault('telegram', {})['allowed_chats'] = ''
c['telegram']['require_mention'] = True
with open(path, 'w') as f:
    yaml.dump(c, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
"
```

## Guardrail
- SELALU stop gateway sebelum clear override
- Jangan gunakan `yaml.dump()` untuk rewrite config besar tanpa backup — bisa mengubah struktur YAML
- Password/token yang diberikan user untuk SSH: ingatkan user untuk mengganti setelah dipakai

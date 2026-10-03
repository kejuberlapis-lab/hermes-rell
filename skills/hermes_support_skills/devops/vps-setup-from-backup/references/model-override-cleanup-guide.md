# Model Override Cleanup Guide

Saat Hermes profile menggunakan model/provider yang salah meski config.yaml sudah benar.

## Penyebab
Model override tersimpan di **4 lokasi**:
1. `state.db` → table `gateway_routing` → column `entry_json` (JSON field `model_override`)
2. `state.db` → table `sessions` → columns `model`, `billing_provider`, `billing_base_url`
3. `sessions.json` (jika ada)
4. `config.yaml` (yang ini paling mudah dicek)

## Diagnosis

```bash
# Cek gateway_routing
python3 -c "
import sqlite3, json
db = sqlite3.connect('state.db')
c = db.cursor()
c.execute('SELECT session_key, entry_json FROM gateway_routing')
for row in c.fetchall():
    entry = json.loads(row[1])
    if 'model_override' in entry:
        print(f'FOUND override in gateway_routing: {row[0]}')
        print(f'  {json.dumps(entry[\"model_override\"], indent=2)}')
"

# Cek sessions
python3 -c "
import sqlite3
db = sqlite3.connect('state.db')
c = db.cursor()
c.execute('SELECT id, model, billing_provider, billing_base_url FROM sessions WHERE model IS NOT NULL OR billing_provider IS NOT NULL')
for row in c.fetchall():
    print(f'FOUND override in sessions: {row[0]} model={row[1]} provider={row[2]} url={row[3]}')
"
```

## Cleanup Script

```python
import sqlite3, json

db = sqlite3.connect('state.db')
c = db.cursor()

# 1. Clear gateway_routing
c.execute('SELECT session_key, entry_json FROM gateway_routing')
for row in c.fetchall():
    entry = json.loads(row[1])
    if 'model_override' in entry:
        del entry['model_override']
        c.execute('UPDATE gateway_routing SET entry_json=? WHERE session_key=?',
                  (json.dumps(entry), row[0]))
        print(f'Cleared gateway_routing: {row[0]}')

# 2. Clear sessions
c.execute('UPDATE sessions SET model=NULL, billing_provider=NULL, billing_base_url=NULL WHERE model IS NOT NULL OR billing_provider IS NOT NULL')
print(f'Cleared {c.rowcount} session overrides')

db.commit()
db.close()
print('Done — restart gateway')
```

## Setelah Cleanup
**WAJIB restart gateway** agar override dari memory juga di-clear:
```bash
systemctl --user restart hermes-gateway-<profile>.service
```

## Pencegahan
- Jangan pakai `/model` command kecuali memang mau switch model
- Jangan pakai `hermes model set` tanpa tujuan jelas
- Config.yaml harus sudah benar SEBELUM user mulai chat

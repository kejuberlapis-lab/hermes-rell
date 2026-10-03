# 9Router API Key Credential Update

## ⚠️ Format DB berubah: db.json (lama) → SQLite (v16.2.1+)

9Router **v16.2.1** (appVersion 0.5.20, schemaVersion 1) menyimpan data di
**SQLite**, bukan `db.json` lagi:

```
~/.9router/db/data.sqlite        # DB utama
~/.9router/db/data.sqlite-wal    # write-ahead log
~/.9router/db/data.sqlite-shm    # shared memory
~/.9router/db/backups/           # backup otomatis
```

Tabel penting: `providerConnections`, `apiKeys`, `providerNodes`, `combos`,
`proxyPools`, `settings`, `kv`, `usageHistory`, `_meta`.

**⚠️ `sqlite3` CLI sering TIDAK terinstall di VPS.** Gunakan Python `sqlite3`
module (selalu ada di python3 stdlib).

Cek versi & lokasi:
```bash
ps aux | grep next-server | grep -v grep | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+'
python3 -c "import sqlite3; c=sqlite3.connect('/home/ubuntu/.9router/db/data.sqlite'); print([r[0] for r in c.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")])"
```

Skema kolom `providerConnections`:
`id, provider, authType, name, email, priority, isActive, data, createdAt, updatedAt`

**apiKey tersimpan sebagai PLAINTEXT JSON di kolom `data`**, contoh:
`{"apiKey":"sk-...","testStatus":"active","lastError":null,...}`.
Karena tidak dienkripsi dengan `jwt-secret`, kredensial **bisa dimigrasi
antar-VPS** meskipun `jwt-secret` kedua VPS berbeda.

## 9Router dikelola sebagai user systemd service

```bash
systemctl --user status 9router.service
systemctl --user stop 9router.service     # flush DB sebelum edit
systemctl --user start 9router.service
```
Proses: `node .../9router --host 0.0.0.0 --port 20128 ...` yang men-spawn
`next-server`. Selalu **stop service dulu** sebelum mengedit data.sqlite,
supaya perubahan tidak ter-clobber oleh cache memory / WAL.

## Prosedur update API key (format SQLite)

### 1. Backup + stop service
```bash
cp ~/.9router/db/data.sqlite ~/.9router/db/data.sqlite.bak-$(date +%Y%m%d_%H%M%S)
systemctl --user stop 9router.service
```

### 2. Update apiKey di kolom `data` (Python)
```python
import sqlite3, json
con = sqlite3.connect("/home/ubuntu/.9router/db/data.sqlite")
con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
for row in con.execute("SELECT id, data FROM providerConnections WHERE provider=?", ("minimax",)).fetchall():
    d = json.loads(row[1])
    d["apiKey"] = "<new_key>"
    d["lastError"] = None; d["lastErrorAt"] = None; d["testStatus"] = "active"
    con.execute("UPDATE providerConnections SET data=?, isActive=1 WHERE id=?", (json.dumps(d), row[0]))
con.commit(); con.close()
```

### 3. Start + verifikasi
```bash
systemctl --user start 9router.service && sleep 4
curl -s -m 30 -w '\nHTTP_CODE:%{http_code}' http://localhost:20128/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"<provider>/<model>","messages":[{"role":"user","content":"ping"}],"max_tokens":5}'
```

## Migrasi kredensial antar-VPS (fresh 9Router install)

Kasus nyata (12 Jul 2026): migrasi ke VPS baru. 9Router sudah terinstall &
jalan (versi sama), TAPI `providerConnections` **kosong (0 baris)** → semua
model gagal `HTTP 404: No active credentials for provider: <x>`. Ini BUKAN
masalah install — cukup migrasi kredensial.

**Diagnosa cepat kosong-tidaknya kredensial:**
```python
import sqlite3
c=sqlite3.connect("/home/ubuntu/.9router/db/data.sqlite")
print("providerConnections:", c.execute("SELECT count(*) FROM providerConnections").fetchone()[0])
```

**Prosedur migrasi (VPS lama → VPS baru):**

1. **Export** dari VPS lama (key tidak dicetak):
```python
import sqlite3, json
con=sqlite3.connect("/home/ubuntu/.9router/db/data.sqlite"); con.row_factory=sqlite3.Row
out={t:[dict(r) for r in con.execute("SELECT * FROM %s"%t).fetchall()]
     for t in ["providerConnections","providerNodes"]}
open("/tmp/9r_migrate.json","w").write(json.dumps(out))
```
2. **Transfer** file `/tmp/9r_migrate.json` ke VPS baru (scp / sftp).
3. **Backup + stop** service di VPS baru (lihat atas).
4. **Inject** (INSERT OR REPLACE, dinamis per kolom):
```python
import sqlite3, json
data=json.load(open("/tmp/9r_migrate.json"))
con=sqlite3.connect("/home/ubuntu/.9router/db/data.sqlite")
con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
def insert(table, rows):
    if not rows: return 0
    cols=list(rows[0].keys()); ph=",".join(["?"]*len(cols))
    q="INSERT OR REPLACE INTO %s (%s) VALUES (%s)"%(table,",".join(cols),ph)
    for r in rows: con.execute(q,[r[c] for c in cols])
    return len(rows)
insert("providerConnections", data["providerConnections"])
insert("providerNodes", data["providerNodes"])
con.commit(); con.close()
```
5. **Start** + curl test model tiap profile.

**⚠️ JANGAN migrasi tabel `apiKeys`** jika error yang muncul `HTTP 404`
(bukan `401`). 404 = auth gateway→9Router sudah lolos, hanya provider kosong.
Menimpa `apiKeys` bisa merusak auth yang sudah jalan. Migrasi `apiKeys` hanya
jika error benar-benar `401` (token gateway tidak dikenal).

**Catatan:** `combos` & `proxyPools` biasanya kosong — skip. `providerNodes`
berisi routing/alias model (mis. MiniMax-M2.7, ds/deepseek-v4-pro) — ikut
migrasi supaya alias tetap resolve.

## Cooldown behavior setelah update

Setelah key diupdate, 9Router perlu ~90 detik untuk re-test credential:

| Field | Nilai sementara | Arti |
|-------|----------------|------|
| `testStatus` | `unavailable` | 9Router sedang re-test, normal |
| `lastError` | `None` | Belum ada hasil test |
| curl test langsung | Bisa HTTP 200 ✅ | Model sudah bisa dipakai |

Jangan panik lihat `testStatus: unavailable` — tes langsung via curl.

## Restart gateway (jika perlu)

Jika model tidak berfungsi setelah key diupdate, restart gateway profile ybs:
```bash
systemctl --user restart hermes-gateway-<profile>.service
sleep 5
cat ~/.hermes/profiles/<profile>/gateway_state.json   # state=running, telegram=connected
```

## Key Security

- **⚠️ Key yang sudah diketik di chat sudah terekspos.** Segera revoke & regen.
- Key yang masuk langsung ke DB (tanpa lewat chat) aman.
- Jangan tampilkan full apiKey di output — cukup prefix + suffix.
- Saat migrasi via file, transfer lewat scp/sftp; jangan echo isi key ke terminal.

## Error Saat Update

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `HTTP 404: No active credentials for provider: X` | providerConnections kosong / isActive=0 untuk provider X | Migrasi/aktifkan kredensial (lihat atas) |
| `HTTP 401: Unavailable (reset after Xm Ys)` | 9Router masih cooldown test credential | Tunggu ~90 detik, test ulang |
| `testStatus: unavailable` tetap >5 menit | Key mungkin invalid | Cek dashboard provider, test key ke endpoint provider |
| `testStatus: error` | Key ditolak | Ganti key, cek format |

## Catatan format lama (db.json — pre-v16.2.1)

Versi 9Router lama menyimpan di `~/.9router/db.json` (JSON tunggal). Jika
menemukan file `db.json` DAN `db/data.sqlite`, yang **aktif adalah SQLite** —
`db.json` hanya artefak lama. Edit di db.json TIDAK berpengaruh pada v16.2.1.

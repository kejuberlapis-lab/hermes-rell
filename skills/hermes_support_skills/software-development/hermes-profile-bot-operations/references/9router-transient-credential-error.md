# 9Router Transient Credential Error

## Symptom

Gateway running (`active_agents=0`, `telegram.state=connected`), tapi API call gagal dengan:

```
Error code: 404 - {
  'error': {
    'message': 'No active credentials for provider: minimax',
    'type': 'invalid_request_error',
    'code': 'model_not_found'
  }
}
```

## Diagnosis Chain

### 1. Cek gateway_state.json

```bash
cat ~/.hermes/profiles/<profile>/gateway_state.json
```

Pastikan:
- `gateway_state: "running"` — gateway hidup
- `telegram.state: "connected"` — Telegram terhubung
- `active_agents: 0` — tidak ada agent stuck

### 2. Cek error di agent.log

```bash
grep "No active credentials" ~/.hermes/profiles/<profile>/logs/agent.log | tail -5
```

Perhatikan `provider` di error message — provider mana yang ditolak?

### 3. Verifikasi credential di 9Router db.json

Cek langsung status credential dari db.json:

```bash
cat ~/.9router/db.json | python3 -c "
import json, sys
db = json.load(sys.stdin)
for conn in db.get('providerConnections', []):
    p = conn.get('provider', '?')
    if p == '<provider-dari-error>':
        print(f'{p}: isActive={conn.get(\"isActive\")}, testStatus={conn.get(\"testStatus\")}, lastError={conn.get(\"lastError\")}')
"
```

### 4. Direct curl test

Ini langkah **paling penting** — test langsung ke 9Router dengan model yang sama:

```bash
curl -s -w '\nHTTP_CODE: %{http_code}' http://localhost:20128/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"<provider>/<model>","messages":[{"role":"user","content":"test"}],"max_tokens":10}'
```

**Interpretasi hasil:**

| Hasil curl | Arti | Tindakan |
|---|---|---|
| HTTP 200, model merespon | **Transient error** — 9Router return 404 sesaat, tapi credential dan model OK | Tidak perlu restart. Kirim ulang pesan ke bot. Error akan hilang dengan sendirinya. |
| HTTP 404 dengan pesan sama | **Credential benar-benar tidak aktif** — mungkin expired atau dihapus | Cek dashboard 9Router, update key, restart 9Router |
| HTTP 401 | **API key invalid** — key expired atau format salah | Ganti key di db.json |

**Penting:** Jangan langsung restart gateway hanya karena error 404 ini. Jika curl test berhasil, gateway akan melanjutkan normal pada request berikutnya.

## Root Cause

9Router kadang mengalami race condition internal saat memvalidasi credential pool. Ini terjadi ketika:

- Banyak request simultan dari berbagai profile/agent
- 9Router sedang sync state internal (misal setelah credential diupdate)
- Beban tinggi pada server 9Router

9Router tetap akan serve model setelah credential pool selesai sync — biasanya dalam hitungan detik.

## Bedakan dari Error Sungguhan

| Karakteristik | Transient (ini) | Credential benar-benar mati |
|---|---|---|
| Cara deteksi | curl test langsung ke 9Router **berhasil** | curl test juga gagal 404/401 |
| Durasi | Hilang sendiri dalam detik-menit | Bertahan sampai credential diperbaiki |
| Test status di db.json | `active` atau berubah ke `active` dalam beberapa detik | `inactive` atau `error` |
| Solusi | Kirim ulang pesan, tunggu | Restart 9Router, update API key |

## Contoh Sesi Nyata

Pada 2026-05-28, hermes-support gateway (profile) menggunakan `minimax/MiniMax-M2.7` via 9Router. Tiba-tiba tiap API call gagal dengan 404 "No active credentials for provider: minimax". Padahal:

- `db.json` credential minimax: `isActive: True, testStatus: active, lastError: None`
- curl test langsung ke `http://localhost:20128/v1/chat/completions` dengan `model=minimax/MiniMax-M2.7`: **HTTP 200, respon normal**
- Masalah hilang sendiri tanpa restart

Kesimpulan: **transient 9Router race condition. Tidak perlu intervensi.**

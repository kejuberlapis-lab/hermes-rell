# Gateway Layered Diagnostic Chain

## Kapan pakai ini

Gateway berjalan (PID terlihat, Telegram "connected") tapi bot tidak membalas pesan. Atau gateway crash-loop dengan exit-code.

## Prinsip

Jangan tebak-tebak profile/provider mana yang error. Ikuti rantai ini dari atas ke bawah:

```
systemd service file  →  journalctl  →  config.yaml  →  .env  →  request_dump JSON
```

Setiap lapisan mengungkap informasi yang lapisan sebelumnya sembunyikan.

## Layer 1: Systemd service file

Menentukan **profile mana** yang gateway-nya error, dan **argumen/var env** apa yang dipakai.

```bash
# Lihat semua service file gateway
ls ~/.config/systemd/user/hermes-gateway*.service

# Baca isi service file tertentu — perhatikan
#   - ExecStart: apakah ada --profile <name>?
#   - Environment=HERMES_HOME: mengarah ke profile mana?
systemctl --user cat hermes-gateway-hermes-support.service
```

**Contoh output:**
```
ExecStart=...python -m hermes_cli.main --profile hermes-support gateway run --replace
Environment="HERMES_HOME=/home/ubuntu/.hermes/profiles/hermes-support"
```

Ini berarti error ada di profile `hermes-support`, bukan di default profile.

## Layer 2: journalctl

Menunjukkan **provider dan model aktual** yang dipanggil — bisa berbeda dari yang terlihat di config.yaml jika ada fallback atau auto-routing.

```bash
# Pastikan pakai service name yang benar dari Layer 1!
journalctl --user -u hermes-gateway-hermes-support.service --no-pager -n 100
```

**Cari baris ini:**
```
API call failed (attempt 1/3) ... provider=minimax model=minimax-m2.7
  endpoint=https://api.minimax.io/anthropic
  summary=HTTP 401: login fail: Please carry the API secret key
```

Perhatikan:
- `provider` dan `model` — ini yang BENAR-BENAR dipakai, bukan config default
- `endpoint` — kadang ada fallback endpoint yang berbeda
- `summary` — pesan error asli dari API

## Layer 3: config.yaml profile

Menunjukkan konfigurasi model default, fallback, dan auxiliary.

```bash
cat ~/.hermes/profiles/<profile>/config.yaml | grep -A5 '^model:'
```

**Perhatikan:**
- `model.default` — model utama
- `model.provider` — provider utama
- `model.fallback_model` dan `model.fallback_providers` — fallback jika utama gagal
- `auxiliary.*.provider` — bisa beda provider untuk subtitle task

## Layer 4: .env profile

Menunjukkan API key mana yang tersedia (tanpa melihat nilainya).

```bash
grep -E 'API_KEY|_TOKEN|_SECRET' ~/.hermes/profiles/<profile>/.env | grep -v '^#' | grep -v 'your_'
```

**Perhatikan:**
- Apakah key provider utama ada?
- Apakah panjang key sesuai? (DeepSeek = 35 chars, MiniMax native = variable)
- Apakah ada key yang terredact jadi `***`? (tanda terkena redaction tool)
- Untuk copy key yang aman: lihat `references/api-key-safe-write-via-ssh.md` (base64 workaround untuk hindari redaction).

## Layer 5: request_dump JSON

Debug dump yang disimpan saat API call gagal. Berisi full request payload tanpa redaction.

```bash
ls -t ~/.hermes/profiles/<profile>/sessions/request_dump_*.json | head -3
```

File ini berisi:
- Request headers (termasuk Authorization — TAPI JANGAN DITAMPILKAN)
- Request body (model, messages, params)
- Error response dari API

**⚠️ Hati-hati:** File ini mengandung RAW API KEY. Jangan cat atau tampilkan isinya.

## Contoh rantai dari sesi nyata

**Gejala:** Bot Telegram terlihat "connected" tapi tidak membalas.

**Layer 1 (service file):**
```
hermes-gateway-hermes-support.service → --profile hermes-support
```

**Layer 2 (journalctl):**
```
provider=minimax model=minimax-m2.7
HTTP 401: login fail: Please carry the API secret key in the 'X-Api-Key' field
```

**Layer 3 (config.yaml):**
```yaml
model:
  default: minimax-m2.7
  provider: minimax
```

**Layer 4 (.env):**
```
MINIMAX_API_KEY=***  ← terlihat ada, tapi 401 berarti expired/invalid
```

**Root cause:** MiniMax API key expired atau format key salah. Ganti key atau pindah provider.

> **Catatan:** Error code `(1004)` setelah "login fail" menandakan format key tidak dikenali — bukan key expired. Key dengan prefix `sk-api-` atau `sk-cp-` selalu ditolak MiniMax. Lihat `references/minimax-api-key-troubleshooting.md` untuk detail key format dan error codes.

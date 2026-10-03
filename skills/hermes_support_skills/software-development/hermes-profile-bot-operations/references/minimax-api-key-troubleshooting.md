# MiniMax API Key Troubleshooting

## Key Format

MiniMax API keys untuk endpoint `api.minimax.io` harus dalam format **native MiniMax** dari https://platform.minimaxi.com/, bukan format OpenAI-compatible (`sk-...`).

| Key prefix | Provider | Status |
|---|---|---|
| `sk-api-...` | OpenAI / generic | ❌ Ditolak MiniMax — 401 baik via `/v1` (code 1004) maupun `/anthropic` (x-api-key header) |
| `sk-cp-...` | OpenCode / custom | ❌ Ditolak MiniMax — 401 error code (1004) |
| `sk-or-...` | OpenRouter | ❌ Bukan untuk MiniMax |
| (random alphanumeric) | MiniMax native | ✅ Bekerja — dapatkan dari https://platform.minimaxi.com/ |

## Hermes Provider Internals

Provider `minimax` di Hermes didefinisikan sebagai:

```python
"minimax": HermesOverlay(
    transport="anthropic_messages",  # Uses Anthropic SDK (x-api-key header)
    base_url_env_var="MINIMAX_BASE_URL",
),
```

- **Transport:** `anthropic_messages` → Hermes menggunakan Anthropic SDK (`@ai-sdk/anthropic`) untuk provider ini, bukan OpenAI-compatible SDK.
- **Auth header:** `x-api-key` (Anthropic style), BUKAN `Authorization: Bearer`.
- **Default API URL (model catalog):** `https://api.minimax.io/anthropic/v1`
- **Endpoint aktual:** `{base_url}/messages` (Anthropic format), bukan `/chat/completions`.

### Bagaimana `MINIMAX_BASE_URL` di .env berinteraksi

1. Jika `MINIMAX_BASE_URL` **TIDAK diset** → Hermes pakai default dari model catalog: `https://api.minimax.io/anthropic/v1`
2. Jika `MINIMAX_BASE_URL` **diset** → override default. Fungsi `determine_api_mode()` di `hermes_cli/providers.py` mengecek:
   - Apakah URL berakhiran `/anthropic`? → `anthropic_messages` mode (gunakan Anthropic SDK)
   - Apakah URL berakhiran `/v1`? → `chat_completions` mode (OpenAI-compatible)
   - Apakah URL mengandung `api.openai.com`? → `codex_responses` mode

**Rekomendasi:** Biarkan `MINIMAX_BASE_URL` tidak diset (commented out) agar Hermes menggunakan default model catalog yang sudah benar. Set `MINIMAX_BASE_URL` hanya jika ingin custom endpoint (misal reverse proxy).

## Endpoint Reference

| Endpoint | Format API | Auth Header | Hermes api_mode |
|---|---|---|---|
| `https://api.minimax.io/v1` | OpenAI-compatible (`/chat/completions`) | `Authorization: Bearer` | `chat_completions` |
| `https://api.minimax.io/anthropic` | Anthropic-compatible (`/messages`) | `x-api-key` | `anthropic_messages` |
| `https://api.minimax.io/anthropic/v1` | Anthropic-compatible (`/messages`) | `x-api-key` | `anthropic_messages` (default catalog) |

Error code `(1004)` muncul saat key dikirim ke endpoint `/v1` dengan format yang tidak dikenali MiniMax. Jika error tanpa code `(1004)` dan menyebut `'X-Api-Key' field`, berarti key dikirim ke endpoint `/anthropic` tapi tetap ditolak.

## Error Codes

### Error (1004) — "login fail: Please carry the API secret key in the 'Authorization' field"

**Arti:** Key format tidak dikenali oleh MiniMax API.

**Penyebab umum:**
- Key adalah format OpenAI (`sk-...`) yang dicoba ke endpoint MiniMax
- Key sudah expired
- Key di-copy dengan typo atau truncation

**Cek:**
```python
import urllib.request, json

key = "<actual_key>"
url = "https://api.minimax.io/v1/chat/completions"
# ... test key
```

### Error (1004) dengan "X-Api-Key" — "login fail: Please carry the API secret key in the 'X-Api-Key' field"

Varian header — sama-sama format key tidak dikenali.

## Prosedur Testing Key dari VPS

Gunakan Python heredoc via SSH untuk test tanpa expose key di log terminal. **PENTING: test langsung ke endpoint yang benar sesuai format endpoint yang dipakai.**

### Test ke OpenAI-compatible endpoint (`/v1`)

```bash
ssh ubuntu@<vps> 'python3 << '\''PYEOF'\''
import urllib.request, json

key = "actual_api_key_here"
url = "https://api.minimax.io/v1/chat/completions"
payload = json.dumps({
    "model": "minimax-m2.7",
    "messages": [{"role": "user", "content": "hi"}],
    "max_tokens": 5
}).encode()
req = urllib.request.Request(url, data=payload)
req.add_header("Authorization", f"Bearer {key}")
req.add_header("Content-Type", "application/json")
try:
    resp = urllib.request.urlopen(req, timeout=20)
    data = json.loads(resp.read())
    print(f"OK: {data['choices'][0]['message']['content']}")
except urllib.error.HTTPError as e:
    body = e.read().decode()[:200]
    print(f"FAIL {e.code}: {body}")
PYEOF'
```

### Test ke Anthropic-compatible endpoint (`/anthropic/v1`)

MiniMax Anthropic endpoint menggunakan **`x-api-key` header** (bukan `Authorization: Bearer`) dan format **Anthropic Messages API** (`/v1/messages`), bukan OpenAI Chat Completions:

```bash
ssh ubuntu@<vps> 'python3 << '\''PYEOF'\''
import urllib.request, json

key = "actual_api_key_here"
url = "https://api.minimax.io/anthropic/v1/messages"
payload = json.dumps({
    "model": "minimax-m2.7",
    "max_tokens": 10,
    "messages": [{"role": "user", "content": "hi"}]
}).encode()
req = urllib.request.Request(url, data=payload)
req.add_header("x-api-key", key)
req.add_header("Content-Type", "application/json")
req.add_header("anthropic-version", "2023-06-01")  # Required by Anthropic API
try:
    resp = urllib.request.urlopen(req, timeout=20)
    data = json.loads(resp.read())
    print(f"OK: {data['content'][0]['text']}")
except urllib.error.HTTPError as e:
    body = e.read().decode()[:200]
    print(f"FAIL {e.code}: {body}")
PYEOF'
```

### Interpretasi hasil

| Hasil | Arti |
|---|---|
| `/v1` OK, `/anthropic` FAIL | Key valid untuk OpenAI endpoint, endpoint `/anthropic` mungkin butuh key berbeda |
| Keduanya FAIL 401 | **Key tidak valid** — ganti key atau gunakan provider lain |
| `/v1` FAIL code (1004), `/anthropic` FAIL tanpa code | Key format tidak dikenali — mungkin key dari platform lain (OpenAI, OpenCode, dll.) |

Jika kedua endpoint gagal dengan 401 meskipun header sudah benar, key tersebut **pasti tidak valid** — jangan buang waktu debugging lebih lanjut. Ganti ke provider lain (DeepSeek, OpenRouter, Google).

## Jika Key Tidak Bekerja

1. **Cek dashboard MiniMax** — pastikan key masih aktif dan model `minimax-m2.7` atau `MiniMax-M2.7` tersedia di akun tersebut.
2. **Cek endpoint** — MiniMax global: `https://api.minimax.io/v1`, MiniMax China: `https://api.minimaxi.com/v1`.
3. **Cek format key** — jika key dimulai `sk-`, itu bukan key MiniMax langsung. Mungkin key dari proxy/reverse-proxy yang perlu endpoint berbeda.
4. **Ganti provider** — jika key terus ditolak, gunakan provider alternatif (DeepSeek, OpenRouter, Google) daripada menghabiskan waktu debugging key invalid.

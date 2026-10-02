# Hermes Provider Reference

Gunakan saat perlu tahu provider apa saja yang tersedia di Hermes, error auth apa yang dihasilkan, dan cara memilih provider yang tepat.

## Daftar provider yang tersedia

Cek di VPS/lokal via:
```bash
ls ~/.hermes/hermes-agent/plugins/model-providers/
```

**Provider umum (aktif):**
| Provider | Nama di config | Base URL default | Catatan |
|----------|---------------|------------------|---------|
| DeepSeek | `deepseek` | `https://api.deepseek.com/v1` | Key 35 karakter. Bisa IP-restricted |
| OpenAI Codex | `openai-codex` | `https://chatgpt.com/backend-api/codex` | OAuth eksternal, bukan API key biasa |
| OpenRouter | `openrouter` | `https://openrouter.ai/api/v1` | Key expired → 401 "User not found" |
| Custom | `custom` | Bisa diisi bebas | Untuk OpenAI API: set `base_url: https://api.openai.com/v1` |
| Gemini | `gemini` | Google AI Studio | Key dari `GOOGLE_API_KEY` atau `GEMINI_API_KEY` |
| Anthropic | `anthropic` | API Anthropic | - |
| xAI | `xai` | API x.ai | - |
| NVIDIA | `nvidia` | NVIDIA AI Foundry | - |
| Ollama Cloud | `ollama-cloud` | - | - |
| Bedrock | `bedrock` | AWS Bedrock | - |

## Error messages yang umum

| Error | Provider | Arti |
|-------|----------|------|
| `NoneType' object is not iterable` | `openai-codex` | OAuth tidak tersedia / Codex API tidak bisa diakses |
| `HTTP 401: User not found` | `openrouter` | API key expired atau salah |
| `HTTP 401: Authentication Fails, Your api key: **** is invalid` | `deepseek` | API key salah (bisa karena copy corrupted) |
| `Unknown provider 'X'` | any | Provider `X` tidak ada di plugin Hermes |
| `HTTP 400: Encrypted content ... not supported` | any | Model name tidak dikenal oleh API |

## Yang sering disalahpahami

| Yang diketik | Yang benar | Kenapa |
|-------------|-----------|--------|
| `provider: openai` | `provider: custom` + `base_url: https://api.openai.com/v1` | Provider `openai` tidak ada |
| `model: gpt-4.1-mini` | Verifikasi dulu via `/v1/models` | Bisa return 400 jika model tidak di-allow akun |
| `provider: google` | `provider: gemini` | Nama provider adalah `gemini` |
| `provider: claude` | `provider: anthropic` | Nama provider adalah `anthropic` |

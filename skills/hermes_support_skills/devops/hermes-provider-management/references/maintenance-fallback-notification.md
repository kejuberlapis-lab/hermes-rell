# Maintenance Fallback Notification Policy

## Auth Error → User-Friendly Message

When auth fails (token invalid/expired, unauthorized, forbidden) or callback API times out, replace the technical error with:

```
Sedang maintenance. Silakan coba beberapa saat lagi.
```

## Implementation rules
- Applies across all bots (global policy).
- Never show internal details: stack traces, endpoints, credential hints, tokens, or secrets to the user.
- Always log the full error detail internally for debugging.
- Retry internally 1-3× before showing the fallback message.
- For recurring issues, report concisely and request approval before major changes.

## Auth error diagnosis matrix

| Error message | Provider | Diagnosis | Fix |
|--------------|----------|-----------|-----|
| `NoneType' object is not iterable` | `openai-codex` | OAuth Codex not available; not a regular API key | Switch provider |
| `HTTP 401: User not found.` | `openrouter` | OpenRouter API key expired / invalid | Replace key or switch provider |
| `HTTP 401: Authentication Fails, Your api key: **** is invalid` | `deepseek` | Key corrupted during copy, or IP-restricted | Re-copy key via SCP script; test via curl from VPS |
| `Unknown provider 'X'` | any | Provider `X` not registered in Hermes | Check `ls ~/.hermes/hermes-agent/plugins/model-providers/` |
| `HTTP 400: Encrypted content not supported` | any | Model name unknown to API | Verify via endpoint `/v1/models` |

**Never display API keys or tokens causing the error to the user. Use generic descriptions only.**

# VPS Profile API Key Matrix

Generated via SSH audit of `~/.hermes/profiles/<profile>/.env` on VPS-Zeus (43.134.233.101).

Last updated: 2026-05-28

## hermes-support
```
MINIMAX_API_KEY=***
OPENROUTER_API_KEY=***
DEEPSEEK_API_KEY=***
GOOGLE_API_KEY=***
```
All providers available. MINIMAX and DEEPSEEK primary.

## profil-admin-mvp
```
DEEPSEEK_API_KEY=***
OPENAI_API_KEY=***
MINIMAX_API_KEY=***   # Added 2026-05-28
```
deepseek primary. MINIMAX available (key added 2026-05-28 but format may need validation).

## profil-admin-node-b
```
OPENROUTER_API_KEY=***
DEEPSEEK_API_KEY=***
OPENAI_API_KEY=***
```
deepseek + OPENROUTER. No MINIMAX.

## profil-admin-olo
```
DEEPSEEK_API_KEY=***
OPENAI_API_KEY=***
```
deepseek only. No MINIMAX. No OPENROUTER.

## profil-admin-plus
```
DEEPSEEK_API_KEY=***
OPENAI_API_KEY=***
```
deepseek only. No MINIMAX. No OPENROUTER.

## Local (.hermes/.env)
```
MINIMAX_API_KEY=***
DEEPSEEK_API_KEY=***
OPENROUTER_API_KEY=***
GOOGLE_API_KEY=***
OPENAI_API_KEY=***
```
All providers available. OAuth works for minimax (local only).

## Implication

When doing a cross-profile sync (all profiles same provider/model):
- **Use `deepseek` / `deepseek-v4-flash`** — it's the only key present in ALL 5 VPS profiles + local
- **NEVER** use `minimax` across all profiles — it's only in hermes-support + lokal + (tentative) profil-admin-mvp
- **NEVER** use `openrouter` on user instruction (permanent constraint)

## Audit Command
```bash
for profile in hermes-support profil-admin-mvp profil-admin-node-b profil-admin-olo profil-admin-plus; do
  echo "=== $profile ==="
  ssh ubuntu@43.134.233.101 "grep -v '^\s*$' ~/.hermes/profiles/$profile/.env 2>/dev/null | grep -E '(MINIMAX|DEEPSEEK|OPENROUTER|GOOGLE|OPENAI)_API_KEY' | sed 's/=.*/=***/g'"
done
```

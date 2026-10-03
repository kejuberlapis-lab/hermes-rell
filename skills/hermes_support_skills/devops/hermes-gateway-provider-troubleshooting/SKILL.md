---
name: hermes-gateway-provider-troubleshooting
description: Troubleshoot Hermes Gateway Telegram/provider authentication failures, OpenAI-compatible custom routers, profile-specific config, and polling conflicts without exposing secrets.
---

# Hermes Gateway Provider Troubleshooting

Use this skill when a Hermes Gateway platform such as Telegram is running but messages fail with provider authentication/configuration errors, unknown provider errors, OpenAI-compatible router issues, or repeated Telegram polling conflicts.

## Safety rules

- Never print Telegram bot tokens, OAuth tokens, API keys, bearer headers, `.env` contents, or `auth.json` secrets.
- When reading logs, always sanitize `Bearer ...`, `token=...`, `api_key=...`, bot-token shaped strings, passwords, and secrets before showing output.
- Prefer profile-scoped commands with `HERMES_HOME=/path/to/profile` when inspecting or changing a non-default profile.
- Treat raw HTTP/IP router endpoints as sensitive operational details; verify reachability, but do not store credentials.

## Diagnostic sequence

1. Confirm the active profile and service process.
   - Read the active profile marker if needed.
   - Check `systemctl --user status hermes-gateway.service --no-pager -l`.
   - Confirm the gateway command is `python -m hermes_cli.main gateway run --replace` and which profile logs it writes to.

2. Inspect the profile's model config.
   - Check `model.provider`, `model.base_url`, and `model.default` in the target profile's `config.yaml`.
   - For OpenAI-compatible custom routers, do not assume `provider: openai` exists in this Hermes install.
   - Run `hermes doctor` under the same `HERMES_HOME` to catch unknown providers, vendor-prefixed model mismatch, missing keys, or config migration warnings.

3. Read the gateway log around the failing Telegram message.
   - Look for `inbound message`, `Primary provider auth failed`, `Unknown provider`, `response ready`, `context-overflow`, and platform connection lines.
   - Distinguish provider failures from platform failures:
     - `telegram.error.InvalidToken` or `Unauthorized` during Telegram startup is a bot-token issue.
     - `Primary provider auth failed` or `Unknown provider` is an LLM provider/config issue.
     - `context-overflow failure` is not authentication; it may require session/context cleanup or a larger/low-context model choice.

4. Test the router directly before changing Hermes again.
   - Verify `/v1/models` returns model IDs.
   - Verify `/v1/chat/completions` with a small prompt and a low/fast model variant if available.
   - If direct router calls time out, reduce model cost/latency first before blaming Hermes.

5. Choose the right Hermes provider for the endpoint.
   - Use the bundled `custom` provider for arbitrary OpenAI-compatible endpoints when no fixed API-key environment variable should be required.
   - Avoid `openrouter` for a custom no-key router unless an `OPENROUTER_API_KEY` is intentionally configured; OpenRouter's provider profile declares `OPENROUTER_API_KEY`.
   - Avoid `openai` if the install reports `Unknown provider 'openai'`; this is configuration-invalid even if the endpoint is OpenAI-compatible.

6. Apply profile-scoped config and restart.
   - Example pattern:
     - `HERMES_HOME=/path/to/profile hermes config set model.provider custom`
     - `HERMES_HOME=/path/to/profile hermes config set model.base_url http://ROUTER/v1`
     - `HERMES_HOME=/path/to/profile hermes config set model.default MODEL_ID`
     - `systemctl --user restart hermes-gateway.service`
   - After restart, verify `Active profile: ...`, `Connected to Telegram`, `✓ telegram connected`, and `Gateway running with 1 platform(s)`.

7. Verify independently from Telegram.
   - Run Hermes one-shot with the same profile: `HERMES_HOME=/path/to/profile hermes -z 'Balas hanya: OK PROVIDER'`.
   - A successful one-shot proves the profile/provider/router path works outside the Telegram adapter.

## Telegram polling conflict pitfall

If logs repeatedly show:

`Conflict: terminated by other getUpdates request; make sure that only one bot instance is running`

then another process or host may be polling the same bot token. Check local processes first, but remember the duplicate poller can be on another server, terminal, or profile. This can make Telegram tests appear to use stale config because a different instance handles the user's message.

## Reference files

- `references/9router-custom-provider.md` — condensed session notes for configuring a no-key OpenAI-compatible router via Hermes `custom` provider and separating provider auth errors from Telegram polling conflicts.

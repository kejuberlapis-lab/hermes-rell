# 9router / custom provider notes

Session-derived pattern for Hermes Gateway provider-auth troubleshooting.

## Scenario

Telegram Gateway was connected, but user messages showed `provider authentication failed`. The target profile was `hermes-support`, and the desired router was an OpenAI-compatible endpoint at an IP-based `/v1` base URL.

## Observations

- `provider: openai` caused gateway log warnings like: `Primary provider auth failed: Unknown provider 'openai'`.
- `provider: openrouter` was recognized, but that provider profile declares `OPENROUTER_API_KEY`; it is not ideal for a custom no-key compatible router.
- The router itself was alive: `/v1/models` returned model IDs with a `cx/` prefix.
- Direct `/v1/chat/completions` succeeded with a smaller/fast model variant (`cx/gpt-5.3-codex-low`) and returned `OK`.
- Switching Hermes to `provider: custom` with the same base URL allowed `hermes -z 'Balas hanya: OK PROVIDER'` to succeed.
- A later Telegram send issue from the global `send_message` tool used different credentials and returned `Unauthorized`; that did not prove the profile gateway token was invalid.
- Repeated Telegram `getUpdates` conflict warnings indicated another poller may have been using the same bot token, which can make Telegram tests appear to hit stale config.

## Durable fix pattern

Use profile-scoped config:

```bash
HERMES_HOME=/path/to/profile hermes config set model.provider custom
HERMES_HOME=/path/to/profile hermes config set model.base_url http://ROUTER_HOST:PORT/v1
HERMES_HOME=/path/to/profile hermes config set model.default cx/gpt-5.3-codex-low
systemctl --user restart hermes-gateway.service
```

Then verify:

```bash
HERMES_HOME=/path/to/profile hermes -z 'Balas hanya: OK PROVIDER'
tail -n 100 /path/to/profile/logs/gateway.log
```

Expected gateway startup lines:

- `Active profile: <profile>`
- `Connected to Telegram (polling mode)`
- `✓ telegram connected`
- `Gateway running with 1 platform(s)`

## Sanitization reminder

When presenting logs, redact bot-token shaped strings, bearer headers, `api_key`, `token`, `secret`, and `password` values. Do not quote `.env` or `auth.json` secrets.

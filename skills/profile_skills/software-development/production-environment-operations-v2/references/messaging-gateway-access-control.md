# Messaging Gateway Access Control & Multi-Admin Administration

Operational guide for auditing, whitelisting, and managing authorized users across Hermes messaging gateways (Telegram, Discord, Slack) in multi-profile environments.

## 1. Access Audit Procedure

To inspect all inbound user interactions across profiles:
```python
import glob, re

users = set()
for log in glob.glob('/home/ubuntu/.hermes/profiles/*/logs/gateway.log'):
    with open(log, 'r', errors='ignore') as f:
        for line in f:
            if 'inbound message: platform=telegram' in line:
                m = re.search(r'user=(.*?) chat=([0-9]+)', line)
                if m:
                    users.add((m.group(1), m.group(2)))

for user, chat_id in sorted(users):
    print(f"User: {user} | Chat ID: {chat_id}")
```

## 2. Multi-Profile Whitelist Synchronization

When updating allowed administrators or users, ensure all active profile configs are updated in tandem to prevent bypasses or desynchronization across multiplexed sessions:

```python
import glob, yaml

configs = [
    '/home/ubuntu/.hermes/config.yaml',
    '/home/ubuntu/.hermes/profiles/profil-admin-mvp/config.yaml',
    '/home/ubuntu/.hermes/profiles/profil-admin-plus/config.yaml',
    '/home/ubuntu/.hermes/profiles/profil-admin-node-b/config.yaml',
    '/home/ubuntu/.hermes/profiles/profil-admin-olo/config.yaml',
    '/home/ubuntu/.hermes/profiles/hermes-support/config.yaml'
]

allowed_ids = ['<ADMIN_ID_1>', '<ADMIN_ID_2>', '<ADMIN_ID_3>']

for cfg_path in configs:
    with open(cfg_path, 'r') as f:
        data = yaml.safe_load(f) or {}
    if 'telegram' not in data or not isinstance(data['telegram'], dict):
        data['telegram'] = {}
    data['telegram']['allowed_chats'] = allowed_ids
    data['telegram']['allow_from'] = allowed_ids
    with open(cfg_path, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False)
```

## 3. Handling `/start` Platform Pings & New User Onboarding

- **Mechanism:** Hermes gateway treats bare Telegram `/start` commands as platform pings (`_hm_cmd_start` in `gateway/run_inbound.py`) and returns an empty string without invoking an LLM conversation turn (`Ignoring /start platform ping for session ...`).
- **Onboarding Rule:** When a newly whitelisted user reports no response after clicking "Start" in Telegram, instruct them to send a standard text message (e.g. "Halo", "Tes") to trigger conversation turn dispatch.

## 4. Multi-Instance Gateway Port Binding & Provider Isolation

When running multiple profile gateways concurrently on a single host (e.g. Master Admin bot + Public AI Tech Worker bot):
1. **Unique API Server Ports**: Each profile's `platforms.api_server.port` must be assigned an isolated port number (e.g. Profile A: `8642`, Profile B: `8644`) to prevent fatal `[Errno 98] Address already in use` startup exits.
2. **Authentic API Key Persistence**: When programmatically copying or updating `config.yaml` across profiles, always resolve the unmasked raw key from `~/.9router/db/data.sqlite` or `.env` rather than copying redacted display strings (`sk-6b7...b877`), which triggers `HTTP 401 Invalid API key` rejection on local LLM proxies.
3. **Public Gateway DM Policy**: To expose a commercial/worker bot to general users while keeping admin tools active, set `platforms.telegram.dm_policy: open` with omitted/wildcard `allow_from`.


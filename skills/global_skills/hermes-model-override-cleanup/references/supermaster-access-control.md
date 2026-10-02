# Super Master Access Control Configuration

## Overview

Configure Hermes Telegram bots so that:
- **All Telegram users** can chat with the bot
- **Only super masters** (2 specific user IDs) can approve system changes and make modifications

## Super Master User IDs

| User ID | Name | Role |
|---------|------|------|
| 661471478 | andi saputra | Super Master #1 |
| 5955713269 | avrell | Super Master #2 |

## Configuration Steps

### 1. Remove TELEGRAM_ALLOWED_USERS from .env

Comment out or remove the `TELEGRAM_ALLOWED_USERS` line from each profile's `.env` file (except `ais`):

```bash
# Comment out in each profile
sed -i 's/^TELEGRAM_ALLOWED_USERS=/# TELEGRAM_ALLOWED_USERS=/' ~/.hermes/profiles/<profile>/.env
```

### 2. Update config.yaml approvals

Set approval mode to require confirmation for destructive actions:

```yaml
approvals:
  mode: auto
  destructive_slash_confirm: true
  cron_mode: deny
  timeout: 60
```

### 3. Set telegram config

```yaml
telegram:
  allowed_chats: ''  # Empty = allow all
  require_mention: true
```

### 4. Restart gateway

```bash
systemctl --user restart hermes-gateway.service
```

## Access Levels

| Action | All Users | Super Masters |
|--------|-----------|---------------|
| Chat with bot | ✅ | ✅ |
| Ask questions | ✅ | ✅ |
| Use /model | ✅ | ✅ |
| /approve commands | ❌ | ✅ |
| System changes | ❌ | ✅ |
| Config modifications | ❌ | ✅ |

## Notes

- The `ais` profile should keep `TELEGRAM_ALLOWED_USERS` restricted as per original configuration
- Super master access is controlled by the `approvals.mode: auto` setting which requires confirmation for destructive commands
- The bot will auto-approve low-risk commands but prompt for high-risk ones
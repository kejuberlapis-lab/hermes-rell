---
name: hermes-configuration
description: Configure Hermes display, catalog, and behavior settings.
version: 1.0.0
author: Hermes Agent
license: MIT
category: devops
triggers:
  - hide tool output in chat
  - hide providers from model picker
  - configure display settings
  - set tool_progress
  - excluded_providers
  - discover_models
  - hermes config set
metadata:
  hermes:
    tags: [hermes, configuration, display, model-catalog, providers]
    related_skills: [hermes-provider-management, hermes-agent]
---

# Hermes Configuration

Umbrella skill for configuring Hermes Agent settings — display preferences, model catalog filtering, provider discovery, and behavior options.

## When to Use

- User wants to hide tool output from chat
- User wants to hide specific providers from model picker
- User wants to enable auto-discovery of models
- User wants to configure display settings
- User asks about `hermes config set` options

## 1. Display Settings

### Hide Tool Output in Chat

By default, Hermes shows tool execution output (terminal commands, search results, etc.) in the chat. To hide this:

```bash
hermes config set display.tool_progress none
```

**Options:**
- `all` — Show all tool output (default)
- `errors` — Show only errors
- `none` — Hide all tool output

**What's hidden:** Terminal output, search results, file operations, process output
**What's shown:** User messages, assistant responses, errors (if configured)

### Other Display Settings

```bash
# Streaming responses
hermes config set display.streaming true

# Timestamps
hermes config set display.timestamps false

# Show reasoning/thinking
hermes config set display.show_reasoning false

# Show cost
hermes config set display.show_cost false

# Compact mode
hermes config set display.compact false
```

## 2. Model Catalog Settings

### Hide Providers from Model Picker

To hide specific providers from the `/model` picker menu:

```bash
hermes config set model_catalog.excluded_providers '["openrouter","anthropic","gemini","xai","deepseek"]'
```

This hides listed providers from all `/model` picker surfaces:
- Gateway interactive/text pickers
- TUI picker
- CLI `hermes model` picker

**Use case:** When using a custom provider (like 9Router) and want to hide unused built-in providers.

### Disable Remote Model Catalog

To disable fetching model lists from remote manifest:

```bash
hermes config set model_catalog.enabled false
```

### Set Catalog TTL

To control how often the catalog refreshes:

```bash
hermes config set model_catalog.ttl_hours 1
```

## 3. Custom Provider Settings

### Auto-Discovery of Models

To auto-fetch models from a custom provider's API endpoint:

```bash
hermes config set custom_providers.0.discover_models true
```

This queries the `/v1/models` endpoint and populates the model list automatically, eliminating manual maintenance.

### Verify Configuration

```bash
# Check current config
hermes config get display.tool_progress
hermes config get model_catalog.excluded_providers
hermes config get custom_providers.0.discover_models

# Full config dump
hermes config get display
hermes config get model_catalog
hermes config get custom_providers
```

## 4. Troubleshooting

### Config Changes Not Applied

**Symptom:** Changes to config.yaml don't take effect in Telegram/chat.

**Fix:** Restart the gateway:
```bash
hermes gateway restart
```

Or from Telegram: `/restart`

### Provider Still Showing Despite excluded_providers

**Symptom:** Provider appears in `/model` picker even after adding to `excluded_providers`.

**Check:**
1. Verify config saved: `hermes config get model_catalog.excluded_providers`
2. Gateway restarted after change
3. Provider name matches exactly (case-insensitive)

### Tool Output Still Showing

**Symptom:** Tool output appears despite `display.tool_progress: none`.

**Check:**
1. Verify config: `hermes config get display.tool_progress`
2. Gateway restarted
3. Session reset (`/reset` in Telegram)

## 5. Common Config Patterns

### Minimal Custom Provider Setup

```bash
# Set provider
hermes config set model.provider custom
hermes config set model.base_url http://localhost:20128/v1
hermes config set model.default xmtp/mimo-v2.5

# Enable auto-discovery
hermes config set custom_providers.0.discover_models true

# Hide unused providers
hermes config set model_catalog.excluded_providers '["openrouter","anthropic","gemini","xai","deepseek","nous","copilot"]'

# Hide tool output (optional)
hermes config set display.tool_progress none

# Restart gateway
hermes gateway restart
```

### Clean Model Picker

```bash
# Only show specific providers
hermes config set model_catalog.excluded_providers '["openrouter","anthropic","gemini","xai","deepseek","nous","copilot","openai-codex","minimax","zai","alibaba","xiaomi","huggingface","fireworks","novita","nvidia","deepinfra","gmi","arcee","stepfun","upstage","kilocode","ai-gateway","ollama-cloud","azure-foundry","bedrock","vertex","qwen-oauth","minimax-cn","kimi-coding","kimi-coding-cn","meta-ai","commandcode","actual"]'

# Restart
hermes gateway restart
```

## References

- Hermes docs: https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- Model Catalog: https://hermes-agent.nousresearch.com/docs/reference/model-catalog

# Telegram First Message Delivery

## When to use
- Sending a first greeting/initial message to a new Telegram ID.
- Multiple bot profiles exist and the target profile is unclear.
- Validating why delivery fails when the ID appears registered.

## Workflow
1. Identify target bot profile: `~/.hermes/profiles/<profile-name>/`
2. Verify the user's allowlist status per profile from `.env` without displaying raw values.
3. Extract the bot token for internal execution only; never display the token.
4. Ensure the user has started the bot — Telegram API returns `chat not found` if they haven't.
5. Send the message only when explicitly instructed by the user for that specific target.
6. Record a safe outcome: success/fail, profile, general reason, without token/secret.

## Prohibitions
- Never send DMs to Telegram IDs without explicit instruction.
- Never display bot tokens, full allowlists, or unnecessary personal data.

---
name: buatqris-payment-gateway-integration
description: "Use when integrating BuatQris QRIS payments and webhooks."
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [qris, payment-gateway, buatqris, webhook, hmac-sha256, saas, telegram-bots, fastapi, python, paywall]
---

# BuatQris Payment Gateway Integration & Dynamic QRIS Automation

A class-level operational guide for integrating the **BuatQris Open API** (`https://api.buatqris.site`) into SaaS platforms, Telegram bots, and backend applications for automated dynamic QRIS generation, secure webhook callback processing, signature verification, micro-trial activations, web-to-bot transaction binding, and quota fulfillment.

## When to Use

- When building automated paywalls, instant subscription checkouts, or coin/token top-ups via dynamic QRIS in Indonesia.
- When connecting Python/FastAPI, Node.js, PHP, or Go backends to the BuatQris Open API platform.
- When implementing HMAC-SHA256 signature verification on raw request bodies to block forged payment notifications.
- When configuring merchant requirements (Website / Link Usaha, Account ID, Secret Token, Signing Secret).
- When implementing automated Telegram bot paywalls, micro-transaction trial verifications (Rp 1.000 minimum), and deep-linked transaction claiming.
- When testing end-to-end payment workflows using Sandbox mode (`test=1`) without real money.

## Core API Characteristics

- **Base URL:** `https://api.buatqris.site`
- **HTTP Method:** `POST`
- **Content-Type:** `application/x-www-form-urlencoded`
- **Response Format:** `application/json` (UTF-8)
- **Minimum Nominal:** `Rp 1.000` (enforced by BuatQris engine; sub-Rp 1.000 amounts fail).
- **Single-Endpoint Architecture:** All actions call the single Base URL and are routed via the `action` form field (e.g. `action=api_create_qris`, `action=api_check_status`, `action=api_withdraw`).

## Procedure

1. **Kredensial & Environment Provisioning:**
   - Obtain credentials from BuatQris Dashboard $\rightarrow$ **Open API**:
     - `BUATQRIS_ACCOUNT_ID`: Merchant account ID string.
     - `BUATQRIS_SECRET_TOKEN`: Secret key starting with `sk_live_...` (min 20 chars).
     - `BUATQRIS_SIGNING_SECRET`: Secret key used specifically for webhook signature verification (`whsec_...`).
   - Store all credentials strictly in `.env` with `chmod 600`; never expose them in frontend code or public repositories.

2. **Generating Dynamic QRIS (`action=api_create_qris`):**
   - Send `POST` with `Content-Type: application/x-www-form-urlencoded` and a standard browser `User-Agent`:
     ```python
     import httpx

     async def create_dynamic_qris(account_id: str, secret_token: str, amount: int, description: str, is_sandbox: bool = False):
         payload = {
             "action": "api_create_qris",
             "account_id": account_id,
             "secret_token": secret_token,
             "amount": str(amount),
             "description": description[:100],
             "fee_by": "user" # or "buyer"
         }
         if is_sandbox:
             payload["test"] = "1"

         headers = {
             "Content-Type": "application/x-www-form-urlencoded",
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
         }
         async with httpx.AsyncClient() as client:
             res = await client.post("https://api.buatqris.site", data=payload, headers=headers, timeout=12.0)
             return res.json()
     ```
   - **Handling the Response:**
     - Extract `data.qr_url` (PNG URL) or `data.qris_image` (base64 PNG) to display the QR image to the user.
     - Always display `data.total_amount` (which includes the unique nominal code `amount_uniq`), not the raw `amount`.
     - Capture `data.transaction_id` and `data.expired_at` for database tracking.

3. **Web-to-Telegram Deep-Linking & Transaction Binding:**
   - When generating QRIS on the web frontend modal, dynamically update the Telegram button URL to:
     `https://t.me/<bot_username>?start=trx_<transaction_id>`
   - When the user clicks the button, Telegram sends `/start trx_<transaction_id>`.
   - In the bot gateway bridge:
     - Extract `transaction_id` from the command argument.
     - Update the `telegram_id` column in the database `transactions` record to bind the order to that user.
     - If the transaction is pending, reply with the order summary and local QR image.
     - **Post-Payment Claim Gate:** If the user already paid before opening Telegram, detect `status == 'success'` and immediately credit the tokens to their user record.

4. **Micro-Payment Trial Verification Pattern (Rp 1.000 Minimum):**
   - When offering a "Free Trial" that requires account verification or anti-spam gating, create a micro-invoice with `amount=1000`.
   - The user pays `Rp 1.000 + amount_uniq` (e.g. Rp 1.079).
   - Upon receiving `payment.success` webhook, immediately credit free trial quota (e.g. 8 tasks) into the database and notify the user on Telegram.

5. **Telegram Bot Gateway Native Photo Delivery:**
   - To send QRIS barcodes natively as photo bubbles in Telegram:
     - Download the QR image from `qr_url` to a local scratch path (e.g. `/tmp/qris_<trx_id>.png`).
     - Prepend `MEDIA:/tmp/qris_<trx_id>.png\n\n` to the response markdown.
     - The Telegram adapter automatically dispatches it as a native photo attachment.

6. **Processing Inbound Webhooks (`POST /api/payment/webhook`):**
   - **Header Inspection:**
     - `X-BuatQris-Event`: e.g. `payment.success`, `payment.expired`, `payment.failed`.
     - `X-BuatQris-Signature`: Format `sha256=<hex_digest>`.
     - `X-BuatQris-Delivery`: `transaction_id`.
   - **Mandatory HMAC-SHA256 Raw Body Verification:**
     ```python
     import hmac
     import hashlib

     def verify_signature(raw_body: bytes, incoming_header: str, signing_secret: str) -> bool:
         calc = "sha256=" + hmac.new(
             signing_secret.encode("utf-8"),
             raw_body,
             hashlib.sha256
         ).hexdigest()
         return hmac.compare_digest(calc, incoming_header or "")
     ```
   - **Fast Response Gate (<6 Seconds):** Return HTTP 200 immediately to prevent BuatQris automated retry loops (0.3s delay retry on non-2xx).
   - **Idempotency Guard:** If `transaction.status == 'success'`, return `{"status": "already_processed"}` without re-crediting quota.

7. **Merchant Website / Link Usaha Requirement:**
   - BuatQris requires a valid URL in **Profil $\rightarrow$ Website / Link Usaha**.
   - Deploy a clean multi-page application with anti-cache headers (`Cache-Control: no-cache, no-store, must-revalidate`), segmented dock navbar, and responsive mobile quick pills.

## Pitfalls

- **Default Python User-Agent Blocking (HTTP 403 Forbidden):** Python's default `urllib` user agent (`Python-urllib/3.x`) is blocked by BuatQris API security filters. Always send a standard browser `User-Agent` header with every request.
- **Unbound Website Transactions:** Generating QRIS on a website without a deep-link transaction parameter (`?start=trx_<ID>`) results in orphaned payments where the bot cannot identify which Telegram account purchased the tokens.
- **Enforcing Amounts Under Rp 1.000:** Attempting to create a QRIS for Rp 1 or Rp 500 fails because BuatQris enforces a minimum base amount of Rp 1.000. Use Rp 1.000 for trial verification checkouts.
- **Sending JSON Payloads to Create QRIS:** BuatQris strictly expects `application/x-www-form-urlencoded`. Sending `application/json` causes parameter parsing errors or silent failures.
- **Relying on Raw QR String (`qris_string`):** `qris_string`, `qris_url`, and `direct_url` are intentionally returned as `null` by the provider for security. Always use `qr_url` or `qris_image` to present the QR code.
- **Parsing Body Before Signature Check:** Verifying HMAC on JSON-decoded or re-serialized strings fails due to key ordering and whitespace discrepancies. Always compute HMAC over the untouched `raw_body` bytes.
- **Matching Base Amount Instead of Total Amount:** Failing to verify `total_amount` (which includes unique 3-digit suffix) causes reconciliation mismatches against bank settlements.
- **Polling Status Aggressively (HTTP 429 Rate Limit):** `action=api_check_status` is hard-limited to 1 request per 20 seconds per transaction. Rely primarily on webhooks rather than client-side polling loops.
- **Hermes Gateway `/start` Platform Ping Interception:** Default gateway dispatch drops bare `/start` commands as empty platform pings. Dispatchers must allow `/start` to fall through to the bridge handler so paywalls and onboarding flows can execute.

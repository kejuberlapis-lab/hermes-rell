---
name: buatqris-payment-gateway-integration
description: "Use when integrating BuatQris QRIS payments and webhooks."
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [qris, payment-gateway, buatqris, webhook, hmac-sha256, saas, telegram-bots, fastapi, python, paywall]
---

# BuatQris Payment Gateway Integration & Dynamic QRIS Automation

A class-level operational guide for integrating the **BuatQris Open API** (`https://api.buatqris.site`) into SaaS platforms, Telegram bots, and backend applications for automated dynamic QRIS generation, secure webhook callback processing, signature verification, micro-trial activations, and quota fulfillment.

## When to Use

- When building automated paywalls, instant subscription checkouts, or coin/token top-ups via dynamic QRIS in Indonesia.
- When connecting Python/FastAPI, Node.js, PHP, or Go backends to the BuatQris Open API platform.
- When implementing HMAC-SHA256 signature verification on raw request bodies to block forged payment notifications.
- When configuring merchant requirements (Website / Link Usaha, Account ID, Secret Token, Signing Secret).
- When implementing automated Telegram bot paywalls and micro-transaction trial verifications (Rp 1.000 minimum).
- When reconciling transaction status on demand (`action=api_check_status`) upon receiving payment receipts or manual confirmation claims.

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
     - `BUATQRIS_SIGNING_SECRET`: Secret key used specifically for webhook signature verification.
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

3. **Reconciling Status on Demand (`action=api_check_status`):**
   - When a user claims payment ("Sudah bayar", sending receipt image) or during account verification checks, query transaction status directly:
     ```python
     import httpx

     def check_qris_status(account_id: str, secret_token: str, transaction_id: str):
         payload = {
             "action": "api_check_status",
             "account_id": account_id,
             "secret_token": secret_token,
             "transaction_id": transaction_id
         }
         headers = {
             "Content-Type": "application/x-www-form-urlencoded",
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
         }
         res = httpx.post("https://api.buatqris.site", data=payload, headers=headers, timeout=15.0)
         data = res.json()
         if data.get("success") and data.get("data", {}).get("status") == "success":
             return True, data["data"]
         return False, data
     ```

4. **Micro-Payment Trial Verification Pattern (Rp 1.000 Minimum):**
   - When offering a "Free Trial" that requires account verification or payment gateway testing, create a micro-invoice with `amount=1000`.
   - The user pays `Rp 1.000 + amount_uniq` (e.g. Rp 1.040).
   - Upon receiving `payment.success` webhook or status check confirmation, immediately credit free trial quota (e.g. 8 tasks) into the database and notify the user on Telegram.

5. **Telegram Bot `/start` Paywall & Gateway Integration:**
   - In Hermes multi-profile Telegram gateways, raw `/start` platform pings must fall through to the agent turn loop (`return False, None` in `gateway/run_inbound.py::_hm_cmd_start`).
   - When a user sends `/start`:
     - Query user status via billing CLI/database.
     - If unverified or tokens == 0, generate dynamic QRIS and send the image markdown `![QRIS Aktivasi](<qr_url>)` with the exact `total_amount` and expiration timer.
     - Once verified via webhook or status reconciliation, the bot deducts 1 token per completed task.

6. **Processing Inbound Webhooks (`POST /api/payment/webhook`):**
   - **Header Inspection:** Check `X-BuatQris-Signature` / `X-Signature` (case-insensitive).
   - **Mandatory HMAC-SHA256 Raw Body Verification:** Compare both raw hex digest and `sha256=<hex>` prefix:
     ```python
     import hmac
     import hashlib

     def verify_signature(raw_body: bytes, incoming_header: str, signing_secret: str) -> bool:
         raw_digest = hmac.new(
             signing_secret.encode("utf-8"),
             raw_body,
             hashlib.sha256
         ).hexdigest()
         return (
             hmac.compare_digest(incoming_header or "", raw_digest)
             or hmac.compare_digest(incoming_header or "", f"sha256={raw_digest}")
         )
     ```
   - **Robust Payload Unpacking:** Extract fields supporting both flat and nested keys (`payload.get("transaction_id") or payload.get("data", {}).get("transaction_id")`).
   - **Fast Response Gate (<6 Seconds):** Return HTTP 200 immediately to prevent BuatQris automated retry loops (0.3s delay retry on non-2xx).
   - **Idempotency Guard:** If `transaction.status == 'success'`, return `{"status": "already_processed"}` without re-crediting quota.

7. **Merchant Website / Link Usaha Requirement:**
   - BuatQris requires a valid URL in **Profil $\rightarrow$ Website / Link Usaha**.
   - Deploy a clean multi-page application with anti-cache headers (`Cache-Control: no-cache, no-store, must-revalidate`), segmented dock navbar, and responsive mobile quick pills.

## Pitfalls

- **Sending JSON Payloads to Status/Create API:** BuatQris strictly expects `application/x-www-form-urlencoded` with form fields (`action`, `account_id`, `secret_token`). Sending JSON payloads results in HTTP 400 (`account_id dan secret_token wajib diisi`).
- **Default Python User-Agent Blocking (HTTP 403 Forbidden):** Python's default `urllib` user agent (`Python-urllib/3.x`) is blocked by BuatQris API security filters. Always send a standard browser `User-Agent` header with every request.
- **Enforcing Amounts Under Rp 1.000:** Attempting to create a QRIS for Rp 1 or Rp 500 fails because BuatQris enforces a minimum base amount of Rp 1.000. Use Rp 1.000 for trial verification checkouts.
- **Sending JSON Payloads to Create QRIS:** BuatQris strictly expects `application/x-www-form-urlencoded`. Sending `application/json` causes parameter parsing errors or silent failures.
- **Relying on Raw QR String (`qris_string`):** `qris_string`, `qris_url`, and `direct_url` are intentionally returned as `null` by the provider for security. Always use `qr_url` or `qris_image` to present the QR code.
- **Parsing Body Before Signature Check:** Verifying HMAC on JSON-decoded or re-serialized strings fails due to key ordering and whitespace discrepancies. Always compute HMAC over the untouched `raw_body` bytes.
- **Matching Base Amount Instead of Total Amount:** Failing to verify `total_amount` (which includes unique 3-digit suffix) causes reconciliation mismatches against bank settlements.
- **Polling Status Aggressively (HTTP 429 Rate Limit):** `action=api_check_status` is hard-limited to 1 request per 20 seconds per transaction. Rely primarily on webhooks rather than client-side polling loops.
- **Hermes Gateway `/start` Platform Ping Interception:** Default gateway dispatch drops bare `/start` commands as empty platform pings. Dispatchers must allow `/start` to fall through to the agent turn loop so paywalls and onboarding flows can execute.

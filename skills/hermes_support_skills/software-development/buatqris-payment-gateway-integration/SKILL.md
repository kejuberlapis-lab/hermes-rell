---
name: buatqris-payment-gateway-integration
description: Use when integrating BuatQris QRIS payments and webhooks.
version: 1.4.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [qris, payment-gateway, buatqris, webhook, hmac-sha256, saas, telegram-bots, fastapi, python, paywall]
---

# BuatQris Payment Gateway Integration & Dynamic QRIS Automation

A class-level operational guide for integrating the **BuatQris Open API** (`https://api.buatqris.site`) into SaaS platforms, Telegram bots, and backend applications for automated dynamic QRIS generation, secure webhook callback processing, signature verification, micro-trial activations, web-to-bot transaction binding, quota fulfillment, and instant push notification delivery.

## When to Use

- When building automated paywalls, instant subscription checkouts, or coin/token top-ups via dynamic QRIS in Indonesia.
- When connecting Python/FastAPI, Node.js, PHP, or Go backends to the BuatQris Open API platform.
- When implementing HMAC-SHA256 signature verification on raw request bodies to block forged payment notifications.
- When configuring merchant requirements (Website / Link Usaha, Account ID, Secret Token, Signing Secret).
- When implementing automated Telegram bot paywalls, micro-transaction trial verifications (Rp 1.000 minimum), and deep-linked transaction claiming.
- When setting up instant post-payment Telegram push notifications to prompt immediate user activation.

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

4. **Micro-Payment Trial Verification & Purchase Capping Pattern (Rp 1.000 Minimum):**
   - When offering an intro trial that requires commitment or anti-spam gating, create a micro-invoice with `amount=1000` (e.g. "Lihat Bagaimana Virtual Tech Worker Bekerja").
   - **Strict Per-User Purchase Quota (Max 2x):**
     - Enforce a hard ceiling on trial purchases per unique `telegram_id` (e.g. max 2 trial transactions with `status in ('success', 'paid')`).
     - If the user attempts a 3rd trial purchase, reject with HTTP 400 and provide a structured upsell response directing them to the primary entry plan (e.g. Starter Tier).
     - Provide an interactive client-side confirmation in the web modal so the user can transition directly to the Starter checkout in one click.
   - Upon receiving `payment.success` webhook, immediately credit quota (e.g. 8 tokens) into the database and notify the user on Telegram.

5. **Operational Dashboard & Timezone Localization (WIB / Asia/Jakarta):**
   - Databases typically persist transaction timestamps in naive UTC (`datetime.utcnow()`).
   - When returning transaction lists and user logs to Indonesian administrative consoles or executive dashboards, always offset UTC timestamps by $+7\text{ hours}$ (`Asia/Jakarta` / WIB) and explicitly label table headers with `(WIB)`.
   - Prevent displaying raw UTC strings (which appear 7 hours behind real local time) to ensure customer trust during settlement audits.

6. **Telegram Bot Gateway Native Photo Delivery:**
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
   - **Fast Response Gate (<6 Seconds):** Return HTTP 200 immediately to prevent BuatQris automated retry loops.
   - **Idempotency Guard:** If `transaction.status == 'success'`, return `{"status": "already_processed"}` without re-crediting quota.

7. **Automated Instant Push Notification & Activation Invitation:**
   - When payment succeeds, immediately invoke Telegram Bot API (`sendMessage`) with parsed HTML markup:
     ```python
     notification_text = (
         f"🎉 <b>PEMBAYARAN BERHASIL DIVERIFIKASI!</b>\n\n"
         f"Halo! Pembayaran QRIS Anda sebesar <b>Rp {total_paid}</b> telah kami terima dan diverifikasi secara otomatis.\n\n"
         f"📋 <b>Detail Akun & Kuota Anda:</b>\n"
         f"• <b>Paket Langganan:</b> {tier_title}\n"
         f"• <b>Kuota Tugas:</b> {tokens_cnt} Token Eksekusi\n"
         f"• <b>Status Akun:</b> 🟢 Aktif & Siap Bekerja\n\n"
         f"🤖 <b>Silakan Mulai Menggunakan Saya Sekarang!</b>\n"
         f"Saya adalah AI Tech Worker Anda. Anda bisa langsung memberikan instruksi pekerjaan teknis apa pun di sini, ketikkan tugas atau pertanyaan pertama Anda sekarang untuk langsung saya eksekusi!"
     )
     ```
   - Use automatic fallback to plain text if markup entity parsing fails.

8. **Automated Instant Push Notification & Activation Invitation:**
   - When payment succeeds, immediately invoke Telegram Bot API (`sendMessage`) with parsed HTML markup:
     ```python
     notification_text = (
         f"🎉 <b>PEMBAYARAN BERHASIL DIVERIFIKASI!</b>\n\n"
         f"Halo! Pembayaran QRIS Anda sebesar <b>Rp {total_paid}</b> telah kami terima dan diverifikasi secara otomatis.\n\n"
         f"📋 <b>Detail Akun & Kuota Anda:</b>\n"
         f"• <b>Paket Langganan:</b> {tier_title}\n"
         f"• <b>Kuota Tugas:</b> {tokens_cnt} Token Eksekusi\n"
         f"• <b>Status Akun:</b> 🟢 Aktif & Siap Bekerja\n\n"
         f"🤖 <b>Silakan Mulai Menggunakan Saya Sekarang!</b>\n"
         f"Saya adalah AI Tech Worker Anda. Anda bisa langsung memberikan instruksi pekerjaan teknis apa pun di sini, ketikkan tugas atau pertanyaan pertama Anda sekarang untuk langsung saya eksekusi!"
     )
     ```
   - Use automatic fallback to plain text if markup entity parsing fails.

9. **Abandoned Pending Transaction Auto-Expiry Sweeper (15–30 Minutes):**
   - When users generate a QRIS (via web modal or `/start` bot) but abandon checkout without paying, the gateway expires the invoice on bank rails after 15–30 minutes but does NOT send webhooks for offline/unpaid expirations.
   - Implement an automated sweeper in `/api/payment/check/{transaction_id}`, `/api/admin/metrics`, and `cli_billing.py` to automatically update transactions where `status == 'pending'` and `(now_utc - created_at) > 900s (15m)` to `status = 'expired'`.
   - On every `/start` command or user check, auto-expire prior pending records for that user so dangling pending invoices never linger.
   - If a user opens an expired Telegram deep-link (`trx_...`), reject immediately with an explicit expiration prompt rather than serving a stale QR code.

10. **Clear Status Badging in Administrative & Executive Dashboards:**
   - In user management tables, never label unverified/unpaid users (0 tokens) with ambiguous labels like `REGISTERED` (which implies active membership).
   - Use distinct, unambiguous badges:
     - `BELUM BAYAR` (Amber badge) $\rightarrow$ `UNVERIFIED` tier, 0 tokens.
     - `FREE TRIAL (AKTIF)` (Emerald badge) $\rightarrow$ `TRIAL` tier, 8 tokens active.
     - `STARTER / ADVANCE / PRO (AKTIF)` (Blue/Indigo/Purple badges) $\rightarrow$ Paid active tiers.

## Pitfalls

- **Leaving Expired Transactions in Pending State:** Without an auto-expiry sweeper on transactions older than 15 minutes, abandoned invoices permanently accumulate as `pending`, misleading administrative dashboards into reporting phantom pending revenue and leaving users confused with stale QR codes.
- **Stacking Multiple Pending Invoices for One User:** Failing to expire prior pending transactions when issuing a new `/start` invoice creates duplicate pending records for the same account. Always expire older pending rows for that `telegram_id` before inserting a new one.
- **Serving Stale QRIS on Expired Deep-Links:** When a user opens a Telegram transaction deep-link (`trx_...`) after 15 minutes, serving the old QRIS leads to payment failures or uncredited transfers. Check timestamp and reject with an explicit expiration prompt immediately.
- **Ambiguous Status Labels in Dashboards:** Labeling unpaid leads as "REGISTERED" creates stakeholder confusion regarding active customer counts versus unpaid abandoned checkouts. Always use clear, explicit status indicators.
- **Default Python User-Agent Blocking (HTTP 403 Forbidden):** Python's default `urllib` user agent (`Python-urllib/3.x`) is blocked by BuatQris API security filters. Always send a standard browser `User-Agent` header with every request.
- **Unbound Website Transactions:** Generating QRIS on a website without a deep-link transaction parameter (`?start=trx_<ID>`) results in orphaned payments where the bot cannot identify which Telegram account purchased the tokens.
- **Enforcing Amounts Under Rp 1.000:** Attempting to create a QRIS for Rp 1 or Rp 500 fails because BuatQris enforces a minimum base amount of Rp 1.000. Use Rp 1.000 for trial verification checkouts.
- **Sending JSON Payloads to Create QRIS:** BuatQris strictly expects `application/x-www-form-urlencoded`. Sending `application/json` causes parameter parsing errors or silent failures.
- **Relying on Raw QR String (`qris_string`):** `qris_string`, `qris_url`, and `direct_url` are intentionally returned as `null` by the provider for security. Always use `qr_url` or `qris_image` to present the QR code.
- **Parsing Body Before Signature Check:** Verifying HMAC on JSON-decoded or re-serialized strings fails due to key ordering and whitespace discrepancies. Always compute HMAC over the untouched `raw_body` bytes.
- **Matching Base Amount Instead of Total Amount:** Failing to verify `total_amount` (which includes unique 3-digit suffix) causes reconciliation mismatches against bank settlements.
- **Polling Status Aggressively (HTTP 429 Rate Limit):** `action=api_check_status` is hard-limited to 1 request per 20 seconds per transaction. Rely primarily on webhooks rather than client-side polling loops.
- **Invoice Timeout vs Failure:** Invoices expire in 15–30 minutes if unpaid. Expired status is expected timeout lifecycle behavior, not an infrastructure defect.
- **Vendor & Gateway White-Labeling Discipline:** Never expose gateway vendor brand names (e.g., "Powered by BuatQris") in public customer-facing footers or UI copy unless legally required. Preserve pure platform brand equity by using neutral terminology (e.g., "Dynamic QRIS · Auto-Settlement").
- **Action CTA over Raw Bot Handles:** Display high-converting actionable callout badges (e.g., `Mulai Kerja di Telegram →`) on the frontend rather than raw bot usernames (`@Olo_SBT_bot`) to elevate professional trust and streamline onboarding.

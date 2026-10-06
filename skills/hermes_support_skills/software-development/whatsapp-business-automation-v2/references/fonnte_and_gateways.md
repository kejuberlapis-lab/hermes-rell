# Fonnte WhatsApp Gateway & Webhook Integration Reference

## 1. Fonnte Architecture & Core Settings

Fonnte (`fonnte.com`) is a third-party WhatsApp gateway that provides REST APIs and Webhooks to send and receive WhatsApp messages without managing headless browser/socket daemons locally.

### Key API Endpoints
- **Device Status:** `POST https://api.fonnte.com/device` (Requires `Authorization: <TOKEN>`)
- **Get QR Code:** `POST https://api.fonnte.com/qr` (Returns base64 encoded QR image)
- **Send Outbound Message:** `POST https://api.fonnte.com/send` (Payload: `target`, `message`, `delay`, `typing`)

---

## 2. Inbound Webhook Execution Pattern

When using custom webhook handlers (e.g. `https://domain.com/api/fonnte_webhook.php`):

1. **Mandatory Setting: "Autoread = ON":**
   In the Fonnte web dashboard (**Device ➔ Edit**), the **Autoread** toggle MUST be switched to **ON**. If Autoread is OFF, Fonnte drops inbound webhook events and will NOT forward messages to your server.

2. **Dual-Response Mechanism:**
   Fonnte supports returning replies directly as JSON:
   ```json
   {
     "reply": "Message content",
     "data": [
       {"target": "628123456789", "message": "Message content"}
     ]
   }
   ```
   To guarantee delivery across network variations, the webhook script should also execute a secondary cURL call to `https://api.fonnte.com/send`.

---

## 3. Native Dashboard Autoreply

- Fonnte does not support inserting or modifying autoreply rules via standard device API tokens (API calls to `/autoreply` return `{'reason': 'unknown user'}`).
- Autoreply rules must be configured in the Fonnte web UI under **Autoreply ➔ + Add Autoreply**.
- Keywords can be multiline (1 keyword per line) with matching modes:
  - `Equal`: for exact single-digit menu selections (`1`, `2`, `3`).
  - `Contains`: for conversational trigger words (`halo`, `hi`, `p`, `menu`, `info`).

---

## 4. Critical Testing Pitfall: Self-Chat Ignore

- **Symptom:** Sending a WhatsApp message to the connected device number yields no response, and server logs show no incoming webhook hits.
- **Root Cause:** WhatsApp and gateway engines systematically filter out messages originating from the same account (`fromMe: true` / self-messages) to prevent infinite auto-reply loops.
- **Rule:** Always conduct end-to-end bot testing using a separate, distinct WhatsApp phone number.

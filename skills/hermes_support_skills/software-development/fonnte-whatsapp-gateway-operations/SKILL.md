---
name: fonnte-whatsapp-gateway-operations
description: "Use when integrating Fonnte WhatsApp Gateway API & Webhook."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [fonnte, whatsapp, webhook, gateway, autoreply, lead-capture]
    related_skills: [whatsapp-business-automation-v2, production-environment-operations]
---

# Fonnte WhatsApp Gateway & Webhook Integration Operations

A class-level operational skill for configuring, deploying, and troubleshooting third-party WhatsApp Gateway APIs via Fonnte (`fonnte.com`), handling dynamic webhook execution, native autoreply rules, and preventing common signal collision loops.

## When to Use

- When connecting business WhatsApp numbers to third-party REST/Webhook gateways (Fonnte) without hosting local socket daemons.
- When configuring inbound webhook endpoints (`/api/fonnte_webhook.php`) to dynamically process incoming customer messages and dispatch replies.
- When debugging non-responsive chatbots on Fonnte (autoread issues, webhook URL mismatches, or self-message ignore loops).
- When structuring multi-tier conversational menus, product catalogs, and sales lead qualification forms.

## Procedure

1. **Device Connection & Token Verification:**
   - Verify connection status via API: `POST https://api.fonnte.com/device` with `Authorization: <TOKEN>`.
   - Ensure device state is `connect` (`status: true`).
   - If disconnected, obtain QR barcode via `POST https://api.fonnte.com/qr` (returns base64 PNG) or use pairing code in Fonnte UI.

2. **Webhook Endpoint Architecture:**
   - Deploy standard PHP webhook receiving JSON payload via `php://input`:
     ```php
     <?php
     header('Content-Type: application/json; charset=utf-8');
     $json = file_get_contents('php://input');
     $data = json_decode($json, true);

     if (empty($data)) {
         echo json_encode(['status' => 'online', 'service' => 'WhatsApp Bot']);
         exit;
     }

     $sender  = isset($data['sender']) ? $data['sender'] : '';
     $message = isset($data['message']) ? trim($data['message']) : '';
     $name    = isset($data['name']) ? trim($data['name']) : 'Pelanggan';

     function sendFonnte($target, $replyData) {
         $curl = curl_init();
         curl_setopt_array($curl, [
             CURLOPT_URL => "https://api.fonnte.com/send",
             CURLOPT_RETURNTRANSFER => true,
             CURLOPT_TIMEOUT => 15,
             CURLOPT_CUSTOMREQUEST => "POST",
             CURLOPT_POSTFIELDS => [
                 'target' => $target,
                 'message' => $replyData['message'],
                 'countryCode' => '62'
             ],
             CURLOPT_HTTPHEADER => ["Authorization: YOUR_TOKEN"]
         ]);
         $res = curl_exec($curl);
         curl_close($curl);
         return $res;
     }

     // Match message and dispatch reply
     $reply = ['message' => 'Your reply text'];
     sendFonnte($sender, $reply);
     ```

3. **Dashboard Configuration & Mandatory Settings:**
   - In Fonnte (**Device ➔ Edit**):
     - **Autoread Toggle:** MUST be set to **ON**. If OFF, Fonnte silently discards webhook dispatches.
     - **Webhook URL (Primary):** Input public HTTPS URL (e.g. `https://mitsindo.co.id/api/fonnte_webhook.php`).
     - **Secondary Webhooks (`Webhook Connect`, `Webhook Message Status`, `Webhook Chaining`):** MUST be left **EMPTY**.

4. **Testing Protocol:**
   - Never test by messaging the connected WhatsApp number from itself.
   - Always send test triggers (`Halo`, `1`, `Menu`) from an independent secondary WhatsApp account.

## Pitfalls

- **Multi-Webhook Field Duplication:** Filling all 4 webhook inputs (`Webhook`, `Webhook Connect`, `Webhook Message Status`, `Webhook Chaining`) with the same script URL causes delivery status callbacks (`status=sent/delivered`) to be treated as inbound user messages, creating infinite parsing loops. Only populate the primary `Webhook` field.
- **Autoread Disabled:** If `Autoread` is set to OFF, incoming messages will not trigger webhook dispatches regardless of valid URL and token configuration.
- **Self-Message Filtering:** Testing from the connected device number to itself will yield no reply because WhatsApp and Fonnte discard `fromMe: true` messages to avoid infinite self-reply loops.
- **Response Source Precedence:** In Fonnte device settings, `Response Source = Autoreply` prioritizes dashboard-configured autoreply rules. If using webhooks, ensure the webhook handles all dynamic logic and direct messaging.

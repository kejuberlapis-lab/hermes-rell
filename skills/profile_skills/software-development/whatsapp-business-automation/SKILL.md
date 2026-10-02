---
name: whatsapp-business-automation
description: "Use when building WhatsApp Business bots or customer menus."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [whatsapp, chatbot, baileys, customer-service, qr-pairing, lead-generation, multi-device, auto-reply]
    related_skills: [production-environment-operations, web-asset-deployment-and-caching]
---

# WhatsApp Business Bot & Messaging Gateway Automation

A class-level operational skill for building, deploying, and managing automated WhatsApp Business chatbots, multi-tier customer service menus, and lead capture gateways using headless socket protocols (`@whiskeysockets/baileys`) on Linux VPS environments.

## When to Use

- When building automated 24/7 customer service, product catalog inquiries, or sales lead generation for WhatsApp Business numbers linked from websites or marketing campaigns.
- When setting up headless WhatsApp multi-device gateways without resource-heavy headless browser stacks (Puppeteer / Chromium).
- When linking WhatsApp accounts via **8-Digit Pairing Code** or **Real-Time QR Barcode Image Delivery**.
- When socket connections encounter connection errors or risk of number suspension, requiring pivoting to **Official WhatsApp Business Mobile Automation (Greeting/Away Messages + Quick Replies)** or **WhatsApp Cloud API Webhooks**.
- When configuring website Click-to-Chat buttons with contextual pre-filled messages (`https://wa.me/<number>?text=...`).
- When structuring conversational routing: main greeting menus, product specification cards, localized service inquiries, and human sales escalation handoffs.

## Procedure

1. **Architecture Selection & Risk Assessment:**
   - Evaluate client constraints and operational risk before selecting the messaging gateway approach:
     - **Option 1: Official In-App Automation (Zero Risk / Instant Deployment):** Best for single-device operations where official compliance, zero server cost, and zero account ban risk are mandatory.
     - **Option 2: Headless Socket Gateway (`@whiskeysockets/baileys`):** Best for local/residential proxy environments requiring custom programmatic bot logic without Meta API fees.
     - **Option 3: Official Meta WhatsApp Cloud API:** Best for multi-agent enterprise server backends requiring official webhooks and verified business status.

2. **Official In-App Automation & Workarounds (No-Code / High Reliability):**
   - **Greeting Message (*Pesan Sambutan*):** Auto-sends main welcome menu to new contacts or chats inactive for 14+ days.
   - **Universal Delivery via Away Message (*Pesan Di Luar Jam Kerja - Selalu Kirim*):**
     - *Issue:* Standard Greeting Messages do NOT fire for returning contacts (<14 days).
     - *Solution:* Configure **Away Message** with Schedule set to **"Always send" (*Selalu kirim*)** and Recipients set to **"Everyone" (*Semua orang*)**. This ensures every inbound message receives the automated menu immediately regardless of past chat history.
   - **Quick Replies (*Balas Cepat* Shortcuts):**
     - Pre-configure numbered shortcuts (`/1`, `/2`, `/3`, `/4`, `/5`) in WhatsApp Business Tools.
     - Maps to detailed product specification cards, TKDN scores, pricing formats, and sales escalation templates, enabling human operators to reply in 1 second.
   - **Contextual Pre-Filled Website Click-to-Chat Links:**
     - Structure web CTA links to auto-fill the user's input field upon clicking:
       `https://wa.me/628119255476?text=Halo%20PT%20Mitsindo%2C%20saya%20ingin%20info%20produk%20IFP`
     - Allows instant matching with pre-configured Quick Reply shortcuts.

3. **Headless Socket Project Scaffolding & Dependencies (`@whiskeysockets/baileys`):**
   - Initialize a lightweight Node.js project directory (e.g. `/home/ubuntu/<brand>-wa-bot`):
     ```bash
     mkdir -p /home/ubuntu/<brand>-wa-bot && cd /home/ubuntu/<brand>-wa-bot
     npm init -y
     npm install @whiskeysockets/baileys pino qrcode qrcode-terminal
     ```
   - Core packages:
     - `@whiskeysockets/baileys`: Pure WebSocket implementation of WhatsApp multi-device protocol (minimal RAM/CPU usage).
     - `qrcode`: Generates PNG image files for remote QR delivery.
     - `qrcode-terminal`: Prints ASCII QR to terminal logs.
     - `pino`: Structured logging with level control (`level: 'silent'` for production cleanliness).

2. **Persistent Auth State Management:**
   - Always persist credentials across process restarts using `useMultiFileAuthState`:
     ```javascript
     const { useMultiFileAuthState, fetchLatestBaileysVersion, DisconnectReason } = require('@whiskeysockets/baileys');
     const path = require('path');

     const AUTH_DIR = path.join(__dirname, 'auth_info_baileys');
     const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
     ```

3. **Dual Authentication Gateway: 8-Digit Pairing Code vs QR Barcode:**
   - **Method A (Recommended: 8-Digit Pairing Code):** Enables instant connection without requiring a second screen or camera scanning (ideal when the user is chatting from the target phone itself):
     ```javascript
     // E.164 phone number without leading '+' or '0' (e.g. '628119255476')
     if (USE_PAIRING_CODE && !sock.authState.creds.registered) {
         setTimeout(async () => {
             try {
                 const code = await sock.requestPairingCode(targetPhoneNumber);
                 console.log(`🔑 PAIRING CODE: ${code}`); // Returns 8-character string e.g. GNY7X9ET
                 fs.writeFileSync(path.join(__dirname, 'pairing_code.txt'), code);
             } catch (err) {
                 console.error('Failed to request pairing code:', err);
             }
         }, 3000);
     }
     ```
     - Provide clear 5-step instructions to the user:
       1. Open WhatsApp / WhatsApp Business ➔ Settings ➔ **Linked Devices**.
       2. Tap **Link a Device**.
       3. Tap **"Link with phone number instead"** (*Tautkan dengan nomor telepon saja*) at bottom of camera screen.
       4. Enter the 8-character code.
   - **Method B (QR Code Image Export):**
     When using QR, export dynamically to a 500px PNG file and transmit via `MEDIA:<absolute_path_to_qr.png>`.

4. **Robust Connection Lifecycle & Auto-Reconnect:**
   - Distinguish between transient network disconnections (auto-reconnect) and explicit logout (auth cleanup):
     ```javascript
     if (connection === 'close') {
         const shouldReconnect = (lastDisconnect?.error)?.output?.statusCode !== DisconnectReason.loggedOut;
         if (shouldReconnect) {
             setTimeout(startBot, 3000);
         } else {
             console.log('Logged out permanently. Clear auth directory to re-pair.');
         }
     }
     ```

5. **Inbound Message Ingestion & Sanity Filters:**
   - Filter out noise, status updates, and loop triggers:
     - Skip if `msg.key.fromMe === true` (prevents self-reply loops).
     - Skip if `msg.key.remoteJid === 'status@broadcast'` (ignores WhatsApp Status stories).
     - Extract clean text from `conversation`, `extendedTextMessage.text`, or `imageMessage.caption`.

6. **Hierarchical Menu & Conversational Architecture:**
   - **Main Menu (Greeting):** Professional intro, brand identity, and clean numbered choices (1–N).
   - **Product / Service Cards:** Concise bullet points (key specs, sizing, certifications like TKDN, applications) followed by navigation cues (`Ketik 0 untuk Menu Utama, atau 5 untuk Sales`).
   - **Escalation to Human Sales:** Provide office address, official hotline, email, and a structured pre-fill template (Name, Project Type, Location, Unit Volume).
   - **Fallback Routing:** Friendly error recovery that re-displays the main menu.

7. **Deployment & Process Monitoring:**
   - Execute the bot as a background service or supervisor process:
     ```bash
     cd /home/ubuntu/<brand>-wa-bot && node bot.js
     ```
   - Monitor logs and connection status. Clean up transient QR image files once pairing status transitions to `open`.

## Pitfalls

- **Datacenter IP Handshake Rejections on Socket Gateways:** WhatsApp actively restricts unofficial socket handshakes originating from cloud/datacenter IP ranges, triggering "Gagal memuat" (*Failed to load*) or device linking timeouts. When encountered, pivot immediately to official in-app WhatsApp Business tools (Greeting + Quick Replies) or official Meta Cloud API.
- **Assuming Greeting Messages Send to All Inbound Chats:** Default WhatsApp Business greeting messages only fire for first-time senders or after 14 days of inactivity; configure Away Messages set to "Always send" to capture existing contacts.
- **Forcing QR Scans on Mobile-Only Users:** When users receive bot instructions on their mobile device, they cannot point their phone's camera at their own screen; always provide the 8-digit **Pairing Code** (`requestPairingCode`) as the primary frictionless alternative.
- **Rendering QR Codes Only in Terminal Output:** ASCII QR codes in terminal logs are distorted and unscannable across chat platforms; always generate standard PNG images when QR mode is requested.
- **Missing Self-Message and Broadcast Guards:** Failing to check `msg.key.fromMe` causes the bot to respond to its own messages, triggering rapid-fire infinite message loops and risking number suspension by WhatsApp.
- **Ignoring Ephemeral Token Expiration:** Both WhatsApp QR codes (20–30s) and pairing codes (1–2 minutes) expire quickly; ensure daemon handles token regeneration cleanly and notifies the user immediately if expired.
- **Losing Auth State on Restart:** Storing credentials in memory or failing to bind `sock.ev.on('creds.update', saveCreds)` requires re-authenticating after every server restart.
- **Overcrowding Responses with Massive Unformatted Text:** Sending massive raw text walls degrades mobile readability; format with WhatsApp bold (`*text*`), bullet points (`•`), and clear single-digit navigation controls.

---
name: telegram-mini-app-automation-v3
description: "Use when automating Telegram Mini Apps or Web3 airdrops."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [Telegram-Mini-App, Web3, TON, Airdrop, Automation, Pyrogram, Telethon, API-Reverse-Engineering, DevTools, DePIN-Simulated-Node]
    related_skills: [automated-trading-systems, zero-hallucination-coder, reverify]
---

# Telegram Mini App & Web3 Airdrop Automation

A standardized operational framework for inspecting, reverse-engineering, automating, and monitoring Telegram Mini Apps (TMAs), tap-to-earn/mining bots, virtual node simulations (DePIN/Testnet), and Web3 airdrop interactions (TON, EVM, BSC).

## When to Use

- When auditing, inspecting, or reverse-engineering Telegram Webview/Mini App network traffic, Supabase Edge Functions, and backend API endpoints.
- When extracting `initData` (`tgWebAppData`) or Bearer JWT tokens for direct backend API automation.
- When creating scheduled 24-hour claim/mining scripts and background workers on a Linux VPS.
- When automating batch actions (e.g. auto-tap energy draining, daily check-in, task claims, virtual node push cycles).
- When inspecting Web3 airdrop contracts, developer wallet balances, and token distributions on TON or EVM block explorers.

## Procedure

1. **Architecture & Authentication Flow:**
   - **Telegram Webview Handshake:** Telegram launches mini-apps by requesting a webview URL via MTProto (`messages.requestAppWebView`).
   - **`initData` Token Structure:** The URL contains `#tgWebAppData=` containing URL-encoded parameters (`query_id`, `user`, `auth_date`, `hash`). This string serves as the bearer token for all subsequent backend REST/GraphQL/Supabase calls.
   - **Console Extraction & Execution Contexts:**
     - *Iframe Context Switching:* Telegram Mini Apps run inside isolated iframes within Telegram Web. In browser DevTools Console, switch the execution context dropdown from `top` to the mini-app iframe (e.g. `<domain>`), or right-click inside the mini-app and choose *Inspect*. Executing `Telegram.WebApp.initData` in `top` context causes `Uncaught ReferenceError: Telegram is not defined`.
     - *Self-XSS Console Warning:* Modern Chromium browsers (Chrome/Brave/Edge) block pasting into DevTools Console by default. Instruct users to type `allow pasting` and press Enter, or type short commands manually.
     - *Session Storage Extraction:* Alternatively in the parent context run:
       ```javascript
       copy(decodeURIComponent(sessionStorage['telegram-apps/launch-params']).split('tgWebAppData=')[1].split('&tgWebAppStartParam')[0])
       ```
     - *Copy as cURL Shortcut:* When users struggle to locate Bearer tokens or request headers manually in DevTools Network tab, instruct them to right-click the target request name (e.g. `state`, `check-in`, `sync`) and select **Copy -> Copy as cURL (bash)**. This captures the complete URL, headers, and authentication tokens in a single string.
     - *Mobile Browser Constraint:* Mobile browsers (Chrome/Safari on iOS/Android/tablets) block `javascript:` pseudo-protocols in the address bar due to self-XSS protection; always use Desktop DevTools, MTProto extraction, or Network tab inspection instead of mobile address bars.

2. **Backend API Automation (Lightweight Direct API & BaaS Endpoints):**
   - **Supabase Edge Function Endpoints:** Look for `https://<project-id>.supabase.co/functions/v1/<function-name>` (e.g. `mima-secure-api`). They expect `x-telegram-init-data`, `apikey`, or `Authorization` headers.
   - **Batch Action Optimization:** Inspect `Network -> Payload` for batch parameters (e.g. `{"action": "tap", "count": 10}`). Batching maximizes rate-limit efficiency and drains tap energy quickly without triggering per-second throttling.
   - **Virtual Simulated Node (DePIN Web Nodes & Hardware Upgrades):**
     - Web testnet nodes (e.g. 9Chain) run via REST/JWT endpoints (e.g. `POST /v2/program/tap` with `{"count": 50}`, `GET /v2/program/catalog`, `POST /v2/program/upgrade` with `{"componentKey": "cpu", "toLevel": 1}`).
     - Inspect `Network -> Fetch/XHR -> Headers -> Request Headers` for `authorization: Bearer <jwt>`. Users must click directly on a specific request under the `Name` column to reveal the `Headers`, `Payload`, and `Response` tabs.
     - Always implement hardware auto-compounding (e.g. upgrading CPU/RAM components) before tier level-ups, as component upgrades immediately boost both base mining rate per hour and point yields per tap.
   - Implement modular Python workers using `httpx` or `urllib.request`:
     ```python
     import httpx

     headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
         "Accept": "application/json, text/plain, */*",
         "x-telegram-init-data": init_data,
         "Authorization": f"Bearer {init_data}",
         "Content-Type": "application/json"
     }
     response = httpx.post(
         "https://<project-id>.supabase.co/functions/v1/mima-secure-api",
         headers=headers,
         json={"action": "tap", "count": 10, "initData": init_data}
     )
     ```
   - Parse response status (`next_available_at`, `balance`, `tap_energy`, `mining_rate`) and calculate sleep cooldown until the next cycle.

3. **On-Chain & Smart Contract Verification:**
   - **Explorer Audits:** Before committing gas or interacting with contracts, inspect developer wallets and token contracts on the respective block explorer (Tonviewer/TonScan for TON Jettons; BscScan for BSC BEP-20; Etherscan for EVM).
   - **Liquidity & Distribution Checks:** Verify whether the token has an active Decentralized Exchange (DEX) liquidity pool (e.g. STON.fi, DeDust, PancakeSwap) and verify real contract balances vs. locked dev allocations.
   - **Gas vs. Yield Evaluation:** Compare on-chain transaction fees against current reward value before initiating automated contract claim calls.

4. **Background Execution & Scheduling on Linux VPS:**
   - **Randomized Jitter:** Add randomized sleep intervals (e.g., `time.sleep(random.uniform(0.8, 1.5))`) between API calls to avoid static fingerprinting.
   - **State Persistence:** Store credentials and cooldown timestamps in a local SQLite or JSON file.
   - **Notifications:** Integrate Telegram bot webhook/alerts to notify the user upon successful claims, milestone reach (e.g. minimum withdrawal threshold), or authentication token expiry.

## Pitfalls

- **Evaluating `Telegram.WebApp` in the `top` window frame:** Telegram Web wraps Mini Apps in nested iframes; running console commands in the `top` context throws `Uncaught ReferenceError: Telegram is not defined`. Always switch the DevTools context dropdown to the iframe.
- **Looking for Headers without selecting a request:** In browser DevTools Network tab, the `Headers` sub-tab does not render until the user clicks a specific request row in the `Name` column.
- **Hardcoding expired `initData` / Bearer tokens:** Mini-app session hashes and JWTs expire (typically within 24 hours); build automatic session refresh logic via MTProto (`telethon`/`pyrogram`) or alert the user when 401/403 occurs rather than looping failures.
- **Instructing users to use `javascript:` in mobile address bars:** Mobile browsers automatically strip the `javascript:` protocol or throw self-XSS security warnings; use desktop DevTools or Network inspector instead.
- **Using primary wallets for airdrop testing:** Connecting primary holding wallets to unverified mini-app smart contracts risks wallet drainers; always enforce isolated secondary/burner wallets.
- **Ignoring missing Telegram WebView headers:** Sending API requests without `User-Agent`, `Origin`, and `Referer` headers results in immediate 403 Forbidden Cloudflare/WAF blocks.
- **Static timing intervals:** Triggering actions at exact round timestamps (e.g. precisely every 60.00 seconds) flags accounts in anti-bot Sybil filters; always inject random delay jitter.
- **Blind on-chain claim execution:** Auto-executing contract transactions without verifying gas reserves can drain native currency (TON/ETH/BNB) on worthless token yields.

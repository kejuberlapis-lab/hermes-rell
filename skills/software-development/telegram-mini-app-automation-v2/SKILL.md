---
name: telegram-mini-app-automation-v2
description: "Use when automating Telegram Mini Apps or Web3 airdrops."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [Telegram-Mini-App, Web3, TON, Airdrop, Automation, Pyrogram, Telethon, API-Reverse-Engineering, DevTools]
    related_skills: [automated-trading-systems, zero-hallucination-coder, reverify]
---

# Telegram Mini App & Web3 Airdrop Automation

A standardized operational framework for inspecting, reverse-engineering, automating, and monitoring Telegram Mini Apps (TMAs), tap-to-earn/mining bots, and Web3 airdrop interactions (TON, EVM, BSC).

## When to Use

- When auditing, inspecting, or reverse-engineering Telegram Webview/Mini App network traffic, Supabase Edge Functions, and backend API endpoints.
- When extracting `initData` (`tgWebAppData`) for direct backend API automation.
- When creating scheduled 24-hour claim/mining scripts and background workers on a Linux VPS.
- When inspecting Web3 airdrop contracts, developer wallet balances, and token distributions on TON or EVM block explorers.

## Procedure

1. **Architecture & Authentication Flow:**
   - **Telegram Webview Handshake:** Telegram launches mini-apps by requesting a webview URL via MTProto (`messages.requestAppWebView`).
   - **`initData` Token Structure:** The URL contains `#tgWebAppData=` containing URL-encoded parameters (`query_id`, `user`, `auth_date`, `hash`). This string serves as the bearer token for all subsequent backend REST/GraphQL/Supabase calls.
   - **Console Extraction & Execution Contexts:**
     - *Iframe Context Switching:* Telegram Mini Apps run inside isolated iframes within Telegram Web. In browser DevTools Console, switch the execution context dropdown from `top` to the mini-app iframe (e.g. `<domain>`), or right-click inside the mini-app and choose *Inspect*. Executing `Telegram.WebApp.initData` in `top` context causes `Uncaught ReferenceError: Telegram is not defined`.
     - *Session Storage Extraction:* Alternatively in the parent context run:
       ```javascript
       copy(decodeURIComponent(sessionStorage['telegram-apps/launch-params']).split('tgWebAppData=')[1].split('&tgWebAppStartParam')[0])
       ```
     - *Mobile Browser Constraint:* Mobile browsers (Chrome/Safari on iOS/Android/tablets) block `javascript:` pseudo-protocols in the address bar due to self-XSS protection; always use Desktop DevTools, MTProto extraction, or Network tab inspection instead of mobile address bars.

2. **Backend API Automation (Lightweight Direct API & BaaS Endpoints):**
   - Identify backend infrastructure (Supabase Edge Functions, Cloudflare Workers, Fastify/Express backends):
     - **Supabase Edge Function Endpoints:** Look for `https://<project-id>.supabase.co/functions/v1/<function-name>` (e.g. `mima-secure-api`). They expect `x-telegram-init-data`, `apikey`, or `Authorization` headers.
     - **Standard REST/GraphQL:** Inspect `Network -> Fetch/XHR` for action payloads (e.g. `{"action": "mine"}`, `{"action": "claim"}`).
   - Implement modular Python workers using `httpx` or `requests`:
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
         json={"action": "mine"}
     )
     ```
   - Parse response status (`next_claim_at`, `balance`, `mining_rate`) and calculate sleep cooldown until the next cycle.

3. **On-Chain & Smart Contract Verification:**
   - **Explorer Audits:** Before committing gas or interacting with contracts, inspect developer wallets and token contracts on the respective block explorer (Tonviewer/TonScan for TON Jettons; BscScan for BSC BEP-20; Etherscan for EVM).
   - **Liquidity & Distribution Checks:** Verify whether the token has an active Decentralized Exchange (DEX) liquidity pool (e.g. STON.fi, DeDust, PancakeSwap) and verify real contract balances vs. locked dev allocations.
   - **Gas vs. Yield Evaluation:** Compare on-chain transaction fees against current reward value before initiating automated contract claim calls.

4. **Background Execution & Scheduling on Linux VPS:**
   - **Randomized Jitter:** Add randomized sleep intervals (e.g., `time.sleep(random.randint(30, 90))`) before claim cycles to avoid static fingerprinting.
   - **State Persistence:** Store credentials and cooldown timestamps in a local SQLite or JSON file.
   - **Notifications:** Integrate Telegram bot webhook/alerts to notify the user upon successful claims, milestone reach (e.g. minimum withdrawal threshold), or authentication token expiry.

## Pitfalls

- **Evaluating `Telegram.WebApp` in the `top` window frame:** Telegram Web wraps Mini Apps in nested iframes; running console commands in the `top` context throws `Uncaught ReferenceError: Telegram is not defined`. Always switch the DevTools context dropdown to the iframe.
- **Hardcoding expired `initData` tokens:** Mini-app session hashes expire (typically within 24 hours); build automatic session refresh logic via MTProto (`telethon`/`pyrogram`) or alert the user when 401 Unauthorized occurs rather than looping failures.
- **Instructing users to use `javascript:` in mobile address bars:** Mobile browsers automatically strip the `javascript:` protocol or throw self-XSS security warnings; use desktop DevTools or Network inspector instead.
- **Using primary wallets for airdrop testing:** Connecting primary holding wallets to unverified mini-app smart contracts risks wallet drainers; always enforce isolated secondary/burner wallets.
- **Ignoring missing Telegram WebView headers:** Sending API requests without `User-Agent`, `Origin`, and `Referer` headers results in immediate 403 Forbidden Cloudflare/WAF blocks.
- **Static timing intervals:** Triggering actions at exact round timestamps (e.g. precisely every 60.00 seconds) flags accounts in anti-bot Sybil filters; always inject random delay jitter.
- **Blind on-chain claim execution:** Auto-executing contract transactions without verifying gas reserves can drain native currency (TON/ETH/BNB) on worthless token yields.

---
name: telegram-mini-app-automation
description: "Use when automating Telegram Mini Apps or Web3 airdrops."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [Telegram-Mini-App, Web3, TON, Airdrop, Automation, Pyrogram, Telethon, API-Reverse-Engineering]
    related_skills: [automated-trading-systems, zero-hallucination-coder, reverify]
---

# Telegram Mini App & Web3 Airdrop Automation

A standardized operational framework for inspecting, reverse-engineering, automating, and monitoring Telegram Mini Apps (TMAs), tap-to-earn/mining bots, and Web3 airdrop interactions (TON, EVM).

## When to Use

- When auditing, inspecting, or reverse-engineering Telegram Webview/Mini App network traffic and API endpoints.
- When extracting `initData` (`tgWebAppData`) for direct backend API automation.
- When creating scheduled 24-hour claim/mining scripts and background workers on a Linux VPS.
- When inspecting Web3 airdrop contracts, developer wallet balances, and token distributions on TON or EVM block explorers.

## Procedure

1. **Architecture & Authentication Flow:**
   - **Telegram Webview Handshake:** Telegram launches mini-apps by requesting a webview URL via MTProto (`messages.requestAppWebView`).
   - **`initData` Token Structure:** The URL contains `#tgWebAppData=` containing URL-encoded parameters (`query_id`, `user`, `auth_date`, `hash`). This string serves as the bearer token for all subsequent backend REST/GraphQL calls.
   - **Direct API Extraction:**
     - In browser/Telegram Web DevTools (Network tab), filter requests to the mini-app backend domain (e.g., `api.<project>.com`).
     - Inspect request headers for `Authorization`, `x-tg-data`, or payload `initData`.
     - *Mobile vs Desktop constraint:* Mobile browsers (Chrome/Safari) strip `javascript:` pseudo-protocols from address bars; always use Desktop DevTools (`F12 -> Console -> Telegram.WebApp.initData`), local MTProto scripts, or proxy sniffers instead of mobile browser address bars.

2. **Backend API Automation (Lightweight Direct API Method):**
   - Implement a modular Python worker using `httpx` or `requests`:
     ```python
     import httpx

     headers = {
         "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
         "Accept": "application/json, text/plain, */*",
         "Authorization": f"Bearer {init_data_or_jwt}",
         "Origin": "https://webapp-domain.com",
         "Referer": "https://webapp-domain.com/"
     }
     response = httpx.post("https://api.project.com/api/v1/claim", headers=headers, json={"action": "mine"})
     ```
   - Parse response status (e.g., `next_claim_at`, `balance`, `energy`) and calculate exact wait duration until the next cycle.

3. **On-Chain & Smart Contract Verification:**
   - **Explorer Audits:** Before committing gas or interacting with contracts, inspect the developer wallet and token contract on the respective block explorer (e.g., Tonviewer / TonScan for TON Jettons; Etherscan / BscScan for EVM).
   - **Liquidity & Distribution Checks:** Verify whether the token has an active Decentralized Exchange (DEX) liquidity pool (e.g., STON.fi, DeDust) and verify real contract balances vs. locked dev allocations.
   - **Gas vs. Yield Evaluation:** Compare on-chain transaction fees against current reward value before initiating automated contract claim calls.

4. **Background Execution & Scheduling on Linux VPS:**
   - **Randomized Jitter:** Add randomized sleep intervals (e.g., `time.sleep(random.randint(30, 90))`) before claim cycles to avoid static fingerprinting.
   - **State Persistence:** Store credentials and cooldown timestamps in a local SQLite or JSON file.
   - **Notifications:** Integrate Telegram bot webhook/alerts to notify the user upon successful claims, milestone reach (e.g. minimum withdrawal threshold), or authentication token expiry.

## Pitfalls

- **Hardcoding expired `initData` tokens:** Mini-app session hashes expire (typically within 24 hours); build automatic session refresh logic via MTProto (`telethon`/`pyrogram`) or notify the user when 401 Unauthorized occurs rather than looping failures.
- **Using primary wallets for airdrop testing:** Connecting primary holding wallets to unverified mini-app smart contracts risks wallet drainers; always enforce isolated secondary/burner wallets.
- **Ignoring missing Telegram WebView headers:** Sending API requests without mobile `User-Agent`, `Origin`, and `Referer` headers results in immediate 403 Forbidden Cloudflare/WAF blocks.
- **Static timing intervals:** Triggering actions at exact round timestamps (e.g. precisely every 60.00 seconds) flags accounts in anti-bot Sybil filters; always inject random delay jitter.
- **Blind on-chain claim execution:** Auto-executing contract transactions without verifying gas reserves can drain native currency (TON/ETH/BNB) on worthless token yields.

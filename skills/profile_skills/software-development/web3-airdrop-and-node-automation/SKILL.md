---
name: web3-airdrop-and-node-automation
description: "Automate Telegram Mini Apps, testnet nodes, and airdrops."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [Web3, Airdrop, Telegram-Mini-App, DePIN-Simulated-Node, TON, EVM, BSC, Solana, API-Automation, Obsidian-Portfolio]
    related_skills: [automated-trading-systems, zero-hallucination-coder, reverify]
---

# Web3 Airdrop, Telegram Mini App & Testnet Node Automation

A comprehensive operational framework for reverse-engineering, automating, and tracking Web3 airdrops, Telegram Mini Apps (TMAs), virtual simulated testnet nodes (DePIN), and multi-chain wallet reward distributions.

## When to Use

- When inspecting, debugging, or reverse-engineering Telegram Webview/Mini App traffic (Supabase Edge Functions, backend APIs).
- When automating daily check-ins, batch tap-to-earn mining, or virtual node push loops via direct HTTP requests (`initData` or Bearer JWT).
- When configuring hardware auto-compounding (e.g. CPU/RAM upgrades in simulated nodes) vs. snapshot balance preservation.
- When managing multi-chain withdrawal settings (EVM/BSC, TON, Solana) and protecting sensitive destination changes with PINs.
- When organizing, tracking, and synchronizing multi-project airdrop portfolios with verified direct links in Obsidian markdown dashboards.
- When diagnosing, recovering, or managing multi-container Android virtual phone farms (Redroid + ws-scrcpy web viewer).

## Procedure

1. **Authentication Token & Sesi Extraction:**
   - **Telegram Mini Apps (`initData`):**
     - In Chrome/Brave DevTools, switch Console execution context from `top` to the mini-app iframe to avoid `Uncaught ReferenceError: Telegram is not defined`.
     - In DevTools Network tab, click directly on a specific API request (e.g. `state`, `check-in`, `tap`) under the `Name` column to reveal `Headers`, `Payload`, and `Response`.
     - Fast extraction shortcut: Right-click target request -> **Copy -> Copy as cURL (bash)** to capture all headers and tokens in one line.
     - Never instruct users to paste `javascript:` in mobile address bars (blocked by self-XSS security).
   - **Web3 Web Testnets (Bearer JWT):**
     - Extract `authorization: Bearer <jwt>` from `Network -> Request Headers`.
     - Reassure users that lifetime cumulative points (`xpEarnedTotal`) are permanently logged for airdrop snapshot allocation and are never reduced by spending spendable balance (`xpTotal`) on upgrades.
     - Note on UI caching: After running headless scripts against backend APIs, instruct users to press `F5` / `Ctrl+R` to force the browser to re-fetch state from server endpoints.

2. **Automated Batch Execution & Compounding (Python Workers):**
   - **Batch Optimization:** Inspect payload schemas for batch parameters (e.g. `count: 10` for Supabase functions, `count: 50` for node taps) to drain daily quotas rapidly without hitting per-second rate limits.
   - **Hardware Compound Rule:** Prioritize upgrading unlocked hardware components (CPU, RAM) before tier level-ups when the payback period is favorable ($\le 24-48$ hours), immediately multiplying both base passive rate and per-tap yield.
   - **GameFi XP & Waitlist Tasks:** For Season 0 / early access models (e.g. QyroLabs, SVP Chain), complete static social tasks (X follow/repost, Telegram, Discord), bind dual wallets (EVM + Solana), and schedule 24-hour daily loot box / expedition cycles.
   - **Anti-Sybil Jitter:** Inject randomized delays (`time.sleep(random.uniform(0.8, 1.5))`) between requests.

3. **Multi-Chain Wallet Security & Verification:**
   - Always enforce isolated secondary/burner wallets for airdrop testing and connection.
   - For EVM/BSC/Solana profile binding, verify public addresses only (`0x...` or base58) and protect destination modifications with a 4-digit PIN.
   - Inspect token contracts and developer liquidity on block explorers (Tonviewer, BscScan, Solscan) before committing gas fees.
   - Cache testnet quiz answer keys and network IDs (e.g. Cosmos/EVM Chain IDs, block times) directly into project documentation.

4. **Android Cloud Phone Farm (Redroid & ws-scrcpy Web Viewer Recovery):**
   - **Architecture:** Redroid instances run as independent headless Android 12 containers mapped to host ports (`5555` to `5560`). The `ws_scrcpy` container provides a centralized browser viewer on port `8000`.
   - **Port Collision & Zombie Server Trap (`Address already in use`):**
     - When client web sessions disconnect abruptly, orphan `app_process / com.genymobile.scrcpy.Server` instances remain locked on internal container port `8886`.
     - Subsequent connection attempts fail with `java.net.BindException: Address already in use` and ws-scrcpy logs `The maximum number of attempts to fetch device info has been reached`, rendering the browser viewer blank.
   - **Zero-Data-Loss Recovery Procedure:**
     1. Inspect and kill the zombie scrcpy server process inside each container without restarting or wiping the Android OS:
        ```bash
        for i in {1..6}; do
          sudo docker exec android_phone_$i pkill -9 -f scrcpy || true
        done
        ```
     2. Restart the `ws_scrcpy` viewer container to re-initialize clean ADB client sockets to the Android devices.

5. **Obsidian Portfolio Organization:**
   - Maintain a master tracker at `ObsidianVault/Airdrop/00_Dashboard_Airdrop.md` with:
     - Project summary table (Network, Category, Status/Level, Current Balance/XP, Next Target Date).
     - Direct clickable links to dashboard portals, explorers, faucets, and verification endpoints.
   - Maintain dedicated sub-notes (`[[9Chain]]`, `[[QyroLabs]]`, `[[MIMA_Coin]]`, `[[Victors_Company]]`, `[[YouPulse]]`, `[[SVP_Chain]]`) detailing account parameters, hardware tiers, daily task checklists, and tokenomics formulas.

## Pitfalls

- **Evaluating `Telegram.WebApp` in `top` frame:** Always switch DevTools context to the iframe.
- **Looking for Headers without selecting a request row:** DevTools requires clicking an entry in the `Name` column before showing the `Headers` panel.
- **Hardcoding expired tokens:** Mini-app sessions and JWTs expire within 24h; catch 401/403 responses and alert the user rather than looping.
- **Over-spending points near snapshot dates:** Once the target tier/multiplier is achieved, halt all upgrades and accumulate 100% of points for TGE conversion.
- **Missing Direct Links in Portfolio:** Always attach direct URL endpoints for dashboards and faucets in Obsidian so audits can be performed immediately without searching chat history.
- **Killing Android Containers Instead of Zombie Processes:** Restarting or removing Redroid containers resets active Android app sessions, clipboard caches, and proxy connections; only kill the specific `scrcpy` server process inside the container.

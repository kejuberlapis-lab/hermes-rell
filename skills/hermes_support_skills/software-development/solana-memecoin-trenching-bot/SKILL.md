---
name: solana-memecoin-trenching-bot
description: Use when building or operating Solana memecoin trading bots.
version: 1.0.0
license: MIT
author: Hermes Agent
metadata:
  hermes:
    tags: [solana, memecoin, pumpfun, trading-bot, backtest]
    related_skills: [crypto-spot-trading-automation]
---

# Solana Memecoin Trenching Bot

## When to Use
Use when building, running, backtesting, or debugging automated memecoin trading bots, sniper tools, or copy-trading workflows on Solana (Pump.fun, Raydium, DexScreener, GMGN.ai).

## 1. Core Architecture
- **Stream/Ingestion:** PumpPortal WebSocket (`wss://pumpportal.fun/api/data`) for live new pair/trade events or Helius Geyser RPC.
- **Execution Engine:** PumpPortal Trade API (`/api/trade-local`) with unsigned transaction deserialization and local Keypair signing + Jito bundle tip / priority fee.
  - Known implementation pattern for Node.js (`@solana/web3.js` + `axios` + `bs58`):
    ```javascript
    const response = await axios.post('https://pumpportal.fun/api/trade-local', {
        publicKey: botKeypair.publicKey.toBase58(),
        action: actionType, // 'buy' or 'sell'
        mint: tokenMint,
        amount: amountVal,  // SOL amount for buy (denominatedInSol: 'true') or percentage like '50%' / '100%' for sell
        denominatedInSol: actionType === 'buy' ? 'true' : 'false',
        slippage: 15,
        priorityFee: 0.0002,
        pool: 'pump'
    }, { responseType: 'arraybuffer', timeout: 10000 });
    const tx = VersionedTransaction.deserialize(new Uint8Array(response.data));
    tx.sign([botKeypair]);
    const sig = await connection.sendTransaction(tx, { skipPreflight: true, maxRetries: 3 });
    ```
- **Security Audit:** RugCheck API (`https://api.rugcheck.xyz/v1/tokens/{mint}/report/summary`) + DexScreener API.

- **PumpPortal Dual-Pool Auto-Detection (`pool: "pump"` vs `"pump-amm"` 400 Bad Request Workaround):**
  - *Pitfall:* `https://pumpportal.fun/api/trade-local` returns `HTTP 400 Bad Request` with text *"Failed to find pump.fun bonding curve for mint... Token has migrated or does not exist. pool: 'pump-amm' is the correct option for migrated tokens"* if `pool: 'pump'` is specified for a token that has completed its bonding curve or migrated to Raydium.
  - *Fix:* Check `coin.complete`. If `complete === true`, prioritize `['pump-amm', 'pump', 'auto']`; if `false`, prioritize `['pump', 'pump-amm', 'auto']`. Wrap swap requests in a pool fallback loop to ensure 100% transaction generation success across both unmigrated and migrated tokens.

- **Command-Triggered Disciplined Micro-Scalper Protocol ("Alur Entry by Command, Auto-TP Receh, dan Total Standby"):**
  - When the operator mandates an on-demand, command-controlled scalping workflow (*"yang entry coin anda jangan nunggu persetujuan, jika saya suruh 'entry' langsung entry coin terbaik, jika profit langsung tp, habis itu stop tunggu saya suruh entry lagi"*):
    1. **Default Standby State:** The engine operates in `STANDBY` mode with automated scanning active, continuously evaluating and ranking the #1 best momentum candidate from Pump.fun and GMGN.ai feeds.
    2. **Mandatory Proactive Mathematical Gate (The Fixed-Fee Warning Rule):**
       - *Critical Pitfall:* When an operator requests micro-take-profit ("profit receh / +2% s/d +5%") on micro-entry sizing ($0.0020\text{ SOL}$), fixed round-trip costs (gas, priority fees, DEX protocol fees, and slippage $\approx 0.0008 - 0.0010\text{ SOL}$) represent up to **$50\%$ of the entry size**. A $+2.8\%$ gross gain ($+0.000056\text{ SOL}$) results in a **guaranteed net-negative cash loss**. See detailed math reference in `references/micro_capital_friction_and_execution_guardrails.md`.
       - *Hard Behavioral Rule:* The agent **MUST proactively compute and warn the operator of the net-loss expectation BEFORE executing**. Do not execute blindly and explain the loss afterward. For micro-positions ($<0.020\text{ SOL}$), require calibrated high-multiple TP targets ($+50\%$ to $+100\%$) or explain that micro-TP ($+3\%$) requires minimum entry sizing of $\ge 0.050 - 0.100\text{ SOL}$ to exceed the fixed fee floor.
    3. **Single Command Trigger (`"entry"` / `"gas"`):** Upon explicit operator confirmation, the bot immediately triggers the buy execution for the Rank #1 candidate with disciplined micro-sizing on a single active slot (`MAX_HOLDINGS_LIMIT = 1`).
    4. **Immediate Synchronous History Logging (Prevent UI Disconnect):** In ultra-fast scalping cycles where buy and sell take place within seconds, immediately push confirmed transaction signatures (`buy_tx`, `sell_tx`, Solscan links) into persistent storage and in-memory dashboard history arrays so the UI reflects the trade instantly without appearing frozen or missing.
    5. **Rapid Take Profit & Full Liquidation:** Execute an immediate 100% full liquidation on-chain upon reaching the designated net-positive profit threshold.
    6. **Telegram Report & Immediate Standby Halt:** Broadcast the verified Solscan buy and sell transaction signatures to the operator, credit liquid SOL cash, and immediately halt all trading activity, remaining in total `STANDBY STOP` until the operator issues the next `"entry"` directive.
    7. **Post-Trade ATA Rent Reclaim Guidance:** Remind the operator to close empty token accounts in Phantom (Settings $\rightarrow$ Manage Accounts / Burn Empty Accounts) to reclaim the locked $\sim 0.002039\text{ SOL}$ ATA storage rent back into liquid SOL balance.

- **Manual Approval Workflow for Low Capital & High-Control Recovery ("Mode Sinyal & Manual Approval"):**
  - When operating on micro-capital ($< 0.050\text{ SOL}$) or recovering from drawdowns under strict operator supervision ("jangan otomatis, tunggu persetujuan jika mau entry"):
    1. **Autonomous Auto-Buy Disabled:** Explicitly set `autoBuy = false` across all evaluation loops. The engine is strictly prohibited from executing buys autonomously.
    2. **Single-Slot Ceiling (`MAX_HOLDINGS_LIMIT = 1`):** Cap active positions strictly to 1 slot to prevent cumulative ATA rent locks.
    3. **Background Radar & Pending Signal Queue:** The scanner continuously monitors Pump.fun/DexScreener feeds and filters Grade A+ momentum setups, placing them into a `pendingApprovals` queue with detailed scoring, market cap, and risk rationale.
    4. **Conversational / Dashboard Authorization:** The agent must present the token signal to the operator (via chat or dashboard approval card) and execute only upon explicit confirmation ("Setuju", "Beli", "Gas").
    5. **100% Full Take-Profit Liquidation & Re-Standby:** When the position reaches the target profit (+5% to +10%), execute an immediate 100% full exit, reclaim ATA rent back to liquid SOL, and return immediately to standby mode until the operator approves the next signal.

- **Frontend Robustness & Sanitization Guard for Mobile Dashboards ("Anti-Crash & Zero Undefined"):**
  - *Pitfall (DOM Freezing & 'undefined' UI Glitches):* Fast-moving memecoin feeds often carry malformed token names, raw HTML characters, or missing API properties, causing client-side JavaScript crashes or unsightly `undefined` text on mobile devices (e.g. iPhone Safari).
  - *Best Practice:*
    1. Implement strict HTML escaping (`escapeHtml()`) for token names, symbols, and mint addresses before injecting into innerHTML.
    2. Enforce defensive null-checking on all numerical properties (e.g. `typeof item.entry_mc === 'number' ? item.entry_mc.toLocaleString() : '0'`).
    3. Provide structured segmented navigation tabs (🎯 Approvals, 💼 Holdings, 📜 Logs) with persistent theme styling to ensure seamless mobile responsiveness.

## 2. Key Empirical Findings (Backtest & Strategy Rules)
- **Mandatory Architectural Separation: Gas Reserve (`MIN_SOL_RESERVE`) vs Trading Capital ("Pemisahan Saldo Gas & Modal Trading"):**
  - *Pitfall (Gas Starvation & Total Capital Lockup):* Treating the entire physical wallet SOL balance as disposable trading capital causes auto-buy loops to deploy every last lamport into tokens and ATA rent. Once free SOL drops below $\sim 0.003\text{ SOL}$, the wallet can no longer prepay priority gas fees to execute sell orders or take profits, resulting in gas starvation (`InstructionError: [3, {'Custom': 1}]`).
  - *Hard Implementation Rule:*
    1. **Strict `MIN_SOL_RESERVE` Floor:** Always declare and enforce an inviolable gas reserve floor ($\ge 0.010 - 0.020\text{ SOL}$, or minimum $0.005\text{ SOL}$ for micro-wallets) that is **strictly forbidden** from being used to purchase tokens.
    2. **Active Trading Capital Formula:**
       $$\text{Available Trading Capital} = \max\left(0, \text{Real Wallet SOL} - \text{MIN\_SOL\_RESERVE} - \text{Estimated ATA Rent for Open Slots}\right)$$
    3. **Automated Entry Block:** If $\text{Available Trading Capital} < \text{Minimum Entry Size}$, the engine must immediately reject all auto-entries and alert the operator, preserving the reserve exclusively for emergency exits, profit sells, and ATA close transactions.

- **Physical Token Portfolio vs Native SOL Balance Discrepancy & Liquidation Recovery ("Kenapa di Phantom Ada $2 tapi SOL Murni Sedikit?"):**
  - *Pitfall:* When real on-chain buys execute, native SOL drops rapidly because funds are converted into SPL / Token-2022 tokens and locked in Associated Token Account (ATA) rent. The operator sees a tiny native SOL balance (e.g. `0.0027 SOL` / $0.41 USD) but their Phantom mobile app shows ~$2.00 USD total portfolio value.
  - *Diagnosis & Resolution Procedure:*
    1. **Token Account Inspection:** Query token accounts across both standard SPL (`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`) and Token-2022 (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`) programs using `connection.getParsedTokenAccountsByOwner`.
    2. **Valuation Breakdown:** Match token amounts with DexScreener/Jupiter price API to show exact USD valuations per token.
    3. **100% On-Chain Recovery Swap:** Broadcast immediate sell transactions via PumpPortal `/api/trade-local` (`action: 'sell', amount: '100%', denominatedInSol: 'false', slippage: 50`) across all held mints to convert physical token assets back into native SOL cash.
    4. **Result Verification:** Query `connection.getBalance` to confirm restored native SOL balance.

- **Micro-Capital Capital Recovery Protocol ("Mode Scalping Hati-Hati Balik Modal"):**
  - When remaining real on-chain capital is depleted to micro-levels ($0.010 - 0.020\text{ SOL}$ / ~$2.00 USD) and the operator mandates conservative recovery scalping:
    1. **Ultra-Lean Sizing:** Downsize trade size to `0.0020 SOL` per trade to preserve gas reserves.
    2. **Strict Slot Capping:** Cap `MAX_HOLDINGS_LIMIT = 2` (or 1) so cumulative Solana ATA rent does not lock up free SOL.
    3. **Elite Ingestion Quality Gate (Score $\ge 120$):** Enforce high-conviction filtering requiring GMGN/Cielo Smart Money inflow, RugCheck safety, and organic volume $>80\%$.
    4. **Direct RPC Lock:** Eliminate all simulated compounding balance drift; hardwire the dashboard cash balance directly to `connection.getBalance(botKeypair.publicKey)`.
    5. **Micro-TP Compounding:** Target $+2.0\%$ to $+3.0\%$ Take Profit with instant 100% sell to lock proceeds immediately back into liquid SOL.

- **Selective Profit Harvest Protocol ("Close All Profitable Only"):**
  - When the operator instructs to selectively liquidate only winning/breakeven positions ("close all yang profit dulu"):
    1. Iterate through `state.positions` and filter positions where `pnl_percent >= 0.0`.
    2. For each profitable position, trigger an immediate 100% on-chain sell (`executeOnChainSell(pos.mint, '100%')`), calculate the returned SOL proceeds, credit `cashBalance` and `realizedProfit`, and record a `🎯 MANUAL PROFIT HARVEST` history event.
    3. Retain negative/drawdown positions in `state.positions` so they have breathing room to rebound without taking immediate realized losses.
    4. Synchronize updated positions and cash balance to `live_trades.json` and Obsidian vault (`memecoin.md`).

- **Total Engine Emergency Shutdown & Standby Protocol ("Berhentikan Semua / OFF Total"):**
  - When the operator mandates a complete trading halt ("berhentikan semua off kan dulu", "matikan bot"):
    1. **Pause Evaluation & Sniping:** Immediately set `isTradingPaused = true` and `isAutoCompoundActive = false` so scanner loops stop evaluating and no new orders can trigger.
    2. **Liquidate / Consolidate Open Positions:** Close any remaining active positions to convert token holdings back into liquid SOL cash.
    3. **Reset State Vectors:** Set `state.positions = []`, `state.pending = []`, update summary mode to `GMGN PRO TERMINAL (🛑 OFF / STANDBY)`.
    4. **Atomic File & Process Sync:** Write the clean state to `live_trades.json`, restart the server process so in-memory state is clean, and document the shutdown in `~/Documents/Obsidian Vault/memecoin.md`.

- **Emergency Wallet Decoupling, Rent ATA Reclaim & Absolute Hard-Kill Directive ("MATIKAN BOT / STOP HAPUS EWALLET"):**
  - When the user issues an emergency distress command to halt trading, delete keys, and reclaim funds ("MATIKAN BOT MEMECOIN", "hapus ewallet", "kembalikan saldo"):
    1. **Immediate Hard Process Termination:** Execute `kill -9 <PID>` and `fuser -k <port>/tcp` immediately to kill any running Node/Python trading daemons. Do not rely on soft flags alone.
    2. **Emergency 100% Token Liquidation:** Sell all remaining SPL and Token-2022 token balances (`action: 'sell', amount: '100%', pool: 'pump'`) to convert physical holdings back into native SOL.
    3. **Token-2022 & SPL ATA Rent Reclaim Routine:**
       - Query all token accounts under both `TOKEN_PROGRAM_ID` (`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`) and `TOKEN_2022_PROGRAM_ID` (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`).
       - For every empty account (`amount === 0`), construct and sign a `createCloseAccountInstruction` to immediately refund the $\sim 0.00151 - 0.002039\text{ SOL}$ rent deposit per account directly back into the wallet's native SOL balance.
    4. **Complete Credential Purging:** Overwrite all `.env` files in trading directories, purging all private keys (`BOT_PRIVATE_KEY=""`), set server constants to `BOT_WALLET_ADDRESS = "DISCONNECTED"`, and update persistent memory to forbid automated trading restarts.
    5. **Direct RPC Verification:** Query `connection.getBalance` on-chain to verify and report the exact physical SOL remaining in the wallet.

- **The Micro-Capital Rapid Churning & ATA Rent Drain Trap:**
  - *Catastrophic Mechanism:* When live on-chain trading is enabled with micro-capital ($< 0.050\text{ SOL}$), rapid multi-token buying (e.g. 10–14 tokens) locks $\sim 0.00151 - 0.002039\text{ SOL}$ per token into Solana Associated Token Account (ATA) rent exemptions. Within minutes, $0.020 - 0.030\text{ SOL}$ is locked in rent plus round-trip gas fees, creating the appearance that the wallet was completely drained.
  - *Hard Rule:* Never enable autonomous high-frequency multi-slot sniping on micro-capital ($< 0.15\text{ SOL}$). If micro-capital live testing is mandated by the user, restrict strictly to 1 slot with manual approval, and always attach `createCloseAccountInstruction` upon selling.
  - *Complete Emergency Purge & Decommission Directive:* When user demands absolute cessation and wallet removal ("stop hapus ewallet saya", "matikan bot", "kembalikan saldo"):
    1. Immediately issue `kill -9` on all trading daemons and release listening ports via `fuser -k`.
    2. Broadcast $100\%$ liquidation sells on all held SPL and Token-2022 tokens, followed immediately by `createCloseAccountInstruction` to refund all ATA rent deposits back into native liquid SOL.
    3. Wipe all private keys from `.env` files and remove any local project directories (`rm -rf`) if requested.
    4. Provide clear manual instructions for external liquidation / rent reclaim tools (e.g. Sol Incinerator / Phantom Burn) in case the server no longer holds keys.

- **Wallet Deletion, Emergency Rent Refund & Token Recovery Workflow ("Hapus E-Wallet / Kembalikan Saldo"):**
  - When the operator demands emergency wallet decoupling, deletion of private keys, and balance recovery ("stop hapus ewallet saya", "kembalikan saldo ewallet"):
    1. **Emergency Token Liquidation:** Immediately broadcast $100\%$ sell transactions (`action: 'sell', amount: '100%', pool: 'pump'`) across all token accounts to convert all held SPL / Token-2022 balances back into liquid SOL.
    2. **Solana Token Account (ATA) Rent Reclaim (Token-2022 & SPL):**
       - Query all token accounts via `connection.getParsedTokenAccountsByOwner(kp.publicKey, { programId: TOKEN_2022_PROGRAM_ID })`.
       - For every empty account (`amount === 0`), construct and sign a `createCloseAccountInstruction` to refund the $\approx 0.00151 - 0.002039\text{ SOL}$ rent deposit per account directly back into the wallet's main lamport balance.
    3. **Complete Credential Purge:** Wipe `BOT_PRIVATE_KEY` / `SOLANA_PRIVATE_KEY` from all `.env` files, update server variables to `BOT_WALLET_ADDRESS = "DISCONNECTED"`, and kill all background bot processes.
    4. **Direct RPC Verification:** Query `connection.getBalance` directly from the Solana RPC node to report the exact physical SOL remaining on-chain.

- **On-Chain Micro-Capital Multi-Slot Rent Lockout & Anchor 6063/6005 Trap:**
  - *Pitfall (The 5-Slot Micro-Balance Bleed & Micro-TP Net-Loss Trap):*
    1. **Solana ATA Rent Depletion:** Each new token account locks $\sim 0.002039\text{ SOL}$ in rent exemption ($5 \text{ tokens} \approx 0.0102\text{ SOL}$, over $70\%$ of a small $<0.015\text{ SOL}$ balance).
    2. **Micro-TP Mathematical Incompatibility:** Target Take-Profit of $+2.0\%$ to $+3.0\%$ on micro-positions ($0.0020 - 0.0050\text{ SOL}$) yields gross gains of only $+0.00004 - 0.0001\text{ SOL}$, while round-trip protocol fees ($1\%$ buy + $1\%$ sell), DEX slippage ($30\%-50\%$), and priority gas fees cost $\sim 0.0003 - 0.0008\text{ SOL}$. Every "winning" trade is actually physically net-negative on-chain.
    3. **High-Frequency Churning Burn:** Rapid auto-fill loops cycling in and out of tokens in seconds multiply fixed transaction and rent friction, rapidly draining liquid SOL reserves.
    4. **Pump.fun Program Anchor Errors (6063 / 6005):** Volatile bonding curve price movement causes slippage / price tolerance failures (`Custom: 6063` or `Custom: 6005`), while still consuming base transaction fees and priority fees.
    5. **Gas Starvation (`InstructionError: [3, {'Custom': 1}]`):** Once unbonded free SOL drops below the minimum required to pay for rent and gas ($\approx 0.0027\text{ SOL}$), all subsequent buy and sell transactions fail completely with insufficient funds.
  - *Hard Rules for Micro-Capital Live On-Chain Trading:*
    - **Never Run High-Frequency Multi-Slot Micro-Scalping on Small Balances ($< 0.10\text{ SOL}$):** Do not promise or run $+2\%$ to $+3\%$ micro-TP loops on micro-capital; on-chain friction will guarantee total capital exhaustion.
    - Strictly enforce `MAX_HOLDINGS_LIMIT = 1` (Single-Slot Sniper Mode) on live on-chain micro-wallets.
    - Always include a `createCloseAccountInstruction` on sells to immediately reclaim the ATA rent back into liquid SOL.
    - When user signals distress / frustration over depleted capital ("rungkad", "habis modal"), immediately execute total emergency shutdown, freeze all daemons, query exact RPC balance, and guide user on manual token sales and ATA rent reclaim via Phantom.

- **Continuous Micro-Scalp Rapid Compounding Loop (+2.0% to +3.0% Full Liquidation):**
  - When the operator requests a high-frequency "TP tipis-tipis balik modal & re-entry" compounding loop:
    1. **Ultra-Fast TP Trigger (+2.0% to +3.0%):** Set the Take Profit threshold to $+2.0\%$ to $+3.0\%$ floating gain.
    2. **100% Full Liquidation:** Execute an immediate $100\%$ full position exit so both original principal and net profit return instantly to liquid SOL cash.
    3. **Immediate Slot Vacancy & Re-Entry:** Splicing the closed coin out of `state.positions` instantly opens a slot in `MAX_HOLDINGS_LIMIT`, prompting the scanner loop to immediately snipe the next incoming Grade A+ breakout token without delay.
    4. **Capital Velocity Maximization:** This minimizes sideways holding exposure, prevents profitable runs from retracing into stop losses, and continuously recycles liquid cash across active momentum breakouts.

- **Strict Verification Protocol for Real On-Chain vs Live-Feed Simulation (Paper vs Real Execution):**
  - When the operator queries whether trading/balance is real or demo ("itu saldo asli kan? bukan demo", "cek bener bener dry run atau simulasi"):
    1. **Private Key Presence Inspection:** Inspect `.env` directly to verify whether `BOT_PRIVATE_KEY` / `SOLANA_PRIVATE_KEY` exists and is validly decoded into `botKeypair`. If the key is purged/disconnected, the engine is operating in **Simulated Execution (Paper Trading)** regardless of UI labels.
    2. **Feed vs Execution Delineation:** Clarify that incoming token prices/market caps are **100% Live Market Data** from Pump.fun/DexScreener, but balance changes are computed mathematically unless real on-chain transaction signatures (`sendTransaction`) are broadcast.
    3. **Direct Solana RPC Balance Confirmation:** Always query the wallet's physical lamport balance via `api.mainnet-beta.solana.com` (`getBalance` & `getSignaturesForAddress`) to give the exact on-chain balance without relying on in-memory state.

- **Emergency Capital Preservation & Stop-All-Entries Mode:**
  - When the user issues an emergency pause or capital lock directive ("stop all entry", "amanin saldo"):
    1. Instantly toggle `isTradingPaused = true` across all auto-buy evaluation loops and instant-snipe endpoints.
    2. Keep the web dashboard (port 8085) and monitoring feeds active so the user can inspect live metrics without risk of new entries.
    3. Ensure all closed positions have their SOL returns fully credited to `cash_sol` (100% liquid cash) and state is synchronized in persistent storage (`live_trades.json`).
- **Strict Quant Score Gate on Auto-Fill Ingestion:**
  - High-frequency auto-fill loops must never buy every incoming token in the feed.
  - Enforce a strict minimum AI Quant Score threshold ($\ge 85/100$) before deducting cash balance and opening a position, preventing high-frequency churn and gas fee erosion from low-conviction tokens.
  - **Mandatory Socials & Minimum Market Cap Filter ($\ge \$6,000$):**
    - *Pitfall (The Low-Score Ingestion & Instant Dev Dump Trap):* Setting loose score filters (e.g. `Score < 10` or accepting micro-caps $<\$6,000$) causes auto-buy loops to ingest 0-second honeypots and dev-dump tokens, leading to catastrophic $-90\%$ to $-99\%$ losses.
    - *Best Practice:* Require verified social links (Twitter/Telegram/Website) and minimum Market Cap ($\ge \$6,000$). Any token lacking socials or below \$6K MC must be immediately rejected (Score = 0 / REJECT).
  - **Emergency Cut-Loss Shield ($-25\%$ Hard Floor):**
    - While normal pullbacks should be tolerated, catastrophic dev dumps exceeding $-25\%$ floating drawdown must trigger an immediate $100\%$ on-chain liquidation to salvage remaining capital rather than letting holdings bleed to $-99\%$.
- **Node.js Initialization Order & Keypair Reference Guard:**
  - *Pitfall (`ReferenceError: Cannot access 'botKeypair' before initialization`):* Defining constants that inspect `botKeypair.publicKey` before `let botKeypair` is instantiated causes unhandled process exit on startup. Always instantiate and decode keypairs (with `bs58.default?.decode || bs58.decode`) before referencing them in wallet constants.
- **Trade History Sequential Replay & Cash Reconciliation:**
  - When state discrepancies arise between active memory and actual on-chain transaction history, reconstruct the exact liquid cash balance by replaying all sequential trade events (deposits, snipes, micro-TPs, trailing exits, stop losses) from the verified anchor point.
- **Detik ke-0 Blind Sniping Failure:** Buying immediately at token creation (even with basic social links) yields >70% loss due to instant developer dumps / fake socials.
- **Momentum & Confirmation Sweet Spot:**
  1. Wait for early developer dump phase to pass (1–2 minutes).
  2. Confirm active community engagement (social link verification + replies/organic trade volume).
  3. Enter when bonding curve shows momentum ($6K–$10K market cap / 15%–30% curve completion).
- **Dual-Stream Multi-Stage Scanner Ingestion (Fresh Trenches + Fast Breakout):**
  - To prevent trading bot stagnation caused by only monitoring high-cap or mature migrated Raydium tokens, implement a **Dual-Stream Ingestion Architecture**:
    1. **Stream 1 (Fresh Trenches):** Poll tokens ordered by `created_timestamp` descending to capture volatile early breakout moves within 30–90 seconds of launch.
    2. **Stream 2 (Active Trades / Breakout Momentum):** Poll tokens ordered by `last_trade_timestamp` descending to capture established volume surges and trend continuations.
    3. Merge and deduplicate streams via a `Map<mint, token>` before scoring and TA pattern evaluation.
- **Portfolio Recycling Workflow (Slow/Stagnant Market Rotation):**
  - When active positions consist of tokens undergoing extended sideways post-migration consolidation (low 5-minute volume) and the user requests a refresh to capture fresh volatile breakout opportunities, execute a complete **Portfolio Recycling routine**:
    1. Close stagnant positions at current market values.
    2. Credit the returned SOL capital back into `SALDO KAS (FREE)`.
    3. Clear holding slots so the scanner/radar immediately captures new high-scoring, high-velocity breakout tokens.
- **Hold-for-Profit Policy & No Arbitrary Time-Based Daur Ulang:**
  - When the user specifies holding positions until profitable, eliminate rigid time-decay recycling rules (such as 45-minute force exits).
  - Implement a **Micro-Profit Trailing Lock (+2.0% to +5.0%)**:
    1. Once price reaches $\ge +2.5\%$, immediately lock Trailing Stop Loss at $+1.0\%$ so any exit is guaranteed in net positive profit (HIJAU/PLUS).
    2. Continue trailing higher as price advances towards standard TP1 (+30%) and TP2 (+60%).
    3. Retain open positions indefinitely until positive profit milestones or real-market emergency stop loss/dump guard triggers are met.
- **Full Take Profit Liquidation & Continuous Re-Cycle Protocol:**
  - *Pitfall (Partial Harvest Dusting & Unrealized Cash):* Holding multi-tier partial fractions (e.g., selling only 50% and leaving 50% as dust) often leaves paper profit trapped in devaluing tokens while confusing operators as to why liquid wallet cash didn't grow.
  - *Best Practice (100% Cash Realization & Dynamic Re-Cycle):*
    1. **Full Liquidation on TP:** When taking profit on micro-scalps (e.g., $+5\%$ to $+8\%$), execute a **$100\%$ full on-chain sell**. This guarantees that $100\%$ of baseline principal plus net profit is immediately returned and consolidated into liquid wallet SOL cash.
    2. **Clean Position Termination:** Immediately remove the closed coin from `state.positions` so the slot is cleanly vacated.
    3. **Continuous Re-Entry Opportunity:** If the same token continues displaying strong volume momentum or breaks out again, the scanner is free to initiate a fresh entry cycle from scratch with newly compounded wallet cash, avoiding trailing drawdown on stagnant leftover tokens.
  - **Manual Harvest via Exact On-Chain Token Sizing:**
    - Always pass exact on-chain integer token balances retrieved from RPC to swap endpoints (`denominatedInSol: false`) to eliminate Anchor Error 6022.
- **Active Capital Re-Cycler (Stagnant / Dead-Volume Rotation):**
  - *Pitfall (Stalled Capital in Sideways Coins):* When trading high-frequency memecoins, coins that fail to pump within the first 3–5 minutes typically lose trading volume, trapping capital and filling available holding slots (`MAX_HOLDINGS_LIMIT`).
  - *Fix:* Implement an active duration gate (e.g. `holdDuration >= 180000 ms` and `PnL < +3.0%`). If a token shows no breakout momentum after 3 minutes, automatically liquidate 100% on-chain to free liquid SOL and immediately rotate into newly launched high-volume breakout candidates.
- **Aggressive High-Frequency Compounding Mode (Targeting Rapid Balance Growth):**
  - When the operator mandates an aggressive balance growth sprint (e.g., reaching $0.05 - 0.1\text{ SOL}$ in a short window):
    1. Lower Take Profit threshold to ultra-fast targets ($+5.0\%$ to $+8.0\%$) with immediate 100% full liquidation on-chain.
    2. Accelerate the evaluation and scanning loop to $1.0\text{ second}$ intervals.
    3. Enable auto-compounding re-cycle so liquid proceeds immediately roll into the next incoming Grade A+ momentum breakout.

- **Exact Token-Account Balance Serialization for PumpPortal Local Trade API:**
  - *Pitfall (Anchor Error 6022 / Amount Mismatch):* Passing string percentage representations (e.g. `amount: '50%'` or `'100%'`) directly to `https://pumpportal.fun/api/trade-local` when `denominatedInSol: 'false'` can fail during transaction simulation on Solana Token-2022 program accounts.
  - *Fix:* Always query exact on-chain token balances dynamically via RPC (`connection.getParsedTokenAccountsByOwner` across both SPL `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` and Token-2022 `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb` programs), compute the exact numerical token balance (`Math.floor(balance * fraction)`), and send the exact numeric integer/float quantity in the `amount` field.

- **Manual Harvest vs Auto-Buy Race Condition Awareness:**
  - When an operator clicks `Panen` / `Close` on the dashboard, cash SOL increases upon swap confirmation. If auto-buy autopilot is active and holding slots are `< MAX_HOLDINGS_LIMIT`, the scanner will immediately deploy the fresh cash into newly detected candidate coins within seconds (making the cash balance rise and immediately drop).
  - Ensure UI status and logs clearly explain this auto-fill cycle or advise operators to pause auto-pilot (`PAUSE AUTOPILOT`) before manual harvesting if they wish cash to sit idle in the wallet.

- **Normal Volatility / Dip Tolerance vs Premature Panic Exits:**
  - *Pitfall:* Treating standard memecoin pullback/dip volatility as an automatic exit signal causes premature liquidation right before reversal rallies.
  - *Rule (User Enforced):* Healthy pullbacks/dips are standard on bonding curves. Do NOT close positions simply on short-term price dips. Analyze charts, volume recovery potential, and dev/smart-money holding before considering any manual action. Maintain positions through normal fluctuations as long as on-chain liquidity and dev safety hold intact, reserving automated exits strictly for positive TP milestones (Fast Scalp +8%, TP1 +25%, TP2 +75%, Moonbag 2.0x) or genuine catastrophic dev dump events.
- **On-Chain Pump.fun Bonding Curve Slippage Hardening & Guaranteed Cash Realization:**
  - *Pitfall (The Floating vs Realized Cash Dilemma):* In simulated/dry-run trading, sell orders always fill at peak prices with zero slippage and zero account rent. In live on-chain trading:
    1. Volatile bonding curve swings reject tight slippage orders (Anchor Error 6002 `0x1772` / `TooMuchSolRequired`), leaving gains trapped on paper while price dumps.
    2. Solana ATA token account rent (`~0.002039 SOL` per token) locks liquid cash across multiple holdings.
    3. Micro-position sizing (`0.001 - 0.005 SOL`) suffers disproportionately from fixed round-trip gas (`~0.0004 SOL` = 8%–40% friction).
  - *Fix (Escalating Slippage & Guaranteed Cash Realization):*
    1. **Dynamic Escalating Sell Slippage:** Configure sell execution with aggressive tier escalation:
       - **Attempt 1:** Slippage **40%** with priority fee `0.00005 SOL`.
       - **Attempt 2:** Auto-escalate to **55%** with priority fee `0.0001 SOL`.
       - **Attempt 3:** Boost to **70%** to guarantee 100% fill under extreme volatility.
    2. **Instant Post-Sell Balance Reconciliation:** Trigger on-chain RPC balance synchronization (`syncRealSolBalance()`) within 2–3 seconds of transaction confirmation to immediately reflect realized SOL cash in the wallet.
    3. **Realistic Tiered Profit Harvesting (Don't Force 500% on Every Token):**
       - **Tier 1 (Fast Micro-Scalp +8.0%):** Sell 50% on-chain immediately upon hitting +8% floating profit. This returns 100% of baseline entry capital back to liquid SOL wallet cash and locks trailing stop at `+2.0%` (eliminating risk).
       - **Tier 2 (Prime Breakout +25.0%):** Sell additional allocation to lock pure profit; raise trailing lock to `+10%`.
       - **Tier 3 (High Momentum +75.0%):** Sell 30% more; lock trailing at `+40%`.
       - **Tier 4 (Mega Moonbag +300% to +500%):** Allow *only* the remaining 20% free-ride runner to aim for +300%–+500% (4x–6x) if the token achieves organic viral momentum. Never force all tokens to hold rigidly waiting for 500%.
- **Mega Moonbag Holding Architecture (+300% to +500% / 4.0x - 6.0x Runner):**
  - *Strategy:* When operators target high-multiple memecoin runs (+300% to +500%), combine early capital de-risking with long-horizon moonbag holding:
    1. **Tier 1 (Fast Scalp +8.0%):** Sell 50% on-chain, immediately returning baseline capital to wallet and locking trailing profit at `+2.0%`.
    2. **Tier 2 (Prime TP2 +75.0%):** Sell 30% on-chain to lock substantial realized profit.
    3. **Tier 3 (Mega Moonbag +300% to +500%):** Keep remaining 20% free-ride bag open through normal chart fluctuations/pullbacks without premature cuts, executing 100% full liquidation only upon reaching +300% to +500% (4x–6x).
- **Slot Capacity Expansion & Fixed Manual Sizing Protocol (e.g. 5 Coins x 0.0010 SOL):**
  - When the operator increases holding slots (e.g. `MAX_HOLDINGS_LIMIT = 5`) while enforcing a fixed manual trade size (`0.0010 SOL`):
    1. Ensure both the scanning engine and manual decision handlers dynamically allocate entries across all 5 concurrent slots.
    2. Enforce the manual trade size override without falling back to dynamic percentages that might over-allocate small balances.
    3. Retain independent state tracking (sparklines, PnL percentages, durations) per position card in the dashboard.
- **Accidental Close & UI Protection (Pure AI Execution):**
  - When users mandate strict, undisciplined-free execution, remove manual Exit action buttons from frontend holding cards to eliminate accidental closures.
  - Let positions be exited strictly by AI rules: Breakeven (+15%), TP1 (+30%), TP2 (+60%), Moonbag Runner, Rebound AI Cut-Loss, 45m Time Decay, or Smart Dump Guard.
- **Dynamic Auto-Compounding Engine (5% Portfolio Allocation Formula):**
  - Calculate dynamic trade sizing on every trade cycle: $\text{Trade Size} = \max\left(0.0010\text{ SOL}, \min(0.05 \times \text{Total Portfolio Value}, \text{Max Allocation Cap})\right)$.
  - Automatically compounds gains after winning trades without compounding risk, and performs anti-bust downsizing during drawdowns.
- **Realistic Profit Targets vs Idealized 2x Pitfall & TP3 Moonbag Full Exit:**
  - *Pitfall:* Waiting for +100% (2.0x) before taking any profit causes profitable trades (+30% to +70%) to round-trip into stop losses because >90% of trench tokens never reach 2.0x. Additionally, leaving remaining fractions (moonbag) unharvested leaves profits unrealized in token form rather than liquid SOL in wallet.
  - *Calibrated Real-Market Strategy:*
    - **Breakeven Shield:** At +15%, move SL to +4% (Risk-Free).
    - **TP1 (Quick Cash):** At +15% to +30%, sell 50% to lock early gains and recover baseline capital.
    - **TP2 (Solid Win):** At +35%, sell 30% (80% total position realized); set Trailing SL to +18%.
    - **TP3 Full Moonbag Harvest (+60% / 2.0x):** Sell 100% of remaining position on-chain so total profits are fully realized back into liquid wallet SOL cash.
    - **Disciplined Hard Stop Loss:** Cut loss at -5% to -8% (tight risk control).
    - **Time-Decay Recycler (4 Menit):** If token is sideways >4m with PnL <1.5%, sell 100% on-chain to free capital slots.
    - **Smart Dump Guard:** Emergency front-run exit if dev dumps >15% supply or price flash-crashes >12% from peak.

## 3. Burner Wallet, Mobile Phantom Keypair & Key Derivation
- Prefer user-controlled burner accounts created in Phantom/Solflare where the user retains the seed phrase.
- **Mobile Phantom Mnemonic Derivation:** Phantom mobile often hides raw private keys for the primary account (`Akun 1`), exposing only the 12/24-word recovery phrase (*Tampilkan Frasa Pemulihan*).
  - Standard derivation path for Phantom Account 1: `m/44'/501'/0'/0'`
  - Scripted derivation using Node.js (`bip39` + `ed25519-hd-key` + `@solana/web3.js`):
    ```javascript
    const bip39 = require('bip39');
    const { derivePath } = require('ed25519-hd-key');
    const { Keypair } = require('@solana/web3.js');
    const bs58 = require('bs58').default || require('bs58');

    const seed = bip39.mnemonicToSeedSync(mnemonic.trim(), '');
    const derived = derivePath("m/44'/501'/0'/0'", seed.toString('hex')).key;
    const keypair = Keypair.fromSeed(derived);
    const privateKeyB58 = bs58.encode(keypair.secretKey);
    console.log('Public Key:', keypair.publicKey.toBase58());
    console.log('Private Key (Base58):', privateKeyB58);
    ```
- Store derived keys strictly in `.env` with restricted filesystem permissions (`chmod 0600`). Never commit secrets to git or combine with client vaults.
- **Port 8085 Web Dashboard Daemon Management:**
  - Check active port binding: `ss -tulpn | grep 8085`
  - Graceful stop / restart: `pkill -f "node.*server_dashboard"` followed by background launch `node server_dashboard.js`
  - Verify dashboard health & authentication: `curl -s -H "Authorization: Bearer trench_secret_token_XXXXXX" http://127.0.0.1:8085/api/data`
- **CEX (Tokocrypto / Pintu / Indodax) On-Ramp:** Explain clearly that CEX accounts cannot serve as DEX execution wallets due to lack of private keys. Route funds via native Solana network withdrawal to the burner wallet.
- **Target Trade Sizing, Micro-Sizing & Flexible Setup:**
  - For standard capital testing: `0.0100 SOL` (~$1.50).
  - For small retail capital tests (e.g. Rp 150.000 – Rp 200.000 / ~0.07 SOL): configure **Ultra-Safe Micro Sizing at `0.0030 SOL` (~Rp 6.000 / $0.35 USD)** per trade.
  - For ultra-micro live tester mode: configure **`0.0010 SOL` (~Rp 2.100 / $0.12 USD)** per trade.
  - **Manual vs Auto-Dynamic Trade Sizing Control:**
    - Provide a zero-friction UI/API endpoint (`POST /api/trade-size`) allowing users to manually set fixed trade size (e.g., `0.0010 SOL`) or switch to `auto` dynamic mode (e.g., 5% of total portfolio value).
    - Ensure manual overrides immediately propagate across the approval queue, instant snipe triggers, and automated execution engines without requiring server restarts or UI redesigns.
- **Holding Capacity Hard Cap & Dual-Gate Enforcement (Auto-Buy + Manual Approval):**
  - When enforcing maximum concurrent positions (e.g., `MAX_HOLDINGS_LIMIT = 2` for micro-capital safety, or `5` for larger capital), gate **both** entry vectors:
    1. Automated snipe evaluation loop (`state.positions.length < MAX_HOLDINGS_LIMIT`).
    2. Manual user approval handler (`handleUserDecision` / `POST /api/decision`), returning an explicit warning when holding slots are full.
  - Slot recycling: Keep incoming opportunities in the pending radar without auto-buying until an existing position exits via TP1/TP2 or Stop Loss.
  - **Dynamic Affordable Sizing (Sub-Target Balance Continuity):**
    - If liquid cash falls below the target manual trade size (e.g. target is `0.0100 SOL` but wallet has `0.0055 SOL` after previous trades), do not stall the engine. Auto-calibrate the entry size dynamically:
      $$\text{Trade Size} = \min\left(\text{Target Size}, \max(0.0030\text{ SOL}, \text{Cash Balance} - 0.0008\text{ SOL})\right)$$
      This ensures continuous sniper execution without failing minimum balance / gas reserve constraints.
  - **Fresh Launch (0–60s) Scoring & Socials Penalty Calibration:**
    - *Pitfall:* Imposing a heavy penalty (e.g. $-40$ points) for missing socials on fresh tokens ($<60\text{s}$ old) will reject 100% of newly created bonding curve tokens before socials are indexed.
    - *Fix:* Soften the early missing-social penalty to $-5$ for fresh launches, calibrate the sweet-spot market cap range to $\$2,500 - \$65,000$, and accept early volume $\ge \$300$ or token age $\le 60\text{s}$ to allow rapid early-curve sniping.
  - **Micro-Capital Position Cap Rule (Max 2 Concurrent Tokens):**
    - For micro-capital wallets ($< 0.050\text{ SOL}$), restrict `MAX_HOLDINGS_LIMIT` to **2 tokens maximum**. This prevents rapid capital exhaustion from cumulative Solana ATA rent locking (`~0.00151 SOL` $\times N$) and keeps free liquid SOL available for sell gas fees.
  - **Single-Slot Sniper Mode & Positive EV Capital Growth Architecture:**
    - When wallet capital is tight ($< 0.030\text{ SOL}$), splitting capital across multiple micro-positions ($0.0050\text{ SOL}$) subjects each trade to severe fixed gas friction ($\sim 8.2\%$ per round trip).
    - *Best Practice (The 4-Pillar Capital Growth Rule):*
      1. **Single-Slot Focus (`MAX_HOLDINGS_LIMIT = 1`):** Concentrate trading into 1 high-conviction position at a time with a more efficient trade size ($0.0100\text{ SOL}$), slashing gas friction to $< 1.5\%$.
      2. **Grade S+ Prime Confluence Ingestion Filter:** Reject 99% of dead/zero-second launches. Enforce proven volume ($> \$1,500$ early volume), GMGN Smart Money multi-wallet inflow, and verified safe dev ownership ($< 8\%$).
      3. **Net-Positive TP Milestones (Free-Ride Mechanics):**
         - **TP1 ($+35\%$):** Sell $50\%$ on-chain. This immediately recovers $100\%$ of baseline SOL capital back into liquid wallet cash.
         - **TP2 ($+75\%$):** Sell $30\%$ on-chain. Secures substantial liquid profit.
         - **TP3 Full Moonbag ($+100\%$ / 2.0x):** Sell $100\%$ of remaining tokens on-chain.
      4. **Complete Elimination of Premature Cuts:** Completely disable tight $-5\%$ stop losses, premature $-6\%$ dump triggers, and 4-minute time decay recycles, granting volatile breakout tokens the necessary breathing room to reach profitable TP levels.
- **The "Tight Cut-Loss & High-Frequency Churn" Capital Bleed Trap:**
  - *Pitfall:* Enforcing ultra-tight stop losses (e.g., $-5\%$ to $-8\%$), premature price-drop dump guards (e.g., drop $-6\%$), and aggressive short time-decay recycles (e.g., force exit after 4 minutes) will rapidly bleed small/micro-capital wallets dry.
  - *Mathematical Reality:* Every round-trip trade (1x Buy + 1x Sell) consumes fixed Solana gas, priority fees, and Pump.fun DEX curve slippage ($\approx 0.0004\text{ SOL}$ total). On a $0.0050\text{ SOL}$ position, a $-5\%$ stop loss actually results in a $\sim 13\% - 15\%$ total net capital drawdown per cycle. Repeating this cycle 5–10 times rapidly depletes the liquid cash balance before volatile tokens have room to rebound and reach profit targets.
  - *Best Practice:*
    1. Eliminate tight $-5\%$ stop-loss and 4-minute time-decay triggers when operating on micro-capital.
    2. Allow positions sufficient volatility breathing room to reach structured Take Profit milestones (**Fast Scalp $+8\%$**, **TP1 $+25\%$**, **TP2 $+50\%$ / $+75\%$**, **TP3 $+100\%$ / 2.0x**).
    3. Restrict automated exits strictly to true on-chain emergencies (e.g., Bloom Dev dumping $100\%$ supply or liquidity curve collapse) and operator-controlled Manual Quick Exit buttons.
- **Strict No-Forced-Close on Chat / Session Instruction Protocol:**
  - *Critical Rule & User Directive:* Never close active open trading positions as a side-effect of receiving chat instructions, conversational prompt updates, or daemon reboots unless the operator explicitly directs a position liquidation ("jual koin X", "close posisi").
  - Auto-exit logic must strictly decouple conversational turns from position lifecycle management so trading positions continue running autonomously without accidental manual cuts.
- **Multi-Tier Fast Scalp Accumulator (+8% Micro Harvest + Trailing Green Lock):**
  - To steadily accumulate liquid cash without premature exits while waiting for explosive 2.0x breakout runners:
    1. **Tier 1 (Fast Scalp $+8.0\%$):** Execute on-chain sell for 50% of the position immediately when floating PnL hits $\ge +8.0\%$. Lock Trailing Stop Loss at $+2.0\%$ (ensures the trade is unconditionally locked in net profit / HIJAU).
    2. **Tier 2 (Prime TP1 $+25\%$ to $+35\%$):** Sell the remaining standard allocation, securing 100% of baseline entry capital back to liquid wallet SOL.
    3. **Tier 3 (Moonbag 2.0x / $+100\%+$):** Allow the final token fraction to ride for extreme upside risk-free.
- **Micro-Capital Gas Overhead vs Take Profit Calibration:**
  - Round-trip on-chain transaction fees (1x Buy + 1x Sell + priority fee $\approx 0.00041\text{ SOL}$) represent $\sim 8.2\%$ of a $0.0050\text{ SOL}$ trade size.
  - On live on-chain micro-capital, micro-scalping at $+2\%$ to $+5\%$ yields negative net PnL after gas.
  - Calibrate live on-chain Take Profit targets higher:
    - **TP1:** $+25\%$ (Sell 50%, lock trailing SL at $+8\%$).
    - **TP2:** $+50\%$ (Sell 30%, lock trailing SL at $+25\%$).
    - **TP3 Full Exit:** $+60\%$ to $+100\%$ (Sell 100% remaining).

## 4. Signal Radar vs Order Execution Decoupling, Fraud Blacklist & Decommissioning
- When operating in zero-cash / awaiting-deposit state (Clean Slate), decouple signal generation from trade execution:
  - Keep the live radar, scoring engine, and Approval Queue active so users can monitor incoming opportunities.
  - Gate only the automated on-chain buy/swap execution behind `cashBalance >= minTradeSize && initialDepositSol > 0`.
- **Clean Wallet Disconnection & Multi-Bot Credential Decommissioning Protocol:**
  - When an operator transitions capital to a different trading asset engine (e.g. XAU/USD Spot DEX) or orders wallet detachment from the memecoin daemon:
    1. **Credential Purging:** Immediately wipe `BOT_PRIVATE_KEY` / `SOLANA_PRIVATE_KEY` from the memecoin bot's `.env` and set permissions strictly (`chmod 0600`).
    2. **Script Disconnection:** Update wallet constants in dashboard servers (`server_dashboard.js`) to `"DISCONNECTED"` to prevent lingering RPC balance lookups or unauthorized transaction construction.
    3. **Daemon Halting:** Kill/pause all background sniper loops and evaluation streams on the memecoin port (e.g. 8085).
    4. **Credential Isolation:** Ensure active keypairs and signing secrets are stored exclusively in the active project directory (e.g. `/home/ubuntu/xau-bot/.env`) to eliminate cross-bot interference or unauthorized signing.
- **Fraud / Non-Owner Wallet Blacklisting Protocol:**
  - If a user reports or discovers an erroneous, third-party, or fraudulent Solana address, immediately apply a hardcoded `BLACKLISTED_FRAUD_WALLETS` Set in the engine.
  - Instantly terminate any RPC sync/polling for that address and purge it from memory, runtime state, and `.env` configs to avoid misrepresenting portfolio balances.

## 5. Multi-Source Ingestion, Technical Chart Analysis & Phantom Terminal Launches
- Combine **On-Chain Security Forensics** with **Technical Candlestick Pattern Reading (TA Engine)** before triggering automated buys:
  - **Candlestick & Volume Pattern Verification:**
    - **Higher-Lows Trajectory (+20):** Confirm the last 3–5 candles establish higher support levels, preventing buys into cascading downtrends.
    - **Bullish Reversal Hammer / Wick Bounce (+15):** Detect long bottom wick rejection confirming buyers stepped in at key support.
    - **EMA 9 > EMA 21 Golden Cross (+10):** Validate short-term trend acceleration crossing above longer-term baseline.
    - **Volume Surge Multiplier $\ge 2.2\times$ (+15):** Ensure green expansion candles are backed by verified fresh volume surges, avoiding low-liquidity fake pumps.
    - **RSI Momentum Check (48–68 Optimal / >78 Overbought Penalty):** Guard against buying market tops. Tokens with $RSI > 78$ must receive a hard penalty (-25) and be excluded from instant auto-buy.
  - **Pump.fun / Raydium RPC & Zero 5m Volume Guard:**
    - Continuously inspect DEX 5-minute trade activity (`m5` buys/sells). Tokens entering dead-volume sideways states ($0 volume in 5m) should be flagged for manual exit or slot recycling.
  - **Phantom Terminal Launches (`trade.phantom.com/launches`):** Holder growth (score bonus if $\ge 30$ unique holders), transaction density ($\ge 50$ txs), and launch age verification to filter out dead volume launches.
  - **Security Audits:** RugCheck top 10 holder distribution + Bubblemaps cluster analysis.
  - **GMGN.ai Smart Money:** Smart money / high win-rate (>65%–78%) whale copy-trade signals.

## 6. Dashboard Financial UI/UX: Direct Live Wallet Sync vs Virtual Cash & Gas Accounting
- **Authoritative Balance Verification Protocol (Preventing Simulated vs On-Chain Discrepancies):**
  - *Pitfall:* Quoting in-memory paper trading tracking or simulated dashboard balance as real wallet funds when the user asks "berapa saldo asli / sisa saldo" or displaying simulated compounding gains in live dashboard.
  - *Mandatory Procedure:*
    1. **Direct RPC Query:** Always verify exact on-chain lamports directly from Solana Mainnet RPC node (`https://api.mainnet-beta.solana.com` -> `getBalance` & `getSignaturesForAddress`) using the actual active wallet address.
    2. **Check Dedicated Obsidian Vault:** Inspect the project's dedicated Obsidian note (`~/Documents/Obsidian Vault/memecoin.md`) for the latest reconciled on-chain state and operational logs.
    3. **Zero Paper Drift in Real Mode (Mandatory RPC Lock):** When the operator mandates real on-chain trading and authentic dashboard display ("tampilan saldo yang bener bener asli, jangan pakai simulasi"), remove all simulated cash balance mathematical accumulators (`cashBalance += returnedSol`). Hardwire the dashboard's cash balance directly to the real-time RPC query `await connection.getBalance(botKeypair.publicKey) / LAMPORTS_PER_SOL` polled every 2 seconds.
    4. **Token-2022 & SPL Holdings Inspection:** When SOL drops after real multi-token entries, inspect `connection.getTokenAccountsByOwner` across both SPL and Token-2022 programs to verify tokens held and explain ATA rent lockup transparently.
    5. **Crystal-Clear Breakdown:** Explicitly delineate between:
       - **Saldo Fisik di Dompet (Phantom / Solscan):** Real on-chain SOL balance available in the blockchain wallet.
       - **Saldo Kas di Dashboard (Paper/Forward Engine):** Strategy performance calculation tracked in `live_trades.json`.
- **Direct Live Wallet Balance vs 4-Box Separation Preference:**
  - *User Preference & Pitfall:* Displaying a separate "Saldo Kas (Free)" alongside "Saldo Wallet" often confuses operators when trading real on-chain funds.
  - *Best Practice:* In Real Mode, streamline the balance overview into **2 Primary Cards**:
    1. `💳 SALDO WALLET`: Directly linked to live Solana RPC on-chain balance (`connection.getBalance(pubKey)` / `LAMPORTS_PER_SOL`), auto-polled every 5 seconds.
    2. `📊 TOTAL P/L (%)`: Cumulative percentage performance & net SOL realized.
  - In Dry-Run / Paper Trading mode, clearly label virtual simulated cash to prevent misinterpreting test gains as real funds.
- **Direct 1-Click External Chart Access & Embedded Mini-Trajectory Charts:**
  - Every active token holding card must feature a direct 1-click button (`📊 Chart`) linking directly to real-time DexScreener candlestick charts (`https://dexscreener.com/solana/${mint}`) or Pump.fun for instant visual price/volume inspection.
  - **Embedded In-Card Real-Time Monitoring Chart (Live Trajectory):** Embed a lightweight inline SVG sparkline/trajectory graph inside each holding card showing real-time price trajectory, current multiplier (e.g. `1.056x`), and peak ATH market cap (`Peak: $23,547`). Use neon green (`#00ffa3`) for positive gains and neon red/pink (`#ff3b69`) for pullbacks, updated smoothly via 2-second polling cycles without full-page reloads.
- **Low-Balance Gas Deadlock on Sell Transactions (`InsufficientFundsForRent` Pitfall):**
  - *Pitfall:* When operating with micro-capital (e.g., `< 0.0500 SOL`) across multiple concurrent token purchases, free liquid SOL in the wallet can drop below `0.0010 SOL`. If `executeOnChainSell` requests a standard or high priority fee (e.g., `0.0002 SOL`), Solana transaction simulation will fail with `{ InsufficientFundsForRent: { account_index: 0 } }` because the wallet cannot prepay the priority gas fee before receiving the swap proceeds.
  - *Fix:*
    1. Set sell `priorityFee` to an ultra-lean value (e.g., `0.00001 SOL`) and configure slippage (e.g., 20%–25%) on sell transactions.
    2. Alternatively, dynamically compute priority fee based on `Math.min(configuredPriorityFee, availableCashSol * 0.5)`.
    3. Ensure `CloseAccount` instructions are executed on 100% full exits to immediately reclaim ATA rent (`~0.00151 SOL` per token account) into liquid SOL.
- **Gas Fee Amortization, Solana Account Rent Exemption & Total P/L Dynamics:**
  - Upfront gas/priority fees (`0.0001 SOL` - `0.0002 SOL` per trade) across multiple buys temporarily impact cash balance.
  - **Solana Associated Token Account (ATA) Rent Exemption Impact:** Each new token bought on-chain locks `0.00151 SOL` to `0.00203 SOL` as Solana account storage rent. With micro-capital (e.g. `0.049 SOL`), holding 5–6 open token accounts temporarily locks `~0.0096 SOL` (~20% of total capital) in rent exemption.
  - Explain clearly to users that:
    1. Cash balance will show lower while funds are deployed in token holdings and ATA rent.
    2. Unrealized high token gains (e.g. +50% to +100%) remain as token balance in the Phantom wallet until Take Profit (100% or partial) is executed.
    - Account rent is refunded automatically to liquid SOL once tokens are fully sold and token accounts are closed.
- **PnL Baseline Synchronization & Live Growth Accounting:**
  - *Pitfall:* When resetting capital baseline after recovery or manual deposit changes, if `initialDepositSol` remains anchored to an older/higher starting balance, the portfolio calculation `((totalPortfolioSol - initialDepositSol) / initialDepositSol) * 100` will show persistent artificial drawdown (e.g. `-60%`) even when active holdings are floating in deep profit (e.g. `+50%`).
  - *Fix:* Always synchronize `initialDepositSol` with the active wallet deposit baseline upon state recovery so `total_growth_percent` accurately reflects actual portfolio performance.
- **Active-Trade Isolated P/L Metric vs Portfolio Lifetime Metric:**
  - *User Preference:* Users frequently demand that top-level dashboard P/L cards reflect ONLY the real-time performance of currently open/active trades (`📊 ACTIVE TRADE P/L`), rather than cumulative lifetime portfolio drift against historical deposits.
  - *Implementation Pattern:*
    - Compute active trade P/L dynamically:
      $$\text{Active P/L } \% = \frac{\sum (\text{Current Value} - \text{Cost Basis})}{\sum \text{Cost Basis}} \times 100$$
    - Keep `CURRENT PORTFOLIO VALUE` percentage strictly synchronized with floating active trade PnL when positions are open, so the UI immediately glows green when the active trade is profitable without showing confusing negative historical offsets.
- **Clean Slate Guard:**
  When resetting to real funds or zero balance state:
  - Enforce `initialDepositSol > 0 && cashBalance >= currentTradeSize` before allowing auto-buys.
  - Reset all state fields (positions, trade logs, active holdings, calendar cells) so boxes strictly display `0.0000 SOL` and 0 holdings until real funds arrive on-chain.

## 7. Paper Trading & Forward Testing Pitfalls
- **Clean Slate Session Reset & Paper Trading Baseline Alignment Protocol (`clear log / mulai dari awal`):**
  - When the operator requests a clean restart ("clear log nya kita mulai lagi dari awal"):
    1. **Storage Reset (`live_trades.json`):** Atomically clear `history: []`, `positions: []`, `pending: []`, and reset `total_trades: 0`, `realized_profit_sol: '+0.0000 SOL'`, and `unrealized_usd: '0.00'`.
    2. **In-Memory Baseline Synchronization:** Align `initialDepositSol` and `cashBalance` in server initialization (e.g. `0.0500 SOL`) with the new paper budget so `total_growth_percent` calculates from the clean baseline rather than stale historical balances.
    3. **Enforce Clean Dry-Run Flag:** Explicitly set `isDryRunMode = true` (or `is_dry_run: true`) to ensure all subsequent entries evaluate under simulation without attempting unsigned on-chain RPC broadcasts.
    4. **Process Restart & Telemetry Verification:** Kill lingering daemon processes on port 8085 (`fuser -k 8085/tcp`), launch `server_dashboard.js` in background, and verify via authenticated `/api/data` request that active positions and history count return exactly `0`.
- **Real On-Chain vs Forward-Test Balance Delineation:**
  - When reporting wallet balances or portfolio status to users, explicitly distinguish between:
    1. **Real On-Chain Balance:** Queried directly from Solana RPC (`connection.getBalance(pubKey)`).
    2. **Simulated / Forward-Test Balance (`live_trades.json`):** The virtual compounding balance tracked by `server_dashboard.js` during forward testing / strategy calibration.
  - Never present paper-trading profits as realized on-chain wallet funds without clearly stating the forward-test mode status.
- **Strict Operator Pin Lock & Security Screen Architecture:**
  - When building mobile/web dashboards on public VPS ports (e.g., port 8085), protect administrative trading actions and confidential portfolio balances with an iPhone-style 6-digit numeric PIN screen (`pinLockOverlay`).
  - Require JWT/Bearer authentication (`trench_secret_token_XXXXXX`) on sensitive endpoints (`/api/data`, `/api/login`, `/api/decision`, `/api/snipe`, `/api/exit`) to prevent unauthorized bot manipulation.
- **Avoid Lookahead Bias:** Never backtest by picking tokens that already succeeded in the past and assuming initial entry. Run forward-testing against live incoming WebSocket/polling events in real-time.
- **Dynamic Cash Flow & Gas Accounting:** Deduct trade allocation + priority fee (`0.0001 SOL`) on entry. Return cash to balance upon hitting TP1 (50%) and TP2 (30%), while tracking open moonbag value separately.

## 8. Live Web Dashboard & Dedicated Knowledge Vault
Before deploying real funds:
1. Run a virtual paper trader subscribing to live WebSocket/polling data (`gmgn_engine.js` / `live_forward_trader.js`).
2. Serve a lightweight live HTML/Bootstrap 5 dashboard (e.g., port 8085) with an auto-refreshing `/api/data` JSON endpoint showing active positions, realtime multiplier/PnL, smart source tag, and TP1/TP2/SL execution history logs.
3. **Interactive Control Switches (ON/OFF Power Toggle & Real vs Dry-Run Mode Switch):**
   - Trading bot dashboards must provide prominent, zero-friction header controls for immediate operator intervention:
     - **Power Switch (Start / Stop):** Toggle `isTradingPaused` via `POST /api/toggle-trading` (`{ action: 'start' | 'stop' }`) to immediately halt opening new positions while leaving open positions monitored.
     - **Trading Mode Switch (⚡ REAL ON-CHAIN vs 🧪 DRY-RUN):** Toggle `isDryRunMode` via `POST /api/toggle-trading` (`{ action: 'toggle_mode' }`) allowing instant transition between live blockchain transaction signing and virtual paper-trading simulation.
     - Ensure order execution wrappers (`executeOnChainBuy` / `executeOnChainSell`) check `isDryRunMode` before invoking RPC transaction signing or third-party execution APIs.
4. **Segmented History & Real vs Dry-Run Log Isolation:**
   - To prevent operator confusion regarding account balance growth and on-chain wallet state:
     - Explicitly tag every trade history item with an `is_real` boolean flag and verifiable transaction signature (`tx`).
     - Provide frontend segmented filter tabs in the transaction log table (`Semua` | `⚡ Real Wallet` | `🧪 Simulasi`).
     - Render distinct visual color-coded badges (`⚡ REAL` in Cyan vs `🧪 SIMULASI` in Gold) on every log entry so real on-chain executions can be verified independently from simulated paper-trades.
     6. **Live Data Stream Forwarding & Slot Stagnation Troubleshooting:**
     - *Pitfall ("Bot Looks Frozen / No Movement"):*
      1. Stagnant legacy positions remaining in `state.positions` fill the `MAX_HOLDINGS_LIMIT` (e.g. 1 slot), causing the evaluation loop to continuously reject new incoming candidate tokens.
      2. Background ingestion feeds (`liveTrenchesFeed`, `liveWhaleRadarFeed`) gathered by polling loops are stored in memory variables but omitted from the `/api/data` JSON response handler, causing the dashboard UI tables to appear empty or static.
     - *Fix:*
      1. Ensure the `/api/data` handler explicitly returns `{ ...state, feed: liveTrenchesFeed, radar: liveWhaleRadarFeed, isTradingPaused, isDryRunMode }`.
      2. In manual or auto-recovery routines, provide an explicit mechanism to clear stale filled slots so the high-scoring sniper engine immediately resumes live evaluation and trade execution.
     7. **Local Timezone Synchronization in Transaction Logs:**
        - *Pitfall:* Cloud VPS instances frequently run on default UTC or cloud provider timezones (e.g. UTC+8 / CST), while the trader monitors from their local timezone (e.g. WIB / UTC+7). Recording timestamps using unformatted server `toLocaleTimeString()` causes confusing time discrepancies in the dashboard log.
        - *Fix:* Standardize server log generation with timezone-aware helpers (`toLocaleTimeString('id-ID', { timeZone: 'Asia/Jakarta', hour12: false })`) and ensure frontend renderers resolve timestamps relative to client device time (`h.time || new Date().toLocaleTimeString('id-ID', { hour12: false })`) so the activity logs match the operator's local clock exactly.
     8. **Precision 3-Column Holding Cards & Zero-Flicker In-Place DOM Updates:**
        - *UI/UX Standard for High-Velocity Trading:*
          - Structure active token cards with a balanced 3-column metric grid: `ENTRY MC`, `CURRENT MC`, and `MULTIPLIER`, paired with a clean inline SVG trajectory sparkline.
          - Provide compact direct action buttons (`Panen 50%` / `Close All`) for manual intervention without navigating into sub-menus.
          - Eliminate screen flickering on fast polling intervals (e.g. 1–2s) by implementing **in-place DOM element updates (`updateCardInPlace`)** rather than wiping and replacing `innerHTML` on every polling tick.
     9. Keep operational notes and research in a dedicated Obsidian note (`~/Documents/Obsidian Vault/memecoin.md`) without mixing with other client vaults.

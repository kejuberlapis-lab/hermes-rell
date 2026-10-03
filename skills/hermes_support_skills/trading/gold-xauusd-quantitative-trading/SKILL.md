---
name: gold-xauusd-quantitative-trading
description: Build and operate XAU/USD gold trading and scalping bots.
version: 1.0.0
license: MIT
author: Hermes Agent
metadata:
  hermes:
    tags: [xauusd, gold, forex, metatrader, mt5, metaapi, smc, scalping, algorithmic-trading]
    related_skills: [crypto-spot-trading-automation, solana-memecoin-trenching-bot]
---

# Gold (XAU/USD) Quantitative Trading & Scalping Architecture

## When to Use
Use when building, backtesting, integrating, or operating automated trading bots, scalping engines, or quantitative models for Gold (XAU/USD) and forex commodities across MetaTrader 4/5 (via MetaApi Cloud SDK / Python bridge), FIX API, or crypto synthetic gold (PAXG/USDT).

## 1. 10-Year Macro & Fundamental Foundations (2016–2026)
- **Real Yields Inverse Correlation (-0.82):** Gold yields no dividend/coupon; its macro price trend is inversely correlated to US 10-Year TIPS Real Yields (US 10Y Nominal Yield minus Breakeven Inflation Expectations).
- **Central Bank Reserves & Geopolitical Floors:** Structural reserve accumulation by non-Western central banks (PBOC, RBI) creates an institutional floor during aggressive monetary tightening cycles.
- **DXY / Dollar Liquidity Divergence:** Dollar index spikes can suppress short-term gold prices, but long-term sovereign debt debasement drives secular bull markets.

## 2. Market Structure, Sessions & Smart Money Concepts (SMC)
- **Session Anatomy & Daily Rhythm (UTC):**
  1. **Asian Session (00:00 – 07:00 UTC / 06:00 – 14:00 WIB):** Compression and consolidation phase. Establishes the Asian Session High (ASH) and Asian Session Low (ASL). Ranges typically stay within $8–$15.
  2. **London Killzone (07:00 – 10:00 UTC / 14:00 – 17:00 WIB):** High volatility expansion ($15–$35). Institutional order flow generates "Judas Swings" (false breakouts sweeping ASH/ASL) followed by true directional trend shifts.
  3. **New York Overlap & Silver Bullet (13:00 – 17:00 UTC / 19:30 – 23:00 WIB):** Deepest liquidity and highest volume. Institutional reactions to US economic releases (CPI, NFP, PPI, FOMC, Retail Sales).
- **Order Flow & Execution Mechanics:**
  - **Liquidity Sweep (BSL/SSL):** Price pushes past key swing points to trigger retail stop losses and build institutional fill liquidity.
  - **Market Structure Shift (MSS) + FVG Mitigation:** Enter only upon a decisive impulse candle creating a Fair Value Gap (FVG), entering at the 50% equilibrium mitigation point.

## 3. High-Probability Quantitative Scalping Models (Empirical Benchmarks)
- **Hybrid SMC + Fresh Supply & Demand at SnR + ATR Adaptive Risk (Validated Model):**
  - **Macro Matrix & Key Levels (H1 / M15):**
    - Identify Big Movements, Key Support & Resistance (Asian High/Low, Session S&R).
    - Map **Fresh Supply (Drop-Base-Drop / Rally-Base-Drop)** and **Fresh Demand (Rally-Base-Rally / Drop-Base-Rally)** zones within Key SnR areas (filters out retail fakeouts).
  - **Execution Trigger & Candlestick Anatomy Confirmation (M5 Execution Timeframe):**
    - Multi-timeframe framework: H1/M15 establishes market structure and valid unmitigated S&D zones; M5 handles execution to filter M1 noise.
    - Setup trigger: Price retests fresh Demand at Support or fresh Supply at Resistance during London / New York Killzones.
    - **Candlestick Confirmation Requirements (Must validate before entry):**
      1. **Bullish / Bearish Engulfing:** Candle body firmly closes engulfing the previous test candle at the zone boundary.
      2. **Rejection Wick ($\ge 40\%$ Shadow):** For BUY setups, lower shadow must be $\ge 40\%$ of total candle range and close firmly above the zone edge (proves institutional liquidity absorption). For SELL setups, upper shadow must be $\ge 40\%$ and close below the zone edge.
      3. **Judas Swing / Liquidity Sweep (London Killzone 14:00–16:00 WIB):** Pin-bar or Swing Failure Pattern (SFP) closing back inside the Asian range after false breakouts above Asian High (ASH) or below Asian Low (ASL).
      4. **Volume Expansion Filter:** Trigger candle volume must exceed the average volume of the preceding 3 compression candles.
  - **Adaptive Stop Loss:** Set strictly to $\text{Zone Extreme} \pm (1.25 \times \text{ATR}_{14})$ to absorb spread fluctuation and prevent stop hunting.
  - **Take Profit & Breakeven Management:**
    - Standard Target: Fixed Risk-to-Reward Ratio (RRR) $1:2.0$ based on Stop Loss distance ($\text{TP} = \text{Entry} \pm (2.0 \times |\text{Entry} - \text{SL}|)$).
    - **Breakeven Shield:** Once floating profit reaches $+1.0 \times \text{ATR}$ (+50 to +70 pips on gold), automatically advance Stop Loss to entry price (0% risk-free guarantee).
  - **Adaptive Pullback Tolerance & Session Dynamics (Preventing Entry Stagnation):**
    - *Pitfall (Static SnR Distance Freeze):* When price is expanding during Asian or London sessions, demanding that price touch an exact static support/resistance price level will cause the bot to stay idle for hours without triggering valid trades.
    - *Fix (ATR-Proportional Dynamic Pullback Gate):* Calibrate entry tolerance relative to live volatility:
      $$\text{Distance to } \text{EMA}_{20} \le (0.75 \times \text{ATR}_{14}) \quad \lor \quad \text{Distance to Key Support} \le (1.50 \times \text{ATR}_{14})$$
      This allows algorithmic scalping engines to execute high-probability pullback entries during active market drift while maintaining strict ATR-based stop-loss envelopes.
  - **Synchronized 1-Second Real-Time Market Polling & Live Ticker Loop:**
    - Configure background server evaluators at `1.0s` and frontend polling intervals at `1.0s` (with `Cache-Control: no-cache` headers). In fast-moving sessions (e.g. London / New York Killzones), a 2.0s+ interval can make prices appear static or unresponsive to operators; a tight 1.0s polling cycle delivers smooth price action updates and instant PnL trajectory feedback.
  - **Forex Sarjana Hybrid S&D at Key SnR with M5 Confirmation:**
    - Reject blind SnR limit orders. Anchor Key Levels on H1/M15, identify fresh unmitigated Rally-Base-Rally (Demand) or Drop-Base-Drop (Supply) zones, and require M5 Bullish/Bearish Engulfing or $\ge 40\%$ Rejection Wick confirmation.
    - Set Stop Loss dynamically outside the S&D boundary plus $1.25\times \text{ATR}(14)$ to prevent spread hunting, locking in a standard $1:2.0$ RRR with a Breakeven Shield at $+1.0\times \text{ATR}$.
  - **Dynamic Pullback Calibration vs Range Freeze:**
    - Broaden pullback tolerance relative to ATR ($\text{distance} \le 0.75 \times \text{ATR}$) to allow responsive execution during active trend expansion rather than demanding strict zero-distance static SnR touches.
  - **M15 Continuous Scalping & Strict Formula Gates (Anti-Premature Auto Re-Entry):**
    - **Micro Lot Sizing (0.01 Lot / Micro SOL):** Using tight risk allocation suitable for high-frequency algorithmic scalping.
    - **M15 Structural Timeframe:** Evaluates dynamic EMA 20/50 trend bias, 14-period ATR volatility, and candlestick wick rejection.
    - **Strict Entry Verification Filters (No Fallback Else Open):**
      - *Pitfall:* Having a loose fallback `else` branch that automatically opens a new position whenever active slots are less than `MAX_POSITIONS` (e.g. immediately after manual Close Profit), causing the bot to open uncontrolled random entries without waiting for technical setup confirmation.
      - *Fix (Mandatory Multi-Indicator Validation):* Order execution MUST only trigger if at least 1 of 3 strict quantitative formulas is confirmed:
        1. *M15 Pinbar Demand Rejection:* $(\text{lowerWick} / \text{candleRange}) \ge 0.40 \land \text{Price} \ge \text{EMA}_{20}$.
        2. *M15 Momentum EMA Breakout:* $\text{PrevClose} > \text{PrevOpen} \land \text{Price} > \text{PrevHigh} \land \text{EMA}_{20} > \text{EMA}_{50}$.
        3. *M15 Oversold Support Rebound:* $\text{RSI}_{14} \le 38 \land \text{Price} > \text{PrevLow} \land \text{Bullish Rebound}$.
        When no condition is met, state must remain strictly in `Waiting for M15 Signal` without opening trades.
    - **Auto Harvest Loop (+5% Target):** Once active trade hits +5.0% profit target (or minimum $5.00 / 2.0x ATR gain), the engine executes an immediate Full Close Take Profit and scans for the next verified setup.
    - **Breakeven Protection (+15 Pips):** Automatically advances Stop Loss to entry price when running profit reaches +15 pips to guarantee zero-risk exposure while targeting the +5% harvest.

## 4. Execution Layer: MetaTrader 4/5 via MetaApi Cloud & Local Dry-Run Simulator
- **Live Local Dry-Run Simulator Pattern (Node.js + REST API on VPS):**
  - For rapid algorithmic testing without external broker dependencies, run a lightweight local simulator on Linux VPS (e.g. port 8086):
    1. Ingest real-time institutional Gold Spot prices via crypto synthetic gold / oracle pricing (e.g. `PAXGUSDT` / Pyth / Binance API).
    2. Dynamically identify active trading sessions (Asian Range, London Killzone, New York Overlap, Rollover Spread Freeze).
    3. Automate SMC EMA 20 Pullback + 1.5x ATR Risk entries and auto-lock the Breakeven Shield once $+1.0 \times \text{ATR}$ (+65 pips) is achieved.
    4. Provide an ultra-clean mobile-ready dark dashboard tracking Live Spot Price, Equity, Realized Profit, Win Rate, Active Positions, and Trade Logs.
    5. **E-Wallet Live Telemetry Card (Phantom / Solana RPC):** Integrate on-chain balance polling (`getBalance` via Solana RPC every 2s) directly beside gold spot charts so operators can track live funding reserves (`SOL` and `USD` value) in real time.
- **Solana On-Chain Gold Trading & Micro-Margin Considerations:**
  - *Critical Liquidity Pitfall on Solana DEX (PAXG / Wrapped Gold):*
    - Wrapped gold tokens on Solana (e.g. PAXG Wormhole `yJujzA2Yft8eo4aV36TGZNB25nwKXhgUHYTNSJx4iZ2`) frequently lack active AMM liquidity on Jupiter and Raydium routing (`The token is not tradable`).
    - Attempting spot DEX swaps for XAU/USD on Solana Phantom wallets leads to failed quotes, routing errors, or swapping SOL to USD stablecoins where PnL tracks SOL/USD currency volatility rather than physical gold spot moves.
    - *Instrument Matching Rule:*
      1. **Physical/Forex Gold (XAU/USD):** Must be executed on liquid CEXs (Binance, Bybit) or Forex brokers via MT4/MT5 / MetaApi Cloud. Never simulate synthetic gold feeds and claim to operators that on-chain Phantom swaps will yield gold price profits.
      2. **Solana Phantom Wallets:** Suitable for liquid native SPL pairs (SOL/USDC Momentum Scalping or Memecoin trenching) where AMM pools have deep verified on-chain liquidity.
  - When bridging XAU/USD execution to Solana on-chain DEXs:
    - **Jalur 1: Spot DEX Limitations:** Wrapped gold lacks direct Jupiter liquidity; if used, require custom liquidity validation probe before deploying capital.
    - **Jalur 2: Perpetual DEX (Drift Protocol / Flash Trade):**
      - Supports 2-way Long and Short execution on oracle-pegged synthetic assets. Requires ~0.06 - 0.08+ SOL minimum to cover subaccount rent (~0.035 SOL) plus trading margin.
      - With small margins (<$10), restrict leverage strictly to 5x - 10x to prevent premature liquidation during normal Judas sweeps.
- **UI Dashboard Standards & Operator Control Patterns for XAU Engines:**
  - **Interactive ON/OFF Switch:** Instant toggle on navbar to halt signal scanning while letting active trades finish safely.
  - **Custom Trade Size Input:** Expose a live manual lot/SOL size input field (e.g. default `0.0010 SOL`) with an instant save action.
  - **Prominent Header Action Buttons & Manual Spot Entry (`[ ➕ OPEN POSISI MANUAL ]`):**
    - Place manual action triggers (e.g. `[ ➕ OPEN POSISI MANUAL ]`) directly in the top sticky navbar beside the `[ BOT ENGINE: ON/OFF ]` toggle rather than buried inside sub-cards, giving operators instant visual access for manual entries.
    - Wire `/api/manual-open` to instantly compute $1.25\times \text{ATR}(14)$ dynamic Stop Loss and $+5.0\%$ / $2.0\times \text{ATR}$ Take Profit at current live spot price, assigning a unique position ID and respecting `MAX_POSITIONS` slot capacity.
  - **Frontend Balance Telemetry, Anti-Cache & Server-Side Initial State Hydration:**
    - *Pitfalls (Stale Cache, Zero-Balance Panic & Phantom State Glitches):* Aggressive browser caching, asynchronous fetch delays, and unpopulated HTML placeholders (`0.000000 SOL` / `$0.00` / `PAUSED (OFF)`) cause operators to see empty positions, duplicate action buttons, or false-zero balances on reload even while backend trading is live.
    - *Robust Implementation Standard:*
      1. **Strict HTTP Anti-Cache Response Headers:** Always serve dashboard root endpoints with:
         `Cache-Control: no-cache, no-store, must-revalidate`, `Pragma: no-cache`, `Expires: 0`.
      2. **Pre-Rendered Initial State:** Render current active positions (Slot 1, Slot 2, Slot 3), live prices, and wallet balances directly inside the server HTML template so the page renders populated content instantaneously on initial load before JavaScript boots.
      3. **Immediate Client-Side Hydration:** Wire client polling via `window.addEventListener('DOMContentLoaded', ...)` at 1.0s–1.5s intervals with safe element exist-checks (`if (elem) elem.innerText = ...`) across all DOM updates to prevent silent script crashes.
      4. **Unified Single-Location Controls & DOM Crash Prevention:** Consolidate controls into clean, dedicated locations rather than scattering duplicate action triggers across both navbar and sub-cards. Use resilient, null-safe rendering loops to prevent JavaScript exceptions from halting dashboard telemetry updates.
      5. **Inline Event Handler Quoting & HTML Entity Safety (`&quot;` vs `\'` Pitfall):** When generating dynamic HTML cards with inline JavaScript handlers (e.g. `onclick="manualClosePosition(...)"`) inside Node.js template literals, never use raw unescaped single quotes (`\'`). In template interpolation, mismatched quotes cause silent browser `SyntaxError` exceptions that immediately terminate subsequent background polling cycles (`fetchState()`). Always use HTML entity escaping (`&quot;`) for string arguments in inline handlers:
         ```javascript
         // Correct, crash-proof inline button generation:
         `<button onclick="manualClosePosition(&quot;${pos.id}&quot;)" class="btn btn-sm">CLOSE</button>`
         ```
      6. **Live Price Tick Animation:** Provide brief color/flash feedback on price updates to visually assure operators that the 1-second real-time market polling is active.
  - **Multi-Slot Entry Scaling & Multi-Entry Architecture (`MAX_POSITIONS = 3` to `5`):**
    - Scale multi-position capacity (e.g. from 2 slots to 3 or 5 simultaneous slots) so the quantitative engine can capture sequential M15 support pullbacks or manual momentum entries at distinct price levels without waiting for initial slots to harvest.
    - Provide individual per-slot telemetry cards with independent `[ 💵 CLOSE PROFIT NOW ]` buttons targeting exact position IDs (`{ id: posId }`) so operators can close specific slots without affecting remaining holdings.
    - **Real On-Chain Balance Realization Mechanics & Liquidity Reality:**
      - *Critical Principle:* Clarify clearly to operators whether an engine is trading synthetic/paper data or real on-chain assets. Never label a price-feed simulator as "Real On-Chain Executor" if no real swap transactions are being broadcast to the blockchain.
      - *Phantom Wallet SPL vs Gold Instruments:* Wrapped gold tokens on Solana DEXs (PAXG) have zero liquidity. If the user expects their Phantom balance to grow, they must be trading liquid native SPL pairs (SOL/USDC or memecoins), whereas physical/forex XAU/USD requires broker APIs (MT4/MT5 / CEX).
      - *Live RPC Balance Sync:* When running real on-chain bots, continuously poll the wallet balance via RPC (`getBalance`) every 2-5s so the dashboard reflects the exact live balance in the user's mobile wallet.
      - In multi-slot operations, ensure state handlers tolerate variable key fields (e.g. `size`, `lot_size_sol`, `size_sol`) to prevent telemetry crashes.
  - **Breakeven Shield ("BE Shield") Operational Standard:**
    - Explain clearly to operators that "BE Shield" automatically moves the Stop Loss to the exact Entry Price once a position reaches moderate running profit, rendering the trade 100% risk-free ($0 downside loss) while allowing it to run toward the +5.0% take-profit goal.
  - **Dedicated E-Wallet Credential Isolation:**
    - When transitioning active capital from another bot (e.g. Memecoin Sniper), completely wipe private keys and disconnect wallet addresses from legacy directories (`/home/ubuntu/trench-bot/.env`), keeping signing keys strictly localized to the active trading environment (`/home/ubuntu/xau-bot/.env`).
  - **Zero-Downtime Hot Configuration Upgrades:**
    - When applying feature enhancements (e.g., expanding position slots, refining UI components, tuning indicators) to live engines, apply changes in-place without toggling off the bot or restarting the daemon process, ensuring active running trades and live floating PnL tracking remain uninterrupted.
  - **Manual Profit Lock (`CLOSE PROFIT NOW` Button) & On-Chain Wire-Up:**
    - *Crucial Implementation Pitfall:* When building a manual close button on a real on-chain engine, never stop at merely updating the in-memory/JSON state and calculating PnL. The `/api/manual-close` endpoint MUST directly trigger the on-chain swap transaction (`executeOnChainSell` / Jupiter v1/v6 DEX swap), sign with the wallet keypair, wait for tx confirmation, and trigger an immediate RPC balance re-sync (`syncPhantomWallet()`). Otherwise, the UI registers a closed trade while the real blockchain wallet balance remains unchanged.
    - *Jupiter DEX Aggregator Integration Standard (Solana Mainnet):*
      - Endpoint Quote: `https://api.jup.ag/swap/v1/quote` with `inputMint` & `outputMint` and `slippageBps`.
      - Endpoint Swap: `https://api.jup.ag/swap/v1/swap` passing `quoteResponse`, `userPublicKey`, and `wrapAndUnwrapSol: true`.
      - Transaction signing with Solana `VersionedTransaction.deserialize(Buffer.from(swapTransaction, 'base64'))` signed by `botKeypair`.
    - *Clean Position State Reset on Full Close / Standby:*
      - When the operator instructs to close all active trades or toggle the engine off ("tutup semua trade"), the system must reset `state.positions = []` and persist `saveState()` atomically to prevent zombie positions from re-appearing upon process reboot or browser polling.
    - *Micro-Scalp Profit vs Gas Fee Economics:* Educate operators that closing tiny floating gains (e.g. $+0.06\%$ on $0.001\text{ SOL} \approx 0.0000006\text{ SOL}$) on-chain will be eaten by network gas fees ($\approx 0.00005\text{ SOL}$). The system must target meaningful $+5.0\%$ to $+10.0\%$ moves to ensure net positive wallet growth.
  - **Precise Timezone Localization (WIB / Asia/Jakarta UTC+7):**
    - Format live digital navbar clocks, position entry timestamps, and execution history logs in explicit `HH:mm:ss WIB` format (`Asia/Jakarta`) to prevent operational confusion between UTC market sessions and local execution time.
- **Cloud Gateway Architecture:**
  - Connect broker MT4/MT5 accounts to a Linux VPS without running heavy Windows emulators/Wine using MetaApi Cloud REST & WebSocket SDK.
  - Detailed Solana DEX spot payload examples and guaranteed slippage ladder scripts are documented in `references/solana_dex_gold_execution.md`.
- **Node.js Integration:**
  ```javascript
  import MetaApi from 'metaapi.cloud-sdk';

  const api = new MetaApi(process.env.METAAPI_TOKEN);
  const account = await api.metatraderAccountApi.getAccount(process.env.METAAPI_ACCOUNT_ID);
  const connection = account.getRPCConnection();
  await connection.connect();

  // Real-time market order with SL & TP
  await connection.createMarketBuyOrder('XAUUSD', 0.01, stopLossPrice, takeProfitPrice);
  ```
- **Microstructure & Execution Safeguards:**
  - **Rollover Spread Freeze (21:00 – 23:00 UTC / 04:00 – 06:00 WIB):** Broker spreads widen dramatically (from 1 pip to 10–25 pips) during day transition. Freeze all new order entries.
  - **High-Impact News Shield:** Pause automated entries $\pm 15$ minutes around Tier-1 news (NFP, CPI, FOMC, Fed Interest Rate Decisions) to prevent extreme slippage.
  - **Daily Circuit Breaker:** Hard stop trading for the session if cumulative drawdown exceeds 3% of account equity.

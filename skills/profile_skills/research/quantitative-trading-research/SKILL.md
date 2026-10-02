---
name: quantitative-trading-research
description: "Use when testing trading rules. Validates market systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: research
    tags: [Trading, Backtesting, Quantitative, Forex, SMC, Risk-Management]
    related_skills: [reverify, anti-hallucinate, grounded-citations]
---

# Quantitative Trading & Strategy Backtesting

A rigorous framework for analyzing price action, Smart Money Concepts (SMC), indicators, and automated grid/hedging trading systems on historical market data without lookahead bias.

## When to Use

- When asked to test, backtest, simulate, or analyze trading strategies, candlestick patterns, or EA bot mechanics on historical Forex, Gold (XAU/USD), or Crypto data.
- When performing multi-timeframe dry-run simulations and validating statistical edges.

## Procedure

1. **Data Ingestion & Multi-Timeframe Resampling:**
   - Stream raw 1-minute (M1) or tick data into SQLite or chunked iterators to prevent memory exhaustion on large datasets (millions of rows).
   - Resample cleanly into higher timeframes (M5, M15, M30, H1, H4, D1) before calculating indicators.

2. **Indicator & Structure Pre-computation:**
   - Compute moving averages (EMA 50/200), ATR volatility buffers, and oscillators (RSI 14) sequentially with zero lookahead bias.
   - Detect structural swings (BOS, CHoCH, Order Blocks, Liquidity Sweeps, and Fibonacci Clusters).

3. **Execution Logic & Filter Enforcement:**
   - **Top-Down Bias:** Filter lower timeframe triggers (M1/M5) strictly against higher timeframe trend bias (H1/H4 EMA 50/200).
   - **Abnormal Candle Gate:** Enforce abnormal candle filters (> 2.0x ATR) to prevent entering at the exhaustion of news spikes.
   - **Session Gating:** Restrict intraday scalping execution to high-liquidity session windows (London & New York Overlap). Avoid 24/7 non-stop execution in low-volume Asian chop.
   - **Asian Range Protocol (07:00–18:00 WIB):** Treat 07:00–13:00 WIB (Asian session) as liquidity mapping (Asian High/Low range) with no active entries; execute Judas Swings and London breakouts primarily between 13:30–18:00 WIB.

4. **Trade Management & Hedging Architecture:**
   - Evaluate trade management models: Single fixed R:R vs Dual Split TP (e.g. Model 4: 50% TP at 1R + SL moved to BEP, 50% runner to 3R-5R).
   - **Grid Hedging Rules:** Never deploy naive 24/7 unhedged grids on trending assets. Enforce strict layer caps (max 3–5 layers), dynamic ATR spacing, and hard basket equity stops (max 1%–3% capital loss per basket).
   - **MQL4/MQL5 Implementation:** Use dual-ticket magic numbers (`Magic_PosA` for 1R and `Magic_PosB` for 3R runner) with dynamic trailing to breakeven upon Pos A closure.
   - **Risk Scaling & Lot Sizing:** Enforce realistic risk parameters ($2,000 capital with fixed 0.01 lot yields $200–$400/month at <3% DD; avoid daily ROI targets >10% that demand dangerous over-leveraging). Refer to `references/gold_scalping_and_ea_playbook.md`.

5. **Performance & Robustness Metrics:**
   - Output Total Trades, Win Rate, Profit Factor, Total R-Gain, Max Consecutive Losses, and Max Floating Drawdown ($ and %).
   - Test sensitivity against broker spread variations ($0.00 to $0.50).

6. **Documentation & Deliverable:**
   - Write clear markdown reports to the project vault with comparative metric tables and step-by-step dry-run scenarios.

## Pitfalls

- **24-Hour Non-Stop Intraday Execution:** Running scalping algorithms across 24 hours unfiltered bleeds capital in the Asian session due to low-volume ranging false breakouts; gate execution to London/NY overlap.
- **Continuous Flip Stop-and-Reverse on M1:** Flipping between Buy and Sell Stop orders on lower timeframes triggers repeated whipsaw cutlosses (>5,000 cuts in ranging markets), causing rapid margin depletion.
- **Naive grid trading on trending commodities:** Unfiltered grids accumulate catastrophic floating drawdowns during macro expansions; always enforce higher-timeframe trend alignment and hard basket cutloss.
- **Lower timeframe confirmation paradox:** Waiting for secondary candle confirmation on M1–M5 often degrades the entry price and widens Stop Loss, lowering the net Profit Factor; always benchmark raw vs confirmed signals.
- **Ignoring spread and execution friction:** High-frequency M1 scalping is hyper-sensitive to spread; always include realistic broker commission and spread ($0.20–$0.30 on Gold) in simulations.
- **Fabricating backtest stats:** Never invent sample counts or win rates; run deterministic scripts against real datasets and cite exact figures.

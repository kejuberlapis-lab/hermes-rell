---
name: market-backtesting
description: "Use when backtesting trading data. Runs deterministic tests."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Trading, Backtest, Quantitative, Market-Data, Risk-Management]
    related_skills: [reverify, anti-hallucination-gates, grounded-citations]
---

# Market Backtesting & Strategy Validation

A quantitative framework for validating mechanical trading strategies against multi-year tick and candlestick data without lookahead bias or fabricated performance.

## When to Use

Use when testing, verifying, or simulating mechanical trading rules, grid hedging, Smart Money Concepts (SMC), or algorithmic trade management models against historical financial market data (XAU/USD, Forex, Crypto, Equities).

## Procedure

1. **Multi-Timeframe Data Aggregation:**
   - Stream high-resolution raw data (1-minute or tick) and resample deterministically into M5, M15, M30, H1, H4, and D1 bars.
   - Cache precomputed indicators (EMA, ATR, RSI) into indexed local storage (e.g. SQLite) to enable high-speed iteration.

2. **Realistic Friction Modeling:**
   - Always include realistic bid-ask spread and round-turn commissions per lot.
   - Do not test with zero spread unless explicitly auditing pure signal edge.

3. **Execution Modeling:**
   - Verify trade entry on the subsequent bar open or limit/stop price hit.
   - Track both balance and floating equity at every bar to accurately measure Maximum Floating Drawdown.

4. **Multi-Timeframe Alignment:**
   - Anchor trade direction to the Higher Timeframe (H1/H4) trend filter before evaluating Lower Timeframe (M1/M5) entry triggers.

5. **Risk Gate & Position Management:**
   - Enforce hard basket stop losses and maximum open layer constraints to prevent runaway floating drawdowns during strong macro trends.
   - Enforce session-gated testing (segmenting London/New York vs Asian sessions) to isolate true momentum edge from low-volume chop.

## Pitfalls

- **24-Hour Non-Stop Low-Timeframe Testing:** Intraday scalping on M1/M5 without session gating produces deceptive drawdowns driven almost entirely by Asian session low-volume range traps.
- **Whipsaw Bleed in Rhythm/Flip Trading:** Continuous stop-and-reverse or naive grids without higher timeframe trend filters bleed capital through repeated spread and micro-chop cutlosses.
- **Ignoring Drawdown:** Evaluating strategies solely on closed trade balance without tracking floating equity masks catastrophic margin risk.
- **Overfitting Low Timeframes:** High win rates on M1 without saturation/exhaustion triggers (e.g. RSI oversold in demand zones) fail when volatility shifts.

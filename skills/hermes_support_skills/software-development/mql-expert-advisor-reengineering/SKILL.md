---
name: mql-expert-advisor-reengineering
description: "Use when re-engineering, cloning, or auditing MQL4/5 EAs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [MQL4, MQL5, Expert-Advisor, Reverse-Engineering, Trading-Bot, MetaTrader, MetaEditor]
    related_skills: [automated-trading-systems, quantitative-trading-research, remote-desktop-environments]
---

# MQL Expert Advisor Re-Engineering & Unlimited Source Cloning

A standardized methodology for reverse-engineering compiled MetaTrader 4 / MetaTrader 5 Expert Advisors (`.ex4`, `.ex5`), extracting hidden strategy parameters, stripping artificial trial / date locks, and cloning them into clean, lifetime, production-grade `.mq5` / `.mq4` source code.

## When to Use

- When analyzing third-party compiled EA binaries (`.ex4`, `.ex5`) with unknown or trial constraints.
- When extracting trading parameters, lot sizing math, and risk models from binary string tables and associated `.set` preset files.
- When cloning and upgrading proprietary or trial EAs into 100% lifetime unlimited, multi-account, and multi-broker source code (`.mq5`).
- When headlessly compiling `.mq5` source code into `.ex5` binaries using MetaEditor CLI in Linux / Wine environments.

## Procedure

1. **Binary Metadata & String Extraction:**
   - Inspect the `.ex5` header magic (`EX5\x02` for modern 64-bit builds).
   - Scan for UTF-16LE and ASCII string literals to extract:
     - Version strings (e.g. `v1.80`, `v4.00`).
     - Trial identifiers (e.g. `TRIAL`, `DEMO ONLY`, `EXPIRED`).
     - Contact numbers, author metadata, and license markers.
   - Locate and parse associated `.set` preset files in `MQL5/Experts/Advisors/` or user directories to extract explicit parameter keys and default values:
     - `InpInitialLot`, `InpMartiMulti`, `InpMaxLayers`, `InpInitialDist`, `InpLayerDist`, `InpTargetProfit`, `InpTargetLoss`, `InpUseTrailing`, `InpMagicNumber`.

2. **Strategy Archetype Identification:**
   - **Bidirectional Straddle Grid:** Places initial `Buy Stop` and `Sell Stop` orders around market price (`InpInitialDist`), followed by geometric (`InpInitialLot * (Multi^Layer)`) or arithmetic layer scaling when price trends.
   - **Money-Target Basket Exit:** Evaluates total floating P/L across all tickets (`PositionGetDouble(POSITION_PROFIT) + Swap + Commission`). Once floating profit $\ge$ `InpTargetProfit` ($ USD), executes `CloseAllPositions()` and `DeleteAllPendingOrders()` to start a fresh cycle.
   - **Trend / Momentum Reversal Grid:** Uses EMA Fast/Slow crosses or RSI overbought/oversold levels to trigger initial market entries, then manages averaging recovery grids.

3. **Unlimited Source Architecture (`.mq5`):**
   - **Strip Artificial Locks:** Omit all hardcoded expiration dates (`TimeCurrent() > D'YYYY.MM.DD'`), account number whitelists (`ACCOUNT_LOGIN`), and demo mode restrictions (`ACCOUNT_TRADE_MODE_DEMO`).
   - **Structured Group Inputs:** Organize parameters cleanly using MQL5 `input group`:
     - `=== 1. PENGATURAN GRID & LOT ===`
     - `=== 2. PENGATURAN TARGET CUAN (MONEY) ===`
     - `=== 3. PENGATURAN TRAILING & BEP ===`
     - `=== 4. PENGATURAN STRATEGI ENTRY ===`
     - `=== 5. PENGATURAN WAKTU TRADING (WIB) ===`
     - `=== 6. PENGATURAN SISTEM & DASHBOARD ===`
   - **Enterprise Protections:** Embed Auto BEP (Break-Even Point), Trailing Stop, Daily Profit Target Cut-Off, Max Loss Protection, Max Lot Safety Cap, and Weekend Friday Close-All logic.
   - **Visual On-Chart GUI Dashboard:** Render non-intrusive lightweight chart labels (`OBJ_LABEL`, `OBJ_RECTANGLE_LABEL`) displaying real-time Balance, Equity, Floating P/L, Layer counts, Target Progress, and EA status.

4. **Headless Compilation via Wine MetaEditor:**
   - Compile source files into binary `.ex5` directly from the Linux terminal without launching GUI instances:
     ```bash
     wine "/home/ubuntu/.wine/drive_c/Program Files/MetaTrader 5/MetaEditor64.exe" /compile:"Z:\path\to\EA.mq5" /log:"Z:\path\to\compile.log"
     ```
   - Verify the generated `compile.log` displays `Result: 0 errors, 0 warnings`.
   - Deploy both `.mq5` (source) and `.ex5` (binary) to `/home/ubuntu/Desktop/` and `C:\Program Files\MetaTrader 5\MQL5\Experts\Advisors\`.

## Pitfalls

- **Compiled `.ex5` Bytecode Encryption vs Algorithmic Assumptions:** Compiled `.ex5` files use VM bytecode and anti-tamper encryption; raw entry algorithms cannot be decompiled deterministically from binary alone. Never assume or fabricate specific entry indicators (e.g., straddle vs MA cross vs RSI) without verifying the EA's Input parameters (via `F7` Inputs tab screenshot) or explicit strategy rules with the user.
- **Trial Expiration Blind-Spots:** Commercial trial EAs often silently stop managing open positions when the expiration date passes, leaving open trades floating without stop losses. Always re-engineer trial bots into full source code before live deployment.
- **Interfering with Running MT5 Terminal:** Never kill or restart `terminal64.exe` to compile or install new EAs. MetaEditor CLI compiles completely out-of-process without touching running trading sessions. Once compiled, refreshing the Navigator panel in MT5 (`Navigator -> Right Click -> Refresh`) immediately loads the new EA without stopping active charts.
- **Lot Step Normalization Error:** Direct multiplication of lot sizes can generate illegal fraction sizes that brokers reject (`Trade error: Invalid volume`). Always normalize lots against symbol specifications (`LotsMin`, `LotsMax`, `LotsStep`):
  ```mql
  double lot_step = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
  if (lot_step > 0) lot = MathFloor(lot / lot_step) * lot_step;
  ```
- **Basket Close Slippage on Fast Markets:** Closing multiple grid orders one-by-one can take several ticks during high volatility. Always loop backwards (`for (int i = PositionsTotal() - 1; i >= 0; i--)`) and immediately delete pending orders after positions close to prevent unintended order execution.

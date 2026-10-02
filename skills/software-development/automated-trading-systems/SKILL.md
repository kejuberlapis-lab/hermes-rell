---
name: automated-trading-systems
description: "Use when developing, testing, or deploying trading bots."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [MQL4, MQL5, MetaTrader, Algorithmic-Trading, VPS, Expert-Advisor, Wine]
    related_skills: [quantitative-trading-research, reverify, zero-hallucination-coder]
---

# Automated Trading Systems (MQL4 / MQL5 & MetaTrader Deployment)

A standardized operational framework for engineering, validating, backtesting, and deploying automated Expert Advisors (EAs) on MetaTrader 4 / MetaTrader 5 platforms, including headless and GUI Linux VPS setups.

## When to Use

- When authoring, debugging, or optimizing MQL4/MQL5 Expert Advisor source files (`.mq4`, `.mq5`).
- When implementing multi-timeframe indicator filters, dynamic ATR risk models, and split-ticket trade management algorithms.
- When configuring Linux servers (Ubuntu) with Wine, XRDP, and XFCE to run MetaTrader 24/7.
- When validating trading algorithms via deterministic Python backtesting engines against multi-year historical datasets.

## Procedure

1. **Architecture & Strategy Design:**
   - **Multi-Timeframe Filtering:** Query higher timeframe context (e.g. H1 EMA 50/200) inside `OnTick()` on new lower timeframe bar opens (`Time[0] != lastBarTime`) to avoid duplicate signal evaluation.
   - **Signal & Confirmation Logic:** Require physical candle close confirmations (e.g., Bullish/Bearish Engulfing followed by a directional confirmation bar).
   - **Volatility Gating:** Measure current candle range against historical ATR (`c1_range > MaxCandleATRRatio * atr`). Skip entries during abnormal spikes (news releases) to prevent excessive initial stop distances.
   - **Execution Constraints:** Enforce `MaxSpreadPoints` check (`(Ask - Bid) / Point <= MaxSpread`) before sending orders.

2. **Model 4 Split Trade Management (Dual-Ticket Engine):**
   - Place two simultaneous orders with distinct magic numbers (`MagicNumber_PosA` for TP1, `MagicNumber_PosB` for TP2 runner).
   - In `OnTick()`, scan open orders. If Pos A has closed in profit (TP1 hit at 1.0R), execute `OrderModify` / `PositionModify` on Pos B to move its Stop Loss to the exact entry price (`OrderOpenPrice`), locking in zero risk for the runner.

3. **Compiled EA (`.ex4`/`.ex5`) Inspection & Parameter Recovery:**
   - **Binary Limitation:** `.ex5` and `.ex4` files are compiled bytecodes protected by MetaQuotes encryption and cannot be decompiled directly into clean C++ source.
   - **Parameter Extraction:** Extract strategy parameters, lot sizing, and risk thresholds by analyzing associated `.set` preset files in `MQL5/Experts/Advisors/` or inspecting embedded UTF-16LE / ASCII string tables in the binary.
   - **Re-Engineering Workflow:** Extract the input parameters (e.g. `InpInitialLot`, `InpMartiMulti`, `InpLayerDist`, `InpTargetProfit`, `InpUseTrailing`), reconstruct the mathematical model (e.g., Bidirectional Grid / Pending Stop Ladder), and author a clean, unencumbered `.mq5` source implementation.

4. **Time-Gating & Broker GMT Translation:**
   - Always translate server time (`TimeCurrent()`) to the target trading session (e.g. WIB / UTC+7) using a configurable `BrokerGMTOffset`:
     ```mql
     int wibHour = (TimeHour(TimeCurrent()) - BrokerGMTOffset + 7) % 24;
     if (wibHour < 0) wibHour += 24;
     if (wibHour < StartHourWIB || wibHour >= EndHourWIB) return;
     ```
   - Provide an optional `CloseAllAtEndHour` boolean flag to liquidate floating positions upon session end.

4. **MetaTrader Linux VPS Deployment (Wine 10 Pinning & Silent Runtime Setup):**
   - **Wine Version Selection:** Always pin and install **Wine 10** (`winehq-stable=10.0.0.0~noble-1`, `wine-stable`, `wine-stable-amd64`, `wine-stable-i386:i386`). Wine 11+ triggers MetaTrader's internal anti-debugger check, resulting in fatal runtime errors (`A debugger has been found running in your system`).
   - **Apt Package Holding:** Lock Wine package versions immediately after installation to prevent automatic updates:
     ```bash
     sudo apt install --allow-downgrades -y winehq-stable=10.0.0.0~noble-1 wine-stable=10.0.0.0~noble-1 wine-stable-amd64=10.0.0.0~noble-1 wine-stable-i386:i386=10.0.0.0~noble-1
     sudo apt-mark hold winehq-stable wine-stable wine-stable-amd64 wine-stable-i386
     ```
   - **Pre-Install Mono & Gecko Runtimes:** Download and install Wine Mono and Gecko MSI packages silently to prevent modal pop-ups during automated execution:
     ```bash
     wine msiexec /i wine-mono-9.4.0-x86.msi /qn
     wine msiexec /i wine-gecko-2.47.4-x86_64.msi /qn
     ```
   - **Installer Execution & Distribution:** Execute `wine mt5setup.exe /auto` and copy `.mq4`/`.mq5` source files directly to `C:\Program Files\MetaTrader 5\MQL5\Experts\`.

5. **XRDP & Desktop Environment Ultra-Low Latency Tuning:**
   - **Disable XFCE Compositing & Animating:** Turn off drop-shadows, vblank sync, cursor blinking, and UI animations to eliminate full-screen redrawing and ensure instantaneous RDP cursor tracking:
     ```bash
     DISPLAY=:10 xfconf-query -c xfwm4 -p /general/use_compositing -s false
     DISPLAY=:10 xfconf-query -c xfwm4 -p /general/vblank_mode -s off
     DISPLAY=:10 xfconf-query -c xsettings -p /Gtk/EnableAnimations -s false
     DISPLAY=:10 xfconf-query -c xsettings -p /Gtk/CursorBlink -s false
     DISPLAY=:10 xfconf-query -c xfce4-desktop -p /desktop-icons/file-icons/show-thumbnails -s false
     ```
   - **XRDP Protocol & Compression (`/etc/xrdp/xrdp.ini`):** Configure `max_bpp=24`, `crypt_level=low`, `tcp_nodelay=true`, `tcp_keepalive=true`, `use_compression=yes`.
   - **Linux Kernel TCP Tuning:** Set `net.core.rmem_max=16777216`, `net.core.wmem_max=16777216`, `net.ipv4.tcp_notsent_lowat=16384`, `net.ipv4.tcp_slow_start_after_idle=0`, `net.ipv4.tcp_fastopen=3`, and `vm.swappiness=10`.

6. **Risk Scaling & Client Communication:**
   - Always present realistic mathematical return projections based on fixed lot sizes (e.g., 0.01 lot on Gold produces $10–$20/day on 100-pip moves, netting $200–$400/month on $2,000 capital with <3% DD).
   - Warn against unrealistic daily return expectations (>10%/day) that require over-leveraging and violate risk-of-ruin thresholds.

## Pitfalls

- **Wine 11 Anti-Debugger Trigger:** Upgrading to Wine 11+ crashes MT5 installers and terminals with `"A debugger has been found running in your system. Please, unload it from memory and restart your program"`. Pin Wine explicitly to version 10.0.0 and lock package upgrades with `apt-mark hold`.
- **RDP Screen Redraw Overhead (Compositing):** Leaving XFCE compositing enabled forces full-screen frame retransmissions over XRDP, causing severe cursor latency and stuttering; always disable `use_compositing`, `vblank_mode`, and reduce color depth to 24-bit (`max_bpp=24`).
- **Evaluating signals mid-bar:** Evaluating indicators on intra-bar tick fluctuations causes false trigger spam; always gate execution to `iTime(Symbol(), Period(), 0) != last_bar_time`.
- **Hardcoding server hours:** Broker server clocks vary between GMT+0, GMT+2 (winter), and GMT+3 (summer); never hardcode raw server hours without a configurable `BrokerGMTOffset`.
- **Ignoring SL buffer under spread:** On SELL orders, failing to add spread to the swing high stop loss (`SwingHigh + ATR + (Ask - Bid)`) results in premature stop-outs during spread widening.
- **Single-order runner management:** Trying to partial-close a single ticket across different MT4/MT5 brokers often fails due to broker-specific execution policies; use dual split tickets with distinct magic numbers instead.
- **Headless Wine hangs:** Launching Wine GUI installers in terminal sessions without an X server (`DISPLAY` or `xvfb-run`) hangs indefinitely; always initialize Wine prefixes headless with `WINEDLLOVERRIDES="mscoree,mshtml=" wineboot --init` or via XRDP/Xvfb.

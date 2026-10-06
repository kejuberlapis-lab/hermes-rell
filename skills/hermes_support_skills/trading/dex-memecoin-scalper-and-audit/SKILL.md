---
name: dex-memecoin-scalper-and-audit
description: "Use when trading memecoins, auditing GMGN, or DEX scalping."
tags: [memecoin, gmgn, dex, scalping, solana, polygon]
version: 1.0.0
author: Rell de Hermes
---

# DEX Memecoin Scalper & GMGN Audit

## Overview
Class-level procedural guide for memecoin screening, on-chain risk auditing (GMGN 5-Gates Framework), DEX execution routing, and multi-cycle scalping profit management.

## 1. On-Chain Screening & The 5-Gates GMGN Audit
Never execute an entry without verifying the 5 mandatory security gates on DexScreener / GMGN:
1. **Top 10 Holder Distribution < 30%:** Prevents single-whale or insider cluster dumps.
2. **Liquidity Pool (LP) 100% Locked / Burned:** Eliminates dev rugpull risk.
3. **Rug Ratio / Risk Score < 0.10:** Rejects toxic contracts and unverified bytecode.
4. **Liquidity Pool > $10,000:** Shields trade entries and exits from devastating slippage.
5. **Mint Authority Revoked:** Guarantees devs cannot print secondary supply into the pool.

## 2. DEX Execution vs Mobile Wallet Oracle Pitfalls
- **Oracle Delay vs AMM Reality:** Mobile wallet homepages (Phantom, MetaMask) fetch aggregate feeds (CoinGecko/CoinMarketCap) which frequently lag or display brief illiquid CEX spikes. Actual swap value is dictated solely by the on-chain AMM pool reserves (QuickSwap, Raydium).
- **Aggregator Spread Avoidance:** In-app wallet swap tools route through multi-hop aggregators with convenience fees. When executing on thin liquidity, connect directly to the native DEX dApp interface to avoid slippage degradation.

## 3. Post-Pump Profit Harvesting & Rotation Cycle
- **+150% to +300% Harvest Rule:** When a momentum trade explodes, liquidate 70%-100% into the native gas token ($SOL, $POL) immediately. Do not hold full size through distribution phases.
- **Trailing Shield (Breakeven Lock):** Move Stop Loss to Entry (+0%) the moment floating profit hits +10% to guarantee zero capital loss.
- **Cycle 2 Allocation Discipline:** Maintain 10%-15% of portfolio in base gas currency as a dedicated gas buffer and sniper reserve.

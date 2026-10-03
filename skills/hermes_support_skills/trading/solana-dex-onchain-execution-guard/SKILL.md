---
name: solana-dex-onchain-execution-guard
description: "Rules and fee guards for micro-capital Solana DEX bots."
tags: [solana, dex, pump-fun, fee-economics, trading-safety, on-chain]
version: 1.0.0
---

# Solana DEX On-Chain Execution Guard

## Overview
Standard operational rules, mathematical constraints, and execution safeguards for running autonomous or semi-automated trading engines on Solana DEXes (Pump.fun, Raydium, Meteora).

## 1. On-Chain Fee Economics & The Micro-Capital Trap
- **Fixed Network & Protocol Friction:**
  - Round-trip transaction cost (Buy gas + Sell gas + Priority fee + DEX pool fee + Slippage) is fixed at approximately **`0.0008 - 0.0012 SOL`**.
- **The Micro-TP Trap (+2% to +5%):**
  - On micro-entries (e.g. `0.0020 SOL`), a +3% gross gain equals `+0.00006 SOL`.
  - Net return: `+0.00006 - 0.00090 = -0.00084 SOL` (**Guaranteed Net Loss**).
  - **Rule:** Never apply micro-scalping (+2% to +5% TP) on position sizes smaller than `0.05 SOL`. For micro-positions (`0.002 - 0.010 SOL`), target high-reward setups (`+50% to +100%`) or abort.

## 2. Associated Token Account (ATA) Rent Storage
- **Rent-Exempt Reserve:** Every newly created token account locks **`~0.002039 SOL`** (SPL) or **`~0.001514 SOL`** (Token-2022) into blockchain state storage.
- **Gas Starvation Pitfall:**
  - Opening 5 slots on a `0.015 SOL` wallet locks `~0.0102 SOL` in rent, leaving `<0.005 SOL` for gas, triggering immediate transaction failures.
- **Remedy:**
  1. Always enforce `MIN_SOL_RESERVE` (minimum `0.0050 - 0.0100 SOL`) strictly isolated from trading funds.
  2. Implement automatic `createCloseAccountInstruction` or rent reclamation after 100% sell to return locked SOL back to the liquid cash balance.

## 3. Micro-Capital Operational Policy (< 0.05 SOL)
- **Slot Capacity:** Strictly lock to **1 active slot** maximum (no multi-slot replenishment).
- **Mode:** Manual approval / user-command triggered only (`entry` command). Prohibit autonomous churning.
- **Strict Prohibition on Rapid Churning / Capital Recycling:**
  - Never implement time-based auto-recyclers (e.g. 3-minute stagnation auto-sell) on micro-capital. Rapid buy/sell cycles rapidly exhaust gas fees and lock liquidity into ATA rent, causing rapid balance drain.
- **Token Forensics:** Metadata alone (MC, replies) cannot prevent 5-second insider bundle dumps on Pump.fun bonding curves; enforce hard stop-loss (`-20% to -30%`) to protect principal.

## 4. Emergency Emergency Token Account Closing & Rent Recovery
- When stopping an on-chain bot or performing account recovery:
  1. Sell all remaining non-zero token balances on DEX (PumpPortal/Jupiter).
  2. Inspect both SPL Token (`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`) and Token-2022 (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`) programs for zero-balance accounts.
  3. Dispatch `createCloseAccountInstruction` across all empty accounts to reclaim `~0.0015 - 0.0020 SOL` per account directly back to the native wallet balance.
  4. Immediately purge private keys from `.env` and disk once recovery is complete.

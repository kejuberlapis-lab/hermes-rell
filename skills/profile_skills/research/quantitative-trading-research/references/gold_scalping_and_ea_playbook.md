# Gold (XAU/USD) Intraday Scalping & EA Architecture Playbook

## 1. Session Framework (WIB / UTC)

| Time Window (WIB) | Time Window (UTC) | Session Name | Primary Objective & Behavior |
|:---|:---|:---|:---|
| **07:00 – 13:00** | 00:00 – 06:00 | Asian Session | **Liquidity Accumulation & Mapping Only.** Mark Asian High (AH) & Asian Low (AL). Do not execute blind breakouts. |
| **13:30 – 15:00** | 06:30 – 08:00 | Frankfurt / Pre-London | **Judas Swing / Liquidity Sweep.** Watch for fake breakouts above AH or below AL followed by M5/M1 rejection. |
| **15:00 – 18:00** | 08:00 – 11:00 | London Open Expansion | **Primary Scalping Execution Window.** Trade confirmed liquidity sweeps back to range equilibrium or London trend breakouts. |
| **19:00 – 23:00** | 12:00 – 16:00 | New York Overlap | **Macro Trend Follow-Through.** Highest directional volume; best for 3R–5R runners. |

---

## 2. Risk & Lot Sizing Matrix for Gold ($2,000 Capital)

| Lot Size | Value per Pip ($0.10 Move) | Risk on 20-Pip SL | Expected Monthly Return (20 Days) | Risk Classification |
|:---:|:---:|:---:|:---:|:---|
| **0.01** | $0.10 | $2.00 (0.10% equity) | $200 – $400 (10% – 20%) | **Ultra Safe / Prop Firm Ready** (Max DD < 3%) |
| **0.05** | $0.50 | $10.00 (0.50% equity) | $500 – $1,000 (25% – 50%) | **Balanced Growth** (Max DD < 8%) |
| **0.10** | $1.00 | $20.00 (1.00% equity) | $1,000 – $2,000 (50% – 100%) | **Active Scalper** (Max DD < 15%) |
| **0.50+** | $5.00+ | $100.00+ (5.0%+ equity) | Unstable / High Ruin Risk | **Extreme Risk / Not Recommended on $2k** |

---

## 3. MQL4/MQL5 Dual-Position Architecture (Model 4)

When automating M5 scalping in MetaTrader:
1. **Open Two Split Orders:**
   - Order A: `MagicNumber = Base + 1`, `TP = Entry + (1.0 * RiskDistance)`
   - Order B: `MagicNumber = Base + 2`, `TP = Entry + (3.0 * RiskDistance)`
2. **OnTick Monitoring:**
   - Check if Order A has been closed (hit TP).
   - If Order A is closed and Order B is still open with Stop Loss at initial level, modify Order B's Stop Loss to `OrderOpenPrice()` (Breakeven).
   - Enforce `MaxSpreadPoints` filter (<= 35 points on Gold) to prevent execution during spread widening.

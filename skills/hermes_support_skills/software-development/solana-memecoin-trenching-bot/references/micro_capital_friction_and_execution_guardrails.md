# Micro-Capital Friction & Execution Guardrails on Solana DEX

## 1. The Fixed-Fee Floor vs Micro-Take-Profit Reality
On Solana DEXs (Pump.fun, Raydium, Orca), transaction costs have fixed minimum components regardless of trade size:
- **Base Network Fee:** ~0.000005 to 0.000010 SOL
- **Priority / Jito Tip:** ~0.000050 to 0.000200 SOL
- **Pump.fun / DEX Protocol Swap Fee:** 1.0% on Buy + 1.0% on Sell
- **Curve Slippage & Price Impact:** 0.5% to 5.0%+ (depending on pool depth)
- **Associated Token Account (ATA) Rent Storage:** ~0.002039 SOL per token account (locked until closed)

### Mathematical Table: Round-Trip Sizing vs Minimum Break-Even PnL

| Entry Sizing (SOL) | Fixed Friction (SOL) | Gross Gain Needed to Break Even | % Move Required on DEX |
| :--- | :--- | :--- | :--- |
| **0.0010 SOL** | ~0.00085 SOL | +0.00085 SOL | **+85.0%** |
| **0.0020 SOL** | ~0.00085 SOL | +0.00085 SOL | **+42.5%** |
| **0.0050 SOL** | ~0.00090 SOL | +0.00090 SOL | **+18.0%** |
| **0.0100 SOL** | ~0.00095 SOL | +0.00095 SOL | **+9.5%** |
| **0.0500 SOL** | ~0.00120 SOL | +0.00120 SOL | **+2.4%** |
| **0.1000 SOL** | ~0.00150 SOL | +0.00150 SOL | **+1.5%** |

### Core Rule for Agent Behavior:
When an operator requests micro-take-profit scalping ("TP tipis-tipis +2% s/d +5%") on micro-entry capital ($< 0.020\text{ SOL}$), the agent **must proactively calculate net PnL and warn/refuse before execution**. Executing a +2.8% win that loses cash on net is a critical failure of quantitative advisory.

---

## 2. Fast Execution Telemetry Synchronization (Preventing "UI Bug / Hilang" Complaints)
In sub-minute scalping loops, trade execution (buy $\rightarrow$ monitor $\rightarrow$ sell) may finish before the HTTP dashboard polling interval triggers.

### Implementation Checklist:
1. **Synchronous Array Mutation:** Immediately `unshift()` the confirmed transaction signatures and metadata into the server's global `engineState.history` array and write to `live_trades.json` at the exact moment of confirmation.
2. **Explicit Transaction Hyperlinks:** Provide direct Solscan/Solana Beach explorer URLs in every telemetry response so the user can verify on-chain finality immediately.
3. **RPC Polling Isolation:** Separate balance fetching into an independent, non-blocking 2-second ticker (`setInterval`) with defensive error catching to prevent RPC timeouts from stalling the dashboard JSON feed.

---

## 3. Solana Token Account (ATA) Rent Reclaim Procedure
When micro-capital trading is stopped or paused, significant capital remains locked in storage rent.
- Query all token accounts owned by wallet via `connection.getParsedTokenAccountsByOwner(walletPubkey, { programId: TOKEN_PROGRAM_ID })` and Token-2022.
- For every zero-balance account, construct and broadcast `createCloseAccountInstruction(accountPubkey, destinationWallet, walletPubkey)` to reclaim $\sim 0.002039\text{ SOL}$ per account.
- Direct users to Phantom: **Settings $\rightarrow$ Manage Accounts $\rightarrow$ Close / Burn Empty Token Accounts** or web tools like `claimyoursol.com` / `sol-incinerator.com` to recover funds manually without CLI tools.

---

## 4. Alternative Capital Generation (Web3 Bounties & Grants over On-Chain Micro-Scalping)
When capital is exhausted or too low for on-chain trading friction:
- Direct operators to **Superteam Earn (`earn.superteam.fun`)**, Gitcoin, or DoraHacks where tasks (deep-dive technical analysis, thread writing, bot development, dApp feedback) pay $50 - $2,000+ USDC/SOL with zero capital risk.
- Assist users with end-to-end bounty delivery: architecture research, whitepaper synthesis, and high-impact submission drafting.

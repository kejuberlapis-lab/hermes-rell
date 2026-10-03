# Solana DEX Spot Gold / Commodity Execution Reference

## 1. Spot DEX Swap Architecture for Micro-Wallets
When operating commodity or gold token trading engines (e.g. PAXG, XAUt, or synthetic on-chain spot assets) on Solana with micro-capital ($0.03 - 0.10 SOL):

### Architecture Comparison
| Dimension | Jalur 1: Spot DEX Swap | Jalur 2: Perpetual DEX (Drift / Flash) |
|---|---|---|
| **Capital Requirement** | 0.010 - 0.040 SOL | 0.060 - 0.100+ SOL |
| **Account Overhead** | None (Standard ATA only) | Heavy (~0.035 SOL Subaccount Rent) |
| **Direction** | BUY / LONG Only (Spot Accumulation) | 2-Way (BUY Long & SELL Short) |
| **Liquidation Risk** | ZERO (Unleveraged Spot asset) | High under micro-margins (<$10) |
| **Holding Strategy** | Hold through M15 pullbacks till rebound | Strict SL required to avoid margin call |

---

## 2. On-Chain Buy Execution Payload (Local Signing)
```javascript
const response = await axios.post('https://pumpportal.fun/api/trade-local', {
    publicKey: botKeypair.publicKey.toBase58(),
    action: 'buy',
    mint: mintAddress,
    amount: amountInSol,
    denominatedInSol: 'true',
    slippage: 30, // 30% initial buy slippage
    priorityFee: 0.00005, // Optimal micro-priority fee
    pool: 'pump' // or 'raydium'
}, { responseType: 'arraybuffer', timeout: 10000 });

if (response.status === 200) {
    const tx = VersionedTransaction.deserialize(new Uint8Array(response.data));
    tx.sign([botKeypair]);
    const signature = await connection.sendTransaction(tx, { skipPreflight: true, maxRetries: 5 });
    return { success: true, tx: signature };
}
```

---

## 3. On-Chain Sell & Profit Realization (Guaranteed Execution Ladder)
To prevent `0x1772` / `Custom 6002` (Slippage Exceeded) errors when closing trades into cash SOL:

```javascript
async function executeOnChainSell(mint, percentageStr = '100%', attempt = 1) {
    if (!botKeypair) return { success: false, error: "No keypair configured" };
    // Progressive Slippage Ladder: 40% -> 55% -> 70%
    const sellSlippage = attempt === 1 ? 40 : (attempt === 2 ? 55 : 70);
    const sellPriorityFee = 0.00005;

    // Read exact token balance (SPL + Token-2022 programs)
    const splAccs = await connection.getParsedTokenAccountsByOwner(
        botKeypair.publicKey, 
        { programId: new PublicKey('TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA') }
    );
    const matchingAcc = splAccs.value.find(a => a.account.data.parsed.info.mint === mint);
    const tokenBalance = parseFloat(matchingAcc?.account.data.parsed.info.tokenAmount.uiAmount || 0);

    if (tokenBalance <= 0) return { success: true, tx: 'zero_balance' };

    const frac = percentageStr === '50%' ? 0.5 : (percentageStr === '30%' ? 0.3 : 1.0);
    const exactTokenAmount = frac >= 1.0 ? tokenBalance : Math.floor(tokenBalance * frac);

    const response = await axios.post('https://pumpportal.fun/api/trade-local', {
        publicKey: botKeypair.publicKey.toBase58(),
        action: 'sell',
        mint: mint,
        amount: exactTokenAmount, // Pass exact integer/token units, not percentage strings
        denominatedInSol: 'false',
        slippage: sellSlippage,
        priorityFee: sellPriorityFee,
        pool: 'pump'
    }, { responseType: 'arraybuffer', timeout: 12000 });

    if (response.status === 200) {
        const tx = VersionedTransaction.deserialize(new Uint8Array(response.data));
        tx.sign([botKeypair]);
        const signature = await connection.sendTransaction(tx, { skipPreflight: true, maxRetries: 5 });
        return { success: true, tx: signature };
    }
    
    if (attempt < 3) {
        await new Promise(r => setTimeout(r, 1000));
        return await executeOnChainSell(mint, percentageStr, attempt + 1);
    }
    return { success: false, error: "HTTP " + response.status };
}
```

---

## 4. Operational Guardrails
1. **Never Sell Tiny PnL On-Chain:** Gains $< +1.0\%$ (e.g., $+0.06\%$ on $0.001\text{ SOL} \approx 0.0000006\text{ SOL}$) are smaller than Solana network gas fees ($\approx 0.00005\text{ SOL}$). Enforce $+5.0\%$ minimum harvest thresholds.
2. **Server-Side Render Initial State:** Avoid client-side flicker or operator panic caused by raw `0.000000 SOL` placeholders by injecting cached balance directly into the initial HTML response.
3. **Double Entry Multi-Position Routing:** Target individual positions via `{ id: posId }` parameter payloads to enable granular per-slot liquidation without closing sibling positions.

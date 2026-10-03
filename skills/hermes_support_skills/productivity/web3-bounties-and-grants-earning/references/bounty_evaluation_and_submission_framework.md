# Web3 Bounty Winning Criteria & Evaluation Framework

## 1. Platform & Evaluation Archetypes

### A. Superteam Earn (Solana Ecosystem)
- **Primary Currencies:** USDC, USDG, SOL (directly paid to claimant's Solana wallet).
- **Core Formats:**
  1. **Technical Deep-Dive Threads (X/Twitter):** Focuses on technical architecture, UX comparisons (TradFi vs Web3), and protocol partnerships.
  2. **Product Feedback & Testing:** Detailed breakdown of UI friction, bugs, and feature recommendations.
  3. **Visual & Design Assets:** Infographics, explainer animations, UI/UX redesigns.
  4. **Code & Mini-Apps:** Smart contract integrations, AI Agent skill development, SDK utilities.

### B. Anti-Disqualification Checklist
1. **Handle Exactness:** Missing a required tag (e.g. `@STEALFxyz` + `@Arcium`) will result in immediate disqualification by automated scrapers.
2. **Character Overflow Prevention:** When crafting tweets, limit bodies to $\le 260$ characters to leave a buffer for handle expansion and media links.
3. **Form Duplication Understanding:** In single-thread content bounties, both "Link to Your Submission" and "Tweet Link" accept the exact root tweet URL (`https://x.com/.../status/...`).
4. **Organic Engagement:** Genuine interactions (discussion replies, peer feedback) amplify scoring; purchased bot likes result in zero evaluation marks.
5. **Campaign Expiration & Status Verification:** On Galxe/Zealy, verify that the quest status is active (`Ongoing / Open`) before directing execution; ended campaigns keep task checkboxes active but disable the final claim button.

---

## 2. Multi-Chain Gas Refueling & Micro-Capital EVM Onboarding

When users transition from Solana-only setups (Phantom) to EVM-based quests (Galxe, Layer3, Testnets) or encounter `Insufficient funds for gas` errors (e.g. Gravity `0.0036 G`, Base, Arbitrum, Polygon):

### A. Friction Diagnosis
1. **Network Mismatch:** Phantom in-app browser defaults to Solana (`4x6x...`); claiming on EVM requires switching to the EVM address (`0x...`).
2. **In-App Onramp Limits:** MetaMask native buy providers (Transak/MoonPay) frequently enforce high minimum purchase thresholds ($10–$15 / ~Rp 150.000+) and default to Ethereum mainnet ETH.
3. **Cross-Chain Bridging Trap:** Attempting to bridge micro-balances ($0.50 SOL) from Solana to EVM drains 100% of capital in bridge fees ($1–$3).

### B. Micro-Capital Gas Refuel Playbook (Rp 10.000 – Rp 20.000 / ~$0.50 – $1.00)
1. **Acquire Low-Fee Native EVM Asset:**
   - Purchase minimal POL (Polygon) or BNB (BSC) via local exchange (Pintu, Indodax, Tokocrypto) or P2P/converter contact.
   - Polygon POL is preferred for minimal withdrawal minimums and sub-cent transfer fees.
2. **Receive on Universal EVM Address:**
   - Single EVM address (`0x...`) in MetaMask/Phantom serves all EVM networks (Polygon, BSC, Gravity, Base, Arbitrum).
3. **Multi-Chain Universal Gas Refueling via Gas.zip:**
   - In MetaMask in-app browser, navigate to `https://gas.zip`.
   - Connect wallet on source chain (e.g. Polygon).
   - Select destination chain requiring gas (e.g. `Gravity`).
   - Swap minimal fraction (e.g. `0.5 POL` / ~$0.20) to receive native gas token (e.g. `$G`).
   - Settle on-chain claim tasks immediately without overspending capital.

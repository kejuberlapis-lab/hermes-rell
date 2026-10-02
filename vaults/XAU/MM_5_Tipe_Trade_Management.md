# ⚙️ MM: 5 Model Manajemen Posisi & Trade Execution

> **Vault:** `XAU` | **Topik:** Trade Management & EA Logic | **Terkait:** [[MM_Kalkulasi_Lot_Dinamis]], [[Setup_Scalping_M5_SnR_Reversal]]

---

## 1. Lima Model Trade Management (Sarjana Trading Assistant)

### 🔹 Tipe 1: Single Target
- 1 posisi tunggal dengan target tetap (1:2 atau 1:3).
- Hasil: Hit TP penuh atau Hit SL penuh.

### 🔹 Tipe 2: Dual Split Position (Safety Target)
- Risiko 1% dibagi menjadi dua posisi (@ 0.5%):
  - Posisi 1 TP di **1R**.
  - Posisi 2 TP di **3R**.
- Jika harga hit 1R lalu berbalik arah terkena SL, total hasil trade = **BEP / Impas (0 Profit 0 Loss)**.

### 🔹 Tipe 3: Auto Move to BEP (Breakeven)
- 1 posisi tunggal dengan target 1:2 atau 1:3.
- Saat harga menyentuh keuntungan 1R, Stop Loss otomatis digeser ke harga entry (BEP).

### 🌟 Tipe 4: Dual Split + Auto BEP (*MODEL UNGGULAN & FAVORIT FOREX SARJANA*)
- Risiko 1% dibagi menjadi dua posisi (@ 0.5%):
  1. Saat harga mencapai **1R**:
     - Posisi 1 **otomatis ditutup (+0.5R keuntungan terkunci)**.
     - Posisi 2 **otomatis digeser SL ke titik BEP (Entry)**.
  2. Skenario Hasil:
     - Jika harga berbalik terkena SL: Tetap **untung +0.5R**.
     - Jika harga tembus hingga TP utama (3R): Untung total **+2.0R**.
     - Jika langsung terkena SL dari awal: Rugi terkontrol **-1.0R**.

### 🔹 Tipe 5: Dynamic Trailing Stop
- Stop Loss bergeser otomatis mengikuti formasi swing high/low baru di timeframe eksekusi untuk menangkap tren panjang.

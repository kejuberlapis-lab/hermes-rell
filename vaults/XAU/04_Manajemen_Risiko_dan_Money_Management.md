# 🛡️ Bagian 4: Manajemen Risiko & Money Management Mekanikal

> **Kategori:** Money Management, Lot Sizing, Trade Management, EA Logic  
> **Tujuan:** Melindungi modal dari drawdowns ekstrem dan memastikan akun bertumbuh secara konsisten secara matematis.

---

## 1. Aturan Dasar Pengelolaan Risiko

Trading bukan tentang seberapa sering kita benar, melainkan **berapa yang kita dapat saat benar dan berapa yang hilang saat salah**.

1. **Batas Risiko Per Transaksi:**
   - Standar aman: **1% dari modal akun**.
   - Maksimal: **2% dari modal akun**.
2. **Kalkulasi Lot Dinamis (Bukan Fixed Lot):**
   - Jarak Stop Loss yang berbeda-beda mewajibkan ukuran lot yang menyesuaikan agar kerugian tetap terkunci di persentase yang sama.
   $$\text{Ukuran Lot} = \frac{\text{Modal Akun} \times \text{Persentase Risiko}}{\text{Jarak Stop Loss (dalam Pips)} \times \text{Nilai Per Pip}}$$

---

## 2. 5 Model Trade Management (Dari Sarjana Trading Assistant)

Forex Sarjana merancang 5 tipe manajemen posisi untuk mengelola order setelah entri:

### 🔹 Model 1: Single Target (Tradisional)
- 1 posisi tunggal dengan target pasti (misal 1:2 atau 1:3).
- *Hasil:* Hit TP (+2R / +3R) atau Hit SL (-1R).

### 🔹 Model 2: Dual Split Position (Safety Target)
- Risiko 1% dipecah menjadi dua posisi (@ 0.5% risiko):
  - **Posisi A:** Target profit di **1R** (TP1).
  - **Posisi B:** Target profit di **3R** (TP2 / Runner).
- *Skenario:* Jika harga menyentuh 1R lalu berbalik arah terkena SL, hasil akhir perdagangan adalah **BEP / Impas (0 Profit 0 Loss)**.

### 🔹 Model 3: Auto Move to BEP (Breakeven Trailing)
- 1 posisi tunggal dengan target 1:2 atau 1:3.
- Begitu harga mencapai keuntungan **1R**, Stop Loss otomatis dipindahkan ke harga entri (BEP).
- *Kelemahan:* Kadang harga menyentuh titik BEP sebelum melanjutkan reli ke TP.

### 🌟 Model 4: Dual Split + Auto BEP (*MODEL TERBAIK / FAVORIT FOREX SARJANA*)
Model ini menggabungkan keuntungan *locking profit* dan *risk-free running*:
- Risiko 1% dibagi menjadi dua posisi (@ 0.5% risiko):
  1. Saat harga mencapai **1R**:
     - Posisi A **langsung ditutup otomatis** ➔ Keuntungan **+0.5R terkunci di saldo**.
     - Posisi B **otomatis dipindahkan Stop Loss-nya ke titik BEP (Entry)**.
  2. Skenario Hasil:
     - Jika harga berbalik turun dan terkena SL ➔ Akun **tetap PROFIT +0.5R** (Posisi A untung +0.5R, Posisi B 0R).
     - Jika harga tembus hingga target utama (3R) ➔ Akun untung total **+2.0R** (+0.5R + +1.5R).
     - Jika harga langsung kena SL dari awal ➔ Rugi terukur -1.0R.

### 🔹 Model 5: Dynamic Trailing Stop
- Stop Loss bergeser mengikuti formasi *Swing High / Swing Low* baru di timeframe M5/M15 untuk menangkap reli tren panjang.

---

## 3. Pemilihan Tipe Akun & Broker untuk XAU/USD

1. **Gunakan Akun Raw Spread / Zero Spread:**
   - XAU/USD memiliki volatilitas tinggi. Akun dengan spread lebar akan memperbesar jarak SL dan memangkas profit scalper.
2. **Waspadai Pelebaran Spread:**
   - Hindari entri 5 menit sebelum dan sesudah rilis berita *High Impact News* (NFP, CPI, FOMC Rate Decision) karena spread dapat melebar drastis.

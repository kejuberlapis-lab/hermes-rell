# 🔄 Setup 3: Supply & Demand + RSI Divergence Confirmation

> **Vault:** `XAU` | **Topik:** SOP Setup Entri | **Terkait:** [[Indikator_RSI_Divergence]], [[SMC_Order_Block_dan_Imbalance]]

---

## 1. Spesifikasi Setup
- **Fokus:** Menyaring zona Supply & Demand palsu dengan memanfaatkan konfirmasi divergensi momentum.
- **Timeframe:** H1 (Zona SnD) ➔ M5 (RSI Divergence & Candlestick Confirmation).

---

## 2. Alur Eksekusi

1. **Zona H1:**
   - Identifikasi zona Supply (Drop-Base-Drop) atau Demand (Rally-Base-Rally).
2. **Filter Divergensi M5:**
   - Saat harga masuk ke zona, periksa RSI:
     - **Setup BUY:** Terbentuk *Bullish Divergence* (Price Low lebih rendah, RSI Low lebih tinggi) + Garis RSI Ungu memotong ke atas garis Kuning MA.
     - **Setup SELL:** Terbentuk *Bearish Divergence* (Price High lebih tinggi, RSI High lebih rendah) + Garis RSI Ungu memotong ke bawah garis Kuning MA.
3. **Trigger:**
   - Buka posisi setelah muncul candle *Strong Engulfing* atau candle *Imbalance* searah dengan divergensi.

---

## 3. Aturan Khusus Re-Entry
- Jika harga kembali masuk ke zona setelah entri pertama:
  - **Hanya boleh Re-entry BUY:** Jika harga saat ini **LEBIH MURAH** dari harga entri pertama.
  - **Hanya boleh Re-entry SELL:** Jika harga saat ini **LEBIH MAHAL** dari harga entri pertama.
- Dilarang re-entry buy di harga yang lebih tinggi dari posisi pertama.

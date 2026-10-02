# ⚡ Setup 1: Multi-Timeframe M5 Scalping (SnR Reversal)

> **Vault:** `XAU` | **Topik:** SOP Setup Entri | **Terkait:** [[Indikator_EMA_50_dan_200]], [[Indikator_ATR_Dynamic_Stop_Loss]], [[MM_5_Tipe_Trade_Management]]

---

## 1. Spesifikasi Setup
- **Instrumen:** XAU/USD (Gold), EUR/USD, GBP/USD.
- **Timeframe Analisa:** H1 (Zona SnR & Trend Filter).
- **Timeframe Eksekusi:** M5 (Momentum Candlestick).

---

## 2. Langkah Demi Langkah Eksekusi

### Langkah 1: Filter Trend H1
- Cek persilangan EMA:
  - `EMA 50 > EMA 200` ➔ Hanya cari Support & posisi BUY.
  - `EMA 50 < EMA 200` ➔ Hanya cari Resistance & posisi SELL.

### Langkah 2: Pemetaan Zona H1
- Gambar kotak zona dari ujung shadow hingga body close terluar swing.
- Pasang alert pada kotak zona.

### Langkah 3: Konfirmasi Momentum M5
- Begitu harga menyentuh zona H1, buka chart M5:
  - **Posisi BUY:** Tunggu pola *Bullish Engulfing* di zona support + 1 candle hijau berikutnya yang close di atas engulfing.
  - **Posisi SELL:** Tunggu pola *Bearish Engulfing* di zona resistance + 1 candle merah berikutnya yang close di bawah engulfing.

### ⚠️ Filter Pembatalan (Abnormal Candle):
- Jika candle konfirmasi terlalu panjang/abnormal, **JANGAN ENTRY** (risiko SL terlalu lebar).

---

## 3. Parameter Risiko & Target
- **SL BUY:** `Swing Low M5 - ATR`
- **SL SELL:** `Swing High M5 + ATR + Spread`
- **TP:** Minimal **1:2** (atau gunakan Model Split TP 1R + BEP).

# 📏 Indikator: ATR (Average True Range) & Dynamic Stop Loss

> **Vault:** `XAU` | **Topik:** Indikator Volatilitas | **Terkait:** [[Indikator_EMA_50_dan_200]], [[MM_Kalkulasi_Lot_Dinamis]]

---

## 1. Masalah Stop Loss Statis
Meletakkan Stop Loss persis di ujung ekor candle sering memicu *Stop Hunt* karena fluktuasi normal volatilitas pasar (terutama pada instrumen volatil seperti XAU/USD).

---

## 2. Rumus ATR Dynamic Buffer

Indikator ATR (periode 14) digunakan untuk memberi "ruang bernapas" bagi posisi kita:

### A. Posisi BUY
$$\text{Stop Loss} = \text{Swing Low Terdekat} - \text{Nilai ATR}$$
*(Pada posisi BUY tidak perlu dikurangi spread).*

### B. Posisi SELL
$$\text{Stop Loss} = \text{Swing High Terdekat} + \text{Nilai ATR} + \text{Spread Broker}$$
*(Wajib ditambah spread broker karena order SELL ditutup pada harga Ask).*

---

## 3. Penyesuaian Volatilitas
- **Pasar Normal:** Gunakan `100% Nilai ATR`.
- **Pasar Momentum Tinggi / Scalping M5 Cepat:** Dapat disesuaikan menggunakan `50% Nilai ATR` untuk memperkecil jarak SL dan memperbesar rasio Risk:Reward.

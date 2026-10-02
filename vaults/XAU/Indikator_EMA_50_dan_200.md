# 📈 Indikator: EMA 50 & EMA 200 (Trend Filter Mutlak)

> **Vault:** `XAU` | **Topik:** Indikator & Filter Tren | **Terkait:** [[Indikator_ATR_Dynamic_Stop_Loss]], [[Setup_Scalping_M5_SnR_Reversal]]

---

## 1. Fungsi Utama
EMA (Exponential Moving Average) periode 50 dan 200 digunakan pada **Timeframe Analisa (H1 / H4)** sebagai filter objektif untuk menentukan bias arah pasar:

| Posisi EMA | Status Tren Pasar | Aturan Tindakan |
|---|---|---|
| **EMA 50 > EMA 200** | **Uptrend (Bullish)** | **Hanya cari peluang BUY** di area Support/Demand. Batalkan seluruh setup Sell. |
| **EMA 50 < EMA 200** | **Downtrend (Bearish)** | **Hanya cari peluang SELL** di area Resistance/Supply. Batalkan seluruh setup Buy. |

---

## 2. Dynamic Support & Resistance
- Pada kondisi trending yang kuat, garis EMA 50 sering bertindak sebagai area *Dynamic Support/Resistance* saat harga melakukan koreksi sehat.
- Jika candle menembus EMA 200 secara signifikan, ini menjadi sinyal awal terjadinya perubahan siklus tren besar.

---

## 3. Golden Rule
> ⚠️ **Dilarang keras melawan tren:** Jangan pernah membuka posisi counter-trend melawan arah persilangan EMA 50/200 di timeframe H1.

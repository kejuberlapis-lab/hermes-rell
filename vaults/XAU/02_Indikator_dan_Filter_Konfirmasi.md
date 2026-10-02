# 📈 Bagian 2: Indikator & Filter Konfirmasi Presisi

> **Kategori:** Indikator Teknikal, Dynamic Risk Filter, Divergence, Fibonacci  
> **Tujuan:** Menghilangkan subjektivitas saat menentukan arah tren, ruang gerak Stop Loss, dan momentum pembalikan.

---

## 1. Filter Trend Utama: EMA 50 & EMA 200

Indikator ini digunakan pada Timeframe Analisa (H1 / H4) sebagai filter mutlak untuk menyaring arah perdagangan:

| Kondisi Indikator | Status Tren | Aturan Eksekusi |
|---|---|---|
| **EMA 50 > EMA 200** | **Uptrend (Bullish)** | **HANYA** mencari zona Demand / Support dan membuka posisi **BUY**. Batalkan semua setup Sell. |
| **EMA 50 < EMA 200** | **Downtrend (Bearish)** | **HANYA** mencari zona Supply / Resistance dan membuka posisi **SELL**. Batalkan semua setup Buy. |

> ⚠️ **Prinsip Utama:** Jangan pernah melakukan counter-trend trading melawan persilangan EMA 50/200 di timeframe besar.

---

## 2. Dynamic Stop Loss dengan Indikator ATR (Average True Range)

Banyak trader terkena *stop hunt* karena meletakkan Stop Loss persis di ujung ekor candle tanpa memperhitungkan volatilitas dan spread. Forex Sarjana menggunakan rumus **ATR Dynamic Buffer**:

### Rumus Perhitungan Stop Loss:

- **Posisi BUY:**
  $$\text{Stop Loss} = \text{Swing Low Terdekat} - \text{Nilai ATR}$$
  *(Pada posisi BUY tidak perlu dikurangi spread).*

- **Posisi SELL:**
  $$\text{Stop Loss} = \text{Swing High Terdekat} + \text{Nilai ATR} + \text{Spread Broker}$$
  *(Wajib ditambah spread karena order SELL ditutup pada harga Ask).*

*Catatan:* Pada setup momentum agresif, penggunaan buffer bisa disesuaikan menjadi `50% dari nilai ATR`.

---

## 3. RSI Divergence & RSI-Based Moving Average

RSI tidak digunakan sekadar untuk melihat Overbought (>70) atau Oversold (<30), melainkan untuk mendeteksi ketidaksesuaian (*divergence*) antara aksi harga dan kekuatan momentum:

### A. Bullish Divergence (Sinyal Pembalikan Naik)
- **Kondisi:** Chart harga mencetak **Lower Low (LL)**, tetapi garis indikator RSI mencetak **Higher Low (HL)**.
- **Makna:** Tekanan seller sudah melemah drastis meskipun harga sempat membuat titik terendah baru.

### B. Bearish Divergence (Sinyal Pembalikan Turun)
- **Kondisi:** Chart harga mencetak **Higher High (HH)**, tetapi garis indikator RSI mencetak **Lower High (LH)**.
- **Makna:** Tekanan buyer sudah kehabisan tenaga (*exhaustion*) di area puncak.

### C. Konfirmasi RSI-Based MA
- **Konfirmasi BUY:** Garis RSI (Ungu) harus berada dan memotong **di atas** garis Moving Average RSI (Kuning).
- **Konfirmasi SELL:** Garis RSI (Ungu) harus berada dan memotong **di bawah** garis Moving Average RSI (Kuning).

---

## 4. Fibonacci Retracement (Discount vs Premium Zone)

Digunakan untuk memilih zona Demand/Supply terbaik saat terdapat lebih dari satu area:

1. **Untuk Posisi BUY (Mencari Harga Murah / Discount):**
   - Tarik Fibonacci dari titik Swing Low ke Swing High.
   - Hanya ambil zona Demand yang terletak di **bawah level Fibonacci 61.8%** (Area OTE - *Optimal Trade Entry*).
2. **Untuk Posisi SELL (Mencari Harga Mahal / Premium):**
   - Tarik Fibonacci dari titik Swing High ke Swing Low.
   - Hanya ambil zona Supply yang terletak di **atas level Fibonacci 61.8%**.

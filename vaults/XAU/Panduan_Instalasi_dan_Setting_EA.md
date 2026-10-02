# 🤖 Panduan Instalasi & Pengaturan EA Forex Sarjana M5 Scalper

> **File EA:** `Forex_Sarjana_M5_Scalper_MQL4.mq4` (MT4) & `Forex_Sarjana_M5_Scalper_MQL5.mq5` (MT5)  
> **Instrumen Utama:** XAU/USD (Gold) | **Timeframe Chart:** M5 (5-Menit)  
> **Dasar Logika:** Hasil Riset & Pembuktian Data Historis 2004–2026 (Forex Sarjana + Model 4 MM)

---

## 🏛️ 1. Arsitektur & Logika Eksekusi EA

Robot trading ini mengimplementasikan aturan kuantitatif yang telah terbukti menghasilkan akurasi tinggi dan meminimalkan risiko:

```
[ Filter Tren H1: EMA 50 vs EMA 200 ]
                  ↓
[ Timeframe Eksekusi M5: Pola Engulfing ]
                  ↓
[ Konfirmasi Lilin Searah M5 ]
                  ↓
[ Filter Lilin Abnormal (< 2.0x ATR) ]
                  ↓
[ Eksekusi Dual-Split Position (Model 4) ]
   ├── Posisi A (0.01 Lot) ➔ Take Profit di 1R
   └── Posisi B (0.01 Lot) ➔ Take Profit di 3R (Runner)
                  ↓
[ Begitu Posisi A Hit TP ➔ SL Posisi B Otomatis Bergeser ke BEP (Zero-Risk) ]
```

---

## 🛠️ 2. Cara Pasang di MetaTrader 4 / MetaTrader 5

### Untuk MetaTrader 4 (MT4):
1. Buka aplikasi MT4 sir.
2. Klik menu **File** ➔ **Open Data Folder**.
3. Masuk ke folder **MQL4** ➔ **Experts**.
4. Salin file `Forex_Sarjana_M5_Scalper_MQL4.mq4` ke dalam folder tersebut.
5. Buka MetaEditor di MT4, buka file tersebut lalu klik tombol **Compile** (F7).
6. Kembali ke MT4, klik kanan pada jendela *Navigator* ➔ pilih **Refresh**.
7. Buka chart **XAU/USD timeframe M5**, lalu seret (drag & drop) EA ke dalam chart.
8. Centang opsi **"Allow Live Trading"** dan **"Allow DLL Imports"**, lalu klik OK.

---

### Untuk MetaTrader 5 (MT5):
1. Buka aplikasi MT5.
2. Klik menu **File** ➔ **Open Data Folder**.
3. Masuk ke folder **MQL5** ➔ **Experts** ➔ **Advisors**.
4. Salin file `Forex_Sarjana_M5_Scalper_MQL5.mq5` ke dalam folder tersebut.
5. Buka MetaEditor di MT5, buka file tersebut lalu klik **Compile** (F7).
6. Pasang pada chart **XAU/USD timeframe M5**, centang **"Allow Algo Trading"**, lalu aktifkan tombol **Algo Trading** di toolbar atas.

---

## ⚙️ 3. Penjelasan Parameter Input Kunci

| Parameter Input | Nilai Standar | Fungsi & Penjelasan |
|---|:---:|---|
| `FixedLotPerPosition` | `0.01` | Ukuran lot per posisi. Untuk modal $2,000, biarkan tetap 0.01 (membuka 2 x 0.01 lot = 0.02 lot total per setup). |
| `UseAutoLot` | `false` | Jika diubah ke `true`, EA akan menghitung ukuran lot otomatis berbasis persentase risiko modal (`RiskPercentPerTrade`). |
| `H1_EMA_Fast` | `50` | Periode EMA cepat pada timeframe H1 untuk filter tren. |
| `H1_EMA_Slow` | `200` | Periode EMA lambat pada timeframe H1 untuk filter tren. |
| `M5_ATR_Period` | `14` | Periode ATR pada timeframe M5 untuk mengukur volatilitas pasar. |
| `M5_ATR_Multiplier_SL` | `1.0` | Pengali ATR untuk memberi jarak bantalan aman pada Stop Loss di balik swing high/low. |
| `MaxCandleATRRatio` | `2.0` | **Penyelamat Modal:** Jika ukuran lilin sinyal $> 2.0\times\text{ATR}$ (misal saat news spike), sinyal otomatis dibatalkan untuk menghindari SL lebar. |
| `TP1_RR_Ratio` | `1.0` | Target keuntungan Posisi A (1x jarak risiko). |
| `TP2_RR_Ratio` | `3.0` | Target keuntungan Posisi B (3x jarak risiko). |
| `AutoMoveBEP_On_TP1` | `true` | Mengaktifkan trailing otomatis: saat Posisi A TP, SL Posisi B langsung bergeser ke harga open (Breakeven). |
| `MaxSpreadPoints` | `35` | Filter spread maksimal. EA tidak akan open posisi jika spread sedang melebar di atas 35 points (35 cents). |

---

## 🎯 4. Rekomendasi Akun & Lingkungan Eksekusi

1. **Wajib Akun Raw Spread / Zero Spread / ECN:**  
   Karena strategi ini menggunakan Stop Loss presisi di M5, akun bebas spread (hanya komisi) sangat direkomendasikan agar target TP1 cepat tercapai dan terhindar dari slip spread.
2. **Gunakan VPS (Virtual Private Server):**  
   Agar EA dapat aktif memantau chart M5 secara stabil 24 jam tanpa terputus koneksi internet rumah.
3. **Jam Operasional Terbaik:**  
   Paling aktif dan likuid saat **Sesi London (14.00 – 22.00 WIB)** dan **Sesi New York (19.00 – 23.00 WIB)**.

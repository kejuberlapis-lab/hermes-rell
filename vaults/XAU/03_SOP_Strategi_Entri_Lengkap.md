# 🎯 Bagian 3: SOP Lengkap 4 Setup Entri Presisi

> **Kategori:** Execution SOP, Trading Setups, Entry Rules, Scalping & Swing  
> **Tujuan:** Panduan langkah demi langkah saat mengeksekusi perdagangan secara mekanikal tanpa ragu.

---

## ⚡ SETUP 1: Multi-Timeframe M5 Scalping (Support & Resistance Momentum)

Setup tercepat untuk scalping harian pada XAU/USD atau Forex Majors.

### 📋 Diagram Alur Eksekusi:
$$\text{H1 Trend Filter (EMA 50/200)} \longrightarrow \text{H1 Zone (SnR)} \longrightarrow \text{M5 Engulfing} \longrightarrow \text{Candle Konfirmasi} \longrightarrow \text{Entry}$$

### Aturan Eksekusi:
1. **Analisa H1:**
   - Tentukan tren (EMA 50 vs EMA 200).
   - Gambar kotak zona SnR dari ujung shadow hingga close body swing high/low. Pasang alarm.
2. **Eksekusi M5 saat Alarm Menyala:**
   - **Posisi BUY:** Tunggu terbentuk pola *Bullish Engulfing* di area Support, diikuti **1 candle hijau berikutnya** yang close di atas pola engulfing.
   - **Posisi SELL:** Tunggu terbentuk pola *Bearish Engulfing* di area Resistance, diikuti **1 candle merah berikutnya** yang close di bawah pola engulfing.
3. **Filter Candle Abnormal:**
   - ⚠️ Jika candle konfirmasi ukurannya sangat panjang/abnormal, **JANGAN ENTRY** (risiko SL terlalu besar dan rawan retest).
4. **SL & TP:**
   - `SL BUY` = Swing Low - ATR
   - `SL SELL` = Swing High + ATR + Spread
   - `TP` = Minimal **1:2**

---

## 🎯 SETUP 2: Sniper Entry (Liquidity Sweep + CHoCH + Imbalance)

Setup akurasi tinggi dengan Risk:Reward besar (1:3 hingga 1:5) dengan memanfaatkan manipulasi market maker.

### Aturan Eksekusi:
1. **Analisa H1:**
   - Tandai area **Unmitigated Order Block** (yang diikuti oleh Imbalance & Major BOS).
2. **Transisi ke M5:**
   - Tunggu harga masuk ke dalam Order Block H1.
   - Amati struktur M5 hingga terjadi **Change of Character (CHoCH)** yang valid (break body + meninggalkan Imbalance).
3. **Identifikasi Level Likuiditas:**
   - Tandai Swing Low (untuk buy) atau Swing High (untuk sell) sebagai *Liquidity Level*.
4. **Menunggu Sweep & Manipulasi:**
   - Tunggu harga menembus level likuiditas tersebut (*Liquidity Sweep*).
   - Tunggu harga segera memantul balik dan mencetak **Candle Imbalance Baru** searah tren utama.
5. **Penempatan Limit Order:**
   - Pasang **Buy Limit** pada candle bearish (merah) terakhir sebelum imbalance (+ spread).
   - Pasang **Sell Limit** pada candle bullish (hijau) terakhir sebelum imbalance.
6. **SL & TP:**
   - `SL` = Beberapa pips di luar ekor manipulasi / swing terjauh.
   - `TP` = Target **1:3** hingga **1:5**.

---

## 🔄 SETUP 3: SMC Supply & Demand + RSI Divergence

Setup pembalikan arah dengan filter multi-lapisan untuk menyaring fakeout di zona SnD.

### Aturan Eksekusi:
1. **Analisa H1:**
   - Identifikasi zona Supply (Drop-Base-Drop) atau Demand (Rally-Base-Rally).
2. **Konfirmasi Divergence di M5:**
   - Saat harga masuk zona, periksa indikator RSI.
   - **Untuk BUY:** Wajib terbentuk **Bullish Divergence** (Harga Low lebih rendah, RSI Low lebih tinggi) + Garis RSI Ungu memotong **ke atas** garis MA Kuning.
   - **Untuk SELL:** Wajib terbentuk **Bearish Divergence** (Harga High lebih tinggi, RSI High lebih rendah) + Garis RSI Ungu memotong **ke bawah** garis MA Kuning.
3. **Trigger:**
   - Entri setelah muncul candle *Strong Engulfing* atau candle *Imbalance* searah divergensi.
4. **Aturan Khusus Re-Entry:**
   - Hanya boleh melakukan *re-entry buy* jika harga masuk kembali ke zona pada **level harga yang LEBIH MURAH** dari entri sebelumnya.
   - Jangan re-entry buy di harga yang lebih tinggi dari entri pertama.

---

## 📐 SETUP 4: Break & Retest Flip Zone + Fibonacci 61.8%

Setup follow trend saat terjadi perpindahan kekuatan struktur pasar (SBR / RBS).

### Aturan Eksekusi:
1. **Identifikasi Breakout:**
   - Resistance kuat H1/Daily berhasil di-breakout ke atas ➔ Menjadi **RBS (Support)**.
   - Support kuat H1/Daily berhasil di-breakout ke bawah ➔ Menjadi **SBR (Supply)**.
2. **Tarik Fibonacci Retracement:**
   - Pastikan zona flip tersebut bertepatan atau berada di area **Golden Ratio (Fibonacci 61.8% - 78.6%)**.
3. **Konfirmasi Rejection:**
   - Tunggu harga melakukan *pullback/retest* ke zona flip tersebut dan membentuk *rejection candle* (pinbar atau engulfing).
4. **SL & TP:**
   - `SL` = Di balik batas zona flip + ATR.
   - `TP` = Swing High / Low sebelumnya atau Target 1:2 / 1:3.

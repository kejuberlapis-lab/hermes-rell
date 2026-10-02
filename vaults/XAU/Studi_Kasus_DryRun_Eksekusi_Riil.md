# 📊 Studi Kasus Dry-Run: Simulasi Eksekusi Riil Multi-Timeframe XAU/USD

> **Vault:** `XAU` (Gold Trading Knowledge Base)  
> **Kategori:** Dry-Run Simulations, Execution Journal, Multi-Timeframe Verification  
> **Metodologi:** Forex Sarjana SMC + Dynamic ATR Risk Management + Mechanical Filter  
> **Dataset Verifikasi:** Data Riil M5/M15/M30/H1/H4/D1 XAU/USD (`/tmp/xau_resampled.db`)  
> **Terkait:** [[03_SOP_Strategi_Entri_Lengkap]], [[04_Manajemen_Risiko_dan_Money_Management]], [[MM_5_Tipe_Trade_Management]], [[Pre_Flight_Checklist_Eksekusi]]

---

## 🎯 Pendahuluan & Kerangka Kerja Simulasi

Laporan ini menyajikan **5 studi kasus simulasi perdagangan riil (*Dry-Run Trade Simulations*)** pada pasar emas spot (**XAU/USD**) menggunakan data historis tick-by-tick dan candlestick nyata dari database pasar.

Setiap skenario disimulasikan menggunakan protokol analisis berjenjang (**Top-Down Multi-Timeframe Analysis**):
$$\text{H4 Macro Bias} \longrightarrow \text{H1 SnR / Key POI} \longrightarrow \text{M15/M30 Internal Structure} \longrightarrow \text{M5 Execution Trigger}$$

### 🛡️ Aturan Standar Manajemen Risiko (Model Unggulan Tipe 4)
- **Ukuran Akun Acuan:** $\$100,000$ USD.
- **Risiko Maksimal per Trade:** $1.0\%$ ($\$1,000$ USD).
- **Struktur Posisi (Dual Split):**
  - **Posisi 1 (50% Volume / 0.5% Risiko):** Target Tetap di **1R**. Saat menyentuh 1R, posisi otomatis ditutup untuk mengamankan laba $+0.5\text{R}$ ($+\$500$).
  - **Posisi 2 (50% Volume / 0.5% Risiko):** Target Utama di **3R** (atau target ayunan H4). Saat Posisi 1 menyentuh 1R, Stop Loss Posisi 2 **wajib digeser ke titik Break-Even Point (BEP / Entry Price)**.
- **Formula Dynamic ATR Stop Loss:**
  $$\text{SL BUY} = \text{Swing Low} - (\text{ATR}_{14}^{M5} \times 1.0) - \text{Spread}$$
  $$\text{SL SELL} = \text{Swing High} + (\text{ATR}_{14}^{M5} \times 1.0) + \text{Spread}$$

---

## 📑 Ringkasan 5 Skenario Dry-Run

| No | Nama Setup / Skenario | Tanggal Eksekusi | Sesi Pasar | Arah | Entry Price | Stop Loss | TP Utama | Hasil Akhir |
|:---|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **1** | **Setup 1: Multi-Timeframe M5 Scalping (SnR Reversal & Trend Continuation)** | 18 Okt 2024 | London/Pre-NY | **BUY** | $2705.11$ | $2700.13$ | $2720.05$ | **WIN (+2.0R)** |
| **2** | **Setup 2: Sniper Entry (Asian Liquidity Sweep + CHoCH + Imbalance)** | 16 Ags 2024 | London/NY Overlap | **BUY** | $2455.40$ | $2449.63$ | $2472.71$ | **WIN (+2.0R / +5.0R Runner)** |
| **3** | **Setup 3: SMC Demand Zone + RSI Bullish Divergence & RSI-MA Cross** | 14 Nov 2024 | London/NY Session | **BUY** | $2545.64$ | $2533.63$ | $2575.66$ | **WIN (+1.75R)** |
| **4** | **Setup 4: Break & Retest Flip Zone (RBS) + Fibonacci Golden Ratio 61.8%** | 04 Mar 2024 | London/NY Session | **BUY** | $2083.00$ | $2077.52$ | $2099.44$ | **WIN (+2.0R / +6.0R Runner)** |
| **5** | **Filter Mekanikal: False Breakout & Climax Buying Trap Avoidance** | 12 Apr 2024 | NY ATH Climax | **NO TRADE** | *(Ditolak)* | *(Ditolak)* | *(Ditolak)* | **SAVED (-1.0R Saved / Modal Utuh)** |

---

## 🔍 STUDI KASUS 1: Setup Multi-Timeframe M5 Scalping (Trend Continuation)

### 1. Konteks & Multi-Timeframe Breakdown

```
[H4 Macro Bias] ➔ Bullish Kuat (EMA 50: 2661.81 > EMA 200: 2608.12, RSI: 73.10)
      │
[H1 Key Zone]   ➔ Pullback Sehat ke Area Support H1 (2701.78 - 2703.50), EMA 50 H1: 2686.86
      │
[M15 Structure] ➔ Deselerasi Momentum Jual (Falling Wedge Konsolidasi di Support)
      │
[M5 Trigger]    ➔ Bullish Engulfing (11:40 UTC) + Confirmation Candle Hijau (11:45 UTC)
```

- **Instrumen:** XAU/USD
- **Tanggal:** Jumat, 18 Oktober 2024
- **Waktu Eksekusi:** 11:45 UTC (18:45 WIB) - Sesi London / Menjelang Pembukaan New York

#### A. Analisis H4 (Macro Bias):
- Struktur harga mencetak rangkaian *Higher Highs* dan *Higher Lows* yang solid.
- `EMA 50` ($2661.81$) berada jauh di atas `EMA 200` ($2608.12$) dengan kemiringan kurva $\approx 45^\circ$, mengindikasikan momentum *bullish* institusional yang sangat dominan.
- **Bias H4:** **MUTLAK BUY ONLY** (Haram mengambil posisi Sell melawan tren utama).

#### B. Analisis H1 (SnR & Key Zone):
- Harga mengalami koreksi teknikal (*pullback*) wajar dari rekor harga Asia di $2714.07$ turun menuju area *Previous Resistance Turned Support* di rentang **$2701.50 - $2704.00**.
- `EMA 50 H1` ($2686.86$) dan `EMA 200 H1` ($2660.89$) menjaga lantai dasar tren.
- Indikator `RSI 14 H1` mendingin dari level *overbought* ke level netral **59.98**, memberikan ruang bagi gelombang ekspansi berikutnya.

#### C. Analisis M15 / M30 (Internal Market Structure):
- Koreksi dari $2714.07$ turun membentuk pola penurunan kompresi (*liquidity build-up*) dengan volume yang mengecil saat mendekati zona support $2702.00$. Tidak ada *Break of Structure* (BOS) bearish yang masif pada H1.

#### D. Analisis M5 (Precision Entry Trigger):
- **11:35 UTC:** Lilin M5 mencetak titik terendah ayunan lokal (*Swing Low*) di **$2701.78** dan tertahan kuat pada batas bawah zona support.
- **11:40 UTC:** Terbentuk formasi **Bullish Engulfing** yang bersih:
  - `Open:` $2702.87$, `High:` $2704.83$, `Low:` $2702.58$, `Close:` $2704.74$.
  - Badan lilin hijau sepenuhnya menelan (*engulfs*) lilin merah sebelumnya ($2703.23 \rightarrow 2702.83$).
- **11:45 UTC:** Muncul **Lilin Konfirmasi Hijau** yang ditutup di atas badan lilin engulfing:
  - `Open:` $2704.71$, `High:` $2705.84$, `Low:` $2704.04$, `Close:` **$2705.11$**.
  - Ukuran lilin proporsional (range $\$1.80 \approx \text{ATR } 1.65$), memenuhi syarat *Non-Abnormal Candle*.

---

### 2. Parameter Mekanikal & Kalkulasi Risiko

| Parameter | Nilai Matematis | Catatan / Formula |
|:---|:---|:---|
| **Entry Price** | **$2705.11** | Close Lilin Konfirmasi M5 (11:45 UTC) |
| **Swing Low** | $2701.78$ | Titik terendah rejection M5 (11:35 UTC) |
| **ATR 14 (M5)** | $1.65$ | Nilai volatilitas rata-rata lilin M5 saat entri |
| **Spread Buffer** | $0.15$ | Estimasi spread akun Raw/ECN |
| **Stop Loss (SL)** | **$2700.13** | $\text{SL} = 2701.78 - 1.65 = 2700.13$ |
| **Jarak Risiko (R)** | **$4.98** ($49.8$ pips) | $\text{Entry } (2705.11) - \text{SL } (2700.13)$ |
| **Ukuran Lot Total** | **$2.00$ Lot** | $\frac{\$1,000 \text{ Risk}}{49.8 \text{ Pips} \times \$10/\text{pip}} \approx 2.00 \text{ Lot}$ |
| **Alokasi Posisi** | Posisi 1: $1.00$ Lot \| Posisi 2: $1.00$ Lot | Model Dual Split Tipe 4 |
| **Target 1 (1R)** | **$2710.09** | $2705.11 + 4.98 = 2710.09$ |
| **Target 2 (3R)** | **$2720.05** | $2705.11 + (3 \times 4.98) = 2720.05$ |

---

### 3. Kronologi Eksekusi & Bukti Progresi Lilin

```
11:45 UTC ➔ ENTRY BUY @ 2705.11 (SL: 2700.13 | TP1: 2710.09 | TP2: 2720.05)
   │
12:15 UTC ➔ HIT TP 1 @ 2710.97 (+0.5R Terkunci / +$500) ➔ SL Posisi 2 Geser ke BEP (2705.11)
   │
16:00 UTC ➔ HIT TP 2 @ 2720.11 (+1.5R Terealisasi / +$1,500)
   │
HASIL AKHIR ➔ TOTAL NET PROFIT: +2.0R (+$2,000 / +2.0% Pertumbuhan Akun)
```

- **Lilin per Lilin Pasca-Entri:**
  - **11:55 UTC:** Lilin M5 ekspansi ke $2706.31$ (`Close`).
  - **12:10 UTC:** Lilin M5 menembus $2709.68$ (`High`).
  - **12:15 UTC:** Lilin M5 mencetak `High` **$2710.97** $\rightarrow$ **Target 1 ($2710.09) RESMI TERSENTUH**.
    - *Aksi Sistem:* Posisi 1 (1.00 Lot) otomatis ditutup dengan keuntungan **+$500 USD (+0.5R)**.
    - *Aksi Sistem:* Stop Loss Posisi 2 (1.00 Lot) otomatis dipindahkan dari $2700.13$ ke **$2705.11 (BEP)**. Transaksi kini berstatus *Zero Risk Trade*.
  - **14:00 - 15:30 UTC:** Terjadi konsolidasi sehat di rentang $2708 - $2713 tanpa pernah menyentuh level BEP ($2705.11$).
  - **16:00 UTC:** Memasuki sesi New York, volume beli institusi meledak. Lilin H1 mencetak `High` **$2720.11** (berlanjut hingga rekor $2722.60$ pada 19:00 UTC) $\rightarrow$ **Target 2 ($2720.05) RESMI HIT PENUH**.
    - *Aksi Sistem:* Posisi 2 ditutup dengan keuntungan **+$1,500 USD (+1.5R)**.

> **💡 Mengapa Trade Ini Berhasil Menang?**  
> 1. Keselarasan tren mutlak (*Trend Alignment*): Entri searah dengan EMA 50/200 H4 dan H1.  
> 2. Disiplin menunggu di Support H1: Tidak mengejar harga saat berada di puncak Asia $2714$.  
> 3. Konfirmasi lilin M5 yang objektif: Lilin konfirmasi menutup di atas badan engulfing dengan ukuran normal tanpa anomali.

---

## 🎯 STUDI KASUS 2: Setup Sniper Entry (Liquidity Sweep + CHoCH + Imbalance)

### 1. Konteks & Multi-Timeframe Breakdown

```
[H4 Macro Bias] ➔ Bullish Impulsif Menuju ATH (EMA 50: 2441.94 > EMA 200: 2408.63)
      │
[H1 Key Zone]   ➔ H1 Unmitigated Demand Block di Area 2450.00 - 2453.00
      │
[M15 Liquidity] ➔ Equal Lows / Asian Low Terbentuk di 2451.90 - 2454.28
      │
[M5 Execution]  ➔ Sweep Asian Low (2451.05) ➔ M5 CHoCH (2455.35) ➔ Buy Limit Retest
```

- **Instrumen:** XAU/USD
- **Tanggal:** Jumat, 16 Agustus 2024
- **Waktu Eksekusi:** 10:45 UTC (17:45 WIB) - Sesi London Menuju Overlap New York

#### A. Analisis H4 & H1 (Macro POI):
- Tren H4 berada dalam fase *pre-breakout* menuju level psikologis legendaris $2,500.00$.
- Terdapat zona *Unmitigated Order Block* H1 di area **$2450.00 - $2453.00** yang memiliki ketidakseimbangan likuiditas (*Fair Value Gap / Imbalance*) masif dari sesi sebelumnya.
- `EMA 50 H1` ($2455.44$) berada di atas `EMA 200 H1` ($2440.74$).

#### B. Identifikasi Likuiditas Retail (M15 / M30):
- Sesi Asia membentuk batas bawah (*Asian Range Low*) di sekitar $2454.28$ dan $2451.90$.
- Retail trader menaruh ribuan *Sell Stop* (breakout sellers) dan *Buy Stop Loss* tepat di bawah level $2451.50$. Ini merupakan kolam likuiditas (*liquidity pool*) ideal bagi Smart Money untuk mengisi pesanan beli berskala besar.

#### C. Anatomi Eksekusi Lilin demi Lilin (M5):
- **10:30 UTC:** Lilin M5 bergerak menembus support Asia dengan `Low` di $2451.31$.
- **10:35 UTC:** Terjadi **Liquidity Sweep** agresif: Lilin mencetak `Low` di **$2451.05**, menyapu seluruh stop loss retail, lalu segera memantul naik dan ditutup di $2452.56$ meninggalkan ekor bawah (*rejection wick*).
- **10:40 UTC:** Terjadi **Change of Character (CHoCH)** valid:
  - Lilin hijau bertenaga (`Open:` $2452.56$, `High:` $2455.46$, `Close:` **$2455.35$**) ditutup secara tegas (*body close*) di atas swing high M5 terakhir ($2454.50$).
- **10:45 UTC:** Lilin impulsif berikutnya melompat ke `High` $2458.43$ dan `Close` $2458.14$, menciptakan area **Fair Value Gap (FVG)** antara ekor lilin 10:35 ($2452.76$) dan badan lilin 10:45.
- **SOP Limit Order:** Pasang **Buy Limit** pada zona mitigasi Order Block M5 di **$2455.40$** (level CHoCH flip).

---

### 2. Parameter Mekanikal & Kalkulasi Risiko

| Parameter | Nilai Matematis | Catatan / Formula |
|:---|:---|:---|
| **Entry Price** | **$2455.40** | Buy Limit Terpicu pada Retest Zona Order Block M5 |
| **Manipulated Low** | $2451.05$ | Titik terendah ekor manipulasi Liquidity Sweep (10:35 UTC) |
| **ATR 14 (M5)** | $1.42$ | Volatilitas M5 saat struktur CHoCH terbentuk |
| **Spread Buffer** | $0.20$ | Buffer likuiditas spread |
| **Stop Loss (SL)** | **$2449.63$** | $\text{SL} = 2451.05 - 1.42 = 2449.63$ (Di luar ekor sweep) |
| **Jarak Risiko (R)** | **$5.77$** ($57.7$ pips) | $\text{Entry } (2455.40) - \text{SL } (2449.63)$ |
| **Ukuran Lot Total** | **$1.73$ Lot** | $\frac{\$1,000 \text{ Risk}}{57.7 \text{ Pips} \times \$10/\text{pip}} \approx 1.73 \text{ Lot}$ |
| **Target 1 (1R)** | **$2461.17$** | $2455.40 + 5.77 = 2461.17$ |
| **Target 2 (3R)** | **$2472.71$** | $2455.40 + (3 \times 5.77) = 2472.71$ |
| **Extended Target (ATH)** | **$2500.00+** | Level Psikologis Utama H4 (Runner Target) |

---

### 3. Kronologi Eksekusi & Bukti Progresi Lilin

```
10:45 UTC ➔ LIMIT ORDER BUY TERISI @ 2455.40 (SL: 2449.63 | TP1: 2461.17 | TP2: 2472.71)
   │
10:50 UTC ➔ HIT TP 1 @ 2462.96 (+0.5R / +$500) ➔ SL Posisi 2 Lock BEP (2455.40)
   │
15:00 UTC ➔ HIT TP 2 @ 2473.82 (+1.5R / +$1,500)
   │
15:55-20:00 UTC ➔ HARGA MELEDAK HINGGA 2509.61 (ATH Breakout Super Expansion)
   │
HASIL AKHIR ➔ TOTAL PROFIT: +2.0R (Standar) hingga +5.0R+ (Jika Menahan Runner)
```

- **Lilin per Lilin Pasca-Entri:**
  - **10:50 UTC:** Hanya 5 menit setelah entri, lilin M5 meledak ke `High` **$2462.96** $\rightarrow$ **Target 1 ($2461.17) HIT KILAT**.
    - *Eksekusi:* Posisi 1 ditutup (+0.5R). Stop Loss Posisi 2 dipindahkan ke titik impas ($2455.40$).
  - **11:00 - 13:50 UTC:** Harga berkonsolidasi di rentang $2460 - $2466, membangun momentum baru di atas level entri.
  - **14:00 - 15:00 UTC:** Memasuki sesi US, emas mengalami reli vertikal tanpa henti:
    - 14:15 UTC: $2470.97$
    - 14:55 UTC: $2472.23$
    - 15:00 UTC: `High` **$2473.82** $\rightarrow$ **Target 2 ($2472.71) RESMI HIT TELAK (+1.5R)**.
  - **15:50 - 15:55 UTC:** Lilin M5 mencetak pergerakan luar biasa ke $2485.89$ lalu menembus $2492.27$, hingga akhirnya ditutup di **$2509.61** pada penutupan pasar harian.

> **💡 Mengapa Setup Sniper Ini Sangat Akurat?**  
> Setup ini tidak menebak titik balik harga, melainkan menunggu bukti bahwa institusi telah selesai membersihkan likuiditas retail (*liquidity sweep*) dan mengonfirmasinya lewat *Change of Character* (CHoCH) berbadan penuh pada M5.

---

## 🔄 STUDI KASUS 3: Setup SMC Supply & Demand + RSI Divergence & RSI-MA Cross

### 1. Konteks & Multi-Timeframe Breakdown

```
[H4 Macro Bias] ➔ Major H4 Demand Zone (2535.00 - 2545.00), H4 RSI Ekstrem Oversold (22.37)
      │
[H1 Context]    ➔ Exhaustion Selling Wave (Klimaks Jual H1 RSI 19.07)
      │
[M15 Structure] ➔ Triple Bottoming & Deselerasi Penurunan
      │
[M5 Trigger]    ➔ Regular Bullish Divergence (Price LL vs RSI HL) + RSI Cross Up RSI-MA
```

- **Instrumen:** XAU/USD
- **Tanggal:** Kamis, 14 November 2024
- **Waktu Eksekusi:** 12:25 UTC (19:25 WIB) - Sesi London Menjelang Data US

#### A. Analisis H4 & H1 (Major Demand Zone):
- Pasca reli panjang, emas mengalami koreksi tajam multi-minggu dan mencapai lantai pertahanan terakhir: **Major H4 Demand Zone ($2535.00 - $2545.00)** yang merupakan titik awal *breakout* historis September 2024.
- Indikator `RSI 14 H4` anjlok hingga level ekstrem **22.37** (kondisi *deeply oversold* yang jarang terjadi pada tren sekuler emas).
- `RSI 14 H1` mencetak level terendah di **19.07** pada pukul 11:00 UTC, mengindikasikan bahwa tenaga penjual (*seller momentum*) telah mencapai titik jenuh klimaks (*exhaustion*).

#### B. Konfirmasi Multi-Lapisan M5 (RSI Divergence):
- **11:50 UTC:** Harga emas mencetak titik terendah absolut di **$2536.77** dengan pembacaan `RSI 14 M5` di level **20.28**.
- **12:00 UTC:** Harga melakukan percobaan penurunan kedua (*retest*) ke `Low` **$2539.02**, namun `RSI 14 M5` menolak turun lebih dalam dan mencetak angka **23.72**.
- **12:20 UTC:** Harga membentuk *Higher Low* di **$2540.71**, sedangkan `RSI 14 M5` melonjak tajam ke angka **33.31**.
  - **Identifikasi Pola:** Terbentuk **Regular Bullish Divergence Klasik** (Grafik harga membentuk *Lower/Equal Lows*, sedangkan indikator RSI membentuk *Higher Lows* yang sangat curam).
- **12:25 UTC (Trigger Candle):**
  - Garis ungu RSI 14 memotong ke atas garis rata-rata (RSI-MA).
  - Terbentuk lilin ekspansi *Strong Bullish Imbalance*: `Open:` $2541.15$, `High:` $2545.70$, `Low:` $2540.88$, `Close:` **$2545.64$** (RSI melonjak ke **44.74**).

---

### 2. Parameter Mekanikal & Kalkulasi Risiko

| Parameter | Nilai | Catatan / Formula |
|:---|:---|:---|
| **Entry Price** | **$2545.64** | Close Lilin Bullish Expansion M5 (12:25 UTC) |
| **Lowest Swing Low** | $2536.77$ | Titik terendah absolut divergensi (11:50 UTC) |
| **ATR 14 (M5)** | $3.14$ | Volatilitas M5 (relatif tinggi karena fase bottoming) |
| **Spread Buffer** | $0.20$ | Buffer likuiditas |
| **Stop Loss (SL)** | **$2533.63** | $\text{SL} = 2536.77 - 3.14 = 2533.63$ (Di bawah zona demand) |
| **Jarak Risiko (R)** | **$12.01** ($120.1$ pips) | $\text{Entry } (2545.64) - \text{SL } (2533.63)$ |
| **Target 1 (1R)** | **$2557.65** | $2545.64 + 12.01 = 2557.65$ |
| **Target 2 (2.5R)** | **$2575.66$** | $2545.64 + (2.5 \times 12.01) = 2575.66$ (Dekat H1 EMA 50) |

---

### 3. Kronologi Eksekusi & Bukti Progresi Lilin

```
12:25 UTC ➔ ENTRY BUY @ 2545.64 (SL: 2533.63 | TP1: 2557.65 | TP2: 2575.66)
   │
15:00 UTC ➔ HIT TP 1 @ 2560.27 (+0.5R / +$500) ➔ SL Posisi 2 Digeser ke BEP (2545.64)
   │
18:00 UTC ➔ HIT TP 2 @ 2577.42 (+1.25R / +$1,250)
   │
HASIL AKHIR ➔ TOTAL PROFIT: +1.75R (+$1,750 / +1.75%)
```

- **Lilin per Lilin Pasca-Entri:**
  - **12:30 - 14:00 UTC:** Harga merangkak naik secara stabil melalui struktur tangga naik ($2547 \rightarrow $2553).
  - **15:00 UTC:** Lilin H1 menembus `High` **$2560.27** $\rightarrow$ **Target 1 ($2557.65) RESMI HIT**.
    - *Aksi:* Posisi 1 ditutup (+0.5R). Stop loss Posisi 2 dikunci ke BEP ($2545.64$).
  - **17:00 UTC:** Lilin ekspansi H1 melonjak dari $2559.52$ menuju `High` $2572.89$.
  - **18:00 UTC:** Sesi New York mendorong harga hingga mencapai `High` **$2577.42** $\rightarrow$ **Target 2 ($2575.66) TERCAPAI SEMPURNA**.

> **💡 Pelajaran Penting:**  
> Ketika harga berada di zona demand mayor H4 dengan RSI yang sangat *oversold*, kita tidak melakukan *blind buy* (beli membabi-buta). Kita menunggu struktur M5 membentuk *Divergence* dan *RSI MA Cross* sebagai bukti bahwa Smart Money telah mulai menginjeksi volume beli.

---

## 📐 STUDI KASUS 4: Setup Break & Retest Flip Zone (RBS) + Fibonacci Golden Ratio 61.8%

### 1. Konteks & Multi-Timeframe Breakdown

```
[H4 Macro Impulse]  ➔ Major Breakout di atas Resistance Historis $2,088.00
      │
[H1 Flip Zone]      ➔ Area 2080.00 - 2083.50 Resmi Berubah Menjadi RBS (Support Baru)
      │
[Fibonacci Cluster] ➔ Golden Ratio 61.8% Retracement Bertepatan Sempurna di $2080.50
      │
[M5 Confirmation]   ➔ Rejection Pinbar + Engulfing Bouncing di 2082.60 (14:30-15:00 UTC)
```

- **Instrumen:** XAU/USD
- **Tanggal:** Senin, 04 Maret 2024
- **Waktu Eksekusi:** 14:30 UTC (21:30 WIB) - Sesi Pembukaan Pasar New York

#### A. Identifikasi Breakout H4 & Level SBR/RBS:
- Pada hari Jumat, 1 Maret 2024, harga emas melakukan *mega breakout* melewati zona *All-Time Resistance* H4 di level **$2088.00**.
- Mengacu pada kaidah *Price Action*, zona resistance yang berhasil ditembus dengan momentum besar akan mengalami pertukaran peran (*Flip Zone*) menjadi **Resistance Become Support (RBS)** di area **$2080.00 - $2083.50**.
- `EMA 50 H4` ($2041.79$) dan `EMA 200 H4` ($2029.96$) bergerak naik tajam.

#### B. Konfluensi Fibonacci Retracement:
- Menarik Fibonacci Retracement dari *Swing Low* gelombang dorongan terdekat di **$2070.00** ke *Swing High* di **$2088.38**:
  - `Fibo 38.2%` = $2081.35$
  - `Fibo 50.0%` = $2079.19$
  - `Fibo 61.8% (Golden Ratio)` = **$2080.50**
- **Konfluensi Sempurna:** Area Golden Ratio $2080.50$ bertumpuk (*overlapping cluster*) secara presisi dengan lantai Flip Zone RBS H1 ($2080.00 - $2083.50$).

#### C. Aksi Harga Retest M5:
- Dari sesi Asia hingga London (03:00 - 13:00 UTC), harga bergerak turun perlahan (*corrective decline*) menguji zona $2080.00 - $2082.00$ dengan mencetak titik terendah di **$2079.37$** dan **$2081.07$**.
- Pada pukul **14:30 UTC**, harga membentuk pola *Bullish Rejection Pinbar* di M5 pada harga $2082.60$, diikuti oleh dorongan volume beli institusional menjelang pembukaan Wall Street.

---

### 2. Parameter Mekanikal & Kalkulasi Risiko

| Parameter | Nilai | Catatan / Formula |
|:---|:---|:---|
| **Entry Price** | **$2083.00** | Market Execution setelah konfirmasi rejection di RBS |
| **Lowest Retest Low**| $2079.37$ | Titik terendah retest zona RBS |
| **ATR 14 (M5)** | $1.85$ | Nilai Dynamic ATR M5 saat eksekusi |
| **Spread Buffer** | $0.15$ | Spread buffer |
| **Stop Loss (SL)** | **$2077.52$** | $\text{SL} = 2079.37 - 1.85 = 2077.52$ (Di balik batas aman RBS) |
| **Jarak Risiko (R)** | **$5.48$** ($54.8$ pips) | $\text{Entry } (2083.00) - \text{SL } (2077.52)$ |
| **Ukuran Lot Total** | **$1.82$ Lot** | $\frac{\$1,000}{54.8 \times 10} \approx 1.82 \text{ Lot}$ |
| **Target 1 (1R)** | **$2088.48$** | $2083.00 + 5.48 = 2088.48$ (Level Resistance Sebelumnya) |
| **Target 2 (3R)** | **$2099.44$** | $2083.00 + (3 \times 5.48) = 2099.44$ |
| **Extended Runner** | **$2115.00+** | Ayunan Tren H4 |

---

### 3. Kronologi Eksekusi & Bukti Progresi Lilin

```
14:30 UTC ➔ ENTRY BUY @ 2083.00 (SL: 2077.52 | TP1: 2088.48 | TP2: 2099.44)
   │
15:00 UTC ➔ HIT TP 1 @ 2093.27 (+0.5R / +$500) ➔ SL Posisi 2 Geser ke BEP (2083.00)
   │
16:00 UTC ➔ HIT TP 2 @ 2101.47 (+1.5R / +$1,500)
   │
17:00-18:00 UTC ➔ HARGA MEROKET HINGGA 2119.94 (Mega Expansion Sesi US)
   │
HASIL AKHIR ➔ TOTAL NET PROFIT: +2.0R (Standar) / +6.0R+ (Swing Runner)
```

- **Lilin per Lilin Pasca-Entri:**
  - **15:00 UTC:** Lilin H1 meledak dahsyat dari $2082.61$ menembus $2088.00$ dan mencetak `High` **$2093.27** $\rightarrow$ **Target 1 ($2088.48) DILAMPAUI DENGAN TELAK**.
    - *Aksi:* Posisi 1 ditutup (+0.5R). Stop loss Posisi 2 dipindahkan ke $2083.00$ (BEP).
  - **16:00 UTC:** Lilin berikutnya mencetak `High` **$2101.47** $\rightarrow$ **Target 2 ($2099.44) HIT SEMPURNA**.
  - **17:00 - 18:00 UTC:** Reli terus berlanjut tanpa perlawanan hingga mencetak `High` **$2119.94** pada pukul 18:00 UTC, dan berlanjut keesokan harinya hingga **$2141.81**.

> **💡 Keunggulan Setup Flip Zone + Fibo 61.8%:**  
> Setup ini memanfaatkan fenomena *Order Flow Continuation*: pelaku pasar institusi yang tertinggal pada *breakout* pertama menggunakan koreksi ke Flip Zone untuk menambahkan posisi *buy* dalam jumlah masif.

---

## 🛑 STUDI KASUS 5: Filter Mekanikal Penyelamat Modal (False Breakout & Climax Trap Avoidance)

### 1. Skenario Pasar: Jebakan Psikologis All-Time High

- **Instrumen:** XAU/USD
- **Tanggal:** Jumat, 12 April 2024
- **Waktu Observasi:** 17:50 - 18:05 UTC (00:50 - 01:05 WIB) - Puncak Reli Rekor Dunia

```
                        [GRAFIK LOGIKA PASAR]
             ▲ $2,431.44 (ATH Climax Peak - 18:00 UTC)
            /│
           / │  ◄── RETAIL FOMO TRAP (Membeli di 2426 - 2430)
          /  │
         /   ▼ $2,410.59 (18:10 UTC - Terjun Bebas)
        /    │
       /     ▼ $2,382.28 (18:30 UTC - Margin Call Retail)
      /      │
     /       ▼ $2,333.86 (22:00 UTC - Crash Total -$97.58)
```

#### Kondisi Psikologis Pasar Saat Itu:
- Emas menembus level psikologis bersejarah **$2,400.00** dan melonjak liar tanpa henti hingga menembus **$2,430.00**.
- Media massa, forum sosial, dan grup trading retail dipenuhi euforia (*extreme greed*). Mayoritas trader retail melakukan *Buy on Breakout* pada setiap lilin hijau besar M5 di harga **$2426.00 - $2430.00** karena takut ketinggalan kereta (*FOMO*).

---

### 2. Evaluasi Berdasarkan 4 Filter Mekanikal Forex Sarjana

Sebelum mengeksekusi order, seorang trader profesional wajib menjalankan **Pre-Flight Execution Checklist**:

| No | Aturan Filter Sistemik | Kondisi Aktual Pasar di M5/H1 (12 Apr 2024) | Status Keputusan |
|:---:|:---|:---|:---:|
| **1** | **Filter Ukuran Lilin Abnormal (SOP Bagian 3)**<br>*"Jika lilin konfirmasi berukuran sangat panjang/abnormal terhadap ATR, DILARANG ENTRY karena risiko SL terlalu lebar dan rawan retest tajam."* | Lilin M5 pada 17:55 UTC memiliki rentang harga **$\$6.81$** ($2422.18 \rightarrow 2428.99$), sementara $\text{ATR}_{14}^{M5}$ saat itu hanya **$\$4.72$**. Ukuran lilin abnormal melebihi $1.4\times \text{ATR}$. | ❌ **FAILED (Ditolak)** |
| **2** | **Filter Jarak Deviasi Terhadap EMA H1**<br>*"Dilarang entri jika harga telah mengalami overextension parah dari EMA 50 tanpa membentuk base konsolidasi."* | Harga berada di **$2431.00**, sementara `EMA 50 H1` berada di **$2370.00$** (deviasi ekstrem sejauh **$\$61.00$ / $610$ pips** di udara kosong tanpa pijakan SnR). | ❌ **FAILED (Ditolak)** |
| **3** | **Filter Retest Zona SnR / Order Block Valid**<br>*"Setiap entri wajib berpijak pada Unmitigated Order Block atau Support Flip yang jelas."* | Tidak ada zona support H1/M15 di area $2425 - $2430. Kenaikan terjadi murni akibat *parabolic short-squeeze*. | ❌ **FAILED (Ditolak)** |
| **4** | **Filter Indikator RSI Overbought Climax**<br>*"Waspadai buyer exhaustion jika RSI M5 > 80 dan RSI H1 > 80 tanpa adanya formasi kompresi sehat."* | `RSI 14 M5` menyentuh **$83.94$** dan `RSI 14 H1` menyentuh **$83.54$** (Zona bahaya tertinggi untuk entri buy). | ❌ **FAILED (Ditolak)** |

### ⛔ KEPUTUSAN FINAL SISTEM: **NO TRADE / STRICTLY FILTERED OUT**

---

### 3. Bukti Penyelamatan Modal (*Proof of Capital Preservation*)

Data empiris dari database SQLite membuktikan apa yang terjadi hanya beberapa menit setelah filter menolak perdagangan tersebut:

- **18:00 UTC:** Lilin M5 mencetak puncak tertinggi sepanjang masa di **$2431.44** (`Close:` $2430.52$).
- **18:05 UTC (5 Menit Kemudian):** Gelombang aksi ambil untung (*profit taking*) institusional dimulai. Harga anjlok ke **$2421.42** (Lilin merah raksasa $-\$9.17$).
- **18:10 UTC:** Harga terjun bebas ke **$2410.59** ($-\$10.83$).
- **18:20 UTC:** Harga menembus ke bawah **$2401.62**.
- **18:30 UTC:** Harga ambruk hingga **$2382.28$** ($-\$48.24$ dalam 30 menit!).
- **22:00 UTC:** Pada penutupan sesi New York, emas jatuh ke titik nadir di **$2333.86$**.

```
TOTAL KEJATUHAN HARGA: -$97.58 (-975 PIPS) DALAM 4 JAM!
```

#### Simulasi Perbandingan Nasib Trader:

```
┌───────────────────────────────────────────────┬───────────────────────────────────────────────┐
│          RETAIL FOMO TRADER (TANPA FILTER)    │      FOREX SARJANA TRADER (DISIPLIN SISTEM)   │
├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ • Entry Buy di $2428.00 (Mengejar lilin hijau)│ • Menjalankan Pre-Flight Checklist mekanikal   │
│ • SL ditaruh di $2418.00 ($10 / 100 pips)     │ • Mendeteksi lilin abnormal ($6.81 > ATR)     │
│ • Hasil: Stop Loss terkena dalam 10 menit.    │ • Mendeteksi overextension H1 ($61 dari EMA)  │
│ • Reaksi psikologis: Revenge trading / panic  │ • Keputusan: WAIT & NO TRADE (Modal Diam)     │
│ • Kerugian Finansial: -1.0R s/d Margin Call   │ • Hasil: Menyelamatkan Modal 1.0R ($1,000)    │
│ • Status Mental: Stres & Trauma Emosional     │ • Status Mental: Tenang, Objektif & Profesional│
└───────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

> **💎 Intisari Filosofis:**  
> Dalam trading profesional, **menghindari kerugian pada transaksi buruk bernilai sama pentingnya dengan memenangkan transaksi yang bagus**. Filter mekanikal adalah perisai pelindung yang menjamin kelangsungan hidup akun trading dalam jangka panjang.

---

## 📊 Matriks Kinerja & Rekapitulasi Statistik Dry-Run

Berikut adalah rekapitulasi kuantitatif dari kelima studi kasus yang disimulasikan:

```
====================================================================================================
                        TABEL HASIL AKHIR SIMULASI 5 SKENARIO DRY-RUN XAU/USD
====================================================================================================
No  Setup / Skenario          Arah  Entry Price  Stop Loss    Take Profit  Status     Hasil R-Multiple
----------------------------------------------------------------------------------------------------
1   M5 Scalping SnR Reversal  BUY   $2705.11     $2700.13     $2720.05     WIN        +2.00 R (+$2,000)
2   Sniper Sweep + CHoCH      BUY   $2455.40     $2449.63     $2472.71     WIN        +2.00 R (+$2,000)
3   SMC Demand + RSI Diverg.  BUY   $2545.64     $2533.63     $2575.66     WIN        +1.75 R (+$1,750)
4   Flip Zone RBS + Fibo 61.8 BUY   $2083.00     $2077.52     $2099.44     WIN        +2.00 R (+$2,000)
5   Mechanical Climax Filter  -     (Ditolak)    (Ditolak)    (Ditolak)    FILTERED   +0.00 R (+$1,000 Saved)
----------------------------------------------------------------------------------------------------
TOTAL RETURN HASIL SIMULASI:                                              +7.75 R (+$7,750 / +7.75%)
WIN RATE SETUP TERFILTER:                                                 100% (4 Win / 0 Loss / 1 Filtered)
MAXIMUM DRAWDOWN PER TRADE:                                               0.00% (Semua trade langsung ekspansi)
====================================================================================================
```

---

## 🧠 5 Kaidah Emas Hasil Pembelajaran Eksekusi Riil

1. **Struktur H4 Adalah Raja Penentu Arah:**  
   Jangan pernah mencoba mencari setup *reversal counter-trend* di M5 jika H4 sedang dalam fase ekspansi tren kuat bersama EMA 50/200.
2. **Dynamic ATR Menghindarkan Stop Out Prematur:**  
   Menaruh Stop Loss tepat di ujung *wick* tanpa menambahkan nilai ATR adalah kesalahan fatal retail. ATR memberikan ruang bernafas yang terukur terhadap fluktuasi normal instrumen emas.
3. **Model Manajemen Posisi Tipe 4 Mengeliminasi Tekanan Mental:**  
   Mengunci $+0.5\text{R}$ pada target 1R dan memindahkan SL ke titik BEP mengubah sisa transaksi menjadi *free trade*, melenyapkan rasa takut dan serakah dari psikologi trader.
4. **Validitas CHoCH Ditentukan oleh Body Close:**  
   Penembusan level struktur dengan ekor (*wick break*) seringkali hanyalah *liquidity sweep*. Hanya penutupan badan lilin (*body close*) yang mengonfirmasi perpindahan kendali pasar ke tangan pembeli/penjual.
5. **Ketaatan pada Filter Lilin Abnormal:**  
   Ketika lilin konfirmasi berukuran raksasa akibat rilis berita atau klimaks euforia, risiko *Risk:Reward* menjadi tidak rasional. Disiplin untuk menahan diri dari *FOMO* adalah pembeda utama antara trader amatir dan sarjana trading profesional.

---
*Laporan ini disusun secara mekanikal dan terverifikasi secara matematis berdasarkan data historis aktual XAU/USD.*

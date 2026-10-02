# 🎯 Setup 2: Sniper Entry (Liquidity Sweep + Imbalance)

> **Vault:** `XAU` | **Topik:** SOP Setup Entri | **Terkait:** [[SMC_Liquidity_Sweep]], [[SMC_Order_Block_dan_Imbalance]], [[SMC_BOS_dan_CHoCH]]

---

## 1. Spesifikasi Setup
- **Fokus:** Menangkap entri presisi dengan Risk:Reward tinggi (**1:3 hingga 1:5**) setelah manipulasi institusi selesai.
- **Timeframe:** H1 (Unmitigated Order Block) ➔ M5 (CHoCH & Liquidity Sweep).

---

## 2. Alur Eksekusi

1. **Identifikasi Zona H1:**
   - Cari Order Block yang masih *fresh (unmitigated)* yang sebelumnya menghasilkan Major BOS dan Imbalance.
2. **Konfirmasi CHoCH di M5:**
   - Saat harga masuk ke Order Block H1, amati struktur M5 hingga terjadi *Change of Character (CHoCH)* valid (break body + imbalance).
3. **Tandai Titik Likuiditas:**
   - Tandai Swing Low (untuk buy) atau Swing High (untuk sell) sebagai *Liquidity Level*.
4. **Tunggu Liquidity Sweep:**
   - Tunggu harga menusuk melewati level likuiditas, lalu segera memantul balik dan mencetak **Candle Imbalance Baru**.
5. **Eksekusi Pending Order:**
   - **Buy Limit:** Pasang pada candle merah terakhir sebelum imbalance (+ spread).
   - **Sell Limit:** Pasang pada candle hijau terakhir sebelum imbalance.

---

## 3. Parameter Risiko & Target
- **Stop Loss:** Beberapa pips di balik ujung ekor sapuan manipulasi (*Sweep Wick*).
- **Take Profit:** Target **1:3** hingga **1:5** dari jarak Stop Loss.

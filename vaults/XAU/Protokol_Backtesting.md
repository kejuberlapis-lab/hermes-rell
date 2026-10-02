# 🔬 Protokol: Standar Uji Backtesting Mekanikal

> **Vault:** `XAU` | **Topik:** Riset & Validasi Data | **Terkait:** [[Psikologi_Mindset_Stop_Loss]], [[Pre_Flight_Checklist_Eksekusi]]

---

## 1. Tujuan Backtesting
Backtesting bertujuan untuk mendapatkan **keyakinan statistik (*statistical confidence*)** sehingga trader tidak ragu atau panik saat mengalami serangkaian kekalahan berturut-turut di pasar riil.

---

## 2. Aturan Pelaksanaan Uji
1. **Jumlah Sampel:** Uji minimal **50 hingga 100 sampel transaksi historis**.
2. **Kondisi Pengujian:**
   - Gunakan aturan entry, stop loss, dan take profit yang 100% kaku dan mekanikal.
   - Sertakan perhitungan spread broker aktual.

---

## 3. Metrik Evaluasi Kunci

| Metrik | Deskripsi | Target Ideal |
|---|---|---|
| **Win Rate (%)** | Persentase trade yang berakhir profit | 45% – 60% |
| **Risk:Reward Ratio** | Perbandingan rata-rata keuntungan vs kerugian | Minimal 1:2 atau 1:3 |
| **Max Consecutive Losses** | Rekor kekalahan beruntun terpanjang | Diketahui agar tidak panik saat terjadi di akun riil |
| **Profit Factor** | Total Gross Profit / Total Gross Loss | > 1.75 |

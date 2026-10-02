# 🛡️ MM: Kalkulasi Lot Dinamis & Pengendalian Risiko

> **Vault:** `XAU` | **Topik:** Money Management | **Terkait:** [[Indikator_ATR_Dynamic_Stop_Loss]], [[MM_5_Tipe_Trade_Management]]

---

## 1. Prinsip Utama: Mengapa Dynamic Lot?
Ukuran Stop Loss (dalam pips) selalu berubah-ubah di setiap setup. Menggunakan fixed lot (misal selalu 0.10 lot) akan membuat risiko kerugian tidak stabil (kadang rugi kecil, kadang rugi besar).

Kalkulasi **Lot Dinamis** memastikan bahwa di manapun Stop Loss diletakkan, jika terkena SL, kerugian akun tetap terkunci persis di **1% atau 2% dari modal**.

---

## 2. Rumus Kalkulasi Lot

$$\text{Ukuran Lot} = \frac{\text{Modal Akun} \times \text{Persentase Risiko}}{\text{Jarak Stop Loss (Pips)} \times \text{Nilai Per Pip}}$$

### Contoh Kasus pada XAU/USD (Gold):
- **Modal:** $1,000
- **Risiko per Trade:** 1% ($10)
- **Jarak SL:** 20 pips ($2.00 pada Gold)
- **Perhitungan:**
  $$\text{Lot} = \frac{\$10}{20 \text{ pips} \times \$1.00} = \mathbf{0.05 \text{ Lot}}$$

---

## 3. Aturan Batasan Risiko
1. **Risiko Normal:** 1% per transaksi.
2. **Risiko Agresif (Maksimal):** 2% per transaksi.
3. **Maksimal Risiko Terbuka (Max Open Risk):** Maksimal 3% total risiko dari seluruh posisi yang sedang terbuka bersamaan.

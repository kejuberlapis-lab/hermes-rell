# 🌐 9Chain (LOVE9) — Testnet C1 Incentivized Node

> **Status:** Aktif Berjalan (Otomasi VPS)  
> **Website Hub:** [9chain.com](https://www.9chain.com/)  
> **Official Docs:** [docs.9chain.org](https://docs.9chain.org/en)  
> **Explorer:** [9scan.org](https://9scan.org)

---

## 📌 Informasi Akun & Sesi
* **Email:** `dionavrel09@gmail.com`
* **Username:** `avrell`
* **User ID:** `621ec357-7c7c-4cb1-b802-7372c5e398ba`
* **Referral Target:** `https://www.9chain.com/ref/396150076`
* **Situs Komunitas:** `https://www.9chain.com/virtual-node`

---

## ⚡ Status Node & Spesifikasi Hardware (Terkini)
* **Node Tier:** **Tier 1 - Iron Small (Seed Node)**
* **Mining Rate:** **`195 Poin / Jam`** (⚡ Meningkat dari bawaan awal 150/jam)
* **Nilai Poin Per Tap:** **`1.95 Poin / Tap`**
* **Push Harian:** **1.000 / 1.000 (MAX Selesai)**
* **Offline Cap:** 24 Jam

### Riwayat Upgrade Hardware:
1. **CPU:** Level 1 (Biaya: 480 Poin) $\rightarrow$ *Power Gain: +20 Rate*
2. **RAM:** Level 1 (Biaya: 600 Poin) $\rightarrow$ *Power Gain: +25 Rate*

---

## 📈 Strategi Tabungan vs Upgrade
* **Total Poin Dihasilkan (`xpEarnedTotal`):** **`1.546,24` Poin** *(Poin kumulatif resmi untuk airdrop, tidak berkurang).*
* **Saldo Belanja (`xpTotal`):** `466,24` Poin.
* **Target Tier 2:** Butuh `3.200` Poin (Mining Rate akan melonjak ke `247.5/jam`).
* **Kebijakan:** Setelah mencapai Tier 2, seluruh poin ditahan/disimpan untuk persiapan WD & konversi token $LOVE9 saat mainnet launch.

---

## 🤖 Skrip Otomasi VPS
* **Lokasi Script:** `/home/ubuntu/9chain_autotap.py`
* **Fungsi:** 
  1. Auto-Check state & sisa kuota tap.
  2. Batch auto-tap hingga kuota 1.000 habis per hari.
  3. Auto-Upgrade hardware dan node tier saat saldo belanja mencukupi.

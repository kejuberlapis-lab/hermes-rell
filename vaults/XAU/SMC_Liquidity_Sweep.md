# 🎯 SMC: Liquidity Sweep & Manipulasi Market Maker

> **Vault:** `XAU` | **Topik:** Smart Money Concept | **Terkait:** [[SMC_BOS_dan_CHoCH]], [[Setup_Sniper_Liquidity_Sweep]]

---

## 1. Konsep Likuiditas Pasar
Institusi besar memerlukan likuiditas masif (kumpulan order Stop Loss retail trader) untuk dapat mengeksekusi order jutaan lot tanpa menggeser harga terlalu jauh dari target mereka:

- **Equal Highs (EQH) / Double Top:** Kumpulan Stop Loss para seller (Buy Stop Liquidity).
- **Equal Lows (EQL) / Double Bottom:** Kumpulan Stop Loss para buyer (Sell Stop Liquidity).

---

## 2. Mekanisme Liquidity Sweep (Fakeout)

1. **Pembentukan Umpan (Inducement):** Market membuat level Support atau Resistance yang terlihat sangat "rapi" untuk memancing retail trader masuk.
2. **Sapuan Likuiditas (The Sweep):** Harga bergerak menembus level tersebut dengan cepat untuk memicu Stop Loss retail dan mengumpulkan likuiditas.
3. **Pembalikan Agresif (Expansion):** Setelah Stop Loss tersapu, institusi langsung mendorong harga ke arah yang berlawanan dan meninggalkan *Imbalance*.

---

## 3. Cara Memanfaatkan Liquidity Sweep untuk Entri
- **Jangan buru-buru entri:** Jangan pasang order buy tepat di support sebelum terjadi sweep.
- **Tunggu konfirmasi pembalikan:** Tunggu ekor candle menyapu level low/high, lalu cari candle rejection atau *imbalance reversal* sebelum melakukan entri mengikuti arah momentum institusi.

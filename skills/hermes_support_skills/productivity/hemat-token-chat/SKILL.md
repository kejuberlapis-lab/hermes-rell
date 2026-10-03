---
name: hemat-token-chat
description: Strategi hemat token untuk chat harian (terutama di Telegram) dengan jawaban ringkas, minim tool mahal, dan klarifikasi cepat.
version: 1.0.0
author: Hermes Agent
---

# Hemat Token Chat

Gunakan skill ini saat pengguna ingin menghemat token/biaya.

## Prinsip
1. Jawaban ringkas dan langsung ke poin (default 3-6 bullet singkat).
2. Hindari penjelasan panjang kecuali diminta.
3. Gunakan klarifikasi 1 pertanyaan jika konteks kurang, jangan tebak panjang.
4. Prioritaskan ringkasan sebelum detail.
5. Saat ada output panjang, berikan versi singkat dulu lalu tawarkan detail opsional.

## Strategi Tool
1. Hindari tool dengan output besar jika tidak perlu.
2. Saat butuh web, ambil inti temuan, bukan dump panjang.
3. Batasi iterasi tool ke kebutuhan minimum untuk menjawab.

## Format Balasan Hemat
- Ringkasan 1 kalimat
- 3-5 poin tindakan
- 1 pertanyaan lanjutan (opsional)

## Contoh Trigger
- "hemat token"
- "jawab singkat"
- "budget token"
- "ringkas aja"

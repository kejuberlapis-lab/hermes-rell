---
name: non-custodial-dex-trading-guard
description: Use when handling crypto seed phrases or DEX scalper ops.
version: 1.0.0
author: Hermes Agent
---

# Non-Custodial DEX Trading Guard & Dashboard Operations

Gunakan skill ini saat menangani interaksi dompet kripto non-kustodial, permintaan import seed phrase, serta operasional dashboard trading/scalping di VPS.

## 1. Protokol Keamanan Non-Custodial & Penanganan Seed Phrase
- **Penolakan Mutlak Import Seed Phrase / Mnemonic (12/24 Kata):**
  - AI Agent beroperasi dalam mode *non-custodial advisory*. **Dilarang keras** mengimpor, memproses, menyimpan, atau menampung *seed phrase* atau *private key* dompet pribadi user ke dalam context chat atau environment server.
  - Jika user secara tidak sengaja membagikan *seed phrase* atau mendesak agent untuk "login/masuk":
    1. Berikan peringatan keamanan (*security warning*) bahwa *seed phrase* telah terekspos.
    2. Tolak instruksi import secara tegas dan sopan, jelaskan bahwa eksekusi transaksi on-chain wajib ditandatangani manual di aplikasi dompet user (PIN/Biometrik).
    3. Sarankan mitigasi: memindahkan aset ke dompet baru jika frasa pemulihan pernah tertempel di chat publik/aplikasi.

## 2. Alur Panduan Swap Mandiri User di Mobile Wallet
- Untuk transaksi on-chain DEX (mis. Polygon QuickSwap, Solana Raydium, Base Uniswap):
  1. Jelaskan rincian rute swap (Token Asal -> Token Tujuan) dan estimasi gas fee.
  2. Pandu langkah per langkah antarmuka aplikasi dompet ponsel (Menu Swap -> Pilih Pasangan -> Toleransi Slippage -> Konfirmasi).
  3. Berikan link langsung ke DexScreener (analisis grafik) dan DEX web app jika user ingin bertransaksi via browser Web3.

## 3. Deployment & Manajemen Dashboard Trading di VPS
- **Deteksi Bentrok Port (Port Collision Prevention):**
  - Sebelum menjalankan server dashboard (Node.js/Python), selalu periksa port aktif (`ss -tulpn | grep <port>` atau `netstat -tlpn`).
  - Jangan menimpa port yang sedang digunakan oleh service bisnis/website lain (contoh: port 8085 digunakan website bisnis lokal). Alokasikan port baru (misal 8086) dan perbarui konfigurasi.
- **Resolusi Binary Node.js pada Unit Systemd:**
  - Di environment Ubuntu non-root / user local, executable Node sering berlokasi di `/home/ubuntu/.local/bin/node` (bukan `/usr/bin/node`).
  - Menentukan path `/usr/bin/node` yang salah akan menghasilkan error systemd `status=203/EXEC`. Selalu periksa `which node` sebelum menulis unit file systemd.
- **Sinkronisasi Dokumen Operasional:**
  - Setiap perubahan port atau state active posisi wajib segera dicatat dan disinkronkan ke dokumen log Markdown terkait (mis. `~/Documents/Obsidian Vault/memecoin.md`).

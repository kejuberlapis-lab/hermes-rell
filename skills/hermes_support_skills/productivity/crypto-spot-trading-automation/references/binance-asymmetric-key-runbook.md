# Binance Asymmetric Key Runbook (Spot Bot)

## Tujuan
Menyiapkan API Binance berbasis RSA/asymmetric key dengan aman untuk bot spot.

## Langkah ringkas
1. Generate key pair di host bot.
2. Upload public key ke Binance API Management.
3. Simpan private key di host (`chmod 600`).
4. Set env:
   - `BINANCE_API_KEY`
   - `BINANCE_PRIVATE_KEY_PATH`
5. Uji signed read-only endpoint `/api/v3/account`.

## Verifikasi minimum
- HTTP 200 pada signed request.
- Response memiliki `canTrade` dan `accountType`.
- Tidak menampilkan saldo/detail sensitif ke chat jika tidak diminta.

## Troubleshooting durable
- Jika signed test gagal setelah regenerate key pair, cek mismatch key pair:
  - public key yang terdaftar di Binance harus pasangan private key di host.
- Jika user menolak replace public key, gunakan private key pasangan lama (jangan generate ulang lagi).

## Guardrail
- Withdraw permission harus OFF.
- Jangan kirim private key/API key di chat/log.
- Live trading hanya setelah paper test lolos.
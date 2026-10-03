# 03 - Spesifikasi Integrasi API BuatQris (Open API Resmi)

Dokumentasi teknis integrasi API **BuatQris** (`https://api.buatqris.site`) sebagai payment gateway QRIS dinamis untuk AI Tech Worker.

---

## 1. Parameter Utama & Endpoint Standar

- **Base URL:** `https://api.buatqris.site`
- **Method:** `POST`
- **Content-Type:** `application/x-www-form-urlencoded`
- **Respons Format:** `application/json` (UTF-8)
- **Mekanisme Endpoint:** Seluruh aksi memanggil SATU URL yang sama, dibedakan lewat parameter `action`.

### Kredensial Wajib (Environment Variables)
- `BUATQRIS_ACCOUNT_ID` : ID akun merchant BuatQris
- `BUATQRIS_SECRET_TOKEN` : Kunci rahasia API (diawali `sk_live_`)
- `BUATQRIS_SIGNING_SECRET` : Kunci rahasia verifikasi webhook signature

---

## 2. Pembuatan QRIS Dinamis (`action=api_create_qris`)

### Parameter Request (Form-Urlencoded)
| Parameter | Tipe | Status | Keterangan |
| :--- | :--- | :--- | :--- |
| `action` | string | Wajib | Nilai tetap: `api_create_qris` |
| `account_id` | string | Wajib | ID Akun Merchant |
| `secret_token` | string | Wajib | Kunci rahasia API |
| `amount` | integer | Wajib | Nominal tagihan (Min: Rp 1.000, Max: Rp 5.000.000) |
| `description` | string | Opsional | Keterangan order (Maksimal 100 karakter) |
| `fee_by` | string | Opsional | `user` (potong saldo kita) atau `buyer` (bebankan ke pembeli) |
| `qris_method` | string | Opsional | `qris_one` | `qris_two` | `qris_three` | `qris_four` |
| `callback_url` | string | Opsional | URL Webhook kustom (default memakai setting dashboard) |
| `test` | string/int | Opsional | `1` atau `true` untuk mode SANDBOX (uji coba tanpa uang asli) |

### Contoh Respons Sukses
```json
{
  "success": true,
  "data": {
    "transaction_id": "100043729581",
    "amount": 100000,
    "total_amount": 100037,
    "amount_uniq": 37,
    "admin_fee": 500,
    "credit_amount": 99500,
    "fee_by": "user",
    "qris_method": "qris_two",
    "description": "Paket Starter AI Tech Worker",
    "qr_url": "https://app.buatqris.site/poto/qris/100043729581.png",
    "qris_image": "data:image/png;base64,iVBORw0KG...",
    "expired_at": "2026-10-02T23:59:00+07:00",
    "status": "pending",
    "payment_url": "https://app.buatqris.site/trx/100043729581"
  }
}
```
*Catatan Penting:* Untuk menampilkan QR ke user Telegram, gunakan `qr_url` (unduh/kirim langsung sebagai photo) atau `qris_image` (base64 PNG). Field `qris_string`, `qris_url`, dan `direct_url` selalu bernilai `null` dari sisi API provider.

---

## 3. Webhook / Callback Handler

Setiap status transaksi berubah (`payment.success`, `payment.expired`, `payment.failed`), BuatQris mengirim HTTP POST ke Webhook URL VPS.

### Header Webhook
- `Content-Type`: `application/json`
- `X-BuatQris-Event`: `payment.success`
- `X-BuatQris-Delivery`: `100043729581` (transaction_id)
- `X-BuatQris-Signature`: `sha256=<hex_hmac_signature>`

### Payload Body Webhook
```json
{
  "event": "payment.success",
  "transaction_id": "100043729581",
  "status": "success",
  "amount": 100000,
  "total_amount": 100037,
  "credit_amount": 99500,
  "admin_fee": 500,
  "fee_by": "user",
  "qris_method": "qris_two",
  "is_test": false,
  "paid_at": "2026-10-02T23:55:12+07:00"
}
```

### Verifikasi Signature (Python)
```python
import hmac
import hashlib

def verify_buatqris_signature(raw_body: bytes, header_signature: str, signing_secret: str) -> bool:
    calc = "sha256=" + hmac.new(
        signing_secret.encode('utf-8'),
        raw_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(calc, header_signature or "")
```

---

## 4. Rule & Batasan Penting (Rate Limit & Timeout)
1. **Rate Limit Buat QRIS:** Maksimal 60 pembuatan transaksi per menit per akun.
2. **Rate Limit Cek Status:** Maksimal 1 kali per 20 detik per (akun + transaksi). Hindari polling berkala, utamakan webhook!
3. **Pencocokan Nominal:** Wajib mencocokkan `total_amount` (sudah termasuk kode unik), bukan `amount` mentah.
4. **Respon Webhook Cepat:** Server wajib membalas HTTP 200 dalam waktu < 6 detik agar sistem BuatQris tidak melakukan retry.
5. **Mode Sandbox:** Selalu uji flow registrasi dan upgrade paket menggunakan parameter `test=1` sebelum peluncuran produksi.

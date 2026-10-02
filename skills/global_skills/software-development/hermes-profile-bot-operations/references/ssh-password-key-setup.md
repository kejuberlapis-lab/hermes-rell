# SSH Password-to-Key Setup — Pitfalls & Workflow

Gunakan saat sir memberi password SSH dan menyuruh menyimpannya agar tidak berulang. Tujuan: setup SSH key-based auth sekali, lalu akses tanpa password selamanya.

## Workflow lengkap

### 1. Simpan credential ke memory (jika sir minta)
Sir berkata "simpan ini semua jangan berulang saya kasi infonya" → simpan IP, user, dan catatan bahwa password tersedia untuk key setup. Jangan simpan password mentah ke memory.

### 2. Generate SSH key (jika belum ada)
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
```

### 3. Copy public key ke VPS (otomatis dengan password)

**JANGAN** gunakan `sshpass` jika tidak terinstall dan tidak bisa sudo.

**Metode via Python subprocess + SSH_ASKPASS:**

```python
import subprocess, os

# Buat askpass script — HATI-HATI dengan special chars di password
askpass_path = os.path.expanduser('~/.ssh/askpass.sh')
# Password: thunder-27$-shadow
#   ^^ $- DI BASH ADALAH VARIABLE SPESIAL (shell flags)
#   GUNAKAN SINGLE QUOTES agar literal
with open(askpass_path, 'w') as f:
    f.write('#!/bin/bash\n')
    f.write("echo 'thunder-27$-shadow'\n")  # SINGLE quotes!
os.chmod(askpass_path, 0o700)

env = os.environ.copy()
env['DISPLAY'] = 'none'
env['SSH_ASKPASS'] = askpass_path
env['SSH_ASKPASS_REQUIRE'] = 'force'

result = subprocess.run(
    ['ssh-copy-id', '-o', 'StrictHostKeyChecking=accept-new',
     'ubuntu@43.134.233.101'],
    capture_output=True, text=True, timeout=20, env=env,
    start_new_session=True  # WAJIB: tanpa ini SSH deteksi TTY dan ignore ASKPASS
)
```

### 4. Verifikasi key-based access
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 ubuntu@<IP> "echo SSH_KEY_OK"
```

### 5. Bersihkan askpass script
```bash
rm ~/.ssh/askpass.sh
```

## Pitfall: Bash variable expansion di password

**Masalah:** Password `thunder-27$-shadow` mengandung `$-`.

Di bash, `$-` adalah **special variable** yang menampilkan shell option flags (misal `hB`).

| Quote style | Hasil output | Penyebab |
|-------------|-------------|----------|
| `echo "thunder-27$-shadow"` | `thunder-27hBshadow` | Double quotes → `$-` di-expand |
| `echo 'thunder-27$-shadow'` | `thunder-27$-shadow` | ✅ Single quotes → literal |

**Deteksi:** Jalankan `bash askpass.sh` dan cek output. Jika berbeda dari password asli, fix quoting.

**Cara fix:**
- Gunakan single quotes di script heredoc: `cat > script << 'EOF'` (EOF pakai quotes)
- Atau escape `$` dengan backslash: `echo "thunder-27\$-shadow"`

## Pitfall: SSH_ASKPASS diabaikan

SSH hanya menggunakan SSH_ASKPASS jika **tidak ada TTY yang terdeteksi**. Di environment non-interaktif (subprocess Python tanpa `start_new_session=True`), SSH kadang masih mendeteksi TTY dari parent process.

**Solusi:**
1. Set `SSH_ASKPASS_REQUIRE=force` — memaksa SSH pakai askpass.
2. Panggil subprocess dengan `start_new_session=True` — memutus chain TTY.
3. Jangan gunakan `subprocess.run` dengan `shell=True` (shell menambah TTY).

**Jika tetap gagal** setelah kedua langkah di atas, kemungkinan SSH di server menolak password auth. Cek server SSH config.

## Kapan SSH VPS tidak bisa diakses

| Skenario | Diagnosis | Action |
|----------|-----------|--------|
| VPS ping OK, port 22 REFUSED, port 80 OPEN | **SSH daemon (sshd) mati** — tidak auto-start setelah reboot | Minta sir masuk via cloud console VNC, jalankan `sudo systemctl enable ssh --now` |
| VPS ping OK, port 22 REFUSED, port 80+443 REFUSED | **Firewall block** — security group atau iptables | Cek cloud console security group inbound rules |
| VPS ping TIMEOUT, semua port TIMEOUT | **VPS mati** — belum boot atau crash | Restart via cloud console, tunggu 1-2 menit |
| Port 22 TIMEOUT (bukan REFUSED) | **Firewall TCP block** — ICMP allowed tapi TCP diblok | Cek security group |

**Key observation:** Port 22 `REFUSED` vs `TIMEOUT` beda arti:
- `REFUSED` = server reachable, port listening, tapi langsung ditolak (daemon mati / reject)
- `TIMEOUT` = server reachable, port tidak direspon (firewall block / host down)

**Catatan:** `Connection refused` kadang muncul di awal setelah reboot (belum sempat SSH daemon start). Tunggu 1-2 menit dan retry.

## Urutan prioritas akses VPS

1. **Coba SSH via BatchMode (key)** — `ssh -o BatchMode=yes`
2. Jika gagal karena key belum ada → **setup key dengan password** (gunakan metode SSH_ASKPASS di atas)
3. Jika port 22 refused/timed out → **diagnosis dulu** (ping + port scan), jangan langsung minta restart VPS
4. Jika SSH daemon mati → **minta sir via cloud console VNC**; tidak bisa diakali dari luar
5. Jika semua gagal → **minta sir akses ke Tencent/AWS/GCP console**

## Guardrail

- Jangan simpan password ke memory/log.
- Jangan tampilkan password dalam output terminal.
- Setelah key terpasang, hapus askpass script (`rm ~/.ssh/askpass.sh`).
- Jika sir memberi izin eksplisit untuk "simpan ini" — simpan hanya host/user ke memory, password tetap tidak disimpan mentah.

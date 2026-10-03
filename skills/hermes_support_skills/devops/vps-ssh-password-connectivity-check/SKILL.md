---
name: vps-ssh-password-connectivity-check
description: Verifikasi akses SSH ke VPS saat hanya punya IP/user/password, termasuk fallback jika sshpass tidak tersedia atau tidak bisa install package karena tanpa sudo.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ssh, vps, troubleshooting, pexpect, connectivity, password-auth]
---

# VPS SSH Password Connectivity Check (No sshpass fallback)

Gunakan skill ini saat user memberi kredensial VPS (IP, user, password) dan meminta cek apakah server bisa diakses, terutama ketika environment lokal tidak punya `sshpass` atau tidak punya akses sudo untuk instal paket sistem.

## Kapan dipakai
- User minta "cek VPS", "cek login SSH", "cek IP/user/password valid atau tidak".
- Login berbasis password (bukan key) dan perlu verifikasi cepat.
- `sshpass` tidak tersedia / gagal diinstal.

## Langkah
1. Cek port SSH dulu (default 22 atau custom port seperti Hostinger `65002`):
   - Gunakan Python socket untuk memastikan host:port reachable.
2. Coba metode cepat dengan `sshpass` jika tersedia.
3. Jika `sshpass` tidak ada dan tidak bisa `apt install` (mis. sudo butuh password), fallback ke `pexpect`.
4. Buat virtualenv sementara agar tidak bentrok PEP 668:
   - `python3 -m venv /tmp/<venv>`
   - `.../bin/pip install pexpect`
5. Jalankan `ssh` via `pexpect`, tangani prompt:
   - `yes/no` untuk host key
   - `password:` untuk autentikasi
6. Jalankan command verifikasi minimal:
   - `echo CONNECTED && hostname && whoami`
7. Jika user tanya OS / direktori domain hosting:
   - `cat /etc/os-release; uname -sr` atau `ls -la domains/`

## Template command (ringkas & custom port)
```bash
python3 -m venv /tmp/hermes-sshcheck-venv
/tmp/hermes-sshcheck-venv/bin/pip install -q pexpect
/tmp/hermes-sshcheck-venv/bin/python - <<'PY'
import pexpect
host='X.X.X.X'; port=65002; user='u123456'; pw='your_password'
cmd=f"ssh -p {port} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {user}@{host} 'echo CONNECTED && whoami && pwd'"
child=pexpect.spawn(cmd, encoding='utf-8', timeout=25)
i=child.expect([r'(?i)password:', r'yes/no', pexpect.EOF, pexpect.TIMEOUT])
if i==1:
    child.sendline('yes'); child.expect(r'(?i)password:'); child.sendline(pw)
elif i==0:
    child.sendline(pw)
else:
    raise SystemExit('SSH prompt gagal')
child.expect(pexpect.EOF)
print((child.before or '').strip())
PY
```

## Pitfalls
- `python3 -m pip install --user ...` bisa gagal di distro dengan PEP 668 (externally-managed-environment). Solusi: pakai virtualenv sementara.
- Jangan mengklaim "online" hanya dari ping; validasi dengan login SSH sukses.
- `child.exitstatus` bisa `None` saat EOF; gunakan output command sebagai indikator keberhasilan.

## Verifikasi hasil
Minimal laporkan:
- Port 22 reachable/tidak
- Login SSH sukses/tidak
- `hostname`
- `whoami`
- (opsional) distro + kernel (`/etc/os-release`, `uname -sr`)

## Catatan keamanan
- Perlakukan password sebagai data sensitif.
- Setelah berhasil login, sarankan user rotasi password jika sudah dibagikan di chat.

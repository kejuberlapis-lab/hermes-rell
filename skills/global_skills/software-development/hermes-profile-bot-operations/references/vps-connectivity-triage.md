# VPS Connectivity Triage — SSH Down or VPS Dead?

Gunakan saat perlu SSH ke VPS tapi gagal — bedakan apakah VPS mati total, SSH service down, atau kendala network/firewall.

## Diagnostic command

```bash
# 1. Ping — VPS hidup?
ping -c 2 -W 3 <PUBLIC_IP>

# 2. Cek port-port kunci
timeout 5 bash -c '</dev/tcp/<PUBLIC_IP>/22' 2>&1 && echo OPEN || echo CLOSED
timeout 5 bash -c '</dev/tcp/<PUBLIC_IP>/80' 2>&1 && echo OPEN || echo CLOSED
timeout 5 bash -c '</dev/tcp/<PUBLIC_IP>/443' 2>&1 && echo OPEN || echo CLOSED

# Alternatif: nc
nc -zv -w 5 <PUBLIC_IP> 22 2>&1
nc -zv -w 5 <PUBLIC_IP> 80 2>&1
nc -zv -w 5 <PUBLIC_IP> 443 2>&1
```

## Matrix diagnosis

| Ping | Port 22 | Port 80 | Port 443 | Diagnosis |
|------|---------|---------|----------|-----------|
| ✅ OK | ✅ OPEN | ✅ OPEN | ✅ OPEN | VPS normal, SSH bisa |
| ✅ OK | ❌ REFUSED | ✅ OPEN | ❌ REFUSED | **SSH service (sshd) down** — restart via console/VNC |
| ✅ OK | ❌ REFUSED | ❌ REFUSED | ❌ REFUSED | **Firewall block** — periksa security group / iptables |
| ❌ TIMEOUT | ❌ TIMEOUT | ❌ TIMEOUT | ❌ TIMEOUT | **VPS mati / network down** — restart via cloud console |
| ✅ OK | ❌ TIMEOUT | ❌ TIMEOUT | ❌ TIMEOUT | **Port firewall** (ICMP allowed tapi TCP diblok) |

**Key observation: REFUSED vs TIMEOUT**
- **REFUSED** = server reachable, port terbuka tapi koneksi langsung ditolak → service daemon mati, belum start, atau reject policy.
- **TIMEOUT** = server reachable, port tidak merespon sama sekali → firewall block (security group, iptables) atau host tidak mendengarkan di port itu.
- Di awal setelah reboot VPS, port 22 bisa menunjukkan REFUSED beberapa detik sebelum daemon sshd start. Jika masih REFUSED setelah 1-2 menit, berarti sshd memang tidak auto-start.

## SSH service down (port 22 REFUSED) — fix via cloud console

Jika VPS pingable, port 22 refused, port 80/443 mungkin open:

1. Login ke **cloud provider console** (Tencent/AWS/GCP).
2. Cari **VNC / remote console** untuk VPS tersebut.
3. Login via VNC, lalu:
   ```bash
   sudo systemctl status ssh         # cek status (nama unit: ssh atau sshd)
   sudo systemctl enable ssh --now   # enable auto-start + start sekarang
   ```
   Catatan: nama unit bisa `ssh` (Ubuntu) atau `sshd` (beberapa distro). `enable --now` melakukan start + enable dalam satu perintah.
4. Cek apakah SSH sudah start:
   ```bash
   systemctl status ssh
   ss -tlnp | grep 22
   ```
5. Atau restart VPS dari console → SSH akan start ulang hanya jika sudah di-enable.

## Jika VPS restart gagal

- Cek cloud console → monitoring → pastikan status "Running".
- Cek security group / firewall rules → pastikan port 22 allowed dari IP saat ini.
- Cek apakah ada maintenance window atau billing issue.

## Setelah SSH pulih

Segera setup SSH key agar tidak bergantung password:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
ssh-copy-id ubuntu@<PUBLIC_IP>
ssh -o BatchMode=yes ubuntu@<PUBLIC_IP> "echo SSH_KEY_OK"
```

Jika password mengandung special character (`$`, `\`, `"`), lihat `references/ssh-password-key-setup.md` untuk metode setup yang benar.

**Workflow saat sir memberi credential VPS:**
1. Simpan IP/hostname/user ke memory.
2. Setup SSH key segera — jangan tunda, karena sir tidak ingin mengulang info credential.
3. Verifikasi key-based access.
4. Hapus askpass script dan jangan simpan password mentah di mana pun.

## Pitfall

- Jangan asumsikan "SSH failed = VPS mati". Ping + port scan dulu.
- Untuk VPS Tencent, security group di console (port 22 inbound) independen dari iptables di dalam VM.
- Jika VPS direstart via console, tunggu 1-2 menit sebelum SSH bisa diakses kembali.
- Jangan simpan password SSH ke memory/log setelah dipakai — perlakukan sebagai `[REDACTED]`.

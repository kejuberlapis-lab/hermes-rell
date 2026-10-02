# 2026-06-29: VPS RAM Crash Recovery Session

## Timeline

1. **00:47 WIB** — VPS reboot (via Tencent Cloud Console) setelah RAM penuh
2. **00:48** — SSH pulih, cleanup (drop_caches + swapoff/swapon)
3. **00:50** — Update Hermes v0.14.0 → v0.17.0 (git conflict resolve + pip install)
4. **00:51** — Restart hermes-support gateway
5. **01:05-01:10** — Migrate avrel-jago dan ais dari root → user service
6. **01:14** — Migrate hermes-support dari user → root service
7. **01:15** — Restart 6 profile user services → memory spike → SSH timeout lagi
8. **01:30** — Restart VPS dari console
9. **01:34** — SSH pulih, hapus Docker + n8n untuk free RAM

## Key Decisions

- **Policy:** Hanya hermes-support yang jalan sebagai root (system service). Semua profile lain sebagai ubuntu (user service).
- **Docker/n8n dihapus** — container n8n consume RAM, sir minta hapus total
- **Memory limit** hermes-support dinaikkan ke 100,000 chars (dari default 2,200)

## Root Causes of Repeated SSH Timeout

1. RAM 1.9GB tidak cukup untuk 8 Hermes gateway + MySQL 361MB + Docker/n8n + Tailscale
2. Batch restart 6 profile menyebabkan memory spike dan sshd tidak bisa fork
3. `swapoff -a` gagal karena RAM tidak cukup untuk menampung 1.3GB swap

## Commands Used

```bash
# SSH diagnosis chain
ping -c 2 <VPS_IP>
nc -zv -w5 <VPS_IP> 22
ssh -vvv -o ConnectTimeout=10 ubuntu@<VPS_IP> "echo OK"

# RAM recovery after reboot
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo swapoff -a && sudo swapon -a
free -h

# Docker removal
docker stop n8n && docker rm n8n
docker volume rm n8n_data
docker system prune -af --volumes
sudo systemctl stop docker docker.socket containerd
sudo apt remove --purge -y docker-ce docker-ce-cli containerd.io
sudo apt autoremove --purge -y
sudo rm -rf /var/lib/docker /etc/docker

# Profile migration root→user
sudo systemctl disable hermes-gateway-<profile>.service
sudo rm -f /etc/systemd/system/hermes-gateway-<profile>.service
sudo systemctl daemon-reload
sudo pkill -f "profile <profile>"
sudo chown -R ubuntu:ubuntu ~/.hermes/profiles/<profile>/
rm -f ~/.hermes/profiles/<profile>/gateway.lock
sed 's/<src>/<dst>/g' ~/.config/systemd/user/hermes-gateway-<src>.service > ~/.config/systemd/user/hermes-gateway-<dst>.service
systemctl --user daemon-reload
systemctl --user enable hermes-gateway-<dst>.service
systemctl --user start hermes-gateway-<dst>.service

# Profile migration user→root (hermes-support only)
systemctl --user stop hermes-gateway-hermes-support.service
systemctl --user disable hermes-gateway-hermes-support.service
# Create system service file (see skill procedures)
sudo systemctl daemon-reload
sudo systemctl enable hermes-gateway-hermes-support.service
sudo systemctl start hermes-gateway-hermes-support.service
```

## Metrics Before/After Docker Removal

| Metric | Before | After |
|--------|--------|-------|
| RAM available | 202MB | 588MB |
| RAM used | 1.7Gi | 1.3Gi |
| Docker/n8n | running | removed |

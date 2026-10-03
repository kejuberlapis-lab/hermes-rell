# Session Example: VPS-Zeus SSH Timeout (29 Jun 2026)

## Initial Report

User: "kenapa profil hermes support tidak respon coba cek apa yang terjadi di VPS-ZEUS"
User: "ram penuh seperti nya"

## Diagnosis Performed

### Step 1 — Ping (✅)
```
PING 43.134.233.101 56(84) bytes of data
64 bytes from 43.134.233.101: icmp_seq=1 ttl=53 time=13.5 ms
2 packets transmitted, 2 received, 0% loss
```
VPS alive, network OK.

### Step 2 — Port 22 check (✅)
```
nc -zv -w5 43.134.233.101 22
→ Connection to 43.134.233.101 22 port [tcp/ssh] succeeded!
```
Port open, TCP handshake works.

### Step 3 — Verbose SSH diagnosis (❌)
```
ssh -vvv -o ConnectTimeout=10 ubuntu@43.134.233.101 "echo OK"
...
debug1: Connection established.
debug1: Local version string SSH-2.0-OpenSSH_10.2p1 Ubuntu-2ubuntu3.2
Connection timed out during banner exchange
```
TCP connect OK, client sent version, server never replied → sshd can't fork.

### Step 4 — Cross-check via HTTP (✅ Port 80 responds)
```
curl -s -o /dev/null -w "%{http_code}" http://43.134.233.101:80/
→ 200
```
nginx running → OS alive, only sshd broken.

### Conclusion
RAM exhaustion → sshd cannot fork → SSH connection accepted at TCP level but banner never sent. Need Tencent Cloud Console VNC to drop caches and restart sshd.

## Key Commands Used

```bash
# Diagnosis chain
ping -c 2 -W 5 43.134.233.101
nc -zv -w5 43.134.233.101 22
ssh -vvv -o ConnectTimeout=10 -o StrictHostKeyChecking=no ubuntu@43.134.233.101 "echo OK" 2>&1 | tail -30
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://43.134.233.101:80/

# Recovery (via console VNC)
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo systemctl restart sshd
free -h
```

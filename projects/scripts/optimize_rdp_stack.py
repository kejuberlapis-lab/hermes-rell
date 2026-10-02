import re
import os
import subprocess

print("=== 1. OPTIMIZING /etc/xrdp/xrdp.ini ===")
xrdp_ini_path = '/etc/xrdp/xrdp.ini'
if os.path.exists(xrdp_ini_path):
    with open(xrdp_ini_path, 'r') as f:
        content = f.read()

    # Settings to enforce
    settings = {
        'max_bpp': '24',
        'crypt_level': 'low',
        'tcp_nodelay': 'true',
        'tcp_keepalive': 'true',
        'tcp_send_buffer_bytes': '4194304',
        'tcp_recv_buffer_bytes': '4194304',
        'use_compression': 'yes',
    }

    for k, v in settings.items():
        pattern = rf'^[;#\s]*{k}\s*=.*$'
        if re.search(pattern, content, flags=re.MULTILINE):
            content = re.sub(pattern, f'{k}={v}', content, flags=re.MULTILINE)
        else:
            # append under [Globals]
            content = content.replace('[Globals]', f'[Globals]\n{k}={v}')

    with open('/tmp/xrdp.ini.optimized', 'w') as f:
        f.write(content)
    
    os.system('sudo cp /tmp/xrdp.ini.optimized /etc/xrdp/xrdp.ini')
    print("xrdp.ini updated successfully")

print("\n=== 2. OPTIMIZING /etc/xrdp/sesman.ini ===")
sesman_path = '/etc/xrdp/sesman.ini'
if os.path.exists(sesman_path):
    with open(sesman_path, 'r') as f:
        ses_content = f.read()
    
    # Ensure X11 display settings are optimal
    if 'MaxSessions' in ses_content:
        ses_content = re.sub(r'^[;#\s]*MaxSessions\s*=.*$', 'MaxSessions=10', ses_content, flags=re.MULTILINE)
    
    with open('/tmp/sesman.ini.optimized', 'w') as f:
        f.write(ses_content)
    os.system('sudo cp /tmp/sesman.ini.optimized /etc/xrdp/sesman.ini')
    print("sesman.ini updated")

print("\n=== 3. CONFIGURING LINUX KERNEL SYSCTL ===")
sysctl_opts = """
# RDP Network & Latency Optimization
net.core.default_qdisc=fq
net.ipv4.tcp_congestion_control=bbr
net.core.rmem_max=16777216
net.core.wmem_max=16777216
net.ipv4.tcp_rmem=4096 87380 16777216
net.ipv4.tcp_wmem=4096 65536 16777216
net.ipv4.tcp_notsent_lowat=16384
net.ipv4.tcp_slow_start_after_idle=0
net.ipv4.tcp_fastopen=3
net.ipv4.tcp_window_scaling=1
net.ipv4.tcp_timestamps=1
net.ipv4.tcp_sack=1

# Memory & I/O Latency
vm.swappiness=10
vm.vfs_cache_pressure=50
vm.dirty_ratio=15
vm.dirty_background_ratio=5
"""

with open('/tmp/99-rdp-performance.conf', 'w') as f:
    f.write(sysctl_opts.strip() + '\n')

os.system('sudo cp /tmp/99-rdp-performance.conf /etc/sysctl.d/99-rdp-performance.conf')
os.system('sudo sysctl -p /etc/sysctl.d/99-rdp-performance.conf')
print("Sysctl parameters loaded")

import urllib.request
import json
import ssl
import time

token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NmNkNjczMC1mYmMxLTQwMzAtOTkwMy0wZjVmYTZmYzdiNWYiLCJlbWFpbCI6ImRpb25hdnJlbDA5QGdtYWlsLmNvbSIsInVzZXJJZCI6IjYyMWVjMzU3LTdjN2MtNGNiYi1iODAyLTczNzJjNWUzOThiYSIsInJvbGVzIjpbIm1lbWJlciJdLCJwZXJtaXNzaW9ucyI6W10sInR2IjowLCJpYXQiOjE3OTA4MzEyNzksImV4cCI6MTc5MDgzMjE3OX0.DKsyr3ru6GufCy9Mre5oF2fze58ftGYf9Id8LCKGhh0'

headers = {
    'Authorization': token,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.9chain.com/virtual-node',
    'Origin': 'https://www.9chain.com'
}

ctx = ssl.create_default_context()

def get_state():
    url = 'https://api.9chain.com/v2/program/state'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data.get('data', {})

import urllib.request
import json
import ssl
import time

token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NmNkNjczMC1mYmMxLTQwMzAtOTkwMy0wZjVmYTZmYzdiNWYiLCJlbWFpbCI6ImRpb25hdnJlbDA5QGdtYWlsLmNvbSIsInVzZXJJZCI6IjYyMWVjMzU3LTdjN2MtNGNiYi1iODAyLTczNzJjNWUzOThiYSIsInJvbGVzIjpbIm1lbWJlciJdLCJwZXJtaXNzaW9ucyI6W10sInR2IjowLCJpYXQiOjE3OTA4MzEyNzksImV4cCI6MTc5MDgzMjE3OX0.DKsyr3ru6GufCy9Mre5oF2fze58ftGYf9Id8LCKGhh0'

headers = {
    'Authorization': token,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.9chain.com/virtual-node',
    'Origin': 'https://www.9chain.com'
}

ctx = ssl.create_default_context()

def get_state():
    url = 'https://api.9chain.com/v2/program/state'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
        return json.loads(resp.read().decode('utf-8')).get('data', {})

def get_catalog():
    url = 'https://api.9chain.com/v2/program/catalog'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
        return json.loads(resp.read().decode('utf-8')).get('data', {})

def auto_upgrade():
    state = get_state()
    catalog = get_catalog()
    current_xp = float(state.get('xpTotal', '0'))
    
    # Check Hardware Upgrades
    for comp in catalog.get('components', []):
        if comp.get('unlocked'):
            key = comp.get('componentKey')
            level = comp.get('level', 0)
            next_cost = float(comp.get('nextCost', '99999999'))
            
            if current_xp >= next_cost:
                print(f"[*] Upgrading {key.upper()} to Level {level+1} (Cost: {next_cost} Poin)...")
                payload = {'componentKey': key, 'toLevel': level + 1}
                req = urllib.request.Request('https://api.9chain.com/v2/program/upgrade', data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
                try:
                    with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
                        res = json.loads(resp.read().decode('utf-8'))
                        if res.get('success'):
                            print(f"[✓] Berhasil upgrade {key.upper()} ke Level {level+1}!")
                            current_xp -= next_cost
                except Exception as e:
                    print(f"[x] Gagal upgrade {key}: {e}")

    # Check Tier Upgrade
    next_tier = state.get('nextTier', {})
    if next_tier.get('affordable'):
        tier = next_tier.get('tier')
        print(f"[*] Upgrading Node to Tier {tier}...")
        req = urllib.request.Request('https://api.9chain.com/v2/program/node/upgrade', data=json.dumps({'toTier': tier}).encode('utf-8'), headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
                print(f"[✓] Berhasil upgrade Node ke Tier {tier}!")
        except Exception as e:
            print(f"[x] Gagal upgrade Tier: {e}")

def run_full_cycle():
    state = get_state()
    taps_remaining = state.get('tapsRemaining', 0)
    print(f"[*] State Awal: Rate {state.get('contributionRate')}/jam | Saldo: {state.get('xpTotal')} | Sisa Tap: {taps_remaining}")
    
    if taps_remaining > 0:
        batch_size = 50
        while taps_remaining > 0:
            count = min(batch_size, taps_remaining)
            payload = {'count': count}
            try:
                req = urllib.request.Request('https://api.9chain.com/v2/program/tap', data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
                with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
                    res = json.loads(resp.read().decode('utf-8'))
                    if res.get('success'):
                        taps_remaining = res.get('data', {}).get('state', {}).get('tapsRemaining', 0)
            except Exception:
                break
            time.sleep(1.0)
            
    auto_upgrade()
    final = get_state()
    print(f"[📊] State Akhir: Rate ⚡ {final.get('contributionRate')}/jam | Saldo: {final.get('xpTotal')} Poin | Upgrades: {final.get('upgrades')}")

if __name__ == '__main__':
    run_full_cycle()

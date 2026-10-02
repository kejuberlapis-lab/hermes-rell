import urllib.request
import json
import ssl
import time

init_data = 'user=%7B%22id%22%3A5955713269%2C%22first_name%22%3A%22avrell%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22theisavrell%22%2C%22language_code%22%3A%22en%22%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2F0gaEgrXWikm1qoz8_mL6BB__zEm0d_qFzqr30J876J2G3ZAnwAizNevQt1GNWZkg.svg%22%7D&chat_instance=-829524341756004651&chat_type=channel&start_param=ref_4636206d7f4e2447&auth_date=1790644418&signature=1grIE_YPvlcrHH-8NAe76mWv85pgxjGc7_vHCWW__djktZeT5IFHj3qa-zzXfAUnXuL1cWT7vI7Y04jPA6ImCg&hash=c8a072093bf63a4310ef4aeaffdabc985b6db1d0ecaf9f16e3b2e5271fcbf416'

url = 'https://julnowgcrkazepbfxkau.supabase.co/functions/v1/mima-secure-api'
ctx = ssl.create_default_context()

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-telegram-init-data': init_data,
    'Authorization': f'Bearer {init_data}'
}

def drain_energy():
    print("[*] Memulai Auto-Tap MIMA sampai energi habis...")
    total_taps = 0
    
    while True:
        payload = {
            'action': 'tap',
            'count': 10,
            'initData': init_data
        }
        
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                
                if data.get('success'):
                    accepted = data.get('accepted', 1)
                    total_taps += accepted
                    balance = data.get('balance')
                    energy = data.get('tap_energy', 0)
                    
                    if total_taps % 50 == 0 or energy <= 10:
                        print(f"[+] Total Taps: {total_taps} | Sisa Energy: {energy} | Saldo: {balance:.6f} MIMA")
                    
                    if energy <= 2:
                        print(f"\n[✓] Energy berhasil dihabiskan! Total Taps: {total_taps}, Saldo Akhir: {balance:.6f} MIMA")
                        break
                else:
                    print(f"[-] Respons server: {data}")
                    break
        except Exception as e:
            print(f"[x] Error koneksi: {e}")
            break
            
        time.sleep(1.0)

if __name__ == '__main__':
    drain_energy()

import urllib.request
import urllib.error
import json

base_url = 'https://hris.mitsindo.co.id'

# 1. Login with admin
login_data = json.dumps({'username': 'admin', 'password': 'admin123'}).encode()
req = urllib.request.Request(f'{base_url}/api/auth/login', data=login_data, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
token = json.loads(resp.read().decode())['token']

pages = ['/', '/dashboard', '/recruitment', '/settings', '/documents', '/register']

for p in pages:
    url = f'{base_url}{p}'
    headers = {
        'Cookie': f'token={token}',
        'Authorization': f'Bearer {token}'
    }
    req = urllib.request.Request(url, headers=headers)
    print(f"\n=================== URL: {p} ===================")
    try:
        resp = urllib.request.urlopen(req, timeout=8)
        print("Status:", resp.status)
        print(resp.read().decode()[:400])
    except urllib.error.HTTPError as e:
        print("HTTP ERROR:", e.code)
        body = e.read().decode()
        print("BODY:", body[:1000])
    except Exception as e:
        print("EXCEPTION:", e)

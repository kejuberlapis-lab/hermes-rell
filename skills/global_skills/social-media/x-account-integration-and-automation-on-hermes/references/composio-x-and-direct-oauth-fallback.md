# Composio X + Direct OAuth Fallback (Session Recipe)

## 1) Composio happy path
```bash
~/.composio/composio login --no-wait --no-skill-install
# user open login_url
~/.composio/composio login --key <CLI_KEY> --no-skill-install
~/.composio/composio whoami
~/.composio/composio link twitter --no-wait
# user authorize URL
~/.composio/composio link twitter --list
```

Sinyal sukses:
- `whoami` menampilkan account/org.
- `link twitter --list` mengembalikan `total > 0`.

## 2) Fallback direct OAuth1.0a (bila Composio mentok)
Simpan env profile (permission ketat):
```bash
cat > /home/ubuntu/.hermes/profiles/<profile>/.env.x_api <<'EOF'
X_CONSUMER_KEY=...
X_CONSUMER_SECRET=...
X_ACCESS_TOKEN=...
X_ACCESS_TOKEN_SECRET=...
EOF
chmod 600 /home/ubuntu/.hermes/profiles/<profile>/.env.x_api
```

Verifikasi API akun:
```python
import os
from requests_oauthlib import OAuth1Session
for line in open('/home/ubuntu/.hermes/profiles/<profile>/.env.x_api'):
    if '=' in line:
        k,v=line.strip().split('=',1); os.environ[k]=v
s=OAuth1Session(
    os.environ['X_CONSUMER_KEY'],
    client_secret=os.environ['X_CONSUMER_SECRET'],
    resource_owner_key=os.environ['X_ACCESS_TOKEN'],
    resource_owner_secret=os.environ['X_ACCESS_TOKEN_SECRET'],
)
r=s.get('https://api.x.com/1.1/account/verify_credentials.json')
print(r.status_code)
print(r.text[:300])
```

Sinyal sukses:
- Status `200`
- Respons mengandung `screen_name`.

## 3) Paket python di Ubuntu managed env
Jika pip blocked (PEP668), pakai apt:
```bash
sudo apt-get install -y python3-requests python3-requests-oauthlib
```

## 4) Post-incident security
Jika token sempat terkirim di chat/log:
- rotate/revoke semua token terkait,
- update env lokal dengan token baru,
- ulang verify endpoint.
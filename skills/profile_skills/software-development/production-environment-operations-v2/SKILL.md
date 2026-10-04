---
name: production-environment-operations-v2
description: "Use when modifying live web services, assets, or DBs."
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [production, deployment, database-sync, hosting, verification, access-audit, static-assets, vps-security, crm-lifecycle]
    related_skills: [systematic-debugging, reverify, zero-hallucination-coder, anti-hallucination-gates]
---

# Production Environment Operations & Multi-Server Synchronization

A standardized operational framework for inspecting, managing, provisioning, debugging, modifying static assets/databases, and auditing access across distributed production architectures (Local VPS vs. Remote cPanel / LiteSpeed / Shared Hosting).

## When to Use

- When resetting user accounts, updating credentials, or modifying databases on live web services.
- When configuring Linux VPS security (UFW firewall, SSH hardening, Nginx reverse proxy, and Certbot SSL).
- When replacing or updating live website images, static assets, and HTML templates on remote hosting (`public_html/`).
- When working in multi-tier architectures where development files reside on a VPS while production is served remotely.
- When delivering complete codebase files to clients working on local IDEs (VS Code) or deploying to remote VPS instances.
- When auditing server, agent, and gateway access surfaces (SSH authorized keys, system users, messaging platform allowed lists).

## Procedure

1. **Architecture & Active Data Path Discovery:**
   - **Inspect Live Domain Routing:** Resolve the target domain's IP and response headers before altering data or assets:
     ```bash
     curl -sI https://target-subdomain.domain.com
     dig +short target-subdomain.domain.com
     ```
   - **Identify the Host Environment:** Determine if the domain is served by the local VPS (via systemd/nginx/uvicorn) or hosted externally (e.g., cPanel LiteSpeed / Hostinger shared hosting).
   - **Locate Active Data/Asset Path:** Determine whether the active application reads from local `/home/ubuntu/...` or an independent remote directory (`public_html/`).

2. **Linux VPS Firewall Hardening & Remote SSH Automation:**
   - **Non-Interactive SSH Deployment:** When credentials (password) are provided by the client, use `sshpass` for reliable, non-interactive remote management:
     ```bash
     sshpass -p '<password>' ssh -o StrictHostKeyChecking=no ubuntu@<IP> '<command>'
     ```
   - **UFW Firewall Security Baseline:** Always permit SSH and web traffic before enabling UFW to prevent accidental administrator lockout:
     ```bash
     sudo ufw allow OpenSSH && sudo ufw allow "Nginx Full" && sudo ufw --force enable
     ```
   - **Certbot SSL/TLS Provisioning:** Verify public DNS resolution (`dig +short <domain>`) matches the VPS public IP before running Certbot to avoid ACME challenge failures:
     ```bash
     sudo certbot --nginx -d <domain> --non-interactive --agree-tos -m <email>
     ```
   - **Asynchronous DNS Propagation & Auto-SSL Daemon Pattern:** When migrating to a newly purchased or unpropagated domain, deploy a lightweight background loop/service to poll DNS resolution (`dig +short <domain> @8.8.8.8`) and execute Certbot automatically once the target IP is detected. This eliminates manual waiting and guarantees instant HTTPS activation without rate-limit errors from premature ACME requests:
     ```bash
     while true; do
       IP=$(dig +short <domain> @8.8.8.8 | head -n1)
       if [ "$IP" = "<target_ip>" ]; then
         certbot --nginx -d <domain> -d www.<domain> --non-interactive --agree-tos -m <email> --redirect && systemctl reload nginx && break
       fi
       sleep 20
     done
     ```

3. **Pre-Change Production Snapshot Protocol:**
   - **Database Dump:** Always generate a timestamped gzip dump before executing any update/migration:
     ```bash
     mysqldump -h <host> -u <user> -p'<password>' <database> | gzip > /path/to/backups/db_backup_pre_change_$(date +%Y%m%d_%H%M%S).sql.gz
     ```
   - **Source Code Snapshot:** Archive the affected directories (`app/`, `routes/`, `resources/`):
     ```bash
     tar -czf /path/to/backups/app_code_backup_$(date +%Y%m%d_%H%M%S).tar.gz app/ routes/
     ```

4. **CRM & Commercial Document Lifecycle Invariants:**
   - **Shipping Fee (Include vs Exclude) Propagation:**
     - *Quotation (QUO):* Shipping must display as non-binding `(-)` without affecting estimated subtotal.
     - *Proforma Invoice (PI) & Invoice (INV):* When Include, display `(-)`; when Exclude, display explicit numerical shipping line item and calculate into payable grand total. Provide manual adjustment options on Proforma generation.
     - *Delivery Order (DO):* Always omit shipping cost columns and figures entirely (surat jalan standard).
   - **Party Autocomplete & Address Autofill:** Store contact names (PIC), phone numbers, email addresses, and shipping addresses on counterparty records (`parties`), and embed client-side event listeners to auto-fill order forms upon party selection.
   - **Product Catalog Brand Invariance:** Ensure brand metadata is persisted into transaction snapshot rows and rendered in dedicated columns across all printed/downloaded documents (QUO, PO, PI, DO, INV).

5. **Large Codebase Delivery for Local Clients (VS Code):**
   - When a client is building locally and requests full code to copy-paste across a large file (>100KB), provide the complete deliverable file artifact directly via `MEDIA:/path/to/file` rather than truncating partial snippets across chat turns.

6. **Node.js Native SQLite (`node:sqlite` DatabaseSync) & Standalone VPS Deployment Pipeline:**
   - **Runtime Provisioning:** For modern ES module apps leveraging native SQLite (`import { DatabaseSync } from 'node:sqlite'`), ensure Node.js 22 LTS (v22.14+) or 24 is provisioned from official repositories:
     ```bash
     curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt-get install -y nodejs nginx rsync
     ```
   - **Systemd Daemon Unit:** Create a dedicated unit (`/etc/systemd/system/<app>.service`) with `Restart=always`, explicit `WorkingDirectory`, and loopback binding:
     ```ini
     [Unit]
     Description=<App Name> Daemon
     After=network.target

     [Service]
     Type=simple
     User=ubuntu
     WorkingDirectory=/home/ubuntu/<app-dir>
     Environment=NODE_ENV=production PORT=3000 HOST=127.0.0.1
     ExecStart=/usr/bin/node server.mjs
     Restart=always
     RestartSec=3

     [Install]
     WantedBy=multi-user.target
     ```
   - **Nginx Reverse Proxy & Payload Size:** Configure Nginx on port 80/443 proxying to `127.0.0.1:3000`. Always set `client_max_body_size 50M;` to accommodate large document attachments (PDFs, XLSX/CSV bulk imports) and pass standard proxy headers (`X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`).
   - **Database & Storage Permission Hardening:** Lock down permissions with `chmod 750 /home/ubuntu/<app-dir>` and `chmod -R 700 /home/ubuntu/<app-dir>/data` to prevent unauthorized local reads.

7. **Multi-Layer Access Auditing:**
   - **SSH Layer:** Inspect `~/.ssh/authorized_keys` for registered public keys.
   - **OS Layer:** Inspect `/etc/passwd` and `sudo` group for active interactive user accounts.
   - **Platform Gateway Layer:** Audit incoming interaction logs (e.g. `gateway.log` for `user=... chat=...`) and verify `allowed_chats` / channel whitelists in `config.yaml`.

8. **Post-Change Live Verification (Green Loop):**
   - **For API/Auth Changes:** Re-test the live HTTP endpoint directly with the exact generated identifier and password:
     ```bash
     curl -i -X POST "https://target-domain.com/api/auth/login" \
       -H "Content-Type: application/json" \
       -d '{"username":"<exact_user_or_email>","password":"<new_password>"}'
     ```
   - Declare completion only after the production endpoint returns HTTP 200 OK with confirmed changes.

## Pitfalls

- **Enabling UFW Before Allowing SSH:** Running `sudo ufw enable` without `sudo ufw allow OpenSSH` cuts off the active SSH connection immediately and locks out the server permanently.
- **Premature Certbot Execution Before DNS Propagation:** Running `certbot --nginx` before the domain's A record resolves to the target server triggers ACME challenge failures and Let's Encrypt rate-limiting.
- **Truncated Snippet Delivery on Large Monolithic Files:** Providing multiple small patch snippets to non-technical users editing massive single-file modules in VS Code creates syntax mismatches and broken scopes; always deliver the validated complete file artifact via `MEDIA:` path.
- **Delivery Order Financial Leaks:** Showing shipping fees, discounts, or price totals on Delivery Orders violates commercial surat jalan privacy; keep warehouse/logistics documents strictly quantity- and condition-focused.
- **Masked Credential Serialization in Multi-Profile Configs:** Copying profile configurations containing truncated/masked API keys (`sk-xxxx...xxxx`) breaks inference proxy authentication immediately with `HTTP 401 Invalid API key`. Always resolve raw keys directly from the source credentials vault before saving YAML configs.
- **Port Collisions on Multi-Profile Gateways:** Running multiple gateway instances with identical `platforms.api_server.port` causes the second instance to crash on startup with `Errno 98: Address already in use`. Enforce unique port offsets per profile.

---
name: production-environment-operations-v2
description: "Use when modifying live web services, assets, or DBs."
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [production, deployment, database-sync, hosting, verification, access-audit, static-assets]
    related_skills: [systematic-debugging, reverify, zero-hallucination-coder, anti-hallucination-gates]
---

# Production Environment Operations & Multi-Server Synchronization

A standardized operational framework for inspecting, managing, provisioning, debugging, modifying static assets/databases, and auditing access across distributed production architectures (Local VPS vs. Remote cPanel / LiteSpeed / Shared Hosting).

## When to Use

- When resetting user accounts, updating credentials, or modifying databases on live web services.
- When replacing or updating live website images, static assets, and HTML templates on remote hosting (`public_html/`).
- When working in multi-tier architectures where development files reside on a VPS while production is served remotely.
- When direct remote filesystem/database access (SFTP/SSH) is unavailable and administrative APIs or FTP must be leveraged.
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

2. **Pre-Change Production Snapshot Protocol:**
   - **Database Dump:** Always generate a timestamped gzip dump before executing any update/migration:
     ```bash
     mysqldump -h <host> -u <user> -p'<password>' <database> | gzip > /path/to/backups/db_backup_pre_change_$(date +%Y%m%d_%H%M%S).sql.gz
     ```
   - **Source Code Snapshot:** Archive the affected directories (`app/`, `routes/`, `resources/`):
     ```bash
     tar -czf /path/to/backups/app_code_backup_$(date +%Y%m%d_%H%M%S).tar.gz app/ routes/
     ```

3. **Scheduled State Transition & Lifecycle Repair (Cron / State Machines):**
   - **Audit State Machine Logic:** Inspect daily status commands (e.g. `UpdateMemberStatus`) to check if temporary states (e.g., `freeze`, `paused`, `suspended`) are being unconditionally skipped:
     ```php
     // Pitfall: Skipping freeze in daily updates leaves members locked when freeze expires
     if ($record->status === STATUS_FREEZE) { return STATUS_FREEZE; }
     ```
   - **Implement Proactive Lifecycle Commands:** Build dedicated Artisan/CLI commands (`members:auto-unfreeze`) that query expired records (`end_date < today`), calculate duration adjustments, restore status to active/expired, and mark transition records as `finished`.
   - **Syntax Check & Dry-Run Testing:** Validate syntax with `php -l <file>` and execute with a `--dry-run` flag to verify matching record counts before committing changes.
   - **Kernel Schedule Sequencing:** Register the transition command in `app/Console/Kernel.php` to run *prior* to the general status updater (e.g. unfreeze at `00:00`, status update at `00:05`).

4. **Remote Static Asset & Hero Banner Deployment:**
   - **Pre-Upload Asset Preparation & High-DPI Upscaling:** Convert and optimize local image/media assets to production formats (PNG-24 or WebP quality 90-95%) and standard canvas dimensions (e.g. `2400x1000` or `2560x1080` for full-width responsive heroes). When source images received via chat platforms suffer from downscaling/compression (e.g. 1280px caps), apply high-quality Lanczos scaling and unsharp masking (`scale=2560:1064:flags=lanczos,unsharp=5:5:1.0:5:5:0.0`) to enhance sharpness while requesting raw files sent as uncompressed documents.
   - **UI Collision & Layout Verification:** When deploying dense banner artwork, inspect for overlap between HTML floating CTA buttons / marquee bars and underlying text/hardware elements. Prototype alternative visual layouts (e.g. dedicated below-banner action bars vs. repositioned badges) using local temporary HTTP servers and browser visual inspection before pushing changes.
   - **Responsive CTA & Typography Sizing:** When adjusting CTA button prominence or size, update both base classes and responsive media queries (`@media (max-width: 1024px)` and `@media (max-width: 480px)`) to maintain proportional hierarchy across devices. Always bump the CSS stylesheet version query string (`style.css?v=N+1`) in `index.html` and verify live visual rendering via browser tools.
   - **Timestamped Remote Backup:** Download or copy the existing remote asset before overwriting (e.g. `public_html/images/<asset>_backup_<timestamp>.<ext>`).
   - **Upload via Clean Connection:** Upload new assets to the destination path. If using FTP on restricted hosts, open dedicated connections per discrete transfer to prevent passive data port timeouts.
   - **Cache-Busting & Metadata Synchronization:** Bump version query parameters (e.g. `images/hero.png?v=N+1`, `css/style.css?v=N+1`) across all HTML files and OpenGraph tags (`og:image`) so LiteSpeed/CDN caches and client browsers immediately receive fresh assets.

5. **Administrative API-Driven Provisioning (When Direct Remote DB Access is Blocked):**
   - **Inspect OpenAPI Specifications:** Query `/openapi.json` or `/docs` on the live domain to identify available registration, approval, and management endpoints.
   - **Authenticate with Admin Credentials:** Obtain a bearer token via `/api/auth/login` to interact with privileged routes.
   - **Execute Provisioning Flow:** Submit account creation through `/api/auth/register` and approve via `/api/auth/approve/{request_id}` (or direct admin CRUD routes) to persist changes directly in the live environment.

6. **Safe Database Modification & Backup (For Local/Direct Access):**
   - **Create Timestamped Backup:** Always snapshot target database files before edits (`cp db.sqlite db.sqlite.bak_$(date +%Y%m%d_%H%M%S)`).
   - **Apply Updates Deterministically:** Execute targeted SQL queries with native hashing libraries (e.g. `bcrypt`, `passlib`).

7. **cPanel / CloudLinux Python (FastAPI / ASGI) Deployment & Hot-Reload:**
   - **Architecture Pattern:** In cPanel / shared hosting setups where a PHP entrypoint (`index.php`) acts as a fast reverse proxy to a local ASGI daemon (`127.0.0.1:<port>`), deploy updates cleanly via an archive bundle:
     ```bash
     tar -czf /tmp/app_update.tar.gz main.py app/ templates/ static/
     ```
   - **Upload & Trigger Atomic Reload:** Upload `app_update.tar.gz` via FTP/SFTP and hit a server-side reload hook (e.g. `temp_reload.php` extracting the archive and issuing `pkill -f "uvicorn main:app"`). The reverse proxy automatically respawns the daemon on the next incoming request.
   - **Initial Wake-up Request:** Ping the domain root right after reload to trigger daemon startup and verify `HTTP 200 OK` before running end-to-end API suites.
   - **Database Auto-Migration on Deployment:** In distributed deployments where direct terminal access to remote SQLite databases is limited, embed idempotent table column migrations (e.g. `ALTER TABLE table_name ADD COLUMN col_name type`) inside the application startup lifecycle (`init_db()`) with graceful exception suppression, ensuring new schema fields propagate instantly upon archive extraction.

8. **WebRTC Camera, Geolocation & Secure Context (HTTPS) Architecture:**
   - **Secure Context Invariant:** Modern browsers (Chrome, Safari iOS, Android WebViews) enforce strict Secure Context policies: `navigator.mediaDevices.getUserMedia` and `navigator.geolocation` are completely undefined and blocked on insecure origins (`http://<IP>:<PORT>`).
   - **Hybrid Dual-Mode Capture Design:**
     - Primary Mode: High-speed live WebRTC streaming (`getUserMedia({ video: { facingMode: 'user' } })`) on `https://` production domains and `http://localhost`.
     - Fallback / Direct Mobile Mode: Native camera capture via `<input type="file" accept="image/*" capture="user">` with instant `FileReader.readAsDataURL` preview, allowing 100% reliable camera activation across any network topology, mobile operating system, or legacy browser.

9. **Centralized Geofencing, Company Settings & RBAC Control:**
   - **Centralized Parameter Persistence:** Store global operational variables (e.g., office GPS coordinates, geofence radius in meters, shift start times, tardiness grace periods, strict vs. flexible WFO enforcement) in a centralized database table (e.g., `company_settings` key-value store) with automatic fallback defaults rather than hardcoding constants in backend route handlers.
   - **Strict RBAC Mutation Guard:** Restrict settings update endpoints (`POST /api/settings/...`) exclusively to elevated roles (`super_admin`, `director`, `admin`) to prevent employees or lower-tier users from tampering with office coordinates or validation rules.
   - **Fair Tardiness (Grace Period) Calculation:** Calculate attendance lateness status dynamically against `(work_start_time + grace_period_mins)` instead of raw start time to prevent false 'late' flags during legitimate grace windows.
   - **Server-Side Distance Audit (Haversine Formula):** Always calculate geodesic distance on the backend using the Haversine formula against the central office coordinates to prevent client-side distance tampering. Validate radius strictly for `WFO` when strict mode is active, while allowing `WFH` and `Dinas Luar` to record GPS coordinates and notes without radius rejection.

10. **Multi-Role Endpoint Matrix Verification (RBAC Audit):**
   - When diagnosing web application 500 errors or after deployments, test authentication and dashboard routes across **every distinct user role** (e.g., `employee`, `manager`, `director`, `super_admin`), not just admin credentials. Subordinate aggregation queries and role-specific template blocks often hide fatal exceptions.

10. **Multi-Layer Access Auditing:**
   - **SSH Layer:** Inspect `~/.ssh/authorized_keys` for registered public keys.
   - **OS Layer:** Inspect `/etc/passwd` and `sudo` group for active interactive user accounts.
   - **Platform Gateway Layer:** Audit incoming interaction logs (e.g. `gateway.log` for `user=... chat=...`) and verify `allowed_chats` / channel whitelists in `config.yaml`.

11. **Post-Change Live Verification (Green Loop):**
   - **For API/Auth Changes:** Re-test the live HTTP endpoint directly with the exact generated identifier and password:
     ```bash
     curl -i -X POST "https://target-domain.com/api/auth/login" \
       -H "Content-Type: application/json" \
       -d '{"username":"<exact_user_or_email>","password":"<new_password>"}'
     ```
   - **For Static Asset Updates:** Curl the cache-busted asset URL directly, verify `HTTP 200` with expected `Content-Length`, and inspect the downloaded live image (e.g. with `vision_analyze`) to confirm visual correctness before completing the turn.
   - Declare completion only after the production endpoint returns HTTP 200 OK with confirmed changes.

## Pitfalls

- **WebRTC & Geolocation Insecure Context Failure:** Calling `navigator.mediaDevices.getUserMedia` or `navigator.geolocation` over plain `http://<IP>:<PORT>` fails silently or raises security errors because modern browsers restrict device sensors to HTTPS / localhost origins. Always provide an explicit fallback `<input type="file" accept="image/*" capture="user">` for native mobile camera activation on insecure origins.
- **Template Null-Math / NoneType Arithmetic Crashes:** In Jinja2/Blade/ERB templates, executing inline arithmetic on nullable metrics (e.g. `{{ (member.avg_achievement * 0.04)|round(2) }}`) crashes the entire route with `TypeError: unsupported operand type(s) for *: 'NoneType' and 'float'` when new records lack historical rows; always guard calculations with `(val or 0)` and explicit conditional null checks (`{% if val and val >= 95 %}`).
- **Database Row Object vs Dict API Mismatch:** `sqlite3.Row` and `aiosqlite.Row` objects do not implement `.get(key, default)` like native Python dictionaries; calling `row.get(...)` raises `AttributeError: 'sqlite3.Row' object has no attribute 'get'`. Convert with `dict(row)` or check keys explicitly.
- **Responsive Breakpoint Omission on CSS Updates:** Modifying desktop button padding or typography size without updating mobile/tablet media queries causes buttons to overflow or display awkwardly on mobile screens.
- **Messaging Platform Image Compression:** Receiving source images via standard photo messages caps resolution to 1280px and applies lossy compression; upscale with Lanczos + unsharp filters for immediate deployment, and instruct users to send master files as "Document / File" for raw quality.
- **Overlay UI Collision on Dense Banners:** Floating action buttons and ticker bars overlaid on top of banners containing text pillars and product hardware obscure vital information; design dedicated safe zones (e.g. lower 25% clean floor space) or shift CTA buttons below the banner frame.
- **Local vs Remote Divergence:** Updating a local SQLite file or local HTML/image on the VPS while the production site runs on an external cPanel/LiteSpeed host results in false-positive success reports; always verify the active data path.
- **Stale Browser & CDN Asset Caching:** Overwriting a static asset on a LiteSpeed/cPanel server without bumping the cache-busting query parameter (e.g., `?v=N`) in referencing HTML files leaves users viewing stale cached assets despite successful file upload.
- **FTP Passive Mode Connection Resets:** Reusing an idle FTP session for multiple sequential large data transfers or file uploads on restricted shared hosts often causes `TimeoutError`; open separate dedicated sessions or reset the connection between discrete operations.
- **Exact Username Format vs Partial Input:** When an account is provisioned with a structured username (e.g. `firstname.lastname`), submitting only `firstname` causes login failure. Always report the exact login string verified by the API probe.
- **Unverified Tool Assumptions:** Claiming an account is active without verifying both `is_active` and valid password hash columns causes immediate user-facing login rejection.
- **Silent Headless Installer Hangs:** Attempting silent `/auto` installations of interactive GUI software (e.g. MetaTrader) under headless terminals hangs indefinitely; always configure desktop launchers for Remote Desktop (XRDP/VNC) sessions.
- **Open Gateway Inbound Surface:** Leaving `telegram.allowed_chats` or platform channel filters empty permits arbitrary public inbound interactions; enforce explicit ID whitelists.

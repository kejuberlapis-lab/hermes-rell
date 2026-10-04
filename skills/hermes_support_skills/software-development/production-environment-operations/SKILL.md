---
name: production-environment-operations
description: "Use when modifying live web services or multi-server DBs."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [production, deployment, database-sync, hosting, verification, scheduler, cron]
    related_skills: [systematic-debugging, reverify, zero-hallucination-coder, anti-hallucination-gates]
---

# Production Environment Operations & Multi-Server Synchronization

A standardized operational framework for inspecting, managing, debugging, and modifying databases, scheduled lifecycle tasks, user accounts, and configurations across distributed or multi-tier production environments (VPS vs. cPanel / Hostinger / Remote Hosting).

## When to Use

- When executing user account resets, credential updates, or database modifications on live web services.
- When fixing stale status/lifecycle bugs where records remain stuck in passive states (e.g. frozen memberships, expired passes, suspended bookings) due to missing background scheduler tasks.
- When working in architectures where local development/VPS and remote production hosting (e.g., cPanel, IDWebHost, Hostinger) coexist.
- When diagnosing why local database changes or service updates fail to take effect on the live production domain.
- When synchronizing files, databases (`.db`, `.sqlite`), or codebases between a management VPS and a live production server.

## Procedure

1. **Architecture & Active Data Path Discovery:**
   - **Inspect Live Domain Routing:** Resolve the target domain's IP and HTTP response headers before touching data:
     ```bash
     curl -sI https://target-subdomain.domain.com
     dig +short target-subdomain.domain.com
     ```
   - **Identify the Host Environment:** Determine if the domain is served directly by the current VPS (via local systemd/nginx/uvicorn) or hosted independently on an external server (e.g. cPanel LiteSpeed server, Hostinger).
   - **Locate the Live Database & Configs:** Determine whether the active application reads from local storage or remote databases (`.env` credentials on the host).

2. **Pre-Change State Verification (Red Loop):**
   - Execute a minimal test probe (e.g., API login, database query, or dry-run command) against the LIVE environment to observe the initial state:
     ```bash
     curl -i -X POST "https://target-domain.com/api/auth/login" \
       -H "Content-Type: application/json" \
       -d '{"username":"<user>","password":"<current_password>"}'
     ```

3. **Mandatory Snapshot Backup:**
   - **Local VPS Backups:** Snapshot local databases and codebases:
     ```bash
     mysqldump -h <host> -u <user> -p'<password>' <database> | gzip > backups/db_backup_pre_fix_$(date +%Y%m%d_%H%M%S).sql.gz
     tar -czf backups/app_code_backup_$(date +%Y%m%d_%H%M%S).tar.gz app/ routes/
     ```
   - **Remote cPanel Hosting Snapshot (via FTP + PHP Helper):**
     - When SSH port 22 is disabled on shared cPanel hosting, upload a short-lived PHP helper to execute a tar archive command on the server:
       ```php
       <?php
       $target_tar = "/home/<user>/app_backup_" . date("Ymd_His") . ".tar.gz";
       shell_exec("tar --exclude='vendor' --exclude='storage' -czf " . escapeshellarg($target_tar) . " -C /home/<user>/<subdomain> . 2>&1");
       echo "BACKUP_FILE:" . $target_tar;
       ?>
       ```
     - Download the generated tar archive locally via FTP (`RETR <tar_name>`) with `ftp.set_pasv(True)`, and immediately delete the temporary helper script from the webroot.

4. **Deterministic Implementation & Syntax Check:**
   - **Write Reusable Artisan/CLI Commands:** For recurring state transitions (e.g. unfreezing expired accounts, recalculating quotas), create a dedicated command with `--dry-run` support.
   - **Syntax Validation:** Always run linter / syntax checks on new or patched files before deploying or executing on production:
     ```bash
     php -l app/Console/Commands/NewCommand.php
     ```
   - **Register in Scheduler:** Wire the command into the application scheduler (`Kernel.php` / cron) with proper ordering (`->withoutOverlapping()`).

5. **Post-Change Verification (Green Loop):**
   - Execute the live command or query and inspect the actual resulting rows:
     ```bash
     php artisan command:name
     ```
   - Query the database to verify all linked tables and cascaded fields updated accurately (e.g., primary membership, child PT/RFM records, end dates, and active flags).
   - Re-test the live HTTP/API endpoint or UI state directly. Only declare completion after verified with real tool output.

## Pitfalls

- **Passive vs Active State Transitions:** If status transitions only occur when an admin views a profile or a user checks in, inactive users remain permanently stuck in stale states (e.g. freeze/expired); always implement a scheduled background command to process lifecycle expirations automatically.
- **Local vs Remote Divergence:** Updating a local database on the VPS while the production site runs on an external host results in false-positive success reports; always verify the active data path and remote connection.
- **Skipping Syntax Checks on Remote Files:** Deploying PHP/Python files directly to production without `php -l` or syntax verification risks 500 Internal Server Errors that halt live traffic.
- **Ignoring Cascading Relations on Unfreeze/Status Update:** When unfreezing or reactivating a parent entity (e.g. membership), failing to also extend and unfreeze linked child records (e.g. PT clients, RFM clients, session quotas) leaves data in an inconsistent hybrid state.
- **Unverified Tool Assumptions:** Claiming an account is active without querying both `is_active` and valid password hash columns in the database causes immediate user-facing login rejection.
- **Silent Headless Installer Hangs:** Attempting silent `/auto` installations of interactive GUI software (e.g. MetaTrader) under headless terminals hangs indefinitely; always configure desktop launchers for Remote Desktop (XRDP/VNC) sessions.

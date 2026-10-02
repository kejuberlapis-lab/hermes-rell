import os

skill_path = "/home/ubuntu/.hermes/profiles/profil-admin-mvp/skills/software-development/production-environment-operations-v2/SKILL.md"

with open(skill_path, 'r') as f:
    content = f.read()

# Let's see what needs to be added
new_section = """
7. **Production Repository Cloning & Bandwidth-Constrained Packaging:**
   - **Gzip Database Dumps:** Always dump and compress MySQL database dumps (`mysqldump ... | gzip > dump.sql.gz`) to achieve ~90% compression (e.g. 48MB raw SQL reduces to 4.8MB).
   - **Handle Broken Symlinks in Zip Bundles:** Standard archive utilities and Python's `zipfile.write()` throw `FileNotFoundError` on broken symlinks (e.g. `public/storage`). Check `os.path.islink(path) and not os.path.exists(path)` and skip them.
   - **Filter Heavy User Uploads & Rotating Logs:** When creating a portable project archive for platform delivery (e.g. Telegram's 50MB limit), exclude raw media directories (`public/media`, `public/uploads`), duplicate test archives (`*.zip`), and rotating logs (`storage/logs/laravel.log`).
   - **Include Local Scaffolding & Setup Guide:** Always generate a `LOCAL_SETUP_GUIDE.md` detailing database import steps (`mysql < dump.sql`), `.env` setup, and dependency commands (`composer install`, `npm install`).
"""

# Let's patch the procedure and pitfalls
if "7. **Production Repository Cloning" not in content:
    target = "   - Declare completion only after the production endpoint returns HTTP 200 OK with confirmed changes.\n"
    content = content.replace(target, target + new_section)

new_pitfalls = """- **Uncompressed Database & Symlink Failures in Archives:** Attempting to zip a raw SQL database dump or unhandled broken symlinks (`public/storage`) results in archive generation crashes or exceeds platform upload caps (e.g. Telegram 50MB); always gzip SQL dumps and filter broken links.
- **Passive Lifecycle State Lock:** Relying solely on interactive user logins or page visits to trigger state transitions (such as unfreezing expired accounts or calculating attendance streaks) causes inactive members to remain permanently locked; always implement dedicated background schedulers with dry-run support.
"""

if "Uncompressed Database & Symlink Failures in Archives" not in content:
    content = content + new_pitfalls

with open(skill_path, 'w') as f:
    f.write(content)

print("SKILL.md updated successfully!")

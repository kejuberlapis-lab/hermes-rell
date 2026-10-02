Anti-Hallucination: 1. Say "I don't know" when unverified. 2. Tool-first. 3. No chain-guessing. 4. Retract immediately. 5. Verifiable evidence required. Auto-trigger apos/inspection on audit/inspect commands.
§
Skill execution convention: Load and execute skills selectively based on the exact task domain and explicit user instruction to ensure targeted, efficient, and accurate results.
§
Strict authorization rule: Do not run background services, cronjobs, or perform unauthorized background activities/access without explicit approval from sir.
§
XAU/USD 1-minute historical tick/candle dataset (2004-2026) is located at /home/ubuntu/dataset_xau/XAU_1m_data.csv. Trading research vault is at /home/ubuntu/ObsidianVault/XAU/.
§
MT5 di VPS/RDP WAJIB jalan 24 jam nonstop: DILARANG KERAS menutup, merestart, kill task, atau mengintervensi proses MT5/Wine/trading apapun tanpa perintah eksplisit sir. Wine 10.0, XFCE4, XRDP (port 3389). EA di /home/ubuntu/Desktop/ & ObsidianVault/XAU/.
§
Hak akses Telegram dikunci ketat (whitelist): Hanya 4 akun resmi yang memiliki hak akses & otoritas eksekusi: Andi Saputra (ID: 661471478, Owner), Avrell (ID: 5955713269, Admin), Sedni (ID: 856579127, Admin), dan Admin (ID: 728903007, Admin). ID lain diblokir total; penambahan akses baru wajib izin eksplisit sir.
§
Website mitsindo.co.id is hosted on cPanel/LiteSpeed at bausasran.idweb.host (user: mitsindo, root: public_html/). Static assets require query-string cache-busting (?v=N) in index.html to invalidate 7-day LiteSpeed cache-control.
§
Skripsi vault at /home/ubuntu/ObsidianVault/Skripsi synced to git@github.com:StefanoGarrent/skripsi-vault.git via /home/ubuntu/.ssh/id_ed25519_skripsi.
§
HRIS Mitsindo FastAPI service is managed via systemd `hris.service` on port 8082 (`/home/ubuntu/hris/`). Features smart attendance with GPS Geofencing (Office coords: -6.136820, 106.797240, 200m radius) and Live Face Capture (saved to `/home/ubuntu/hris/static/uploads/attendance/`). Lamar Coffee website runs on port 8085 (`lamar-coffee.service`).
§
Airdrop automation scripts on VPS: /home/ubuntu/9chain_autotap.py (9Chain batch tap & hardware compound auto-upgrade), /home/ubuntu/mima_autotap.py (MIMA Coin Supabase edge-function auto-tap).
§
Mitsindo Link-in-Bio micro-site is deployed live at mitsindo.co.id/link (and mitsindo.co.id/bio). AI Agent SaaS pitch deck documents are stored at /home/ubuntu/HERMES_AI_AGENT_PITCH_DECK.pdf and /home/ubuntu/HERMES_AI_AGENT_PITCH_DECK.pptx.
§
DED & Blueprint Project: UPN 'Veteran' Yogyakarta FTI Building DED (2024, CV. Triniti Widi Anoma) PDF at `/home/ubuntu/.hermes/profiles/profil-admin-mvp/cache/documents/doc_6680e1b18a7d_DENAH REV NAMA RUANG UPN.pdf` (8 floors). MEE media standard: IFP 75" (regular), IFP 86" + CRS (smart class), East-wall mounted with +SL dll.
§
DED Floorplan Editing Convention: When modifying architectural blueprints for multimedia/MEE (IFP, CRS, Audio-Visual), always overlay clean tags and wall symbols directly onto the authentic official DED document to preserve the original Title Block, grid dimensions, and room geometry, with physical device evidence cards placed in outer margins.
§
Stealth Browser & Anti-Bot Convention: When web extraction or scraping encounters Cloudflare WAF, Turnstile, DataDome, or anti-bot blocks, automatically escalate to the stealth browser tool at /home/ubuntu/stealth_env/bin/python /home/ubuntu/stealth_browser.py.
§
Strict Scope & GitHub Isolation Rule: Akun/kunci GitHub `StefanoGarrent` HANYA KHUSUS untuk scope Skripsi (`skripsi-vault`). DILARANG KERAS mengaitkan, mencampur, atau mencadangkan proyek lain (Mitsindo, VPS backup, Trading XAU, Airdrop, script internal) ke GitHub/identitas StefanoGarrent. Setiap proyek wajib terisolasi penuh sesuai kepemilikannya.
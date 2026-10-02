# Safe local/VPS Hermes sync notes

Use this when syncing local Hermes, VPS-Zeus profile `hermes-support`, and Telegram-facing runtime as one operational ecosystem.

## Safe sync scope
Sync these when asked to keep identity/rules/skills operationally aligned:
- `SOUL.md`
- `SYNC_POLICY.md`
- allowlisted custom skills
- non-secret config behavior fields (display, memory, approvals, platform toolsets, auxiliary model routing when explicitly requested)
- operational logs with redacted summaries

Do not sync:
- `.env`
- provider keys, Telegram tokens, passwords, cookies, auth/session stores
- private keys
- raw message/session databases unless explicitly requested and privacy-reviewed

## Robust transfer pattern
- Prefer explicit allowlists over broad directory sync.
- Do not use `rsync --delete` on broad `skills/` roots with include/exclude patterns; it can attempt to delete unrelated skill directories. Sync specific skill directories or use allowlist without delete.
- Create a dedicated SSH key for machine-to-machine sync if sir approves. Store only the private key locally, install the public key on the VPS, and log only the fingerprint.
- Systemd timers are useful for local-to-VPS sync while local/WSL is online; make the script idempotent and log safe summaries.

## Verification
- Compare hashes for core policy files.
- Verify expected custom skills exist on both sides.
- Verify gateway runner responsibility: VPS-Zeus should be Telegram runner if it is the always-on host; local gateway should stay stopped unless sir chooses local as runner.
- **Lokal gateway fix kuat:** Jika VPS runner utama, jangan hanya `stop` + `disable` gateway lokal. **Hapus service file** untuk mencegah restart dalam kondisi apapun:
  ```bash
  rm -f ~/.config/systemd/user/hermes-gateway.service
  systemctl --user daemon-reload
  ```
  `disable` saja masih bisa restart via lingering, on-failure, atau preset enable setelah reboot WSL.

## 1 KESATUAN model sync
Model, provider, dan base_url HARUS sama di semua sisi (lokal, VPS all profiles). Saat ini:
```yaml
model:
  default: deepseek-v4-flash
  provider: deepseek
  base_url: https://api.deepseek.com/v1
```
Setiap perubahan model WAJIB diterapkan ke semua 6 config files (lokal + 5 VPS profiles) secara serentak. Jangan pernah membuat satu profile berbeda tanpa instruksi eksplisit.

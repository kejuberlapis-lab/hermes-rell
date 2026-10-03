# OpenRouter fallback + exchange migration notes

## Ringkasan praktik yang terbukti
1. **Validasi provider LLM dua tahap**:
   - Tes endpoint daftar model (konektivitas + auth dasar).
   - Tes endpoint chat/completions (inferensi nyata).
2. **Saat uji API exchange signed request**:
   - Jika `signature invalid`, utamakan cek pasangan key, format signature, timestamp.
3. **Saat user pindah exchange**:
   - Bersihkan env var exchange lama.
   - Hapus key file lama jika diminta user.
   - Verifikasi tidak ada jejak config lama.

## Pola komunikasi untuk user mode ketat
- Eksekusi hanya atas instruksi eksplisit.
- Hasil teknis dilaporkan ringkas: status OK/FAIL + error inti.
- Jangan tampilkan credential; mask jika perlu.

## Guardrail sensitif
- Jangan minta user kirim private key/token mentah di chat bila bisa dihindari.
- Jika user terlanjur kirim, sarankan revoke/rotate secepatnya.
- Minimal enforce: no-withdraw + IP whitelist untuk API trading.

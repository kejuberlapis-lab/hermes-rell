#!/usr/bin/env bash
# Encrypted, timestamped backup of a Hermes deployment's state.
# Part of the hermes-backup-recovery skill. Vendor- and hardware-agnostic.
set -euo pipefail

: "${HERMES_HOME:?set HERMES_HOME to your Hermes data directory (memory, skills, config)}"
: "${BACKUP_DIR:?set BACKUP_DIR to where encrypted backups should be written}"
: "${AGE_RECIPIENT:?set AGE_RECIPIENT to an age public key (age1...)}"
KEEP="${KEEP:-14}"   # how many backups to retain

command -v age >/dev/null || { echo "error: 'age' not installed (https://github.com/FiloSottile/age)" >&2; exit 1; }
command -v tar >/dev/null || { echo "error: 'tar' not found" >&2; exit 1; }
[ -d "$HERMES_HOME" ] || { echo "error: HERMES_HOME '$HERMES_HOME' is not a directory" >&2; exit 1; }

mkdir -p "$BACKUP_DIR"
ts="$(date -u +%Y%m%dT%H%M%SZ)"
out="$BACKUP_DIR/hermes-$ts.tar.gz.age"

echo "backing up $HERMES_HOME -> $out"
tar -C "$(dirname "$HERMES_HOME")" -czf - "$(basename "$HERMES_HOME")" \
  | age -r "$AGE_RECIPIENT" -o "$out"

( cd "$BACKUP_DIR" && sha256sum "$(basename "$out")" > "$(basename "$out").sha256" )
echo "wrote $out ($(du -h "$out" | cut -f1))"

# retention: keep the newest $KEEP, remove the rest (and their checksums).
# Portable (no mapfile) so it also runs on older bash, e.g. macOS bash 3.2.
ls -1t "$BACKUP_DIR"/hermes-*.tar.gz.age 2>/dev/null | tail -n +"$((KEEP + 1))" | while IFS= read -r f; do
  [ -n "$f" ] || continue
  rm -f -- "$f" "$f.sha256"
  echo "pruned $f"
done
echo "done."

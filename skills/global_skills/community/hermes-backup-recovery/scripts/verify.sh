#!/usr/bin/env bash
# Verify the latest (or a given) encrypted backup: checksum + test decrypt/extract.
# Exit 0 = backup is decryptable and non-empty; non-zero = problem.
set -euo pipefail

: "${BACKUP_DIR:?set BACKUP_DIR}"
: "${AGE_IDENTITY:?set AGE_IDENTITY to your age private key file (keys.txt)}"
command -v age >/dev/null || { echo "error: 'age' not installed" >&2; exit 1; }

file="${1:-$(ls -1t "$BACKUP_DIR"/hermes-*.tar.gz.age 2>/dev/null | head -n1 || true)}"
[ -n "${file:-}" ] && [ -f "$file" ] || { echo "no backup found in $BACKUP_DIR" >&2; exit 1; }
echo "verifying $file"

if [ -f "$file.sha256" ]; then
  ( cd "$(dirname "$file")" && sha256sum -c "$(basename "$file").sha256" ) \
    || { echo "CHECKSUM FAILED" >&2; exit 1; }
fi

tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
age -d -i "$AGE_IDENTITY" "$file" | tar -tzf - > "$tmp/list.txt"
n="$(wc -l < "$tmp/list.txt")"
[ "$n" -gt 0 ] || { echo "backup decrypts but contains no entries" >&2; exit 1; }
echo "OK: decrypts, checksum valid, $n entries."

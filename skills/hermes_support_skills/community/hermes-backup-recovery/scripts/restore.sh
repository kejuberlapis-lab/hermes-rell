#!/usr/bin/env bash
# Restore a Hermes backup. DRY-RUN by default; pass --apply to actually write files.
set -euo pipefail

: "${AGE_IDENTITY:?set AGE_IDENTITY to your age private key file}"
command -v age >/dev/null || { echo "error: 'age' not installed" >&2; exit 1; }

apply=0; file=""
for a in "$@"; do
  case "$a" in
    --apply) apply=1 ;;
    -*) echo "unknown option: $a" >&2; exit 2 ;;
    *) file="$a" ;;
  esac
done

[ -n "$file" ] && [ -f "$file" ] || { echo "usage: restore.sh [--apply] <backup.tar.gz.age>" >&2; exit 1; }
: "${RESTORE_TARGET:?set RESTORE_TARGET to the directory to restore into}"

if [ "$apply" -eq 0 ]; then
  echo "DRY RUN — would restore $file into $RESTORE_TARGET:"
  age -d -i "$AGE_IDENTITY" "$file" | tar -tzf - | sed 's/^/  /'
  echo "re-run with --apply to write these files."
  exit 0
fi

echo "restoring $file into $RESTORE_TARGET"
mkdir -p "$RESTORE_TARGET"
age -d -i "$AGE_IDENTITY" "$file" | tar -xzf - -C "$RESTORE_TARGET"
echo "done. Review $RESTORE_TARGET, then restart Hermes."

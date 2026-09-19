#!/usr/bin/env bash
# Take the newest drop from ~/Downloads, apply the local fixes, check it, publish it.
#
#   tools/deploy-drop.sh              newest zip in ~/Downloads
#   tools/deploy-drop.sh --dry-run    do everything except commit and push
#   tools/deploy-drop.sh path/to.zip  a specific zip
#
# Any failed check stops the run before anything is committed. Nothing is published
# that has not passed every check below.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY=0
ZIP=""
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    *) ZIP="$arg" ;;
  esac
done

say()  { printf '\n\033[1m%s\033[0m\n' "$*"; }
ok()   { printf '  ok    %s\n' "$*"; }
fail() { printf '  FAIL  %s\n' "$*"; FAILED=$((FAILED+1)); }

# ---------------------------------------------------------------- find the drop
if [ -z "$ZIP" ]; then
  ZIP="$(ls -t "$HOME"/Downloads/*.zip 2>/dev/null | head -1 || true)"
fi
[ -n "$ZIP" ] && [ -f "$ZIP" ] || { echo "No zip found. Pass one as an argument."; exit 1; }

say "Drop: $ZIP  ($(date -r "$ZIP" '+%d %b %H:%M'))"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
unzip -q "$ZIP" -d "$WORK/a"

# the drop is sometimes a zip inside a zip
for inner in "$WORK"/a/*.zip; do
  [ -e "$inner" ] || break
  unzip -q "$inner" -d "$WORK/b"
done

SRC="$(find "$WORK" -type f -path '*/ibc2026/index.html' -print0 \
        | xargs -0 -n1 dirname | xargs -n1 dirname | sort -u | head -1)"
[ -n "$SRC" ] || { echo "No ibc2026/index.html inside that zip."; exit 1; }

VER="$(grep -o 'id="version">v\. [0-9.]*' "$SRC/ibc2026/index.html" | head -1 | sed 's/.*v\. //')"
echo "  version in the drop: ${VER:-unstamped}"

# --------------------------------------------------------------- apply the fixes
say "Applying local fixes"
python3 "$REPO/tools/apply-drop.py" "$SRC" "$REPO" | sed 's/^/  /'

# --------------------------------------------------------------------- check it
say "Checking the result"
FAILED=0
SCAN="$REPO/ibc2026/index.html"
SRCS="$REPO/ibc2026/sources/index.html"
count() { grep -c "$1" "$2" || true; }

[ "$(count cloudflareinsights "$SCAN")" = 1 ] && ok "analytics beacon on the scan"        || fail "analytics beacon on the scan"
[ "$(count cloudflareinsights "$SRCS")" = 1 ] && ok "analytics beacon on sources"          || fail "analytics beacon on sources"
[ "$(count 'whatsnew.js' "$SCAN")" = 1 ]     && ok "what-changed notice included"          || fail "what-changed notice included"
[ "$(count 'prefers-color-scheme:dark' "$SCAN")" = 0 ] &&
[ "$(count 'prefers-color-scheme:dark' "$SRCS")" = 0 ] && ok "no dark blocks"              || fail "no dark blocks"
[ "$(count 'color-scheme:light' "$SCAN")" -ge 1 ] && ok "light rendering forced"           || fail "light rendering forced"
[ "$(count 'class="promo p' "$SCAN")" = 5 ]  && ok "five promos"                           || fail "five promos (book and course split)"
[ "$(count 'B0DQ6XYZ12' "$SCAN")" = 0 ]      && ok "no placeholder book link"              || fail "no placeholder book link"
[ "$(count 'href="#database">The database' "$SCAN")" = 1 ] &&
[ "$(count 'href="#top">The database' "$SCAN")" = 0 ] && ok "database link hits the filter bar" \
                                                       || fail "database link hits the filter bar"

python3 - "$REPO" <<'PY' && ok "structure and records" || fail "structure and records"
import json, re, sys, pathlib
repo = pathlib.Path(sys.argv[1])
h = (repo / 'ibc2026/index.html').read_text()
body = re.sub(r'<script.*?</script>', '', h[h.index('<div class="wrap"'):], flags=re.S)
problems = []

o, c = len(re.findall(r'<div\b', body)), len(re.findall(r'</div>', body))
if o != c:
    problems.append('div tags unbalanced (%d open, %d close)' % (o, c))
if '</p>\n</div>\n<div class="col">' in h:
    problems.append('the wrapper still closes before the trailing column')

m = re.search(r'(const|let|var)\s+D\s*=\s*\[', h)
start = h.index('[', m.end() - 1); depth = 0
for j in range(start, len(h)):
    if h[j] == '[': depth += 1
    elif h[j] == ']':
        depth -= 1
        if depth == 0:
            end = j + 1; break
inlined = json.loads(h[start:end])
onfile = json.loads((repo / 'ibc2026/data.json').read_text())

if len(inlined) != len(onfile):
    problems.append('page has %d records, data.json has %d' % (len(inlined), len(onfile)))
if not 50 <= len(inlined) <= 500:
    problems.append('record count of %d looks wrong' % len(inlined))

platform = sum(1 for r in inlined if r.get('tier') == 'platform')
words = {6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten'}
said = set(re.findall(r'(Six|Seven|Eight|Nine|Ten) cloud and platform companies', h))
if said and said != {words.get(platform, '')}:
    problems.append('prose says %s cloud and platform companies, data has %d'
                    % ('/'.join(sorted(said)), platform))

for p in problems:
    print('        ' + p)
sys.exit(1 if problems else 0)
PY

if [ "$FAILED" -gt 0 ]; then
  say "$FAILED check(s) failed. Nothing committed."
  echo "  The working tree holds the applied drop, so you can look at it with: git -C \"$REPO\" diff"
  exit 1
fi

# --------------------------------------------------------------------- publish
if ! git -C "$REPO" diff --quiet || ! git -C "$REPO" diff --cached --quiet; then
  :
else
  say "Nothing changed. The drop matches what is already live."
  exit 0
fi

git -C "$REPO" --no-pager diff --stat | sed 's/^/  /'

if [ "$DRY" = 1 ]; then
  say "Dry run. Stopping before commit."
  exit 0
fi

say "Publishing"
git -C "$REPO" add -A
git -C "$REPO" -c user.name="Carlo De Marchis" -c user.email="carlodemarchis@gmail.com" \
  commit -q -m "IBC2026 vendor scan v${VER:-update}: new drop, local fixes re-applied

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git -C "$REPO" push -q origin main
echo "  pushed $(git -C "$REPO" rev-parse --short HEAD)"

say "Waiting for the live site"
for i in $(seq 1 40); do
  live="$(curl -s https://research.aguywithascarf.com/ibc2026/ \
          | grep -o 'id="version">v\. [0-9.]*' | head -1 | sed 's/.*v\. //' || true)"
  if [ -n "$VER" ] && [ "$live" = "$VER" ]; then
    echo "  live: v. $live"
    exit 0
  fi
  sleep 10
done
echo "  still serving v. ${live:-unknown} after 400s. Pushed, so it should land shortly."

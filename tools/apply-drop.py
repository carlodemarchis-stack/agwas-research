#!/usr/bin/env python3
"""Apply a drop of ibc2026/* into the repo, re-applying the four local fixes.
Usage: apply-drop.py <unzipped-drop-dir> <repo-dir>
Leaves the repo's own index.html (the hub) alone."""
import re, shutil, sys, pathlib

drop, repo = (pathlib.Path(p) for p in sys.argv[1:3])

BEACON = ("<!-- Cloudflare Web Analytics --><script type='module' "
          "src='https://static.cloudflareinsights.com/beacon.min.js' "
          "data-cf-beacon='{\"token\": \"f80d4833a806470fa2f3ad80ad8beda9\"}'>"
          "</script><!-- End Cloudflare Web Analytics -->")
BOOK = "https://www.amazon.it/Becoming-Better-Vendor-Sports-Media/dp/B0GP66Q1ZK/"
COURSE = "https://b2b.aguywithascarf.com/"
WHATSNEW = '<script src="whatsnew.js" defer></script>'

# 1. copy everything the drop carries except the hub page
for src in drop.rglob('*'):
    if src.is_dir() or src.name == 'index.html' and src.parent == drop:
        continue
    dst = repo / src.relative_to(drop)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print('copied', dst.relative_to(repo))


DROP = {'1 Legion'}   # records Carlo removed by hand; re-applied on every drop

def drop_records(h):
    """Remove DROP entries from the page's inlined D array and fix the prose tally."""
    import json as _json
    m = re.search(r'(const|let|var)\s+D\s*=\s*\[', h)
    if not m:
        return h
    start = h.index('[', m.end() - 1)
    depth = 0
    for j in range(start, len(h)):
        if h[j] == '[': depth += 1
        elif h[j] == ']':
            depth -= 1
            if depth == 0:
                end = j + 1; break
    arr = _json.loads(h[start:end])
    kept = [r for r in arr if r.get('v') not in DROP]
    if len(kept) == len(arr):
        return h
    h = h[:start] + _json.dumps(kept, separators=(',', ':'), ensure_ascii=False) + h[end:]
    n = sum(1 for r in kept if r.get('tier') == 'platform')
    words = {7: 'Seven', 8: 'Eight', 9: 'Nine', 6: 'Six'}
    for k, w in words.items():
        if k != n:
            h = h.replace(w + ' cloud and platform companies', words[n] + ' cloud and platform companies')
    return h

def fix(rel, fn):
    p = repo / rel
    h = p.read_text(); before = h
    h = fn(h)
    if 'cloudflareinsights' not in h:
        h = h.rstrip('\n') + '\n' + BEACON + '\n'
    if rel == 'ibc2026/index.html' and WHATSNEW not in h:
        h = h.rstrip('\n') + '\n' + WHATSNEW + '\n'
    # light only: drop dark blocks, force light UA controls
    h = re.sub(r'\n?@media \(prefers-color-scheme:dark\)\{[^@]*?\}\}', '', h)
    if 'color-scheme:light' not in h:
        h = h.replace('<style>', '<style>\n:root{color-scheme:light}', 1)
    p.write_text(h)
    print('patched', rel, '(changed)' if h != before else '(no change)')

def scan(h):
    # book and course as two promos, with the real links
    old = re.search(r'<div class="promo p4 amz">.*?</div>', h, re.S)
    if old and 'B0DQ6XYZ12' in old.group(0):
        h = h.replace(old.group(0), f'''<div class="promo p4 amz">
 <p class="eyebrow">Book</p>
 <h4>Becoming a Better B2B Tech Vendor in Sports and Media</h4>
 <p>Ten things to consider, written up from the vendor side. What this scan keeps finding: how vendors pitch, and what buyers actually hear.</p>
 <a class="cta" href="{BOOK}" target="_blank" rel="noopener">Get the book</a>
</div>

<div class="promo p5 amz">
 <p class="eyebrow">Course &middot; paid</p>
 <h4>Becoming a better B2B tech vendor</h4>
 <p>Twelve lessons in four movements, plus the companion book. Positioning, pricing and how buying decisions get made. Yours for life.</p>
 <a class="cta" href="{COURSE}" target="_blank" rel="noopener">View the course</a>
</div>''', 1)
    if '.promo.p5{' not in h:
        h = h.replace('.promo.p4{top:168px}', '.promo.p4{top:168px}.promo.p5{top:192px}', 1)
    # the trailing note and footer belong inside .wrap; the source closes it early,
    # which drops them out of the centred column and flush against the left edge
    early = ('<p class="empty" id="empty" hidden>Nothing matches that combination. Clear a filter.</p>'
             '\n</div>\n<div class="col">')
    if early in h:
        h = h.replace(early, early.replace('\n</div>\n<div class="col">', '\n\n<div class="col">'), 1)
        i = h.rindex('</footer>')
        j = h.index('</div>', i) + len('</div>')
        h = h[:j] + '\n</div>' + h[j:]

    # records Carlo has asked to be dropped from the scan
    h = drop_records(h)

    # the database jump link points at the filter bar, not the page head
    h = h.replace('<a href="#top">The database</a>', '<a href="#database">The database</a>', 1)
    if '#database{scroll-margin-top:0}' not in h:
        h = h.replace('#top{scroll-margin-top:0}', '#top{scroll-margin-top:0}\n#database{scroll-margin-top:0}', 1)
    return h

# data.json is a downloadable copy of the same records, so it has to drop them too
import json as _json
_dp = repo / 'ibc2026/data.json'
if _dp.exists():
    _recs = _json.loads(_dp.read_text())
    _kept = [r for r in _recs if r.get('v') not in DROP]
    if len(_kept) != len(_recs):
        _dp.write_text(_json.dumps(_kept, indent=1, ensure_ascii=False))
        print('data.json', len(_recs), '->', len(_kept))

fix('ibc2026/index.html', scan)
fix('ibc2026/sources/index.html', lambda h: h)

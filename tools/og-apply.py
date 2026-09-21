import pathlib, re, html as H

BASE = 'https://research.aguywithascarf.com'
SITE = 'A Guy With A Scarf: Research'

FALLBACK = {
    'index.html': 'Working datasets and scans behind the writing, published with their methods attached.',
    'ibc2026/changes/index.html': 'Every version of the IBC2026 vendor scan as it went live, newest first.',
}

def img_for(rel):
    if rel.startswith('ibc2026/'): return BASE + '/ibc2026/og.png'
    if rel.startswith('automated-video/'): return BASE + '/automated-video/og.png'
    return BASE + '/og.png'

def url_for(rel):
    if rel == 'index.html': return BASE + '/'
    if rel.endswith('/index.html'): return BASE + '/' + rel[:-len('index.html')]
    return BASE + '/' + rel

def apply(p):
    rel = str(p); h = p.read_text()
    if 'og:image' in h:          # already complete
        return False
    title = re.search(r'<title>(.*?)</title>', h, re.S)
    title = H.unescape(title.group(1).strip()) if title else 'A Guy With A Scarf: Research'
    title = re.sub(r'^A Guy With A Scarf: ', '', title)
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    desc = H.unescape(d.group(1)) if d else FALLBACK.get(rel, '')
    if not desc:
        lede = re.search(r'<p class="lede">(.*?)</p>', h, re.S)
        desc = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', lede.group(1))).strip()[:200] if lede else ''
    url, img = url_for(rel), img_for(rel)
    e = lambda s: H.escape(s, quote=True)

    add = []
    if 'name="description"' not in h and desc:
        add.append(f'<meta name="description" content="{e(desc)}">')
    if 'rel="canonical"' not in h:
        add.append(f'<link rel="canonical" href="{url}">')
    if 'og:type' not in h:      add.append('<meta property="og:type" content="website">')
    if 'og:site_name' not in h: add.append(f'<meta property="og:site_name" content="{e(SITE)}">')
    if 'og:title' not in h:     add.append(f'<meta property="og:title" content="{e(title)}">')
    if 'og:description' not in h and desc:
        add.append(f'<meta property="og:description" content="{e(desc)}">')
    if 'og:url' not in h:       add.append(f'<meta property="og:url" content="{url}">')
    add += [f'<meta property="og:image" content="{img}?v=1">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            f'<meta property="og:image:alt" content="{e(title)}">']
    if 'twitter:card' not in h:
        add.append('<meta name="twitter:card" content="summary_large_image">')
        add.append(f'<meta name="twitter:title" content="{e(title)}">')
        if desc: add.append(f'<meta name="twitter:description" content="{e(desc)}">')
    add.append(f'<meta name="twitter:image" content="{img}?v=1">')

    block = '\n'.join(add) + '\n'
    m = re.search(r'<title>.*?</title>\n?', h, re.S)
    assert m, rel
    p.write_text(h[:m.end()] + block + h[m.end():])
    return True

pages = sorted(p for p in pathlib.Path('.').rglob('*.html') if '.git' not in p.parts)
n = sum(1 for p in pages if apply(p))
print(f'{n} of {len(pages)} pages given social meta')

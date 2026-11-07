#!/usr/bin/env python3
"""Render a 1200x630 share card in the research site's style.

    tools/og-card.py <out.png> <title> <subtitle> <url-shown-on-card>

Writes an HTML card, screenshots it with headless Chrome at 2x so the Archivo
from Google Fonts is real (it is not installed on this Mac), then downsamples
to 1200x630. Chrome writes the file and then hangs, so it is launched in the
background and killed after a fixed wait.
"""
import html, os, pathlib, shutil, subprocess, sys, tempfile, time

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
KICKER = 'A Guy With A Scarf · Research'

TPL = """<!doctype html><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Archivo+Narrow:wght@600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:#FBFAF7;color:#1C1B19;font-family:"Archivo",system-ui,sans-serif;
 padding:64px 72px;display:flex;flex-direction:column;justify-content:space-between;
 border-left:14px solid #B05708}
.top{display:flex;align-items:center;gap:18px}
.mark{display:flex;gap:5px;align-items:flex-end;height:34px}
.mark i{display:block;width:9px;border-radius:2px}
.kicker{font-family:"Archivo Narrow",sans-serif;font-size:21px;font-weight:700;letter-spacing:.14em;
 text-transform:uppercase;color:#B05708}
h1{font-size:__SIZE__px;font-weight:700;letter-spacing:-.025em;line-height:1.04;max-width:19ch}
p{font-size:27px;line-height:1.4;color:#5B6169;max-width:40ch;margin-top:22px}
.strip{display:flex;gap:3px;height:22px;width:520px;flex:0 0 520px}
.strip i{flex:1;border-radius:1px}
.foot{display:flex;justify-content:space-between;align-items:center;gap:30px}
.url{font-family:"Archivo Narrow",sans-serif;font-size:20px;font-weight:600;letter-spacing:.06em;
 text-transform:uppercase;color:#9A958B;white-space:nowrap}
</style>
<div class="top">
 <span class="mark"><i style="background:#E2DED6;height:26px"></i><i style="background:#F6CFA8;height:30px"></i><i style="background:#EE9A55;height:34px"></i><i style="background:#C25C06;height:22px"></i></span>
 <span class="kicker">__KICKER__</span>
</div>
<div>
 <h1>__TITLE__</h1>
 <p>__SUB__</p>
</div>
<div class="foot">
  <span class="strip">__STRIP__</span>
  <span class="url">__URL__</span>
</div>
"""
SHADES = ['#C25C06', '#EE9A55', '#F6CFA8', '#E2DED6']


def render(out, title, sub, url, size=70):
    strip = ''.join('<i style="background:%s"></i>' % SHADES[i % 4] for i in range(34))
    page = (TPL.replace('__KICKER__', html.escape(KICKER)).replace('__TITLE__', html.escape(title))
               .replace('__SUB__', html.escape(sub)).replace('__URL__', html.escape(url))
               .replace('__STRIP__', strip).replace('__SIZE__', str(size)))
    work = pathlib.Path(tempfile.mkdtemp(prefix='ogcard-'))
    src, raw = work / 'card.html', work / 'raw.png'
    src.write_text(page)
    prof = work / 'profile'
    proc = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                             '--force-device-scale-factor=2', '--window-size=1200,630',
                             f'--user-data-dir={prof}', f'--screenshot={raw}', src.as_uri()],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):                       # writes the file, then never exits
        time.sleep(0.5)
        if raw.exists() and raw.stat().st_size > 0:
            time.sleep(1.5)
            break
    proc.kill()
    subprocess.run(['pkill', '-f', f'user-data-dir={prof}'], check=False)
    if not raw.exists():
        sys.exit('chrome produced no screenshot')
    subprocess.run(['sips', '-z', '630', '1200', str(raw), '--out', str(out)],
                   check=True, stdout=subprocess.DEVNULL)
    shutil.rmtree(work, ignore_errors=True)
    print('wrote', out)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    render(*sys.argv[1:5])

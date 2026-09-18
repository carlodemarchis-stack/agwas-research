#!/usr/bin/env python3
"""Bump the version stamp on the scan page. Usage: python3 bump.py [major|minor|patch] "what changed"."""
import re, sys, json, datetime, pathlib
P=pathlib.Path('/mnt/user-data/outputs/ibc2026-vendor-database.html')
LOG=pathlib.Path('/home/claude/version-log.json')
level=sys.argv[1] if len(sys.argv)>1 else "patch"
note=sys.argv[2] if len(sys.argv)>2 else ""
h=P.read_text()
m=re.search(r'<p class="version" id="version">v\. (\d+)\.(\d+)\.(\d+)', h)
if m: a,b,c=map(int,m.groups())
else: a,b,c=1,0,0
if m:
    if level=="major": a,b,c=a+1,0,0
    elif level=="minor": b,c=b+1,0
    else: c+=1
ver=f"{a}.{b}.{c}"
today=datetime.date.today().strftime("%-d %B %Y")
# the note goes to the log only; the page shows version and date
stamp=f'<p class="version" id="version">v. {ver} \u00b7 updated {today}</p>'
if m:
    h=re.sub(r'<p class="version" id="version">.*?</p>', stamp, h, flags=re.S)
else:
    anchor='<p class="stripnote halls">'
    end=h.index('</p>', h.index(anchor))+4
    h=h[:end]+"\n"+stamp+h[end:]
    h=h.replace(".jump{", """.version{margin:-18px 0 30px;font-family:"Archivo Narrow",sans-serif;font-size:12px;
 letter-spacing:.04em;color:#A8A29A}
.jump{""")
P.write_text(h)
log=json.loads(LOG.read_text()) if LOG.exists() else []
log.append({"version":ver,"date":str(datetime.date.today()),"note":note})
LOG.write_text(json.dumps(log,indent=1))
print(f"v. {ver} \u00b7 {today}" + (f" \u00b7 {note}" if note else ""))

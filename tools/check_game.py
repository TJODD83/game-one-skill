#!/usr/bin/env python3
"""Check a game folder against the live server limits (GET /api/config) before uploading.
   python3 check_game.py my_game/ http://<server>:8787      exit code 1 if anything is over a limit."""
import sys, os, json, re, urllib.request
src, base = sys.argv[1], sys.argv[2].rstrip('/')
L = json.load(urllib.request.urlopen(base + '/api/config'))['experience']
ALLOWED = {'.js', '.json', '.glb', '.vrm', '.png', '.jpg', '.jpeg', '.webp', '.ogg', '.mp3', '.wav', '.txt'}
BANNED = [r'\beval\s*\(', r'new\s+Function', r'\bWebAssembly\b', r'XMLHttpRequest', r'new\s+WebSocket', r'\blocalStorage\b', r'\bsessionStorage\b', r'\bindexedDB\b', r'\bimport\s*\(', r'document\.cookie']
errs, files, total, js = [], 0, 0, 0
if not os.path.exists(os.path.join(src, 'experience.json')): errs.append('experience.json missing at the top level')
else:
    m = json.load(open(os.path.join(src, 'experience.json')))
    if not (1 <= len(m.get('name', '')) <= 48): errs.append('name must be 1-48 characters')
    if not os.path.exists(os.path.join(src, m.get('entry', '-'))): errs.append('entry file missing')
for root, _, fs in os.walk(src):
    for f in fs:
        p = os.path.join(root, f); rel = os.path.relpath(p, src); n = os.path.getsize(p); files += 1; total += n
        if os.path.splitext(f)[1].lower() not in ALLOWED: errs.append(f'{rel}: file type not allowed')
        if not re.fullmatch(r'[A-Za-z0-9_./-]+', rel.replace(os.sep, '/')): errs.append(f'{rel}: path has characters other than letters, digits, _ . / -')
        if n > L['perFileBytes']: errs.append(f'{rel}: {n} bytes > {L["perFileBytes"]}')
        if f.endswith('.js'):
            js += n; t = open(p, encoding='utf8', errors='replace').read()
            for i, line in enumerate(t.split('\n'), 1):
                if len(line) > L['maxLine']: errs.append(f'{rel}:{i}: line of {len(line)} characters > {L["maxLine"]}')
            for b in BANNED:
                if re.search(b, t): errs.append(f'{rel}: uses {b} (refused)')
if files > L['maxFiles']: errs.append(f'{files} files > {L["maxFiles"]}')
if total > L['totalBytes']: errs.append(f'{total} bytes > {L["totalBytes"]}')
if js > L['jsBytes']: errs.append(f'{js} bytes of JavaScript > {L["jsBytes"]}')
print(json.dumps({'ok': not errs, 'files': files, 'bytes': total, 'jsBytes': js, 'errors': errs}, indent=1))
sys.exit(1 if errs else 0)

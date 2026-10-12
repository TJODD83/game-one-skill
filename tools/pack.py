#!/usr/bin/env python3
"""Zip a game folder (experience.json + entry .js at the top level) for upload: python3 pack.py my_game/ my_game.zip"""
import sys, os, zipfile
src, out = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(src):
        for f in files:
            p = os.path.join(root, f); z.write(p, os.path.relpath(p, src).replace(os.sep, '/'))
print(out, os.path.getsize(out), 'bytes')

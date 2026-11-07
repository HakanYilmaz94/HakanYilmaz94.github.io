#!/usr/bin/env python3
"""Tells IndexNow search engines (Bing, which also feeds ChatGPT search and Copilot; Yandex; Seznam…) that pages changed.
Usage: python3 -I tools/indexnow.py https://hyapps.app/page1/ https://hyapps.app/page2/ …   (after the push is live)
       python3 -I tools/indexnow.py --all        (every URL in sitemap.xml)
The key file <key>.txt at the site root proves the site is ours; the key is in tools/indexnow_key.txt.
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
key = open(os.path.join(ROOT, "tools", "indexnow_key.txt")).read().strip()
urls = sys.argv[1:]
if urls == ["--all"]:
    urls = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(ROOT, "sitemap.xml")).read())
if not urls:
    sys.exit(__doc__)
body = json.dumps({"host": "hyapps.app", "key": key, "keyLocation": f"https://hyapps.app/{key}.txt", "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "hyapps-site-tools"})
print(urllib.request.urlopen(req, timeout=30).status, f"({len(urls)} urls)")

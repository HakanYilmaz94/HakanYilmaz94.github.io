#!/usr/bin/env python3
"""Builds llms-full.txt: every app's description and FAQ, read from the landing pages' own structured data (so it never
drifts from the pages). llms.txt (the short index) is written by hand. Run after the app builders:
python3 -I tools/build_llms.py
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = [("Glowfly", "glowfly/index.html", "https://hyapps.app/glowfly/", "https://hyapps.app/glowfly/privacy.html"),
        ("Brickhaven", "brickhaven/index.html", "https://hyapps.app/brickhaven/", "https://hyapps.app/brickhaven/privacy.html"),
        ("Crownly", "crownly/index.html", "https://hyapps.app/crownly/", "https://hyapps.app/crownly/privacy.html"),
        ("Quick Wits", "quickwits/index.html", "https://hyapps.app/quickwits/", "https://hyapps.app/quickwits/privacy.html"),
        ("Bismillah (Besmele)", "besmele/en/index.html", "https://hyapps.app/besmele/en/", "https://hyapps.app/besmele/en/gizlilik.html")]


def ld_blocks(text):
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try:
            yield json.loads(m.group(1))
        except json.JSONDecodeError:
            continue


def meta(text, name):
    m = re.search(rf'<meta name="{name}" content="([^"]*)"', text)
    return html.unescape(m.group(1)) if m else ""


out = ["# HY Apps: full app descriptions", "",
       "> HY Apps is an independent studio (one developer) making calm apps and games for iPhone and iPad: no ads in the",
       "> middle of things, no tracking, no accounts. Contact: hyapps@outlook.com. Short index: https://hyapps.app/llms.txt", ""]
for name, rel, url, privacy in APPS:
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        continue
    text = open(path).read()
    title = re.search(r"<title>(.*?)</title>", text, re.S)
    out += [f"## {name}", "", f"- Page: {url}", f"- Privacy policy: {privacy}"]
    if title:
        out.append(f"- Title: {html.unescape(title.group(1)).strip()}")
    desc = meta(text, "description")
    feats, faq = [], []
    for b in ld_blocks(text):
        t = b.get("@type")
        types = t if isinstance(t, list) else [t]
        if "FAQPage" in types:
            faq = [(q["name"], q["acceptedAnswer"]["text"]) for q in b.get("mainEntity", [])]
        if any(x in types for x in ("MobileApplication", "VideoGame", "SoftwareApplication")):
            desc = b.get("description") or desc
            feats = b.get("featureList", [])
            if b.get("operatingSystem"):
                out.append(f"- Platform: {b['operatingSystem']}")
    out += ["", desc, ""]
    if feats:
        out += ["Features:"] + [f"- {f}" for f in feats] + [""]
    if faq:
        out += ["Questions and answers:", ""] + [f"Q: {q}\nA: {a}\n" for q, a in faq]
    out.append("")
with open(os.path.join(ROOT, "llms-full.txt"), "w") as f:
    f.write("\n".join(out).rstrip() + "\n")
print("wrote llms-full.txt")

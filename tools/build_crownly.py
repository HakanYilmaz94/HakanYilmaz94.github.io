#!/usr/bin/env python3
"""Crownly notice pages (2026-11-25). Crownly was taken off the App Store in every country on 2026-11-23; players who
already have it keep playing. /crownly/ and /crownly/tr/ now tell them that, keep the support e-mail and the privacy
policy, and point to Birbdoku (same studio, the same Queens rules with two cockatiels). noindex: the guides moved to
/birbdoku/ (redirect stubs in build_guides.py). crownly/privacy.html and crownly/duel/ stay as they are.

Usage: python3 -I tools/build_crownly.py
"""
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYTICS = ("<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
             "data-cf-beacon='{\"token\": \"89e9ceae59114244a972f60af4a20851\"}'></script><!-- End Cloudflare Web Analytics -->")
T = {
    "en": dict(path="crownly/index.html", h="Crownly is no longer available for download",
               p=["Crownly was removed from the App Store in November 2026. If you already have it on your iPhone or iPad, you can keep "
                  "playing; your progress stays on your device and in your iCloud.",
                  "Questions or a problem? Write to hyapps@outlook.com."],
               next_h="Try Birbdoku", next_p="From the same studio: the same Queens rules (one in every row, column and color, never "
               "touching) with two cockatiels, a daily puzzle and hints that explain the logic.", next_href="/birbdoku/",
               privacy="Crownly privacy policy", privacy_href="privacy.html", home="/", other="tr/", other_label="Türkçe"),
    "tr": dict(path="crownly/tr/index.html", h="Crownly artık indirilemiyor",
               p=["Crownly Kasım 2026'da App Store'dan kaldırıldı. iPhone ya da iPad'inde zaten varsa oynamaya devam edebilirsin; "
                  "ilerlemen cihazında ve iCloud'unda kalır.",
                  "Bir sorun ya da soru mu var? hyapps@outlook.com adresine yaz."],
               next_h="Birbdoku'yu dene", next_p="Aynı stüdyodan: aynı Queens kuralları (her satıra, sütuna ve renge bir tane, "
               "birbirine değmeden), iki sultan papağanı, günlük bulmaca ve mantığı anlatan ipuçları.", next_href="/birbdoku/tr/",
               privacy="Crownly gizlilik politikası", privacy_href="../privacy.html#tr", home="/tr/", other="../", other_label="English"),
}
for lang, t in T.items():
    e = html.escape
    paras = "".join(f"<p>{e(x)}</p>" for x in t["p"])
    out = f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Crownly</title>
  <meta name="robots" content="noindex, follow">
  <link rel="icon" href="/crownly/img/icon.png">
  <link rel="stylesheet" href="/assets/app.css">
  {ANALYTICS}
</head>
<body>
<article class="article">
  <h1>{e(t["h"])}</h1>
  {paras}
  <div class="cta-card">
    <img src="/birbdoku/img/icon.png" alt="" width="72" height="72">
    <h2>{e(t["next_h"])}</h2>
    <p>{e(t["next_p"])}</p>
    <a class="store" href="{t["next_href"]}">Birbdoku →</a>
  </div>
</article>
<footer class="foot">
  <a href="{t["home"]}">HY Apps</a><a href="{t["privacy_href"]}">{e(t["privacy"])}</a><a href="{t["other"]}">{t["other_label"]}</a>
  <a href="mailto:hyapps@outlook.com">hyapps@outlook.com</a>
</footer>
</body>
</html>
'''
    full = os.path.join(ROOT, t["path"])
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(out)
    print("wrote", t["path"])

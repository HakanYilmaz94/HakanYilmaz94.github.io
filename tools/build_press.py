#!/usr/bin/env python3
"""Builds the press page (EN /press/, TR /tr/press/): who HY Apps is, every app with its facts, links, icon and
screenshots, and how to reach us. For journalists, video makers and AI assistants that need plain facts.

Usage: python3 -I tools/build_press.py   (run from the site repo root; then tools/build_guides.py for the sitemap)
Store links appear only for apps whose builder has LIVE = True (or no LIVE flag, e.g. Besmele).
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESC = html.escape
ANALYTICS = ("<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
             "data-cf-beacon='{\"token\": \"89e9ceae59114244a972f60af4a20851\"}'></script><!-- End Cloudflare Web Analytics -->")
SOC = [("YouTube", "https://www.youtube.com/@hyappsgames"), ("Instagram", "https://www.instagram.com/hyappsgames"),
       ("X", "https://x.com/hyappsgames"), ("TikTok", "https://www.tiktok.com/@hyappsgames")]


def live(app):
    with open(os.path.join(ROOT, "tools", f"build_{app}.py")) as f:
        m = re.search(r"^LIVE = (True|False)", f.read(), re.M)
    return m is None or m.group(1) == "True"


# (builder, App Store id, name, page en, page tr, icon, screenshots folder, facts en, facts tr)
APPS = [
    ("pyramidcraft", "6836529298", "Pyramid Craft: Brick Builder", "/pyramidcraft/", "/pyramidcraft/tr/", "/pyramidcraft/img/icon.png",
     ["/pyramidcraft/img/en-anit.jpg", "/pyramidcraft/img/en-otomasyon.jpg"],
     "First-person pyramid building game for iPhone. Dig Nile mud, mould and dry bricks, lay three monuments (1,240 · 5,456 · 26,235 bricks), hire workers, build ramps, water wheels and conveyor belts. Plays offline.",
     "iPhone için birinci şahıs piramit inşa oyunu. Nil'den çamur çıkar, tuğlaları kalıpla ve kurut, üç anıt ör (1.240 · 5.456 · 26.235 tuğla), işçi tut, rampa, su çarkı ve bant kur. İnternetsiz oynanır."),
    ("glowfly", "6830895618", "Glowfly: Idle Brick Breaker", "/glowfly/", "/glowfly/tr/", "/glowfly/img/icon.png", [],
     "Relaxing idle merge game for iPhone and iPad: fireflies of light break glass walls and reveal a hand-drawn night landscape. 10 chapters, 1,000 nights; keeps playing while closed.",
     "iPhone ve iPad için rahatlatıcı idle birleştirme oyunu: ışık ateşböcekleri cam duvarları kırar ve elle çizilmiş bir gece manzarası açar. 10 bölüm, 1.000 gece; kapalıyken de oynar."),
    ("brickhaven", "6826958666", "Brickhaven: Cozy Brick Builder", "/brickhaven/", "/brickhaven/tr/", "/brickhaven/img/icon.png", [],
     "Cozy first-person building game for iPhone and iPad: rebuild a seaside town one brick at a time. Offline, no timers, no ads.",
     "iPhone ve iPad için rahat, birinci şahıs inşa oyunu: bir sahil kasabasını tuğla tuğla yeniden kur. İnternetsiz, zamanlayıcısız, reklamsız."),
    ("birbdoku", "6837803599", "Birbdoku: Cute Parrot Puzzle", "/birbdoku/", "/birbdoku/tr/", "/birbdoku/img/icon.png",
     ["/birbdoku/img/shots/en-play.jpg", "/birbdoku/img/shots/en-garden.jpg"],
     "Cozy Queens-style logic puzzle for iPhone and iPad with two cockatiels, Pika and Chiko: one bird in every row, column and color, birds never touch. Daily puzzle, hints that teach, streak garden, weekly season.",
     "İki sultan papağanı Pika ve Çiko ile iPhone ve iPad için rahat, Queens tarzı mantık bulmacası: her satıra, sütuna ve renge bir kuş, kuşlar birbirine değmez. Günlük bulmaca, öğreten ipuçları, seri bahçesi, haftalık sezon."),
    ("quickwits", "6826451513", "Quick Wits", "/quickwits/", "/quickwits/tr/", "/quickwits/img/icon.png", [],
     "Party game of quick skill rounds for iPhone: reflex duels, guessing, memory and group games on one phone or in an online room.",
     "iPhone için kısa beceri turlarından oluşan parti oyunu: refleks düelloları, tahmin, hafıza ve grup oyunları; tek telefonda ya da online odada."),
    ("besmele", "6821501310", "Bismillah (Besmele)", "/besmele/en/", "/besmele/", "/besmele/img/icon.png", [],
     "Daily Islamic companion for iPhone: prayer times, the Qur'an with audio, Qibla, a daily verse, hadith, dua and the 99 Names. Free and ad-free.",
     "iPhone için günlük İslami yardımcı: namaz vakitleri, sesli Kur'an, kıble, günün ayeti, hadis, dua ve 99 isim. Ücretsiz ve reklamsız."),
]

T = {
    "en": dict(path="/press/", title="Press kit · HY Apps", h1="Press kit",
               desc="Facts, icons, screenshots and contact for HY Apps, an independent studio making calm games and apps for iPhone and iPad.",
               about_h="About the studio",
               about="HY Apps is an independent studio: one developer who designs, codes and draws every app and game. Our games are calm, "
                     "fair and private: no accounts, no tracking for advertising, everything explained in plain words. Pages and apps are "
                     "in English and Turkish; newer games add German, French, Spanish, Italian, Portuguese, Russian, Japanese, Korean and Chinese.",
               facts=[("Studio", "HY Apps (independent, one developer)"), ("Since", "2026"), ("Platforms", "iPhone, iPad"),
                      ("Website", "hyapps.app"), ("Press and support", "hyapps@outlook.com")],
               apps_h="Games and apps", page="Page", store="App Store", soon="Coming soon", icon="Icon (PNG)", shots="Screenshots",
               use_h="Using our material",
               use="You may use our icons, screenshots and trailers to write about or film our games. For keys, interviews or anything else, write to us.",
               social_h="Follow", contact_h="Contact", contact="Write to hyapps@outlook.com. We answer every message, usually within two days.",
               other="/tr/press/", other_label="Türkçe", home="/"),
    "tr": dict(path="/tr/press/", title="Basın kiti · HY Apps", h1="Basın kiti",
               desc="iPhone ve iPad için sakin oyunlar ve uygulamalar yapan bağımsız stüdyo HY Apps için bilgiler, simgeler, ekran görüntüleri ve iletişim.",
               about_h="Stüdyo hakkında",
               about="HY Apps bağımsız bir stüdyo: her uygulamayı ve oyunu tasarlayan, kodlayan ve çizen tek bir geliştirici. Oyunlarımız "
                     "sakin, adil ve gizliliğe saygılı: hesap yok, reklam için takip yok, her şey sade bir dille anlatılır. Sayfalar ve "
                     "uygulamalar Türkçe ve İngilizce; yeni oyunlarda Almanca, Fransızca, İspanyolca, İtalyanca, Portekizce, Rusça, Japonca, Korece ve Çince de var.",
               facts=[("Stüdyo", "HY Apps (bağımsız, tek geliştirici)"), ("Kuruluş", "2026"), ("Platformlar", "iPhone, iPad"),
                      ("Web sitesi", "hyapps.app"), ("Basın ve destek", "hyapps@outlook.com")],
               apps_h="Oyunlar ve uygulamalar", page="Sayfa", store="App Store", soon="Yakında", icon="Simge (PNG)", shots="Ekran görüntüleri",
               use_h="Materyallerimizi kullanmak",
               use="Oyunlarımız hakkında yazmak ya da video çekmek için simgelerimizi, ekran görüntülerimizi ve fragmanlarımızı kullanabilirsin. Kod, röportaj ya da başka bir şey için bize yaz.",
               social_h="Takip et", contact_h="İletişim", contact="hyapps@outlook.com adresine yaz. Her mesaja, genellikle iki gün içinde cevap veriyoruz.",
               other="/press/", other_label="English", home="/tr/"),
}


def page(lang):
    t = T[lang]
    url = f"https://hyapps.app{t['path']}"
    rows = []
    for app, aid, name, pen, ptr, icon, shots, fen, ftr in APPS:
        p = pen if lang == "en" else ptr
        country = "tr/" if lang == "tr" else ""
        store = (f'<a href="https://apps.apple.com/{country}app/apple-store/id{aid}?pt=129592179&ct=press&mt=8">{t["store"]}</a>'
                 if live(app) else f'<span class="soon">{t["soon"]}</span>')
        shot_links = "".join(f'<a href="{s}">{t["shots"]} {i + 1}</a>' for i, s in enumerate(shots))
        rows.append(f'''  <div class="press-app">
    <img src="{icon}" alt="{ESC(name)}" width="72" height="72">
    <div><h3>{ESC(name)}</h3><p>{ESC(fen if lang == "en" else ftr)}</p>
    <p class="links"><a href="{p}">{t["page"]}</a>{store}<a href="{icon}" download>{t["icon"]}</a>{shot_links}</p></div>
  </div>''')
    facts = "".join(f"<dt>{ESC(k)}</dt><dd>{ESC(v)}</dd>" for k, v in t["facts"])
    soc = "".join(f'<a href="{u}" rel="me">{n}</a>' for n, u in SOC)
    ld = {"@context": "https://schema.org", "@type": "AboutPage", "name": t["title"], "url": url, "inLanguage": lang,
          "description": t["desc"], "about": {"@type": "Organization", "@id": "https://hyapps.app/#org", "name": "HY Apps",
          "url": "https://hyapps.app/", "email": "hyapps@outlook.com", "logo": "https://hyapps.app/assets/apple-touch-icon.png",
          "sameAs": [u for _, u in SOC]}}
    on = lambda l: ' class="on" aria-current="page"' if l == lang else ""
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{ESC(t["title"])}</title>
  <meta name="description" content="{ESC(t["desc"])}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="https://hyapps.app/press/">
  <link rel="alternate" hreflang="tr" href="https://hyapps.app/tr/press/">
  <link rel="alternate" hreflang="x-default" href="https://hyapps.app/press/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{ESC(t["title"])}">
  <meta property="og:description" content="{ESC(t["desc"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://hyapps.app/assets/og/studio-{lang}.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="stylesheet" href="/assets/site.css">
  <link rel="alternate" type="application/rss+xml" title="HY Apps" href="{"/tr/feed.xml" if lang == "tr" else "/feed.xml"}">
  <style>
    .press {{ max-width: 860px; margin: 0 auto; padding: 32px 16px 56px; }}
    .press h1 {{ font-size: 40px; margin: 8px 0 4px; }}
    .press h2 {{ margin: 36px 0 10px; }}
    .press dl {{ display: grid; grid-template-columns: max-content 1fr; gap: 6px 18px; margin: 0; }}
    .press dt {{ font-weight: 800; }} .press dd {{ margin: 0; }}
    .press-app {{ display: flex; gap: 16px; align-items: flex-start; padding: 16px 0; border-bottom: 1px solid rgba(127,127,127,.25); }}
    .press-app img {{ border-radius: 16px; flex: none; }}
    .press-app h3 {{ margin: 0 0 4px; }} .press-app p {{ margin: 0 0 6px; }}
    .press .links a, .press .links .soon, .press .social a {{ margin-right: 14px; font-weight: 700; }}
    .press .soon {{ opacity: .6; }}
    .press .top {{ display: flex; justify-content: space-between; align-items: center; }}
  </style>
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  {ANALYTICS}
</head>
<body>
<main class="press">
  <div class="top"><a href="{t["home"]}">HY Apps</a>
    <span class="lang"><a href="/press/" hreflang="en" lang="en"{on("en")}>EN</a><a href="/tr/press/" hreflang="tr" lang="tr"{on("tr")}>TR</a></span></div>
  <h1>{ESC(t["h1"])}</h1>
  <p>{ESC(t["desc"])}</p>
  <h2>{ESC(t["about_h"])}</h2>
  <p>{ESC(t["about"])}</p>
  <dl>{facts}</dl>
  <h2>{ESC(t["apps_h"])}</h2>
{chr(10).join(rows)}
  <h2>{ESC(t["use_h"])}</h2>
  <p>{ESC(t["use"])}</p>
  <h2>{ESC(t["social_h"])}</h2>
  <p class="social">{soc}</p>
  <h2>{ESC(t["contact_h"])}</h2>
  <p><a href="mailto:hyapps@outlook.com">{ESC(t["contact"])}</a></p>
</main>
<footer class="studio-foot"><a href="{t["home"]}">HY Apps</a><a href="{t["other"]}">{t["other_label"]}</a><p>© 2026 HY Apps</p></footer>
</body>
</html>
'''


for lang, rel in (("en", "press/index.html"), ("tr", "tr/press/index.html")):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(page(lang))
    print("wrote", rel)

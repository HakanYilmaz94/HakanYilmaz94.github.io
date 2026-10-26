#!/usr/bin/env python3
"""Builds the Quick Wits (Kıvrak Zeka in Turkish) landing pages (EN + TR) from one template.

Usage: python3 -I tools/build_quickwits.py   (run from the site repo root)
Writes quickwits/index.html and quickwits/tr/index.html. Shares assets/app.css with Crownly.
Until the app is on the App Store, LIVE is False: the store button is a "coming soon" badge.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ID = "6826451513"
LIVE = False

T = {
    "en": dict(
        lang="en", path="/quickwits/", img="img/", other_lang="tr", other_href="tr/", other_label="Türkçe",
        name="Quick Wits",
        store=f"https://apps.apple.com/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Quick Wits · Party Games & Reaction Games with Friends (iPhone)",
        desc="Quick Wits is a party game of quick skill rounds for iPhone: reflex duels, guessing, memory and group games. "
             "Play solo, pass one phone around, or open an online room where everyone plays on their own phone.",
        og_desc="Quick skill games with friends: reflex duels, guessing, memory and group games.",
        nav_features="Features", nav_support="Support", privacy_href="privacy.html",
        eyebrow="A party game for iPhone",
        h1="Who has the <em>quickest wits</em> at the table?",
        lead="87 short skill games, 1,000 points a round. Out-draw your friends, count flashing dots, keep the beat, find cities on the map and guess what the group will pick.",
        cta="Download on the App Store", soon="Coming soon to the App Store", cta_note="Free · iPhone · iOS 17+",
        marquee=["87 mini games", "Pass the phone", "Online rooms", "Up to 12 players", "Daily challenge",
                 "Reflex duels", "Group games", "English & Türkçe"],
        rules_kicker="Three ways to play", rules_h="One phone or everyone's.",
        rules=["Solo: beat your own best score, any time.",
               "Pass the phone: one iPhone, taking turns. Up to 4 players free, up to 8 with the Party Pack.",
               "Online room: everyone joins with a 4-letter code or an invite link and plays at once. Up to 4 free, up to 12 with the Party Pack."],
        rules_note="Every phone builds exactly the same round from a shared seed, so nobody gets an easier question.",
        rules_shot=("turn", "Pass the phone to the next player"),
        features=[
            ("game", "87 mini games", "Quick to learn. Hard to master.",
             "Reflex duels, colour traps, optical illusions, estimates, a world map, billiards and tower physics, memory tests, rhythm and sound games, little detective cases, and games that use the phone itself: tilt it, blow into it, count the buzzes. Each round takes seconds."),
            ("scores", "Group games", "Read the room.",
             "Some games are scored against the whole table: pick what most people pick, find the lowest number nobody else chose, or land on the group's wavelength."),
            ("home", "Daily challenge", "Five games. Same for everyone. Every day.",
             "A new five-game challenge every day, one try each. Build a streak and compare your score on the Game Center leaderboard."),
        ],
        stats=[("87", "mini games"), ("12", "players online"), ("1,000", "points a round"), ("0", "ads in a party")],
        fair_h="Fair by design.",
        fair="Timing is measured on your own phone, so a slow connection never costs you points. No ads in the middle of a party, no tracking, no account needed.",
        support_h="Support",
        contact="Found a bug, have an idea for a game or a question? Write to us at {mail}.",
        faq=[
            ("How many players can play?",
             "Solo, or up to 4 players for free, passing one phone or in an online room. With the Party Pack: up to 8 on one phone and up to 12 in an online room. Group games (Crowd Mind, Lowest Unique, Two Thirds, Same Wavelength) need at least 3 players."),
            ("Is it free?",
             "Solo play is free with all 87 games, and so are the daily challenge and statistics. With friends, 25 games are free each week (12 favourites plus 13 that change every Monday), for up to 4 players and as many matches as you like. No ads, no subscription. The Party Pack is a one-time purchase that opens all 87 games to groups, up to 8 players on one phone and 12 in an online room. In a room the host's pack is enough. Family Sharing is on."),
            ("Does everyone need the app?",
             "For pass-the-phone, only one phone needs it. For an online room, everyone plays on their own phone, so everyone needs Quick Wits."),
            ("Do I need an internet connection?",
             "Solo, pass-the-phone and the daily challenge work offline, except Map Pin, which needs the internet to load the map. Online rooms need a connection."),
            ("What if my phone drops out of an online room?",
             "Open the app and join with the same code: you get your seat back and continue from the current round. The host can also choose not to wait."),
            ("When does the daily challenge change?",
             "Every day at 07:00 UTC, the same moment everywhere, so everyone plays the same five games and rounds and shares one leaderboard."),
        ],
        final_h="Gather your friends.",
        footer_privacy="Privacy policy", made="Made with care by an independent developer.",
        alts=dict(home="Quick Wits home screen with the daily challenge", game="A Higher or Lower round",
                  turn="Pass the phone to the next player", scores="Scores after a group game"),
    ),
    "tr": dict(
        lang="tr", path="/quickwits/tr/", img="../img/", other_lang="en", other_href="../", other_label="English",
        name="Kıvrak Zeka",
        store=f"https://apps.apple.com/tr/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Kıvrak Zeka · Arkadaşlarla Parti ve Refleks Oyunları (iPhone)",
        desc="Kıvrak Zeka, iPhone için kısa yetenek turlarından oluşan bir parti oyunu: refleks düelloları, tahmin, hafıza ve grup oyunları. "
             "Tek başına oyna, telefonu elden ele dolaştır ya da herkesin kendi telefonunda oynadığı online oda aç.",
        og_desc="Arkadaşlarla kısa yetenek oyunları: refleks düelloları, tahmin, hafıza ve grup oyunları.",
        nav_features="Özellikler", nav_support="Destek", privacy_href="../privacy.html#tr",
        eyebrow="iPhone için bir parti oyunu",
        h1="Masadaki en <em>kıvrak zeka</em> kim?",
        lead="87 kısa yetenek oyunu, tur başına 1.000 puan. Düelloda arkadaşından hızlı ol, parlayan noktaları say, ritmi tut, şehirleri haritada bul, grubun ne seçeceğini tahmin et.",
        cta="App Store'dan indir", soon="Yakında App Store'da", cta_note="Ücretsiz · iPhone · iOS 17+",
        marquee=["87 mini oyun", "Telefonu pasla", "Online oda", "12 oyuncuya kadar", "Günlük meydan okuma",
                 "Refleks düelloları", "Grup oyunları", "Türkçe ve İngilizce"],
        rules_kicker="Üç oyun şekli", rules_h="Tek telefon ya da herkesinki.",
        rules=["Tek başına: kendi rekorunu kır, istediğin zaman.",
               "Telefonu pasla: tek iPhone, sırayla. 4 kişiye kadar ücretsiz, Parti Paketi ile 8 kişi.",
               "Online oda: herkes 4 harfli kodla ya da davet bağlantısıyla katılır, aynı anda oynar. 4 kişiye kadar ücretsiz, Parti Paketi ile 12 kişi."],
        rules_note="Her telefon aynı turu ortak bir tohumdan birebir aynı üretir; kimseye daha kolay soru düşmez.",
        rules_shot=("turn", "Telefonu sıradaki oyuncuya ver"),
        features=[
            ("game", "87 mini oyun", "Öğrenmesi kolay. Ustalaşması zor.",
             "Refleks düelloları, renk tuzağı, göz yanılmaları, tahminler, dünya haritası, bilardo ve kule fiziği, hafıza testleri, ritim ve ses oyunları, küçük dedektiflik vakaları ve telefonun kendisini kullanan oyunlar: eğ, üfle, titreşimleri say. Her tur birkaç saniye sürer."),
            ("scores", "Grup oyunları", "Masayı oku.",
             "Bazı oyunlar tüm masaya göre puanlanır: çoğunluğun seçeceğini seç, kimsenin seçmediği en küçük sayıyı bul ya da grubun frekansını yakala."),
            ("home", "Günlük meydan okuma", "Beş oyun. Herkese aynı. Her gün.",
             "Her gün yeni bir beş oyunluk meydan okuma, tek hak. Serini büyüt, puanını Game Center sıralamasında karşılaştır."),
        ],
        stats=[("87", "mini oyun"), ("12", "online oyuncu"), ("1.000", "tur başına puan"), ("0", "partide reklam")],
        fair_h="Adil tasarım.",
        fair="Süre senin telefonunda ölçülür; yavaş bağlantı sana puan kaybettirmez. Parti ortasında reklam yok, izleme yok, hesap gerekmez.",
        support_h="Destek",
        contact="Bir hata buldun, bir oyun fikrin ya da sorun mu var? {mail} adresine yaz.",
        faq=[
            ("Kaç kişi oynayabilir?",
             "Tek başına ya da tek telefonu dolaştırarak veya online odada 4 kişiye kadar ücretsiz. Parti Paketi ile tek telefonda 8, online odada 12 kişiye kadar. Grup oyunları (Çoğunluk, En Küçük Tek, Üçte İki, Aynı Frekans) en az 3 oyuncu ister."),
            ("Ücretsiz mi?",
             "Tek başına 87 oyunun hepsi ücretsiz; günlük meydan okuma ve istatistikler de. Arkadaşlarla her hafta 25 oyun ücretsiz (12 sevilen oyun ve her pazartesi değişen 13 oyun), 4 kişiye kadar ve istediğin kadar maç. Reklam ve abonelik yok. Parti Paketi tek seferlik bir satın alma: arkadaşlarla 87 oyunun hepsini, tek telefonda 8, online odada 12 kişiyi açar. Odada ev sahibinin paketi yeterli. Aile Paylaşımı açık."),
            ("Herkesin uygulamayı indirmesi gerekiyor mu?",
             "Telefonu pasla modunda yalnız bir telefon yeter. Online odada herkes kendi telefonunda oynadığı için herkeste Kıvrak Zeka olmalı."),
            ("İnternet gerekiyor mu?",
             "Tek başına, telefonu pasla ve günlük meydan okuma internetsiz çalışır; yalnız Haritada Bul haritayı yüklemek için internet ister. Online oda bağlantı gerektirir."),
            ("Online odada telefonum düşerse ne olur?",
             "Uygulamayı açıp aynı kodla katıl: yerin geri gelir ve kaldığın turdan devam edersin. Ev sahibi beklemeden devam etmeyi de seçebilir."),
            ("Günlük meydan okuma ne zaman değişir?",
             "Her gün 07:00 UTC'de (Türkiye saatiyle 10:00), her yerde aynı anda; böylece herkes aynı beş oyunu ve turları oynar, sıralama tek."),
        ],
        final_h="Arkadaşlarını topla.",
        footer_privacy="Gizlilik politikası", made="Bağımsız bir geliştirici tarafından özenle yapıldı.",
        alts=dict(home="Kıvrak Zeka ana ekranı ve günlük meydan okuma", game="Bir Hangisi Büyük turu",
                  turn="Telefonu sıradaki oyuncuya ver", scores="Grup oyunundan sonra puan tablosu"),
    ),
}

MORE = {
    "en": ("More from HY Apps", "/crownly/", "/crownly/img/icon.png", "Crownly",
           "A calm daily logic puzzle. One crown in every row, column and region.", "All apps", "/"),
    "tr": ("HY Apps'in diğer uygulamaları", "/crownly/tr/", "/crownly/img/icon.png", "Crownly",
           "Sakin bir günlük mantık bulmacası. Her satıra, sütuna ve bölgeye bir taç.", "Tüm uygulamalar", "/tr/"),
}


def phone(src, alt, cls=""):
    return (f'<div class="phone {cls}"><div class="screen"><img src="{src}" alt="{html.escape(alt)}" '
            f'width="500" height="1086" loading="lazy" decoding="async"></div></div>')


def store_button(t):
    if LIVE:
        return f'<a class="store" href="{html.escape(t["store"])}">{html.escape(t["cta"])}</a>'
    return f'<span class="store" aria-disabled="true">{html.escape(t["soon"])}</span>'


def faq_ld(t):
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'


def more(t):
    h, href, icon, name, desc, all_label, all_href = MORE[t["lang"]]
    return f'''  <section class="more reveal">
    <p class="kicker">{html.escape(h)}</p>
    <a class="more-app" href="{href}"><img src="{icon}" alt="" width="64" height="64">
      <span><strong>{html.escape(name)}</strong><span>{html.escape(desc)}</span></span><b aria-hidden="true">→</b></a>
    <a class="more-all" href="{all_href}">{html.escape(all_label)} →</a>
  </section>'''


def lang_switch(t):
    en = "./" if t["lang"] == "en" else "../"
    tr = "tr/" if t["lang"] == "en" else "./"
    on = lambda l: ' class="on" aria-current="page"' if t["lang"] == l else ""
    return (f'<span class="lang"><a href="{en}" hreflang="en" lang="en"{on("en")}>EN</a>'
            f'<a href="{tr}" hreflang="tr" lang="tr"{on("tr")}>TR</a></span>')


def page(t):
    i = t["img"]
    a = t["alts"]
    shot = lambda key: i + t["lang"] + "-" + key + ".jpg"
    mail = f'<a href="mailto:hyapps@outlook.com?subject={t["name"]}">hyapps@outlook.com</a>'
    marquee = "".join(f"<span>{html.escape(m)}</span><b>⚡</b>" for m in t["marquee"])
    rules = "".join(f'<li><span class="num">{n + 1}</span>{html.escape(r)}</li>' for n, r in enumerate(t["rules"]))
    feats = []
    for n, (key, kicker, h, body) in enumerate(t["features"]):
        side = "" if n % 2 else "flip"
        feats.append(f'''
  <section class="feature {side} reveal">
    <div class="feature-media">{phone(shot(key), a[key], "tilt")}</div>
    <div class="feature-text">
      <p class="kicker">{html.escape(kicker)}</p>
      <h2>{html.escape(h)}</h2>
      <p>{html.escape(body)}</p>
    </div>
  </section>''')
    stats = "".join(f'<div><strong>{s}</strong><span>{html.escape(l)}</span></div>' for s, l in t["stats"])
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(ans)}</p></details>" for q, ans in t["faq"])
    canonical = f"https://hyapps.app{t['path']}"
    itunes = f'\n  <meta name="apple-itunes-app" content="app-id={APP_ID}">' if LIVE else ""
    return f'''<!doctype html>
<html lang="{t["lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(t["title"])}</title>
  <meta name="description" content="{html.escape(t["desc"])}">
  <meta name="theme-color" content="#17123a">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en" href="https://hyapps.app/quickwits/">
  <link rel="alternate" hreflang="tr" href="https://hyapps.app/quickwits/tr/">
  <link rel="alternate" hreflang="x-default" href="https://hyapps.app/quickwits/">{itunes}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(t["title"])}">
  <meta property="og:description" content="{html.escape(t["og_desc"])}">
  <meta property="og:image" content="https://hyapps.app/assets/og/quickwits-{t["lang"]}.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(t["title"])}">
  <meta name="twitter:description" content="{html.escape(t["og_desc"])}">
  <meta property="og:url" content="{canonical}">
  <link rel="icon" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="stylesheet" href="/assets/app.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"MobileApplication","name":"{t["name"]}","operatingSystem":"iOS 17 or later",
   "applicationCategory":"GameApplication","url":"{canonical}","inLanguage":"{t["lang"]}",
   "offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}},
   "publisher":{{"@type":"Organization","name":"HY Apps","url":"https://hyapps.app/"}}}}
  </script>
{faq_ld(t)}
  <!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "89e9ceae59114244a972f60af4a20851"}}'></script><!-- End Cloudflare Web Analytics -->
</head>
<body id="top">

<header class="bar">
  <a class="brand" href="./#top"><img src="{i}icon.png" alt="" width="28" height="28">{t["name"]}</a>
  <nav>
    <a href="#features">{t["nav_features"]}</a>
    <a href="#support">{t["nav_support"]}</a>
    {lang_switch(t)}
  </nav>
</header>

<section class="hero">
  <div class="blobs" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
  <div class="hero-copy">
    <img class="hero-icon" src="{i}icon.png" alt="{t["name"]}" width="96" height="96">
    <p class="eyebrow">{html.escape(t["eyebrow"])}</p>
    <h1>{t["h1"]}</h1>
    <p class="lead">{html.escape(t["lead"])}</p>
    {store_button(t)}
    <p class="cta-note">{html.escape(t["cta_note"])}</p>
  </div>
  <div class="stage" id="stage" aria-hidden="false">
    {phone(shot("game"), a["game"], "side left")}
    {phone(shot("home"), a["home"], "center")}
    {phone(shot("scores"), a["scores"], "side right")}
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="track">{marquee}{marquee}</div></div>

<main id="features">
  <section class="rules reveal">
    <div class="rules-text">
      <p class="kicker">{html.escape(t["rules_kicker"])}</p>
      <h2>{html.escape(t["rules_h"])}</h2>
      <ol>{rules}</ol>
      <p class="muted">{html.escape(t["rules_note"])}</p>
    </div>
    <div class="feature-media">{phone(shot(t["rules_shot"][0]), t["rules_shot"][1], "tilt")}</div>
  </section>
{"".join(feats)}

  <section class="stats reveal">{stats}</section>

  <section class="fair reveal">
    <h2>{html.escape(t["fair_h"])}</h2>
    <p>{html.escape(t["fair"])}</p>
  </section>

  <section class="support reveal" id="support">
    <h2>{html.escape(t["support_h"])}</h2>
    <div class="card"><p>{t["contact"].format(mail=mail)}</p></div>
    {faq}
  </section>
{more(t)}
</main>

<section class="final">
  <div class="blobs" aria-hidden="true"><i></i><i></i><i></i></div>
  <img src="{i}icon.png" alt="" width="88" height="88">
  <h2>{html.escape(t["final_h"])}</h2>
  {store_button(t)}
</section>

<footer class="foot">
  <a href="/">HY Apps</a><a href="{t["privacy_href"]}">{t["footer_privacy"]}</a>
  <a href="{t["other_href"]}" lang="{t["other_lang"]}">{t["other_label"]}</a><a href="mailto:hyapps@outlook.com">hyapps@outlook.com</a>
  <p>{html.escape(t["made"])} © 2026 HY Apps</p>
</footer>
<script src="/assets/app.js" defer></script>
</body>
</html>
'''


def join_page():
    """Where a room invite link lands when the app does not open it: the code, an open button, the store."""
    en, tr = T["en"], T["tr"]
    store = lambda t: (f'<a class="store" href="{html.escape(t["store"])}">{html.escape(t["cta"])}</a>' if LIVE
                       else f'<span class="store off">{html.escape(t["soon"])}</span>')
    itunes = f'\n  <meta name="apple-itunes-app" content="app-id={APP_ID}">' if LIVE else ""
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Join a Quick Wits room</title>
  <meta name="robots" content="noindex">
  <meta name="theme-color" content="#17123a">{itunes}
  <link rel="icon" href="/quickwits/img/icon.png">
  <style>
    body {{ margin: 0; min-height: 100vh; display: grid; place-items: center; background: #17123a; color: #fff;
      font: 17px/1.45 ui-rounded, -apple-system, system-ui, sans-serif; text-align: center; }}
    main {{ padding: 32px 20px; max-width: 420px; }}
    img {{ border-radius: 22px; }}
    h1 {{ font-size: 26px; margin: 18px 0 6px; }}
    p {{ color: #b9b3d9; margin: 0 0 14px; }}
    .code {{ font-size: 56px; font-weight: 900; letter-spacing: 10px; color: #ffc93c; margin: 8px 0 18px; }}
    a.open, .store {{ display: block; padding: 16px; border-radius: 18px; font-weight: 800; text-decoration: none; margin: 10px 0; }}
    a.open {{ background: #ffc93c; color: #17123a; }}
    .store {{ background: rgba(255,255,255,.1); color: #fff; }}
    .off {{ opacity: .6; }}
    [data-lang] {{ display: none; }}
    html[lang=en] [data-lang=en], html[lang=tr] [data-lang=tr] {{ display: block; }}
  </style>
</head>
<body>
<main>
  <img src="/quickwits/img/icon.png" alt="" width="88" height="88">
  <div data-lang="en"><h1>You're invited to a Quick Wits room</h1><p>Room code</p></div>
  <div data-lang="tr"><h1>Kıvrak Zeka odasına davetlisin</h1><p>Oda kodu</p></div>
  <div class="code" id="code">····</div>
  <div data-lang="en">
    <a class="open" id="open-en" href="quickwits://join">Open in Quick Wits</a>
    {store(en)}
    <p>No app yet? Install it, open it, tap Online room and enter the code.</p>
  </div>
  <div data-lang="tr">
    <a class="open" id="open-tr" href="quickwits://join">Kıvrak Zeka'da aç</a>
    {store(tr)}
    <p>Uygulama yok mu? Yükle, aç, Online oda'ya dokun ve kodu gir.</p>
  </div>
</main>
<script>
  const code = (new URLSearchParams(location.search).get("code") || "").toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 4);
  if ((navigator.language || "").toLowerCase().startsWith("tr")) document.documentElement.lang = "tr";
  if (code.length === 4) {{
    document.getElementById("code").textContent = code;
    for (const id of ["open-en", "open-tr"]) document.getElementById(id).href = "quickwits://join?code=" + code;
  }}
</script>
  <!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "89e9ceae59114244a972f60af4a20851"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
'''


for key, out in (("en", "quickwits/index.html"), ("tr", "quickwits/tr/index.html")):
    path = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(page(T[key]))
    print("wrote", out)

os.makedirs(os.path.join(ROOT, "quickwits/join"), exist_ok=True)
with open(os.path.join(ROOT, "quickwits/join/index.html"), "w") as f:
    f.write(join_page())
print("wrote quickwits/join/index.html")

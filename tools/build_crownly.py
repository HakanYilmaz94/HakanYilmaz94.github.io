#!/usr/bin/env python3
"""Builds the Crownly landing pages (EN + TR) from one template.

Usage: python3 -I tools/build_crownly.py   (run from the site repo root)
Writes crownly/index.html and crownly/tr/index.html.
"""
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ID = "6822852151"

T = {
    "en": dict(
        lang="en", path="/crownly/", img="img/", other_lang="tr", other_href="tr/", other_label="Türkçe",
        store=f"https://apps.apple.com/app/id{APP_ID}",
        title="Crownly · Daily Queens Logic Puzzle for iPhone",
        desc="Crownly is a calm daily logic puzzle for iPhone. Place one crown in every row, column and region. "
             "A new puzzle every day, 2,000 levels, hints that explain the logic, color-blind mode. No ads, works offline.",
        og_desc="A calm daily logic puzzle. One crown in every row, column and region.",
        nav_features="Features", nav_support="Support", nav_privacy="Privacy", privacy_href="privacy.html",
        eyebrow="A little logic game for iPhone",
        h1="One crown.<br>Every row, every column, <em>every region.</em>",
        lead="Crownly is a calm daily logic puzzle with hints that explain the logic, not the answer.",
        cta="Download on the App Store", cta_note="Free · iPhone · iOS 17+",
        marquee=["New puzzle every day", "2,000 levels", "Hints that teach", "Color-blind friendly", "No ads",
                 "Works offline", "Lo-fi music", "12 languages"],
        rules_kicker="How to play", rules_h="Three rules. Pure logic.",
        rules=["One crown in every row and every column.", "One crown in every colored region.",
               "Crowns never touch, not even diagonally."],
        rules_note="Tap once for a dot, twice for a crown, or drag to mark many cells. Every puzzle has exactly one solution, so you never have to guess.",
        board_label="A 5×5 Crownly puzzle solving itself",
        features=[
            ("hint", "Hints that teach", "Stuck? Hints don't spoil.",
             "A built-in solver finds the next logical step and explains why it works, in plain words. Ask once to see the idea, again to see the cells."),
            ("home", "A daily ritual", "One new puzzle. Every day. For everyone.",
             "The same daily puzzle for the whole world, plus a 10×10 Daily Hard for the brave. Build your streak; a streak freeze saves you on busy days."),
            ("levels", "2,000 levels", "From your first crown to Expert.",
             "Easy, Medium, Hard and Expert boards from 6×6 to 10×10. Solve without hints and beat the clock to earn three stars."),
            ("school", "Logic School", "Learn every technique.",
             "Six short interactive lessons teach the tricks that solve any board, one step at a time."),
            ("dark", "Made for everyone", "Color is never required.",
             "Color-blind mode adds a symbol to every region and bolder borders. Dark mode, larger text and Reduce Motion are fully supported."),
            ("solved", "Celebrate", "See how you did today.",
             "Game Center leaderboards, 16 achievements, Home and Lock Screen widgets, and a spoiler-free card to share your time."),
        ],
        stats=[("2,000", "levels"), ("12", "languages"), ("0", "ads"), ("1", "new puzzle a day")],
        fair_h="Fair by design.",
        fair="The daily puzzles are always free. No ads in the middle of a game, no tracking, works offline. One optional, one-time Crownly Pro purchase unlocks every level, unlimited hints and the puzzle archive.",
        support_h="Support",
        contact="Found a bug, have an idea or a question? Write to us at {mail}. In the app you can also use <em>Settings → Send feedback</em>, which adds your app version and device for us.",
        faq=[
            ("When does the daily puzzle change?",
             "A new daily puzzle appears every day at 07:00 UTC, at the same moment for everyone in the world."),
            ("Will I lose my progress if I change phones?",
             "With iCloud sync turned on (Settings → General), your solved puzzles, stars and streak sync to your other devices through your private iCloud account. Without iCloud, progress is stored only on this device and deleting the app deletes it."),
            ("How do I restore Crownly Pro?",
             "Open Settings → Crownly Pro → Restore purchases while signed in with the Apple Account you used to buy it. Pro is shared with your Family Sharing group."),
            ("I missed a day. Is my streak gone?",
             "Not always. A streak freeze is used automatically when you miss a day (one per month, three with Pro)."),
            ("Some colors look alike to me.",
             "Turn on Color-blind mode in Settings → Game. Every region gets its own symbol and the borders get bolder, so you never need to tell colors apart. You can also try the High contrast board palette."),
        ],
        final_h="Today's puzzle is waiting.",
        footer_privacy="Privacy policy", made="Made with care by an independent developer.",
        alts=dict(home="Crownly home screen with the daily puzzle", hard="The 10×10 Daily Hard puzzle",
                  hint="A hint explaining the next logical step", levels="Level list with stars",
                  school="Logic School lessons", dark="Dark mode with color-blind symbols",
                  solved="Daily puzzle solved celebration"),
    ),
    "tr": dict(
        lang="tr", path="/crownly/tr/", img="../img/", other_lang="en", other_href="../", other_label="English",
        store=f"https://apps.apple.com/tr/app/id{APP_ID}",
        title="Crownly · Günlük Queens Mantık Bulmacası (iPhone)",
        desc="Crownly, iPhone için sakin bir günlük mantık bulmacası. Her satıra, sütuna ve renkli bölgeye bir taç koy. "
             "Her gün yeni bulmaca, 2.000 seviye, mantığı açıklayan ipuçları, renk körü modu. Reklam yok, internetsiz oynanır.",
        og_desc="Sakin bir günlük mantık bulmacası. Her satıra, sütuna ve bölgeye bir taç.",
        nav_features="Özellikler", nav_support="Destek", nav_privacy="Gizlilik", privacy_href="../privacy.html#tr",
        eyebrow="iPhone için küçük bir mantık oyunu",
        h1="Tek taç.<br>Her satır, her sütun, <em>her bölge.</em>",
        lead="Crownly, cevabı değil mantığı anlatan ipuçlarıyla sakin bir günlük bulmaca.",
        cta="App Store'dan indir", cta_note="Ücretsiz · iPhone · iOS 17+",
        marquee=["Her gün yeni bulmaca", "2.000 seviye", "Öğreten ipuçları", "Renk körü dostu", "Reklam yok",
                 "İnternetsiz oynanır", "Lo-fi müzik", "12 dil"],
        rules_kicker="Nasıl oynanır", rules_h="Üç kural. Saf mantık.",
        rules=["Her satırda ve her sütunda bir taç.", "Her renkli bölgede bir taç.",
               "Taçlar birbirine dokunmaz, çapraz da olsa."],
        rules_note="Bir dokunuş nokta, iki dokunuş taç; sürükleyerek birçok hücreyi işaretle. Her bulmacanın tek çözümü var, hiç tahmin etmen gerekmez.",
        board_label="Kendi kendine çözülen 5×5 Crownly bulmacası",
        features=[
            ("hint", "Öğreten ipuçları", "Takıldın mı? İpucu cevabı söylemez.",
             "Yerleşik çözücü sıradaki mantıklı adımı bulur ve neden işe yaradığını sade bir dille anlatır. Bir kez sor fikri gör, bir daha sor hücreleri gör."),
            ("home", "Günlük ritüel", "Her gün yeni bir bulmaca. Herkese aynı.",
             "Tüm dünyaya aynı günün bulmacası ve cesurlar için 10×10 Günlük Zor. Serini büyüt; yoğun günlerde seri dondurma seni korur."),
            ("levels", "2.000 seviye", "İlk tacından Uzman'a.",
             "6×6'dan 10×10'a Kolay, Orta, Zor ve Uzman tahtalar. İpucusuz ve süreyi geçmeden çöz, üç yıldızı kap."),
            ("school", "Mantık okulu", "Her tekniği öğren.",
             "Altı kısa, etkileşimli ders her tahtayı çözen püf noktalarını adım adım öğretir."),
            ("dark", "Herkes için", "Renkleri ayırt etmen gerekmez.",
             "Renk körü modu her bölgeye bir sembol ve kalın sınırlar ekler. Koyu tema, büyük yazı ve Hareketi azalt tam desteklenir."),
            ("solved", "Kutla", "Bugün nasıl geçti, gör.",
             "Game Center sıralamaları, 16 başarım, ana ekran ve kilit ekranı widget'ları, süreni paylaşmak için spoiler'sız kart."),
        ],
        stats=[("2.000", "seviye"), ("12", "dil"), ("0", "reklam"), ("1", "her gün yeni bulmaca")],
        fair_h="Adil olsun diye tasarlandı.",
        fair="Günlük bulmacalar her zaman ücretsiz. Oyunun ortasında reklam yok, takip yok, internetsiz oynanır. İsteğe bağlı, tek seferlik Crownly Pro tüm seviyeleri, sınırsız ipucunu ve bulmaca arşivini açar.",
        support_h="Destek",
        contact="Bir hata mı buldun, bir fikrin ya da sorun mu var? Bize {mail} adresinden yaz. Uygulamada <em>Ayarlar → Geri bildirim gönder</em> de kullanabilirsin; uygulama sürümünü ve cihazını ekler.",
        faq=[
            ("Günün bulmacası ne zaman değişir?",
             "Yeni günlük bulmaca her gün 07:00 UTC'de (Türkiye saatiyle 10:00) dünyanın her yerinde aynı anda çıkar."),
            ("Telefon değiştirirsem ilerlemem kaybolur mu?",
             "iCloud eşitleme açıksa (Ayarlar → Genel) çözdüğün bulmacalar, yıldızların ve serin özel iCloud hesabın üzerinden diğer cihazlarına aktarılır. iCloud kapalıysa ilerlemen yalnız bu cihazda saklanır ve uygulamayı silince silinir."),
            ("Crownly Pro'yu nasıl geri yüklerim?",
             "Satın aldığın Apple hesabıyla giriş yapmışken Ayarlar → Crownly Pro → Satın alımları geri yükle'ye dokun. Pro, Aile Paylaşımı grubunla da paylaşılır."),
            ("Bir günü kaçırdım. Serim gitti mi?",
             "Her zaman değil. Bir günü kaçırınca seri dondurma otomatik kullanılır (ayda bir, Pro ile üç)."),
            ("Bazı renkler bana birbirine benziyor.",
             "Ayarlar → Oyun'dan Renk körü modunu aç. Her bölgeye kendi sembolü eklenir ve sınırlar kalınlaşır; renkleri ayırt etmen gerekmez. Yüksek kontrast tahta paletini de deneyebilirsin."),
        ],
        final_h="Bugünün bulmacası seni bekliyor.",
        footer_privacy="Gizlilik politikası", made="Bağımsız bir geliştirici tarafından özenle yapıldı.",
        alts=dict(home="Günün bulmacası ile Crownly ana sayfası", hard="10×10 Günlük Zor bulmaca",
                  hint="Sıradaki mantıklı adımı anlatan ipucu", levels="Yıldızlı seviye listesi",
                  school="Mantık okulu dersleri", dark="Renk körü sembolleriyle koyu tema",
                  solved="Günün bulmacası çözüldü kutlaması"),
    ),
}

# 5×5 demo board: region letter per cell and the solution (row, col) in reveal order.
BOARD = ["AABBB", "ACCBB", "DCCEB", "DDCEE", "DDEEE"]
CROWNS = [(2, 0), (0, 1), (3, 2), (1, 3), (4, 4)]
REGION_COLOR = {"A": "#CDBEEB", "B": "#B9D3F2", "C": "#F6CFA8", "D": "#C5E0B5", "E": "#F2B8C6"}

CROWN_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 18h18l-1.6-9.2-4.6 3.8L12 5.5 9.2 12.6 4.6 8.8z" '
             'fill="url(#g)" stroke="#8a5a00" stroke-width=".8" stroke-linejoin="round"/><circle cx="12" cy="5" r="1.4" fill="#f4d06f"/>'
             '<circle cx="4.4" cy="8.4" r="1.2" fill="#f4d06f"/><circle cx="19.6" cy="8.4" r="1.2" fill="#f4d06f"/></svg>')


def board_html():
    cells = []
    order = {rc: i for i, rc in enumerate(CROWNS)}
    for r, row in enumerate(BOARD):
        for c, reg in enumerate(row):
            edges = []
            if r == 0 or BOARD[r - 1][c] != reg: edges.append("t")
            if r == 4 or BOARD[r + 1][c] != reg: edges.append("b")
            if c == 0 or BOARD[r][c - 1] != reg: edges.append("l")
            if c == 4 or BOARD[r][c + 1] != reg: edges.append("r")
            cls = " ".join(f"e{e}" for e in edges)
            crown = ""
            if (r, c) in order:
                crown = f'<span class="crown" style="--i:{order[(r, c)]}">{CROWN_SVG}</span>'
            cells.append(f'<div class="cell {cls}" style="background:{REGION_COLOR[reg]}">{crown}</div>')
    return "\n        ".join(cells)


def phone(src, alt, cls=""):
    return (f'<div class="phone {cls}"><div class="screen"><img src="{src}" alt="{html.escape(alt)}" '
            f'width="500" height="1086" loading="lazy" decoding="async"></div></div>')


def page(t):
    i = t["img"]
    a = t["alts"]
    mail = '<a href="mailto:hyapps@outlook.com?subject=Crownly">hyapps@outlook.com</a>'
    marquee = "".join(f"<span>{html.escape(m)}</span><b>♛</b>" for m in t["marquee"])
    rules = "".join(f'<li><span class="num">{n + 1}</span>{html.escape(r)}</li>' for n, r in enumerate(t["rules"]))
    feats = []
    for n, (shot, kicker, h, body) in enumerate(t["features"]):
        side = "flip" if n % 2 else ""
        feats.append(f'''
  <section class="feature {side} reveal">
    <div class="feature-media">{phone(i + t["lang"] + "-" + shot + ".jpg", a[shot], "tilt")}</div>
    <div class="feature-text">
      <p class="kicker">{html.escape(kicker)}</p>
      <h2>{html.escape(h)}</h2>
      <p>{html.escape(body)}</p>
    </div>
  </section>''')
    stats = "".join(f'<div><strong>{s}</strong><span>{html.escape(l)}</span></div>' for s, l in t["stats"])
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(ans)}</p></details>" for q, ans in t["faq"])
    canonical = f"https://hyapps.app{t['path']}"
    return f'''<!doctype html>
<html lang="{t["lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(t["title"])}</title>
  <meta name="description" content="{html.escape(t["desc"])}">
  <meta name="theme-color" content="#2b1a42">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en" href="https://hyapps.app/crownly/">
  <link rel="alternate" hreflang="tr" href="https://hyapps.app/crownly/tr/">
  <link rel="alternate" hreflang="x-default" href="https://hyapps.app/crownly/">
  <meta name="apple-itunes-app" content="app-id={APP_ID}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(t["title"])}">
  <meta property="og:description" content="{html.escape(t["og_desc"])}">
  <meta property="og:image" content="https://hyapps.app/crownly/img/icon.png">
  <meta property="og:url" content="{canonical}">
  <link rel="icon" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="stylesheet" href="/crownly/crownly.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"MobileApplication","name":"Crownly","operatingSystem":"iOS 17 or later",
   "applicationCategory":"GameApplication","url":"{canonical}","installUrl":"{t["store"]}","inLanguage":"{t["lang"]}",
   "offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}},
   "publisher":{{"@type":"Organization","name":"HY Apps","url":"https://hyapps.app/"}}}}
  </script>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4D06F"/><stop offset="1" stop-color="#C08A12"/></linearGradient></defs></svg>

<header class="bar">
  <a class="brand" href="/"><img src="{i}icon.png" alt="" width="28" height="28">Crownly</a>
  <nav>
    <a href="#features">{t["nav_features"]}</a>
    <a href="#support">{t["nav_support"]}</a>
    <a href="{t["other_href"]}" hreflang="{t["other_lang"]}" lang="{t["other_lang"]}">{t["other_label"]}</a>
  </nav>
</header>

<section class="hero">
  <div class="blobs" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
  <div class="hero-copy">
    <img class="hero-icon" src="{i}icon.png" alt="Crownly" width="96" height="96">
    <p class="eyebrow">{html.escape(t["eyebrow"])}</p>
    <h1>{t["h1"]}</h1>
    <p class="lead">{html.escape(t["lead"])}</p>
    <a class="store" href="{t["store"]}">{html.escape(t["cta"])}</a>
    <p class="cta-note">{html.escape(t["cta_note"])}</p>
  </div>
  <div class="stage" id="stage" aria-hidden="false">
    {phone(i + t["lang"] + "-hard.jpg", a["hard"], "side left")}
    {phone(i + t["lang"] + "-home.jpg", a["home"], "center")}
    {phone(i + t["lang"] + "-solved.jpg", a["solved"], "side right")}
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
    <div class="board" role="img" aria-label="{html.escape(t["board_label"])}">
        {board_html()}
    </div>
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
</main>

<section class="final">
  <div class="blobs" aria-hidden="true"><i></i><i></i><i></i></div>
  <img src="{i}icon.png" alt="" width="88" height="88">
  <h2>{html.escape(t["final_h"])}</h2>
  <a class="store" href="{t["store"]}">{html.escape(t["cta"])}</a>
</section>

<footer class="foot">
  <a href="/">HY Apps</a><a href="{t["privacy_href"]}">{t["footer_privacy"]}</a>
  <a href="{t["other_href"]}" lang="{t["other_lang"]}">{t["other_label"]}</a><a href="mailto:hyapps@outlook.com">hyapps@outlook.com</a>
  <p>{html.escape(t["made"])} © 2026 HY Apps</p>
</footer>
<script src="/crownly/crownly.js" defer></script>
</body>
</html>
'''


for key, out in (("en", "crownly/index.html"), ("tr", "crownly/tr/index.html")):
    path = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(page(T[key]))
    print("wrote", out)

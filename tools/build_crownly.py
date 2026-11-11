#!/usr/bin/env python3
"""Builds the Crownly landing pages (EN + TR) from one template.

Usage: python3 -I tools/build_crownly.py   (run from the site repo root)
Writes crownly/index.html and crownly/tr/index.html.
Until the app is on the App Store, LIVE is False: the store button is a "coming soon" badge.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ID = "6822852151"
LIVE = True
# STORE mirrors the app: 1.2 (live 2026-11-11) has Crownly Pro, three games (Crowns, Route, Mosaic), duels and 6,500
# levels. STORE = False was the purchase-free 1.0.1 (200 levels, no Pro); it now only drops Pro from the FAQ and fair text.
STORE = True

T = {
    "en": dict(
        lang="en", path="/crownly/", img="img/", other_lang="tr", other_href="tr/", other_label="Türkçe",
        store=f"https://apps.apple.com/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Crownly · Daily Queens, Route & Mosaic Logic Puzzles",
        desc="Crownly is a calm collection of daily logic puzzles for iPhone and iPad: Crowns (Queens), Route and Mosaic. "
             "A new puzzle in every game every day, live duels with friends, 6,500 levels, hints that explain the logic. No ads, works offline.",
        og_desc="Three calm daily logic puzzles: Crowns, Route and Mosaic. Plus live duels with friends.",
        nav_features="Features", nav_support="Support", nav_privacy="Privacy", privacy_href="privacy.html",
        eyebrow="Daily logic puzzles for iPhone and iPad",
        h1="Three puzzles.<br>One quiet habit, <em>every day.</em>",
        lead="Crownly brings you a daily Crowns, Route and Mosaic puzzle, with hints that explain the logic, not the answer.",
        cta="Download on the App Store", soon="Coming soon to the App Store", cta_note="Free · iPhone & iPad · iOS 17+",
        marquee=["3 daily puzzles", "Crowns · Route · Mosaic", "Live duels", "6,500 levels", "Hints that teach",
                 "Color-blind friendly", "No ads", "Works offline", "12 languages"],
        rules_kicker="How to play Crowns", rules_h="Three rules. Pure logic.",
        rules=["One crown in every row and every column.", "One crown in every colored region.",
               "Crowns never touch, not even diagonally."],
        rules_note="Tap once for a dot, twice for a crown, or drag to mark many cells. Every puzzle has exactly one solution, so you never have to guess.",
        board_label="A 5×5 Crownly puzzle solving itself",
        features=[
            ("home", "A daily ritual", "Three new puzzles. Every day. For everyone.",
             "A daily Crowns, Route and Mosaic puzzle, the same for the whole world, plus a Hard Daily in every game. Solve any one to keep your streak, all three for a Full Day."),
            ("route", "Route", "One line through every cell.",
             "Draw a single path that visits the numbered stops in order and passes through every cell exactly once, without crossing a wall."),
            ("mosaic", "Mosaic", "Split the grid into rectangles.",
             "Every piece holds exactly one number, and the number is its size. Drag from corner to corner and watch the mosaic come together."),
            ("duel", "Live duels", "Race your friends on the same board.",
             "Share a room code and race 2 to 4 friends live on the same Crowns board, with emoji and playful surprises. Or practice against bots any time."),
            ("hint", "Hints that teach", "Stuck? Hints don't spoil.",
             "A built-in solver finds the next logical step and explains why it works, in plain words. Ask once to see the idea, again to see the cells."),
            ("levels", "6,500 levels", "From your first crown to Expert.",
             "Easy to Expert in every game, up to 10×10, plus Double Crowns: two crowns in every row, column and region. Solve without hints and beat the clock for three stars."),
            ("dark", "Made for everyone", "Color is never required.",
             "Color-blind mode adds a symbol to every region and bolder borders. Dark mode, larger text, VoiceOver and Reduce Motion are fully supported."),
        ],
        stats=[("3", "daily puzzles"), ("6,500", "levels"), ("12", "languages"), ("0", "ads")],
        fair_h="Fair by design.",
        fair="The daily puzzles are always free. No ads in the middle of a game, no tracking, works offline. One optional, one-time Crownly Pro purchase unlocks every level, unlimited hints and duels, and the puzzle archive.",
        support_h="Support",
        contact="Found a bug, have an idea or a question? Write to us at {mail}. In the app you can also use <em>Settings → Send feedback</em>, which adds your app version and device for us.",
        faq=[
            ("When do the daily puzzles change?",
             "New daily puzzles appear every day at 07:00 UTC, at the same moment for everyone in the world."),
            ("How do duels work?",
             "Open Duel, create a room and share its code. 2 to 4 friends race live on the same Crowns board; the first to solve it wins. You can also practice against bots without an internet connection."),
            ("Will I lose my progress if I change phones?",
             "With iCloud sync turned on (Settings → General), your solved puzzles, stars and streak sync to your other devices through your private iCloud account. Without iCloud, progress is stored only on this device and deleting the app deletes it."),
            ("What does Crownly Pro add?",
             "All 6,500 levels (the first 50 of every difficulty are free), unlimited hints and duels, the archive of every past daily puzzle and 3 streak freezes a month instead of 1. It is a one-time purchase, shared with your Family Sharing group. To restore it, open Settings → Crownly Pro → Restore purchases."),
            ("I missed a day. Is my streak gone?",
             "Not always. A streak freeze is used automatically when you miss a day (one per month, three with Pro)."),
            ("Some colors look alike to me.",
             "Turn on Color-blind mode in Settings → Game. Every region gets its own symbol and the borders get bolder, so you never need to tell colors apart. You can also try the High contrast board palette."),
        ],
        final_h="Today's puzzles are waiting.",
        footer_privacy="Privacy policy", made="Made with care by an independent developer.",
        alts=dict(home="Crownly home screen with the daily puzzles", hard="The 10×10 Hard Daily Crowns puzzle",
                  route="A Route puzzle with numbered stops", mosaic="A Mosaic puzzle split into rectangles",
                  duel="A live duel with four players on the same board",
                  hint="A hint explaining the next logical step", levels="Level list with stars",
                  dark="Dark mode with color-blind symbols", solved="Daily puzzle solved celebration"),
    ),
    "tr": dict(
        lang="tr", path="/crownly/tr/", img="../img/", other_lang="en", other_href="../", other_label="English",
        store=f"https://apps.apple.com/tr/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Crownly · Günlük Queens, Rota ve Mozaik Bulmacaları",
        desc="Crownly, iPhone ve iPad için sakin günlük mantık bulmacaları: Taçlar (Queens), Rota ve Mozaik. "
             "Her oyunda her gün yeni bulmaca, arkadaşlarınla canlı düello, 6.500 seviye, mantığı açıklayan ipuçları. Reklam yok, internetsiz oynanır.",
        og_desc="Üç sakin günlük mantık bulmacası: Taçlar, Rota ve Mozaik. Bir de arkadaşlarınla canlı düello.",
        nav_features="Özellikler", nav_support="Destek", nav_privacy="Gizlilik", privacy_href="../privacy.html#tr",
        eyebrow="iPhone ve iPad için günlük mantık bulmacaları",
        h1="Üç bulmaca.<br>Her gün sakin <em>bir alışkanlık.</em>",
        lead="Crownly her gün bir Taçlar, bir Rota ve bir Mozaik bulmacası getirir; ipuçları cevabı değil mantığı anlatır.",
        cta="App Store'dan indir", soon="Yakında App Store'da", cta_note="Ücretsiz · iPhone ve iPad · iOS 17+",
        marquee=["Her gün 3 bulmaca", "Taçlar · Rota · Mozaik", "Canlı düello", "6.500 seviye", "Öğreten ipuçları",
                 "Renk körü dostu", "Reklam yok", "İnternetsiz oynanır", "12 dil"],
        rules_kicker="Taçlar nasıl oynanır", rules_h="Üç kural. Saf mantık.",
        rules=["Her satırda ve her sütunda bir taç.", "Her renkli bölgede bir taç.",
               "Taçlar birbirine dokunmaz, çapraz da olsa."],
        rules_note="Bir dokunuş nokta, iki dokunuş taç; sürükleyerek birçok hücreyi işaretle. Her bulmacanın tek çözümü var, hiç tahmin etmen gerekmez.",
        board_label="Kendi kendine çözülen 5×5 Crownly bulmacası",
        features=[
            ("home", "Günlük ritüel", "Her gün üç yeni bulmaca. Herkese aynı.",
             "Tüm dünyaya aynı günün Taçlar, Rota ve Mozaik bulmacası, her oyunda bir de Günlük Zor. Birini çöz serin sürsün, üçünü çöz Tam Gün olsun."),
            ("route", "Rota", "Her hücreden geçen tek çizgi.",
             "Numaralı durakları sırayla dolaşan, her hücreden yalnız bir kez geçen ve duvarları aşmayan tek bir yol çiz."),
            ("mosaic", "Mozaik", "Tahtayı dikdörtgenlere böl.",
             "Her parçada tam bir sayı olur ve sayı parçanın büyüklüğüdür. Köşeden köşeye sürükle, mozaiğin tamamlanışını izle."),
            ("duel", "Canlı düello", "Arkadaşlarınla aynı tahtada yarış.",
             "Oda kodunu paylaş, 2–4 arkadaşınla aynı Taçlar tahtasında canlı yarış; emojiler ve eğlenceli sürprizler de var. Ya da istediğin zaman botlarla antrenman yap."),
            ("hint", "Öğreten ipuçları", "Takıldın mı? İpucu cevabı söylemez.",
             "Yerleşik çözücü sıradaki mantıklı adımı bulur ve neden işe yaradığını sade bir dille anlatır. Bir kez sor fikri gör, bir daha sor hücreleri gör."),
            ("levels", "6.500 seviye", "İlk tacından Uzman'a.",
             "Her oyunda Kolay'dan Uzman'a, 10×10'a kadar; bir de Çift Taç: her satırda, sütunda ve bölgede iki taç. İpucusuz ve süreyi geçmeden çöz, üç yıldızı kap."),
            ("dark", "Herkes için", "Renkleri ayırt etmen gerekmez.",
             "Renk körü modu her bölgeye bir sembol ve kalın sınırlar ekler. Koyu tema, büyük yazı, VoiceOver ve Hareketi azalt tam desteklenir."),
        ],
        stats=[("3", "günlük bulmaca"), ("6.500", "seviye"), ("12", "dil"), ("0", "reklam")],
        fair_h="Adil olsun diye tasarlandı.",
        fair="Günlük bulmacalar her zaman ücretsiz. Oyunun ortasında reklam yok, takip yok, internetsiz oynanır. İsteğe bağlı, tek seferlik Crownly Pro tüm seviyeleri, sınırsız ipucu ve düelloyu ve bulmaca arşivini açar.",
        support_h="Destek",
        contact="Bir hata mı buldun, bir fikrin ya da sorun mu var? Bize {mail} adresinden yaz. Uygulamada <em>Ayarlar → Geri bildirim gönder</em> de kullanabilirsin; uygulama sürümünü ve cihazını ekler.",
        faq=[
            ("Günün bulmacaları ne zaman değişir?",
             "Yeni günlük bulmacalar her gün 07:00 UTC'de (Türkiye saatiyle 10:00) dünyanın her yerinde aynı anda çıkar."),
            ("Düello nasıl oynanır?",
             "Düello'yu aç, bir oda kur ve kodunu paylaş. 2–4 arkadaş aynı Taçlar tahtasında canlı yarışır; ilk çözen kazanır. İnternet olmadan botlara karşı da antrenman yapabilirsin."),
            ("Telefon değiştirirsem ilerlemem kaybolur mu?",
             "iCloud eşitleme açıksa (Ayarlar → Genel) çözdüğün bulmacalar, yıldızların ve serin özel iCloud hesabın üzerinden diğer cihazlarına aktarılır. iCloud kapalıysa ilerlemen yalnız bu cihazda saklanır ve uygulamayı silince silinir."),
            ("Crownly Pro neler ekler?",
             "6.500 seviyenin hepsi (her zorluğun ilk 50'si ücretsiz), sınırsız ipucu ve düello, geçmiş tüm günlük bulmacaların arşivi ve ayda 1 yerine 3 seri dondurma. Tek seferlik bir satın almadır ve Aile Paylaşımı grubunla paylaşılır. Geri yüklemek için Ayarlar → Crownly Pro → Satın alımları geri yükle'ye dokun."),
            ("Bir günü kaçırdım. Serim gitti mi?",
             "Her zaman değil. Bir günü kaçırınca seri dondurma otomatik kullanılır (ayda bir, Pro ile üç)."),
            ("Bazı renkler bana birbirine benziyor.",
             "Ayarlar → Oyun'dan Renk körü modunu aç. Her bölgeye kendi sembolü eklenir ve sınırlar kalınlaşır; renkleri ayırt etmen gerekmez. Yüksek kontrast tahta paletini de deneyebilirsin."),
        ],
        final_h="Bugünün bulmacaları seni bekliyor.",
        footer_privacy="Gizlilik politikası", made="Bağımsız bir geliştirici tarafından yapıldı.",
        alts=dict(home="Günün bulmacalarıyla Crownly ana sayfası", hard="10×10 Günlük Zor Taçlar bulmacası",
                  route="Numaralı duraklı bir Rota bulmacası", mosaic="Dikdörtgenlere bölünmüş bir Mozaik bulmacası",
                  duel="Aynı tahtada dört oyunculu canlı düello",
                  hint="Sıradaki mantıklı adımı anlatan ipucu", levels="Yıldızlı seviye listesi",
                  dark="Renk körü sembolleriyle koyu tema", solved="Günün bulmacası çözüldü kutlaması"),
    ),
}

# 5×5 demo board: region letter per cell and the solution (row, col) in reveal order.
BOARD = ["AABBB", "ACCBB", "DCCEB", "DDCEE", "DDEEE"]
CROWNS = [(2, 0), (0, 1), (3, 2), (1, 3), (4, 4)]
REGION_COLOR = {"A": "#CDBEEB", "B": "#B9D3F2", "C": "#F6CFA8", "D": "#C5E0B5", "E": "#F2B8C6"}

CROWN_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 18h18l-1.6-9.2-4.6 3.8L12 5.5 9.2 12.6 4.6 8.8z" '
             'fill="url(#g)" stroke="#8a5a00" stroke-width=".8" stroke-linejoin="round"/><circle cx="12" cy="5" r="1.4" fill="#f4d06f"/>'
             '<circle cx="4.4" cy="8.4" r="1.2" fill="#f4d06f"/><circle cx="19.6" cy="8.4" r="1.2" fill="#f4d06f"/></svg>')



def _without_pro(value):
    """1.0.1 texts: 200 levels instead of 6,500 (strings in lists and tuples too)."""
    if isinstance(value, str):
        return value.replace("6,500", "200").replace("6.500", "200")
    if isinstance(value, list):
        return [_without_pro(v) for v in value]
    if isinstance(value, tuple):
        return tuple(_without_pro(v) for v in value)
    return value


if not STORE:
    for _lang, _pro_q, _fair, _freeze in (
            ("en", "What does Crownly Pro add?",
             "Crownly is free. No ads in the middle of a game, no tracking, works offline, and no in-app purchases.",
             ("I missed a day. Is my streak gone?",
              "Not always. A streak freeze is used automatically when you miss a day (one per month).")),
            ("tr", "Crownly Pro neler ekler?",
             "Crownly ücretsiz. Oyunun ortasında reklam yok, takip yok, internetsiz oynanır ve uygulama içi satın alma yok.",
             ("Bir günü kaçırdım. Serim gitti mi?",
              "Her zaman değil. Bir günü kaçırınca seri dondurma otomatik kullanılır (ayda bir)."))):
        _t = T[_lang]
        for _key in list(_t):
            _t[_key] = _without_pro(_t[_key])
        _t["fair"] = _fair
        _t["faq"] = [_freeze if q == _freeze[0] else (q, a) for q, a in _t["faq"] if q != _pro_q]

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


MORE = {
    "en": ("More from HY Apps", "/besmele/en/", "/besmele/img/icon.png", "Bismillah",
           "Prayer times, the Qur'an with audio, the Qibla and a daily verse. No ads.", "All apps", "/"),
    "tr": ("HY Apps'in diğer uygulamaları", "/besmele/", "/besmele/img/icon.png", "Besmele",
           "Namaz vakitleri, sesli Kur'an, kıble ve her gün bir ayet. Reklamsız.", "Tüm uygulamalar", "/tr/"),
}


GUIDES = {
    "en": ("Guides", [("How to play Queens", "/crownly/queens-puzzle-rules/"), ("6 techniques to solve any board", "/crownly/queens-strategy/"),
                      ("LinkedIn Queens alternative", "/crownly/linkedin-queens-alternative/"),
                      ("Games like sudoku", "/crownly/games-like-sudoku/")]),
    "tr": ("Rehberler", [("Queens nasıl oynanır?", "/crownly/tr/queens-nasil-oynanir/"), ("Her tahtayı çözen 6 teknik", "/crownly/tr/queens-stratejileri/"),
                         ("LinkedIn Queens alternatifi", "/crownly/tr/linkedin-queens-alternatifi/"),
                         ("Sudoku benzeri oyunlar", "/crownly/tr/sudoku-benzeri-oyunlar/")]),
}


def store_button(t):
    if LIVE:
        return f'<a class="store" href="{html.escape(t["store"])}">{html.escape(t["cta"])}</a>'
    return f'<span class="store" aria-disabled="true">{html.escape(t["soon"])}</span>'


def guides(t):
    h, links = GUIDES[t["lang"]]
    items = "".join(f'<a href="{href}">{html.escape(label)} →</a>' for label, href in links)
    return f'''  <section class="support reveal">
    <h2>{html.escape(h)}</h2>
    <div class="guides-links">{items}</div>
  </section>'''


def faq_ld(t):
    """FAQPage structured data so Google can show the questions as rich results."""
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'


def more(t):
    """Cross-promotion card for the studio's other app, plus a link to the studio home."""
    h, href, icon, name, desc, all_label, all_href = MORE[t["lang"]]
    return f'''  <section class="more reveal">
    <p class="kicker">{html.escape(h)}</p>
    <a class="more-app" href="{href}"><img src="{icon}" alt="" width="64" height="64">
      <span><strong>{html.escape(name)}</strong><span>{html.escape(desc)}</span></span><b aria-hidden="true">→</b></a>
    <a class="more-all" href="{all_href}">{html.escape(all_label)} →</a>
  </section>'''


def lang_switch(t):
    """EN | TR pill; the current language is highlighted."""
    en = "./" if t["lang"] == "en" else "../"
    tr = "tr/" if t["lang"] == "en" else "./"
    on = lambda l: ' class="on" aria-current="page"' if t["lang"] == l else ""
    return (f'<span class="lang"><a href="{en}" hreflang="en" lang="en"{on("en")}>EN</a>'
            f'<a href="{tr}" hreflang="tr" lang="tr"{on("tr")}>TR</a></span>')


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
    itunes = f'  <meta name="apple-itunes-app" content="app-id={APP_ID}">\n' if LIVE else ""
    app = {"@context": "https://schema.org", "@type": ["VideoGame", "MobileApplication"], "name": "Crownly: Queens Logic Puzzles",
           "alternateName": "Crownly", "description": t["desc"], "url": canonical, "inLanguage": t["lang"],
           "operatingSystem": "iOS 17 or later", "applicationCategory": "GameApplication", "gamePlatform": ["iPhone", "iPad"],
           "genre": ["Puzzle", "Logic"], "playMode": ["SinglePlayer", "MultiPlayer"], "isFamilyFriendly": True,
           "image": "https://hyapps.app/crownly/img/icon.png",
           "screenshot": [f"https://hyapps.app/crownly/img/{t['lang']}-{s}.jpg" for s in ("home", "route", "mosaic", "duel", "levels", "solved")],
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
           "author": {"@type": "Organization", "name": "HY Apps", "url": "https://hyapps.app/"},
           "publisher": {"@type": "Organization", "name": "HY Apps", "url": "https://hyapps.app/"}}
    if LIVE:
        app["installUrl"] = app["downloadUrl"] = t["store"]
    app_ld = json.dumps(app, ensure_ascii=False)
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
{itunes}  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(t["title"])}">
  <meta property="og:description" content="{html.escape(t["og_desc"])}">
  <meta property="og:image" content="https://hyapps.app/assets/og/crownly-{t["lang"]}.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(t["title"])}">
  <meta name="twitter:description" content="{html.escape(t["og_desc"])}">
  <meta property="og:url" content="{canonical}">
  <link rel="icon" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="stylesheet" href="/assets/app.css">
  <script type="application/ld+json">{app_ld}</script>
{faq_ld(t)}
  <!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "89e9ceae59114244a972f60af4a20851"}}'></script><!-- End Cloudflare Web Analytics -->
</head>
<body id="top">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4D06F"/><stop offset="1" stop-color="#C08A12"/></linearGradient></defs></svg>

<header class="bar">
  <a class="brand" href="./#top"><img src="{i}icon.png" alt="" width="28" height="28">Crownly</a>
  <nav>
    <a href="#features">{t["nav_features"]}</a>
    <a href="#support">{t["nav_support"]}</a>
    {lang_switch(t)}
  </nav>
</header>

<section class="hero">
  <div class="blobs" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
  <div class="hero-copy">
    <img class="hero-icon" src="{i}icon.png" alt="Crownly" width="96" height="96">
    <p class="eyebrow">{html.escape(t["eyebrow"])}</p>
    <h1>{t["h1"]}</h1>
    <p class="lead">{html.escape(t["lead"])}</p>
    {store_button(t)}
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

{guides(t)}

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


for key, out in (("en", "crownly/index.html"), ("tr", "crownly/tr/index.html")):
    path = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(page(T[key]))
    print("wrote", out)

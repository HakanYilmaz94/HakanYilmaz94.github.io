#!/usr/bin/env python3
"""Builds the Birbdoku landing pages (EN + TR, also the App Store support page) and its privacy policy.

Usage: python3 -I tools/build_birbdoku.py   (run from the site repo root)
Writes birbdoku/index.html, birbdoku/tr/index.html and birbdoku/privacy.html; style in birbdoku/birbdoku.css.
Until the app is on the App Store, LIVE is False: a "coming soon" badge instead of the store button, no Smart App Banner.
1.1 (2026-11-25): ads (AdMob), purchases and anonymous Firebase analytics; 1.0 was the plain build; Game Center, iCloud
progress and the weekly season groups (CloudKit). 1.1 adds ads, purchases and friends: the policy must say so first.
Pictures: the app icon and Pika / Chiko poses (birbdoku/img/); App Store screenshots go in a gallery once they exist.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ID = "6837803599"
LIVE = True
ANALYTICS = ("<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
             "data-cf-beacon='{\"token\": \"89e9ceae59114244a972f60af4a20851\"}'></script><!-- End Cloudflare Web Analytics -->")
NAME = "Birbdoku: Cute Parrot Puzzle"
MAIL = '<a href="mailto:hyapps@outlook.com?subject=Birbdoku">hyapps@outlook.com</a>'

T = {
    "en": dict(
        lang="en", path="/birbdoku/", img="img/", other_href="tr/", other_label="Türkçe", privacy_href="privacy.html",
        store=f"https://apps.apple.com/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Birbdoku · Cozy Cockatiel Bird Puzzle Game for iPhone & iPad (Queens logic)",
        desc="Birbdoku is a cozy bird puzzle game for iPhone and iPad with two cockatiels, Pika and Chiko: place one bird in every "
             "row, column and color, birds never touch. A Queens-style logic puzzle with a daily board, hints that teach and a streak garden.",
        eyebrow="A cozy logic puzzle for iPhone",
        h1="One bird in every row, <em>column and color.</em>",
        lead="Meet Pika and Chiko, two cockatiels who love logic puzzles. Tap to rule a cell out, double-tap to place a bird, "
             "and remember: birds never touch, not even corner to corner.",
        soon="Coming soon to the App Store", cta="Download on the App Store",
        note="iPhone & iPad · Puzzles play offline",
        nav_story="Features", nav_support="Support",
        features=[
            ("🐦", "Two cockatiels", "Pika and Chiko fill the board with a different face in every cell and cheer when you get it right."),
            ("🧩", "Pure logic, hints that teach", "Every puzzle has exactly one solution, found by logic alone. Hints explain the next step instead of giving the answer."),
            ("📈", "A gentle path", "From a 4×4 starter board up to 10×10, with hide-and-seek levels and Bird Duo (two birds per line) along the way."),
            ("📅", "Daily puzzle", "A new board every day, the same for everyone. You can also play today's board free in your browser."),
            ("🌱", "A streak garden", "Pika and Chiko's millet grows each day you clear a level; the cockatiels walk, peck and nap in their garden."),
            ("🏆", "Weekly season and friends", "Race up to 49 other players in your weekly group, add friends with a player code and visit their gardens."),
        ],
        support_h="Support",
        contact="A bug, an idea or a question? Write to us at {mail}. We read every message.",
        faq=[
            ("Is Birbdoku free?", "Yes. Birbdoku is free to download and every level can be played without paying. It shows ads, and optional in-app purchases remove them or add helpers."),
            ("How do I play?", "Tap a cell once to mark it with an X, tap it twice to place a bird. Every row, every column and "
             "every color needs exactly one bird, and birds may not touch, not even diagonally. Drag across the board to mark many cells."),
            ("What happens when I place a wrong bird?", "You lose one of your three feathers. When all three are gone, start the level again "
             "or use a revive to carry on."),
            ("How does the weekly season work?", "From level 11, every level you clear adds the feathers you kept (up to 3). You race up "
             "to 49 other players in a group of 50. A new season starts every Monday."),
            ("Someone has an offensive name in my group.", "Touch and hold their row in the ranking to report the name or block the player."),
            ("Does it need the internet?", "No for the puzzles. The season ranking and Game Center update when you are online."),
            ("Will my progress move to my new phone?", "Yes. With \"Save progress (iCloud)\" on, your progress follows your Apple Account."),
            ("Is Birbdoku like LinkedIn Queens?", "Yes, it uses the same rules (also known as Star Battle): one per row, column and colored region, never touching. Birbdoku draws birds instead of crowns and adds a level path, a daily puzzle and hints that explain the logic. It is not affiliated with LinkedIn."),
            ("Is there a cockatiel game?", "Birbdoku stars two cockatiels: Pika, a lutino with a pink bow, and Chiko, a grey cockatiel. They play on the board and live in a garden that grows as you play."),
            ("Does it work on iPad?", "Yes, on iPhone and iPad with iOS 17 or later."),
            ("Which languages?", "English, Turkish, German, French, Spanish, Italian, Portuguese (Brazil), Dutch, Russian, Japanese, Korean and Traditional Chinese."),
        ],
        shots_h="Screenshots", shots_alt="Birbdoku screenshot",
        play_h="Play today's puzzle in your browser", play_p="The same daily board as in the app, free, no download.", play_href="/birbdoku/daily-queens-puzzle/", play_cta="Play today's puzzle →",
        guides_h="Guides",
        guides=[("How to play Queens: the rules", "/birbdoku/queens-puzzle-rules/"), ("Queens strategy: 6 techniques", "/birbdoku/queens-strategy/"),
                ("A LinkedIn Queens alternative", "/birbdoku/linkedin-queens-alternative/"), ("A cockatiel game for iPhone", "/birbdoku/cockatiel-game/"),
                ("Bird games for iPhone", "/birbdoku/bird-games-iphone/"), ("Games like sudoku", "/birbdoku/games-like-sudoku/"),
                ("Daily puzzle games like Wordle", "/birbdoku/daily-puzzle-games-like-wordle/"), ("A daily brain teaser habit", "/birbdoku/daily-brain-teaser/")],
        made="Made with care by an independent developer.", footer_privacy="Privacy policy",
    ),
    "tr": dict(
        lang="tr", path="/birbdoku/tr/", img="../img/", other_href="../", other_label="English", privacy_href="../privacy.html#tr",
        store=f"https://apps.apple.com/tr/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Birbdoku · Sultan Papağanlı Kuş Bulmaca Oyunu (iPhone ve iPad, zeka oyunu)",
        desc="Birbdoku, iki sultan papağanı Pika ve Çiko ile iPhone ve iPad için rahat bir kuş bulmaca oyunu: her satıra, sütuna ve "
             "renge bir kuş koy, kuşlar birbirine değmesin. Günlük bulmaca, öğreten ipuçları ve seri bahçesiyle Queens tarzı bir zeka oyunu.",
        eyebrow="iPhone için rahat bir mantık bulmacası",
        h1="Her satıra, sütuna ve <em>renge bir kuş.</em>",
        lead="Mantık bulmacalarını seven iki sultan papağanı Pika ve Çiko ile tanış. Bir kareyi elemek için dokun, kuş koymak "
             "için iki kez dokun ve unutma: kuşlar birbirine değmez, köşeden bile.",
        soon="Yakında App Store'da", cta="App Store'dan indir",
        note="iPhone ve iPad · Bulmacalar internetsiz",
        nav_story="Özellikler", nav_support="Destek",
        features=[
            ("🐦", "İki sultan papağanı", "Pika ve Çiko tahtayı her karede farklı bir yüzle doldurur, doğru hamlede sevinir."),
            ("🧩", "Saf mantık, öğreten ipuçları", "Her bulmacanın tek çözümü var, yalnız mantıkla bulunur. İpuçları cevabı değil sonraki adımı anlatır."),
            ("📈", "Yumuşak bir yol", "4×4 başlangıç tahtasından 10×10'a; yol boyunca saklambaç seviyeleri ve Kuş İkilisi (hat başına iki kuş)."),
            ("📅", "Günlük bulmaca", "Her gün herkese aynı yeni tahta. Bugünün tahtasını tarayıcında da ücretsiz çözebilirsin."),
            ("🌱", "Seri bahçesi", "Bölüm geçtiğin her gün Pika ile Çiko'nun darısı büyür; sultan papağanları bahçelerinde yürür, gagalar, uyuklar."),
            ("🏆", "Haftalık sezon ve arkadaşlar", "Haftalık grubundaki 49 oyuncuyla yarış, oyuncu koduyla arkadaş ekle, bahçelerini ziyaret et."),
        ],
        support_h="Destek",
        contact="Bir hata, bir fikir ya da bir soru mu var? {mail} adresine yaz. Her mesajı okuyoruz.",
        faq=[
            ("Birbdoku ücretsiz mi?", "Evet. Birbdoku ücretsiz indirilir ve her bölüm ödeme yapmadan oynanır. Reklam gösterir; isteğe bağlı satın almalar reklamları kaldırır ya da yardımcı ekler."),
            ("Nasıl oynanır?", "Bir kareye bir kez dokununca X konur, iki kez dokununca kuş konur. Her satırda, her sütunda ve her "
             "renkte tam bir kuş olmalı; kuşlar çaprazdan bile birbirine değemez. Birçok kareyi işaretlemek için parmağını sürükle."),
            ("Yanlış kuş koyarsam ne olur?", "Üç tüyünden birini kaybedersin. Üçü de giderse bölüme baştan başla ya da canlandırmayla devam et."),
            ("Haftalık sezon nasıl işler?", "11. seviyeden sonra geçtiğin her bölüm koruduğun tüyleri (en fazla 3) ekler. 50 kişilik bir "
             "grupta 49 oyuncuyla yarışırsın. Her pazartesi yeni sezon başlar."),
            ("Grubumda kötü bir isim var.", "Sıralamada o satıra basılı tut; ismi bildirebilir ya da oyuncuyu engelleyebilirsin."),
            ("İnternet gerekir mi?", "Bulmacalar için hayır. Sezon sıralaması ve Game Center çevrimiçi olunca güncellenir."),
            ("İlerlemem yeni telefonuma geçer mi?", "Evet. \"İlerlemeyi kaydet (iCloud)\" açıksa ilerlemen Apple Hesabınla gelir."),
            ("LinkedIn Queens gibi mi?", "Evet, aynı kuralları kullanır (Star Battle olarak da bilinir): her satıra, sütuna ve renkli bölgeye bir tane, birbirine değmeden. Birbdoku taç yerine kuş çizer; seviye yolu, günlük bulmaca ve mantığı anlatan ipuçları ekler. LinkedIn ile bağlantısı yoktur."),
            ("Sultan papağanı oyunu mu?", "Evet: Birbdoku'nun iki kahramanı sultan papağanı. Pembe fiyonklu lutino Pika ve gri Çiko tahtada oynar, oynadıkça büyüyen bir bahçede yaşar."),
            ("iPad'de çalışır mı?", "Evet, iOS 17 ve sonrası iPhone ve iPad'de."),
            ("Hangi dillerde?", "Türkçe, İngilizce, Almanca, Fransızca, İspanyolca, İtalyanca, Portekizce (Brezilya), Felemenkçe, Rusça, Japonca, Korece ve Geleneksel Çince."),
        ],
        shots_h="Ekran görüntüleri", shots_alt="Birbdoku ekran görüntüsü",
        play_h="Bugünün bulmacasını tarayıcında çöz", play_p="Uygulamadakiyle aynı günlük tahta; ücretsiz, indirme yok.", play_href="/birbdoku/tr/gunluk-queens-bulmacasi/", play_cta="Bugünün bulmacasını çöz →",
        guides_h="Rehberler",
        guides=[("Queens nasıl oynanır: kurallar", "/birbdoku/tr/queens-nasil-oynanir/"), ("Queens taktikleri: 6 teknik", "/birbdoku/tr/queens-stratejileri/"),
                ("LinkedIn Queens alternatifi", "/birbdoku/tr/linkedin-queens-alternatifi/"), ("Sultan papağanı oyunu", "/birbdoku/tr/sultan-papagani-oyunu/"),
                ("Kuş oyunları", "/birbdoku/tr/kus-oyunlari/"), ("Sudoku benzeri oyunlar", "/birbdoku/tr/sudoku-benzeri-oyunlar/"),
                ("Wordle gibi günlük bulmacalar", "/birbdoku/tr/wordle-gibi-gunluk-bulmaca-oyunlari/"), ("Zeka oyunu: günlük 5 dakika", "/birbdoku/tr/zeka-oyunu/")],
        made="Bağımsız bir geliştirici tarafından özenle yapıldı.", footer_privacy="Gizlilik politikası",
    ),
}


def store_button(t):
    if LIVE:
        return f'<a class="store" href="{html.escape(t["store"])}">{html.escape(t["cta"])}</a>'
    return f'<span class="store off">{html.escape(t["soon"])}</span>'


def page(t):
    i, lang = t["img"], t["lang"]
    feats = "".join(f'<div class="feat"><span class="em" aria-hidden="true">{e}</span><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>'
                    for e, h, p in t["features"])
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in t["faq"])
    canonical = f"https://hyapps.app{t['path']}"
    app_ld = {
        "@context": "https://schema.org", "@type": ["VideoGame", "MobileApplication"], "name": NAME,
        "alternateName": "Birbdoku", "operatingSystem": "iOS 17 or later", "applicationCategory": "GameApplication",
        "applicationSubCategory": "Logic puzzle", "genre": ["Puzzle", "Logic"],
        "description": t["desc"], "url": canonical, "inLanguage": lang, "image": "https://hyapps.app/birbdoku/img/icon.png",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "gamePlatform": ["iPhone", "iPad"], "playMode": "SinglePlayer",
        "screenshot": [f"https://hyapps.app/birbdoku/img/shots/{lang}-{n}.jpg" for n in ("play", "big", "garden", "season")],
        "character": [{"@type": "Person", "name": "Pika", "description": "a lutino cockatiel with a pink bow"}, {"@type": "Person", "name": "Chiko", "description": "a grey cockatiel"}],
        "keywords": ("cockatiel game, bird puzzle game, parrot game, logic puzzle, queens puzzle, star battle, daily puzzle, cozy game, brain teaser, cute animal puzzle"
                     if lang == "en" else "sultan papağanı oyunu, kuş oyunu, kuş bulmaca, papağan oyunu, mantık bulmacası, queens bulmaca, zeka oyunu, günlük bulmaca"),
        "isFamilyFriendly": True,
        "featureList": [f"{f[1]}: {f[2]}" for f in t["features"]],
        "author": {"@type": "Organization", "name": "HY Apps", "url": "https://hyapps.app/"},
        "publisher": {"@type": "Organization", "name": "HY Apps", "url": "https://hyapps.app/", "email": "hyapps@outlook.com"},
    }
    if LIVE:
        app_ld["installUrl"] = t["store"]
        app_ld["sameAs"] = [f"https://apps.apple.com/app/id{APP_ID}"]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
    itunes = f'\n  <meta name="apple-itunes-app" content="app-id={APP_ID}">' if LIVE else ""
    en_on = ' class="on" aria-current="page"' if lang == "en" else ""
    tr_on = ' class="on" aria-current="page"' if lang == "tr" else ""
    en_href, tr_href = ("./", "tr/") if lang == "en" else ("../", "./")
    chiko = "Chiko" if lang == "en" else "Çiko"
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(t["title"])}</title>
  <meta name="description" content="{html.escape(t["desc"])}">
  <meta name="theme-color" content="#9fd8f5">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en" href="https://hyapps.app/birbdoku/">
  <link rel="alternate" hreflang="tr" href="https://hyapps.app/birbdoku/tr/">
  <link rel="alternate" hreflang="x-default" href="https://hyapps.app/birbdoku/">{itunes}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="HY Apps">
  <meta property="og:title" content="{html.escape(t["title"])}">
  <meta property="og:description" content="{html.escape(t["desc"])}">
  <meta property="og:image" content="https://hyapps.app/assets/og/birbdoku-{lang}.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="{"en_US" if lang == "en" else "tr_TR"}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/birbdoku/img/icon.png">
  <link rel="apple-touch-icon" href="/birbdoku/img/icon.png">
  <link rel="stylesheet" href="/birbdoku/birbdoku.css">
  <script type="application/ld+json">{json.dumps(app_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
  {ANALYTICS}
</head>
<body>
<header class="bar">
  <a class="brand" href="./"><img src="{i}icon.png" alt="" width="28" height="28">Birbdoku</a>
  <nav><a href="#features">{t["nav_story"]}</a><a href="#support">{t["nav_support"]}</a>
    <span class="lang"><a href="{en_href}" hreflang="en" lang="en"{en_on}>EN</a><a href="{tr_href}" hreflang="tr" lang="tr"{tr_on}>TR</a></span></nav>
</header>

<section class="hero">
  <img class="icon" src="{i}icon.png" alt="Birbdoku app icon" width="112" height="112">
  <p class="eyebrow">{html.escape(t["eyebrow"])}</p>
  <h1>{t["h1"]}</h1>
  <p class="lead">{html.escape(t["lead"])}</p>
  {store_button(t)}
  <p class="note">{html.escape(t["note"])}</p>
  <div class="duo"><img src="{i}pika_wave.png" alt="Pika" width="360" height="360"><img src="{i}chiko_wave.png" alt="{chiko}" width="360" height="360"></div>
</section>

<main>
  <section class="features" id="features">{feats}</section>

  <section class="shots" aria-label="{html.escape(t["shots_h"])}">
    <h2>{html.escape(t["shots_h"])}</h2>
    <div class="shot-row">{"".join(f'<img src="/birbdoku/img/shots/{lang}-{n}.jpg" alt="{html.escape(t["shots_alt"])}" width="540" height="1173" loading="lazy">' for n in ("play", "big", "garden", "season", "friends", "hint"))}</div>
  </section>

  <section class="card play">
    <h2>{html.escape(t["play_h"])}</h2>
    <p>{html.escape(t["play_p"])}</p>
    <a href="{t["play_href"]}">{html.escape(t["play_cta"])}</a>
  </section>

  <section class="guides" id="guides">
    <h2>{html.escape(t["guides_h"])}</h2>
    <ul>{"".join(f'<li><a href="{h}">{html.escape(x)}</a></li>' for x, h in t["guides"])}</ul>
  </section>

  <section class="support" id="support">
    <h2>{html.escape(t["support_h"])}</h2>
    <p class="card">{t["contact"].format(mail=MAIL)}</p>
    {faq}
  </section>
</main>

<footer class="foot">
  <a href="{"/" if lang == "en" else "/tr/"}">HY Apps</a><a href="{t["privacy_href"]}">{t["footer_privacy"]}</a>
  <a href="{t["other_href"]}">{t["other_label"]}</a><a href="mailto:hyapps@outlook.com">hyapps@outlook.com</a>
  <p>{html.escape(t["made"])} © 2026 HY Apps</p>
</footer>
</body>
</html>
'''


PRIVACY = {
    "en": dict(
        h="Privacy Policy", date=f"{NAME} · Effective November 25, 2026 (version 1.1)",
        sections=[
            (None, "Birbdoku is a logic puzzle game. It needs no account and does not track you. From version 1.1 it shows ads, "
                   "offers optional in-app purchases and uses anonymous analytics. This page explains, in plain words, what the "
                   "game stores, what other players can see, what is shared with whom, and where."),
            ("No account, no tracking", "You do not need an account to play. We never ask for your e-mail address, contacts or "
             "precise location. The game does not ask for tracking permission and does not use the advertising identifier "
             "(IDFA). Nothing collected is linked to your name or Apple Account."),
            ("Stored on your device and in your iCloud", "Your progress and settings are stored on your device. With \"Save progress "
             "(iCloud)\" on, the game also keeps them in your own iCloud (iCloud key-value storage) so a new device can carry on. "
             "We cannot see or read this data; it is handled by Apple under "
             "<a href=\"https://www.apple.com/legal/privacy/\">Apple's privacy policy</a>."),
            ("Ads (Google AdMob)", "The game shows banner, full-screen and optional rewarded video ads through Google AdMob. To "
             "show and measure ads, Google receives technical data from your device: an app-specific device identifier, your "
             "IP address (from which a coarse location such as your country is derived), device and app information, ad "
             "interactions and diagnostic data. In the EU, UK and Switzerland the game first asks for your consent through "
             "Google's consent form, and you can change your choice later in Settings. See "
             "<a href=\"https://policies.google.com/technologies/partner-sites\">how Google uses data from partner apps</a>. "
             "Buying \"Remove ads\" or the Special Offer stops the banner and full-screen ads."),
            ("In-app purchases", "Purchases are handled entirely by Apple. We never see your payment details; the game only learns "
             "which item was bought so it can deliver it. \"Restore purchases\" in the shop brings back permanent items."),
            ("Anonymous analytics (Firebase)", "Copies installed from the App Store send anonymous usage events to Google "
             "Analytics for Firebase (for example a level started or finished, a setting changed, an item bought), with a "
             "random app-instance identifier. We use them only to improve the game. They are not linked to you, not used for "
             "advertising and not sold."),
            ("Weekly season ranking", "From level 11 the game puts you in a weekly group of up to 50 players. For this it stores a "
             "season entry in Apple's CloudKit public database: the name you chose in your profile (or \"Player\" with a few "
             "random letters), your avatar and frame, your level, this week's feathers and levels cleared, and a random player "
             "code that is not linked to your name or Apple Account. Players in your group can see your name, avatar, frame and "
             "feathers. Names are filtered for offensive words; you can report a name or block a player by touching and holding "
             "their row. Reported names are reviewed by us. Old entries are not shown after their week. To have your entries "
             "deleted, write to us."),
            ("Friends", "You can add friends with their player code or an invitation link. Your public profile in CloudKit then "
             "holds your name, avatar, frame, level, profile numbers (for example streaks and stars), your garden's name and "
             "whether you played today, and, if you joined through an invitation, the code of the friend who invited you. "
             "Friends can see these. You can remove a friend or block and report a player from their profile card."),
            ("Game Center", "Game Center is optional. If you are signed in, the game sends your highest level, Bird Duo level, daily "
             "puzzle time and weekly feathers to Game Center leaderboards, and the achievements you earn, which Apple runs."),
            ("This website", "hyapps.app uses Cloudflare Web Analytics, which counts visits without cookies and without identifying you."),
            ("Children", "Birbdoku is not directed at children under 13 and has no chat. Ads are filtered by content rating so that "
             "mature or adult ads are not shown. Other players only see the profile details described above."),
            ("Your choices", "Turn off \"Save progress (iCloud)\", Game Center or the season ranking, change your ad consent in "
             "Settings, and delete all your data by deleting the app (and its iCloud data in Settings → your name → iCloud). To "
             "have a season entry or your public profile removed, write to us."),
            ("Changes and contact", "If a future version changes any of this, this page will say so first, with a new date. "
             "Questions: " + MAIL + "."),
        ]),
    "tr": dict(
        h="Gizlilik Politikası", date="Birbdoku: Kuş Bulmaca Oyunu · Yürürlük: 25 Kasım 2026 (1.1 sürümü)",
        sections=[
            (None, "Birbdoku bir mantık bulmacası oyunudur. Hesap gerektirmez ve seni izlemez. 1.1 sürümünden itibaren reklam "
                   "gösterir, isteğe bağlı uygulama içi satın alma sunar ve anonim analitik kullanır. Bu sayfa oyunun neyi nerede "
                   "sakladığını, diğer oyuncuların ne gördüğünü ve neyin kiminle paylaşıldığını sade bir dille anlatır."),
            ("Hesap yok, izleme yok", "Oynamak için hesap gerekmez. E-posta adresini, kişilerini ya da kesin konumunu hiçbir zaman "
             "istemeyiz. Oyun izleme izni istemez ve reklam kimliğini (IDFA) kullanmaz. Toplanan hiçbir şey adına ya da Apple "
             "Hesabına bağlanmaz."),
            ("Cihazında ve iCloud'unda saklananlar", "İlerlemen ve ayarların cihazında saklanır. \"İlerlemeyi kaydet (iCloud)\" açıksa "
             "oyun bunları yeni bir cihazda devam edebilmen için kendi iCloud'unda (iCloud anahtar-değer deposu) da tutar. Bu "
             "verileri göremeyiz; Apple tarafından "
             "<a href=\"https://www.apple.com/tr/legal/privacy/\">Apple'ın gizlilik politikası</a> kapsamında işlenir."),
            ("Reklamlar (Google AdMob)", "Oyun Google AdMob ile banner, tam ekran ve isteğe bağlı ödüllü video reklamlar gösterir. "
             "Reklamları göstermek ve ölçmek için Google cihazından teknik veriler alır: uygulamaya özel bir cihaz kimliği, IP "
             "adresin (buradan ülke gibi kaba bir konum çıkarılır), cihaz ve uygulama bilgileri, reklam etkileşimleri ve tanılama "
             "verileri. AB, Birleşik Krallık ve İsviçre'de oyun önce Google'ın izin formuyla onayını ister; seçimini sonra Ayarlar'dan "
             "değiştirebilirsin. Ayrıntı: <a href=\"https://policies.google.com/technologies/partner-sites?hl=tr\">Google'ın iş ortağı "
             "uygulamalardan gelen verileri kullanımı</a>. \"Reklamları kaldır\" ya da Özel Teklif alınınca banner ve tam ekran "
             "reklamlar durur."),
            ("Uygulama içi satın almalar", "Satın almaları tamamen Apple yürütür. Ödeme bilgilerini hiçbir zaman görmeyiz; oyun yalnız "
             "hangi ürünün alındığını öğrenir ve onu verir. Mağazadaki \"Satın alımları geri yükle\" kalıcı ürünleri geri getirir."),
            ("Anonim analitik (Firebase)", "App Store'dan kurulan kopyalar Google Analytics for Firebase'e anonim kullanım olayları "
             "gönderir (ör. bölüm başladı ya da bitti, ayar değişti, ürün alındı) ve rastgele bir uygulama örneği kimliği taşır. "
             "Bunları yalnız oyunu geliştirmek için kullanırız. Sana bağlanmaz, reklam için kullanılmaz ve satılmaz."),
            ("Haftalık sezon sıralaması", "11. seviyeden sonra oyun seni en fazla 50 kişilik haftalık bir gruba koyar. Bunun için "
             "Apple'ın CloudKit herkese açık veritabanında bir sezon kaydı tutar: profilde seçtiğin ad (ya da \"Player\" ve birkaç "
             "rastgele harf), avatarın ve çerçeven, seviyen, bu haftaki tüylerin ve geçtiğin bölüm sayısı, adınla ya da Apple "
             "Hesabınla bağlantısı olmayan rastgele bir oyuncu kodu. Grubundaki oyuncular adını, avatarını, çerçeveni ve tüylerini "
             "görür. İsimler kötü kelimelere karşı süzülür; bir satıra basılı tutarak ismi bildirebilir ya da oyuncuyu "
             "engelleyebilirsin. Bildirilen isimleri biz inceleriz. Eski kayıtlar haftası bitince gösterilmez. Kayıtlarının "
             "silinmesini istersen bize yaz."),
            ("Arkadaşlar", "Arkadaşlarını oyuncu koduyla ya da davet bağlantısıyla ekleyebilirsin. CloudKit'teki herkese açık profilin "
             "o zaman adını, avatarını, çerçeveni, seviyeni, profil sayılarını (ör. seriler, yıldızlar), bahçenin adını ve bugün "
             "oynayıp oynamadığını, davetle geldiysen seni davet eden arkadaşın kodunu tutar. Arkadaşların bunları görür. Bir "
             "arkadaşı profil kartından çıkarabilir, bir oyuncuyu engelleyebilir ya da bildirebilirsin."),
            ("Game Center", "Game Center isteğe bağlıdır. Giriş yaptıysan oyun en yüksek seviyeni, Kuş İkilisi seviyeni, günlük "
             "bulmaca süreni, haftalık tüylerini ve kazandığın başarımları Apple'ın işlettiği Game Center'a gönderir."),
            ("Bu web sitesi", "hyapps.app, ziyaretleri çerezsiz ve seni tanımadan sayan Cloudflare Web Analytics kullanır."),
            ("Çocuklar", "Birbdoku 13 yaş altı çocuklara yönelik değildir ve sohbet içermez. Reklamlar içerik derecesine göre süzülür; "
             "yetişkinlere yönelik reklamlar gösterilmez. Diğer oyuncular yalnız yukarıda anlatılan profil bilgilerini görür."),
            ("Seçimlerin", "\"İlerlemeyi kaydet (iCloud)\"u, Game Center'ı ya da sezon sıralamasını kapatabilir, reklam iznini "
             "Ayarlar'dan değiştirebilir, uygulamayı (ve Ayarlar → adın → iCloud'daki verisini) silerek bütün verilerini "
             "silebilirsin. Bir sezon kaydının ya da herkese açık profilinin silinmesini istersen bize yaz."),
            ("Değişiklikler ve iletişim", "İleriki bir sürüm bunlardan birini değiştirirse bu sayfa önce bunu yeni tarihle yazar. "
             "Sorular için: " + MAIL + "."),
        ]),
}


def privacy():
    body = []
    for lang in ("en", "tr"):
        p = PRIVACY[lang]
        anchor = ' id="tr"' if lang == "tr" else ""
        body.append(f'<section lang="{lang}"{anchor}><h1>{p["h"]}</h1><p class="muted">{html.escape(p["date"])}</p>')
        for h, text in p["sections"]:
            if h:
                body.append(f"<h2>{html.escape(h)}</h2>")
            body.append(f"<p>{text}</p>")
        body.append("</section>")
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Birbdoku Privacy Policy · Gizlilik Politikası</title>
  <meta name="description" content="Birbdoku privacy policy: no account, no tracking; ads (AdMob), in-app purchases, anonymous analytics, iCloud progress, friends, Game Center and the weekly season ranking explained.">
  <link rel="canonical" href="https://hyapps.app/birbdoku/privacy.html">
  <link rel="icon" href="/birbdoku/img/icon.png">
  <link rel="stylesheet" href="/birbdoku/birbdoku.css">
  {ANALYTICS}
</head>
<body class="policy">
<main>
  <nav class="crumbs"><a href="/">HY Apps</a> · <a href="./">Birbdoku</a> · <a href="./#support">Support</a> · <a href="#tr">Türkçe</a></nav>
  {"".join(body)}
</main>
</body>
</html>
'''


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    print("wrote", rel)


write("birbdoku/index.html", page(T["en"]))
write("birbdoku/tr/index.html", page(T["tr"]))
write("birbdoku/privacy.html", privacy())

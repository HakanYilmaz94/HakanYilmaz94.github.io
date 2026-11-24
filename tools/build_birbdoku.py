#!/usr/bin/env python3
"""Builds the Birbdoku landing pages (EN + TR, also the App Store support page) and its privacy policy.

Usage: python3 -I tools/build_birbdoku.py   (run from the site repo root)
Writes birbdoku/index.html, birbdoku/tr/index.html and birbdoku/privacy.html; style in birbdoku/birbdoku.css.
Until the app is on the App Store, LIVE is False: a "coming soon" badge instead of the store button, no Smart App Banner.
1.0 is the plain build (Birbdoku/CLAUDE.md "Sade ilk sürüm"): no ads, no purchases, no analytics; Game Center, iCloud
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
        title="Birbdoku: Cute Parrot Puzzle · A cozy Queens logic puzzle with two cockatiels (iPhone)",
        desc="Birbdoku is a cozy logic puzzle for iPhone: place one bird in every row, column and color, and birds never "
             "touch. Two cockatiels, Pika and Chiko, a gentle level path, a daily puzzle, hints that teach and a weekly season.",
        eyebrow="A cozy logic puzzle for iPhone",
        h1="One bird in every row, <em>column and color.</em>",
        lead="Meet Pika and Chiko, two cockatiels who love logic puzzles. Tap to rule a cell out, double-tap to place a bird, "
             "and remember: birds never touch, not even corner to corner.",
        soon="Coming soon to the App Store", cta="Download on the App Store",
        note="iPhone · Puzzles play offline · No ads",
        nav_story="Features", nav_support="Support",
        features=[
            ("🐦", "Two cockatiels", "Pika and Chiko fill the board with a different face in every cell and cheer when you get it right."),
            ("🧩", "Pure logic", "Every puzzle has exactly one solution, found by logic alone. No guessing needed."),
            ("📈", "A gentle path", "From a 4×4 starter board up to 10×10, with hide-and-seek levels and harder boards along the way."),
            ("📅", "Daily puzzle and streak", "A new board every day, the same for everyone, and a streak plant that grows each day you clear a level."),
            ("💡", "Hints that teach", "Hints explain the next logical step instead of just giving the answer. Binoculars find a bird."),
            ("🏆", "Weekly season", "Clear levels, keep your feathers and race up to 49 other players in your group. The winner earns the golden frame."),
        ],
        support_h="Support",
        contact="A bug, an idea or a question? Write to us at {mail}. We read every message.",
        faq=[
            ("Is Birbdoku free?", "Yes. It is free to play, with no ads and no in-app purchases."),
            ("How do I play?", "Tap a cell once to mark it with an X, tap it twice to place a bird. Every row, every column and "
             "every color needs exactly one bird, and birds may not touch, not even diagonally. Drag across the board to mark many cells."),
            ("What happens when I place a wrong bird?", "You lose one of your three feathers. When all three are gone, start the level again "
             "or use a revive to carry on."),
            ("How does the weekly season work?", "From level 11, every level you clear adds the feathers you kept (up to 3). You race up "
             "to 49 other players in a group of 50. A new season starts every Monday."),
            ("Someone has an offensive name in my group.", "Touch and hold their row in the ranking to report the name or block the player."),
            ("Does it need the internet?", "No for the puzzles. The season ranking and Game Center update when you are online."),
            ("Will my progress move to my new phone?", "Yes. With \"Save progress (iCloud)\" on, your progress follows your Apple Account."),
        ],
        made="Made with care by an independent developer.", footer_privacy="Privacy policy",
    ),
    "tr": dict(
        lang="tr", path="/birbdoku/tr/", img="../img/", other_href="../", other_label="English", privacy_href="../privacy.html#tr",
        store=f"https://apps.apple.com/tr/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Birbdoku: Kuş Bulmaca Oyunu · İki sultan papağanıyla Queens mantık bulmacası (iPhone)",
        desc="Birbdoku, iPhone için rahat bir mantık bulmacası: her satıra, sütuna ve renge bir kuş koy, kuşlar birbirine değmesin. "
             "İki sultan papağanı Pika ve Çiko, yumuşak bir seviye yolu, günlük bulmaca, öğreten ipuçları ve haftalık sezon.",
        eyebrow="iPhone için rahat bir mantık bulmacası",
        h1="Her satıra, sütuna ve <em>renge bir kuş.</em>",
        lead="Mantık bulmacalarını seven iki sultan papağanı Pika ve Çiko ile tanış. Bir kareyi elemek için dokun, kuş koymak "
             "için iki kez dokun ve unutma: kuşlar birbirine değmez, köşeden bile.",
        soon="Yakında App Store'da", cta="App Store'dan indir",
        note="iPhone · Bulmacalar internetsiz · Reklamsız",
        nav_story="Özellikler", nav_support="Destek",
        features=[
            ("🐦", "İki sultan papağanı", "Pika ve Çiko tahtayı her karede farklı bir yüzle doldurur, doğru hamlede sevinir."),
            ("🧩", "Saf mantık", "Her bulmacanın tek bir çözümü var, yalnız mantıkla bulunur. Tahmin gerekmez."),
            ("📈", "Yumuşak bir yol", "4×4 başlangıç tahtasından 10×10'a; yol boyunca saklambaç seviyeleri ve zor tahtalar."),
            ("📅", "Günlük bulmaca ve seri", "Her gün herkese aynı yeni bir tahta ve bölüm geçtiğin her gün büyüyen bir seri fidanı."),
            ("💡", "Öğreten ipuçları", "İpuçları cevabı vermek yerine bir sonraki mantıklı adımı anlatır. Dürbün bir kuş bulur."),
            ("🏆", "Haftalık sezon", "Bölüm geç, tüylerini koru ve grubundaki 49 oyuncuyla yarış. Birinci altın çerçeveyi kazanır."),
        ],
        support_h="Destek",
        contact="Bir hata, bir fikir ya da bir soru mu var? {mail} adresine yaz. Her mesajı okuyoruz.",
        faq=[
            ("Birbdoku ücretsiz mi?", "Evet. Ücretsiz oynanır; reklam ve uygulama içi satın alma yoktur."),
            ("Nasıl oynanır?", "Bir kareye bir kez dokununca X konur, iki kez dokununca kuş konur. Her satırda, her sütunda ve her "
             "renkte tam bir kuş olmalı; kuşlar çaprazdan bile birbirine değemez. Birçok kareyi işaretlemek için parmağını sürükle."),
            ("Yanlış kuş koyarsam ne olur?", "Üç tüyünden birini kaybedersin. Üçü de giderse bölüme baştan başla ya da canlandırmayla devam et."),
            ("Haftalık sezon nasıl işler?", "11. seviyeden sonra geçtiğin her bölüm koruduğun tüyleri (en fazla 3) ekler. 50 kişilik bir "
             "grupta 49 oyuncuyla yarışırsın. Her pazartesi yeni sezon başlar."),
            ("Grubumda kötü bir isim var.", "Sıralamada o satıra basılı tut; ismi bildirebilir ya da oyuncuyu engelleyebilirsin."),
            ("İnternet gerekir mi?", "Bulmacalar için hayır. Sezon sıralaması ve Game Center çevrimiçi olunca güncellenir."),
            ("İlerlemem yeni telefonuma geçer mi?", "Evet. \"İlerlemeyi kaydet (iCloud)\" açıksa ilerlemen Apple Hesabınla gelir."),
        ],
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
        "gamePlatform": ["iPhone"], "playMode": "SinglePlayer",
        "keywords": ("logic puzzle, queens puzzle, cockatiel, bird game, daily puzzle, cozy game, brain teaser"
                     if lang == "en" else "mantık bulmacası, queens bulmaca, sultan papağanı, kuş oyunu, günlük bulmaca, zeka oyunu"),
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
  <meta property="og:image" content="https://hyapps.app/birbdoku/img/icon.png">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="{"en_US" if lang == "en" else "tr_TR"}">
  <meta name="twitter:card" content="summary">
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
        h="Privacy Policy", date=f"{NAME} · Effective November 23, 2026",
        sections=[
            (None, "Birbdoku is a logic puzzle game. It needs no account, shows no ads, has no in-app purchases and does not track "
                   "you. This page explains, in plain words, what the game stores, what other players can see and where."),
            ("No account, no tracking", "You do not need an account to play. We never ask for your e-mail address, contacts or "
             "location. The game uses no analytics or advertising service and does not use the advertising identifier (IDFA)."),
            ("Stored on your device and in your iCloud", "Your progress and settings are stored on your device. With \"Save progress "
             "(iCloud)\" on, the game also keeps them in your own iCloud (iCloud key-value storage) so a new device can carry on. "
             "We cannot see or read this data; it is handled by Apple under "
             "<a href=\"https://www.apple.com/legal/privacy/\">Apple's privacy policy</a>."),
            ("Weekly season ranking", "From level 11 the game puts you in a weekly group of up to 50 players. For this it stores a "
             "season entry in Apple's CloudKit public database: the name you chose in your profile (or \"Player\" with a few "
             "random letters), your avatar and frame, your level, this week's feathers and levels cleared, and a random player "
             "code that is not linked to your name or Apple Account. Players in your group can see your name, avatar, frame and "
             "feathers. Names are filtered for offensive words; you can report a name or block a player by touching and holding "
             "their row. Reported names are reviewed by us. Old entries are not shown after their week. To have your entries "
             "deleted, write to us."),
            ("Game Center", "Game Center is optional. If you are signed in, the game sends your highest level, Bird Duo level, daily "
             "puzzle time and weekly feathers to Game Center leaderboards, and the achievements you earn, which Apple runs."),
            ("This website", "hyapps.app uses Cloudflare Web Analytics, which counts visits without cookies and without identifying you."),
            ("Children", "Birbdoku has no chat, no ads and no in-app purchases. The only thing other players see is your chosen name, "
             "avatar and score in the weekly ranking."),
            ("Your choices", "Turn off \"Save progress (iCloud)\" or Game Center, "
             "and delete all your data by deleting the app (and its iCloud data in Settings → your name → iCloud). To have a "
             "season entry removed, write to us."),
            ("Changes and contact", "If a future version adds anything to this (for example ads or friends), this page will say so "
             "first, with a new date. Questions: " + MAIL + "."),
        ]),
    "tr": dict(
        h="Gizlilik Politikası", date="Birbdoku: Kuş Bulmaca Oyunu · Yürürlük: 23 Kasım 2026",
        sections=[
            (None, "Birbdoku bir mantık bulmacası oyunudur. Hesap gerektirmez, reklam göstermez, uygulama içi satın alma yoktur ve "
                   "seni izlemez. Bu sayfa oyunun neyi nerede sakladığını ve diğer oyuncuların ne gördüğünü sade bir dille anlatır."),
            ("Hesap yok, izleme yok", "Oynamak için hesap gerekmez. E-posta adresini, kişilerini ya da konumunu hiçbir zaman "
             "istemeyiz. Oyun analitik ya da reklam hizmeti kullanmaz ve reklam kimliğini (IDFA) kullanmaz."),
            ("Cihazında ve iCloud'unda saklananlar", "İlerlemen ve ayarların cihazında saklanır. \"İlerlemeyi kaydet (iCloud)\" açıksa "
             "oyun bunları yeni bir cihazda devam edebilmen için kendi iCloud'unda (iCloud anahtar-değer deposu) da tutar. Bu "
             "verileri göremeyiz; Apple tarafından "
             "<a href=\"https://www.apple.com/tr/legal/privacy/\">Apple'ın gizlilik politikası</a> kapsamında işlenir."),
            ("Haftalık sezon sıralaması", "11. seviyeden sonra oyun seni en fazla 50 kişilik haftalık bir gruba koyar. Bunun için "
             "Apple'ın CloudKit herkese açık veritabanında bir sezon kaydı tutar: profilde seçtiğin ad (ya da \"Player\" ve birkaç "
             "rastgele harf), avatarın ve çerçeven, seviyen, bu haftaki tüylerin ve geçtiğin bölüm sayısı, adınla ya da Apple "
             "Hesabınla bağlantısı olmayan rastgele bir oyuncu kodu. Grubundaki oyuncular adını, avatarını, çerçeveni ve tüylerini "
             "görür. İsimler kötü kelimelere karşı süzülür; bir satıra basılı tutarak ismi bildirebilir ya da oyuncuyu "
             "engelleyebilirsin. Bildirilen isimleri biz inceleriz. Eski kayıtlar haftası bitince gösterilmez. Kayıtlarının "
             "silinmesini istersen bize yaz."),
            ("Game Center", "Game Center isteğe bağlıdır. Giriş yaptıysan oyun en yüksek seviyeni, Kuş İkilisi seviyeni, günlük "
             "bulmaca süreni, haftalık tüylerini ve kazandığın başarımları Apple'ın işlettiği Game Center'a gönderir."),
            ("Bu web sitesi", "hyapps.app, ziyaretleri çerezsiz ve seni tanımadan sayan Cloudflare Web Analytics kullanır."),
            ("Çocuklar", "Birbdoku'da sohbet, reklam ve uygulama içi satın alma yoktur. Diğer oyuncuların gördüğü tek şey haftalık "
             "sıralamadaki seçtiğin ad, avatar ve puandır."),
            ("Seçimlerin", "\"İlerlemeyi kaydet (iCloud)\"u ya da Game Center'ı kapatabilir, "
             "uygulamayı (ve Ayarlar → adın → iCloud'daki verisini) silerek bütün verilerini silebilirsin. Bir sezon kaydının "
             "silinmesini istersen bize yaz."),
            ("Değişiklikler ve iletişim", "İleriki bir sürüm buna bir şey eklerse (örneğin reklam ya da arkadaşlar) bu sayfa önce bunu "
             "yeni tarihle yazar. Sorular için: " + MAIL + "."),
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
  <meta name="description" content="Birbdoku privacy policy: no account, no ads, no tracking; iCloud progress, Game Center and the weekly season ranking explained.">
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

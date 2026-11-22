#!/usr/bin/env python3
"""Builds the Pyramid Craft landing pages (EN + TR, also the App Store support page) and its privacy policy.

Usage: python3 -I tools/build_pyramidcraft.py   (run from the site repo root)
Writes pyramidcraft/index.html, pyramidcraft/tr/index.html and pyramidcraft/privacy.html; style in pyramidcraft/pyramidcraft.css.
Until the app is on the App Store, LIVE is False: a "coming soon" badge instead of the store button, no Smart App Banner.
1.0 is the plain build: no ads, no purchases, no analytics (Piramit/CLAUDE.md "İlk sürüm sade"). 1.1 adds analytics and,
later, purchases and ads: the policy must say so (and the App Privacy answers in App Store Connect) before that build
goes to review. Pictures: the five App Store screenshots (pyramidcraft/img/<lang>-<name>.jpg) in a gallery; share image assets/og/pyramidcraft-<lang>.jpg.
"""
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ID = "6836529298"
LIVE = False
ANALYTICS = ("<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
             "data-cf-beacon='{\"token\": \"89e9ceae59114244a972f60af4a20851\"}'></script><!-- End Cloudflare Web Analytics -->")
NAME = "Pyramid Craft: Brick Builder"

T = {
    "en": dict(
        lang="en", path="/pyramidcraft/", img="img/", other_href="tr/", other_label="Türkçe", privacy_href="privacy.html",
        store=f"https://apps.apple.com/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Pyramid Craft: Brick Builder · Build the pyramids of ancient Egypt brick by brick (iPhone)",
        desc="Pyramid Craft is an offline pyramid building game for iPhone. Dig Nile mud, mould and dry bricks in the sun, "
             "carry them up and lay three monuments layer by layer, from a mudbrick tomb to the Great Pyramid. Hire workers, "
             "build ramps, water wheels and conveyor belts.",
        eyebrow="An offline building game for iPhone",
        h1="Build the pyramids, <em>one brick at a time.</em>",
        lead="Dig mud from the banks of the Nile, pour it into moulds and let the sun dry it. Carry the bricks up the steps "
             "you laid yourself and watch a monument rise into the desert sky.",
        soon="Coming soon to the App Store", cta="Download on the App Store",
        note="iPhone · Plays offline · No ads",
        nav_story="Monuments", nav_support="Support",
        shots_kicker="In the game", shots_h="Mud, bricks, workers and the Nile.",
        shots=[("anit", "Laying the Mudbrick Tomb"), ("isciler", "Workers with jobs"), ("otomasyon", "A water wheel and conveyor belts"),
               ("ufo", "The monuments at sunset"), ("ustalik", "The mastery tree")],
        guides_h="Guides", guides=[("/pyramidcraft/pyramid-building-game/", "An offline pyramid building game"),
                                   ("/pyramidcraft/beginners-guide/", "Beginner's guide: 10 tips"),
                                   ("/pyramidcraft/how-were-the-pyramids-built/", "How were the pyramids built?")],
        mon_kicker="Three monuments", mon_h="From a mudbrick tomb to the Great Pyramid.",
        monuments=[("Mudbrick Tomb", "1,240 bricks"), ("Sky Stairway", "5,456 bricks, stepped"), ("The Great Pyramid", "26,235 bricks")],
        features=[
            ("🧱", "Every brick by hand", "Mud from the river, a wooden mould, the sun to dry it, and your own hands to set it in the layer."),
            ("🪜", "Ramps and a hand cart", "Climb the steps you built, lay ramps up the sides and push a cart full of bricks to the top."),
            ("👷", "Workers with jobs", "Hire workers and make them diggers, moulders, carriers or masons. Each needs a hut of their own."),
            ("⚙️", "Water wheels and belts", "Wheels on the Nile turn conveyor belts that carry mud to automatic moulds and bricks to the stores."),
            ("⭐", "A mastery tree", "Bricks earn mastery: stronger arms, faster drying, bigger loads, ramps, belts and more."),
            ("🌅", "Calm and offline", "No internet, no timers chasing you. A slow sunset over the dunes and the Nile."),
        ],
        support_h="Support",
        contact="A bug, an idea or a question? Write to us at {mail}. We read every message.",
        faq=[
            ("Is Pyramid Craft free?", "Yes. It is free to play, with no ads and no in-app purchases."),
            ("Does it need the internet?", "No. The whole game plays offline. Game Center leaderboards update when you are online."),
            ("How do I play?", "Walk with the stick on the left and look around by dragging on the right side of the screen. The big "
             "button does whatever you are looking at: dig mud, pour it into a mould, take dry bricks, lay them. Follow the tasks "
             "and the gold arrow at the start."),
            ("Does the game go on while it is closed?", "No. Nothing happens while the game is closed; you carry on exactly where you left off."),
            ("I got stuck somewhere. What can I do?", "Jump up one brick with the Jump button. If you are boxed in by your own buildings, "
             "open Build and take one down with Remove."),
            ("Will my progress move to my new phone?", "Yes. The game keeps a backup in your own iCloud. Sign in with the same Apple "
             "Account and iCloud on the new phone."),
            ("Is it suitable for children?", "Pyramid Craft has no violence, no chat, no account, no ads and no in-app purchases."),
        ],
        made="Made with care by an independent developer.", footer_privacy="Privacy policy",
    ),
    "tr": dict(
        lang="tr", path="/pyramidcraft/tr/", img="../img/", other_href="../", other_label="English", privacy_href="../privacy.html#tr",
        store=f"https://apps.apple.com/tr/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Pyramid Craft: Piramit Yapma · Antik Mısır piramitlerini tuğla tuğla inşa et (iPhone)",
        desc="Pyramid Craft, iPhone için internetsiz bir piramit inşa oyunu. Nil'den çamur çıkar, tuğlaları kalıpla ve güneşte "
             "kurut, yukarı taşı ve üç anıtı katman katman ör: kerpiç mezardan Büyük Piramit'e. İşçi tut, rampa, su çarkı ve bant kur.",
        eyebrow="iPhone için internetsiz bir inşa oyunu",
        h1="Piramitleri <em>tuğla tuğla</em> kendin yükselt.",
        lead="Nil kıyısından çamur çıkar, kalıplara dök ve güneşte kurumaya bırak. Tuğlaları kendi ördüğün basamaklardan "
             "yukarı taşı ve bir anıtın çöl göğüne yükselişini izle.",
        soon="Yakında App Store'da", cta="App Store'dan indir",
        note="iPhone · İnternetsiz oynanır · Reklamsız",
        nav_story="Anıtlar", nav_support="Destek",
        shots_kicker="Oyundan", shots_h="Çamur, tuğla, işçiler ve Nil.",
        shots=[("anit", "Kerpiç Mezar'ı örmek"), ("isciler", "Görevli işçiler"), ("otomasyon", "Su çarkı ve bantlar"),
               ("ufo", "Gün batımında anıtlar"), ("ustalik", "Ustalık ağacı")],
        guides_h="Rehberler", guides=[("/pyramidcraft/tr/piramit-yapma-oyunu/", "İnternetsiz piramit yapma oyunu"),
                                      ("/pyramidcraft/tr/baslangic-rehberi/", "Başlangıç rehberi: 10 ipucu"),
                                      ("/pyramidcraft/tr/piramitler-nasil-yapildi/", "Piramitler nasıl yapıldı?")],
        mon_kicker="Üç anıt", mon_h="Kerpiç mezardan Büyük Piramit'e.",
        monuments=[("Kerpiç Mezar", "1.240 tuğla"), ("Gök Merdiveni", "5.456 tuğla, basamaklı"), ("Büyük Piramit", "26.235 tuğla")],
        features=[
            ("🧱", "Her tuğla elle", "Nehirden çamur, tahta bir kalıp, kurutmak için güneş ve katmana yerleştirmek için kendi ellerin."),
            ("🪜", "Rampalar ve el arabası", "Ördüğün basamaklara tırman, kenarlara rampa kur ve tuğla dolu arabayı tepeye it."),
            ("👷", "Görevli işçiler", "İşçi tut, çamurcu, kalıpçı, taşıyıcı ya da duvarcı yap. Her birine bir kulübe gerekir."),
            ("⚙️", "Su çarkları ve bantlar", "Nil'deki çarklar, çamuru otomatik kalıplara ve tuğlaları depolara taşıyan bantları döndürür."),
            ("⭐", "Ustalık ağacı", "Tuğlalar ustalık kazandırır: güçlü kollar, hızlı kuruma, büyük yükler, rampalar, bantlar ve fazlası."),
            ("🌅", "Sakin ve internetsiz", "İnternet yok, seni kovalayan süre yok. Kumulların ve Nil'in üstünde ağır bir gün batımı."),
        ],
        support_h="Destek",
        contact="Bir hata, bir fikir ya da bir soru mu var? {mail} adresine yaz. Her mesajı okuyoruz.",
        faq=[
            ("Pyramid Craft ücretsiz mi?", "Evet. Ücretsiz oynanır; reklam ve uygulama içi satın alma yoktur."),
            ("İnternet gerekir mi?", "Hayır. Oyunun tamamı internetsiz oynanır. Game Center sıralamaları çevrimiçi olunca güncellenir."),
            ("Nasıl oynanır?", "Soldaki çubukla yürü, ekranın sağ tarafını sürükleyerek etrafına bak. Büyük düğme baktığın şeyle ilgili "
             "işi yapar: çamur al, kalıba dök, kuru tuğlayı al, yerine koy. Başta görevleri ve altın oku takip et."),
            ("Oyun kapalıyken devam eder mi?", "Hayır. Oyun kapalıyken hiçbir şey ilerlemez; bıraktığın yerden aynen devam edersin."),
            ("Bir yerde sıkıştım, ne yapabilirim?", "Zıpla düğmesiyle bir tuğla yukarı çıkabilirsin. Kendi binaların arasında kaldıysan "
             "Kur'u aç ve Sök ile birini kaldır."),
            ("İlerlemem yeni telefonuma geçer mi?", "Evet. Oyun kendi iCloud'unda bir yedek tutar. Yeni telefonda aynı Apple Hesabı ve "
             "iCloud ile giriş yap."),
            ("Çocuklar için uygun mu?", "Pyramid Craft'ta şiddet, sohbet, hesap, reklam ve uygulama içi satın alma yoktur."),
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
    mail = '<a href="mailto:hyapps@outlook.com?subject=Pyramid%20Craft">hyapps@outlook.com</a>'
    feats = "".join(f'<div class="feat"><span class="em" aria-hidden="true">{e}</span><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>'
                    for e, h, p in t["features"])
    mons = "".join(f"<div><b>{html.escape(n)}</b><span>{html.escape(c)}</span></div>" for n, c in t["monuments"])
    shots = "".join(f'<figure><img src="{i}{lang}-{k}.jpg" alt="{html.escape(c)}" width="1200" height="552" loading="lazy">'
                    f'<figcaption>{html.escape(c)}</figcaption></figure>' for k, c in t["shots"])
    guides = "".join(f'<a href="{h}">{html.escape(n)} →</a>' for h, n in t["guides"])
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in t["faq"])
    canonical = f"https://hyapps.app{t['path']}"
    app_ld = {
        "@context": "https://schema.org", "@type": ["VideoGame", "MobileApplication"], "name": NAME,
        "alternateName": "Pyramid Craft", "operatingSystem": "iOS 18 or later", "applicationCategory": "GameApplication",
        "applicationSubCategory": "Building game, simulation", "genre": ["Simulation", "Strategy", "Building"],
        "description": t["desc"], "url": canonical, "inLanguage": lang, "image": "https://hyapps.app/pyramidcraft/img/icon.png",
        "screenshot": [f"https://hyapps.app/pyramidcraft/img/{lang}-{k}.jpg" for k, _ in t["shots"]],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "gamePlatform": ["iPhone"], "playMode": "SinglePlayer", "numberOfPlayers": {"@type": "QuantitativeValue", "value": 1},
        "keywords": ("pyramid builder, building game, offline game, ancient egypt, simulation, automation, conveyor belts"
                     if lang == "en" else "piramit oyunu, inşa oyunu, internetsiz oyun, antik mısır, simülasyon, otomasyon"),
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
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(t["title"])}</title>
  <meta name="description" content="{html.escape(t["desc"])}">
  <meta name="theme-color" content="#f6dfb4">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en" href="https://hyapps.app/pyramidcraft/">
  <link rel="alternate" hreflang="tr" href="https://hyapps.app/pyramidcraft/tr/">
  <link rel="alternate" hreflang="x-default" href="https://hyapps.app/pyramidcraft/">{itunes}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="HY Apps">
  <meta property="og:title" content="{html.escape(t["title"])}">
  <meta property="og:description" content="{html.escape(t["desc"])}">
  <meta property="og:image" content="https://hyapps.app/assets/og/pyramidcraft-{lang}.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="{"en_US" if lang == "en" else "tr_TR"}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="alternate" type="application/rss+xml" title="HY Apps" href="{"/tr/feed.xml" if lang == "tr" else "/feed.xml"}">
  <link rel="icon" href="/pyramidcraft/img/icon.png">
  <link rel="apple-touch-icon" href="/pyramidcraft/img/icon.png">
  <link rel="stylesheet" href="/pyramidcraft/pyramidcraft.css">
  <script type="application/ld+json">{json.dumps(app_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
  {ANALYTICS}
</head>
<body>
<header class="bar">
  <a class="brand" href="./"><img src="{i}icon.png" alt="" width="28" height="28">Pyramid Craft</a>
  <nav><a href="#monuments">{t["nav_story"]}</a><a href="#support">{t["nav_support"]}</a>
    <span class="lang"><a href="{en_href}" hreflang="en" lang="en"{en_on}>EN</a><a href="{tr_href}" hreflang="tr" lang="tr"{tr_on}>TR</a></span></nav>
</header>

<section class="hero">
  <img class="icon" src="{i}icon.png" alt="Pyramid Craft app icon" width="112" height="112">
  <p class="eyebrow">{html.escape(t["eyebrow"])}</p>
  <h1>{t["h1"]}</h1>
  <p class="lead">{html.escape(t["lead"])}</p>
  {store_button(t)}
  <p class="note">{html.escape(t["note"])}</p>
</section>

<main>
  <section class="shots-sec">
    <p class="kicker">{html.escape(t["shots_kicker"])}</p>
    <h2>{html.escape(t["shots_h"])}</h2>
    <div class="shots">{shots}</div>
  </section>

  <section class="features">{feats}</section>

  <section id="monuments">
    <p class="kicker">{html.escape(t["mon_kicker"])}</p>
    <h2>{html.escape(t["mon_h"])}</h2>
    <div class="monuments">{mons}</div>
  </section>

  <section class="guides-sec">
    <h2>{html.escape(t["guides_h"])}</h2>
    <div class="guides-links">{guides}</div>
  </section>

  <section class="support" id="support">
    <h2>{html.escape(t["support_h"])}</h2>
    <p class="card">{t["contact"].format(mail=mail)}</p>
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
        h="Privacy Policy", date=f"{NAME} · Effective November 20, 2026",
        sections=[
            (None, "Pyramid Craft is an offline building game. It needs no account, collects no personal data, shows no ads and "
                   "does not track you. This page explains, in plain words, what the game stores and where."),
            ("No account, no data collected", "You do not need an account to play. We never ask for your name, e-mail address, "
             "contacts or location, and the game sends no data to us or to any analytics or advertising service."),
            ("Stored on your device and in your iCloud", "Your progress and settings are stored on your device. If iCloud is on, "
             "the game also keeps a backup of your progress in your own iCloud (iCloud key-value storage) so it can be restored on "
             "a new device. We cannot see or read this data; it is handled by Apple under "
             "<a href=\"https://www.apple.com/legal/privacy/\">Apple's privacy policy</a>."),
            ("Game Center", "Game Center is optional. If you are signed in, the game sends your total bricks laid, bricks laid this "
             "week and time played to Game Center leaderboards, which Apple runs. You can manage what others see in the Settings app."),
            ("Notifications", "If you allow notifications, the game schedules a daily reminder on your device. It is created on the "
             "device itself; nothing is sent to a server."),
            ("This website", "hyapps.app uses Cloudflare Web Analytics, which counts visits without cookies and without identifying you."),
            ("Children", "Pyramid Craft collects no personal data from anyone, including children. It has no chat, no ads and no "
             "in-app purchases."),
            ("Your choices", "You can turn off notifications and iCloud at any time in the Settings app, and delete all your data by "
             "deleting the app (and its iCloud backup in Settings → your name → iCloud)."),
            ("Changes and contact", "If a future version adds anything to this (for example anonymous statistics), this page will "
             "say so first, with a new date. Questions: "
             "<a href=\"mailto:hyapps@outlook.com?subject=Pyramid%20Craft\">hyapps@outlook.com</a>."),
        ]),
    "tr": dict(
        h="Gizlilik Politikası", date="Pyramid Craft: Piramit Yapma · Yürürlük: 20 Kasım 2026",
        sections=[
            (None, "Pyramid Craft internetsiz bir inşa oyunudur. Hesap gerektirmez, kişisel veri toplamaz, reklam göstermez ve seni "
                   "izlemez. Bu sayfa oyunun neyi nerede sakladığını sade bir dille anlatır."),
            ("Hesap yok, veri toplanmaz", "Oynamak için hesap gerekmez. Adını, e-posta adresini, kişilerini ya da konumunu hiçbir "
             "zaman istemeyiz; oyun bize ya da herhangi bir analitik veya reklam hizmetine veri göndermez."),
            ("Cihazında ve iCloud'unda saklananlar", "İlerlemen ve ayarların cihazında saklanır. iCloud açıksa oyun, yeni bir cihazda "
             "geri yüklenebilsin diye ilerlemenin bir yedeğini kendi iCloud'unda (iCloud anahtar-değer deposu) tutar. Bu verileri "
             "göremeyiz ve okuyamayız; Apple tarafından "
             "<a href=\"https://www.apple.com/tr/legal/privacy/\">Apple'ın gizlilik politikası</a> kapsamında işlenir."),
            ("Game Center", "Game Center isteğe bağlıdır. Giriş yaptıysan oyun toplam koyduğun tuğlayı, bu hafta koyduğun tuğlayı ve "
             "oyun süreni Apple'ın işlettiği Game Center sıralamalarına gönderir. Başkalarının ne göreceğini Ayarlar uygulamasından yönetebilirsin."),
            ("Bildirimler", "Bildirimlere izin verirsen oyun cihazında günlük bir hatırlatma kurar. Bu cihazın kendisinde oluşturulur; "
             "hiçbir sunucuya bir şey gönderilmez."),
            ("Bu web sitesi", "hyapps.app, ziyaretleri çerezsiz ve seni tanımadan sayan Cloudflare Web Analytics kullanır."),
            ("Çocuklar", "Pyramid Craft çocuklar dahil kimseden kişisel veri toplamaz. Sohbet, reklam ve uygulama içi satın alma yoktur."),
            ("Seçimlerin", "Bildirimleri ve iCloud'u istediğin zaman Ayarlar uygulamasından kapatabilir, uygulamayı (ve Ayarlar → adın → "
             "iCloud'daki yedeğini) silerek bütün verilerini silebilirsin."),
            ("Değişiklikler ve iletişim", "İleriki bir sürüm buna bir şey eklerse (örneğin anonim istatistikler) bu sayfa önce bunu "
             "yeni tarihle yazar. Sorular için: <a href=\"mailto:hyapps@outlook.com?subject=Pyramid%20Craft\">hyapps@outlook.com</a>."),
        ]),
}


# The 1.1 policy (ads, purchases, anonymous statistics). Ready since 2026-11-21; set PRIVACY_VERSION = "1.1" and rebuild
# when 1.1 goes to review (not before: 1.0 collects nothing). Piramit/Plans/gizlilik-1.1.md has the rest of the list.
PRIVACY_VERSION = "1.0"   # also switches the page's "no ads, no purchases" lines (see V11_TEXT)
# Preview without publishing: python3 -I tools/build_pyramidcraft.py --preview <dir> (writes only <dir>/privacy.html, 1.1)
PREVIEW = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
if PREVIEW: PRIVACY_VERSION = "1.1"
_MAIL = "<a href=\"mailto:hyapps@outlook.com?subject=Pyramid%20Craft\">hyapps@outlook.com</a>"
PRIVACY_V11 = {
    "en": dict(
        h="Privacy Policy", date=f"{NAME} · Effective with version 1.1",
        sections=[
            (None, "Pyramid Craft is a building game you can play offline. It needs no account and does not track you across "
                   "other companies' apps or websites. From version 1.1 it shows ads, offers optional purchases and counts "
                   "anonymous statistics. This page explains, in plain words, what is collected, why, and by whom."),
            ("No account", "You do not need an account to play. We never ask for your name, e-mail address, contacts or precise location."),
            ("Stored on your device and in your iCloud", "Your progress and settings are stored on your device. If iCloud is on, "
             "the game also keeps a backup of your progress in your own iCloud (iCloud key-value storage). We cannot see or read "
             "this data; it is handled by Apple under <a href=\"https://www.apple.com/legal/privacy/\">Apple's privacy policy</a>."),
            ("Ads (Google AdMob)", "The game shows a full-screen ad about every ten minutes of play, at a pause (never with the full game)."
             " Ads come from Google AdMob, which may process your device's IP address (for a rough location), "
             "device and app information and how ads are viewed, to show and measure ads and prevent fraud. The game does not use "
             "the advertising identifier (IDFA) and never shows the tracking prompt. In the EEA, the UK and Switzerland, Google's "
             "consent form asks first, and ads are limited to what you allow. See "
             "<a href=\"https://policies.google.com/technologies/partner-sites\">how Google uses information from apps</a>."),
            ("Anonymous statistics (Google Firebase Analytics)", "On copies installed from the App Store, the game counts how it is "
             "played: tutorial steps, layers and monuments finished, buildings and skills chosen, workers hired, when the shop is "
             "opened and purchases started or finished, and ads shown. These events are not linked to your identity, contain no "
             "personal details and do not use the advertising identifier. They help us make the game better."),
            ("Purchases", "Purchases (the full game, Deluxe and gold for workers) are "
             "handled entirely by Apple. We never see your payment details; the game only remembers on your device what you own."),
            ("Game Center", "Game Center is optional. If you are signed in, the game sends your total bricks laid, bricks laid this "
             "week and time played to Game Center leaderboards, and achievements you earn, which Apple runs."),
            ("Friends' visits", "If you are signed in to Game Center and iCloud, the game keeps a copy of your world (what you have "
             "built, your Game Center nickname and your brick count) in Apple's CloudKit, so your Game Center friends who play "
             "can walk round it. It is stored under a code made from your Game Center player ID, not your name or Apple Account. "
             "Your friends list is only read on your device to show who plays. Turn it off in the game's Settings "
             "(\"Let my friends see my world\"); the copy is then deleted."),
            ("Notifications", "If you allow notifications, the game schedules a daily reminder on your device. Nothing is sent to a server."),
            ("This website", "hyapps.app uses Cloudflare Web Analytics, which counts visits without cookies and without identifying you."),
            ("Children", "Pyramid Craft is not directed at children under 13 and collects no personal data knowingly from them."),
            ("Your choices", "You can buy the full game to turn ads off, change your ad consent in the EEA/UK from the form, turn off "
             "notifications and iCloud in the Settings app, stop sharing your world with friends in the game's Settings, and "
             "delete all your data by deleting the app (and its iCloud backup in Settings → your name → iCloud)."),
            ("Changes and contact", "If this changes, this page will say so first, with a new date. Questions: " + _MAIL + "."),
        ]),
    "tr": dict(
        h="Gizlilik Politikası", date="Pyramid Craft: Piramit Yapma · 1.1 sürümüyle yürürlükte",
        sections=[
            (None, "Pyramid Craft internetsiz oynanabilen bir inşa oyunudur. Hesap gerektirmez ve seni başka şirketlerin uygulama ve "
                   "sitelerinde izlemez. 1.1 sürümünden itibaren reklam gösterir, isteğe bağlı satın almalar sunar ve anonim "
                   "istatistik sayar. Bu sayfa neyin, neden ve kim tarafından toplandığını sade bir dille anlatır."),
            ("Hesap yok", "Oynamak için hesap gerekmez. Adını, e-posta adresini, kişilerini ya da tam konumunu hiçbir zaman istemeyiz."),
            ("Cihazında ve iCloud'unda saklananlar", "İlerlemen ve ayarların cihazında saklanır. iCloud açıksa oyun ilerlemenin bir "
             "yedeğini kendi iCloud'unda (iCloud anahtar-değer deposu) tutar. Bu verileri göremeyiz; Apple tarafından "
             "<a href=\"https://www.apple.com/tr/legal/privacy/\">Apple'ın gizlilik politikası</a> kapsamında işlenir."),
            ("Reklamlar (Google AdMob)", "Oyun yaklaşık her on dakikalık oyunda bir, bir mola anında tam ekran reklam gösterir "
             "(tam sürümde hiç göstermez). Reklamlar Google AdMob'dan gelir; Google reklamı göstermek, ölçmek "
             "ve sahtekârlığı önlemek için cihazının IP adresini (kaba konum için), cihaz ve uygulama bilgisini ve reklamın nasıl "
             "görüntülendiğini işleyebilir. Oyun reklam kimliğini (IDFA) kullanmaz ve izleme izni sormaz. AB, İngiltere ve "
             "İsviçre'de önce Google'ın onay formu çıkar; reklamlar verdiğin izinle sınırlıdır. Ayrıntı: "
             "<a href=\"https://policies.google.com/technologies/partner-sites?hl=tr\">Google uygulamalardan gelen bilgileri nasıl kullanır</a>."),
            ("Anonim istatistikler (Google Firebase Analytics)", "App Store'dan kurulan kopyalarda oyun nasıl oynandığını sayar: "
             "öğretici adımları, biten katman ve anıtlar, seçilen yapılar ve yetenekler, işe alınan işçiler, mağazanın açılması, "
             "başlayan ya da biten satın almalar ve gösterilen reklamlar. Bu olaylar kimliğine bağlanmaz, kişisel bilgi içermez ve "
             "reklam kimliğini kullanmaz. Oyunu geliştirmemize yardım eder."),
            ("Satın almalar", "Satın almaları (tam sürüm, Deluxe ve işçiler için altın) "
             "tamamen Apple işler. Ödeme bilgilerini hiçbir zaman görmeyiz; oyun yalnız neyin senin olduğunu cihazında hatırlar."),
            ("Game Center", "Game Center isteğe bağlıdır. Giriş yaptıysan oyun toplam ve bu haftaki tuğlanı, oyun süreni ve "
             "kazandığın başarımları Apple'ın işlettiği Game Center'a gönderir."),
            ("Arkadaş ziyaretleri", "Game Center'a ve iCloud'a giriş yaptıysan oyun, bu oyunu oynayan Game Center arkadaşların "
             "gezebilsin diye dünyanın bir kopyasını (yaptıkların, Game Center takma adın ve tuğla sayın) Apple'ın CloudKit "
             "hizmetinde tutar. Kopya adınla ya da Apple Hesabınla değil, Game Center oyuncu kimliğinden üretilen bir kodla "
             "saklanır. Arkadaş listen yalnız cihazında, kimin oynadığını göstermek için okunur. Oyunun Ayarlar'ından "
             "(\"Arkadaşlarım dünyamı görsün\") kapatabilirsin; kopya o zaman silinir."),
            ("Bildirimler", "Bildirimlere izin verirsen oyun cihazında günlük bir hatırlatma kurar. Hiçbir sunucuya bir şey gönderilmez."),
            ("Bu web sitesi", "hyapps.app, ziyaretleri çerezsiz ve seni tanımadan sayan Cloudflare Web Analytics kullanır."),
            ("Çocuklar", "Pyramid Craft 13 yaşından küçük çocuklara yönelik değildir ve onlardan bilerek kişisel veri toplamaz."),
            ("Seçimlerin", "Reklamları kapatmak için tam sürümü alabilir, AB/İngiltere'de reklam onayını formdan değiştirebilir, "
             "bildirimleri ve iCloud'u Ayarlar'dan kapatabilir, dünyanı arkadaşlarınla paylaşmayı oyunun Ayarlar'ından "
             "durdurabilir, uygulamayı (ve iCloud yedeğini) silerek bütün verilerini silebilirsin."),
            ("Değişiklikler ve iletişim", "Bu değişirse bu sayfa önce bunu yeni tarihle yazar. Sorular için: " + _MAIL + "."),
        ]),
}
if PRIVACY_VERSION == "1.1":
    PRIVACY = PRIVACY_V11
    # 1.1 has optional purchases and a rare interstitial at a break (at most about one per ten minutes).
    V11_TEXT = {
        "en": dict(note="iPhone · Plays offline · Free to play",
                   faq={0: ("Is Pyramid Craft free?", "Yes. The whole Mudbrick Tomb is free. The full game, a one-time purchase, opens the other monuments "
                            "and removes ads; Deluxe adds every companion; gold for more workers is optional. Without it, a short "
                            "ad may show at a break, at most about once every ten minutes, never in the middle of an action."),
                        6: ("Is it suitable for children?", "Pyramid Craft has no violence, no chat and no account. It has optional "
                            "purchases and occasional ads at breaks, which Screen Time can limit.")}),
        "tr": dict(note="iPhone · İnternetsiz oynanır · Ücretsiz",
                   faq={0: ("Pyramid Craft ücretsiz mi?", "Evet. Kerpiç Mezar'ın tamamı ücretsiz. Tek seferlik tam sürüm diğer anıtları "
                            "açar ve reklamları kaldırır; Deluxe bütün yol arkadaşlarını ekler; ek işçi için altın isteğe bağlıdır. Onsuz, bir molada en "
                            "fazla yaklaşık on dakikada bir kısa bir reklam çıkabilir, asla bir işin ortasında değil."),
                        6: ("Çocuklar için uygun mu?", "Pyramid Craft'ta şiddet, sohbet ve hesap yok. İsteğe bağlı satın almalar ve "
                            "molalarda ara sıra reklam var; Ekran Süresi ile sınırlanabilir.")}),
    }
    for _l, _v in V11_TEXT.items():
        T[_l]["note"] = _v["note"]
        for _i, _qa in _v["faq"].items():
            T[_l]["faq"][_i] = _qa

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
  <title>Pyramid Craft Privacy Policy · Gizlilik Politikası</title>
  <meta name="description" content="{'Pyramid Craft privacy policy: no account, no tracking; ads (AdMob), purchases and anonymous statistics explained.' if PRIVACY_VERSION == '1.1' else 'Pyramid Craft privacy policy: no account, no data collected, no ads, no tracking.'}">
  <link rel="canonical" href="https://hyapps.app/pyramidcraft/privacy.html">
  <link rel="icon" href="/pyramidcraft/img/icon.png">
  <link rel="stylesheet" href="/pyramidcraft/pyramidcraft.css">
  {ANALYTICS}
</head>
<body class="policy">
<main>
  <nav class="crumbs"><a href="/">HY Apps</a> · <a href="./">Pyramid Craft</a> · <a href="./#support">Support</a> · <a href="#tr">Türkçe</a></nav>
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


if PREVIEW:
    os.makedirs(PREVIEW, exist_ok=True)
    open(os.path.join(PREVIEW, "privacy.html"), "w").write(privacy())
    print("preview", os.path.join(PREVIEW, "privacy.html"))
    sys.exit()
write("pyramidcraft/index.html", page(T["en"]))
write("pyramidcraft/tr/index.html", page(T["tr"]))
write("pyramidcraft/privacy.html", privacy())

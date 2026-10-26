#!/usr/bin/env python3
"""Builds the Brickhaven landing pages (EN + TR) and its privacy policy (EN + TR on one page).

Usage: python3 -I tools/build_brickhaven.py   (run from the site repo root)
Writes brickhaven/index.html, brickhaven/tr/index.html and brickhaven/privacy.html; style in brickhaven/brickhaven.css.
Until the app is on the App Store, LIVE is False: the store button is a "coming soon" badge.
Pictures: brickhaven/img/icon.png (the app icon, 512) and <lang>-<building>.jpg (the game's postcards, 720 wide).
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ID = "6826958666"
LIVE = False
BUILDINGS = ["firin", "ahir", "ev", "kafe", "dondurmaci", "kitapci", "itfaiye", "istasyon"]
ANALYTICS = ("<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
             "data-cf-beacon='{\"token\": \"89e9ceae59114244a972f60af4a20851\"}'></script><!-- End Cloudflare Web Analytics -->")

T = {
    "en": dict(
        lang="en", path="/brickhaven/", img="img/", other_href="tr/", other_label="Türkçe", privacy_href="privacy.html",
        name="Brickhaven",
        store=f"https://apps.apple.com/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Brickhaven: Cozy Brick Builder · Build a seaside town brick by brick (iPhone & iPad)",
        desc="Brickhaven is a cozy first-person building game for iPhone and iPad. Find the right brick, carry it, lay it, "
             "and rebuild Grandma Rose's seaside town one building at a time. Offline, no timers, no ads.",
        eyebrow="A cozy building game for iPhone & iPad",
        h1="Rebuild a seaside town, <em>brick by brick.</em>",
        lead="Grandma Rose left you Brickhaven, a little town by the sea that has fallen to ruin. Pick the right brick from "
             "the pile, carry it to the wall and lay it in place, until the bakery smells of bread again.",
        soon="Coming soon to the App Store", cta="Download on the App Store",
        note="iPhone & iPad · Offline · No ads",
        nav_town="The town", nav_support="Support",
        town_kicker="Eight buildings, eight stories", town_h="Every building has its owner waiting.",
        captions={"firin": "Bakery", "ahir": "Red Barn", "ev": "Flower Shop", "kafe": "Seaside Café",
                  "dondurmaci": "Ice Cream Parlor", "kitapci": "Bookshop", "itfaiye": "Fire Station", "istasyon": "Train Station"},
        features=[
            ("🧱", "Brick by brick", "Find the right shape and colour in the pile, carry up to twenty at a time, and lay every one yourself."),
            ("🏡", "A story to finish", "Each building brings its owner back: Martha's bakery, Joe's barn, Daisy's flowers, all the way to the station."),
            ("📐", "Your own design", "At the Architect's Table you draw your own house, café or shop, then build it on your lot."),
            ("🌷", "Decorate the town", "Benches, lamps, flower beds, trees, cats and chickens: make the streets your own."),
            ("🛠️", "Skills that grow", "Stronger arms, faster hands, a lift that climbs higher and a magnet that pulls bricks to you."),
            ("☕", "Calm by design", "Play offline at your own pace. No timers, no energy, no ads. The first two buildings are free; the rest of the town is a one-time purchase."),
        ],
        support_h="Support",
        contact="A bug, an idea or a question? Write to us at {mail}. We read every message.",
        faq=[
            ("Is Brickhaven free?",
             "The first two buildings, the Bakery and the Red Barn, are free. The Whole Town is a one-time purchase that opens every other building, the Architect's Table and Decorate. There is no subscription and there are no ads."),
            ("Does it need an internet connection?",
             "No. Brickhaven plays fully offline. Purchases, iCloud sync and Game Center use the internet when it is there."),
            ("Will my town move to my new phone or iPad?",
             "Yes. Your saves are kept in your own iCloud, so signing in with the same Apple Account brings them along."),
            ("I bought it on another device. How do I get it back?",
             "Open the purchase screen and tap Restore. Purchases are also shared with your Family Sharing group."),
            ("Is there a mode for colour blindness?",
             "Yes: Settings → Colour-blind mode prints a small symbol on every brick colour, so shapes, not colours alone, tell them apart."),
        ],
        made="Made with care by an independent developer.", footer_privacy="Privacy policy",
    ),
    "tr": dict(
        lang="tr", path="/brickhaven/tr/", img="../img/", other_href="../", other_label="English", privacy_href="../privacy.html#tr",
        name="Brickhaven",
        store=f"https://apps.apple.com/tr/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Brickhaven: Tuğla Yapı Ustası · Sahil kasabasını tuğla tuğla yeniden kur (iPhone & iPad)",
        desc="Brickhaven, iPhone ve iPad için rahat, birinci şahıs bir inşa oyunu. Doğru tuğlayı bul, taşı, yerine koy ve "
             "Büyükanne Rose'un sahil kasabasını bina bina yeniden kur. İnternetsiz, zamanlayıcısız, reklamsız.",
        eyebrow="iPhone ve iPad için rahat bir inşa oyunu",
        h1="Bir sahil kasabasını <em>tuğla tuğla</em> yeniden kur.",
        lead="Büyükannen Rose sana Brickhaven'ı bıraktı: deniz kenarında, yıkılıp gitmiş küçük bir kasaba. Yığından doğru tuğlayı "
             "seç, duvara taşı, yerine koy; fırından yine ekmek kokusu gelene kadar.",
        soon="Yakında App Store'da", cta="App Store'dan indir",
        note="iPhone ve iPad · İnternetsiz · Reklamsız",
        nav_town="Kasaba", nav_support="Destek",
        town_kicker="Sekiz bina, sekiz hikâye", town_h="Her binanın sahibi geri dönmeyi bekliyor.",
        captions={"firin": "Fırın", "ahir": "Kırmızı Ahır", "ev": "Çiçekçi", "kafe": "Sahil Kafesi",
                  "dondurmaci": "Dondurmacı", "kitapci": "Kitapçı", "itfaiye": "İtfaiye", "istasyon": "Tren İstasyonu"},
        features=[
            ("🧱", "Tuğla tuğla", "Yığında doğru şekli ve rengi bul, bir seferde yirmiye kadar taşı, her birini kendin yerine koy."),
            ("🏡", "Bitirilecek bir hikâye", "Her bina sahibini geri getirir: Martha'nın fırını, Joe'nun ahırı, Daisy'nin çiçekleri, istasyona kadar."),
            ("📐", "Kendi tasarımın", "Mimar Masası'nda kendi evini, kafeni ya da dükkânını çiz, sonra arsana kur."),
            ("🌷", "Kasabayı süsle", "Bank, fener, çiçek tarhı, ağaç, kedi ve tavuk: sokakları kendine göre donat."),
            ("🛠️", "Gelişen ustalık", "Daha güçlü kollar, daha hızlı eller, daha yükseğe çıkan asansör ve tuğlaları çeken mıknatıs."),
            ("☕", "Sakin oyun", "İnternetsiz, kendi hızında oyna. Zamanlayıcı yok, enerji yok, reklam yok. İlk iki bina ücretsiz; kasabanın geri kalanı tek seferlik satın alma."),
        ],
        support_h="Destek",
        contact="Bir hata, bir fikir ya da bir soru mu var? {mail} adresine yaz. Her mesajı okuyoruz.",
        faq=[
            ("Brickhaven ücretsiz mi?",
             "İlk iki bina, Fırın ve Kırmızı Ahır ücretsiz. Tüm Kasaba tek seferlik bir satın almadır; diğer bütün binaları, Mimar Masası'nı ve Süsle'yi açar. Abonelik ve reklam yok."),
            ("İnternet gerekiyor mu?",
             "Hayır. Brickhaven tamamen internetsiz oynanır. Satın alma, iCloud eşitlemesi ve Game Center internet olduğunda onu kullanır."),
            ("Kasabam yeni telefonuma ya da iPad'ime geçer mi?",
             "Evet. Kayıtların kendi iCloud'unda tutulur; aynı Apple Hesabı ile girince seninle gelir."),
            ("Başka bir cihazda satın aldım, nasıl geri alırım?",
             "Satın alma ekranını aç ve Geri yükle'ye dokun. Satın almalar Aile Paylaşımı grubunla da paylaşılır."),
            ("Renk körleri için bir mod var mı?",
             "Evet: Ayarlar → Renk körü modu her tuğla rengine küçük bir simge basar; renkler yalnız renkle değil, şekille de ayrılır."),
        ],
        made="Bağımsız bir geliştirici tarafından özenle yapıldı.", footer_privacy="Gizlilik politikası",
    ),
}


def store_button(t):
    if LIVE:
        return f'<a class="store" href="{html.escape(t["store"])}">{html.escape(t["cta"])}</a>'
    return f'<span class="store off">{html.escape(t["soon"])}</span>'


def page(t):
    i = t["img"]
    lang = t["lang"]
    mail = f'<a href="mailto:hyapps@outlook.com?subject=Brickhaven">hyapps@outlook.com</a>'
    cards = "".join(f'<figure><img src="{i}{lang}-{b}.jpg" alt="{html.escape(t["captions"][b])}" width="720" height="480" loading="lazy">'
                    f'<figcaption>{html.escape(t["captions"][b])}</figcaption></figure>' for b in BUILDINGS)
    feats = "".join(f'<div class="feat"><span class="em" aria-hidden="true">{e}</span><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>'
                    for e, h, p in t["features"])
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in t["faq"])
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}, ensure_ascii=False)
    canonical = f"https://hyapps.app{t['path']}"
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
  <meta name="theme-color" content="#2f9fa8">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en" href="https://hyapps.app/brickhaven/">
  <link rel="alternate" hreflang="tr" href="https://hyapps.app/brickhaven/tr/">
  <link rel="alternate" hreflang="x-default" href="https://hyapps.app/brickhaven/">{itunes}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(t["title"])}">
  <meta property="og:description" content="{html.escape(t["desc"])}">
  <meta property="og:image" content="https://hyapps.app/brickhaven/img/{lang}-firin.jpg">
  <meta property="og:url" content="{canonical}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/brickhaven/img/icon.png">
  <link rel="apple-touch-icon" href="/brickhaven/img/icon.png">
  <link rel="stylesheet" href="/brickhaven/brickhaven.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"MobileApplication","name":"Brickhaven","operatingSystem":"iOS 18 or later",
   "applicationCategory":"GameApplication","url":"{canonical}","inLanguage":"{lang}",
   "offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}},
   "publisher":{{"@type":"Organization","name":"HY Apps","url":"https://hyapps.app/"}}}}
  </script>
  <script type="application/ld+json">{faq_ld}</script>
  {ANALYTICS}
</head>
<body>
<header class="bar">
  <a class="brand" href="./"><img src="{i}icon.png" alt="" width="28" height="28">Brickhaven</a>
  <nav><a href="#town">{t["nav_town"]}</a><a href="#support">{t["nav_support"]}</a>
    <span class="lang"><a href="{en_href}" hreflang="en" lang="en"{en_on}>EN</a><a href="{tr_href}" hreflang="tr" lang="tr"{tr_on}>TR</a></span></nav>
</header>

<section class="hero">
  <img class="icon" src="{i}icon.png" alt="Brickhaven" width="112" height="112">
  <p class="eyebrow">{html.escape(t["eyebrow"])}</p>
  <h1>{t["h1"]}</h1>
  <p class="lead">{html.escape(t["lead"])}</p>
  {store_button(t)}
  <p class="note">{html.escape(t["note"])}</p>
  <img class="hero-shot" src="{i}{lang}-firin.jpg" alt="{html.escape(t["captions"]["firin"])}" width="720" height="480">
</section>

<main>
  <section class="features">{feats}</section>

  <section class="town" id="town">
    <p class="kicker">{html.escape(t["town_kicker"])}</p>
    <h2>{html.escape(t["town_h"])}</h2>
    <div class="cards">{cards}</div>
  </section>

  <section class="support" id="support">
    <h2>{html.escape(t["support_h"])}</h2>
    <p class="card">{t["contact"].format(mail=mail)}</p>
    {faq}
  </section>
</main>

<footer class="foot">
  <a href="/">HY Apps</a><a href="{t["privacy_href"]}">{t["footer_privacy"]}</a>
  <a href="{t["other_href"]}">{t["other_label"]}</a><a href="mailto:hyapps@outlook.com">hyapps@outlook.com</a>
  <p>{html.escape(t["made"])} © 2026 HY Apps</p>
</footer>
</body>
</html>
'''


PRIVACY = {
    "en": dict(
        h="Privacy Policy", date="Brickhaven: Cozy Brick Builder · Effective October 26, 2026",
        sections=[
            (None, "Brickhaven is a building game. It collects no personal data, has no ads and no analytics tools, and does "
                   "not track you across other apps or websites."),
            ("No account", "You do not need an account to play. We do not ask for your name, e-mail address, contacts or location."),
            ("Stored on your device and in your iCloud", "Your saved towns, designs and settings are stored on your device. If "
             "iCloud is on, the game also keeps a copy of your saves in your own iCloud (iCloud key-value storage) so they "
             "reach your other devices. We cannot see or read this data; it is handled by Apple under "
             "<a href=\"https://www.apple.com/legal/privacy/\">Apple's privacy policy</a>. Deleting the app deletes the copy on the device."),
            ("Game Center", "Game Center is optional. If you are signed in, the game reports your achievements to Game Center, "
             "handled by Apple. You can manage what others see in the Settings app."),
            ("Photos", "When a building is finished you can share or save its film and photo. If you choose to save them, the "
             "game asks for permission to add them to your Photos. It never reads your photo library."),
            ("Purchases", "In-app purchases are made through the App Store. Payment is handled entirely by Apple; we never see "
             "your payment details or Apple Account."),
            ("Crash reports", "If you agreed to share analytics with app developers in your device settings, Apple may send us "
             "anonymous crash reports. We use them only to fix bugs."),
            ("This website", "hyapps.app uses Cloudflare Web Analytics, which counts visits without cookies and without "
             "identifying you."),
            ("Children", "Brickhaven is suitable for all ages and collects no data from anyone, including children."),
            ("Changes and contact", "If this policy changes, the new version will be posted on this page with a new date. "
             "Questions: <a href=\"mailto:hyapps@outlook.com?subject=Brickhaven\">hyapps@outlook.com</a>."),
        ]),
    "tr": dict(
        h="Gizlilik Politikası", date="Brickhaven: Tuğla Yapı Ustası · Yürürlük: 26 Ekim 2026",
        sections=[
            (None, "Brickhaven bir inşa oyunudur. Kişisel veri toplamaz, reklam ve analiz aracı içermez, seni başka uygulama "
                   "ve sitelerde izlemez."),
            ("Hesap yok", "Oynamak için hesap gerekmez. Adını, e-posta adresini, kişilerini ya da konumunu istemeyiz."),
            ("Cihazında ve iCloud'unda saklananlar", "Kayıtlı kasabaların, tasarımların ve ayarların cihazında saklanır. iCloud "
             "açıksa oyun, diğer cihazlarına ulaşsın diye kayıtlarının bir kopyasını kendi iCloud'unda (iCloud anahtar-değer "
             "deposu) tutar. Bu verileri göremeyiz ve okuyamayız; Apple tarafından "
             "<a href=\"https://www.apple.com/tr/legal/privacy/\">Apple'ın gizlilik politikası</a> kapsamında işlenir. "
             "Uygulamayı silmek cihazdaki kopyayı siler."),
            ("Game Center", "Game Center isteğe bağlıdır. Giriş yaptıysan oyun başarımlarını Apple'ın işlettiği Game Center'a "
             "bildirir. Başkalarının ne göreceğini Ayarlar uygulamasından yönetebilirsin."),
            ("Fotoğraflar", "Bir bina bitince onun filmini ve fotoğrafını paylaşabilir ya da kaydedebilirsin. Kaydetmeyi "
             "seçersen oyun, Fotoğraflar'a ekleme izni ister. Fotoğraf arşivini hiçbir zaman okumaz."),
            ("Satın almalar", "Uygulama içi satın almalar App Store üzerinden yapılır. Ödemeyi tamamen Apple yürütür; ödeme "
             "bilgilerini ya da Apple Hesabını görmeyiz."),
            ("Çökme raporları", "Cihaz ayarlarında uygulama geliştiricileriyle analiz paylaşmayı kabul ettiysen Apple bize anonim "
             "çökme raporları gönderebilir. Bunları yalnız hataları düzeltmek için kullanırız."),
            ("Bu web sitesi", "hyapps.app, ziyaretleri çerezsiz ve seni tanımadan sayan Cloudflare Web Analytics kullanır."),
            ("Çocuklar", "Brickhaven her yaşa uygundur ve çocuklar dahil kimseden veri toplamaz."),
            ("Değişiklikler ve iletişim", "Bu politika değişirse yeni hâli yeni tarihle bu sayfada yayınlanır. Sorular için: "
             "<a href=\"mailto:hyapps@outlook.com?subject=Brickhaven\">hyapps@outlook.com</a>."),
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
  <title>Brickhaven Privacy Policy · Gizlilik Politikası</title>
  <meta name="description" content="Brickhaven privacy policy: no account, no ads, no tracking, no personal data collected.">
  <link rel="canonical" href="https://hyapps.app/brickhaven/privacy.html">
  <link rel="icon" href="/brickhaven/img/icon.png">
  <link rel="stylesheet" href="/brickhaven/brickhaven.css">
  {ANALYTICS}
</head>
<body class="policy">
<main>
  <nav class="crumbs"><a href="/">HY Apps</a> · <a href="./">Brickhaven</a> · <a href="./#support">Support</a> · <a href="#tr">Türkçe</a></nav>
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


write("brickhaven/index.html", page(T["en"]))
write("brickhaven/tr/index.html", page(T["tr"]))
write("brickhaven/privacy.html", privacy())

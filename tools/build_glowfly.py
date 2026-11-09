#!/usr/bin/env python3
"""Builds the Glowfly landing pages (EN + TR) and its privacy policy (EN + TR on one page).

Usage: python3 -I tools/build_glowfly.py   (run from the site repo root)
Writes glowfly/index.html, glowfly/tr/index.html and glowfly/privacy.html; style in glowfly/glowfly.css.
Until the app is on the App Store, LIVE is False: the store button is a "coming soon" badge and there is no Smart App Banner.
Pictures: glowfly/img/icon.png (the app icon, 512) and ch1…ch10.jpg (one postcard per chapter, drawn with the game's own
painters: Glowfly/Tools/scene_sheet.sh with SHEET_SCALE=2).
English names follow the app's English build; if they change in the translation, change them here too.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ID = "6830895618"
LIVE = True
# STORE mirrors the app's STORE compile flag: 1.0 has no purchases and no ads (Guideline 2.5.19), 1.1 brings Glowfly Plus,
# gems, the ad-free option and reward videos back. With STORE = False the FAQ and privacy policy leave them out.
# build_guides.py reads it from here too. 1.1: set True and run this and build_guides.py.
STORE = False
ANALYTICS = ("<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
             "data-cf-beacon='{\"token\": \"89e9ceae59114244a972f60af4a20851\"}'></script><!-- End Cloudflare Web Analytics -->")

T = {
    "en": dict(
        lang="en", path="/glowfly/", img="img/", other_href="tr/", other_label="Türkçe", privacy_href="privacy.html",
        store=f"https://apps.apple.com/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Glowfly: Idle Brick Breaker · A relaxing idle game of fireflies, light and night skies (iPhone & iPad)",
        desc="Glowfly is a relaxing idle merge game for iPhone and iPad. Fireflies of light bounce through the dark, break "
             "glass walls and reveal a hand-drawn night landscape. Merge ten lights into a brighter one, find the fallen "
             "stars across 10 chapters and 1,000 nights. It keeps playing while you're away.",
        eyebrow="A relaxing idle merge game for iPhone & iPad",
        h1="Light up the night, <em>one firefly at a time.</em>",
        lead="The stars have fallen to the earth. Lumi, a small light, sets out to bring them home. Send your lights "
             "bouncing through the dark, break the glass walls and watch a quiet night landscape appear underneath.",
        soon="Coming soon to the App Store", cta="Download on the App Store",
        note="iPhone & iPad · Plays while you're away · Free to play",
        nav_story="The story", nav_support="Support",
        story_kicker="10 chapters, 1,000 nights", story_h="Every chapter is a new night sky.",
        chapters=["Forest Night", "Lakeshore", "Lavender Field", "Northern Lights", "Lighthouse",
                  "Desert Night", "Sleeping Town", "Deep Sea", "Moon and Planets", "Milky Way"],
        chapter_word="Chapter",
        features=[
            ("✨", "Merge into brighter light", "Ten lights merge into one stronger light. Twelve kinds of light, each brighter and more beautiful than the last."),
            ("🌙", "A story told in postcards", "Every ten nights Lumi finds a fallen star and a postcard joins your story: a cabin in the woods, a lighthouse, a sleeping town, the Milky Way."),
            ("💤", "Plays while you're away", "Your lights keep working for hours after you close the game. Come back to nights cleared and light to collect."),
            ("🪨", "Glass, rock and hard stone", "Thin glass shatters at a touch, big rocks take a beating. Tap the walls yourself or hold to speed everything up."),
            ("⭐", "Skills and upgrades", "Level up each light, pick a skill at levels 5, 20 and 40, and strengthen all your lights at once."),
            ("🎧", "Calm by design", "Soft lo-fi music, gentle glass sounds and no timers chasing you." + (" Ads only ever play when you choose to watch one for a reward." if STORE else "")),
        ],
        support_h="Support",
        contact="A bug, an idea or a question? Write to us at {mail}. We read every message.",
        faq=[
            ("Is Glowfly free?",
             "Yes, Glowfly is free to play from the first night to the last." + (" Glowfly Plus (an optional subscription), an "
             "ad-free option and gem packs are available as in-app purchases; prices are always shown on the button before you buy." if STORE else "")),
            ("Does the game keep going when it's closed?",
             "Yes. Your lights keep breaking walls for 4 hours after you leave (longer with Deep Sleep" + (" or Glowfly Plus" if STORE else "") + "). "
             "When you come back, the game shows how many nights were cleared and the light you earned."),
            ("Are there ads?",
             ("Only if you want them. Some rewards, like a boost, can be earned by watching a short video ad. No ad ever "
              "plays on its own, and with Plus or the ad-free option you get those rewards without ads." if STORE else
              "No. Glowfly has no ads.")),
            ("What is in a Star Box?",
             "Boxes drop from the sky now and then and at every chapter end. The game lists exactly what a box can "
             "contain and the chance of each prize before you open one."),
            ("Will my progress move to my new phone?",
             "Yes. The game keeps a backup in your own iCloud." + (" Purchases come back with Restore Purchases on the Glowfly Plus screen." if STORE else "")),
            ("Is it suitable for children?",
             ("Glowfly has no violence, no chat and no account. In-app purchases are protected by your Apple Account and Screen Time settings." if STORE else "Glowfly has no violence, no chat, no account, no ads and no in-app purchases.")),
        ],
        made="Made with care by an independent developer.", footer_privacy="Privacy policy",
        guides_h="Guides",
        guides=[("A relaxing idle merge game that plays while you're away", "/glowfly/relaxing-idle-merge-game/"),
                ("Beginner's guide: 10 tips for Glowfly", "/glowfly/beginners-guide/"),
                ("How offline progress works in idle games", "/glowfly/idle-games-offline-progress/")],
    ),
    "tr": dict(
        lang="tr", path="/glowfly/tr/", img="../img/", other_href="../", other_label="English", privacy_href="../privacy.html#tr",
        store=f"https://apps.apple.com/tr/app/apple-store/id{APP_ID}?pt=129592179&ct=web&mt=8",
        title="Glowfly: Idle Işık Birleştirme · Ateşböcekleri, ışık ve gece gökyüzüyle rahatlatıcı bir idle oyun (iPhone ve iPad)",
        desc="Glowfly, iPhone ve iPad için rahatlatıcı bir idle birleştirme oyunu. Ateşböceği gibi ışıklar karanlıkta "
             "seker, cam duvarları kırar ve altından elle çizilmiş bir gece manzarası çıkar. On ışığı birleştirip daha "
             "parlak bir ışık yap, 10 bölüm ve 1.000 gece boyunca düşen yıldızları bul. Sen yokken de oynamaya devam eder.",
        eyebrow="iPhone ve iPad için rahatlatıcı bir idle birleştirme oyunu",
        h1="Geceyi <em>ateşböcekleriyle</em> aydınlat.",
        lead="Yıldızlar yeryüzüne düştü. Küçük bir ışık olan Lumi onları evine götürmek için yola çıkıyor. Işıklarını "
             "karanlıkta sektir, cam duvarları kır ve altından sakin bir gece manzarasının çıkışını izle.",
        soon="Yakında App Store'da", cta="App Store'dan indir",
        note="iPhone ve iPad · Sen yokken de oynar · Ücretsiz",
        nav_story="Hikâye", nav_support="Destek",
        story_kicker="10 bölüm, 1.000 gece", story_h="Her bölüm yeni bir gece gökyüzü.",
        chapters=["Orman Gecesi", "Göl Kıyısı", "Lavanta Tarlası", "Kuzey Işıkları", "Deniz Feneri",
                  "Çöl Gecesi", "Uyuyan Kasaba", "Derin Deniz", "Ay ve Gezegenler", "Samanyolu"],
        chapter_word="Bölüm",
        features=[
            ("✨", "Birleştir, daha parlak yap", "On ışık birleşip daha güçlü tek bir ışık olur. On iki ayrı ışık, her biri öncekinden daha parlak ve güzel."),
            ("🌙", "Kartpostallarla bir hikâye", "Her on gecede Lumi düşmüş bir yıldız bulur ve hikâyene bir kartpostal eklenir: ormanda bir kulübe, bir deniz feneri, uyuyan bir kasaba, Samanyolu."),
            ("💤", "Sen yokken de oynar", "Oyunu kapattıktan sonra ışıkların saatlerce çalışmaya devam eder. Döndüğünde aydınlanmış geceler ve toplanacak ışıltı seni bekler."),
            ("🪨", "Cam, kaya ve sert taş", "İnce cam bir dokunuşta kırılır, iri kayalar dayanır. Duvarlara kendin dokun ya da basılı tutup her şeyi hızlandır."),
            ("⭐", "Beceriler ve güçlendirmeler", "Her ışığın seviyesini yükselt, 5, 20 ve 40. seviyede bir beceri seç, bütün ışıklarını birden güçlendir."),
            ("🎧", "Sakin oyun", "Yumuşak lo-fi müzik, hafif cam sesleri, seni kovalayan zamanlayıcı yok." + (" Reklam yalnız bir ödül için izlemeyi seçtiğinde oynar." if STORE else "")),
        ],
        support_h="Destek",
        contact="Bir hata, bir fikir ya da bir soru mu var? {mail} adresine yaz. Her mesajı okuyoruz.",
        faq=[
            ("Glowfly ücretsiz mi?",
             "Evet, Glowfly ilk geceden son geceye kadar ücretsiz oynanır." + (" Glowfly Plus (isteğe bağlı abonelik), reklamsız "
             "seçenek ve elmas paketleri uygulama içi satın alma olarak sunulur; fiyat satın almadan önce düğmede yazar." if STORE else "")),
            ("Oyun kapalıyken de ilerler mi?",
             "Evet. Ayrıldıktan sonra ışıkların 4 saat boyunca duvar kırmaya devam eder (Derin uyku" + (" ya da Glowfly Plus" if STORE else "") + " ile "
             "daha uzun). Döndüğünde oyun kaç gecenin aydınlandığını ve kazandığın ışıltıyı gösterir."),
            ("Reklam var mı?",
             ("Yalnız sen istersen. Takviye gibi bazı ödüller kısa bir video reklam izleyerek kazanılabilir. Hiçbir reklam "
              "kendiliğinden oynamaz; Plus ya da reklamsız seçenekle bu ödülleri reklamsız alırsın." if STORE else
              "Hayır. Glowfly'da reklam yok.")),
            ("Yıldız kutusunda neler var?",
             "Kutular ara sıra gökten ve her bölüm sonunda düşer. Oyun, bir kutudan neler çıkabileceğini ve her ödülün "
             "olasılığını kutuyu açmadan önce açıkça listeler."),
            ("İlerlemem yeni telefonuma geçer mi?",
             "Evet. Oyun kendi iCloud'unda bir yedek tutar." + (" Satın almalar Glowfly Plus ekranındaki Satın alımları geri yükle ile geri gelir." if STORE else "")),
            ("Çocuklar için uygun mu?",
             ("Glowfly'da şiddet, sohbet ve hesap yoktur. Uygulama içi satın almalar Apple Hesabın ve Ekran Süresi ayarlarınla korunur." if STORE else "Glowfly'da şiddet, sohbet, hesap, reklam ve uygulama içi satın alma yoktur.")),
        ],
        made="Bağımsız bir geliştirici tarafından özenle yapıldı.", footer_privacy="Gizlilik politikası",
        guides_h="Rehberler",
        guides=[("Sen yokken de oynayan rahatlatıcı bir idle birleştirme oyunu", "/glowfly/tr/rahatlatici-idle-birlestirme-oyunu/"),
                ("Başlangıç rehberi: Glowfly için 10 ipucu", "/glowfly/tr/baslangic-rehberi/"),
                ("Idle oyunlarda kapalıyken ilerleme nasıl çalışır", "/glowfly/tr/idle-oyunlarda-kapaliyken-ilerleme/")],
    ),
}


def store_button(t):
    if LIVE:
        return f'<a class="store" href="{html.escape(t["store"])}">{html.escape(t["cta"])}</a>'
    return f'<span class="store off">{html.escape(t["soon"])}</span>'


def page(t):
    i, lang = t["img"], t["lang"]
    mail = '<a href="mailto:hyapps@outlook.com?subject=Glowfly">hyapps@outlook.com</a>'
    cards = "".join(f'<figure><img src="{i}ch{n + 1}.jpg" alt="{html.escape(t["chapters"][n])}, Glowfly" width="600" height="900" loading="lazy">'
                    f'<figcaption>{t["chapter_word"]} {n + 1}<b>{html.escape(t["chapters"][n])}</b></figcaption></figure>' for n in range(10))
    feats = "".join(f'<div class="feat"><span class="em" aria-hidden="true">{e}</span><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>'
                    for e, h, p in t["features"])
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in t["faq"])
    guides = "".join(f'<a href="{h}">{html.escape(label)} →</a>' for label, h in t["guides"])
    canonical = f"https://hyapps.app{t['path']}"
    app_ld = {
        "@context": "https://schema.org", "@type": ["VideoGame", "MobileApplication"], "name": "Glowfly: Idle Brick Breaker",
        "alternateName": "Glowfly", "operatingSystem": "iOS 18 or later", "applicationCategory": "GameApplication",
        "applicationSubCategory": "Idle game, merge game, casual game", "genre": ["Idle", "Merge", "Casual"],
        "description": t["desc"], "url": canonical, "inLanguage": lang, "image": "https://hyapps.app/glowfly/img/icon.png",
        "screenshot": [f"https://hyapps.app/glowfly/img/ch{n}.jpg" for n in (1, 5, 8, 10)],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "gamePlatform": ["iPhone", "iPad"], "playMode": "SinglePlayer", "numberOfPlayers": {"@type": "QuantitativeValue", "value": 1},
        "keywords": ("idle game, merge game, relaxing game, offline progress, idle merge, fireflies, night sky, casual game"
                     if lang == "en" else "idle oyun, birleştirme oyunu, rahatlatıcı oyun, kapalıyken ilerleme, ateşböceği, gece gökyüzü"),
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
  <meta name="theme-color" content="#0b1023">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en" href="https://hyapps.app/glowfly/">
  <link rel="alternate" hreflang="tr" href="https://hyapps.app/glowfly/tr/">
  <link rel="alternate" hreflang="x-default" href="https://hyapps.app/glowfly/">{itunes}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="HY Apps">
  <meta property="og:title" content="{html.escape(t["title"])}">
  <meta property="og:description" content="{html.escape(t["desc"])}">
  <meta property="og:image" content="https://hyapps.app/assets/og/glowfly-{lang}.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="{"en_US" if lang == "en" else "tr_TR"}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/glowfly/img/icon.png">
  <link rel="apple-touch-icon" href="/glowfly/img/icon.png">
  <link rel="stylesheet" href="/glowfly/glowfly.css">
  <script type="application/ld+json">{json.dumps(app_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
  {ANALYTICS}
</head>
<body>
<header class="bar">
  <a class="brand" href="./"><img src="{i}icon.png" alt="" width="28" height="28">Glowfly</a>
  <nav><a href="#story">{t["nav_story"]}</a><a href="#support">{t["nav_support"]}</a>
    <span class="lang"><a href="{en_href}" hreflang="en" lang="en"{en_on}>EN</a><a href="{tr_href}" hreflang="tr" lang="tr"{tr_on}>TR</a></span></nav>
</header>

<section class="hero">
  <img class="icon" src="{i}icon.png" alt="Glowfly app icon" width="112" height="112">
  <p class="eyebrow">{html.escape(t["eyebrow"])}</p>
  <h1>{t["h1"]}</h1>
  <p class="lead">{html.escape(t["lead"])}</p>
  {store_button(t)}
  <p class="note">{html.escape(t["note"])}</p>
  <div class="hero-shots">
    <img src="{i}ch1.jpg" alt="{html.escape(t["chapters"][0])}" width="600" height="900">
    <img src="{i}ch5.jpg" alt="{html.escape(t["chapters"][4])}" width="600" height="900">
    <img src="{i}ch10.jpg" alt="{html.escape(t["chapters"][9])}" width="600" height="900">
  </div>
</section>

<main>
  <section class="features">{feats}</section>

  <section class="chapters" id="story">
    <p class="kicker">{html.escape(t["story_kicker"])}</p>
    <h2>{html.escape(t["story_h"])}</h2>
    <div class="cards">{cards}</div>
  </section>

  <section class="support" id="support">
    <h2>{html.escape(t["support_h"])}</h2>
    <p class="card">{t["contact"].format(mail=mail)}</p>
    {faq}
  </section>

  <section class="support">
    <h2>{html.escape(t["guides_h"])}</h2>
    <div class="guides-links">{guides}</div>
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
        h="Privacy Policy", date="Glowfly: Idle Brick Breaker · Effective November 7, 2026",
        sections=[
            (None, "Glowfly is an idle game. It needs no account, asks for no personal information and does not track you "
                   "across other apps or websites. This page explains, in plain words, what data the game uses and why."),
            ("No account", "You do not need an account to play. We never ask for your name, e-mail address, contacts or location."),
            ("Stored on your device and in your iCloud", "Your progress and settings are stored on your device. If iCloud is "
             "on, the game also keeps a backup of your progress in your own iCloud (iCloud key-value storage) so it can be "
             "restored on a new device. We cannot see or read this data; it is handled by Apple under "
             "<a href=\"https://www.apple.com/legal/privacy/\">Apple's privacy policy</a>."),
            ("Game Center", "Game Center is optional. If you are signed in, the game sends your furthest night and your "
             "achievements to Game Center, which Apple runs. You can manage what others see in the Settings app."),
            ("Notifications", "If you allow notifications, the game schedules reminders on your device (for example when "
             "the daily gift is ready). They are created on the device itself; nothing is sent to a server."),
            ("Purchases", "Glowfly Plus, the ad-free option and gem packs are bought through the App Store. Payment is "
             "handled entirely by Apple; we never see your payment details or your Apple Account. The game only learns "
             "which product was bought so it can unlock it."),
            ("Anonymous statistics", "To learn which parts of the game are too slow or too hard, the App Store version "
             "sends anonymous events through Google Firebase Analytics: for example which night or chapter was reached, "
             "when a new light was made, which skills and boosts were chosen, which screens were opened" + (", whether a reward " if STORE else ". ")
             + ("video was watched and which product was bought (without any payment details). " if STORE else "") + "Firebase also uses a random "
             "app-instance identifier and an approximate (country/region level) location derived from the network. "
             "This data contains no name, e-mail address or advertising identifier, is not linked to your identity and is "
             "not used for tracking. Google processes it under the "
             "<a href=\"https://firebase.google.com/support/privacy\">Firebase privacy terms</a>. Test and TestFlight "
             "builds send nothing."),
            ("Reward videos (ads)", "Glowfly never shows ads on its own. Some rewards can be earned by choosing to watch a "
             "short video ad, served by Google AdMob. When an ad is requested, Google receives information such as your "
             "device type, iOS version, IP address (used for an approximate location), and how you interact with the ad, "
             "in order to deliver the ad, measure it and prevent fraud. The game does not ask for permission to track you "
             "and does not use the advertising identifier (IDFA). In the EU, the UK and Switzerland the game asks for your "
             "consent through Google's consent form first, and you can change your choice later. With Glowfly Plus or "
             "the ad-free option you get these rewards without ads. Google's practices are described at "
             "<a href=\"https://policies.google.com/technologies/partner-sites\">How Google uses information from sites or apps that use its services</a>."),
            ("This website", "hyapps.app uses Cloudflare Web Analytics, which counts visits without cookies and without "
             "identifying you."),
            ("Children", "Glowfly is not directed at children under 13 and collects no personal data from anyone." + (" Purchases "
             "are protected by your Apple Account and Screen Time settings." if STORE else "")),
            ("Your choices", "You can turn off notifications and iCloud at any time in the Settings app, " + ("play without "
             "ever watching an ad, and " if STORE else "and ") + "delete all your data by deleting the app (and its iCloud backup in Settings → "
             "your name → iCloud)."),
            ("Changes and contact", "If this policy changes, the new version will be posted on this page with a new date. "
             "Questions: <a href=\"mailto:hyapps@outlook.com?subject=Glowfly\">hyapps@outlook.com</a>."),
        ]),
    "tr": dict(
        h="Gizlilik Politikası", date="Glowfly: Idle Işık Birleştirme · Yürürlük: 7 Kasım 2026",
        sections=[
            (None, "Glowfly bir idle oyundur. Hesap gerektirmez, kişisel bilgi istemez, seni başka uygulama ve sitelerde "
                   "izlemez. Bu sayfa oyunun hangi verileri neden kullandığını sade bir dille anlatır."),
            ("Hesap yok", "Oynamak için hesap gerekmez. Adını, e-posta adresini, kişilerini ya da konumunu hiçbir zaman istemeyiz."),
            ("Cihazında ve iCloud'unda saklananlar", "İlerlemen ve ayarların cihazında saklanır. iCloud açıksa oyun, yeni bir "
             "cihazda geri yüklenebilsin diye ilerlemenin bir yedeğini kendi iCloud'unda (iCloud anahtar-değer deposu) tutar. "
             "Bu verileri göremeyiz ve okuyamayız; Apple tarafından "
             "<a href=\"https://www.apple.com/tr/legal/privacy/\">Apple'ın gizlilik politikası</a> kapsamında işlenir."),
            ("Game Center", "Game Center isteğe bağlıdır. Giriş yaptıysan oyun en ileri geceni ve başarımlarını Apple'ın "
             "işlettiği Game Center'a gönderir. Başkalarının ne göreceğini Ayarlar uygulamasından yönetebilirsin."),
            ("Bildirimler", "Bildirimlere izin verirsen oyun cihazında hatırlatmalar kurar (örneğin günlük hediye hazır "
             "olduğunda). Bunlar cihazın kendisinde oluşturulur; hiçbir sunucuya bir şey gönderilmez."),
            ("Satın almalar", "Glowfly Plus, reklamsız seçenek ve elmas paketleri App Store üzerinden satın alınır. Ödemeyi "
             "tamamen Apple yürütür; ödeme bilgilerini ya da Apple Hesabını görmeyiz. Oyun yalnız hangi ürünün alındığını "
             "öğrenir ki onu açabilsin."),
            ("Anonim istatistikler", "Oyunun hangi kısmının fazla yavaş ya da zor olduğunu anlamak için App Store sürümü "
             "Google Firebase Analytics ile anonim olaylar gönderir: örneğin hangi geceye ya da bölüme ulaşıldığı, ne zaman "
             "yeni bir ışık yapıldığı, hangi becerilerin ve takviyelerin seçildiği" + (", hangi ekranların açıldığı, ödüllü bir "
             "videonun izlenip izlenmediği ve hangi ürünün alındığı (ödeme bilgisi olmadan). " if STORE else " ve hangi ekranların açıldığı. ") + "Firebase ayrıca rastgele bir "
             "uygulama kimliği ve ağdan çıkarılan yaklaşık (ülke/bölge düzeyinde) konum kullanır. Bu veriler ad, e-posta ya "
             "da reklam kimliği içermez, kimliğine bağlanmaz ve izleme için kullanılmaz. Google bunları "
             "<a href=\"https://firebase.google.com/support/privacy\">Firebase gizlilik koşulları</a> kapsamında işler. "
             "Test ve TestFlight sürümleri hiçbir şey göndermez."),
            ("Ödüllü videolar (reklam)", "Glowfly kendiliğinden hiçbir reklam göstermez. Bazı ödüller, Google AdMob'un "
             "sunduğu kısa bir video reklamı izlemeyi seçerek kazanılabilir. Reklam istendiğinde Google, reklamı göstermek, "
             "ölçmek ve sahtekârlığı önlemek için cihaz türü, iOS sürümü, IP adresi (yaklaşık konum için) ve reklamla nasıl "
             "etkileşime girdiğin gibi bilgileri alır. Oyun seni izlemek için izin istemez ve reklam kimliğini (IDFA) "
             "kullanmaz. AB, Birleşik Krallık ve İsviçre'de oyun önce Google'ın onay formuyla iznini ister; seçimini sonra "
             "değiştirebilirsin. Glowfly Plus ya da reklamsız seçenekle bu ödülleri reklamsız alırsın. Google'ın "
             "uygulamaları: <a href=\"https://policies.google.com/technologies/partner-sites?hl=tr\">Google, hizmetlerini "
             "kullanan site veya uygulamalardaki bilgileri nasıl kullanır</a>."),
            ("Bu web sitesi", "hyapps.app, ziyaretleri çerezsiz ve seni tanımadan sayan Cloudflare Web Analytics kullanır."),
            ("Çocuklar", "Glowfly 13 yaşından küçük çocuklara yönelik değildir ve kimseden kişisel veri toplamaz." + (" Satın "
             "almalar Apple Hesabın ve Ekran Süresi ayarlarınla korunur." if STORE else "")),
            ("Seçimlerin", "Bildirimleri ve iCloud'u istediğin zaman Ayarlar uygulamasından kapatabilir" + (", hiç reklam izlemeden "
             "oynayabilir" if STORE else "") + " ve uygulamayı (ve Ayarlar → adın → iCloud'daki yedeğini) silerek bütün verilerini silebilirsin."),
            ("Değişiklikler ve iletişim", "Bu politika değişirse yeni hâli yeni tarihle bu sayfada yayınlanır. Sorular için: "
             "<a href=\"mailto:hyapps@outlook.com?subject=Glowfly\">hyapps@outlook.com</a>."),
        ]),
}


# Sections that only exist in store builds (purchases, AdMob reward videos).
STORE_ONLY = {"Purchases", "Reward videos (ads)", "Satın almalar", "Ödüllü videolar (reklam)"}


def privacy():
    body = []
    for lang in ("en", "tr"):
        p = PRIVACY[lang]
        anchor = ' id="tr"' if lang == "tr" else ""
        body.append(f'<section lang="{lang}"{anchor}><h1>{p["h"]}</h1><p class="muted">{html.escape(p["date"])}</p>')
        for h, text in p["sections"]:
            if not STORE and h in STORE_ONLY:
                continue
            if h:
                body.append(f"<h2>{html.escape(h)}</h2>")
            body.append(f"<p>{text}</p>")
        body.append("</section>")
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Glowfly Privacy Policy · Gizlilik Politikası</title>
  <meta name="description" content="Glowfly privacy policy: no account, no tracking, no personal data; anonymous statistics{" and optional reward videos" if STORE else ""}.">
  <link rel="canonical" href="https://hyapps.app/glowfly/privacy.html">
  <link rel="icon" href="/glowfly/img/icon.png">
  <link rel="stylesheet" href="/glowfly/glowfly.css">
  {ANALYTICS}
</head>
<body class="policy">
<main>
  <nav class="crumbs"><a href="/">HY Apps</a> · <a href="./">Glowfly</a> · <a href="./#support">Support</a> · <a href="#tr">Türkçe</a></nav>
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


write("glowfly/index.html", page(T["en"]))
write("glowfly/tr/index.html", page(T["tr"]))
write("glowfly/privacy.html", privacy())

#!/usr/bin/env python3
"""Builds the Besmele / Bismillah landing pages (TR at /besmele/, EN at /besmele/en/).

Usage: python3 -I tools/build_besmele.py   (run from the site repo root)
Support and privacy pages next to them (destek.html, gizlilik.html) come from
Hikmet/Araclar/site_uret.py, which must not write index.html.
Images: besmele/img/<lang>_<n>.jpg are the App Store screenshots (Hikmet/Magaza/ekranlar).
"""
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ID = "6821501310"

T = {
    "tr": dict(
        lang="tr", name="Besmele", path="/besmele/", img="img/", store=f"https://apps.apple.com/tr/app/id{APP_ID}",
        title="Besmele · Namaz Vakitleri, Sesli Kur'an ve Kıble (iPhone)",
        desc="Besmele; namaz vakitleri ve ezan, sesli Kur'an ve meal, kıble pusulası, kaza takibi, zikirmatik ve her gün bir ayet, "
             "hadis ve dua. Reklamsız, sade ve büyük yazılı iPhone uygulaması.",
        og_desc="Namaz vakitleri, sesli Kur'an, kıble ve günlük ibadet için sade ve reklamsız bir yol arkadaşı.",
        nav_features="Özellikler", nav_support="Destek",
        eyebrow="iPhone için sade ve reklamsız",
        h1="Her namaz için<br><em>sakin bir yol arkadaşı.</em>",
        lead="Namaz vakitleri ve ezan, sesli Kur'an, kıble ve her gün beş güzel söz. Büyük yazılar, kolay ekranlar, her yaş için.",
        cta="App Store'dan indir", cta_note="Ücretsiz · iPhone",
        marquee=["Namaz vakitleri", "Ezan bildirimi", "Sesli Kur'an ve meal", "Kıble pusulası", "Kaza takibi",
                 "Zikirmatik", "Esmaül Hüsna", "Reklam yok"],
        features=[
            (1, "Namaz vakitleri", "Vakti hiç kaçırma.",
             "Bulunduğun şehre göre doğru vakitler (Türkiye'de Diyanet hesabı). Her vakit için ayrı bildirim: ezan sesi, kanun ya da telefonun sesi; vakit girince ya da 10, 15, 30 dakika önce."),
            (2, "Kur'an-ı Kerim", "Dinle, oku, kaldığın yerden sür.",
             "114 sûre mushaf yazısıyla Arapça ve meal. Ayet ayet ya da sûrenin tamamını dinle; kilit ekranında da sürer. Dinlediğin ayetler işaretlenir, Kur'an radyosu sûreleri art arda okur."),
            (4, "Kıble", "Telefonu çevir, kıbleyi bul.",
             "Kâbe simgesi oka geldiğinde kıble yönündesin. Dünyanın her yerinde çalışır."),
            (7, "Her gün beş güzel söz", "Bir ayet, bir hadis, bir dua.",
             "Allah'ın güzel isimlerinden biri ve günün sözüyle birlikte her gün beş güzel söz. Beğendiklerini kaydet, güzel kartlarla sevdiklerine gönder."),
            (6, "İbadet araçları", "Kaza namazı ve zikir, tek yerde.",
             "Kılamadığın namazları gir, kıldıkça düşsün. Zikirmatik ile dokunarak say, hedefte titreşsin. Dini günler takvimi ve 99 isim gün gün."),
            (3, "Widget", "Vakitler ana ekranında.",
             "Ana ekranda ve kilit ekranında günün namaz vakitleri, sıradaki vakit ve kalan süre. Günün Ayeti ve Günün İsmi widget'ları."),
        ],
        stats=[("114", "sûre, sesli"), ("99", "güzel isim"), ("5", "güzel söz her gün"), ("0", "reklam")],
        fair_h="Reklamsız. Sade. Senin.",
        fair="Temel özelliklerin hepsi ücretsiz ve reklam yok. Konumun telefonundan dışarı çıkmaz. İsteğe bağlı, tek seferlik Besmele Plus farklı hafızlar, ek kart tasarımları, Kur'an sayfa renkleri ve widget renkleri açar; dilersen bahşişle de destek olabilirsin.",
        support_h="Destek",
        contact="Soru, öneri ya da bir hata bildirmek için bize {mail} adresinden yaz.",
        faq=[
            ("Namaz vakitleri camimizin takviminden farklı.",
             "Türkiye'de vakitler Diyanet yöntemiyle hesaplanır. Başka ülkelerde ülkeye uygun yöntem otomatik seçilir. Ayarlar → Hesaplama yöntemi bölümünden değiştirebilirsin."),
            ("Bildirim gelmiyor.",
             "Uygulamanın Ayarlar ekranında bildirimin açık olduğundan ve telefonunun Ayarlar → Bildirimler → Besmele bölümünde iznin verildiğinden emin ol. Bildirimler, uygulamayı her açtığında önümüzdeki 7 gün için yeniden hazırlanır; arada bir uygulamayı açman yeterli."),
            ("Kıble pusulası yanlış gösteriyor.",
             "Telefonu düz tut, metal eşyalardan ve mıknatıslı kılıflardan uzaklaştır. Telefonu havada 8 çizer gibi birkaç kez hareket ettirmek pusulayı düzeltir."),
            ("Bir günü kaçırdım, ilerlemem silindi mi?",
             "Hayır. Öğrendiğin isimler ve serin silinmez; kaldığın yerden devam edersin."),
        ],
        more="Tüm destek sayfası", support_href="destek.html", privacy_href="gizlilik.html", footer_privacy="Gizlilik politikası",
        final_h="Bugünün ayeti seni bekliyor.",
        made="Bağımsız bir geliştirici tarafından yapıldı.",
        alt="Besmele ekran görüntüsü",
    ),
    "en": dict(
        lang="en", name="Bismillah", path="/besmele/en/", img="../img/", store=f"https://apps.apple.com/app/id{APP_ID}",
        title="Bismillah · Prayer Times, Quran Audio and Qibla for iPhone",
        desc="Bismillah is a calm, ad-free companion for prayer times with adhan, the Qur'an with audio and translation, "
             "a Qibla compass, a missed prayer tracker, a dhikr counter and a daily verse, hadith and dua.",
        og_desc="A calm, ad-free companion for prayer times, the Qur'an, the Qibla and daily worship.",
        nav_features="Features", nav_support="Support",
        eyebrow="Simple and ad-free, for iPhone",
        h1="A calm companion<br><em>for every prayer.</em>",
        lead="Prayer times with adhan, the Qur'an with audio, the Qibla and five beautiful passages every day. Large text and simple screens for all ages.",
        cta="Download on the App Store", cta_note="Free · iPhone",
        marquee=["Prayer times", "Adhan alerts", "Qur'an with audio", "Qibla compass", "Missed prayers",
                 "Dhikr counter", "99 Names", "No ads"],
        features=[
            (1, "Prayer times", "Never miss a prayer.",
             "Accurate prayer times for your city, anywhere in the world. A separate alert for each prayer: adhan, qanun or your phone's sound, at prayer time or 10, 15 or 30 minutes before."),
            (2, "The Holy Qur'an", "Listen, read, continue where you left off.",
             "All 114 surahs in mushaf script with translation. Listen verse by verse or the whole surah; it keeps playing on the lock screen. Verses you listened to are marked, and Qur'an Radio plays surahs one after another."),
            (4, "Qibla", "Turn your phone, find the Qibla.",
             "When the Kaaba reaches the arrow, you are facing the Qibla. Works worldwide."),
            (7, "Five passages a day", "A verse, a hadith, a dua.",
             "Plus one of Allah's Beautiful Names and a word of wisdom, every day. Save your favorites and share them as beautiful cards."),
            (6, "Tools for worship", "Missed prayers and dhikr in one place.",
             "Enter the prayers you missed and check them off as you make them up. Count dhikr by tapping, with a vibration at your goal. Learn the 99 Names, one a day."),
            (3, "Widgets", "Prayer times on your Home Screen.",
             "Today's prayer times, the next prayer and the time left on your Home and Lock Screen. Verse of the Day and Name of the Day widgets."),
        ],
        stats=[("114", "surahs with audio"), ("99", "Beautiful Names"), ("5", "passages a day"), ("0", "ads")],
        fair_h="No ads. Simple. Yours.",
        fair="All core features are free and there are no ads. Your location never leaves your phone. An optional one-time Bismillah Plus purchase unlocks more reciters, extra card designs, Qur'an page colors and widget colors; you can also leave a tip to support development.",
        support_h="Support",
        contact="For questions, suggestions or to report a problem, write to us at {mail}.",
        faq=[
            ("Prayer times differ from my mosque's calendar.",
             "The calculation method is chosen automatically for your country. You can change it in Settings → Calculation method."),
            ("I don't get notifications.",
             "Make sure notifications are on in the app's Settings and allowed in your phone's Settings → Notifications → Bismillah. Notifications are prepared for the next 7 days each time you open the app, so open it now and then."),
            ("The Qibla compass looks wrong.",
             "Hold your phone flat, away from metal objects and magnetic cases. Moving the phone in a figure 8 a few times recalibrates the compass."),
            ("I missed a day. Is my progress lost?",
             "No. Your learned names and streak are kept; just continue where you left off."),
        ],
        more="Full support page", support_href="destek.html", privacy_href="gizlilik.html", footer_privacy="Privacy policy",
        final_h="Today's verse is waiting.",
        made="Made with care by an independent developer.",
        alt="Bismillah screenshot",
    ),
}


def poster(src, alt, cls=""):
    return (f'<div class="poster {cls}"><img src="{src}" alt="{html.escape(alt)}" width="500" height="1086" '
            f'loading="lazy" decoding="async"></div>')


MORE = {
    "en": ("More from HY Apps", "/crownly/", "/crownly/img/icon.png", "Crownly",
           "A calm daily logic puzzle with hints that explain the logic.", "All apps", "/"),
    "tr": ("HY Apps'in diğer uygulamaları", "/crownly/tr/", "/crownly/img/icon.png", "Crownly",
           "Mantığı anlatan ipuçlarıyla sakin bir günlük bulmaca.", "Tüm uygulamalar", "/tr/"),
}


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
    en = "en/" if t["lang"] == "tr" else "./"
    tr = "./" if t["lang"] == "tr" else "../"
    on = lambda l: ' class="on" aria-current="page"' if t["lang"] == l else ""
    return (f'<span class="lang"><a href="{en}" hreflang="en" lang="en"{on("en")}>EN</a>'
            f'<a href="{tr}" hreflang="tr" lang="tr"{on("tr")}>TR</a></span>')


def page(t):
    i, L = t["img"], t["lang"]
    shot = lambda n: f"{i}{L}_{n}.jpg"
    mail = '<a href="mailto:hyapps@outlook.com?subject=Besmele">hyapps@outlook.com</a>'
    marquee = "".join(f"<span>{html.escape(m)}</span><b>☾</b>" for m in t["marquee"])
    feats = []
    for k, (n, kicker, h, body) in enumerate(t["features"]):
        feats.append(f'''
  <section class="feature {"flip" if k % 2 else ""} reveal">
    <div class="feature-media">{poster(shot(n), f"{t['alt']}: {kicker}", "tilt")}</div>
    <div class="feature-text">
      <p class="kicker">{html.escape(kicker)}</p>
      <h2>{html.escape(h)}</h2>
      <p>{html.escape(body)}</p>
    </div>
  </section>''')
    stats = "".join(f'<div><strong>{s}</strong><span>{html.escape(l)}</span></div>' for s, l in t["stats"])
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in t["faq"])
    canonical = f"https://hyapps.app{t['path']}"
    return f'''<!doctype html>
<html lang="{L}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(t["title"])}</title>
  <meta name="description" content="{html.escape(t["desc"])}">
  <meta name="theme-color" content="#0f3324">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="tr" href="https://hyapps.app/besmele/">
  <link rel="alternate" hreflang="en" href="https://hyapps.app/besmele/en/">
  <link rel="alternate" hreflang="x-default" href="https://hyapps.app/besmele/en/">
  <meta name="apple-itunes-app" content="app-id={APP_ID}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(t["title"])}">
  <meta property="og:description" content="{html.escape(t["og_desc"])}">
  <meta property="og:image" content="https://hyapps.app/besmele/img/icon.png">
  <meta property="og:url" content="{canonical}">
  <link rel="icon" href="{i}icon.png">
  <link rel="apple-touch-icon" href="{i}icon.png">
  <link rel="stylesheet" href="/assets/app.css">
  <link rel="stylesheet" href="/besmele/besmele.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"MobileApplication","name":"{t["name"]}","operatingSystem":"iOS",
   "applicationCategory":"LifestyleApplication","url":"{canonical}","installUrl":"{t["store"]}","inLanguage":"{L}",
   "offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}},
   "publisher":{{"@type":"Organization","name":"HY Apps","url":"https://hyapps.app/"}}}}
  </script>
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
  <div class="crescent" aria-hidden="true"></div>
  <div class="hero-copy">
    <img class="hero-icon" src="{i}icon.png" alt="{t["name"]}" width="96" height="96">
    <p class="eyebrow">{html.escape(t["eyebrow"])}</p>
    <h1>{t["h1"]}</h1>
    <p class="lead">{html.escape(t["lead"])}</p>
    <a class="store" href="{t["store"]}">{html.escape(t["cta"])}</a>
    <p class="cta-note">{html.escape(t["cta_note"])}</p>
  </div>
  <div class="stage" id="stage">
    {poster(shot(2), t["alt"], "side left")}
    {poster(shot(1), t["alt"], "center")}
    {poster(shot(7), t["alt"], "side right")}
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="track">{marquee}{marquee}</div></div>

<main id="features">
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
    <p style="margin-top:18px"><a href="{t["support_href"]}">{html.escape(t["more"])} →</a></p>
  </section>
{more(t)}
</main>

<section class="final">
  <div class="blobs" aria-hidden="true"><i></i><i></i><i></i></div>
  <img src="{i}icon.png" alt="" width="88" height="88">
  <h2>{html.escape(t["final_h"])}</h2>
  <a class="store" href="{t["store"]}">{html.escape(t["cta"])}</a>
</section>

<footer class="foot">
  <a href="/">HY Apps</a><a href="{t["privacy_href"]}">{t["footer_privacy"]}</a><a href="{t["support_href"]}">{t["nav_support"]}</a>
  <a href="mailto:hyapps@outlook.com">hyapps@outlook.com</a>
  <p>{html.escape(t["made"])} © 2026 HY Apps</p>
</footer>
<script src="/assets/app.js" defer></script>
</body>
</html>
'''


for key, out in (("tr", "besmele/index.html"), ("en", "besmele/en/index.html")):
    path = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(page(T[key]))
    print("wrote", out)

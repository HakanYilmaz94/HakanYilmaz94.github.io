#!/usr/bin/env python3
"""Builds the SEO guide pages and the sitemap.

Usage: python3 -I tools/build_guides.py   (run from the site repo root)

- Besmele: Esmaül Hüsna hub + 99 name pages (TR /besmele/esma/, EN /besmele/en/names/) from the app's own data
  (Hikmet/Ortak/icerik.json, icerik_en.json), plus two how-to guides per language.
- Crownly: Queens rules, strategy and "LinkedIn Queens alternative" guides (EN + TR).
- Quick Wits: one-phone party games, a reaction time test (with a live test on the page) and group games for game night.
- Brickhaven: a cozy offline building game page and a beginner's guide.
Apps whose builder still has LIVE = False get a "coming soon" badge instead of the store button and no Smart App Banner.
- sitemap.xml for the whole site.
Shared look: /assets/app.css (+ /besmele/besmele.css). Analytics snippet and share tags on every page.
"""
import html
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIKMET = os.path.join(os.path.dirname(ROOT), "Hikmet", "Ortak")
SITE = "https://hyapps.app"
PT = "?pt=129592179&ct=web&mt=8"
ANALYTICS = ("<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
             "data-cf-beacon='{\"token\": \"89e9ceae59114244a972f60af4a20851\"}'></script><!-- End Cloudflare Web Analytics -->")
ESC = html.escape
PAGES = []  # (path, {lang: path} alternates) for the sitemap

APPS = {
    "crownly": dict(id="6822852151", css=[], theme="#2b1a42", icon="/crownly/img/icon.png",
                    name={"en": "Crownly", "tr": "Crownly"}, home={"en": "/crownly/", "tr": "/crownly/tr/"},
                    og={"en": "/assets/og/crownly-en.jpg", "tr": "/assets/og/crownly-tr.jpg"},
                    cta_h={"en": "Play a new Queens puzzle every day", "tr": "Her gün yeni bir Queens bulmacası çöz"},
                    cta_p={"en": "Crownly: a daily puzzle, 2,000 levels and hints that explain the logic. Free on iPhone.",
                           "tr": "Crownly: günlük bulmaca, 2.000 seviye ve mantığı anlatan ipuçları. iPhone'da ücretsiz."}),
    "besmele": dict(id="6821501310", css=["/besmele/besmele.css"], theme="#0f3324", icon="/besmele/img/icon.png",
                    name={"en": "Bismillah", "tr": "Besmele"}, home={"en": "/besmele/en/", "tr": "/besmele/"},
                    og={"en": "/assets/og/besmele-en.jpg", "tr": "/assets/og/besmele-tr.jpg"},
                    cta_h={"en": "Learn one Beautiful Name every day", "tr": "Her gün bir güzel isim öğren"},
                    cta_p={"en": "Bismillah: prayer times, the Qur'an with audio, the Qibla and a daily verse. Free and ad-free on iPhone.",
                           "tr": "Besmele: namaz vakitleri, sesli Kur'an, kıble ve her gün bir ayet. iPhone'da ücretsiz ve reklamsız."}),
    "quickwits": dict(id="6826451513", css=[], theme="#17123a", icon="/quickwits/img/icon.png",
                      name={"en": "Quick Wits", "tr": "Kıvrak Zeka"}, home={"en": "/quickwits/", "tr": "/quickwits/tr/"},
                      og={"en": "/assets/og/quickwits-en.jpg", "tr": "/assets/og/quickwits-tr.jpg"},
                      cta_h={"en": "87 quick games for your next game night", "tr": "Bir sonraki oyun gecen için 87 kısa oyun"},
                      cta_p={"en": "Quick Wits: reflex duels, guessing, memory and group games. Pass one phone or open an online room. Free on iPhone.",
                             "tr": "Kıvrak Zeka: refleks düelloları, tahmin, hafıza ve grup oyunları. Tek telefonu dolaştır ya da online oda aç. iPhone'da ücretsiz."}),
    "brickhaven": dict(id="6826958666", css=["/brickhaven/guide.css"], theme="#2f9fa8", icon="/brickhaven/img/icon.png",
                       name={"en": "Brickhaven", "tr": "Brickhaven"}, home={"en": "/brickhaven/", "tr": "/brickhaven/tr/"},
                       og={"en": "/assets/og/brickhaven-en.jpg", "tr": "/assets/og/brickhaven-tr.jpg"},
                       cta_h={"en": "Rebuild a seaside town, one brick at a time", "tr": "Bir sahil kasabasını tuğla tuğla yeniden kur"},
                       cta_p={"en": "Brickhaven: a cozy building game for iPhone and iPad. Offline, no timers, no ads. The first two buildings are free.",
                              "tr": "Brickhaven: iPhone ve iPad için rahat bir inşa oyunu. İnternetsiz, zamanlayıcısız, reklamsız. İlk iki bina ücretsiz."}),
}


def is_live(app):
    """Reads LIVE from the app's landing-page builder, so the store button flips with one change there."""
    builder = os.path.join(ROOT, "tools", f"build_{app}.py")
    with open(builder) as f:
        m = re.search(r"^LIVE = (True|False)", f.read(), re.M)
    return m is None or m.group(1) == "True"


for _app in APPS:
    APPS[_app]["live"] = is_live(_app)

STORE_LABEL = {"en": "Download on the App Store", "tr": "App Store'dan indir"}
SOON_LABEL = {"en": "Coming soon to the App Store", "tr": "Yakında App Store'da"}
MADE = {"en": "Made with care by an independent developer.", "tr": "Bağımsız bir geliştirici tarafından yapıldı."}
PRIVACY = {"crownly": {"en": "/crownly/privacy.html", "tr": "/crownly/privacy.html#tr"},
           "besmele": {"en": "/besmele/en/gizlilik.html", "tr": "/besmele/gizlilik.html"},
           "quickwits": {"en": "/quickwits/privacy.html", "tr": "/quickwits/privacy.html#tr"},
           "brickhaven": {"en": "/brickhaven/privacy.html", "tr": "/brickhaven/privacy.html#tr"}}
PRIVACY_LABEL = {"en": "Privacy policy", "tr": "Gizlilik politikası"}


def store_url(app, lang):
    country = "tr/" if lang == "tr" else ""
    return f"https://apps.apple.com/{country}app/apple-store/id{APPS[app]['id']}{PT}"


def slug(text):
    t = text.replace("ı", "i").replace("İ", "I")
    for q in "’‘'`ʼ":
        t = t.replace(q, "")
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    out, dash = [], False
    for c in t.lower():
        if c.isalnum() and c.isascii():
            out.append(c); dash = False
        elif not dash:
            out.append("-"); dash = True
    return "".join(out).strip("-")


def write(path, text):
    full = os.path.join(ROOT, path.lstrip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)


def lang_pill(lang, alts):
    on = lambda l: ' class="on" aria-current="page"' if l == lang else ""
    links = "".join(f'<a href="{alts[l]}" hreflang="{l}" lang="{l}"{on(l)}>{l.upper()}</a>' for l in ("en", "tr") if l in alts)
    return f'<span class="lang">{links}</span>'


def page(app, lang, path, alts, title, desc, body, crumbs, schema=None, head=""):
    """Renders one guide page. alts = {lang: path} for hreflang; crumbs = [(label, href)]; head = extra <head> markup."""
    a = APPS[app]
    itunes = f'\n  <meta name="apple-itunes-app" content="app-id={a["id"]}">' if a["live"] else ""
    store = (f'<a class="store" href="{ESC(store_url(app, lang))}">{ESC(STORE_LABEL[lang])}</a>' if a["live"]
             else f'<span class="store" aria-disabled="true">{ESC(SOON_LABEL[lang])}</span>')
    PAGES.append((path, alts))
    hreflang = "".join(f'\n  <link rel="alternate" hreflang="{l}" href="{SITE}{p}">' for l, p in alts.items())
    if "en" in alts:
        hreflang += f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}{alts["en"]}">'
    css = "".join(f'\n  <link rel="stylesheet" href="{c}">' for c in a["css"])
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + h} for i, (n, h) in enumerate(crumbs)]}
    art = {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
           "inLanguage": lang, "mainEntityOfPage": SITE + path,
           "publisher": {"@type": "Organization", "name": "HY Apps", "url": SITE + "/"}}
    schemas = [bc, art] + ([schema] if schema else [])
    ld = "\n  ".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    crumb_html = " › ".join(f'<a href="{h}">{ESC(n)}</a>' for n, h in crumbs[:-1])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{ESC(title)}</title>
  <meta name="description" content="{ESC(desc)}">
  <meta name="theme-color" content="{a["theme"]}">
  <link rel="canonical" href="{SITE}{path}">{hreflang}{itunes}
  <meta property="og:type" content="article">
  <meta property="og:title" content="{ESC(title)}">
  <meta property="og:description" content="{ESC(desc)}">
  <meta property="og:url" content="{SITE}{path}">
  <meta property="og:image" content="{SITE}{a["og"][lang]}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{a["icon"]}">
  <link rel="apple-touch-icon" href="{a["icon"]}">
  <link rel="stylesheet" href="/assets/app.css">{css}{head}
  {ld}
  {ANALYTICS}
</head>
<body>
<header class="bar">
  <a class="brand" href="{a["home"][lang]}"><img src="{a["icon"]}" alt="" width="28" height="28">{a["name"][lang]}</a>
  <nav>{lang_pill(lang, alts)}</nav>
</header>
<article class="article">
  <p class="crumbs">{crumb_html}</p>
{body}
  <div class="cta-card">
    <img src="{a["icon"]}" alt="" width="72" height="72">
    <h2>{ESC(a["cta_h"][lang])}</h2>
    <p>{ESC(a["cta_p"][lang])}</p>
    {store}
  </div>
</article>
<footer class="foot">
  <a href="{"/tr/" if lang == "tr" else "/"}">HY Apps</a><a href="{a["home"][lang]}">{a["name"][lang]}</a>
  <a href="{PRIVACY[app][lang]}">{PRIVACY_LABEL[lang]}</a><a href="mailto:hyapps@outlook.com">hyapps@outlook.com</a>
  <p>{ESC(MADE[lang])} © 2026 HY Apps</p>
</footer>
</body>
</html>
'''


def paras(*ps):
    return "\n".join(f"  <p>{p}</p>" for p in ps)


def related(title, links):
    items = "".join(f'<a href="{h}">{ESC(t)} →</a>' for t, h in links)
    return f'  <div class="related"><p class="kicker">{ESC(title)}</p>{items}</div>'


# ---------------------------------------------------------------- Besmele: Esmaül Hüsna

def load_names(file):
    with open(os.path.join(HIKMET, file)) as f:
        data = json.load(f)
    return [s for day in data for s in day["sozler"] if s["kategori"] == "esma"]


NAMES = {"tr": load_names("icerik.json"), "en": load_names("icerik_en.json")}
assert len(NAMES["tr"]) == len(NAMES["en"]) == 99
NAME_BASE = {"tr": "/besmele/esma/", "en": "/besmele/en/names/"}


def name_path(lang, i):
    return f"{NAME_BASE[lang]}{i + 1}-{slug(NAMES[lang][i]['baslik'])}/"


T_ESMA = {
    "tr": dict(hub_title="Esmaül Hüsna: Allah'ın 99 İsmi ve Anlamları",
               hub_desc="Esmaül Hüsna, Allah'ın 99 güzel ismi: Arapça yazılışları, okunuşları ve kısa anlamlarıyla tam liste.",
               hub_intro="Esmaül Hüsna, \"en güzel isimler\" demektir ve Allah'ın Kur'an'da ve hadislerde geçen güzel isimlerini ifade eder. "
                         "Aşağıda 99 ismin Arapça yazılışını, Türkçe okunuşunu ve kısa anlamını bulabilirsin. Her isme dokunarak ayrıntısını aç.",
               crumbs_home="Besmele", crumbs_hub="Esmaül Hüsna",
               page_title="{name} ne demek? Anlamı ve Arapçası · Esmaül Hüsna",
               page_desc="{name} ({ar}) Esmaül Hüsna'dan, Allah'ın 99 isminden {n}. isimdir. Anlamı: {meaning}",
               nth="Esmaül Hüsna · {n}. isim", meaning_h="Anlamı",
               about="{name}, Allah'ın güzel isimlerinden biridir ve Esmaül Hüsna listesinde {n}. sırada yer alır. "
                     "Besmele uygulamasında her gün bir isim, anlamıyla birlikte ana sayfada gösterilir; böylece 99 ismi gün gün öğrenebilirsin.",
               prev="‹ Önceki isim", next="Sonraki isim ›", all="Tüm 99 isim",
               note="Okunuş ve anlamlar Besmele uygulamasındaki metinlerden alınmıştır.",
               related="Daha fazla", other_guides=[("Kıble yönü nasıl bulunur?", "/besmele/kible-nasil-bulunur/"),
                                                    ("Namaz vakitleri nasıl hesaplanır?", "/besmele/namaz-vakitleri-nasil-hesaplanir/")]),
    "en": dict(hub_title="The 99 Names of Allah (Asma ul Husna) with Meanings",
               hub_desc="The 99 Beautiful Names of Allah (Asma ul Husna): full list with Arabic script, transliteration and meaning.",
               hub_intro="Al-Asma al-Husna means \"the most beautiful names\": the names of Allah found in the Qur'an and the hadith. "
                         "Below are all 99 names with their Arabic script, transliteration and a short meaning. Tap a name to open it.",
               crumbs_home="Bismillah", crumbs_hub="99 Names of Allah",
               page_title="{name} meaning: {ar} · 99 Names of Allah",
               page_desc="{name} ({ar}) is name {n} of the 99 Names of Allah (Asma ul Husna). Meaning: {meaning}",
               nth="99 Names of Allah · name {n}", meaning_h="Meaning",
               about="{name} is one of the Beautiful Names of Allah and number {n} in the list of the 99 Names. "
                     "The Bismillah app shows one name with its meaning on the home screen every day, so you can learn all 99, one day at a time.",
               prev="‹ Previous name", next="Next name ›", all="All 99 names",
               note="Transliterations and meanings are taken from the Bismillah app.",
               related="More", other_guides=[("How to find the Qibla direction", "/besmele/en/how-to-find-qibla/"),
                                              ("How prayer times are calculated", "/besmele/en/how-prayer-times-are-calculated/")]),
}


def build_esma():
    for lang in ("tr", "en"):
        t, names = T_ESMA[lang], NAMES[lang]
        other = "en" if lang == "tr" else "tr"
        hub = NAME_BASE[lang]
        crumbs = [(t["crumbs_home"], APPS["besmele"]["home"][lang]), (t["crumbs_hub"], hub)]
        items = "".join(
            f'<li><a href="{name_path(lang, i)}"><span class="ar" lang="ar">{ESC(n["arapca"])}</span>'
            f'<strong>{i + 1}. {ESC(n["baslik"])}</strong><span class="m">{ESC(n["metin"])}</span></a></li>'
            for i, n in enumerate(names))
        body = (f'  <h1>{ESC(t["hub_title"])}</h1>\n  <p class="intro">{ESC(t["hub_intro"])}</p>\n'
                f'  <ol class="names">{items}</ol>\n  <p class="note">{ESC(t["note"])}</p>\n' + related(t["related"], t["other_guides"]))
        schema = {"@context": "https://schema.org", "@type": "ItemList", "name": t["hub_title"], "numberOfItems": 99,
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n["baslik"], "url": SITE + name_path(lang, i)}
                                      for i, n in enumerate(names)]}
        write(hub, page("besmele", lang, hub, {lang: hub, other: NAME_BASE[other]}, t["hub_title"], t["hub_desc"], body, crumbs, schema))
        for i, n in enumerate(names):
            p = name_path(lang, i)
            fmt = dict(name=n["baslik"], ar=n["arapca"], n=i + 1, meaning=n["metin"])
            pager = '<div class="pager">'
            pager += f'<a href="{name_path(lang, i - 1)}">{ESC(t["prev"])}</a>' if i > 0 else "<span></span>"
            pager += f'<a href="{hub}">{ESC(t["all"])}</a>'
            pager += f'<a href="{name_path(lang, i + 1)}">{ESC(t["next"])}</a>' if i < 98 else "<span></span>"
            pager += "</div>"
            body = (f'  <div class="name-hero"><span class="name-num">{ESC(t["nth"].format(**fmt))}</span>'
                    f'<div class="ar" lang="ar">{ESC(n["arapca"])}</div><h1 style="margin:0">{ESC(n["baslik"])}</h1></div>\n'
                    f'  <h2>{ESC(t["meaning_h"])}</h2>\n  <p class="intro">{ESC(n["metin"])}</p>\n'
                    f'  <p>{ESC(t["about"].format(**fmt))}</p>\n  {pager}\n')
            write(p, page("besmele", lang, p, {lang: p, other: name_path(other, i)},
                          t["page_title"].format(**fmt), t["page_desc"].format(**fmt), body,
                          crumbs + [(n["baslik"], p)]))


# ---------------------------------------------------------------- Besmele: how-to guides

def build_besmele_guides():
    q = {"tr": "/besmele/kible-nasil-bulunur/", "en": "/besmele/en/how-to-find-qibla/"}
    pt = {"tr": "/besmele/namaz-vakitleri-nasil-hesaplanir/", "en": "/besmele/en/how-prayer-times-are-calculated/"}
    esma = {"tr": ("Esmaül Hüsna: Allah'ın 99 ismi", NAME_BASE["tr"]), "en": ("The 99 Names of Allah", NAME_BASE["en"])}
    home = {"tr": ("Besmele", "/besmele/"), "en": ("Bismillah", "/besmele/en/")}
    G = {
        ("qibla", "tr"): ("Kıble Yönü Nasıl Bulunur? Telefonla Kolay Yöntem",
            "Kıble yönünü telefonun pusulasıyla bulmanın adımları, pusulanın neden şaşabileceği ve nasıl düzeltileceği.",
            "Kıble, namazda yönelinen Mekke'deki Kâbe'nin yönüdür. Bulunduğun yerden Kâbe'ye giden en kısa yol (büyük daire) hesaplanır ve bu yön pusula ile gösterilir.",
            [("Telefonla kıble bulma", ["Besmele'de Kıble ekranını aç; konumun telefonundan dışarı çıkmadan yön hesaplanır.",
                                        "Telefonu yere paralel, düz tut.", "Kâbe simgesi okun ucuna gelene kadar kendi etrafında dön.",
                                        "Simge ok ile hizalanınca kıble yönündesin; telefon hafifçe titreşir."]),
             ("Pusula yanlış gösteriyorsa", ["Metal eşyalardan, hoparlörlerden ve mıknatıslı kılıflardan uzaklaş.",
                                             "Telefonu havada birkaç kez 8 çizer gibi hareket ettir; pusula kendini kalibre eder.",
                                             "Konum izninin açık olduğundan emin ol: yön, bulunduğun yere göre hesaplanır."])],
            "Kıble yönü dünyanın her yerinde farklıdır: Türkiye'den güneydoğuya, Avrupa'nın çoğundan güneydoğuya, Amerika'dan ise kuzeydoğuya doğrudur. Bu yüzden harita üzerinde düz çizgi yerine küresel hesap kullanılır."),
        ("qibla", "en"): ("How to Find the Qibla Direction with Your Phone",
            "Step-by-step: find the Qibla with your phone's compass, why the compass can be off and how to fix it.",
            "The Qibla is the direction of the Kaaba in Mecca, which Muslims face in prayer. The shortest path (great circle) from where you are to the Kaaba is calculated and shown with your compass.",
            [("Finding the Qibla with your phone", ["Open the Qibla screen in Bismillah; the direction is calculated on your phone, your location never leaves it.",
                                                    "Hold your phone flat, parallel to the ground.", "Turn around until the Kaaba icon reaches the arrow.",
                                                    "When the icon lines up with the arrow you are facing the Qibla; the phone gives a gentle tap."]),
             ("If the compass looks wrong", ["Move away from metal objects, speakers and magnetic cases.",
                                             "Move your phone in a figure 8 a few times to recalibrate the compass.",
                                             "Make sure location access is on: the direction depends on where you are."])],
            "The Qibla points a different way in every place: south-east from Turkey and most of Europe, north-east from North America. That is why a spherical calculation is used instead of a straight line on a flat map."),
        ("times", "tr"): ("Namaz Vakitleri Nasıl Hesaplanır?",
            "İmsak, güneş, öğle, ikindi, akşam ve yatsı vakitlerinin güneşin konumuna göre nasıl hesaplandığı ve takvimler arasındaki farkın nedeni.",
            "Namaz vakitleri güneşin gökyüzündeki konumuna göre belirlenir. Bu yüzden her şehirde ve her gün farklıdır; konumun ve tarih bilinirse hesaplanabilir.",
            [("Vakitler ve güneş", ["İmsak (sabah): şafak sökerken, güneş ufkun belli bir derece altındayken başlar.",
                                    "Güneş: güneşin doğduğu an.", "Öğle: güneş en yüksek noktasını geçtikten hemen sonra.",
                                    "İkindi: bir cismin gölgesi belli bir uzunluğa ulaştığında.", "Akşam: güneş battığında.",
                                    "Yatsı: akşam kızıllığı kaybolup gökyüzü karardığında."]),
             ("Takvimler neden farklı?", ["İmsak ve yatsı için güneşin ufkun kaç derece altında sayılacağı yöntemden yönteme değişir (genelde 15–18 derece).",
                                          "Bazı kurumlar güvenlik payı (temkin) olarak birkaç dakika ekler ya da çıkarır.",
                                          "Besmele Türkiye'de Diyanet yöntemini, diğer ülkelerde o ülkede yaygın yöntemi otomatik seçer; Ayarlar → Hesaplama yöntemi bölümünden değiştirebilirsin."])],
            "Camindeki takvimle birkaç dakikalık fark görürsen sebebi genellikle yöntem ya da temkin farkıdır. Hangi yöntemi kullanacağını yerel camine ya da müftülüğe danışabilirsin."),
        ("times", "en"): ("How Are Prayer Times Calculated?",
            "How Fajr, sunrise, Dhuhr, Asr, Maghrib and Isha are calculated from the position of the sun, and why prayer timetables differ.",
            "Prayer times follow the position of the sun in the sky. That is why they change every day and in every city, and why they can be calculated from your location and the date.",
            [("The prayers and the sun", ["Fajr: dawn, when the sun is a certain angle below the horizon.", "Sunrise: the moment the sun rises.",
                                          "Dhuhr: just after the sun passes its highest point.", "Asr: when an object's shadow reaches a certain length.",
                                          "Maghrib: at sunset.", "Isha: when the twilight has gone and the sky is dark."]),
             ("Why timetables differ", ["Methods use different sun angles below the horizon for Fajr and Isha (usually between 15 and 18 degrees).",
                                        "Some authorities add or subtract a few minutes as a safety margin.",
                                        "Bismillah picks the common method for your country automatically; you can change it in Settings → Calculation method."])],
            "If your mosque's timetable differs by a few minutes, the reason is usually a different method or safety margin. Your local mosque can tell you which method they follow."),
    }
    links = {"qibla": q, "times": pt}
    for (key, lang), (title, desc, intro, sections, outro) in G.items():
        path = links[key][lang]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(intro)}</p>\n'
        for h, items in sections:
            body += f'  <h2>{ESC(h)}</h2>\n  <ol>' + "".join(f"<li>{ESC(i)}</li>" for i in items) + "</ol>\n"
        body += paras(ESC(outro)) + "\n"
        others = [(T_ESMA[lang]["other_guides"][0 if key == "times" else 1]), esma[lang]]
        body += related(T_ESMA[lang]["related"], others)
        write(path, page("besmele", lang, path, links[key], title, desc, body, [home[lang], (title, path)]))


# ---------------------------------------------------------------- Crownly: Queens guides

BOARD = ["AABBB", "ACCBB", "DCCEB", "DDCEE", "DDEEE"]
CROWNS = {(2, 0), (0, 1), (3, 2), (1, 3), (4, 4)}
REGION = {"A": "#CDBEEB", "B": "#B9D3F2", "C": "#F6CFA8", "D": "#C5E0B5", "E": "#F2B8C6"}
CROWN = ('<span class="crown"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 18h18l-1.6-9.2-4.6 3.8L12 5.5 9.2 12.6 4.6 8.8z" '
         'fill="#E3AE2C" stroke="#8a5a00" stroke-width=".8" stroke-linejoin="round"/></svg></span>')


def board(label):
    cells = []
    for r, row in enumerate(BOARD):
        for c, reg in enumerate(row):
            e = [n for n, cond in (("et", r == 0 or BOARD[r - 1][c] != reg), ("eb", r == 4 or BOARD[r + 1][c] != reg),
                                   ("el", c == 0 or BOARD[r][c - 1] != reg), ("er", c == 4 or BOARD[r][c + 1] != reg)) if cond]
            cells.append(f'<div class="cell {" ".join(e)}" style="background:{REGION[reg]}">{CROWN if (r, c) in CROWNS else ""}</div>')
    return f'  <div class="board" role="img" aria-label="{ESC(label)}">{"".join(cells)}</div>\n'


TECH = {
    "en": [("Crown's reach", "A crown rules out its row, its column, its region and every cell touching it, diagonals included. Mark those cells with a dot right away."),
           ("Last cell", "If a region, row or column has only one open cell left, the crown must go there."),
           ("Region in one line", "If all open cells of a region sit in a single row (or column), that region's crown is in that line, so every other cell of the line is out."),
           ("Line inside one region", "If all open cells of a row (or column) belong to one region, the row's crown is that region's crown: the rest of the region is out."),
           ("Group squeeze", "If two regions can only fit in the same two rows, those two rows belong to them, and every other region's cells in those rows are out. The same works for three regions in three rows."),
           ("Blocking cell", "Imagine a crown on a cell. If it would leave some region, row or column with no open cell, that cell can't hold a crown.")],
    "tr": [("Tacın etki alanı", "Bir taç; satırını, sütununu, bölgesini ve çapraz dahil değdiği her hücreyi eler. Bu hücrelere hemen nokta koy."),
           ("Son hücre", "Bir bölgede, satırda ya da sütunda tek boş hücre kaldıysa taç oraya gelir."),
           ("Tek hatta sıkışan bölge", "Bir bölgenin tüm boş hücreleri tek bir satırdaysa (ya da sütundaysa) o bölgenin tacı o hattadır; hattın geri kalanı elenir."),
           ("Tek bölgeye ait hat", "Bir satırın (ya da sütunun) tüm boş hücreleri tek bir bölgedeyse satırın tacı o bölgenin tacıdır; bölgenin geri kalanı elenir."),
           ("Grup sıkışması", "İki bölge yalnızca aynı iki satıra sığıyorsa o iki satır onlarındır; başka bölgelerin o satırlardaki hücreleri elenir. Üç bölge ve üç satır için de geçerlidir."),
           ("Engelleyen hücre", "Bir hücreye taç koyduğunu düşün. Bu taç bir bölgede, satırda ya da sütunda hiç boş hücre bırakmıyorsa o hücreye taç gelemez.")],
}

CG = {
    "en": dict(
        home=("Crownly", "/crownly/"),
        rules=("/crownly/queens-puzzle-rules/", "How to Play Queens: Rules of the Queens Logic Puzzle",
               "The rules of the Queens puzzle (also known as Star Battle) explained simply: one crown per row, column and region, and crowns never touch."),
        strategy=("/crownly/queens-strategy/", "Queens Puzzle Strategy: 6 Techniques to Solve Any Board",
                  "Six logical techniques that solve every Queens puzzle without guessing, from crown's reach to group squeezes."),
        alt=("/crownly/linkedin-queens-alternative/", "LinkedIn Queens Alternative: Play Queens Every Day on iPhone",
             "Love the LinkedIn Queens game? Crownly is a free iPhone app with a new Queens puzzle every day, 2,000 levels and hints that explain the logic."),
        board_label="A solved 5×5 Queens puzzle", related="More guides"),
    "tr": dict(
        home=("Crownly", "/crownly/tr/"),
        rules=("/crownly/tr/queens-nasil-oynanir/", "Queens Nasıl Oynanır? Queens Mantık Bulmacası Kuralları",
               "Queens bulmacasının (Star Battle olarak da bilinir) kuralları sade bir dille: her satıra, sütuna ve bölgeye bir taç; taçlar birbirine dokunmaz."),
        strategy=("/crownly/tr/queens-stratejileri/", "Queens Bulmacası Taktikleri: Her Tahtayı Çözen 6 Teknik",
                  "Her Queens bulmacasını tahmin etmeden çözen altı mantık tekniği: tacın etki alanından grup sıkışmasına."),
        alt=("/crownly/tr/linkedin-queens-alternatifi/", "LinkedIn Queens Alternatifi: iPhone'da Her Gün Queens Oyna",
             "LinkedIn'deki Queens oyununu seviyor musun? Crownly her gün yeni bir Queens bulmacası, 2.000 seviye ve mantığı anlatan ipuçları sunan ücretsiz bir iPhone uygulaması."),
        board_label="Çözülmüş 5×5 Queens bulmacası", related="Diğer rehberler"),
}


def build_crownly_guides():
    for lang in ("en", "tr"):
        g = CG[lang]
        other = CG["tr" if lang == "en" else "en"]
        alts = lambda key: {lang: g[key][0], ("tr" if lang == "en" else "en"): other[key][0]}
        rel = lambda skip: related(g["related"], [(g[k][1].split(":")[0], g[k][0]) for k in ("rules", "strategy", "alt") if k != skip])
        en = lang == "en"

        # Rules
        path, title, desc = g["rules"]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        body += f'  <h2>{"The rules" if en else "Kurallar"}</h2>\n  <ol>' + "".join(f"<li>{ESC(x)}</li>" for x in (
            ["Place exactly one crown in every row.", "Place exactly one crown in every column.",
             "Place exactly one crown in every colored region.", "Crowns may not touch each other, not even diagonally."] if en else
            ["Her satıra tam bir taç koy.", "Her sütuna tam bir taç koy.", "Her renkli bölgeye tam bir taç koy.",
             "Taçlar birbirine dokunamaz, çapraz olarak da."])) + "</ol>\n"
        body += board(g["board_label"])
        body += paras(*([ESC("On an N×N board there are N rows, N columns and N regions, so a solved board always has exactly N crowns. "
                             "A good puzzle has exactly one solution and can be solved with logic alone, without guessing."),
                         ESC("Queens is a version of the classic Star Battle puzzle with one star per line. It became popular as a quick daily "
                             "game; in some apps crowns are drawn as queens, in Crownly they are golden crowns.")] if en else
                        [ESC("N×N bir tahtada N satır, N sütun ve N bölge vardır; bu yüzden çözülmüş tahtada her zaman tam N taç bulunur. "
                             "İyi bir bulmacanın tek çözümü vardır ve tahmin etmeden, yalnızca mantıkla çözülür."),
                         ESC("Queens, hat başına bir yıldızlı klasik Star Battle bulmacasının bir türüdür. Kısa bir günlük oyun olarak "
                             "popüler oldu; bazı uygulamalarda vezir, Crownly'de altın taç olarak çizilir.")])) + "\n"
        body += f'  <h2>{"How to start" if en else "Nasıl başlanır"}</h2>\n  <ol>' + "".join(f"<li>{ESC(x)}</li>" for x in (
            ["Look for the smallest region or a region squeezed into one row or column.",
             "Mark cells that can't hold a crown with a dot (tap once in Crownly). Dots are as important as crowns.",
             "Every time you place a crown, dot its row, column, region and the eight cells around it.",
             "When you get stuck, look for a region whose open cells all sit in one line."] if en else
            ["En küçük bölgeye ya da tek bir satıra veya sütuna sıkışmış bölgeye bak.",
             "Taç gelemeyecek hücrelere nokta koy (Crownly'de bir dokunuş). Noktalar taçlar kadar önemlidir.",
             "Her taç koyduğunda satırına, sütununa, bölgesine ve çevresindeki sekiz hücreye nokta koy.",
             "Takılınca boş hücrelerinin hepsi tek bir hatta olan bir bölge ara."])) + "</ol>\n"
        body += rel("rules")
        write(path, page("crownly", lang, path, alts("rules"), title, desc, body, [g["home"], (title, path)]))

        # Strategy
        path, title, desc = g["strategy"]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        for i, (h, p) in enumerate(TECH[lang]):
            body += f"  <h2>{i + 1}. {ESC(h)}</h2>\n  <p>{ESC(p)}</p>\n"
        body += paras(ESC("Crownly's hints use exactly these techniques: when you are stuck, a hint names the technique, highlights the "
                          "row, column or region it is about and explains the step. The Logic School has a short interactive lesson for each one."
                          if en else
                          "Crownly'nin ipuçları tam olarak bu teknikleri kullanır: takıldığında ipucu tekniğin adını söyler, ilgili satırı, sütunu "
                          "ya da bölgeyi vurgular ve adımı açıklar. Mantık okulunda her teknik için kısa, etkileşimli bir ders var.")) + "\n"
        body += rel("strategy")
        write(path, page("crownly", lang, path, alts("strategy"), title, desc, body, [g["home"], (title, path)]))

        # LinkedIn Queens alternative
        path, title, desc = g["alt"]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        body += paras(*([ESC("LinkedIn's Queens is one puzzle a day, and then it's over until tomorrow. If you want more, Crownly gives you the same "
                             "kind of puzzle with the same rules (one crown in every row, column and region, no touching), designed as a calm iPhone game."),] if en else
                        [ESC("LinkedIn'deki Queens günde bir bulmaca sunar, sonra ertesi güne kadar bitti. Daha fazlasını istiyorsan Crownly aynı "
                             "kurallarla (her satıra, sütuna ve bölgeye bir taç, taçlar birbirine dokunmaz) aynı türde bulmacalar sunan sakin bir iPhone oyunu.")]))
        whats_in = "What you get in Crownly" if en else "Crownly'de neler var"
        body += f'\n  <h2>{whats_in}</h2>\n  <ul>' +"".join(f"<li>{ESC(x)}</li>" for x in (
            ["A new daily puzzle at the same time for everyone, plus a 10×10 Daily Hard.",
             "2,000 levels from Easy to Expert, with up to three stars each.",
             "Hints that explain the next logical step instead of revealing the answer.",
             "A Logic School with six interactive lessons.",
             "Streaks, streak freezes, Game Center leaderboards and widgets.",
             "Color-blind mode, dark mode, no ads, works offline."] if en else
            ["Herkese aynı anda gelen yeni bir günlük bulmaca ve 10×10 Günlük Zor.",
             "Kolaydan Uzmana 2.000 seviye, her birinde üç yıldıza kadar.",
             "Cevabı vermek yerine sıradaki mantıklı adımı anlatan ipuçları.",
             "Altı etkileşimli dersten oluşan Mantık okulu.",
             "Seri, seri dondurma, Game Center sıralamaları ve widget'lar.",
             "Renk körü modu, koyu tema, reklamsız, internetsiz oynanır."])) + "</ul>\n"
        body += paras(ESC("Crownly is an independent app and is not affiliated with or endorsed by LinkedIn. Queens and Star Battle are names of a puzzle type."
                          if en else "Crownly bağımsız bir uygulamadır; LinkedIn ile bir bağlantısı yoktur ve LinkedIn tarafından desteklenmez. "
                          "Queens ve Star Battle bir bulmaca türünün adlarıdır.")).replace("<p>", '<p class="note">') + "\n"
        body += rel("alt")
        write(path, page("crownly", lang, path, alts("alt"), title, desc, body, [g["home"], (title, path)]))


# ---------------------------------------------------------------- Quick Wits: party game guides

def steps(h, items, ordered=True):
    tag = "ol" if ordered else "ul"
    return f'  <h2>{ESC(h)}</h2>\n  <{tag}>' + "".join(f"<li>{ESC(i)}</li>" for i in items) + f"</{tag}>\n"


def defs(h, items):
    """A heading followed by named items: [(name, text)]."""
    return f'  <h2>{ESC(h)}</h2>\n' + "".join(f"  <h3>{ESC(n)}</h3>\n  <p>{ESC(t)}</p>\n" for n, t in items)


QG = {
    "en": dict(
        home=("Quick Wits", "/quickwits/"), related="More guides",
        phone=("/quickwits/games-to-play-with-friends-on-one-phone/", "Games to Play with Friends on One Phone",
               "How pass-and-play party games work on one iPhone, which kinds of games suit them best, and how to run a great game night with up to 8 players."),
        reaction=("/quickwits/reaction-time-test/", "Reaction Time Test: How Fast Are Your Reflexes?",
                  "Test your reaction time right here: tap when the box turns green. What is a normal reaction time, why it changes and how to get faster."),
        group=("/quickwits/group-games-for-game-night/", "Group Games for Game Night: 7 Mind Games for 3 to 12 Players",
               "Seven group games where your score depends on what everyone else picks: majority, minority, two thirds of the average and more. Rules and tactics."),
    ),
    "tr": dict(
        home=("Kıvrak Zeka", "/quickwits/tr/"), related="Diğer rehberler",
        phone=("/quickwits/tr/tek-telefonla-oynanan-oyunlar/", "Tek Telefonla Arkadaşlarla Oynanacak Oyunlar",
               "Tek iPhone'u elden ele dolaştırarak oynanan parti oyunları nasıl işler, hangi oyunlar buna uygun ve 8 kişilik keyifli bir oyun gecesi nasıl kurulur."),
        reaction=("/quickwits/tr/refleks-testi/", "Refleks Testi: Tepki Süren Kaç Milisaniye?",
                  "Tepki süreni hemen burada ölç: kutu yeşile dönünce dokun. Normal tepki süresi kaç ms, neden değişir ve nasıl hızlanırsın?"),
        group=("/quickwits/tr/oyun-gecesi-grup-oyunlari/", "Oyun Gecesi İçin Grup Oyunları: 3–12 Kişilik 7 Akıl Oyunu",
               "Puanının herkesin seçimine bağlı olduğu yedi grup oyunu: çoğunluk, azınlık, ortalamanın üçte ikisi ve daha fazlası. Kurallar ve taktikler."),
    ),
}

RT_TEXT = {
    "en": dict(start="Tap to start", start_sub="Wait for green, then tap as fast as you can.", wait="Wait for green…", wait_sub="",
               go="Tap!", early="Too soon!", again="Tap to try again.", next="Try {n} of 5. Tap for the next one.",
               avg="Your average: {ms} ms. Tap to start over.", label="Reaction time test"),
    "tr": dict(start="Başlamak için dokun", start_sub="Yeşili bekle, sonra olabildiğince hızlı dokun.", wait="Yeşili bekle…", wait_sub="",
               go="Dokun!", early="Çok erken!", again="Tekrar denemek için dokun.", next="5 denemeden {n}. Sıradaki için dokun.",
               avg="Ortalaman: {ms} ms. Baştan başlamak için dokun.", label="Refleks testi"),
}

RT_STYLE = """
  <style>
    .rt { display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 6px; width: 100%; min-height: 240px;
          margin: 8px 0 28px; padding: 24px 16px; border: 0; border-radius: 24px; cursor: pointer; font: inherit; color: #fff;
          background: #3d2660; touch-action: manipulation; user-select: none; -webkit-user-select: none; transition: background .08s; }
    .rt strong { font-family: var(--serif); font-size: clamp(34px, 7vw, 54px); line-height: 1.1; }
    .rt span { font-size: 17px; opacity: .9; min-height: 1.6em; }
    .rt.wait { background: #b8402f; } .rt.go { background: #23935a; } .rt.early { background: #8a5a00; }
    .rt:focus-visible { outline: 3px solid var(--gold); outline-offset: 3px; }
  </style>"""


def reaction_widget(lang):
    t = RT_TEXT[lang]
    js = """
  <script>
  (function () {
    var T = %s, b = document.getElementById("rt"), big = b.querySelector("strong"), small = b.querySelector("span");
    var state = "idle", start = 0, timer = 0, results = [];
    function show(cls, a, c) { b.className = "rt " + cls; big.textContent = a; small.textContent = c; }
    function press(e) {
      if (e) e.preventDefault();
      if (state === "wait") { clearTimeout(timer); state = "early"; show("early", T.early, T.again); return; }
      if (state === "go") {
        var ms = Math.round(performance.now() - start);
        results.push(ms); state = "done";
        if (results.length < 5) { show("", ms + " ms", T.next.replace("{n}", results.length)); }
        else {
          var avg = Math.round(results.reduce(function (s, x) { return s + x; }, 0) / results.length);
          show("", ms + " ms", T.avg.replace("{ms}", avg)); results = [];
        }
        return;
      }
      state = "wait"; show("wait", T.wait, T.wait_sub);
      timer = setTimeout(function () { state = "go"; start = performance.now(); show("go", T.go, ""); }, 1500 + Math.random() * 2500);
    }
    b.addEventListener("pointerdown", press);
    b.addEventListener("keydown", function (e) { if ((e.key === " " || e.key === "Enter") && !e.repeat) press(e); });
  })();
  </script>
""" % json.dumps(t, ensure_ascii=False)
    return (f'  <button type="button" class="rt" id="rt" aria-label="{ESC(t["label"])}" aria-live="polite">'
            f'<strong>{ESC(t["start"])}</strong><span>{ESC(t["start_sub"])}</span></button>\n' + js)


def build_quickwits_guides():
    for lang in ("en", "tr"):
        g = QG[lang]
        other = QG["tr" if lang == "en" else "en"]
        alts = lambda key: {lang: g[key][0], ("tr" if lang == "en" else "en"): other[key][0]}
        rel = lambda skip: related(g["related"], [(g[k][1].split(":")[0], g[k][0]) for k in ("phone", "reaction", "group") if k != skip])
        en = lang == "en"

        # One phone, pass and play
        path, title, desc = g["phone"]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        body += paras(ESC("You don't need a deck of cards or a board game box for a good game night. One phone on the table is enough: "
                          "everyone plays the same round in turn, the phone goes to the next person, and the scores come out together at the end."
                          if en else
                          "İyi bir oyun gecesi için deste ya da kutu oyunu gerekmez. Masada tek telefon yeter: herkes aynı turu sırayla oynar, "
                          "telefon sıradakine geçer ve puanlar sonunda birlikte açıklanır.")) + "\n"
        body += steps("How pass-the-phone works" if en else "Telefonu pasla nasıl oynanır",
                      ["Write everyone's name once; up to 4 players are free, up to 8 with the Party Pack.",
                       "Pick a few games and how many rounds each.",
                       "The first player plays a short round, a few seconds long, then hands the phone on.",
                       "Each player gets exactly the same round, so nobody gets an easier question.",
                       "When everyone has played, the results of the round are revealed together."] if en else
                      ["Herkesin adını bir kez yaz; 4 kişiye kadar ücretsiz, Parti Paketi ile 8 kişi.",
                       "Birkaç oyun ve her biri için tur sayısını seç.",
                       "İlk oyuncu birkaç saniyelik kısa turunu oynar, telefonu sıradakine verir.",
                       "Her oyuncuya birebir aynı tur gelir; kimseye daha kolay soru düşmez.",
                       "Herkes oynayınca turun sonuçları birlikte açıklanır."])
        body += defs("Games that work best on one phone" if en else "Tek telefonda en iyi giden oyunlar",
                     [("Reflex", "Quick Draw, Balloon Pop, Star or Bomb and Colour Trap: the whole table watches while one person taps."),
                      ("Visual and memory", "Dot Flash, Odd Shade, Chimp Test and Where Was It?: short, quiet rounds that everybody understands at a glance."),
                      ("Prediction", "Will It Fall?, Billiards, Ballpark, What Year? and Map Pin: guesses spark the most arguments when the answer comes out."),
                      ("The phone itself", "Tilt it, blow into the microphone or count the buzzes: games that only a phone can do.")] if en else
                     [("Refleks", "Silahşor, Balon Patlat, Bombaya Basma ve Renk Tuzağı: biri dokunurken bütün masa izler."),
                      ("Görsel ve hafıza", "Nokta Şimşeği, Farklı Ton, Şempanze Testi ve Neredeydi?: herkesin bir bakışta anladığı kısa, sessiz turlar."),
                      ("Tahmin", "Devrilir mi?, Bilardo, Tahmin Et, Hangi Yıl? ve Haritada Bul: cevap açıklanınca en çok tartışma bunlarda çıkar."),
                      ("Telefonun kendisi", "Eğ, mikrofona üfle ya da titreşimleri say: yalnız bir telefonla oynanabilecek oyunlar.")])
        body += steps("Tips for a great game night" if en else "Keyifli bir oyun gecesi için ipuçları",
                      ["Start with 5 games and 3 rounds each: about 15 minutes for 4 players.",
                       "Mix kinds: a reflex game, a guessing game, a memory game, then a group game.",
                       "With 3 or more players, add a group game; scores depend on what the others pick, which starts the best debates.",
                       "If everyone has their phone, open an online room instead: everyone plays at the same moment, up to 12 players.",
                       "Pass-the-phone works offline, so it's handy on a trip, in a cabin or at a family dinner."] if en else
                      ["5 oyun ve her birinde 3 turla başla: 4 kişi için yaklaşık 15 dakika.",
                       "Türleri karıştır: bir refleks, bir tahmin, bir hafıza, ardından bir grup oyunu.",
                       "3 ve daha fazla kişiyseniz bir grup oyunu ekle; puan diğerlerinin seçimine bağlı olduğu için en güzel tartışmalar orada çıkar.",
                       "Herkesin telefonu yanındaysa online oda aç: herkes aynı anda oynar, 12 kişiye kadar.",
                       "Telefonu pasla internetsiz çalışır; yolculukta, yazlıkta ya da aile yemeğinde işe yarar."], ordered=False)
        body += rel("phone")
        write(path, page("quickwits", lang, path, alts("phone"), title, desc, body, [g["home"], (title, path)]))

        # Reaction time test
        path, title, desc = g["reaction"]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        body += reaction_widget(lang)
        body += f'  <h2>{"What is a normal reaction time?" if en else "Normal tepki süresi kaç ms?"}</h2>\n'
        body += paras(*([ESC("For a simple test like this one, where you react to one signal you are already waiting for, most adults land "
                             "somewhere between 200 and 300 milliseconds. Around 250 ms is typical; under 200 ms is very quick."),
                         ESC("A screen adds its own delay: the display, the touch sensor and the browser all take a few milliseconds, so "
                             "the same person can score differently on different devices. Compare yourself on the same phone, not with a friend's laptop.")] if en else
                        [ESC("Bunun gibi basit bir testte, yani beklediğin tek bir işarete tepki verdiğinde yetişkinlerin çoğu 200 ile 300 "
                             "milisaniye arasında kalır. 250 ms civarı olağandır; 200 ms'nin altı çok hızlıdır."),
                         ESC("Ekranın da kendi gecikmesi var: ekran, dokunmatik algılayıcı ve tarayıcı birkaç milisaniye ekler; aynı kişi farklı "
                             "cihazlarda farklı sonuç alabilir. Kendini arkadaşının bilgisayarıyla değil, aynı telefonla karşılaştır.")])) + "\n"
        body += steps("What changes your reaction time" if en else "Tepki süreni neler değiştirir", (
            ["Sleep and tiredness: a short night slows you down more than almost anything else.",
             "Warming up: the first few tries are usually the slowest.",
             "Attention: looking straight at the spot where the signal comes is faster than looking around it.",
             "Choices: when you must decide what to do (tap the green, not the yellow), reaction time grows."] if en else
            ["Uyku ve yorgunluk: kısa bir gece seni neredeyse her şeyden çok yavaşlatır.",
             "Isınma: ilk birkaç deneme genelde en yavaşıdır.",
             "Dikkat: işaretin geleceği noktaya doğrudan bakmak, çevresine bakmaktan hızlıdır.",
             "Seçim: ne yapacağına karar vermen gerekince (sarıya değil yeşile dokun) tepki süresi uzar."]), ordered=False)
        body += steps("How to get faster" if en else "Nasıl hızlanırsın", (
            ["Rest your finger just above the screen instead of lifting it from far away.",
             "Don't guess the moment: anticipating leads to false starts, which cost more than a slow tap.",
             "Practise little and often; short daily sessions beat one long one.",
             "Play against friends: a little rivalry makes almost everyone faster."] if en else
            ["Parmağını uzaktan kaldırmak yerine ekranın hemen üstünde beklet.",
             "Anı tahmin etmeye çalışma: önceden basmak erken başlamaya yol açar, bu da yavaş dokunuştan pahalıya patlar.",
             "Az ama sık çalış; her gün kısa denemeler tek bir uzun denemeden iyidir.",
             "Arkadaşlarınla yarış: biraz rekabet neredeyse herkesi hızlandırır."]))
        body += paras(ESC("Quick Wits turns this into a party game: in Quick Draw two or more players wait for green and the first to tap wins, "
                          "with a yellow bait to catch the jumpy ones. Balloon Pop, Star or Bomb and Colour Trap test reflexes with a decision on top. "
                          "Timing is measured on each player's own phone, so a slow connection never costs points."
                          if en else
                          "Kıvrak Zeka bunu bir parti oyununa çevirir: Silahşor'da iki ya da daha fazla oyuncu yeşili bekler, ilk dokunan kazanır; "
                          "aceleci olanları yakalamak için bir de sarı tuzak var. Balon Patlat, Bombaya Basma ve Renk Tuzağı refleksin üstüne bir karar ekler. "
                          "Süre her oyuncunun kendi telefonunda ölçülür; yavaş bağlantı puan kaybettirmez.")) + "\n"
        body += rel("reaction")
        write(path, page("quickwits", lang, path, alts("reaction"), title, desc, body, [g["home"], (title, path)], head=RT_STYLE))

        # Group games
        path, title, desc = g["group"]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        body += paras(ESC("In most quiz games there is one right answer. In these there isn't: the answer that scores is the one that fits "
                          "the group. You have to guess how your friends think, which is why they work best with 3 to 12 people who know each other."
                          if en else
                          "Çoğu bilgi yarışmasında tek bir doğru cevap vardır. Bunlarda yok: puan getiren cevap, gruba uyan cevaptır. "
                          "Arkadaşlarının nasıl düşündüğünü tahmin etmen gerekir; bu yüzden birbirini tanıyan 3 ila 12 kişiyle en iyi gider.")) + "\n"
        games = ([("Crowd Mind", "There is no right answer, only the majority. Everyone answers the same question in secret; the most popular answer scores best. Tactic: pick the obvious answer, not your favourite."),
                  ("Minority Wins", "Two options, one secret pick. Everyone on the side fewer people chose wins. Tactic: if the table looks predictable, go against it, but so will the others."),
                  ("Two Thirds", "Everyone picks a number from 0 to 100. The target is two thirds of the average of all picks. A classic of game theory: in theory everyone should say 0, in real groups the winning number is usually much higher."),
                  ("Lowest Unique", "Pick a number from 1 to 20. The smallest number that only one person picked wins. Tactic: 1 and 2 are crowded; the sweet spot is often a little higher."),
                  ("Same Wavelength", "A clue sits between two extremes, like 'cold' and 'hot'. Place the marker where you think it belongs; the closer to the group's middle, the more points."),
                  ("Dilemma", "A would-you-rather question. Make your own pick, then guess what share of the table picked the first option."),
                  ("Place Your Bets", "An estimation question. Type your guess, then bet on who will be closest, which can be you.")] if en else
                 [("Çoğunluk", "Doğru cevap yok, yalnız çoğunluk var. Herkes aynı soruyu gizlice cevaplar; en çok seçilen cevap en çok puanı alır. Taktik: en sevdiğini değil, en akla geleni seç."),
                  ("Azınlık Kazanır", "İki seçenek, gizli bir seçim. Daha az kişinin seçtiği taraftaki herkes kazanır. Taktik: masa tahmin edilebilir görünüyorsa tersine git; ama diğerleri de öyle düşünebilir."),
                  ("Üçte İki", "Herkes 0 ile 100 arasında bir sayı seçer. Hedef, tüm seçimlerin ortalamasının üçte ikisidir. Oyun kuramının bir klasiği: kâğıt üstünde herkes 0 demeli, gerçek gruplarda kazanan sayı çoğu zaman çok daha yüksektir."),
                  ("En Küçük Tek", "1 ile 20 arasında bir sayı seç. Yalnız bir kişinin seçtiği en küçük sayı kazanır. Taktik: 1 ve 2 kalabalıktır; doğru yer çoğu zaman biraz daha yukarıdadır."),
                  ("Aynı Frekans", "Bir ipucu iki uç arasında durur, örneğin 'soğuk' ve 'sıcak'. İşareti ait olduğunu düşündüğün yere koy; grubun ortasına ne kadar yakınsan o kadar puan."),
                  ("İkilem", "Bir 'hangisini seçerdin' sorusu. Kendi seçimini yap, sonra masanın yüzde kaçının ilk seçeneği seçtiğini tahmin et."),
                  ("Bahisler Açıldı", "Bir tahmin sorusu. Tahminini yaz, sonra en yakın kimin olacağına bahis koy; bu sen de olabilirsin.")])
        body += defs("The games" if en else "Oyunlar", games)
        body += paras(ESC("In Quick Wits these games run in a pass-the-phone match or in an online room where everyone answers at the same "
                          "moment on their own phone; results appear together so nobody can copy. Mix them with a few reflex rounds for a full evening."
                          if en else
                          "Kıvrak Zeka'da bu oyunlar telefonu pasla maçında ya da herkesin aynı anda kendi telefonundan cevap verdiği online odada "
                          "oynanır; sonuçlar birlikte açıklanır, kimse kopya çekemez. Dolu bir akşam için araya birkaç refleks turu ekle.")) + "\n"
        body += rel("group")
        write(path, page("quickwits", lang, path, alts("group"), title, desc, body, [g["home"], (title, path)]))


# ---------------------------------------------------------------- Brickhaven: cozy building guides

BG = {
    "en": dict(
        home=("Brickhaven", "/brickhaven/"), related="More guides",
        cozy=("/brickhaven/cozy-offline-building-game/", "A Cozy Offline Building Game for iPhone and iPad",
              "Looking for a relaxing game with no timers, no ads and no internet needed? Brickhaven lets you rebuild a seaside town one brick at a time."),
        tips=("/brickhaven/beginners-guide/", "Brickhaven Beginner's Guide: 8 Tips to Build Faster",
              "Eight tips for new builders: reading the blueprint, carrying more bricks, which skills to pick first and designing your own house."),
    ),
    "tr": dict(
        home=("Brickhaven", "/brickhaven/tr/"), related="Diğer rehberler",
        cozy=("/brickhaven/tr/internetsiz-rahatlatici-insa-oyunu/", "İnternetsiz, Rahatlatıcı Bir İnşa Oyunu: iPhone ve iPad",
              "Zamanlayıcısız, reklamsız, internet gerektirmeyen sakin bir oyun mu arıyorsun? Brickhaven'da bir sahil kasabasını tuğla tuğla yeniden kurarsın."),
        tips=("/brickhaven/tr/baslangic-rehberi/", "Brickhaven Başlangıç Rehberi: Daha Hızlı İnşa İçin 8 İpucu",
              "Yeni ustalar için sekiz ipucu: planı okumak, daha çok tuğla taşımak, önce hangi yetenekleri almak ve kendi evini tasarlamak."),
    ),
}


def build_brickhaven_guides():
    for lang in ("en", "tr"):
        g = BG[lang]
        other = BG["tr" if lang == "en" else "en"]
        alts = lambda key: {lang: g[key][0], ("tr" if lang == "en" else "en"): other[key][0]}
        rel = lambda skip: related(g["related"], [(g[k][1].split(":")[0], g[k][0]) for k in ("cozy", "tips") if k != skip])
        en = lang == "en"
        shot = lambda b, alt: f'  <img class="shot" src="/brickhaven/img/{lang}-{b}.jpg" alt="{ESC(alt)}" width="720" height="480" loading="lazy">\n'

        # Cozy offline building game
        path, title, desc = g["cozy"]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        body += shot("kafe", "The Seaside Café in Brickhaven" if en else "Brickhaven'da Sahil Kafesi")
        body += paras(ESC("A cozy game is one you can open after a long day without any pressure: nothing chases you, nothing runs out, and "
                          "every minute you play leaves something nice behind. Brickhaven is built around that idea."
                          if en else
                          "Rahat (cozy) oyun, uzun bir günün sonunda hiçbir baskı hissetmeden açabileceğin oyundur: seni kovalayan bir şey yoktur, "
                          "hiçbir şey tükenmez ve oynadığın her dakika geride güzel bir şey bırakır. Brickhaven bu fikir üzerine kuruldu.")) + "\n"
        body += defs("What you do in Brickhaven" if en else "Brickhaven'da ne yaparsın", (
            [("Build with your own hands", "Walk to the brick pile, find the right shape and color, carry it to the wall and lay it. Row by row, a bakery, a barn or a clock tower rises in front of you."),
             ("Bring the town back to life", "Grandma Rose left you a seaside town that has fallen to ruin. Each finished building brings its owner home, from Martha's bakery to the train station."),
             ("Design and decorate", "Draw your own house, café or shop at the Architect's Table, build it on your lot, then add benches, lamps, flower beds, trees, cats and chickens.")] if en else
            [("Kendi ellerinle inşa et", "Tuğla yığınına yürü, doğru şekli ve rengi bul, duvara taşı ve yerine koy. Sıra sıra bir fırın, bir ahır ya da bir saat kulesi gözünün önünde yükselir."),
             ("Kasabayı yeniden canlandır", "Büyükannen Rose sana yıkılıp gitmiş bir sahil kasabası bıraktı. Biten her bina sahibini eve getirir: Martha'nın fırınından tren istasyonuna kadar."),
             ("Tasarla ve süsle", "Mimar Masası'nda kendi evini, kafeni ya da dükkânını çiz, arsana kur; sonra bank, fener, çiçek tarhı, ağaç, kedi ve tavuk ekle.")]))
        body += steps("Why it stays calm" if en else "Neden sakin kalır", (
            ["Fully offline: play on a plane, on the train or anywhere without Wi-Fi.",
             "No timers, no energy bars, no lives: play five minutes or an hour, at your own pace.",
             "No ads, no subscription: the first two buildings are free, the rest of the town is one purchase.",
             "Your town lives in your own iCloud, so it follows you from iPhone to iPad.",
             "A color-blind mode prints a symbol on every brick color."] if en else
            ["Tamamen internetsiz: uçakta, trende ya da Wi-Fi olmayan her yerde oyna.",
             "Zamanlayıcı, enerji çubuğu ya da can yok: beş dakika ya da bir saat, kendi hızında oyna.",
             "Reklam ve abonelik yok: ilk iki bina ücretsiz, kasabanın geri kalanı tek bir satın alma.",
             "Kasaban kendi iCloud'unda durur; iPhone'dan iPad'e seninle gelir.",
             "Renk körü modu her tuğla rengine bir simge basar."]), ordered=False)
        body += paras(ESC("It suits all ages: there is no violence, no chat with strangers and nothing to buy by accident."
                          if en else "Her yaşa uygundur: şiddet yok, yabancılarla sohbet yok ve yanlışlıkla satın alınacak bir şey yok.")) + "\n"
        body += rel("cozy")
        write(path, page("brickhaven", lang, path, alts("cozy"), title, desc, body, [g["home"], (title, path)]))

        # Beginner's guide
        path, title, desc = g["tips"]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        tips = ([("Read the blueprint first", "Open the blueprint at the easel next to each building. It shows the finished building and how many bricks of each shape and color the next section needs."),
                 ("Pick shape and color together", "Two bricks can share a shape but not a color. If a brick doesn't match the plan, the game tells you before you lay it."),
                 ("Carry a full load", "Fill your arms before you walk to the wall. Every trip to the pile costs time; a full load saves many of them."),
                 ("Build section by section", "Each building is split into sections, like a wall or a roof. Finishing a section gives you skill points."),
                 ("Spend skill points on Strong Arms early", "Strong Arms lets you carry more bricks at once, up to twenty. It pays back on every single trip."),
                 ("Then get the Brick Magnet", "The magnet pulls matching bricks of the type you have selected straight to you. Searching the pile is the slowest part on a phone, and this skips it."),
                 ("Use the lift and jump for high rows", "Upper walls and roofs are reached with the lift; skills make it faster and let you jump higher."),
                 ("Make it yours", "Once the town is open, draw your own building at the Architect's Table and decorate the streets. There is no wrong answer.")] if en else
                [("Önce planı oku", "Her binanın yanındaki şövaledeki planı aç. Binanın bitmiş hâlini ve sıradaki bölüm için her şekil ve renkten kaç tuğla gerektiğini gösterir."),
                 ("Şekli ve rengi birlikte seç", "İki tuğlanın şekli aynı, rengi farklı olabilir. Tuğla plana uymuyorsa oyun koymadan önce söyler."),
                 ("Kucağını doldur", "Duvara yürümeden önce kucağını doldur. Yığına her gidiş zaman alır; dolu bir yük birçok gidişi kurtarır."),
                 ("Bölüm bölüm ilerle", "Her bina duvar, çatı gibi bölümlere ayrılır. Bir bölümü bitirmek yetenek puanı kazandırır."),
                 ("Puanları önce Güçlü Kollar'a ver", "Güçlü Kollar bir seferde daha çok, yirmiye kadar tuğla taşımanı sağlar. Her gidişte kendini geri öder."),
                 ("Sonra Tuğla Mıknatısı'nı al", "Mıknatıs seçtiğin türden eşleşen tuğlaları doğrudan sana çeker. Telefonda en yavaş iş yığında aramaktır; mıknatıs bunu atlar."),
                 ("Yüksek sıralar için asansör ve zıplama", "Üst duvarlara ve çatıya asansörle çıkılır; yetenekler asansörü hızlandırır ve daha yükseğe zıplatır."),
                 ("Kendine göre yap", "Kasaba açılınca Mimar Masası'nda kendi binanı çiz ve sokakları süsle. Yanlış cevap yok.")])
        for i, (h, p) in enumerate(tips):
            body += f"  <h2>{i + 1}. {ESC(h)}</h2>\n  <p>{ESC(p)}</p>\n"
            if i == 3:
                body += shot("firin", "The Bakery in Brickhaven" if en else "Brickhaven'da Fırın")
        body += paras(ESC("Stuck or found a bug? Write to hyapps@outlook.com; every message is read."
                          if en else "Takıldın ya da bir hata mı buldun? hyapps@outlook.com adresine yaz; her mesaj okunur.")) + "\n"
        body += rel("tips")
        write(path, page("brickhaven", lang, path, alts("tips"), title, desc, body, [g["home"], (title, path)]))


# ---------------------------------------------------------------- sitemap

STATIC = [("/", {"en": "/", "tr": "/tr/"}), ("/tr/", {"en": "/", "tr": "/tr/"}),
          ("/crownly/", {"en": "/crownly/", "tr": "/crownly/tr/"}), ("/crownly/tr/", {"en": "/crownly/", "tr": "/crownly/tr/"}),
          ("/crownly/privacy.html", {}),
          ("/quickwits/", {"en": "/quickwits/", "tr": "/quickwits/tr/"}), ("/quickwits/tr/", {"en": "/quickwits/", "tr": "/quickwits/tr/"}),
          ("/quickwits/privacy.html", {}),
          ("/brickhaven/", {"en": "/brickhaven/", "tr": "/brickhaven/tr/"}), ("/brickhaven/tr/", {"en": "/brickhaven/", "tr": "/brickhaven/tr/"}),
          ("/brickhaven/privacy.html", {}),
          ("/besmele/", {"tr": "/besmele/", "en": "/besmele/en/"}), ("/besmele/en/", {"tr": "/besmele/", "en": "/besmele/en/"}),
          ("/besmele/destek.html", {}), ("/besmele/en/destek.html", {}), ("/besmele/gizlilik.html", {}), ("/besmele/en/gizlilik.html", {})]


def build_sitemap():
    rows = []
    for path, alts in STATIC + PAGES:
        links = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{p}"/>' for l, p in alts.items())
        rows.append(f"  <url><loc>{SITE}{path}</loc>{links}</url>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n")
    print(f"sitemap: {len(rows)} urls")


build_esma()
build_besmele_guides()
build_crownly_guides()
build_quickwits_guides()
build_brickhaven_guides()
build_sitemap()
print(f"guide pages: {len(PAGES)}")

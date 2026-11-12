#!/usr/bin/env python3
"""Builds the SEO guide pages and the sitemap.

Usage: python3 -I tools/build_guides.py   (run from the site repo root)

- Besmele: Esmaül Hüsna hub + 99 name pages (TR /besmele/esma/, EN /besmele/en/names/) from the app's own data
  (Hikmet/Ortak/icerik.json, icerik_en.json), plus two how-to guides per language.
- Crownly: Queens rules, strategy and "LinkedIn Queens alternative" guides (EN + TR).
- Quick Wits: one-phone party games, a reaction time test (with a live test on the page) and group games for game night.
- Brickhaven: a cozy offline building game page and a beginner's guide.
- Glowfly: a relaxing idle merge game page and a beginner's guide (EN + TR).
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


def crownly_store():
    """Reads STORE from build_crownly.py: 1.2 has 6,500 levels in three games; 1.0.1 had 200 and no purchases."""
    with open(os.path.join(ROOT, "tools", "build_crownly.py")) as f:
        m = re.search(r"^STORE = (True|False)", f.read(), re.M)
    return m is None or m.group(1) == "True"


CROWNLY_STORE = crownly_store()
CROWNLY_LEVELS = {"en": "6,500" if CROWNLY_STORE else "200", "tr": "6.500" if CROWNLY_STORE else "200"}
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
                    cta_p={"en": f"Crownly: three daily logic puzzles, live duels, {CROWNLY_LEVELS['en']} levels and hints that explain the logic. Free on iPhone and iPad.",
                           "tr": f"Crownly: her gün üç mantık bulmacası, canlı düello, {CROWNLY_LEVELS['tr']} seviye ve mantığı anlatan ipuçları. iPhone ve iPad'de ücretsiz."}),
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
    "glowfly": dict(id="6830895618", css=["/glowfly/guide.css"], theme="#0b1023", icon="/glowfly/img/icon.png",
                    name={"en": "Glowfly", "tr": "Glowfly"}, home={"en": "/glowfly/", "tr": "/glowfly/tr/"},
                    og={"en": "/assets/og/glowfly-en.jpg", "tr": "/assets/og/glowfly-tr.jpg"},
                    cta_h={"en": "Light up the night, one firefly at a time", "tr": "Geceyi ateşböcekleriyle aydınlat"},
                    cta_p={"en": "Glowfly: a relaxing idle merge game for iPhone and iPad. 10 chapters, 1,000 nights, and it plays while you're away. Free to play.",
                           "tr": "Glowfly: iPhone ve iPad için rahatlatıcı bir idle birleştirme oyunu. 10 bölüm, 1.000 gece; sen yokken de oynar. Ücretsiz."}),
}


def is_live(app):
    """Reads LIVE from the app's landing-page builder, so the store button flips with one change there."""
    builder = os.path.join(ROOT, "tools", f"build_{app}.py")
    with open(builder) as f:
        m = re.search(r"^LIVE = (True|False)", f.read(), re.M)
    return m is None or m.group(1) == "True"


for _app in APPS:
    APPS[_app]["live"] = is_live(_app)


def glowfly_store():
    """Reads STORE from build_glowfly.py: 1.0 has no purchases or ads, so the guides leave Plus and ads out."""
    with open(os.path.join(ROOT, "tools", "build_glowfly.py")) as f:
        m = re.search(r"^STORE = (True|False)", f.read(), re.M)
    return m is None or m.group(1) == "True"


GLOWFLY_STORE = glowfly_store()

STORE_LABEL = {"en": "Download on the App Store", "tr": "App Store'dan indir"}
SOON_LABEL = {"en": "Coming soon to the App Store", "tr": "Yakında App Store'da"}
MADE = {"en": "Made with care by an independent developer.", "tr": "Bağımsız bir geliştirici tarafından yapıldı."}
PRIVACY = {"crownly": {"en": "/crownly/privacy.html", "tr": "/crownly/privacy.html#tr"},
           "besmele": {"en": "/besmele/en/gizlilik.html", "tr": "/besmele/gizlilik.html"},
           "quickwits": {"en": "/quickwits/privacy.html", "tr": "/quickwits/privacy.html#tr"},
           "brickhaven": {"en": "/brickhaven/privacy.html", "tr": "/brickhaven/privacy.html#tr"},
           "glowfly": {"en": "/glowfly/privacy.html", "tr": "/glowfly/privacy.html#tr"}}
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
           "author": {"@type": "Organization", "name": "HY Apps", "url": SITE + "/"},
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
             f"Love the LinkedIn Queens game? Crownly is a free iPhone app with a new Queens puzzle every day, {CROWNLY_LEVELS['en']} levels and hints that explain the logic."),
        board_label="A solved 5×5 Queens puzzle", related="More guides"),
    "tr": dict(
        home=("Crownly", "/crownly/tr/"),
        rules=("/crownly/tr/queens-nasil-oynanir/", "Queens Nasıl Oynanır? Queens Mantık Bulmacası Kuralları",
               "Queens bulmacasının (Star Battle olarak da bilinir) kuralları sade bir dille: her satıra, sütuna ve bölgeye bir taç; taçlar birbirine dokunmaz."),
        strategy=("/crownly/tr/queens-stratejileri/", "Queens Bulmacası Taktikleri: Her Tahtayı Çözen 6 Teknik",
                  "Her Queens bulmacasını tahmin etmeden çözen altı mantık tekniği: tacın etki alanından grup sıkışmasına."),
        alt=("/crownly/tr/linkedin-queens-alternatifi/", "LinkedIn Queens Alternatifi: iPhone'da Her Gün Queens Oyna",
             f"LinkedIn'deki Queens oyununu seviyor musun? Crownly her gün yeni bir Queens bulmacası, {CROWNLY_LEVELS['tr']} seviye ve mantığı anlatan ipuçları sunan ücretsiz bir iPhone uygulaması."),
        board_label="Çözülmüş 5×5 Queens bulmacası", related="Diğer rehberler"),
}


def build_crownly_guides():
    for lang in ("en", "tr"):
        g = CG[lang]
        other = CG["tr" if lang == "en" else "en"]
        alts = lambda key: {lang: g[key][0], ("tr" if lang == "en" else "en"): other[key][0]}
        rel = lambda skip: related(g["related"], [(CG_PLAY[lang][1].split(":")[0], CG_PLAY[lang][0])]
                                            + [(g[k][1].split(":")[0], g[k][0]) for k in ("rules", "strategy", "alt") if k != skip]
                                            + [(CG_LIKE[lang][1].split(":")[0], CG_LIKE[lang][0])])
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
                          "row, column or region it is about and explains the step."
                          if en else
                          "Crownly'nin ipuçları tam olarak bu teknikleri kullanır: takıldığında ipucu tekniğin adını söyler, ilgili satırı, sütunu "
                          "ya da bölgeyi vurgular ve adımı açıklar.")) + "\n"
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
             f"{CROWNLY_LEVELS['en']} levels from Easy to Expert in three games, with up to three stars each.",
             "Hints that explain the next logical step instead of revealing the answer.",
             "Two more daily puzzles, Route and Mosaic, plus Double Crowns and live duels with friends.",
             "Streaks, streak freezes, Game Center leaderboards and widgets.",
             "Color-blind mode, dark mode, no ads, works offline."] if en else
            ["Herkese aynı anda gelen yeni bir günlük bulmaca ve 10×10 Günlük Zor.",
             f"Üç oyunda Kolaydan Uzmana {CROWNLY_LEVELS['tr']} seviye, her birinde üç yıldıza kadar.",
             "Cevabı vermek yerine sıradaki mantıklı adımı anlatan ipuçları.",
             "İki günlük bulmaca daha (Rota ve Mozaik), Çift Taç ve arkadaşlarınla canlı düello.",
             "Seri, seri dondurma, Game Center sıralamaları ve widget'lar.",
             "Renk körü modu, koyu tema, reklamsız, internetsiz oynanır."])) + "</ul>\n"
        body += paras(ESC("Crownly is an independent app and is not affiliated with or endorsed by LinkedIn. Queens and Star Battle are names of a puzzle type."
                          if en else "Crownly bağımsız bir uygulamadır; LinkedIn ile bir bağlantısı yoktur ve LinkedIn tarafından desteklenmez. "
                          "Queens ve Star Battle bir bulmaca türünün adlarıdır.")).replace("<p>", '<p class="note">') + "\n"
        body += rel("alt")
        write(path, page("crownly", lang, path, alts("alt"), title, desc, body, [g["home"], (title, path)]))


# ---------------------------------------------------------------- Crownly: playable web daily

CG_PLAY = {
    "en": ("/crownly/daily-queens-puzzle/", "Daily Queens Puzzle: Play Today's Crownly Puzzle Online",
           "Play today's Queens logic puzzle free in your browser: one crown in every row, column and region, and crowns never touch. "
           "A new board every day at 07:00 UTC, the same one as in the Crownly app."),
    "tr": ("/crownly/tr/gunluk-queens-bulmacasi/", "Günlük Queens Bulmacası: Bugünün Crownly Bulmacasını Online Çöz",
           "Bugünün Queens mantık bulmacasını tarayıcında ücretsiz çöz: her satıra, sütuna ve bölgeye bir taç, taçlar birbirine dokunmaz. "
           "Her gün 07:00 UTC'de yeni tahta; Crownly uygulamasındakiyle aynı bulmaca."),
}
PLAY_TEXT = {
    "en": dict(crown="crown", dot="dot", empty="empty", cell="Row {r}, column {c}", left="Crowns left: {n}",
               next="Next puzzle in {t}", ready="A new puzzle is ready. Reload the page.", solved="Solved in {t}!",
               share="Share result", copied="Copied", error="Today's puzzle could not be loaded. Check your connection and reload."),
    "tr": dict(crown="taç", dot="nokta", empty="boş", cell="{r}. satır, {c}. sütun", left="Kalan taç: {n}",
               next="Yeni bulmacaya {t}", ready="Yeni bulmaca hazır. Sayfayı yenile.", solved="{t} sürede çözdün!",
               share="Sonucu paylaş", copied="Kopyalandı", error="Bugünün bulmacası yüklenemedi. Bağlantını kontrol edip sayfayı yenile."),
}


def asset_version(rel):
    """Short content hash for cache busting (?v=…), so browsers fetch play.js/play.css again after a change."""
    import hashlib
    with open(os.path.join(ROOT, rel.lstrip("/")), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def build_crownly_play():
    js_v, css_v = asset_version("/crownly/play.js"), asset_version("/crownly/play.css")
    for lang in ("en", "tr"):
        en = lang == "en"
        path, title, desc = CG_PLAY[lang]
        other = CG_PLAY["tr" if en else "en"][0]
        g = CG[lang]
        t = dict(PLAY_TEXT[lang], **{})
        cfg = json.dumps({"lang": lang, "url": SITE + path, "t": t}, ensure_ascii=False)
        store = f"https://apps.apple.com/{'tr/' if lang == 'tr' else ''}app/apple-store/id6822852151?pt=129592179&ct=webdaily&mt=8"
        h1 = "Today's Queens Puzzle" if en else "Bugünün Queens Bulmacası"
        intro = ("Place one crown in every row, column and colored region. Crowns never touch, not even diagonally. "
                 "Tap a cell once for a dot, twice for a crown, or drag to dot many cells." if en else
                 "Her satıra, sütuna ve renkli bölgeye bir taç koy. Taçlar birbirine dokunmaz, çapraz da. "
                 "Hücreye bir kez dokun nokta, iki kez taç; sürükleyerek çok hücreye nokta koy.")
        body = f'  <h1>{ESC(h1)}</h1>\n  <p class="intro">{ESC(intro)}</p>\n'
        body += f"""  <section class="cq loading" id="cq" aria-label="{ESC(h1)}">
    <div class="cq-head"><span class="cq-date" id="cq-date"></span><span class="cq-time" id="cq-time" aria-label="{'Time' if en else 'Süre'}">0:00</span></div>
    <div class="cq-board" id="cq-board" role="grid" aria-label="{'Puzzle board' if en else 'Bulmaca tahtası'}"></div>
    <div class="cq-tools"><span class="cq-count" id="cq-count"></span>
      <button type="button" id="cq-undo" disabled>{'Undo' if en else 'Geri al'}</button>
      <button type="button" id="cq-clear" disabled>{'Clear' if en else 'Temizle'}</button></div>
    <p class="cq-status" id="cq-status" aria-live="polite"></p>
    <div class="cq-result" id="cq-result" hidden>
      <p>{'Solved!' if en else 'Çözdün!'}</p>
      <p class="big" id="cq-result-time">0:00</p>
      <button type="button" class="cq-share" id="cq-share">{ESC(t['share'])}</button>
      <p class="next" id="cq-next"></p>
      <p class="more">{ESC('Want more? Crownly has two more daily puzzles (Route and Mosaic), a 10×10 Hard Daily, streaks and live duels.' if en else 'Daha fazlası mı? Crownly’de iki günlük bulmaca daha (Rota ve Mozaik), 10×10 Günlük Zor, seri ve canlı düello var.')}</p>
      <a class="store" href="{ESC(store)}">{ESC(STORE_LABEL[lang])}</a>
    </div>
  </section>
  <script>window.CROWNLY_PLAY = {cfg};</script>
  <script src="/crownly/play.js?v={js_v}" defer></script>
"""
        body += f'  <h2>{"How to play Queens" if en else "Queens nasıl oynanır"}</h2>\n  <ol>' + "".join(f"<li>{ESC(x)}</li>" for x in (
            ["Place exactly one crown in every row and every column.", "Place exactly one crown in every colored region.",
             "Crowns may not touch each other, not even diagonally.",
             "Use dots to mark cells that can't hold a crown. Every puzzle has exactly one solution, so you never have to guess."] if en else
            ["Her satıra ve her sütuna tam bir taç koy.", "Her renkli bölgeye tam bir taç koy.", "Taçlar birbirine dokunamaz, çapraz da.",
             "Taç gelemeyecek hücreleri noktayla işaretle. Her bulmacanın tek çözümü var; tahmin etmen gerekmez."])) + "</ol>\n"
        faq = ([("When does a new puzzle come out?", "Every day at 07:00 UTC, at the same moment for everyone in the world."),
                ("Is it the same puzzle as in the app?", "Yes. The web puzzle is Crownly's normal daily Crowns puzzle (7×7). In the app you also get the 10×10 Hard Daily, Route and Mosaic dailies, a streak and Game Center leaderboards."),
                ("Is it free?", "Yes, today's puzzle is free here and in the app. Your progress is saved in this browser until the next puzzle."),
                ("Can I play older puzzles?", "Past daily puzzles are in the Crownly app's archive (Crownly Pro).")] if en else
               [("Yeni bulmaca ne zaman çıkıyor?", "Her gün 07:00 UTC'de (Türkiye saatiyle 10:00), dünyadaki herkes için aynı anda."),
                ("Uygulamadakiyle aynı bulmaca mı?", "Evet. Web bulmacası Crownly'nin normal günlük Taçlar bulmacasıdır (7×7). Uygulamada ayrıca 10×10 Günlük Zor, Rota ve Mozaik günlükleri, seri ve Game Center sıralamaları var."),
                ("Ücretsiz mi?", "Evet, bugünün bulmacası burada da uygulamada da ücretsiz. İlerlemen yeni bulmacaya kadar bu tarayıcıda saklanır."),
                ("Eski bulmacaları çözebilir miyim?", "Geçmiş günlük bulmacalar Crownly uygulamasının arşivinde (Crownly Pro).")])
        body += f'  <h2>{"Questions" if en else "Sorular"}</h2>\n' + "".join(f"  <h3>{ESC(q)}</h3>\n  <p>{ESC(a)}</p>\n" for q, a in faq)
        body += related(g["related"], [(g[k][1].split(":")[0], g[k][0]) for k in ("rules", "strategy", "alt")]) + "\n"
        schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
        write(path, page("crownly", lang, path, {lang: path, ("tr" if en else "en"): other}, title, desc, body,
                         [g["home"], (title, path)], schema=schema, head=f'\n  <link rel="stylesheet" href="/crownly/play.css?v={css_v}">'))


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
                      ["Write everyone's name once, up to 8 players.",
                       "Pick a few games and how many rounds each.",
                       "The first player plays a short round, a few seconds long, then hands the phone on.",
                       "Each player gets exactly the same round, so nobody gets an easier question.",
                       "When everyone has played, the results of the round are revealed together."] if en else
                      ["Herkesin adını bir kez yaz, 8 kişiye kadar.",
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
        buildings=("/brickhaven/buildings/", "All 9 Buildings in Brickhaven: Owners, Order and What Makes Each One Special",
                   "The nine story buildings of Brickhaven in order, from Martha's Bakery to the Train Station: who lives there, what is new in each and which ones are free."),
        skills=("/brickhaven/skill-tree/", "Brickhaven Skill Tree: Which Skills to Unlock First",
                "Every skill in Brickhaven explained: Strong Arms, Skilled Hands, the Brick Magnet, the lift and the rest, with a sensible order to spend your points."),
        design=("/brickhaven/design-your-own-house/", "Design Your Own House: The Architect's Table in Brickhaven",
                "Draw your own house, shop, café or farm on iPhone and iPad, pick the colors and windows, then build it by hand on your own lot."),
    ),
    "tr": dict(
        home=("Brickhaven", "/brickhaven/tr/"), related="Diğer rehberler",
        cozy=("/brickhaven/tr/internetsiz-rahatlatici-insa-oyunu/", "İnternetsiz, Rahatlatıcı Bir İnşa Oyunu: iPhone ve iPad",
              "Zamanlayıcısız, reklamsız, internet gerektirmeyen sakin bir oyun mu arıyorsun? Brickhaven'da bir sahil kasabasını tuğla tuğla yeniden kurarsın."),
        tips=("/brickhaven/tr/baslangic-rehberi/", "Brickhaven Başlangıç Rehberi: Daha Hızlı İnşa İçin 8 İpucu",
              "Yeni ustalar için sekiz ipucu: planı okumak, daha çok tuğla taşımak, önce hangi yetenekleri almak ve kendi evini tasarlamak."),
        buildings=("/brickhaven/tr/binalar/", "Brickhaven'daki 9 Bina: Sahipleri, Sırası ve Özellikleri",
                   "Brickhaven'ın dokuz hikâye binası sırasıyla, Martha'nın Fırını'ndan Tren İstasyonu'na: kim yaşıyor, her binada ne yeni ve hangileri ücretsiz."),
        skills=("/brickhaven/tr/ustalik-agaci/", "Brickhaven Ustalık Ağacı: Önce Hangi Beceriler Alınmalı?",
                "Brickhaven'daki bütün beceriler: Güçlü Kollar, Usta Eller, Tuğla Mıknatısı, asansör ve diğerleri; puanları harcamak için mantıklı bir sıra."),
        design=("/brickhaven/tr/ev-tasarlama-oyunu/", "Ev Tasarlama Oyunu: Kendi Evini Çiz, Tuğla Tuğla Kur",
                "iPhone ve iPad'de kendi evini, dükkânını, kafeni ya da çiftliğini çiz; renkleri ve pencereleri seç, sonra kendi arsana tuğla tuğla kur."),
    ),
}


def brickhaven_more(lang, g, alts, rel, shot):
    """Buildings list, skill tree and Architect's Table guides."""
    en = lang == "en"
    crumbs = lambda title, path: [g["home"], (title, path)]

    # All nine buildings
    path, title, desc = g["buildings"]
    body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
    body += paras(ESC("Brickhaven's story has nine buildings. You build them in order, every brick by hand, and each one is bigger "
                      "or taller than the last: the Bakery takes about 500 bricks, the Fire Station about 1,400. The first two are "
                      "free; the Whole Town, a one-time purchase, opens the other seven."
                      if en else
                      "Brickhaven'ın hikâyesinde dokuz bina var. Sırayla, her tuğlayı kendi elinle koyarak kurarsın; her biri bir "
                      "öncekinden daha büyük ya da daha yüksektir: Fırın yaklaşık 500, İtfaiye yaklaşık 1.400 tuğla tutar. İlk ikisi "
                      "ücretsiz; tek seferlik satın alma olan Tüm Kasaba diğer yedisini açar.")) + "\n"
    rows = ([("firin", "Bakery", "Martha the baker", "The first building and the tutorial: pink walls, a tiled roof and a chimney. You learn to read the blueprint, carry bricks and ride the lift. Free."),
             ("ahir", "Red Barn", "Farmer Joe", "Almost twice the bricks, with double doors and barn windows. When it is done the cows, chickens and hay bales come back. Free."),
             ("ev", "Flower Shop", "Daisy", "A two-tone shop with a fenced front garden, where Grandma Rose's roses used to come from."),
             ("kafe", "Seaside Café", "Lucy", "A mint-green shop floor, a glass conservatory and a terrace you pave yourself, stone by stone."),
             ("dondurmaci", "Ice Cream Parlor", "Mia", "A flat-roofed parlor in pink and mint with a giant cone on the roof and tables outside."),
             ("kitapci", "Bookshop", "Mr. Oliver", "Three floors, a corner tower and a covered porch. The first building where the lift really matters."),
             ("saat", "Clock Tower", "Arthur the clockmaker", "An eleven-meter tower on the town square with a clock face on all four sides and a pointed spire. When it is finished the clock shows the real time and the bell rings."),
             ("itfaiye", "Fire Station", "Sam and his crew", "The biggest build: two garage doors, a flat roof and a tall lookout tower, with the red truck waiting outside."),
             ("istasyon", "Train Station", "Henry the station master", "A long hall with a clock tower and a platform canopy. Finish it and the train calls at Brickhaven again.")] if en else
            [("firin", "Fırın", "Fırıncı Martha", "İlk bina ve öğretici: pembe duvarlar, kiremit çatı ve baca. Planı okumayı, tuğla taşımayı ve asansöre binmeyi burada öğrenirsin. Ücretsiz."),
             ("ahir", "Kırmızı Ahır", "Çiftçi Joe", "Neredeyse iki katı tuğla, çift kanatlı kapı ve ahır pencereleri. Bitince inekler, tavuklar ve saman balyaları geri gelir. Ücretsiz."),
             ("ev", "Çiçekçi", "Daisy", "Çitli ön bahçesi olan iki renkli bir dükkân; Büyükanne Rose'un gülleri hep buradan gelirdi."),
             ("kafe", "Sahil Kafesi", "Lucy", "Nane yeşili dükkân katı, cam kış bahçesi ve taş taş kendin döşediğin bir teras."),
             ("dondurmaci", "Dondurmacı", "Mia", "Pembe ve nane renkli, düz çatılı bir dükkân; çatıda dev bir külah, önünde masalar."),
             ("kitapci", "Kitapçı", "Bay Oliver", "Üç kat, köşe kulesi ve kapalı veranda. Asansörün gerçekten işe yaradığı ilk bina."),
             ("saat", "Saat Kulesi", "Saatçi Arthur", "Kasaba meydanında on bir metrelik bir kule: dört yüzünde saat kadranı, tepesinde sivri külah. Bitince saat gerçek zamanı gösterir, çan çalar."),
             ("itfaiye", "İtfaiye", "Sam ve ekibi", "En büyük yapı: iki garaj kapısı, düz çatı ve yüksek bir gözetleme kulesi; kırmızı araç kapıda bekler."),
             ("istasyon", "Tren İstasyonu", "İstasyon şefi Henry", "Saat kuleli, peron saçaklı uzun bir salon. Bitirince tren yeniden Brickhaven'a uğrar.")])
    for i, (b, name, owner, text) in enumerate(rows):
        body += f"  <h2>{i + 1}. {ESC(name)}</h2>\n"
        body += shot(b, f"{name} in Brickhaven" if en else f"Brickhaven'da {name}")
        body += f"  <p><strong>{ESC(owner)}.</strong> {ESC(text)}</p>\n"
    body += f"  <h2>{ESC('After the ninth building' if en else 'Dokuzuncu binadan sonra')}</h2>\n"
    body += paras(ESC("When the station is finished the whole town gathers on the square to celebrate. After that Brickhaven is yours "
                      "to walk around, decorate, and add to with buildings you design yourself at the Architect's Table."
                      if en else
                      "İstasyon bitince bütün kasaba kutlama için meydanda toplanır. Sonrasında Brickhaven senindir: gezersin, "
                      "süslersin ve Mimar Masası'nda kendi tasarladığın binaları eklersin.")) + "\n"
    body += rel("buildings")
    write(path, page("brickhaven", lang, path, alts("buildings"), title, desc, body, crumbs(title, path)))

    # Skill tree
    path, title, desc = g["skills"]
    body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
    body += paras(ESC("You earn skill points by laying bricks correctly and by finishing sections and buildings. Open Skills from "
                      "the top of the screen to spend them. The board has three columns, and you can reset it and spend the points again."
                      if en else
                      "Yetenek puanını tuğlaları doğru koyarak, bölümleri ve binaları bitirerek kazanırsın. Harcamak için ekranın "
                      "üstündeki Ustalık'ı aç. Panoda üç sütun var; istersen sıfırlayıp puanları yeniden dağıtabilirsin.")) + "\n"
    cols = ([("Carrying", [("Strong Arms", "Carry more bricks per trip: from 6 at the start up to 20 at the last level."),
                           ("Brick Magnet", "A button that pulls bricks of the kind you are looking at straight into your arms: 1 brick at first, 10 at the last level, with a shorter wait each level."),
                           ("Drop All", "Hold Drop to put your whole load down at once.")]),
             ("Laying", [("Skilled Hands", "Each brick goes into the wall faster."),
                         ("Nonstop Laying", "Hold the button and keep laying brick after brick."),
                         ("Long Arms", "Reach farther: place bricks up to 3 meters away instead of 2.1.")]),
             ("Moving", [("Sprint", "Walk faster between the pile and the wall."),
                         ("Lift", "The lift is free and always reaches the roof; this skill makes it rise and travel faster."),
                         ("High Jump", "Jump higher, up to almost a meter.")])] if en else
            [("Taşıma", [("Güçlü Kollar", "Bir seferde daha çok tuğla taşırsın: başta 6, son kademede 20."),
                         ("Tuğla Mıknatısı", "Baktığın türden tuğlaları doğrudan eline çeken bir düğme: başta 1, son kademede 10 tuğla; bekleme süresi her kademede kısalır."),
                         ("Toplu Bırak", "Bırak'ı basılı tutunca elindekilerin hepsini birden yere koyarsın.")]),
             ("Örme", [("Usta Eller", "Her tuğla duvara daha çabuk yerleşir."),
                       ("Kesintisiz Örme", "Düğmeyi basılı tut, tuğlaları art arda koy."),
                       ("Uzun Kollar", "Daha uzağa uzanırsın: tuğlayı 2,1 yerine 3 metreye kadar koyabilirsin.")]),
             ("Hareket", [("Koşma", "Yığınla duvar arasında daha hızlı yürürsün."),
                          ("Asansör", "Asansör ücretsizdir ve her zaman çatıya yetişir; bu beceri onu daha hızlı çıkarır ve yürütür."),
                          ("Yüksek Zıplama", "Daha yükseğe, neredeyse bir metreye kadar zıplarsın.")])])
    for h, items in cols:
        body += defs(h, items)
    body += steps("A good order" if en else "İyi bir sıra", (
        ["Strong Arms first. Every trip to the pile carries more, on every building.",
         "A few levels of Skilled Hands, so a full load goes into the wall quickly.",
         "The Brick Magnet as soon as it opens. Searching the pile is the slowest part on a phone.",
         "Sprint and Lift once the buildings get tall, from the Bookshop on.",
         "Nonstop Laying, Long Arms, Drop All and High Jump are comforts: take them when points are left over."] if en else
        ["Önce Güçlü Kollar. Yığına her gidişte daha çok taşırsın, her binada işe yarar.",
         "Birkaç kademe Usta Eller; dolu bir yük duvara çabucak girer.",
         "Açılır açılmaz Tuğla Mıknatısı. Telefonda en yavaş iş yığında tuğla aramaktır.",
         "Binalar yükselince, Kitapçı'dan itibaren, Koşma ve Asansör.",
         "Kesintisiz Örme, Uzun Kollar, Toplu Bırak ve Yüksek Zıplama rahatlıktır: puan artınca al."]))
    body += paras(ESC("The story gives enough points for the whole board, so no choice is final." if en else
                      "Hikâye bütün panoya yetecek kadar puan verir; hiçbir seçim kalıcı değildir.")) + "\n"
    body += rel("skills")
    write(path, page("brickhaven", lang, path, alts("skills"), title, desc, body, crumbs(title, path)))

    # Architect's Table
    path, title, desc = g["design"]
    body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
    body += paras(ESC("Most house design games stop at the drawing. In Brickhaven the drawing is only the plan: once it is ready, the "
                      "bricks are delivered to your lot and you build the house yourself, row by row, like every other building in town."
                      if en else
                      "Ev tasarlama oyunlarının çoğu çizimde biter. Brickhaven'da çizim yalnızca plandır: hazır olunca tuğlalar arsana "
                      "gelir ve evi, kasabadaki diğer binalar gibi sıra sıra kendin kurarsın.")) + "\n"
    body += shot("kitapci", "The Bookshop, one of the story buildings in Brickhaven" if en else "Brickhaven'ın hikâye binalarından Kitapçı")
    body += steps("How to design a building" if en else "Bir bina nasıl tasarlanır", (
        ["Open the Architect's Table from the menu and start a new design, or pick one of the ready-made sketches.",
         "Body: choose the width and depth, one to three floors, and a pitched or a flat roof.",
         "Colors: walls, upper floor, corner stones, trim, roof, door and windows each get their own color.",
         "Facade: tap any spot on a wall to switch it between wall, window, wide window and door.",
         "Extras: add a side wing or a corner tower.",
         "Identity: make it a home, a shop, a café or a farm and write the name on its sign.",
         "Tap Build and choose one of your four lots."] if en else
        ["Menüden Mimar Masası'nı aç ve yeni bir tasarıma başla ya da hazır taslaklardan birini seç.",
         "Gövde: genişliği ve derinliği, bir ile üç arasında kat sayısını, beşik ya da düz çatıyı seç.",
         "Renkler: duvar, üst kat, köşe taşları, silme, çatı, kapı ve pencerelerin her birine ayrı renk ver.",
         "Cephe: duvarda bir yere dokunarak duvar, pencere, geniş pencere ve kapı arasında değiştir.",
         "Ekler: yan kanat ya da köşe kulesi ekle.",
         "Kimlik: ev, dükkân, kafe ya da çiftlik yap; tabelasına adını yaz.",
         "İnşa et'e dokun ve dört arsandan birini seç."]))
    body += defs("Good to know" if en else "Bilmekte fayda var", (
        [("You see it before you build it", "A 3D preview turns next to the controls and shows the brick count, so you know how long the build will take."),
         ("The theme decides who moves in", "A finished café gets tables and a barista, a farm gets hay, a cow and chickens, a home gets a bench and flowers."),
         ("Designing is free", "Anyone can draw and save designs. Building them on a lot is part of the Whole Town purchase."),
         ("Then decorate", "After a building is finished you can place benches, lamps, trees, flower beds and animals around it.")] if en else
        [("Kurmadan önce görürsün", "Ayarların yanında dönen 3B önizleme tuğla sayısını da gösterir; inşaatın ne kadar süreceğini bilirsin."),
         ("Tema, kimin taşınacağını belirler", "Biten kafeye masalar ve barista, çiftliğe saman, inek ve tavuklar, eve bank ve çiçekler gelir."),
         ("Tasarlamak ücretsiz", "Herkes tasarım çizip kaydedebilir. Arsaya kurmak Tüm Kasaba satın almasına dahildir."),
         ("Sonra süsle", "Bina bitince çevresine bank, fener, ağaç, çiçek tarhı ve hayvanlar koyabilirsin.")]))
    body += rel("design")
    write(path, page("brickhaven", lang, path, alts("design"), title, desc, body, crumbs(title, path)))


def build_brickhaven_guides():
    for lang in ("en", "tr"):
        g = BG[lang]
        other = BG["tr" if lang == "en" else "en"]
        alts = lambda key: {lang: g[key][0], ("tr" if lang == "en" else "en"): other[key][0]}
        rel = lambda skip: related(g["related"], [(g[k][1].split(":")[0], g[k][0]) for k in ("cozy", "tips", "buildings", "skills", "design") if k != skip])
        en = lang == "en"
        shot = lambda b, alt: f'  <img class="shot" src="/brickhaven/img/{lang}-{b}.jpg" alt="{ESC(alt)}" width="720" height="480" loading="lazy">\n'
        brickhaven_more(lang, g, alts, rel, shot)

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


# ---------------------------------------------------------------- Glowfly: idle merge guides

GG = {
    "en": dict(
        home=("Glowfly", "/glowfly/"), related="More guides",
        idle=("/glowfly/relaxing-idle-merge-game/", "A Relaxing Idle Merge Game for iPhone That Plays While You're Away",
              "Looking for a calm idle game with no forced ads? In Glowfly, lights bounce through the dark, merge into brighter "
              "ones and reveal a hand-drawn night sky, even while the game is closed."),
        offline=("/glowfly/idle-games-offline-progress/", "How Offline Progress Works in Idle Games (and How to Get the Most From It)",
                 "Idle games keep earning while they're closed. Here is how offline progress is usually calculated, why it has a "
                 "time limit, and simple habits that make every return worth it, with Glowfly as the example."),
        tips=("/glowfly/beginners-guide/", "Glowfly Beginner's Guide: 10 Tips to Light Up More Nights",
              "Ten tips for new players: when to add lights and when to level them, how merging works, which boosts to use "
              "before bed and how to break the big rocks faster."),
    ),
    "tr": dict(
        home=("Glowfly", "/glowfly/tr/"), related="Diğer rehberler",
        idle=("/glowfly/tr/rahatlatici-idle-birlestirme-oyunu/", "Sen Yokken de Oynayan Rahatlatıcı Bir Idle Birleştirme Oyunu: iPhone",
              "Zorla reklam izletmeyen sakin bir idle oyun mu arıyorsun? Glowfly'da ışıklar karanlıkta seker, birleşip daha "
              "parlak olur ve oyun kapalıyken bile elle çizilmiş bir gece gökyüzünü ortaya çıkarır."),
        offline=("/glowfly/tr/idle-oyunlarda-kapaliyken-ilerleme/", "Idle Oyunlarda Kapalıyken İlerleme Nasıl Çalışır (ve En İyi Nasıl Kullanılır)",
                 "Idle oyunlar kapalıyken de kazanmaya devam eder. Kapalıyken ilerlemenin genelde nasıl hesaplandığını, neden bir "
                 "süre sınırı olduğunu ve her dönüşü değerli kılan basit alışkanlıkları Glowfly örneğiyle anlatıyoruz."),
        tips=("/glowfly/tr/baslangic-rehberi/", "Glowfly Başlangıç Rehberi: Daha Çok Gece Aydınlatmak İçin 10 İpucu",
              "Yeni oyuncular için on ipucu: ne zaman ışık ekleyip ne zaman seviye yükseltmeli, birleştirme nasıl işler, "
              "yatmadan önce hangi takviyeler kullanılır ve büyük kayalar nasıl daha hızlı kırılır."),
    ),
}


def build_glowfly_guides():
    for lang in ("en", "tr"):
        g = GG[lang]
        other = GG["tr" if lang == "en" else "en"]
        alts = lambda key: {lang: g[key][0], ("tr" if lang == "en" else "en"): other[key][0]}
        rel = lambda skip: related(g["related"], [(g[k][1].split(":")[0], g[k][0]) for k in ("idle", "tips", "offline") if k != skip])
        en = lang == "en"
        shot = lambda n, alt: f'  <img class="shot" src="/glowfly/img/ch{n}.jpg" alt="{ESC(alt)}" width="600" height="900" loading="lazy">\n'

        # Relaxing idle merge game
        path, title, desc = g["idle"]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        body += paras(ESC("An idle game is one that keeps making progress on its own: you make a few good choices, and the game does the "
                          "rest, even while your phone is in your pocket. A merge game adds one simple rule: combine identical things "
                          "into one better thing. Glowfly puts both ideas under a quiet night sky."
                          if en else
                          "Idle oyun, kendi kendine ilerlemeye devam eden oyundur: birkaç iyi seçim yaparsın, gerisini oyun yapar; telefon "
                          "cebindeyken bile. Birleştirme oyunu buna basit bir kural ekler: aynı şeyleri birleştirip daha iyi tek bir şey "
                          "yap. Glowfly bu iki fikri sakin bir gece gökyüzünün altında buluşturur.")) + "\n"
        body += shot(1, "Forest Night, the first chapter of Glowfly" if en else "Glowfly'ın ilk bölümü Orman Gecesi")
        body += defs("How Glowfly plays" if en else "Glowfly nasıl oynanır", (
            [("Lights that bounce", "Each light flies in a straight line, bounces off the walls and breaks the glass and rock it hits. Every broken piece reveals a little more of the night landscape underneath."),
             ("Ten become one", "Collect ten lights of the same kind and merge them into one brighter, stronger light. There are twelve kinds of light, from a soft spark to the brightest star."),
             ("A night at a time", "When every wall is broken, the whole landscape lights up and the next night begins. Every ten nights a fallen star is found and a postcard joins your story."),
             ("A story to the end", "Ten chapters, from a forest cabin to a lighthouse, a desert, a sleeping town, the deep sea, the planets and the Milky Way. Night 1,000 completes the sky.")] if en else
            [("Seken ışıklar", "Her ışık düz bir çizgide uçar, duvarlardan seker ve çarptığı camı ve kayayı kırar. Kırılan her parça alttaki gece manzarasından biraz daha gösterir."),
             ("On ışık, bir ışık", "Aynı türden on ışık topla ve onları daha parlak, daha güçlü tek bir ışıkta birleştir. Yumuşak bir kıvılcımdan en parlak yıldıza kadar on iki ayrı ışık var."),
             ("Gece gece", "Bütün duvarlar kırılınca manzaranın tamamı aydınlanır ve sıradaki gece başlar. Her on gecede düşmüş bir yıldız bulunur ve hikâyene bir kartpostal eklenir."),
             ("Sonuna kadar bir hikâye", "Ormandaki bir kulübeden deniz fenerine, çöle, uyuyan bir kasabaya, derin denize, gezegenlere ve Samanyolu'na on bölüm. 1.000. gece gökyüzünü tamamlar.")]))
        body += steps("Why it stays relaxing" if en else "Neden rahatlatıcı kalır", (
            ["It plays while you're away: your lights keep working for hours after you close the game, and you come back to nights already cleared.",
             "No ad ever plays on its own. Some rewards can be earned by choosing to watch a short video, and that's all.",
             "No timers chasing you, no energy bars and no lives. Open it for a minute or an hour.",
             "Soft lo-fi music and gentle glass sounds, with options for fewer effects and no flashing.",
             "Your progress is backed up in your own iCloud and follows you to a new iPhone or iPad."] if en else
            ["Sen yokken de oynar: oyunu kapattıktan sonra ışıkların saatlerce çalışır, döndüğünde geceler çoktan aydınlanmış olur.",
             "Hiçbir reklam kendiliğinden oynamaz. Bazı ödüller kısa bir video izlemeyi seçerek kazanılır, o kadar.",
             "Seni kovalayan zamanlayıcı, enerji çubuğu ya da can yok. Bir dakika ya da bir saat aç.",
             "Yumuşak lo-fi müzik ve hafif cam sesleri; daha az efekt ve yanıp sönmesiz arayüz seçenekleri.",
             "İlerlemen kendi iCloud'unda yedeklenir, yeni iPhone ya da iPad'ine seninle gelir."]), ordered=False)
        body += shot(5, "The Lighthouse chapter in Glowfly" if en else "Glowfly'da Deniz Feneri bölümü")
        body += defs("Who it is for" if en else "Kimler için", (
            [("Players who like to check in", "If you enjoy opening a game for a few minutes, collecting what built up and making one or two choices, Glowfly is made for that rhythm."),
             ("Players who like to watch", "Hold the speed button and watch a wall of glass shatter under dozens of lights, or tap the rocks yourself. It is satisfying without asking for skill."),
             ("Anyone who wants a calm screen", "Dark, quiet colors, a slow story and no pressure: it is a pleasant thing to leave running.")] if en else
            [("Arada bir uğramayı sevenler", "Bir oyunu birkaç dakikalığına açıp biriken kazancı toplamayı ve bir iki seçim yapmayı seviyorsan Glowfly tam bu ritim için yapıldı."),
             ("İzlemeyi sevenler", "Hızlandır düğmesine basılı tut ve onlarca ışığın altında bir cam duvarın parçalanışını izle ya da kayalara kendin dokun. Beceri istemeden tatmin edici."),
             ("Sakin bir ekran isteyen herkes", "Koyu, sessiz renkler, yavaş akan bir hikâye ve baskı yok: açık bırakmak bile hoş.")]))
        if GLOWFLY_STORE:
            free = ("Glowfly is free to play from the first night to the last. Glowfly Plus, an optional subscription, makes the "
                    "lights work longer while you're away and gives ad-free rewards; there is also a one-time ad-free option."
                    if en else
                    "Glowfly ilk geceden son geceye kadar ücretsiz oynanır. İsteğe bağlı abonelik Glowfly Plus, sen yokken "
                    "ışıkların daha uzun çalışmasını ve ödülleri reklamsız almanı sağlar; tek seferlik bir reklamsız seçenek de var.")
        else:
            free = ("Glowfly is free to play from the first night to the last, with no ads and no in-app purchases." if en else
                    "Glowfly ilk geceden son geceye kadar ücretsiz oynanır; reklam ve uygulama içi satın alma yoktur.")
        body += paras(ESC(free)) + "\n"
        body += rel("idle")
        faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in (
                [("Is Glowfly an idle game?", "Yes. Glowfly is an idle merge game: your lights keep breaking walls and earning light for hours after you close it."),
                 ("Does Glowfly force you to watch ads?", "No. Ads only play when you choose to watch one for a reward, and Glowfly Plus or the ad-free option gives those rewards without ads." if GLOWFLY_STORE else "No. Glowfly has no ads."),
                 ("Is Glowfly free?", "Yes, it is free to play. Glowfly Plus, an ad-free option and gem packs are optional in-app purchases." if GLOWFLY_STORE else "Yes, it is free to play, with no in-app purchases.")] if en else
                [("Glowfly bir idle oyun mu?", "Evet. Glowfly bir idle birleştirme oyunudur: oyunu kapattıktan sonra ışıkların saatlerce duvar kırmaya ve ışıltı kazanmaya devam eder."),
                 ("Glowfly zorla reklam izletiyor mu?", "Hayır. Reklam yalnız bir ödül için izlemeyi seçtiğinde oynar; Glowfly Plus ya da reklamsız seçenek bu ödülleri reklamsız verir." if GLOWFLY_STORE else "Hayır. Glowfly'da reklam yok."),
                 ("Glowfly ücretsiz mi?", "Evet, ücretsiz oynanır. Glowfly Plus, reklamsız seçenek ve elmas paketleri isteğe bağlı uygulama içi satın almalardır." if GLOWFLY_STORE else "Evet, ücretsiz oynanır; uygulama içi satın alma yoktur.")])]}
        write(path, page("glowfly", lang, path, alts("idle"), title, desc, body, [g["home"], (title, path)], schema=faq))


        # Offline progress explainer
        path, title, desc = g["offline"]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        body += defs("How it is usually calculated" if en else "Genelde nasıl hesaplanır", (
            [("Measured, not guessed", "While you play, the game measures how much damage or income you make per second. When you come back, it multiplies that rate by the time you were away. Glowfly measures your lights' real damage per second while the game is open."),
             ("Usually at a reduced rate", "Most idle games pay offline time at a share of the live rate, so playing actively still matters. In Glowfly, walls keep breaking at a share of your measured power and nights are cleared one by one."),
             ("Capped in time", "Offline progress stops after a few hours. The cap keeps the game fair and gives a reason to check in: in Glowfly the lights work for 4 hours after you leave, longer with Deep Sleep" + (" or Glowfly Plus" if GLOWFLY_STORE else "") + "."),
             ("Shown when you return", "A welcome-back screen sums up what happened: how long you were away, how many nights were cleared and what you earned, with the postcards you found on the way.")] if en else
            [("Tahmin değil, ölçüm", "Sen oynarken oyun saniyede ne kadar hasar ya da gelir ürettiğini ölçer. Döndüğünde bu hızı uzak kaldığın süreyle çarpar. Glowfly, oyun açıkken ışıklarının gerçek saniyelik hasarını ölçer."),
             ("Genelde düşük oranla", "Çoğu idle oyun kapalı süreyi canlı hızın bir payıyla öder; böylece aktif oynamak yine önemlidir. Glowfly'da duvarlar ölçülen gücünün bir payıyla kırılmaya devam eder, geceler tek tek aydınlanır."),
             ("Süre sınırlı", "Kapalıyken ilerleme birkaç saat sonra durur. Sınır oyunu adil tutar ve uğramak için bir sebep verir: Glowfly'da ışıklar ayrıldıktan sonra 4 saat çalışır; Derin uyku" + (" ya da Glowfly Plus" if GLOWFLY_STORE else "") + " ile daha uzun."),
             ("Döndüğünde gösterilir", "Tekrar hoş geldin ekranı olanları özetler: ne kadar uzak kaldığın, kaç gecenin aydınlandığı, ne kazandığın ve yolda bulunan kartpostallar.")]))
        body += shot(7, "The Sleeping Town chapter in Glowfly" if en else "Glowfly'da Uyuyan Kasaba bölümü")
        body += steps("Habits that make every return worth it" if en else "Her dönüşü değerli kılan alışkanlıklar", (
            ["Spend before you leave: upgrades bought now work for the whole time you're away.",
             "Start a boost that lasts through your break, like Deep Sleep before bed.",
             "Come back about when the cap runs out; after that, nothing more is earned.",
             "Collect first when you return, then merge and level up with what you earned.",
             "Don't worry about missing a day: an idle game is meant to wait for you."] if en else
            ["Ayrılmadan önce harca: şimdi aldığın güçlendirmeler uzak kaldığın sürenin tamamında çalışır.",
             "Arana yetecek bir takviye başlat; örneğin yatmadan önce Derin uyku.",
             "Sınır dolmaya yakın dön; sonrasında artık bir şey kazanılmaz.",
             "Döndüğünde önce topla, sonra kazancınla birleştir ve seviye yükselt.",
             "Bir gün kaçırmayı dert etme: idle oyun seni beklemek için yapılmıştır."]), ordered=False)
        body += paras(ESC("Good offline progress is generous but honest: it never asks you to set alarms, and it never punishes you for living your life."
                          if en else "İyi bir kapalıyken ilerleme cömert ama dürüsttür: sana alarm kurdurmaz ve hayatını yaşadığın için seni cezalandırmaz.")) + "\n"
        body += rel("offline")
        faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in (
                [("Do idle games keep progressing when closed?", "Most do. They measure your rate while you play and pay out the time you were away, usually at a reduced rate and up to a time limit."),
                 ("How long does Glowfly keep playing while closed?", "4 hours after you leave, longer with the Deep Sleep boost" + (" or Glowfly Plus" if GLOWFLY_STORE else "") + ".")] if en else
                [("Idle oyunlar kapalıyken ilerler mi?", "Çoğu ilerler. Oynarken hızını ölçer ve uzak kaldığın süreyi genelde düşük bir oranla ve bir süre sınırına kadar öder."),
                 ("Glowfly kapalıyken ne kadar oynar?", "Ayrıldıktan sonra 4 saat; Derin uyku takviyesi" + (" ya da Glowfly Plus" if GLOWFLY_STORE else "") + " ile daha uzun.")])]}
        write(path, page("glowfly", lang, path, alts("offline"), title, desc, body, [g["home"], (title, path)], schema=faq))
        # Beginner's guide
        path, title, desc = g["tips"]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        tips = ([("Collect often", "Light you earn waits on the Collect button at the top. Nothing is lost, but light you haven't collected can't be spent, so collect before you shop."),
                 ("Add lights to the lowest card", "The + is always on your lowest light. Once three kinds of light are open, each press adds five at once."),
                 ("Merge at ten", "When a card shows 10/10, merge: ten lights become one of the next kind, which is far stronger. Three kinds of light are in play at a time."),
                 ("Level up, too", "The ▲ button raises a light's level and every copy of it gets stronger. When adding lights gets expensive, levels are often the better deal."),
                 ("Pick skills at levels 5, 20 and 40", "Each light has three skill slots. A glowing slot is waiting for you to choose: more power, more light earned, faster flight or stronger hits on hard rock."),
                 ("Nothing is wasted", "When a fourth kind of light opens, the lowest one fades away, but a quarter of its levels passes on to the light above it."),
                 ("Tap and hold", "Tap a wall to hit it yourself, or hold the speed button to make everything faster. Glass breaks in one hit; big rocks take many."),
                 ("Use Power boosts for big walls", "A Power boost makes every light hit harder (and their trails flicker with flames). Light boosts double what you earn."),
                 ("Before bed, Deep Sleep", "The lights keep working for 4 hours after you leave. Deep Sleep adds more, so start it before a long break."),
                 ("Open boxes and daily gifts", "Star Boxes drop now and then and at every chapter end; the game shows exactly what each can contain. Claim the daily gift every day for boosts and gems.")] if en else
                [("Sık sık topla", "Kazandığın ışıltı üstteki Topla düğmesinde bekler. Hiçbir şey kaybolmaz ama toplanmamış ışıltı harcanamaz; alışverişten önce topla."),
                 ("Işığı en alttaki karta ekle", "+ her zaman en alttaki ışığındadır. Üç ışık açıldıktan sonra her basış beş ışığı birden ekler."),
                 ("10'da birleştir", "Bir kart 10/10 olunca birleştir: on ışık, çok daha güçlü bir sonraki ışık olur. Aynı anda üç ışık oyundadır."),
                 ("Seviye de yükselt", "▲ düğmesi ışığın seviyesini yükseltir, o ışığın bütün kopyaları güçlenir. Işık eklemek pahalılaşınca seviye çoğu zaman daha kârlıdır."),
                 ("5, 20 ve 40. seviyede beceri seç", "Her ışığın üç beceri yuvası var. Parlayan yuva seçim bekliyor: daha çok güç, daha çok ışıltı, daha hızlı uçuş ya da sert kayaya daha güçlü vuruş."),
                 ("Hiçbir şey boşa gitmez", "Dördüncü ışık açılınca en alttaki ışık solar, ama seviyelerinin dörtte biri bir üstteki ışığa geçer."),
                 ("Dokun ve basılı tut", "Bir duvara dokunarak kendin vur ya da her şeyi hızlandırmak için Hızlandır'a basılı tut. Cam tek vuruşta kırılır, iri kayalar çok vuruş ister."),
                 ("Büyük duvarlara Güç takviyesi", "Güç takviyesi bütün ışıkların daha sert vurmasını sağlar (izlerinden alevler yükselir). Işıltı takviyeleri kazancını ikiye katlar."),
                 ("Yatmadan önce Derin uyku", "Ayrıldıktan sonra ışıklar 4 saat çalışır. Derin uyku bu süreyi uzatır; uzun bir aradan önce başlat."),
                 ("Kutuları ve günlük hediyeyi aç", "Yıldız kutuları ara sıra ve her bölüm sonunda düşer; oyun her birinden neler çıkabileceğini açıkça gösterir. Takviye ve elmas için günlük hediyeyi her gün al.")])
        for i, (h, p) in enumerate(tips):
            body += f"  <h2>{i + 1}. {ESC(h)}</h2>\n  <p>{ESC(p)}</p>\n"
            if i == 4:
                body += shot(8, "The Deep Sea chapter in Glowfly" if en else "Glowfly'da Derin Deniz bölümü")
        body += paras(ESC("Stuck or found a bug? Write to hyapps@outlook.com; every message is read."
                          if en else "Takıldın ya da bir hata mı buldun? hyapps@outlook.com adresine yaz; her mesaj okunur.")) + "\n"
        body += rel("tips")
        write(path, page("glowfly", lang, path, alts("tips"), title, desc, body, [g["home"], (title, path)]))


# ---------------------------------------------------------------- Besmele: verses, hadiths and duas from the app

def load_kind(file, kind):
    with open(os.path.join(HIKMET, file)) as f:
        return [s for day in json.load(f) for s in day["sozler"] if s["kategori"] == kind]


COLLECTIONS = {
    "dua": {"tr": ("/besmele/kisa-dualar/", "Kısa Dualar: Arapçası ve Türkçe Anlamıyla 99 Dua",
                   "Kur'an'dan ve sünnetten 99 kısa dua: Arapça yazılışı, Türkçe anlamı ve kaynağıyla. Ezberlemesi kolay, günlük okunabilecek dualar.",
                   "Aşağıda Arapça yazılışı, Türkçe anlamı ve kaynağıyla 99 kısa dua bulacaksın. Hepsi Besmele uygulamasında her gün bir tane olmak üzere gösterilen dualardır."),
            "en": ("/besmele/en/short-duas/", "99 Short Duas in Arabic with English Meaning",
                   "99 short duas (supplications) from the Qur'an and the Sunnah, each with its Arabic text, English meaning and source. Easy to memorize and read every day.",
                   "Below are 99 short duas, each with its Arabic text, English meaning and source. They are the duas the Bismillah app shows one day at a time.")},
    "hadis": {"tr": ("/besmele/kisa-hadisler/", "Kısa Hadisler: Anlamı ve Kaynağıyla 99 Hadis-i Şerif",
                     "Anlamı ve kaynağıyla 99 kısa hadis-i şerif: güzel ahlak, niyet, merhamet, sabır ve iyilik üzerine; ezberlemesi ve paylaşması kolay.",
                     "Aşağıda Türkçe anlamı ve kaynağıyla 99 kısa hadis bulacaksın; bir kısmının Arapça metni de var. Hepsi Besmele uygulamasında her gün bir tane olmak üzere gösterilen hadislerdir."),
              "en": ("/besmele/en/short-hadiths/", "99 Short Hadiths with English Meaning and Source",
                     "99 short hadiths with their English meaning and source, on good character, intention, mercy, patience and kindness. Easy to memorize and share.",
                     "Below are 99 short hadiths with their English meaning and source; some include the Arabic text. They are the hadiths the Bismillah app shows one day at a time.")},
    "ayet": {"tr": ("/besmele/kisa-ayetler/", "Kısa Ayetler: Arapçası ve Mealiyle 99 Kur'an Ayeti",
                    "Arapça yazılışı, Türkçe meali ve sûre adıyla 99 kısa Kur'an ayeti: sabır, şükür, umut ve huzur veren ayetler.",
                    "Aşağıda Arapça yazılışı, Türkçe meali ve sûresiyle 99 kısa ayet bulacaksın. Hepsi Besmele uygulamasında her gün bir tane olmak üzere gösterilen ayetlerdir."),
             "en": ("/besmele/en/short-quran-verses/", "99 Short Qur'an Verses in Arabic with English Meaning",
                    "99 short verses of the Qur'an with their Arabic text, English meaning and surah reference: verses on patience, gratitude, hope and peace of heart.",
                    "Below are 99 short verses with their Arabic text, English meaning and surah reference. They are the verses the Bismillah app shows one day at a time.")},
}
COLLECTION_SHORT = {"dua": {"tr": "Kısa dualar", "en": "Short duas"}, "hadis": {"tr": "Kısa hadisler", "en": "Short hadiths"},
                    "ayet": {"tr": "Kısa ayetler", "en": "Short Qur'an verses"}}


def build_besmele_collections():
    files = {"tr": "icerik.json", "en": "icerik_en.json"}
    for kind, langs in COLLECTIONS.items():
        for lang in ("tr", "en"):
            path, title, desc, intro = langs[lang]
            other = "en" if lang == "tr" else "tr"
            items = load_kind(files[lang], kind)
            assert len(items) == 99
            rows = ""
            for s in items:
                ar = f'<p class="ar" lang="ar">{ESC(s["arapca"])}</p>' if s.get("arapca") else ""
                text = ESC(s["metin"]).replace("\n", "<br>")
                rows += f'<li>{ar}<p class="t">{text}</p><p class="src">{ESC(s.get("kaynak", ""))}</p></li>'
            body = (f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(intro)}</p>\n  <ol class="quotes">{rows}</ol>\n'
                    f'  <p class="note">{ESC(T_ESMA[lang]["note"])}</p>\n')
            links = [(COLLECTION_SHORT[k][lang], COLLECTIONS[k][lang][0]) for k in COLLECTIONS if k != kind]
            links.append((T_ESMA[lang]["hub_title"], NAME_BASE[lang]))
            body += related(T_ESMA[lang]["related"], links)
            crumbs = [(T_ESMA[lang]["crumbs_home"], APPS["besmele"]["home"][lang]), (title, path)]
            write(path, page("besmele", lang, path, {lang: path, other: langs[other][0]}, title, desc, body, crumbs))


# ---------------------------------------------------------------- Crownly: logic puzzles like sudoku

CG_LIKE = {
    "en": ("/crownly/games-like-sudoku/", "Games Like Sudoku: Queens and 5 Other Logic Puzzles Worth Trying",
           "Finished your sudoku? Six logic puzzles with the same pure-deduction feel: Queens, nonograms, kakuro, killer sudoku, futoshiki and tents, with the rules of each."),
    "tr": ("/crownly/tr/sudoku-benzeri-oyunlar/", "Sudoku Benzeri Oyunlar: Queens ve Denemeye Değer 5 Mantık Bulmacası",
           "Sudoku'yu bitirdin mi? Aynı saf mantık tadını veren altı bulmaca: Queens, nonogram, kakuro, killer sudoku, futoshiki ve çadırlar; her birinin kurallarıyla."),
}


def build_crownly_like():
    for lang in ("en", "tr"):
        en = lang == "en"
        g = CG[lang]
        path, title, desc = CG_LIKE[lang]
        other = CG_LIKE["tr" if en else "en"][0]
        body = f'  <h1>{ESC(title)}</h1>\n  <p class="intro">{ESC(desc)}</p>\n'
        body += paras(ESC("What makes sudoku satisfying is not the numbers. It is that every puzzle has exactly one solution and you can "
                          "reach it by reasoning alone, never by guessing. These six puzzles share that quality." if en else
                          "Sudoku'yu keyifli yapan sayılar değildir. Her bulmacanın tek bir çözümü olması ve o çözüme tahminle değil, "
                          "yalnızca akıl yürüterek ulaşılmasıdır. Bu altı bulmaca da aynı özelliği taşır.")) + "\n"
        items = ([("1. Queens", "The board is split into colored regions. Place one crown in every row, every column and every region, and no two crowns may touch, not even diagonally. There are no numbers at all, so a board reads at a glance, and a small one takes a minute or two. It is the same family as Star Battle."),
                  ("2. Nonogram", "Numbers beside each row and above each column give the lengths of the filled blocks in that line, in order. Fill the right cells and a small picture appears."),
                  ("3. Kakuro", "A crossword made of sums. Each run of white cells must add up to the clue next to it, using the digits 1 to 9 without repeating a digit inside a run."),
                  ("4. Killer sudoku", "Ordinary sudoku rules, but instead of given digits the grid is divided into cages. The digits in a cage add up to its small number, and a digit cannot repeat inside a cage."),
                  ("5. Futoshiki", "Fill the grid so every row and column holds each number once, like a small sudoku without boxes, while obeying the greater-than and less-than signs between cells."),
                  ("6. Tents", "Every tree on the grid needs one tent in a cell next to it. Tents may not touch each other, not even diagonally, and the numbers at the edges say how many tents each row and column holds.")] if en else
                 [("1. Queens", "Tahta renkli bölgelere ayrılmıştır. Her satıra, her sütuna ve her bölgeye bir taç koyarsın; iki taç birbirine çaprazdan bile dokunamaz. Hiç sayı yoktur, tahta bir bakışta okunur; küçük bir tahta bir iki dakika sürer. Star Battle ile aynı ailedendir."),
                  ("2. Nonogram", "Her satırın yanındaki ve her sütunun üstündeki sayılar, o çizgideki dolu blokların uzunluklarını sırasıyla verir. Doğru kareleri doldurunca küçük bir resim ortaya çıkar."),
                  ("3. Kakuro", "Toplamlardan oluşan bir çapraz bulmaca. Her beyaz kare dizisi, yanındaki ipucu sayısını vermelidir; 1'den 9'a rakamlar kullanılır ve bir dizide aynı rakam tekrarlanmaz."),
                  ("4. Killer sudoku", "Kurallar bildiğin sudoku, ama verilmiş rakamlar yerine ızgara kafeslere bölünmüştür. Bir kafesteki rakamların toplamı köşedeki küçük sayıyı verir ve kafes içinde rakam tekrarlanmaz."),
                  ("5. Futoshiki", "Her satır ve sütunda her sayı bir kez bulunacak şekilde ızgarayı doldurursun (kutusuz küçük bir sudoku gibi); kareler arasındaki büyüktür ve küçüktür işaretlerine de uyarsın."),
                  ("6. Çadırlar (Tents)", "Izgaradaki her ağacın yanındaki bir kareye bir çadır gerekir. Çadırlar birbirine çaprazdan bile dokunamaz; kenardaki sayılar her satır ve sütunda kaç çadır olduğunu söyler.")])
        for h, p in items:
            body += f"  <h2>{ESC(h)}</h2>\n  <p>{ESC(p)}</p>\n"
        body += f"  <h2>{ESC('Where to start' if en else 'Nereden başlamalı')}</h2>\n"
        body += paras(ESC(f"If you want something quicker than sudoku, start with Queens: the rules fit in one sentence and the first boards "
                          f"are solved in a minute. Crownly has a new Queens puzzle every day and {CROWNLY_LEVELS['en']} levels, and when you are "
                          f"stuck its hints explain the reasoning instead of just showing the answer." if en else
                          f"Sudoku'dan daha kısa süren bir şey istiyorsan Queens ile başla: kuralları tek cümleye sığar, ilk tahtalar bir dakikada "
                          f"çözülür. Crownly'de her gün yeni bir Queens bulmacası ve {CROWNLY_LEVELS['tr']} seviye var; takıldığında ipuçları "
                          f"yalnızca cevabı göstermez, mantığını anlatır.")) + "\n"
        body += related(g["related"], [(g[k][1].split(":")[0], g[k][0]) for k in ("rules", "strategy", "alt")])
        write(path, page("crownly", lang, path, {lang: path, ("tr" if en else "en"): other}, title, desc, body, [g["home"], (title, path)]))


# ---------------------------------------------------------------- sitemap

STATIC = [("/", {"en": "/", "tr": "/tr/"}), ("/tr/", {"en": "/", "tr": "/tr/"}),
          ("/crownly/", {"en": "/crownly/", "tr": "/crownly/tr/"}), ("/crownly/tr/", {"en": "/crownly/", "tr": "/crownly/tr/"}),
          ("/crownly/privacy.html", {}),
          ("/quickwits/", {"en": "/quickwits/", "tr": "/quickwits/tr/"}), ("/quickwits/tr/", {"en": "/quickwits/", "tr": "/quickwits/tr/"}),
          ("/quickwits/privacy.html", {}),
          ("/brickhaven/", {"en": "/brickhaven/", "tr": "/brickhaven/tr/"}), ("/brickhaven/tr/", {"en": "/brickhaven/", "tr": "/brickhaven/tr/"}),
          ("/brickhaven/privacy.html", {}),
          ("/glowfly/", {"en": "/glowfly/", "tr": "/glowfly/tr/"}), ("/glowfly/tr/", {"en": "/glowfly/", "tr": "/glowfly/tr/"}),
          ("/glowfly/privacy.html", {}),
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
build_besmele_collections()
build_crownly_guides()
build_crownly_like()
build_crownly_play()
build_quickwits_guides()
build_brickhaven_guides()
build_glowfly_guides()
build_sitemap()
print(f"guide pages: {len(PAGES)}")

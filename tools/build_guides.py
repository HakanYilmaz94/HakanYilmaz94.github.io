#!/usr/bin/env python3
"""Builds the SEO guide pages and the sitemap.

Usage: python3 -I tools/build_guides.py   (run from the site repo root)

- Besmele: Esmaül Hüsna hub + 99 name pages (TR /besmele/esma/, EN /besmele/en/names/) from the app's own data
  (Hikmet/Ortak/icerik.json, icerik_en.json), plus two how-to guides per language.
- Crownly: Queens rules, strategy and "LinkedIn Queens alternative" guides (EN + TR).
- sitemap.xml for the whole site.
Shared look: /assets/app.css (+ /besmele/besmele.css). Analytics snippet and share tags on every page.
"""
import html
import json
import os
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
}
STORE_LABEL = {"en": "Download on the App Store", "tr": "App Store'dan indir"}
MADE = {"en": "Made with care by an independent developer.", "tr": "Bağımsız bir geliştirici tarafından yapıldı."}
PRIVACY = {"crownly": {"en": "/crownly/privacy.html", "tr": "/crownly/privacy.html#tr"},
           "besmele": {"en": "/besmele/en/gizlilik.html", "tr": "/besmele/gizlilik.html"}}
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


def page(app, lang, path, alts, title, desc, body, crumbs, schema=None):
    """Renders one guide page. alts = {lang: path} for hreflang; crumbs = [(label, href)]."""
    a = APPS[app]
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
  <link rel="canonical" href="{SITE}{path}">{hreflang}
  <meta name="apple-itunes-app" content="app-id={a["id"]}">
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
  <link rel="stylesheet" href="/assets/app.css">{css}
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
    <a class="store" href="{ESC(store_url(app, lang))}">{ESC(STORE_LABEL[lang])}</a>
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


# ---------------------------------------------------------------- sitemap

STATIC = [("/", {"en": "/", "tr": "/tr/"}), ("/tr/", {"en": "/", "tr": "/tr/"}),
          ("/crownly/", {"en": "/crownly/", "tr": "/crownly/tr/"}), ("/crownly/tr/", {"en": "/crownly/", "tr": "/crownly/tr/"}),
          ("/crownly/privacy.html", {}),
          ("/quickwits/", {"en": "/quickwits/", "tr": "/quickwits/tr/"}), ("/quickwits/tr/", {"en": "/quickwits/", "tr": "/quickwits/tr/"}),
          ("/quickwits/privacy.html", {}),
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
build_sitemap()
print(f"guide pages: {len(PAGES)}")

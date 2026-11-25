"""Link-in-bio pages for the social accounts: /links/<platform>/ (noindex, not in the sitemap).
Each App Store button carries the platform as its campaign (ct=<platform>), so App Store Connect -> Analytics ->
Acquisition -> Campaigns shows which account brought the downloads. Cloudflare Web Analytics counts page visits per path.
usage: python3 -I tools/build_links.py
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATFORMS = ["tiktok", "instagram", "youtube", "x"]
APPS = [  # (folder, name, line, App Store id)
    ("brickhaven", "Brickhaven", "Build a cozy brick town, one brick at a time", "6826958666"),
    ("birbdoku", "Birbdoku", "A cozy cockatiel logic puzzle", "6837803599"),
    ("glowfly", "Glowfly", "A relaxing idle game of glowing fireflies", "6830895618"),
]
CF = """<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "89e9ceae59114244a972f60af4a20851"}'></script><!-- End Cloudflare Web Analytics -->"""

def page(platform):
    cards = "\n".join(f"""    <a class="app" href="https://apps.apple.com/app/apple-store/id{aid}?pt=129592179&ct={platform}&mt=8">
      <img src="/{k}/img/icon.png" alt="" width="64" height="64">
      <span><b>{name}</b><small>{line}</small></span>
      <i>App Store</i>
    </a>""" for k, name, line, aid in APPS)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>HY Apps · Cozy games by a solo dev</title>
  <link rel="icon" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <style>
    :root {{ --bg:#2e1b47; --card:#fff8e8; --ink:#3b2a57; --muted:#7a6f8f; --accent:#cc663d; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; min-height:100vh; background:radial-gradient(circle at 50% 30%, #6a4596, #4a2d6e 50%, #2e1b47);
           color:var(--ink); font:16px/1.4 ui-rounded, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    main {{ max-width:460px; margin:0 auto; padding:40px 16px 56px; display:grid; gap:14px; }}
    header {{ text-align:center; color:#fff8e8; margin-bottom:10px; }}
    header img {{ width:96px; height:96px; border-radius:50%; box-shadow:0 8px 24px rgba(0,0,0,.35); }}
    h1 {{ font-size:26px; margin:12px 0 2px; }}
    header p {{ margin:0; opacity:.85; }}
    .app {{ display:flex; align-items:center; gap:14px; padding:14px; background:var(--card); border-radius:20px;
            color:var(--ink); text-decoration:none; box-shadow:0 6px 18px rgba(0,0,0,.25); }}
    .app img {{ border-radius:15px; flex:none; }}
    .app span {{ flex:1; display:grid; }}
    .app b {{ font-size:18px; }}
    .app small {{ color:var(--muted); font-size:14px; }}
    .app i {{ font-style:normal; font-weight:700; font-size:13px; color:#fff; background:var(--ink); padding:7px 12px; border-radius:999px; white-space:nowrap; }}
    footer {{ text-align:center; margin-top:8px; }}
    footer a {{ color:#fff8e8; opacity:.85; }}
  </style>
  {CF}
</head>
<body>
  <main>
    <header>
      <img src="/assets/hyapps-logo.png" alt="HY Apps">
      <h1>HY Apps</h1>
      <p>Cozy games by a solo dev</p>
    </header>
{cards}
    <footer><a href="/?ref={platform}">hyapps.app</a></footer>
  </main>
</body>
</html>
"""

for p in PLATFORMS:
    d = os.path.join(ROOT, "links", p)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(page(p))
    print(f"links/{p}/index.html")

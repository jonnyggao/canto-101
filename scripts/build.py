#!/usr/bin/env python3
"""
Rebuild the public site in /docs from UTF-8 copies in /source/raw.
Downloads images from the original EdUHK host (requires legacy TLS).
"""
from __future__ import annotations

import re
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "source" / "raw"
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets" / "original"
BASE = "https://www.eduhk.hk/cle/resources/cep/cantonese-survival-package/"

PAGES: list[tuple[str, str, str, str]] = [
    # raw_filename, out_filename, nav_id, document_title
    ("index.html", "index.html", "home", "Course overview"),
    ("unit1.html", "unit1.html", "unit1", "Unit 1 — Introduction"),
    ("unit2.html", "unit2.html", "unit2", "Unit 2 — Greetings"),
    ("unit3.html", "unit3.html", "unit3", "Unit 3 — Introducing oneself"),
    ("unit4.html", "unit4.html", "unit4", "Unit 4 — Manners"),
    ("unit5.html", "unit5.html", "unit5", "Unit 5 — Numbers and money"),
    ("unit6.html", "unit6.html", "unit6", "Unit 6 — Time and routine"),
    ("unit7.html", "unit7.html", "unit7", "Unit 7 — Getting around"),
    ("unit8.html", "unit8.html", "unit8", "Unit 8 — Shopping, food & drink"),
    ("unit9.html", "unit9.html", "unit9", "Unit 9 — Transportation"),
    ("unit10.html", "unit10.html", "unit10", "Unit 10 — Education terms"),
    ("unit11.html", "unit11.html", "unit11", "Unit 11 — Emergency"),
    ("unit12.html", "unit12.html", "unit12", "Unit 12 — Classroom language"),
    ("unit13.html", "unit13.html", "unit13", "Unit 13 — Social skills"),
    ("unit14.html", "unit14.html", "unit14", "Unit 14 — Places in Hong Kong"),
    ("unit15.html", "unit15.html", "unit15", "Unit 15 — Reflection"),
    ("Appendix_I.html", "appendix-i.html", "appendix", "Appendix I — Romanization"),
]


def ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    if hasattr(ssl, "OP_LEGACY_SERVER_CONNECT"):
        ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT
    return ctx


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, context=ssl_context(), timeout=120).read()


def extract_main(html: str) -> str:
    m_open = re.search(r'<div style="Z-INDEX: 1[^>]*>', html, re.I)
    if not m_open:
        raise ValueError("Could not find main content container")
    start = m_open.end()
    m_close = re.search(
        r"</div>\s*<p class=\"style3\"><b>© Copyright",
        html[start:],
        re.S,
    )
    if not m_close:
        raise ValueError("Could not find end of main content")
    return html[start : start + m_close.start()]


def transform_content(fragment: str) -> str:
    # Drop legacy banner
    fragment = re.sub(
        r"\s*<br\s*/?>\s*<div style=\"text-decoration:center[^\"]*\"[^>]*>\s*"
        r'<img src="Banner\.png"\s*>\s*</div>\s*<br\s*/?>\s*<br\s*/?>\s*',
        "",
        fragment,
        flags=re.I,
    )
    # Point images to vendored copies
    fragment = re.sub(
        r'src="pic/', 'src="assets/original/pic/', fragment, flags=re.I
    )
    fragment = re.sub(
        r'src="star\.png"', 'src="assets/original/star.png"', fragment, flags=re.I
    )
    # Remove decorative line.gif rows (spacing handled in CSS)
    fragment = re.sub(
        r'(?:<br\s*/?>\s*)*<div[^>]*>\s*(?:<img[^>]*(?:line\.gif)[^>]*>\s*)+</div>\s*(?:<br\s*/?>\s*)*',
        "\n",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(
        r'<img[^>]*(?:line\.gif)[^>]*>\s*',
        "",
        fragment,
        flags=re.I,
    )
    # Fix missing hash in inline colors
    fragment = re.sub(
        r"color:0101DF", "color:#0101DF", fragment, flags=re.I
    )
    fragment = re.sub(
        r"color:0101DF;", "color:#0101DF;", fragment, flags=re.I
    )
    # Lazy-load figures
    fragment = re.sub(
        r"<img ",
        '<img loading="lazy" ',
        fragment,
        flags=re.I,
    )
    fragment = re.sub(
        r'<img loading="lazy" loading="lazy" ',
        '<img loading="lazy" ',
        fragment,
        flags=re.I,
    )
    fragment = re.sub(r'class="style2"style=', 'class="style2" style=', fragment, flags=re.I)
    fragment = re.sub(r'(href="[^"]+")style=', r"\1 style=", fragment, flags=re.I)
    return fragment.strip()


def link_index_units(fragment: str) -> str:
    for i in range(1, 16):
        fragment = re.sub(
            rf'<p class="style2">\s*Unit {i}:\s*([^<]*)</p>',
            rf'<p class="style2"><a href="unit{i}.html">Unit {i}: \1</a></p>',
            fragment,
            flags=re.I,
        )
    return fragment


def collect_asset_paths(html: str) -> set[str]:
    paths: set[str] = set()
    for m in re.finditer(r'src="(pic/[^"]+|star\.png|Banner\.png)"', html, re.I):
        paths.add(m.group(1).replace("\\", "/"))
    return paths


def page_shell(*, title: str, nav_id: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="color-scheme" content="light dark" />
  <title>{title} · Survival Cantonese</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="assets/site.css" />
</head>
<body data-current="{nav_id}">
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="layout">
    <header class="site-header">
      <div class="brand">
        <span class="brand-title">Survival Cantonese</span>
        <span class="brand-sub">Beginner themes for life in Hong Kong (legacy CLE materials, remastered layout)</span>
      </div>
      <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="drawer-nav">
        Menu
      </button>
    </header>
    <div class="layout-inner">
      <aside class="drawer" id="drawer-nav">
        <nav class="side-nav" aria-label="Units"></nav>
      </aside>
      <div class="backdrop" id="nav-backdrop" hidden></div>
      <main id="main" class="main prose">
        <article class="content-area">
{body}
        </article>
        <footer class="site-footer">
          <p><strong>© The Hong Kong Institute of Education (2013)</strong> — original materials. Not to be reproduced without permission of the copyright holder.</p>
          <p class="muted">Modernized static mirror for personal / educational use. Source: EdUHK CLE Cantonese Survival Package.</p>
        </footer>
      </main>
    </div>
  </div>
  <script src="assets/site.js" defer></script>
</body>
</html>
"""


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "pic").mkdir(parents=True, exist_ok=True)

    all_html = ""
    for raw_name, _, _, _ in PAGES:
        all_html += (RAW / raw_name).read_text(encoding="utf-8")

    rel_paths = collect_asset_paths(all_html)
    print(f"Downloading {len(rel_paths)} assets…")
    for rel in sorted(rel_paths):
        dest = ASSETS / Path(rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        url = BASE + rel.replace("\\", "/")
        if dest.exists() and dest.stat().st_size > 0:
            continue
        try:
            data = fetch_bytes(url)
            dest.write_bytes(data)
            print("  OK", rel, len(data))
        except Exception as e:
            print("  FAIL", rel, e)

    DOCS.mkdir(parents=True, exist_ok=True)
    for raw_name, out_name, nav_id, doc_title in PAGES:
        raw = (RAW / raw_name).read_text(encoding="utf-8")
        inner = transform_content(extract_main(raw))
        if out_name == "index.html":
            inner = link_index_units(inner)
        title = doc_title
        out = page_shell(title=title, nav_id=nav_id, body=inner)
        (DOCS / out_name).write_text(out, encoding="utf-8")
        print("Wrote", out_name)

    # Copy static shared assets (css/js) from repo templates
    static_css = ROOT / "site-static" / "site.css"
    static_js = ROOT / "site-static" / "site.js"
    if static_css.exists():
        (DOCS / "assets" / "site.css").write_bytes(static_css.read_bytes())
    if static_js.exists():
        (DOCS / "assets" / "site.js").write_bytes(static_js.read_bytes())

    print("Done.")


if __name__ == "__main__":
    main()

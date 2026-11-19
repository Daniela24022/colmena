"""Builds the Colmena page.

Reads src/colmena.html, embeds the images from src/img/ as data URIs and writes:
  - pagina_web/index.html          full standalone page (open offline, or upload to any free host)
  - pagina_web/src/_fragment.html  same content without the document wrapper (for the Claude artifact)
Run:  python build.py
"""
import base64, pathlib, re

SRC = pathlib.Path(__file__).resolve().parent
OUT = SRC.parent
html = (SRC / "colmena.html").read_text(encoding="utf-8")

def embed(m):
    name = m.group(1)
    data = (SRC / "img" / f"{name}.jpg").read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(data).decode()

html = re.sub(r"\{\{IMG:([\w-]+)\}\}", embed, html)
(SRC / "_fragment.html").write_text(html, encoding="utf-8")

full = (
    "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
    "<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 92'%3E%3Cpolygon points='50,10 67.3,20 67.3,40 50,50 32.7,40 32.7,20' fill='%23E09200'/%3E%3Cpolygon points='31.2,42.5 48.5,52.5 48.5,72.5 31.2,82.5 13.9,72.5 13.9,52.5' fill='%23F6C453'/%3E%3Cpolygon points='68.8,42.5 86.1,52.5 86.1,72.5 68.8,82.5 51.5,72.5 51.5,52.5' fill='%232F6B6B'/%3E%3C/svg%3E\">\n"
)
# move <title>/<meta>/<link>/<style> into <head>, the rest into <body>
split = html.index("</style>") + len("</style>")
full += html[:split] + "\n<style>[hidden]{display:none!important}img{max-width:100%}</style>\n</head>\n<body>\n" + html[split:] + "\n</body>\n</html>\n"
(OUT / "index.html").write_text(full, encoding="utf-8")
print("OK:", OUT / "index.html", f"{len(full)//1024} KB")

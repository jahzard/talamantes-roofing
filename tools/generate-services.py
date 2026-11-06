#!/usr/bin/env python3
"""Build four service pages with shared homepage chrome and bilingual copy."""
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://talamantes-roofing.vercel.app"
SERVICES = json.loads((ROOT / "tools/services.json").read_text())
HOME = (ROOT / "index.html").read_text()
COPY_FILE = ROOT / "script.js"
script = COPY_FILE.read_text()
copy = json.loads(re.search(r"const spanishCopy = (\{.*?\n\});", script, re.S).group(1))


def register(value):
    if isinstance(value, list):
        if len(value) == 2 and all(isinstance(v, str) for v in value):
            copy[value[0]] = value[1]
        else:
            for item in value:
                register(item)
    elif isinstance(value, dict):
        for item in value.values():
            register(item)


COMMON = {
    "Home": "Inicio",
    "Roofing services": "Servicios de techado",
    "Service navigation": "Navegación de servicios",
    "Learn more": "Más información",
    "What to expect": "Qué esperar",
    "A clear path from inspection to roofing work.": "Un proceso claro, desde la inspección hasta el trabajo de techado.",
    "From our project gallery": "De nuestra galería de proyectos",
    "Real roofing work, up close.": "Trabajos reales de techado, de cerca.",
    "These photos show separate projects, not a before-and-after sequence.": "Estas fotos muestran proyectos distintos, no una secuencia de antes y después.",
    "See all past work": "Ver todos los trabajos",
    "Common questions": "Preguntas frecuentes",
    "Explore other roofing services": "Explore otros servicios de techado",
    "Talk through your roofing project.": "Hablemos de su proyecto de techado.",
    "Based in Los Angeles. Serving Los Angeles, Orange County, Ventura, and San Bernardino.": "Con sede en Los Ángeles. Atendemos Los Ángeles, Orange County, Ventura y San Bernardino.",
    "Available daily, 6 a.m.–6 p.m.": "Horario: todos los días, de 6 a. m. a 6 p. m.",
    "Breadcrumb": "Ruta de navegación",
}
copy.update(COMMON)
for service in SERVICES:
    register(service)


def t(pair):
    return html.escape(pair[0], quote=True)


def image(src, alt, eager=False):
    # Explicit dimensions reserve image space; CSS handles the editorial crop.
    return f'<img src="{src}" alt="{t(alt)}" width="1200" height="900" loading="{"eager" if eager else "lazy"}" decoding="async"' + (' fetchpriority="high"' if eager else '') + '>'


def render(service):
    slug = service["slug"]
    head = HOME.split("<body>")[0]
    head = re.sub(r'<meta name="google-site-verification"[^>]+>\s*', '', head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{t(service["description"])}">', head)
    head = re.sub(r'<title>.*?</title>', f'<title>{t(service["title"])}</title>', head)
    head = head.replace(f'{ORIGIN}/es/"', f'{ORIGIN}/es/{slug}.html"')
    head = head.replace(f'{ORIGIN}/"', f'{ORIGIN}/{slug}.html"')
    chrome = HOME.split('<body>')[1].split('  <main')[0]
    for anchor in ('top', 'services', 'areas', 'testimonials'):
        chrome = chrome.replace(f'href="#{anchor}"', 'href="./"' if anchor == 'top' else f'href="./#{anchor}"')
    chrome = chrome.replace('href="es/"', f'href="es/{slug}.html"')
    footer = '  <footer' + HOME.split('  <footer', 1)[1]
    footer = footer.replace('href="es/"', f'href="es/{slug}.html"')
    nav = ''.join(f'<a href="{s["slug"]}.html"' + (' aria-current="page"' if s["slug"] == slug else '') + f'>{t(s["label"])}</a>' for s in SERVICES)
    features = ''.join(f'<article><span class="service-feature-number">0{i}</span><h3>{t(title)}</h3><p>{t(body)}</p></article>' for i, (title, body) in enumerate(service['features'], 1))
    steps = ''.join(f'<li><h3>{t(title)}</h3><p>{t(body)}</p></li>' for title, body in service['process'])
    photos = ''.join(f'<figure>{image(src, alt)}<figcaption>{t(caption)}</figcaption></figure>' for src, alt, caption in service['photos'])
    faqs = ''.join(f'<details><summary>{t(question)}</summary><p>{t(answer)}</p></details>' for question, answer in service['faqs'])
    related = ''.join(f'<a href="{s["slug"]}.html">{t(s["label"])}<svg class="icon" aria-hidden="true"><use href="#arrow"/></svg></a>' for s in SERVICES if s['slug'] != slug)
    main = f'''  <main id="main" class="service-page">
    <section class="service-hero"><div class="wrap">
      <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="./">Home</a><span aria-hidden="true">/</span><a href="./#services">Roofing services</a><span aria-hidden="true">/</span><span>{t(service['label'])}</span></nav>
      <div class="service-hero-grid"><div class="service-hero-copy"><p class="eyebrow">Los Angeles roofing <span></span></p><h1>{t(service['heading'])}</h1><p class="service-lead">{t(service['lead'])}</p><p>{t(service['intro'])}</p><div class="service-actions"><button class="button button-copper" data-estimate>Free Estimate</button><a class="service-call" href="tel:+18183958754"><svg class="icon" aria-hidden="true"><use href="#phone"/></svg>818-395-8754</a></div></div>
      <figure class="service-hero-photo">{image(service['hero'], service['heroAlt'], True)}<figcaption>{t(service['heroCaption'])}</figcaption></figure></div>
    </div></section>
    <nav class="service-navigation" aria-label="Service navigation"><div class="wrap">{nav}</div></nav>
    <section class="service-overview service-section"><div class="wrap"><div class="service-section-intro"><p class="eyebrow">{t(service['label'])}</p><h2>{t(service['overviewTitle'])}</h2><p>{t(service['overview'])}</p></div><div class="service-feature-grid">{features}</div></div></section>
    <section class="service-process service-section"><div class="wrap"><div class="service-section-intro"><p class="eyebrow">What to expect</p><h2>A clear path from inspection to roofing work.</h2></div><ol>{steps}</ol></div></section>
    <section class="service-projects service-section"><div class="wrap"><div class="service-section-intro"><p class="eyebrow">From our project gallery</p><h2>Real roofing work, up close.</h2><p>These photos show separate projects, not a before-and-after sequence.</p></div><div class="service-photo-grid">{photos}</div><a class="service-gallery-link" href="past-work.html">See all past work <svg class="icon" aria-hidden="true"><use href="#arrow"/></svg></a></div></section>
    <section class="service-faq service-section"><div class="wrap service-faq-grid"><h2>Common questions</h2><div>{faqs}</div></div></section>
    <section class="service-related service-section"><div class="wrap"><h2>Explore other roofing services</h2><div class="service-related-grid">{related}</div></div></section>
    <section class="service-local"><div class="wrap"><div><h2>Talk through your roofing project.</h2><p>Based in Los Angeles. Serving Los Angeles, Orange County, Ventura, and San Bernardino.</p><p class="service-hours">Available daily, 6 a.m.–6 p.m.</p></div><button class="button button-copper" data-estimate>Free Estimate</button></div></section>
  </main>

'''
    (ROOT / f'{slug}.html').write_text(head + '<body>' + chrome + main + footer)
    print(f'Generated {slug}.html')


for service in SERVICES:
    render(service)
script = re.sub(r'const spanishCopy = (\{.*?\n\});', lambda _: 'const spanishCopy = ' + json.dumps(copy, ensure_ascii=False, indent=2) + ';', script, count=1, flags=re.S)
COPY_FILE.write_text(script)

# Each URL advertises its matching language version, including in the sitemap.
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
tree = ET.Element(ns + 'urlset')
for file in ['index.html', 'past-work.html'] + [s['slug'] + '.html' for s in SERVICES]:
    en = ORIGIN + ('/' if file == 'index.html' else '/' + file)
    es = ORIGIN + ('/es/' if file == 'index.html' else '/es/' + file)
    for loc in (en, es):
        entry = ET.SubElement(tree, ns + 'url')
        ET.SubElement(entry, ns + 'loc').text = loc
        for lang, href in [('en', en), ('es', es), ('x-default', en)]:
            ET.SubElement(entry, '{http://www.w3.org/1999/xhtml}link', {'rel': 'alternate', 'hreflang': lang, 'href': href})
ET.indent(tree, space='  ')
ET.ElementTree(tree).write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)

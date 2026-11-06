# Talamantes Roofing

This is a static HTML website with no build step or dependency installation. Use a local server to preview all page and language links.

For a local server, run `python3 -m http.server 8000 --bind 127.0.0.1` from this folder, then open http://127.0.0.1:8000.

## Included

- Responsive desktop, tablet, and mobile layouts based on the approved mockup.
- All eight services, followed by Areas Served and then the benefits section.
- Phone links for 818-395-8754.
- Free Estimate buttons that open an accessible contact dialog. They do not submit data; the next step is a call.
- Mobile navigation, keyboard support, reduced-motion support, and locally stored images.
- Top and bottom language links connect complete English and Spanish pages. Spanish content, metadata, navigation, testimonials, accessibility labels, and gallery captions are present in the HTML, including when JavaScript is disabled. Each URL always serves its own language, independently of browser settings or past preferences.

## Files

- `index.html`: page content and icon definitions.
- `past-work.html`: gallery of ten project photos and three video highlights, with bilingual captions and a photo viewer.
- `gallery.js`: photo viewer, keyboard controls, and video playback management.
- `styles.css`: layout, colors, and responsive styles.
- `script.js`: mobile navigation and estimate dialog.
- `es/index.html` and `es/past-work.html`: complete Spanish pages, with shared styles, scripts, and assets.
- `tools/generate-spanish.py`: generates the Spanish pages from the English HTML and the translation dictionary in `script.js`. After changing the English pages or translations, run `python3 tools/generate-spanish.py`, then `python3 tools/check-localization.py`, and commit the generated HTML too. No build step is needed for hosting.
- `assets/`: generated homepage roof photographs and favicon. The homepage hero and storm images are illustrative.
- `assets/projects/`: real project photos and browser-ready video clips selected from the supplied `Example Work` folder. These copies are optimized and the supplied originals are intact. Video highlights are silent and do not autoplay.

## Hosting

This is a buildless static site configured for Vercel. The repository root is the site root, with no installation or build step required. The Free Estimate buttons use telephone contact; an online submission form would need a real delivery destination and service.

English URLs are `/` and `/past-work.html`; Spanish URLs are `/es/` and `/es/past-work.html`. Each page has its own canonical URL and reciprocal `en`, `es`, and `x-default` alternate links. The generator and checks are excluded from Vercel uploads.

The published testimonial section contains the two customer reviews supplied by the owner. The supplied California licensing and inspection guarantee copy is retained. The original approved hero image is retained.

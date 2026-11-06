# Talamantes Roofing

This is a static HTML website with no build step or dependency installation. Use a local server to preview all page and language links.

For a local server, run `python3 -m http.server 8000 --bind 127.0.0.1` from this folder, then open http://127.0.0.1:8000.

## Included

- Responsive desktop, tablet, and mobile layouts based on the approved mockup.
- All eight services, followed by Areas Served and then the benefits section.
- Dedicated roof replacement, roof repair, flat roofing, and commercial roofing pages in both languages, linked from the matching homepage cards. Each includes relevant project photos, a service overview, process, FAQs, related services, and estimate links.
- Phone links for 818-395-8754.
- Link previews use Open Graph and large-image Twitter/X metadata in the initial HTML on all twelve pages, with localized titles, descriptions, and the approved homepage roof image at an absolute public HTTPS URL.
- Free Estimate buttons that open an accessible contact dialog. They do not submit data; the next step is a call.
- Mobile navigation, keyboard support, reduced-motion support, and locally stored images.
- Top and bottom language links connect complete English and Spanish pages. Spanish content, metadata, navigation, testimonials, accessibility labels, and gallery captions are present in the HTML, including when JavaScript is disabled. Each URL always serves its own language, independently of browser settings or past preferences.

## Files

- `index.html`: page content and icon definitions.
- `past-work.html`: gallery of ten project photos and three video highlights, with bilingual captions and a photo viewer.
- `gallery.js`: photo viewer, keyboard controls, and video playback management.
- `styles.css`: layout, colors, and responsive styles.
- `script.js`: mobile navigation and estimate dialog.
- `sitemap.xml`: all twelve canonical English and Spanish page URLs with reciprocal language alternates.
- `robots.txt`: allows crawling and points search engines to the sitemap.
- `es/index.html` and `es/past-work.html`: complete Spanish pages, with shared styles, scripts, and assets.
- `roof-replacement.html`, `roof-repair.html`, `flat-roofing.html`, `commercial-roofing.html`: English service pages, with matching files in `es/`.
- `tools/services.json` and `tools/generate-services.py`: bilingual service content and its static-page generator. Run `python3 tools/generate-services.py`, then the Spanish generator and localization checks after changing service content or shared page chrome.
- `tools/share_metadata.py`: refreshes sharing metadata from each page's title, description, canonical URL, and language. Run it after editing homepage/gallery metadata. The service and Spanish generators also use this helper automatically.
- `tools/generate-spanish.py`: generates the Spanish pages from the English HTML and the translation dictionary in `script.js`. After changing the English pages or translations, run `python3 tools/generate-spanish.py`, then `python3 tools/check-localization.py`, and commit the generated HTML too. No build step is needed for hosting.
- `assets/`: generated homepage roof photographs and favicon. The homepage hero and storm images are illustrative.
- `assets/projects/`: real project photos and browser-ready video clips selected from the supplied `Example Work` folder. These copies are optimized and the supplied originals are intact. Video highlights are silent and do not autoplay.
- `assets/services/roof-repair-detail-illustration.jpg`: generated repair-detail illustration, visibly labeled as illustrative on the repair page. All supporting service-page project photos are from the supplied work; they are not presented as before-and-after pairs.

## Hosting

This is a buildless static site configured for Vercel. The repository root is the site root, with no installation or build step required. The Free Estimate buttons use telephone contact; an online submission form would need a real delivery destination and service.

English URLs are `/`, `/past-work.html`, and the four service URLs listed above; Spanish equivalents are under `/es/`. Each page has its own canonical URL and reciprocal `en`, `es`, and `x-default` alternate links. The generator and checks are excluded from Vercel uploads.

For Google Search Console, use the URL-prefix property `https://talamantes-roofing.vercel.app/`, verify ownership with the HTML file or tag supplied by Google, and submit `sitemap.xml`. Retain the verification file or tag in future deployments. Search Console verification and sitemap submission require the managing Google account; publishing a sitemap alone does not confirm submission or indexing.

The published testimonial section contains the two customer reviews supplied by the owner. The supplied California licensing and inspection guarantee copy is retained. The original approved hero image is retained.

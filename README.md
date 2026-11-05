# Talamantes Roofing

Open `index.html` in a modern browser. The website works directly from the folder: no build step, installation, account, or internet connection is required.

For a local server, run `python3 -m http.server 8000 --bind 127.0.0.1` from this folder, then open http://127.0.0.1:8000.

## Included

- Responsive desktop, tablet, and mobile layouts based on the approved mockup.
- All eight services, followed by Areas Served and then the benefits section.
- Phone links for 818-395-8754.
- Free Estimate buttons that open an accessible contact dialog. They do not submit data; the next step is a call.
- Mobile navigation, keyboard support, reduced-motion support, and locally stored images.
- Top and bottom language buttons switch the complete page between English and Spanish, including navigation, testimonials, the estimate dialog, accessibility labels, and page metadata. The browser remembers the selected language when storage is available. Translations are bundled locally in `script.js`; no external service is used.

## Files

- `index.html`: page content and icon definitions.
- `past-work.html`: gallery of ten project photos and three video highlights, with bilingual captions and a photo viewer.
- `gallery.js`: photo viewer, keyboard controls, and video playback management.
- `styles.css`: layout, colors, and responsive styles.
- `script.js`: mobile navigation and estimate dialog.
- `assets/`: generated homepage roof photographs and favicon. The homepage hero and storm images are illustrative.
- `assets/projects/`: real project photos and browser-ready video clips selected from the supplied `Example Work` folder. These copies are optimized and the supplied originals are intact. Video highlights are silent and do not autoplay.

## Hosting

This is a buildless static site configured for Vercel. The repository root is the site root, with no installation or build step required. The Free Estimate buttons use telephone contact; an online submission form would need a real delivery destination and service.

The published testimonial section contains the two customer reviews supplied by the owner. The supplied California licensing and inspection guarantee copy is retained. The original approved hero image is retained.

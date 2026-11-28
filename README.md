# Brandon Candela — financial crime portfolio

Live website: https://brandoncandela.github.io/

Adapted from [itsyujay/apple-style-portfolio](https://github.com/itsyujay/apple-style-portfolio) (MIT). Original license is retained at `theme/LICENSE`. Uses the template's Astro, React, Inter typography and Three.js/GSAP hero, personalized with Brandon's existing portfolio content.

## Edit and build

Requires Node 20 or newer.

1. `cd theme && npm ci && cd ..`
2. Edit `theme/src/components/Hero.astro`, `theme/src/content/portfolio.html`, or `theme/src/styles/portfolio.css`.
3. `node scripts/build-site.mjs`
4. Preview the repository root with `python3 -m http.server 4321`.
5. Commit the source plus generated `index.html` and `_astro/` assets. GitHub Pages serves the root of `main`.
6. Technical case studies live in `scripts/build_case_studies.py`. Edit the data there, then run `python3 scripts/build_case_studies.py` to regenerate `case-studies/`.
7. Responsive images: after adding or replacing a photo or screenshot, run `node scripts/optimize-images.mjs` (needs `theme/node_modules`, which includes `sharp`). It writes AVIF, WebP and JPEG copies at fixed widths to `assets/img/` and never upscales. Pages reference them with `<picture>`, `srcset` and `sizes`. `assets/og-image.jpg` stays a plain JPEG for social previews.

The original `assets/site.css` remains available for the existing articles. Static output includes `.nojekyll` so GitHub Pages serves Astro's underscore-prefixed assets. Project demos remain separate repositories with their existing URLs.

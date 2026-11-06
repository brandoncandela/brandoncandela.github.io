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

The original `assets/site.css` remains available for the existing articles. Static output includes `.nojekyll` so GitHub Pages serves Astro's underscore-prefixed assets. Project demos remain separate repositories with their existing URLs.

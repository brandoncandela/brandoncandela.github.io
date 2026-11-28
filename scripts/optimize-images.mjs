// Make responsive AVIF, WebP and JPEG copies of the site's photos and screenshots.
//
// Run from the repository root after `cd theme && npm ci`:
//   node scripts/optimize-images.mjs
//
// Sources stay where they are (assets/projects/*.jpg, assets/brandon-portrait*.jpg,
// assets/wynwood-*.jpg). Output goes to assets/img/<name>-<width>.{avif,webp,jpg}.
// A width larger than the source is skipped, so nothing is ever upscaled.
// The script is deterministic: running it twice produces the same files.
import { createRequire } from "node:module";
import { mkdirSync, readdirSync, statSync } from "node:fs";
import { basename, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const require = createRequire(join(root, "theme/package.json"));
const sharp = require("sharp");

const out = join(root, "assets/img");
mkdirSync(out, { recursive: true });

const projectDir = join(root, "assets/projects");
const jobs = [
  // Project screenshots. Flagship cards render up to 590 CSS px wide, so 1440 covers 2x screens.
  ...readdirSync(projectDir)
    .filter((f) => f.endsWith(".jpg") && !f.includes("poster"))
    .map((f) => ({ src: join(projectDir, f), widths: [480, 720, 1440] })),
  // Hero portrait renders at 120 to 136 CSS px.
  { src: join(root, "assets/brandon-portrait-square.jpg"), widths: [144, 288] },
  { src: join(root, "assets/brandon-portrait.jpg"), widths: [220, 440] },
  // Community photos render up to 670 CSS px (group photo) and 395 CSS px (patio photo).
  { src: join(root, "assets/wynwood-tech-community.jpg"), widths: [675, 1024, 1400] },
  { src: join(root, "assets/wynwood-networking-conversations.jpg"), widths: [400, 675] },
];

let written = 0;
let bytes = 0;
for (const { src, widths } of jobs) {
  const name = basename(src, ".jpg");
  const { width: sourceWidth } = await sharp(src).metadata();
  for (const w of widths.filter((w) => w <= sourceWidth)) {
    const resized = () => sharp(src).resize({ width: w, withoutEnlargement: true });
    const targets = [
      [`${name}-${w}.avif`, resized().avif({ quality: 52, effort: 6 })],
      [`${name}-${w}.webp`, resized().webp({ quality: 76, effort: 6 })],
      [`${name}-${w}.jpg`, resized().jpeg({ quality: 80, mozjpeg: true })],
    ];
    for (const [file, pipeline] of targets) {
      await pipeline.toFile(join(out, file));
      bytes += statSync(join(out, file)).size;
      written += 1;
    }
  }
}
console.log(`Wrote ${written} files (${Math.round(bytes / 1024)} KB) to assets/img/`);

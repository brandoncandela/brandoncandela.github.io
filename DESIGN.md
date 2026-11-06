---
name: Brandon Candela Portfolio
description: A light Apple-style portfolio adapted from itsyujay/apple-style-portfolio.
colors:
  canvas: "#f5f5f7"
  canvas-deep: "#edf2fa"
  surface: "#ffffff"
  ink: "#1d1d1f"
  muted: "#55555d"
  subtle: "#61616a"
  line: "#dedee4"
  line-strong: "#b6bac4"
  signal: "#0066cc"
  signal-strong: "#005bb8"
  sphere: "#0066ff"
  evidence-soft: "#42424a"
typography:
  display:
    fontFamily: "Inter Variable, system-ui, sans-serif"
    fontSize: "clamp(2.6rem, 6vw, 4.5rem)"
    fontWeight: 750
    lineHeight: 1.1
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Inter Variable, system-ui, sans-serif"
    fontSize: "clamp(1.5rem, 2.5vw, 2.125rem)"
    fontWeight: 650
    lineHeight: 1.1
    letterSpacing: "-0.025em"
  title:
    fontFamily: "Inter Variable, system-ui, sans-serif"
    fontSize: "1.45rem"
    lineHeight: 1.3
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Inter Variable, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.7
  label:
    fontFamily: "Inter Variable, system-ui, sans-serif"
    fontSize: "13px"
rounded:
  sm: "12px"
  md: "16px"
  pill: "999px"
  circle: "50%"
spacing:
  xs: "8px"
  sm: "12px"
  md: "24px"
  lg: "32px"
  xl: "48px"
  section: "80px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.pill}"
    padding: "13px 25px"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "13px 25px"
  project-card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.md}"
  tool-pill:
    backgroundColor: "{colors.canvas-deep}"
    textColor: "{colors.muted}"
    rounded: "{rounded.pill}"
    padding: "8px 12px"
  navigation:
    backgroundColor: "rgba(245,245,247,.94)"
    textColor: "{colors.muted}"
    height: "60px"
---

# Design System: Brandon Candela Portfolio

## Overview

**Creative North Star: "The Personal Product Showcase"**

The homepage adapts the user-selected itsyujay/apple-style-portfolio template: quiet light gray canvas, white rounded panels, Inter typography and a centered personal introduction. A circular portrait and large name anchor the hero while translucent blue spheres add restrained depth around it. Real project screenshots and existing portfolio content carry the evidence.

**Key Characteristics:**
- Light surfaces and spacious composition.
- Centered portrait and name with floating blue spheres.
- Rounded white project and content panels.
- Inter typography with dark pill actions and blue text links.

**The Scope Rule.** This system governs the Astro homepage. Existing note detail pages retain their dark casebook appearance through `assets/site.css` and `assets/notes.css`; do not describe or migrate those pages as light without an explicit scope change. The effective homepage source is `theme/src/styles/portfolio.css`, including its final Apple-style overrides, plus `Hero.astro` and `Scene3D.tsx`.

## Colors

Primary: signal blue identifies links and interactive details; stronger blue supports readable links. The brighter sphere blue is decorative, rendered at 0.3 material opacity.

Neutral: canvas gray separates white content surfaces; dark ink leads, muted gray carries paragraphs, and subtle gray carries dates and tags. Border colors divide content inside panels. The evidence-soft token now supplies dark gray focus outlines rather than the former gold accent.

**The Light Surface Rule.** New homepage sections use the light canvas and white surfaces defined above; do not infer the effective palette from the earlier dark declarations in the stylesheet.

## Typography

Inter Variable is the homepage's display and body family. The name uses the display role; section headings use headline; project headings use title. Paragraph line-height is intentionally generous. The hero subtitle scales from 1.15rem to 1.9rem. At the mobile breakpoint the name scales with `clamp(2.3rem, 9vw, 3.5rem)`.

## Layout

The centered content container has a maximum width of 1152px and desktop side gutters of 24px. The hero has a 690px minimum height, an 850px content maximum, and centered actions. Project cards form two columns with 24px gaps; homepage note previews form three columns with 20px gaps. Experience, SQL, tools, community and contact retain their content-specific layouts inside light panels.

At 760px and below, project and note grids become one column, the portrait contracts from 136px to 120px, and the hero minimum height becomes 650px. Navigation wraps into stacked rows with horizontally scrollable links. Container gutters become 18px, then 14px at 420px. Existing 900px and 980px layout rules also govern intermediate content layouts.

## Elevation & Depth

White panels provide most of the separation from the gray page. Project and SQL panels use a faint ambient shadow; the portrait has a stronger soft shadow and white border. The sticky navigation uses a translucent canvas-colored surface with 18px backdrop blur.

The decorative Three.js spheres drift vertically with sine easing over 3–4.2 seconds. Animation pauses outside the viewport and when the document is hidden. Reduced motion renders a static scene and disables CSS transitions and animations. Hero content remains usable if WebGL is unavailable.

## Shapes

Content cards and most grouped panels use the medium radius. Media and contact use the small radius; actions and tool labels use pill ends. The portrait is a true circle with a 4px white border. Project screenshots fill the card top at a 16:10 aspect ratio.

## Components

Primary actions are dark filled pills; secondary actions use a transparent fill and dark outline. Both retain at least 46px height. Hover darkens the primary surface and gives the secondary a pale gray fill. Keyboard focus uses a 3px outline with a 4px offset.

Project cards place the screenshot above a padded content body, followed by links and optional native disclosures. The default body padding is 26px, reducing to 24px on mobile. Note previews use white rounded cards and a pale hover surface. Experience disclosures and SQL tabs preserve their existing functionality. Tool labels are pale blue-gray pills. Navigation uses compact text and a blue contact link. There is no homepage form input component.

## Do's and Don'ts

- Do keep Brandon's portrait, factual claims, working project links and original photographs.
- Do use the centered portrait/name hero and blue sphere treatment from the selected template.
- Do preserve visible keyboard focus and the static reduced-motion experience.
- Don't introduce template placeholder claims or testimonials.
- Don't apply this light homepage palette to the dark note detail pages implicitly.
- Don't restore the former navy, gold and serif homepage design from stale declarations or documentation.

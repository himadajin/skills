---
name: monochrome-design
description: Applies an achromatic ink-on-paper visual identity to any artifact — slides, documents, diagrams, images, HTML, or UI. Use ONLY when the user names this language explicitly, for example "monochrome-design", "monochrome", "achromatic", or "ink on paper". Never use it for design work that does not name it.
---

# Monochrome Design

## Overview

An achromatic visual identity, set as if printed with ink on white paper.
Reduce decoration to meaning. Express hierarchy and state with size, density, and line — not hue, weight extremes, or motion.
The intended register is a well-set technical document, not a corporate ad.

Apply this look to any artifact you compose: slides, documents, diagrams, images, HTML, UI, or print.

## Scope: composition and quotation

This skill governs what you **compose**: text, structure, spacing, chrome, surfaces, and any figure or component you draw yourself. The rules below apply there without exception.

It does not govern **quoted** content — things the page holds but did not author: code inside a code surface (the highlighter's theme), imported components, screenshots, photos, logos, and diagrams or charts produced elsewhere. Reproduce them as they are, inside a frame you compose. Do not recolor them to match, and do not restyle them unless the user asks.

**Hue is data, not design.** In the composition, the only hue is the seal. Inside a figure you draw, prefer line style, opacity, and direct labels; reach for hue only when the data holds more distinctions than those can carry — and then hue encodes the data, never the frame around it.

Test: *Did I draw it?* Yes → the rules apply. No → frame it, don't recolor it.

## Tokens

- Paper: `#ffffff` — background. Pure white. No dark mode or inverted palette.
- Ink: `#171717` — all text, frames, and structural marks. Ink is also the accent.
- Muted: `#f5f5f5` — inline-code fills and quiet surfaces.
- Hairline: `#ebebeb` — 1px structural rules and table borders. Decorative only (1.2:1 on paper); a control's boundary needs ink.
- Seal: `#ed6d2f` — the only chromatic token. A vermilion mark that names the compositional center, like a stamp on ink-wash paper. It carries no meaning of its own. It is a mark or a fill, never a text color (3.1:1 on paper); ink may sit on it.

Do not add blue links, green success, red error, or any other hue. If a distinction seems to need a color, use ink opacity.

**Ink opacity (three steps, no new tokens):**

| Opacity | On paper | Role |
|---|---|---|
| 35% | 2.2:1 | Non-text marks only: fading rules, prefix symbols |
| 60% | 4.7:1 | Static meta (labels, dates, captions) |
| 70% | 6.6:1 | Secondary reading text (lede, quotes, footnotes, deep headings) and interactive meta |

Text is never below 60%. Targets: 4.5:1 for text, 3:1 for marks. Do not invent a fourth step.

## Typography

- **Body and headings**: Geist, then Noto Sans JP for Japanese glyphs, then system-ui / Hiragino / Yu Gothic / Meiryo. Keep Latin first; reversing the order renders Latin in Noto.
- **Code and meta**: Geist Mono, then ui-monospace / Menlo / Consolas.
- **Weights**: 400 / 500 / 600 only. No 700, no italic; do not load them. `strong` is 600, `em` is 500.
- **Voices**: body copy and headings are sans. Meta (labels, tags, dates, language names) is mono, uppercase, one scale (~70% of body, tracking `0.10em`); its only variation is opacity, static 60% and interactive 70%. Do not set body paragraphs in mono. Do not set sans headings in all caps — uppercase is the meta voice.
- **Links**: ink with a 1px underline, always. Hover and visited do not change it.

Hierarchy is modest size + weight + attached spacing, not a large type ramp. The page title is capped at **1.5× body**; do not grow it on large viewports. Representative scale at 16px body:

| Level | Size | Note |
|---|---|---|
| h1 (title) | 24 | tracking ~`-0.02em` |
| h2 | 20 | |
| h3 | 18 | |
| h4 | 17 | |
| h5 | 16 | |
| h6 | 16 | ink 70%; anything deeper switches to the meta voice |
| body | 16 | |
| tables | 14 | |
| code | 13 | |
| meta | 11 | |

Line-height 1.65 (1.6 minimum for mixed JP/EN). Negative tracking only on large type; leave body tracking alone.

Avoid the marketing hero: oversized title + tiny mono caption + large empty space.

## Spacing

Pick block spacing from a six-step ladder. The ladder governs gaps between blocks (paragraphs, headings, sections), not padding inside a component.

| Step | Ratio | At 16px body | Role |
|---|---|---|---|
| 1 | 1 | 4px | Inside one thing (list items, title → caption) |
| 2 | 2 | 8px | Heading attached to its content |
| 3 | 4 | 16px | Block break (paragraphs, code surfaces) |
| 4 | 6 | 24px | Small topic shift |
| 5 | 8 | 32px | Large topic shift |
| 6 | 12 | 48px | Page-level break |

Headings attach to their content, **4:1 above:below** (e.g. 32/8 for a large heading, 24/8 for a medium one).
List gaps stay clearly tighter than paragraph gaps. Keep content dense and the frame generous.

## Seal

Default is no seal.
If used: one per composition, beside the thing the reader should see first (a key number, the latest item, an annotation on a figure, one word in a title).

Test: remove it. If the eye's first landing point does not change, it is ornament — move it to the center of gravity or delete it.
Never use it as a link, state, heading, or logo-side decoration. Chrome (headers, footers) is not the center of gravity.

## Surfaces and shapes

- No shadow, gradient, wave, or rounded corners (4px on inline code is the only exception).
- Hairline rules mark structure. Fills are rare.
- Symbols are typed characters, not icons. Separators, prefixes, and markers are set in the meta voice (`/`, `#`, `→`); an icon appears only where no character says the same thing.
- Code is a quotation on paper: paper fill, 1px ink frame, no radius, mono. The highlighter's colors belong to the quotation — this skill does not choose them; pick a light theme so the surface stays paper, not a dark pane.
- Inside a figure you draw, ink may mean something else: dashed strokes may mark a series or a forecast. Outside figures, do not invent extra line meanings.

## Derivation

These rules are axioms, not a catalog. For anything unlisted, ask what meaning the difference carries.

**If you cannot say that meaning in one sentence, do not make the difference. One distinction gets one signal. When unsure, pick the quietest option.**

## Applying to a medium

### Fonts

In HTML, load Geist, Geist Mono, and Noto Sans JP from Google Fonts, weights 400;500;600 only, with `display=swap`. In every other medium (slides, images, diagrams), use the fallback stacks; do not add an install step.

### CSS tokens

Map the hex values to `--background`, `--foreground`, `--muted`, `--border`, and `--seal`.
Optional `--accent` may alias ink for later tuning; do not introduce a second accent hue. White paper is the given; do not add a dark theme.

### Scaling

Treat the body's size on the current medium as 1×. Keep the ratios; replace the 16px representatives.
Slides, posters, and diagrams use the same roles and the same 1:2:4:6:8:12 spacing ladder.
On a 1280×720 slide, body is 24px and the 1.5× title cap holds (36px).

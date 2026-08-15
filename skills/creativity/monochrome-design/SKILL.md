---
name: monochrome-design
description: Applies an achromatic ink-on-paper visual identity to any artifact — slides, documents, diagrams, images, HTML, or UI. Use ONLY when the user names this language explicitly, for example "monochrome-design", "monochrome", "achromatic", or "ink on paper". Never use it for design work that does not name it.
---

# Monochrome Design

## Overview

An achromatic visual identity, set as if printed with ink on white paper.
Reduce decoration to meaning. Express hierarchy and state with size, density, and line — not hue, weight extremes, or motion.
The intended register is a well-set technical document, not a corporate ad.

Apply this look to any artifact: slides, documents, diagrams, images, HTML, UI, or print.

**Keywords**: monochrome, achromatic, ink on paper, visual identity, typography, grayscale, seal, technical document

## Brand Guidelines

### Colors

**Main colors:**

- Paper: `#ffffff` — background. Pure white. No dark mode or inverted palette.
- Ink: `#171717` — all text, frames, and structural marks. Ink is also the accent.
- Muted: `#f5f5f5` — inline-code fills and quiet surfaces
- Hairline: `#ebebeb` — 1px structural rules and table borders

**Seal (only chromatic token):**

- Seal: `#ffc799` — a vermilion mark that names the compositional center, like a stamp on ink-wash paper. It carries no meaning of its own.

Do not add blue links, green success, red error, or any other hue. If a distinction seems to need color, try ink opacity first.

**Ink opacity (three steps, no new tokens):**

| Opacity | Role |
|---|---|
| 35% | Fading marks and prefix symbols |
| 50% | Static meta (labels, dates, captions) |
| 70% | Secondary reading text (lede, quotes, footnotes, deep headings) |

Do not invent a fourth opacity. Raise opacity for accessibility if needed; do not add a new signal.

### Typography

- **Body and headings**: Geist, with Noto Sans JP for Japanese glyphs (system-ui / Hiragino / Yu Gothic / Meiryo fallback)
- **Code and meta**: Geist Mono (ui-monospace / Menlo / Consolas fallback)
- **Weights**: 400 / 500 / 600 only. Do not use 700 or italic. Do not load them.
- **Voices**: body copy is sans. Meta (labels, tags, dates, language names) is mono, uppercase, one scale (~70% of body, tracking `0.10em`). Do not set body paragraphs in mono. Do not set sans headings in all caps — uppercase is the meta voice.

Hierarchy is modest size + weight + attached spacing, not a large type ramp. Page title is capped at **1.5× body**. Heading sizes stop at five steps. Deeper levels drop to ink 70%, then switch to the meta voice. Do not grow titles on large viewports.

Representative scale at 16px body: title 24 / headings 20, 18, 17, 16 / body 16 / tables 14 / code 13 / meta 11. Line-height 1.65 (1.6 minimum for mixed JP/EN). Negative tracking only on large type (~`-0.02em` at 24px); leave body tracking alone.

Avoid the marketing hero: oversized title + tiny mono caption + large empty space.

### Spacing

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

## Features

### Voice application

- Headings and body: sans
- Meta, labels, code: mono
- Meta stays one size; difference is opacity (static 50%, interactive 70%)
- Breadcrumb separators are `/`, not `»` or `>`. Tag prefixes are the character `#`, not icons.

### Seal placement

Default is no seal.
If used: one per composition, beside the thing the reader should see first (a key number, the latest item, an annotation on a figure, one word in a title).

Test: remove it. If the eye's first landing point does not change, it is ornament — move it to the center of gravity or delete it.
Never use it as a link, state, heading, or logo-side decoration. Chrome (headers, footers) is not the center of gravity.

### Surfaces and shapes

- No shadow, gradient, wave, or rounded corners (4px on inline code is the only exception)
- Hairline rules mark structure. Fills are rare.
- Code is a quotation on paper: same paper fill, 1px ink frame, no radius,
  restrained light syntax (near-black + gray + one ink). No dark terminal panes.
- Inside figures and charts, ink may mean something else; dashed strokes may mark a series or a forecast.
  Outside figures, do not invent extra line meanings.

### Derivation

These rules are axioms, not a catalog. For anything unlisted, ask what meaning the difference carries.

**If you cannot say that meaning in one sentence, do not make the difference. One distinction gets one signal. When unsure, pick the quietest option.**

## Technical Details

### Font management

Prefer Geist and Geist Mono when available. Keep Latin-first in the sans stack (`Geist`, then `Noto Sans JP`); reversing the order renders Latin in Noto.
Fall back to system-ui / Hiragino / Yu Gothic / Meiryo for sans, and ui-monospace / Menlo / Consolas for mono.
No install step is required.

### Color application

Use the hex values above. In CSS, map them as `--background`, `--foreground`, `--muted`, `--border`, and `--cursor` (seal).
Optional `--accent` may alias ink for later tuning; do not introduce a second accent hue. White paper is the given; do not add a dark theme.

### Scaling

Treat the body's size on the current medium as 1×. Keep the ratios; replace the 16px representatives.
lides,　posters, and diagrams use the same roles and the same 1:2:4:6:8:12 spacing ladder.

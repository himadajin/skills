---
name: plain-design
description: Applies a plain, printed-document look — black ink on white paper with sparing, meaningful color — to any artifact, such as slides, documents, diagrams, images, HTML, or UI. Use ONLY when the user names this style explicitly, for example "plain-design", "plain design", or "like a printed document". Never use it for design work that does not name it.
---

# Plain Design

Set every artifact as if it were a well-made document printed on white paper.
Ink carries the structure; color appears only where it means something.
Avoid the look of generated templates: decoration that carries no meaning is removed, not toned down.

## Scope

These rules govern what you compose: text, structure, spacing, surfaces, and any figure or component you draw.
They do not govern what you quote: screenshots, photos, logos, imported components, highlighted code, or figures made elsewhere.
Test: did I draw it? If not, frame it and leave its colors alone.
Set code surfaces in a light highlighting theme so the page stays paper.

## Paper and ink

- Paper `#ffffff` is the only background. No dark mode or inverted sections.
- Ink `#171717` for text, frames, and structural marks.
- Hairline `#ebebeb` for 1px rules and table borders; Muted `#f5f5f5` for inline code and rare quiet surfaces.
- Lighter text is ink at reduced opacity, never below 60%.

## Typography

No typeface is prescribed; use what the medium offers.

- Two voices: sans for body and headings; monospace for code and meta (labels, dates, tags).
- Weights 400, 500, and 600 only. No bold 700, no italic.
- Hierarchy is modest: the page title is at most 1.5× body, and smaller levels step down gently.
- Line height 1.65.
- Use normal letter case. Do not set text in all caps for decoration.

## Spacing

Treat the body size on the current medium as 1× and keep every ratio when scaling.
Gaps between blocks follow 1:2:4:6:8:12 of a base unit that is ¼ of the body size (4px at 16px).
A heading sits closer to its content than to what precedes it, 4:1 above to below.
Keep content dense and the frame generous.

## Color

Color has two roles only:

- **Attention**: guide the eye to what should be seen first, or make one thing memorable.
- **Action**: mark what can be operated — links and buttons.

Each hue has exactly one meaning, stated in one sentence and kept consistent across the artifact.
There is no fixed palette or hue count; choose values that fit the context, and keep colored text at 4.5:1 or more against paper.

- Never use color to tell kinds apart (categories, tags, node types, sections).
- Attention test: remove the color. If the eye's first landing point does not change, it was ornament; delete it.
- State is said with words and characters ("Error:", `×`). Only errors and destructive actions may take a color, and that hue then means danger and nothing else.
- In a figure you draw, color may highlight one series against ink, or encode quantity as shades of one hue.
  Separate series by line style, shape, or direct labels; use per-series hues only when those cannot carry the distinctions, and keep those hues inside the figure.

## Links and buttons

Links are set in the action color with a solid underline, so they survive grayscale print.
If the artifact has no action color, links are ink with a solid underline.
Buttons use the same action color. No dashed or dotted underlines.

## Shapes

- No shadows, gradients, or rounded corners. A small radius on inline code is the only exception.
- Hairline rules mark structure; fills are rare.
- Symbols are typed characters (`→`, `/`, `#`), not icons or emoji. Use an icon only where no character says the same thing.
- No marketing hero: no oversized title over a tiny caption and wide empty space.

## Derivation

These rules are axioms, not a catalog. For anything unlisted, ask what meaning the difference carries.
If you cannot say that meaning in one sentence, do not make the difference. When unsure, pick the quietest option.

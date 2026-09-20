# Academic Figure Style

## Typography

- Sans-serif for labels (Helvetica/Arial-like, or the paper's font); math via LaTeX syntax
  (`$p_T$`, `$\theta$`) so it typesets in the paper's font.
- Final printed size >= 6-7 pt (aim 8 pt); test by scaling to the column width.
- Hierarchy: one size for node text, one slightly smaller for edge labels/annotations,
  one bolder for group titles. No more than three sizes.
- Preserve notation exactly as defined in the paper (`\hat{\theta}` vs `\theta`, `\mathcal{L}`).
  Do not re-letter symbols for layout reasons.

## Color

- Grayscale-safe by default: verify by mentally (or actually) desaturating. Distinguish by
  fill lightness + border/line style + shape + label.
- Color for semantic grouping only: data vs simulation, signal vs background, training vs
  inference, deterministic vs stochastic, detector subsystems, software layers.
- Colorblind-safe palette, e.g. Okabe-Ito: `#000000 #E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7`
  (avoid red/green as the only contrast). Use <= 4 hues per figure.
- Keep the same color for the same concept across every figure in a paper.

## Line and shape vocabulary (suggested, declare in a legend when used)

| Meaning | Encoding |
|---|---|
| process / computation | rectangle, light fill |
| data / artifact | rounded rectangle or parallelogram |
| storage | cylinder |
| decision | diamond |
| observed variable | shaded circle |
| latent variable | unshaded circle |
| parameter / hyperparameter | small square or bare symbol |
| learned component | double border or bold outline |
| training-only | dashed border |
| inference-only | dotted border or separate group |
| simulation | dashed outline; data solid |
| control flow | dashed arrow; data flow solid |

## Column and page geometry

| Target | Width (typical, verify against the venue template) |
|---|---|
| Single column (REVTeX/APS) | ~8.6 cm (3.4 in), from the APS Reviews of Modern Physics style guide; the REVTeX 4.2 guide states no width and only says page-spanning figures use `figure*` |
| Double column span (REVTeX/APS) | ~17.8 cm (7 in), common default, not stated in the REVTeX 4.2 guide |
| JHEP (`jheppub`, a4paper) | text width 15.5 cm (~74% of the paper width); a float wider than 60% of the text width is centered on the page |
| NeurIPS 2026 | text width 5.5 in (13.97 cm), single column |
| ICML 2026 | two columns; overall text width 6.75 in (17.1 cm), 0.25 in between columns, so each column is 3.25 in (8.26 cm); left margin 0.75 in |
| ICLR | single column, text width ~5.5 in in recent kits (not re-checked) |
| Beamer 16:9 | ~ full slide; text >= 14-18 pt |
| Poster | text >= 24 pt for labels |

Checked 2026-09-21 against: the ICML 2026 example paper (widths above, plus figure lines at least 0.5 pt thick, no text on a gray background, and Type-1 fonts only - avoid Type-3 fonts from exported figures), the NeurIPS 2026 formatting instructions, the JHEP `jheppub` documentation, and the APS RMP style guide. Re-check each year and for every journal. These are common defaults, not guarantees: read the venue's author kit. Design at final size;
avoid scaling a large figure down until the text is unreadable. Prefer vector (PDF/SVG) output.

## Panels and multi-figure consistency

- Panels `(a) (b) (c)` labeled consistently top-left; each panel one message; shared node names.
- One `figure_style` block for the whole paper:

```yaml
figure_style:
  orientation: left-to-right     # or top-to-bottom
  typography: academic           # sans labels, LaTeX math
  color_policy: grayscale-safe
  edge_style: semantic           # style encodes meaning; legend when >1
  math_format: latex
  abstraction: paper             # overview | paper | presentation | technical | educational
  output: svg                    # or pdf / tikz
```

- Keep a symbol table (figure label <-> paper symbol) to guarantee the figure matches the text.

## Equations inside diagrams

Put short equations on nodes/edges only when they are the point (`$p(\theta \mid x)$`). Long
equations belong in the text; reference them ("Eq. 3") only if the paper's numbering is known -
do not invent numbers.

## Talks, posters, theses

- Talk: 3-7 nodes, one idea per slide, build progressively (reveal stages), large labels.
- Poster: one dominant flow, minimal prose, high contrast.
- Thesis: may use paper level in the body and the detailed technical version in an appendix.
- Beamer: TikZ overlays (`\onslide<2->`) or Mermaid/SVG exported per step.

## Export

Prefer vector: SVG -> PDF (Inkscape/`rsvg-convert`), Graphviz `dot -Tsvg|pdf`, Mermaid
`mmdc -o fig.svg`, TikZ compile natively (or `standalone` class for a cropped PDF). State any
external tool needed; do not assume it is installed.

## Final readability check

Grayscale test; column-width test; can a reader in the field name every arrow's meaning without
the caption? Is anything in the figure absent from the text (or vice versa)?

# Figures and Tables

Publication figures are a different design problem than analysis plots made for
yourself or a collaboration meeting. This assumes plots already exist (e.g. from
ROOT/matplotlib work under `hep-analysis`) and focuses on turning them into
publication-quality figures with correct, complete captions.

## Table of contents
- [What makes a figure publication-ready](#what-makes-a-figure-publication-ready)
- [Figure types and when to use them](#figure-types-and-when-to-use-them)
- [Caption writing](#caption-writing)
- [Tables](#tables)
- [Color and accessibility](#color-and-accessibility)
- [File formats and resolution](#file-formats-and-resolution)

## What makes a figure publication-ready

- **One clear message per figure.** If a figure needs a full paragraph to
  explain what to look at, either split it or redesign it (remove clutter,
  add an annotation/arrow, reorder panels).
- **Self-contained with the caption.** A reader flipping straight to the
  figures should understand the axes, what's plotted, and the headline
  takeaway without reading the main text.
- **Axis labels include units**, and are large enough to read at the
  journal's printed column width (test at ~8.6 cm wide for a single-column
  figure) — not just legible on a laptop screen.
- **Legends inside the plot area** (or a compact key in the caption) rather
  than a separate wide legend that wastes horizontal space in a two-column
  layout.
- **Uncertainty bands/error bars are present** on any data points or curves
  where they matter to the claim, and their meaning (stat only vs. stat+syst)
  is stated in the caption.

## Figure types and when to use them

| Goal | Good choice |
|---|---|
| Distribution comparison (data vs. MC/background) | Stacked histogram with data points + ratio panel below |
| Result vs. previous measurements | Horizontal "measurement comparison" plot (points with error bars, one row per measurement) |
| Exclusion/discovery reach | 2D exclusion contour, or Brazil-band limit plot |
| Correlation between two quantities | 2D scatter or profile histogram, or a correlation-coefficient table for many variables |
| Cutflow / selection efficiency | Table, not a figure, unless efficiency vs. a continuous variable is the point |
| Systematic breakdown | Stacked or grouped bar chart, or a table if there are more than ~6 sources |

Avoid 3D plots for print publications — they rarely survive being flattened to
a static page and are hard to read precisely; a 2D projection or a pair of 2D
slices usually communicates more.

## Caption writing

A caption typically has three parts, in order:
1. **What is shown** — plot type, what's on each axis, what the data source is.
2. **How it was made**, briefly, if not obvious (selection applied, binning
   choice, what error bars represent).
3. **What to take away** — the one-sentence interpretation, especially for the
   paper's headline figure.

Example:
> Figure 2: Reconstructed dijet invariant mass distribution after the full
> event selection (points, with statistical uncertainties), compared to the
> background-only fit (solid line) and the signal-plus-background fit (dashed
> line). The lower panel shows the fit residuals in units of the statistical
> uncertainty. The excess near 750 GeV corresponds to a local significance of
> 2.1σ.

Keep captions self-contained but not redundant with the main text — the main
text can discuss implications at length; the caption states facts about the
figure itself.

## Tables

- Use tables (not prose) for anything with more than ~4 numeric values a
  reader might want to look up individually — systematic uncertainty
  breakdowns, cutflows, results across multiple channels/bins.
- One consistent number of significant figures/decimal places per column.
- State units in the column header, not repeated in every cell
  (`p_T [GeV]`, not `p_T = 42 GeV`, `p_T = 51 GeV`, ...).
- For cutflow tables, include both absolute yield and relative/cumulative
  efficiency — either alone forces the reader to do arithmetic.
- `booktabs` (`\toprule`/`\midrule`/`\bottomrule`) rather than full grid
  lines is the near-universal house style for physics journals; avoid
  vertical rules.

## Color and accessibility

- Use colorblind-safe palettes (e.g. Okabe-Ito, or ROOT's `kViridis`/
  `kCividis`) rather than default red/green distinctions.
- Ensure figures remain interpretable in grayscale — many readers print or
  view PDFs without color; use distinct line styles (solid/dashed/dotted) in
  addition to color for curves.
- Do not rely on color alone to distinguish more than ~4-5 categories; add
  markers or hatching.

## File formats and resolution

- Vector formats (PDF, EPS) for anything that's lines/text/histograms — they
  stay sharp at any zoom and keep file size small.
- Raster (PNG at ≥300 dpi) only for genuinely raster content (detector event
  displays, photographs, heatmaps with very many points where vector output
  would bloat file size).
- Avoid re-exporting a raster screenshot of a vector plot — regenerate from
  source (ROOT macro / matplotlib script) at the target format instead.

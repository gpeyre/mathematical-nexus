# Mathematical Nexus Authoring Method

This document defines the editorial and technical philosophy for all Python notebooks in this repository.  
Its purpose is to preserve consistency over time and ensure each new notebook remains educational, standalone, and visually strong.

## Core Objective

Convert each topic from `matlab/<topic>/` into a standalone notebook:
- target path: `python/<topic>/<topic>.ipynb`
- no runtime dependency on MATLAB helper code
- equivalent conceptual content, but not a line-by-line translation

The notebook should teach the idea clearly, not merely reproduce code.

## Pedagogical Principles

- Start with a **detailed exposition** of what is at stake:
  - why the problem matters
  - what mathematical object is studied
  - what the notebook will demonstrate
- Split content into many small, readable pedagogical blocks.
- Before **every code cell**, add a markdown explanation:
  - what is implemented
  - key formula(s) defining the object/algorithm
  - interpretation of expected output
- Use equations generously (LaTeX in markdown).
- Avoid section numbering in notebook headings.
- Do not mention the legacy source or “reimplementation from MATLAB” inside notebooks.
- Split long implementations into multiple short code cells with clear substeps:
  - one substep = one conceptual action (data/model setup, solver step, diagnostics, plotting)
  - each substep cell must be preceded by a markdown cell explaining the math and intent
  - avoid large monolithic cells that mix model definition, optimization loop, and final visualization in one block
- Spread figures throughout the notebook to support each numerical step:
  - after a meaningful computation cell, include a nearby result/diagnostic visualization cell
  - do not postpone most or all plots to a single final “all results” section
  - prefer progressive visual checkpoints (intermediate + final) so readers can verify each stage of the method

## Notebook Content Requirements

- Each notebook must be standalone and executable with Python scientific stack.
- Preferred libraries:
  - `numpy`
  - `matplotlib`
  - `scipy` when needed
  - `ipywidgets` for interactivity when meaningful
- Include interactivity when it helps understanding (parameter sliders, time index, model scale, etc.).
- Interactive cell handling recommendation:
  - keep widget-heavy animation/playback logic in dedicated code cells tagged `interactive`
  - provide a separate non-interactive static snapshot/render cell for automated execution contexts
  - avoid duplicate displays in interactive mode by guarding static render cells with a flag (for example `STATIC_SNAPSHOT = False` by default)
  - ensure interactive controls include a slider and, when temporal evolution is shown, a play/stop control
- Use clear and visually informative plots.
- When relevant, avoid relying on a single rendered image only; prefer a **series of images** or multi-panel figures to show:
  - effect of parameter variations
  - effect of input changes
  - temporal/iterative evolution of the method
  - side-by-side method comparisons
- End with brief takeaways and, when relevant, a bibliography section:
  - main papers
  - textbooks
  - foundational references

## Repository-Level Presentation

- Root `README.md` should index notebooks clearly.
- For each notebook:
  - add direct link
  - add Open in Colab badge
  - add a visual snippet image
  - add a concise one-sentence description in the gallery/topic entry
- README update constraints (must hold whenever README is modified):
  - keep snippet, description, notebook link, and Colab badge consistent for each entry
  - preserve gallery formatting consistency (thumbnail size/style and table structure)
  - ensure new or renamed notebooks are reflected immediately
  - keep snippet scale/readability balanced and consistent with existing gallery presentation choices
- Snippet policy:
  - square format
  - extracted from representative notebook rendering
  - chosen to be the most illustrative view of the topic

## Unified Catalog Presentation (Root `index.html`)

The repository now exposes a **single searchable catalog** at root:
- entry point: `index.html`
- content sources:
  - notebooks under `python/` (type = `notebook`)
  - media entries under `vignettes/` (type = `vignette`)

### Naming and Structure

- Use `vignettes/` as the canonical folder name for rendered media collection.
- Do not re-introduce a parallel `rendered/` folder.
- Keep legacy source list for vignettes in `vignettes/mydata.js` (unless a future migration replaces it globally).

### Catalog Database Requirements

- Maintain a root catalog file: `database.xlsx` with exactly these columns:
  - `title`
  - `content`
  - `filename`
  - `type`
  - `related_notebook` (optional; blank unless a vignette has a direct match)
- One row = one searchable entry.
- Include both notebooks and vignettes in the same table.
- Give every vignette a short, descriptive title rather than exposing a terse archival filename or unexplained acronym.
- Order notebook and vignette rows together by the first non-trivial word of the title (ignoring articles and short linking words such as `the`, `a`, `of`, and `for`).
- `type` values must be normalized and constrained to:
  - `notebook`
  - `vignette`
- Vignette rows may define an optional `related_notebook` path only when the
  conceptual match is direct and unambiguous. The relation must be generated
  from the catalog script and must point to an existing notebook.

### Generation Workflow

- Regenerate catalog data programmatically (single source of truth), using:
  - `scripts/build_catalog_database.py`
- Generated artifacts at root:
  - `database.xlsx` (human-editable table view)
  - `database.json` (structured export)
  - `database.js` (browser-ready payload for `index.html`)
- When notebooks or vignettes are added/renamed/removed, re-run generation so catalog stays in sync.

### Root Search Browser Requirements

- `index.html` must:
  - load catalog entries from generated database payload
  - provide a text search box across title/content/filename
  - provide a compact clear-search control at the right edge of the text input
  - provide page-size selector (`20`, `50`, `100`, `200`; default `100`)
  - provide a type filter toggle:
    - all types
    - notebook only
    - vignette only
  - paginate results with previous/next navigation
  - display media previews for vignettes and direct links for notebooks
  - omit archival source filenames from vignette cards
  - append a `code` link to a vignette's external links when its catalog row
    contains a valid `related_notebook`
- The UI must remain responsive for large catalogs (hundreds of entries).
- If search/filter returns no result, display a clear empty-state message.

## Figure Output Hygiene (No Root Artifacts)

- Never write generated figures to repository root (e.g. `./figure.png` from top-level execution).
- Figure outputs must use one of these locations:
  - notebook-local folder: `python/<topic>/` (for persistent assets such as `snippet.png`)
  - notebook-local temp/output subfolder: `python/<topic>/_tmp/` or `python/<topic>/outputs/`
  - system temporary directory for transient validation artifacts (for example via `tempfile`)
- During batch execution from repository root, all `savefig` paths must still resolve away from `./`.
- If a figure is only diagnostic/intermediate:
  - prefer temporary output (`_tmp/` or system temp)
  - do not leave it in repository root
- If a figure is intended for README/gallery:
  - save it explicitly as `python/<topic>/snippet.png`
  - keep it square and representative

## Execution Validation Protocol (30s Rule)

### How to run notebooks so figures are embedded in the `.ipynb`

- Use in-place execution with nbconvert:
  - `python3 -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=30 python/<topic>/<topic>.ipynb`
- Why this embeds figures:
  - `--execute` runs cells and captures outputs
  - `--to notebook --inplace` writes captured outputs back into the same notebook file
  - matplotlib figures shown by the cell (for example with `plt.show()`) are stored as notebook outputs
- Validation after execution:
  - open notebook JSON or view in Jupyter and confirm code cells contain `display_data` / `image/png` outputs
  - confirm `python/<topic>/snippet.png` exists when snippet generation is part of the notebook

### How to tag interactive cells to avoid blocking automated runs

- Any widget/event-loop/playback cell must be tagged `interactive` in notebook cell metadata.
- Recommended metadata format:
  - `{"tags": ["interactive"]}`
- In JupyterLab:
  - select cell -> Property Inspector -> Tags -> add `interactive`
- In batch validation, skip these cells with:
  - `--TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags='["interactive"]'`
- Interactive design rule:
  - keep a separate static fallback cell (not tagged) that renders representative figures for stored outputs
  - interactive cell should enrich exploration, never be required for core computation correctness

- Every notebook must be execution-tested before being considered valid.
- Validation command/process:
  - execute notebook with `nbclient`/`nbconvert` and enforce a **30-second max runtime per code cell**
  - automated runs must skip UI-only cells tagged `interactive`
  - static fallback render cells must still execute, so exported notebooks keep figures
- Interactive handling constraints during validation:
  - interactive widget cells must be isolated and tagged `interactive`
  - they must not be required for core computations
  - playback widgets (slider + play/stop) should be optional for batch execution
- If a cell exceeds 30s or blocks:
  - check first for blocking UI (`plt.show()` loops, widget waits, event loops)
  - move UI logic to a tagged `interactive` cell and keep a non-interactive fallback cell
  - reduce computational load (grid size, number of particles/samples, iteration count, frame count)
  - prefer vectorization or lighter diagnostic subsets for default execution
  - keep an optional “high-resolution” parameter path only for manual exploration
- After execution validation:
  - verify no new `*.png` (or other figure dumps) were created in repository root
  - if root artifacts exist, move/remove them and fix notebook save paths before marking validation complete
- A notebook passes only if:
  - no non-interactive cell exceeds 30s in validation
  - no execution error occurs
  - outputs/figures are stored in the notebook after execution

## Quality Checklist (to run before considering a notebook done)

- [ ] Notebook has an in-depth opening exposition.
- [ ] No mention of legacy/original source inside notebook.
- [ ] Every code cell has preceding explanatory markdown with equations where relevant.
- [ ] Long implementations are split into clear substep cells (no monolithic all-in-one code blocks).
- [ ] Figures are distributed across the notebook as local checkpoints, not deferred to the end only.
- [ ] No numbered section headings.
- [ ] Notebook is standalone (no MATLAB/toolbox dependency).
- [ ] Visualizations are clear and pedagogically useful.
- [ ] When meaningful, figures include multi-state or comparative rendering (not only one isolated image).
- [ ] Interactive controls included when beneficial.
- [ ] Interactive cells are non-blocking for automated execution (tagged strategy + static fallback render).
- [ ] Bibliographical resources included when relevant.
- [ ] README entry + Colab badge + square snippet present.
- [ ] README snippet/description/gallery constraints are respected.
- [ ] Notebook parses correctly as valid `.ipynb`.
- [ ] In-place execution (`nbconvert --execute --inplace`) stores rendered figure outputs in the notebook.
- [ ] Figure outputs are stored in notebook-local or temp directories (never repository root).
- [ ] Root unified catalog (`index.html`) correctly lists and searches notebooks + vignettes.
- [ ] `database.xlsx` schema (`title`, `content`, `filename`, `type`) is respected.
- [ ] Catalog artifacts regenerated after content updates (`database.xlsx/json/js`).

## Tone and Style Expectations

- Explain with rigor but keep readability high.
- Favor conceptual clarity over compactness.
- Make each notebook feel like a mini-course page: narrative, math, code, experiments, interpretation.

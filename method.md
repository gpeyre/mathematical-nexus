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
- [ ] Figure outputs are stored in notebook-local or temp directories (never repository root).

## Tone and Style Expectations

- Explain with rigor but keep readability high.
- Favor conceptual clarity over compactness.
- Make each notebook feel like a mini-course page: narrative, math, code, experiments, interpretation.

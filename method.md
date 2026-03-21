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
- Snippet policy:
  - square format
  - extracted from representative notebook rendering
  - chosen to be the most illustrative view of the topic

## Quality Checklist (to run before considering a notebook done)

- [ ] Notebook has an in-depth opening exposition.
- [ ] No mention of legacy/original source inside notebook.
- [ ] Every code cell has preceding explanatory markdown with equations where relevant.
- [ ] No numbered section headings.
- [ ] Notebook is standalone (no MATLAB/toolbox dependency).
- [ ] Visualizations are clear and pedagogically useful.
- [ ] When meaningful, figures include multi-state or comparative rendering (not only one isolated image).
- [ ] Interactive controls included when beneficial.
- [ ] Bibliographical resources included when relevant.
- [ ] README entry + Colab badge + square snippet present.
- [ ] README snippet/description/gallery constraints are respected.
- [ ] Notebook parses correctly as valid `.ipynb`.

## Tone and Style Expectations

- Explain with rigor but keep readability high.
- Favor conceptual clarity over compactness.
- Make each notebook feel like a mini-course page: narrative, math, code, experiments, interpretation.

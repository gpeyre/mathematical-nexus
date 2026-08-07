# Correction Log

## AdaBoost: Weak Learners, Strong Decisions

Date: 2026-07-13

- Expanded the opening exposition to connect weighted weak-learner selection, the exponential objective, adaptive reweighting, margins, and nonlinear decision geometry.
- Replaced the overloaded optimization display with distinct pedagogical checkpoints: exponential-loss decay, sample-weight concentration, boundary evolution, and the final margin distribution.
- Reconstructed the partial ensemble $F_t$ at every boosting round, making the evolving decision boundary visible rather than showing only the terminal classifier.
- Added a final boundary plot with training accuracy and signed margins $y_iF_T(x_i)$, so the reader can distinguish residual errors from confident classifications.
- Added an optional `interactive`-tagged round slider. It is isolated from the numerical path and therefore remains safe to skip in automated execution.
- Corrected the plotting layout bug that created an unused figure with empty axes.
- Removed an unused plotting import.
- Updated the bibliography with a directly relevant regularization perspective on boosting.

### Execution Check

The notebook was executed in place with a 30-second timeout per non-interactive cell, using `ExecutePreprocessor.skip_cells_with_tag=interactive` so the widget remains in the saved notebook while UI code is not run during batch validation.

- Execution completed without errors.
- Six static PNG figure outputs are embedded in the notebook.
- The interactive cell is preserved and tagged `interactive`.
- Longest non-interactive cell: 0.78 seconds.
- No generated image or video artifact was written to the repository root.

## Batch 5 Notebook-Schema Repair

The fifth fresh execution batch covers the 20 notebooks from `hump-algebra` through `kernel-approx-1d` in alphabetical order.

- Removed the invalid top-level `nbformat_minus` field from `python/interior-points/interior-points.ipynb` without changing its mathematical narrative or numerical cells.
- Re-executed the repaired notebook in place with the 30-second cell timeout and interactive cells skipped.
- Revalidated all 20 notebooks for notebook-schema compliance, error-free non-interactive outputs, preserved interactive tags, and embedded static PNG figures.
- All 20 passed; the longest recorded non-interactive cell was 2.55 seconds (`interior-points`).

## Batch 6 Embedded-Figure Repairs

The sixth fresh execution batch covers the 20 notebooks from `kernel-pca` through `mean-curvature-flow` in alphabetical order.

- Restored inline static output in 15 notebooks that saved and closed Matplotlib figures without displaying them, while preserving their existing asset exports.
- Replaced forced `Agg` backends with a guarded headless fallback, so scripts remain headless-capable while Jupyter notebooks use the inline backend and retain their figure outputs.
- Re-executed and validated all 20 notebooks with a 30-second per-cell timeout and interactive cells skipped; each now contains embedded static PNG figures and no non-interactive error output.
- The longest recorded non-interactive cell in this batch was 1.78 seconds (`kernel-svm`).

## Batches 7-8 Full-Scan Completion

The final two batches cover the remaining 23 notebooks, from `newton-fractals-complex` through `wave-equation-dispersion`.

- Executed every non-interactive cell with a 30-second timeout and preserved cells tagged `interactive`.
- Confirmed valid notebook schemas, no non-interactive error output, explanatory markdown immediately before each non-interactive code cell, and at least one embedded static PNG in every notebook.
- No repairs were required in these final batches; the longest recorded non-interactive cell was 1.13 seconds (`unbalanced-ot`).

### Final Repository-Wide Consistency Repairs

- Added a concise explanatory markdown transition before the Cahn--Hilliard rendering cell in `allen-cahn-cahn-hilliard`.
- Restored two embedded static figures in `autoregressive` by displaying the existing plots before their existing file exports.
- Re-executed both notebooks successfully: their longest non-interactive cells were 0.60 and 0.41 seconds respectively.

## Boltzmann Batch-Execution Repair

Date: 2026-07-13

- Removed the `interactive` tag from the Boltzmann notebook's import and random-seed setup cell. That cell is part of the core simulation path, not interface code; skipping it left `rng` undefined and prevented headless execution.
- Kept the actual widget playback cell tagged `interactive`, so batch execution still avoids nonessential UI behavior.

### Execution Check

- The notebook now executes successfully with `ExecutePreprocessor.skip_cells_with_tag=interactive`.
- A representative static figure remains embedded, and the longest non-interactive cell takes 0.71 seconds.

## Batch 2 Documentation Repairs

Date: 2026-07-13

- Added short local interpretation cells before the Allen-Cahn and Cahn-Hilliard rendering panels, explaining their fixed phase scale and contrasting the two coarsening dynamics.
- Added an ISTA derivation before the Basis Pursuit regularization-path solver and redirected its snippet output to the notebook directory.

### Execution Check

- Both repaired notebooks execute cleanly with interactive cells skipped.
- Their static figures are embedded, and all checked non-interactive cells remain under the 30-second limit.

## Batch 3 Notebook-Schema Repairs

Date: 2026-07-13

- Removed invalid `outputs` fields from markdown cells in the Mirror Descent, Momentum Methods, and Gradient Flow notebooks. Markdown cells cannot carry execution outputs under the Jupyter notebook schema.
- Re-executed all three notebooks after the cleanup, preserving their code-cell outputs and any tagged interactive controls.

### Execution Check

- All 20 batch-3 notebooks pass in-place execution, `nbformat` validation, and the 30-second per-cell rule.
- Their static figures are embedded, and no generated image or video artifact was written to the repository root.

## Batch 4 Notebook-Schema Repairs

Date: 2026-07-13

- Removed invalid `outputs` fields from markdown cells in 13 notebooks spanning gradient methods, graph learning, gravitation, harmonic analysis, and heat-flow topics.
- Re-executed all 20 batch-4 notebooks after cleanup, so saved figures and execution metadata correspond to the valid notebook structure.

### Execution Check

- All 20 batch-4 notebooks pass in-place execution, `nbformat` validation, and the 30-second per-cell rule.
- Static figures are embedded in every notebook, and no generated image or video artifact was written to the repository root.

## Two-Dimensional Advection on a Periodic Domain

Date: 2026-07-13

- Expanded the opening exposition to connect the advection PDE, characteristic curves, periodic transport, and the stability-versus-diffusion trade-off of semi-Lagrangian interpolation.
- Clarified the periodic bilinear warp as the discrete operator $\mathcal W_{\rho u}$ and explained why its convex weights keep values bounded while damping fine detail.
- Replaced the independently smoothed random velocity components with a smooth periodic stream-function construction $u=(\partial_y\psi,-\partial_x\psi)$, giving a divergence-free transport field.
- Replaced the obsolete transport-amplitude sensitivity study with five temporal snapshots and a quantitative panel for mean value and contrast decay.
- Added a standalone interactive explorer with a time slider and play/stop control; it uses precomputed frames and is tagged `interactive` for safe batch execution.
- Regenerated the representative gallery image as a 600 x 600 square snippet saved locally in `python/advection/`.
- Updated the concluding explanation and bibliography with directly relevant references on semi-Lagrangian advection and stable fluid simulation.

### Execution Check

The notebook was executed in place with a 30-second timeout per non-interactive cell and `ExecutePreprocessor.skip_cells_with_tag=interactive`.

- Execution completed without errors.
- Three static PNG figure outputs are embedded in the notebook.
- The interactive slider/playback cell is preserved with the `interactive` tag and was not executed during batch validation.
- Longest non-interactive cell: 0.45 seconds.
- No generated image or video artifact was written to the repository root.

## ADMM for Sparse Recovery

Date: 2026-07-13

- Reworked the opening exposition around the underdetermined sparse-recovery problem, the LASSO objective, and the role of ADMM as a split method rather than a black-box solver.
- Split the former monolithic implementation into short cells for problem construction, critical regularization scale, ADMM updates, convergence monitoring, iterate snapshots, and final support recovery.
- Added the subgradient derivation of $\lambda_{\max}=\lVert A^\top y\rVert_\infty$, with the explicit choice $\lambda=\lambda_{\max}/10$ and a correlation-scale visualization.
- Replaced the explicit matrix inverse with a single Cholesky factorization reused at every ADMM round.
- Added a feasible LASSO dual certificate, so the primal-dual gap accompanies the primal and dual ADMM residuals instead of relying only on reconstruction error.
- Added distributed static figures for the target and measurements, regularization scale, convergence diagnostics, sparse-iterate evolution, and final support recovery.
- Added an `interactive`-tagged iterate slider while keeping the complete static numerical narrative available for automated execution.
- Replaced the execution-directory-relative snippet output with a notebook-local path and regenerated the snippet as a 613 x 613 square image.
- Added topic-specific references on ADMM, the LASSO, convex duality, and proximal algorithms.

### Execution Check

The notebook was executed in place with a 30-second timeout per non-interactive cell and `ExecutePreprocessor.skip_cells_with_tag=interactive`.

- Execution completed without errors.
- Five static PNG figure outputs are embedded in the notebook.
- The interactive cell is preserved with the `interactive` tag and was not executed during batch validation.
- Longest non-interactive cell: 0.97 seconds.
- The notebook passes `nbformat` validation, and every code cell has immediately preceding explanatory markdown.
- No generated image or video artifact was written to the repository root.

# Notebook Verification Tracker

This file tracks execution verification status for all notebooks currently present under `python/`.
It is a live snapshot and should be updated whenever notebooks are added or modified in parallel.

Validation rule used: execute with a 30-second max per code cell, skipping cells tagged `interactive`.

| Notebook | Status | Last verification | Improvement TODO |
|---|---|---|---|
| `python/ada-boost/ada-boost.ipynb` | Validated (30s rule) | 2026-03-22 | Pedagogical polish pass: verify equation rendering and bibliography completeness. |
| `python/advection/advection.ipynb` | Validated (30s rule) | 2026-03-22 | Pedagogical polish pass: verify equation rendering and bibliography completeness. |
| `python/alpha-shapes/alpha-shapes.ipynb` | Validated (30s rule) | 2026-03-22 | Add a parameter-sweep figure panel to better compare alpha values side-by-side. |
| `python/apolonian/apolonian.ipynb` | Validated (30s rule) | 2026-03-22 | Add a clearer geometric derivation cell before implementation details. |
| `python/approximation/approximation.ipynb` | Validated (30s rule) | 2026-03-22 | Add error-vs-parameter comparative plots for stronger interpretability. |
| `python/arithmetico-geometric/arithmetico-geometric.ipynb` | Validated (30s rule) | 2026-03-22 | Add a convergence-rate diagnostic plot and a brief reference list. |
| `python/autoregressive/autoregressive.ipynb` | Validated (30s rule) | 2026-03-22 | Add explicit stationarity-condition equations near simulation code. |
| `python/backprojection-radon/backprojection-radon.ipynb` | Validated (30s rule) | 2026-03-22 | Add a noise-level sweep to show robustness limits visually. |
| `python/bayesian/bayesian.ipynb` | Validated (30s rule) | 2026-03-22 | Add prior-sensitivity comparative panel for key posterior quantities. |
| `python/bernouilli-tcl/bernouilli-tcl.ipynb` | Validated (30s rule) | 2026-03-22 | Add finite-sample error curves vs Gaussian approximation. |
| `python/bifurcation/bifurcation.ipynb` | Validated (30s rule) | 2026-03-22 | Add a bifurcation-diagram refinement study with denser control-parameter sampling. |
| `python/bilateral-filtering/bilateral-filtering.ipynb` | Validated (30s rule) | 2026-03-22 | Add parameter-grid comparisons for sigma choices with fixed color scales. |
| `python/boltzmann/boltzmann.ipynb` | Validated (30s rule) | 2026-03-22 | Add a short bibliography and optional higher-accuracy collision notes. |
| `python/brachistochrone/brachistochrone.ipynb` | Validated (30s rule) | 2026-03-22 | Add sensitivity panel for discretization density and runtime tradeoff. |
| `python/bregman-flow/bregman-flow.ipynb` | Validated (30s rule) | 2026-03-22 | Add side-by-side trajectories for multiple damping/step choices. |
| `python/brownian/brownian.ipynb` | Validated (30s rule) | 2026-03-22 | Add MSD scaling-fit diagnostics and confidence bands. |
| `python/burgers/burgers.ipynb` | Validated (30s rule) | 2026-03-22 | Add a short note justifying CFL constants and default resolution choices. |
| `python/cellular/cellular.ipynb` | Validated (30s rule) | 2026-03-22 | Add a compact rule-comparison montage beyond current examples. |
| `python/conjugate-gradient/conjugate-gradient.ipynb` | Validated (30s rule) | 2026-03-22 | Add convergence comparison against steepest descent on same system. |
| `python/de-casteljau/de-casteljau.ipynb` | Validated (30s rule) | 2026-03-22 | Add control-point perturbation sweep to show geometric stability. |
| `python/dijkstra/dijkstra.ipynb` | Validated (30s rule) | 2026-03-22 | Add a complexity-focused section with scaling experiment. |
| `python/dtw/dtw.ipynb` | Validated (30s rule) | 2026-03-22 | Add sequence-length scaling analysis and optional pruning variants. |
| `python/dykstra/dykstra.ipynb` | Validated (30s rule) | 2026-03-22 | Add projection-set geometry variants to highlight convergence behavior. |
| `python/edge-detection/edge-detection.ipynb` | Validated (30s rule) | 2026-03-22 | Add threshold-sweep visual comparisons and explicit edge-quality metrics. |
| `python/error-diffusion/error-diffusion.ipynb` | Validated (30s rule) | 2026-03-22 | Add method comparison across dithering kernels on multiple images. |
| `python/extreme-values/extreme-values.ipynb` | Validated (30s rule) | 2026-03-22 | Add tail-fit diagnostics across sample sizes and confidence intervals. |
| `python/farthest-point/farthest-point.ipynb` | Validated (30s rule) | 2026-03-22 | Add coverage-error vs number-of-samples plots for multiple seeds. |
| `python/fixed-point/fixed-point.ipynb` | Validated (30s rule) | 2026-03-22 | Add contraction-vs-divergence scenario panel with theoretical condition checks. |
| `python/flocking/flocking.ipynb` | Validated (30s rule) | 2026-03-22 | Add an order-parameter time series to quantify alignment over time. |
| `python/floyd-warshall/floyd-warshall.ipynb` | Validated (30s rule) | 2026-03-22 | Add path-reconstruction visual examples on weighted random graphs. |
| `python/fluids/fluids.ipynb` | Validated (30s rule) | 2026-03-22 | Improve snapshot-step scheduling so all displayed frames map to intended times. |
| `python/fourier-atoms/fourier-atoms.ipynb` | Validated (30s rule) | 2026-03-22 | Add basis-size comparative reconstruction panel and error curves. |
| `python/fourier-cristal/fourier-cristal.ipynb` | Validated (30s rule) | 2026-03-22 | Add parameter sweep over minimum-distance values for blue-noise structure. |
| `python/fourier-curves/fourier-curves.ipynb` | Validated (30s rule) | 2026-03-22 | Add harmonics-count animation/static sequence with approximation error. |
| `python/fourier-matrix/fourier-matrix.ipynb` | Validated (30s rule) | 2026-03-22 | Add conditioning discussion with scaling plots over matrix sizes. |
| `python/fourier-signal/fourier-signal.ipynb` | Validated (30s rule) | 2026-03-22 | Add aliasing demonstrations at multiple sampling rates and filter settings. |
| `python/foveation/foveation.ipynb` | Validated (30s rule) | 2026-03-22 | Add eccentricity-parameter comparison gallery with quantitative reconstruction metrics. |
| `python/frac-der-gaussian/frac-der-gaussian.ipynb` | Validated (30s rule) | 2026-03-22 | Add order-parameter effect montage and normalization sensitivity analysis. |
| `python/fraction-continued/fraction-continued.ipynb` | Validated (30s rule) | 2026-03-22 | Add approximation-error vs depth chart for multiple irrational targets. |
| `python/fractional-laplacian/fractional-laplacian.ipynb` | Validated (30s rule) | 2026-03-22 | Add alpha sweep with consistent color scales and boundary-condition variants. |
| `python/frank-wolfe/frank-wolfe.ipynb` | Validated (30s rule) | 2026-03-22 | Add comparison against projected gradient on identical constraints/objectives. |
| `python/game-theory/game-theory.ipynb` | Validated (30s rule) | 2026-03-22 | Add payoff-parameter sensitivity scenarios with equilibrium stability notes. |
| `python/gauss-luca/gauss-luca.ipynb` | Validated (30s rule) | 2026-03-22 | Add polynomial-family comparisons (random, orthogonal, clustered roots). |
| `python/gaussian-fisher/gaussian-fisher.ipynb` | Validated (30s rule) | 2026-03-22 | Add information-geometry trajectory examples with geodesic/Euclidean contrast. |
| `python/gaussian-prod-convol/gaussian-prod-convol.ipynb` | Validated (30s rule) | 2026-03-22 | Add dimension-parameter comparative plots and numerical-stability notes. |
| `python/gears-non-circ/gears-non-circ.ipynb` | Validated (30s rule) | 2026-03-22 | Add contact/rolling-constraint diagnostics over a full motion cycle. |
| `python/geodesic-heat/geodesic-heat.ipynb` | Validated (30s rule) | 2026-03-22 | Add mesh-resolution tradeoff analysis and error-vs-runtime plot. |
| `python/gershgorin/gershgorin.ipynb` | Validated (30s rule) | 2026-03-22 | Add random-matrix examples with eigenvalue overlays across scales. |
| `python/gibbs-oscillations/gibbs-oscillations.ipynb` | Validated (30s rule) | 2026-03-22 | Add truncation-level sweep as a compact image series with overshoot metrics. |
| `python/gibbs-sampling/gibbs-sampling.ipynb` | Validated (30s rule) | 2026-03-22 | Add explicit convergence diagnostics (ESS/autocorrelation) and chain comparison. |
| `python/grad-desc-mirror/grad-desc-mirror.ipynb` | Validated (30s rule) | 2026-03-22 | Add side-by-side optimizer trajectories under multiple mirror maps. |
| `python/grad-desc-momentum/grad-desc-momentum.ipynb` | Validated (30s rule) | 2026-03-22 | Add momentum-parameter stability map and tag widget cells as interactive if added. |
| `python/grad-desc-ode/grad-desc-ode.ipynb` | Validated (30s rule) | 2026-03-22 | Add timestep discretization comparison with local/global error plots. |
| `python/grad-desc-quad/grad-desc-quad.ipynb` | Validated (30s rule) | 2026-03-22 | Add conditioning sweep experiments with rate-fit overlays. |
| `python/grad-desc/grad-desc.ipynb` | Validated (30s rule) | 2026-03-22 | Add line-search/stepsize comparative panel with per-iteration cost. |
| `python/gradflow-metric/gradflow-metric.ipynb` | Validated (30s rule) | 2026-03-22 | Add metric-choice visual comparisons and invariance discussion. |
| `python/graph-coloring/graph-coloring.ipynb` | Validated (30s rule) | 2026-03-22 | Add graph-size scaling metrics and color-count histograms across seeds. |
| `python/graph-laplacian/graph-laplacian.ipynb` | Validated (30s rule) | 2026-03-22 | Add eigenvector interpretation examples on multiple graph families. |
| `python/graphical-lasso/graphical-lasso.ipynb` | Validated (30s rule) | 2026-03-22 | Add regularization-path summary visuals and sparsity-vs-fit metrics. |
| `python/gravitation/gravitation.ipynb` | Validated (30s rule) | 2026-03-22 | Tag any future animation widgets and keep static fallback snapshots. |
| `python/gromov-wasserstein/gromov-wasserstein.ipynb` | Validated (30s rule) | 2026-03-22 | Add transport-cost scaling notes and heavier-case profiling. |
| `python/haar-walsh/haar-walsh.ipynb` | Validated (30s rule) | 2026-03-22 | Add basis truncation quality comparisons with compression ratios. |
| `python/harmonic-coords/harmonic-coords.ipynb` | Validated (30s rule) | 2026-03-22 | Add mesh/boundary-condition sensitivity examples; keep explicit triplot style kwargs. |
| `python/harmonic/harmonic.ipynb` | Validated (30s rule) | 2026-03-22 | Add comparative boundary-value test cases and residual diagnostics. |
| `python/heat-1d/heat-1d.ipynb` | Validated (30s rule) | 2026-03-22 | Add stability/accuracy curves over timesteps and grid refinements. |
| `python/heat-polynomials/heat-polynomials.ipynb` | Validated (30s rule) | 2026-03-22 | Add degree-vs-approximation error panel with log-scale residuals. |
| `python/heat-vs-tv/heat-vs-tv.ipynb` | Validated (30s rule) | 2026-03-22 | Add denoising-quality metric comparisons (PSNR/SSIM) across noise levels. |
| `python/heavy-ball/heavy-ball.ipynb` | Validated (30s rule) | 2026-03-22 | Add damping-regime phase diagram and explicit unstable-region examples. |
| `python/hermite-function/hermite-function.ipynb` | Validated (30s rule) | 2026-03-22 | Add order-dependent concentration visual series and uncertainty summary table. |
| `python/hilbert-curve/hilbert-curve.ipynb` | Validated (30s rule) | 2026-03-22 | Add order-growth complexity chart with memory/runtime trends. |
| `python/hist-eq/hist-eq.ipynb` | Validated (30s rule) | 2026-03-22 | Add before/after metric panel (contrast, entropy, local variance). |
| `python/holder-inequality/holder-inequality.ipynb` | Validated (30s rule) | 2026-03-22 | Add numerical tightness examples with controlled equality cases. |
| `python/hopfield-network/hopfield-network.ipynb` | Validated (30s rule) | 2026-03-22 | Add energy-landscape diagnostics and basin-size empirical estimates. |
| `python/ica/ica.ipynb` | Validated (30s rule) | 2026-03-22 | Add source-separation quality metrics and initialization sensitivity tests. |
| `python/icp/icp.ipynb` | Validated (30s rule) | 2026-03-22 | Add robustness tests under initialization noise and outlier contamination. |
| `python/integral-lines/integral-lines.ipynb` | Validated (30s rule) | 2026-03-22 | Add seed-density effect visual comparison and streamline-length statistics. |
| `python/interpolation-rkhs/interpolation-rkhs.ipynb` | Validated (30s rule) | 2026-03-22 | Add kernel-parameter sensitivity curves and regularization-path effects. |
| `python/interpolation-shepard/interpolation-shepard.ipynb` | Validated (30s rule) | 2026-03-22 | Add exponent-parameter interpolation comparisons with error heatmaps. |
| `python/hump-algebra/hump-algebra.ipynb` | Validated (30s rule) | 2026-03-22 | Add parameter-sweep panels showing hump morphology transitions. |
| `python/interior-points/interior-points.ipynb` | Validated (30s rule) | 2026-03-22 | Add barrier-parameter schedule diagnostics and KKT residual plots. |
| `python/interpol-vizu/interpol-vizu.ipynb` | Validated (30s rule) | 2026-03-22 | Add side-by-side interpolation-method comparisons on common datasets. |
| `python/interpolation-natural/interpolation-natural.ipynb` | Validated (30s rule) | 2026-03-22 | Add boundary-condition sensitivity and overshoot metrics. |
| `python/inverse-kinematics/inverse-kinematics.ipynb` | Validated (30s rule) | 2026-03-22 | Add convergence-vs-initialization study and joint-limit scenarios. |
| `python/ising-model/ising-model.ipynb` | Validated (30s rule) | 2026-03-22 | Add temperature sweep near criticality with magnetization/energy statistics. |
| `python/ista/ista.ipynb` | Validated (30s rule) | 2026-03-22 | Keep portable colormaps (`viridis`) and add sparsity-vs-error trajectory plots. |
| `python/iterated-polygons/iterated-polygons.ipynb` | Validated (30s rule) | 2026-03-22 | Add shape-evolution gallery across iteration and parameter choices. |
| `python/jko-flow/jko-flow.ipynb` | Validated (30s rule) | 2026-03-22 | Add timestep sensitivity and Wasserstein-distance decay diagnostics. |
| `python/joukowski/joukowski.ipynb` | Validated (30s rule) | 2026-03-22 | Add parameter variation over airfoil shapes with flow-field snapshots. |
| `python/julia-sets/julia-sets.ipynb` | Validated (30s rule) | 2026-03-22 | Add complex-parameter sweep panel and convergence-iteration histogram. |

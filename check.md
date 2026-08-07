# Notebook Verification Tracker

This file tracks execution verification status for all notebooks currently present under `python/`.
It is a live snapshot and should be updated whenever notebooks are added or modified in parallel.

Validation rule used: execute with a 30-second max per code cell, skipping cells tagged `interactive`.

Recent rechecks (2026-03-24):
- `python/gears-non-circ/gears-non-circ.ipynb` rewritten and executed with embedded outputs.
- `python/geodesic-heat/geodesic-heat.ipynb` rewritten and executed with embedded outputs.
- `python/hump-algebra/hump-algebra.ipynb` rewritten and executed with embedded outputs.
- `python/icp/icp.ipynb` rewritten and executed with embedded outputs.
- `python/integral-lines/integral-lines.ipynb` rewritten and executed with embedded outputs.
- `python/interior-points/interior-points.ipynb` rewritten and executed with embedded outputs.
- `python/interpol-vizu/interpol-vizu.ipynb` rewritten and executed with embedded outputs.
- `python/interpolation-natural/interpolation-natural.ipynb` rewritten and executed with embedded outputs.

Historical snapshot (2026-03-22): 149 notebooks tracked, 149 validated, 0 pending.

Fresh scan status (2026-07-14): 143 notebooks are currently present under `python/`. Batches 1 through 8 revalidated all 143 paths in alphabetical order: all passed the 30-second execution rule with embedded static figures. The documentation and metadata follow-ups found during the scan were corrected and revalidated.

| Notebook | Status | Last verification | Improvement TODO |
|---|---|---|---|
| `python/ada-boost/ada-boost.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Pedagogical polish pass: verify equation rendering and bibliography completeness. |
| `python/admm-first-principles/admm-first-principles.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add rho-parameter sweep with primal/dual residual balance visualization. |
| `python/advection/advection.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Pedagogical polish pass: verify equation rendering and bibliography completeness. |
| `python/allen-cahn-cahn-hilliard/allen-cahn-cahn-hilliard.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Rendering exposition restored; optional next step: add side-by-side phase-field evolution snapshots for parameter changes. |
| `python/alpha-shapes/alpha-shapes.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add a parameter-sweep figure panel to better compare alpha values side-by-side. |
| `python/apolonian/apolonian.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add a clearer geometric derivation cell before implementation details. |
| `python/approximation/approximation.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add error-vs-parameter comparative plots for stronger interpretability. |
| `python/arithmetico-geometric/arithmetico-geometric.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add a convergence-rate diagnostic plot and a brief reference list. |
| `python/autoregressive/autoregressive.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add explicit stationarity-condition equations near simulation code. |
| `python/backprojection-radon/backprojection-radon.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add a noise-level sweep to show robustness limits visually. |
| `python/bayesian/bayesian.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add prior-sensitivity comparative panel for key posterior quantities. |
| `python/bernouilli-tcl/bernouilli-tcl.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add finite-sample error curves vs Gaussian approximation. |
| `python/bifurcation/bifurcation.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add a bifurcation-diagram refinement study with denser control-parameter sampling. |
| `python/bilateral-filtering/bilateral-filtering.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add parameter-grid comparisons for sigma choices with fixed color scales. |
| `python/boltzmann/boltzmann.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Core setup untagged and revalidated; optional next step: add a short bibliography and higher-accuracy collision notes. |
| `python/brachistochrone/brachistochrone.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add sensitivity panel for discretization density and runtime tradeoff. |
| `python/bregman-flow/bregman-flow.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add side-by-side trajectories for multiple damping/step choices. |
| `python/brownian/brownian.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add MSD scaling-fit diagnostics and confidence bands. |
| `python/burgers/burgers.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add a short note justifying CFL constants and default resolution choices. |
| `python/cellular/cellular.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add a compact rule-comparison montage beyond current examples. |
| `python/conjugate-gradient/conjugate-gradient.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add convergence comparison against steepest descent on same system. |
| `python/de-casteljau/de-casteljau.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add control-point perturbation sweep to show geometric stability. |
| `python/dijkstra/dijkstra.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add a complexity-focused section with scaling experiment. |
| `python/dtw/dtw.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add sequence-length scaling analysis and optional pruning variants. |
| `python/dykstra/dykstra.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add projection-set geometry variants to highlight convergence behavior. |
| `python/edge-detection/edge-detection.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add threshold-sweep visual comparisons and explicit edge-quality metrics. |
| `python/error-diffusion/error-diffusion.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add method comparison across dithering kernels on multiple images. |
| `python/extreme-values/extreme-values.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add tail-fit diagnostics across sample sizes and confidence intervals. |
| `python/farthest-point/farthest-point.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add coverage-error vs number-of-samples plots for multiple seeds. |
| `python/fixed-point/fixed-point.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add contraction-vs-divergence scenario panel with theoretical condition checks. |
| `python/flocking/flocking.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add an order-parameter time series to quantify alignment over time. |
| `python/floyd-warshall/floyd-warshall.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add path-reconstruction visual examples on weighted random graphs. |
| `python/fluids/fluids.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Snapshot scheduling fixed; next pass can add Reynolds-number parameter sweep panel. |
| `python/fourier-atoms/fourier-atoms.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add basis-size comparative reconstruction panel and error curves. |
| `python/fourier-cristal/fourier-cristal.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add parameter sweep over minimum-distance values for blue-noise structure. |
| `python/fourier-curves/fourier-curves.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add harmonics-count animation/static sequence with approximation error. |
| `python/fourier-matrix/fourier-matrix.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add conditioning discussion with scaling plots over matrix sizes. |
| `python/fourier-signal/fourier-signal.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add aliasing demonstrations at multiple sampling rates and filter settings. |
| `python/foveation/foveation.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add eccentricity-parameter comparison gallery with quantitative reconstruction metrics. |
| `python/frac-der-gaussian/frac-der-gaussian.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add order-parameter effect montage and normalization sensitivity analysis. |
| `python/fraction-continued/fraction-continued.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add approximation-error vs depth chart for multiple irrational targets. |
| `python/fractional-laplacian/fractional-laplacian.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add alpha sweep with consistent color scales and boundary-condition variants. |
| `python/frank-wolfe/frank-wolfe.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add comparison against projected gradient on identical constraints/objectives. |
| `python/game-theory/game-theory.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add payoff-parameter sensitivity scenarios with equilibrium stability notes. |
| `python/gauss-luca/gauss-luca.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add polynomial-family comparisons (random, orthogonal, clustered roots). |
| `python/gaussian-fisher/gaussian-fisher.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add information-geometry trajectory examples with geodesic/Euclidean contrast. |
| `python/gaussian-prod-convol/gaussian-prod-convol.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add dimension-parameter comparative plots and numerical-stability notes. |
| `python/gears-non-circ/gears-non-circ.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add contact/rolling-constraint diagnostics over a full motion cycle. |
| `python/geodesic-heat/geodesic-heat.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add mesh-resolution tradeoff analysis and error-vs-runtime plot. |
| `python/gershgorin/gershgorin.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add random-matrix examples with eigenvalue overlays across scales. |
| `python/gibbs-oscillations/gibbs-oscillations.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add truncation-level sweep as a compact image series with overshoot metrics. |
| `python/gibbs-sampling/gibbs-sampling.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add explicit convergence diagnostics (ESS/autocorrelation) and chain comparison. |
| `python/grad-desc-mirror/grad-desc-mirror.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; optional next step: add side-by-side optimizer trajectories under multiple mirror maps.
| `python/grad-desc-momentum/grad-desc-momentum.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; optional next step: add a momentum-parameter stability map.
| `python/grad-desc-ode/grad-desc-ode.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; optional next step: add timestep-discretization error plots.
| `python/grad-desc-quad/grad-desc-quad.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add conditioning sweep experiments with rate-fit overlays. |
| `python/gradflow-metric/gradflow-metric.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add metric-choice visual comparisons and invariance discussion. |
| `python/graph-coloring/graph-coloring.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add graph-size scaling metrics and color-count histograms across seeds. |
| `python/graph-laplacian/graph-laplacian.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add eigenvector interpretation examples on multiple graph families. |
| `python/graphical-lasso/graphical-lasso.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add regularization-path summary visuals and sparsity-vs-fit metrics. |
| `python/gravitation/gravitation.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; tag any future animation widgets and keep static fallback snapshots. |
| `python/gromov-wasserstein/gromov-wasserstein.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add transport-cost scaling notes and heavier-case profiling. |
| `python/haar-walsh/haar-walsh.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add basis truncation quality comparisons with compression ratios. |
| `python/harmonic/harmonic.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add comparative boundary-value test cases and residual diagnostics. |
| `python/heat-1d/heat-1d.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add stability/accuracy curves over timesteps and grid refinements. |
| `python/heat-polynomials/heat-polynomials.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add degree-vs-approximation error panel with log-scale residuals. |
| `python/heat-vs-tv/heat-vs-tv.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add denoising-quality metric comparisons (PSNR/SSIM) across noise levels. |
| `python/heavy-ball/heavy-ball.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add damping-regime phase diagram and explicit unstable-region examples. |
| `python/hermite-function/hermite-function.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Removed invalid `outputs` fields from markdown cells; add order-dependent concentration visual series and uncertainty summary table. |
| `python/hilbert-curve/hilbert-curve.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add order-growth complexity chart with memory/runtime trends. |
| `python/hist-eq/hist-eq.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add before/after metric panel (contrast, entropy, local variance). |
| `python/holder-inequality/holder-inequality.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add numerical tightness examples with controlled equality cases. |
| `python/hopfield-network/hopfield-network.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add energy-landscape diagnostics and basin-size empirical estimates. |
| `python/hump-algebra/hump-algebra.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add parameter-sweep panels showing hump morphology transitions. |
| `python/ica/ica.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add source-separation quality metrics and initialization sensitivity tests. |
| `python/icp/icp.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add robustness tests under initialization noise and outlier contamination. |
| `python/integral-lines/integral-lines.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add seed-density effect visual comparison and streamline-length statistics. |
| `python/interior-points/interior-points.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Remove invalid top-level `nbformat_minus` metadata; re-executed with embedded figures. |
| `python/interpol-vizu/interpol-vizu.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add side-by-side interpolation-method comparisons on common datasets. |
| `python/interpolation-natural/interpolation-natural.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add boundary-condition sensitivity and overshoot metrics. |
| `python/interpolation-rkhs/interpolation-rkhs.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add kernel-parameter sensitivity curves and regularization-path effects. |
| `python/interpolation-shepard/interpolation-shepard.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add exponent-parameter interpolation comparisons with error heatmaps. |
| `python/inverse-kinematics/inverse-kinematics.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add convergence-vs-initialization study and joint-limit scenarios. |
| `python/ising-model/ising-model.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add temperature sweep near criticality with magnetization/energy statistics. |
| `python/ista/ista.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Keep portable colormaps (`viridis`) and add sparsity-vs-error trajectory plots. |
| `python/iterated-polygons/iterated-polygons.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add shape-evolution gallery across iteration and parameter choices. |
| `python/jko-flow/jko-flow.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add timestep sensitivity and Wasserstein-distance decay diagnostics. |
| `python/joukowski/joukowski.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add parameter variation over airfoil shapes with flow-field snapshots. |
| `python/julia-sets/julia-sets.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add complex-parameter sweep panel and convergence-iteration histogram. |
| `python/k-nn/k-nn.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kaczmarz/kaczmarz.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kalman/kalman.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kernel-approx-1d/kernel-approx-1d.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kernel-pca/kernel-pca.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kernel-svm/kernel-svm.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kinetics-evolution/kinetics-evolution.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kmean++/kmeanpp.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Convergence-mean aggregation fixed for variable-length Lloyd curves; add seed-sensitivity boxplot. |
| `python/kmeans/kmeans.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kriging/kriging.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kubo-matrix-mean/kubo-matrix-mean.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Mathtext labels fixed (`\sharp`); add 3x3 SPD example to broaden intuition. |
| `python/lagrange-hermite/lagrange-hermite.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/lagrangian-flows/lagrangian-flows.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/lagrangian-vs-eulerian/lagrangian-vs-eulerian.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Matplotlib compatibility fix applied (`streamplot` alpha removed); add side-by-side time-parameter sweep snapshots. |
| `python/laplacian-eigenmaps/laplacian-eigenmaps.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/laplacian-pyramid/laplacian-pyramid.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Execute with 30s-per-cell rule and embed outputs. |
| `python/laplacian-spectrum/laplacian-spectrum.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add eigenvalue-gap diagnostics across multiple graph families. |
| `python/laplacian-weighted/laplacian-weighted.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add a side-by-side weight-kernel parameter sweep with consistent color scales. |
| `python/lda-qda/lda-qda.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add covariance-regularization sensitivity and decision-boundary comparison. |
| `python/legendre/legendre.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add degree-growth stability plots and orthogonality numerical error diagnostics. |
| `python/sinkhorn-distance/sinkhorn-distance.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add an epsilon-scaling panel showing plan sharpness vs numerical stability. |
| `python/unbalanced-ot/unbalanced-ot.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add a mass-penalty sweep to clarify balanced/unbalanced behavior transition. |
| `python/wasserstein-barycenters/wasserstein-barycenters.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add a weights-interpolation grid to better expose barycenter geometry changes. |
| `python/sliced-wasserstein/sliced-wasserstein.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add projection-count sensitivity with error/runtime tradeoff curves. |
| `python/schrodinger-bridge/schrodinger-bridge.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add diffusion-strength comparison to separate stochastic vs deterministic transport effects. |
| `python/mean-curvature-flow/mean-curvature-flow.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add timestep sensitivity and area-decay diagnostics for numerical consistency. |
| `python/eikonal-fast-marching/eikonal-fast-marching.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add obstacle/metric variation examples to compare travel-time geometry. |
| `python/reaction-diffusion-turing/reaction-diffusion-turing.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add parameter-map thumbnails to classify stripe/spot regimes. |
| `python/wave-equation-dispersion/wave-equation-dispersion.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add dispersion-relation overlays for multiple discretization choices. |
| `python/hamiltonian-symplectic/hamiltonian-symplectic.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Reworked to a periodic 2D N-body Hamiltonian simulation with Euler vs velocity-Verlet comparison; optional next step: add interactive slider for dt and particle count. |
| `python/fem-1d-2d/fem-1d-2d.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add mesh-refinement convergence rates and boundary-condition variants. |
| `python/poisson-meshes/poisson-meshes.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add boundary-data perturbation examples and residual/error field visualizations. |
| `python/level-set-methods/level-set-methods.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add reinitialization-frequency sweep to quantify interface distortion effects. |
| `python/compressed-sensing-basis-pursuit/compressed-sensing-basis-pursuit.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Added local ISTA exposition and safe snippet path; optional next step: add phase-transition heatmaps over sparsity and sampling ratios. |
| `python/orthogonal-matching-pursuit/orthogonal-matching-pursuit.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add support-recovery precision/recall diagnostics under noise. |
| `python/pdhg-chambolle-pock/pdhg-chambolle-pock.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add step-size condition stress tests and objective-gap trajectories. |
| `python/newton-fractals-complex/newton-fractals-complex.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add polynomial-family comparisons (root multiplicity, clustered roots) for basin sensitivity. |
| `python/chebyshev-minimax/chebyshev-minimax.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add explicit equioscillation diagnostics and a lightweight Remez comparison. |
| `python/markov-chains-mixing/markov-chains-mixing.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add spectral-gap vs empirical mixing-rate overlay for multiple chain families. |
| `python/hmm-forward-backward/hmm-forward-backward.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add backward-smoothing curves to complement filtering and Viterbi paths. |
| `python/diffusion-models-toy/diffusion-models-toy.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add multi-step reverse chain snapshots rather than single-step denoise proxy. |
| `python/tsne-umap-comparison/tsne-umap-comparison.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add neighborhood-preservation metrics (trustworthiness/continuity) per embedding. |
| `python/spectral-graph-wavelets/spectral-graph-wavelets.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add localization-width diagnostics across scales and graph topologies. |
| `python/pagerank-random-walks/pagerank-random-walks.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add power-iteration convergence curves and teleportation personalization variants. |
| `python/riemannian-optimization-stiefel/riemannian-optimization-stiefel.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add stepsize sweep and tangent-norm decay plots for optimization diagnostics. |
| `python/matrix-completion-nuclear-norm/matrix-completion-nuclear-norm.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-13 | Add sampling-ratio phase plot for recovery probability. |
| `python/robust-pca-lowrank-sparse/robust-pca-lowrank-sparse.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add corruption-level sensitivity and singular-value spectrum comparisons. |
| `python/persistent-homology-topology/persistent-homology-topology.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add explicit barcode rendering and a one-cycle ($H_1$) toy example. |
| `python/spherical-harmonics-signals/spherical-harmonics-signals.ipynb` | Validated (fresh batch; 30s rule) | 2026-07-14 | Add coefficient-energy spectrum and reconstruction truncation study. |

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

Current sync (2026-03-22): 149 notebooks tracked, 149 validated, 0 pending.

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
| `python/fluids/fluids.ipynb` | Validated (30s rule) | 2026-03-22 | Snapshot scheduling fixed; next pass can add Reynolds-number parameter sweep panel. |
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
| `python/harmonic-coords/harmonic-coords.ipynb` | Validated (30s rule) | 2026-03-22 | Intro now matches uniform Laplacian implementation; add cotangent-Laplacian comparison panel. |
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
| `python/hump-algebra/hump-algebra.ipynb` | Validated (30s rule) | 2026-03-22 | Add parameter-sweep panels showing hump morphology transitions. |
| `python/ica/ica.ipynb` | Validated (30s rule) | 2026-03-22 | Add source-separation quality metrics and initialization sensitivity tests. |
| `python/icp/icp.ipynb` | Validated (30s rule) | 2026-03-22 | Add robustness tests under initialization noise and outlier contamination. |
| `python/integral-lines/integral-lines.ipynb` | Validated (30s rule) | 2026-03-22 | Add seed-density effect visual comparison and streamline-length statistics. |
| `python/interior-points/interior-points.ipynb` | Validated (30s rule) | 2026-03-22 | Add barrier-parameter schedule diagnostics and KKT residual plots. |
| `python/interpol-vizu/interpol-vizu.ipynb` | Validated (30s rule) | 2026-03-22 | Add side-by-side interpolation-method comparisons on common datasets. |
| `python/interpolation-natural/interpolation-natural.ipynb` | Validated (30s rule) | 2026-03-22 | Add boundary-condition sensitivity and overshoot metrics. |
| `python/interpolation-rkhs/interpolation-rkhs.ipynb` | Validated (30s rule) | 2026-03-22 | Add kernel-parameter sensitivity curves and regularization-path effects. |
| `python/interpolation-shepard/interpolation-shepard.ipynb` | Validated (30s rule) | 2026-03-22 | Add exponent-parameter interpolation comparisons with error heatmaps. |
| `python/inverse-kinematics/inverse-kinematics.ipynb` | Validated (30s rule) | 2026-03-22 | Add convergence-vs-initialization study and joint-limit scenarios. |
| `python/ising-model/ising-model.ipynb` | Validated (30s rule) | 2026-03-22 | Add temperature sweep near criticality with magnetization/energy statistics. |
| `python/ista/ista.ipynb` | Validated (30s rule) | 2026-03-22 | Keep portable colormaps (`viridis`) and add sparsity-vs-error trajectory plots. |
| `python/iterated-polygons/iterated-polygons.ipynb` | Validated (30s rule) | 2026-03-22 | Add shape-evolution gallery across iteration and parameter choices. |
| `python/jko-flow/jko-flow.ipynb` | Validated (30s rule) | 2026-03-22 | Add timestep sensitivity and Wasserstein-distance decay diagnostics. |
| `python/joukowski/joukowski.ipynb` | Validated (30s rule) | 2026-03-22 | Add parameter variation over airfoil shapes with flow-field snapshots. |
| `python/julia-sets/julia-sets.ipynb` | Validated (30s rule) | 2026-03-22 | Add complex-parameter sweep panel and convergence-iteration histogram. |
| `python/k-nn/k-nn.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kaczmarz/kaczmarz.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kalman/kalman.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kernel-approx-1d/kernel-approx-1d.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kernel-pca/kernel-pca.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kernel-svm/kernel-svm.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kinetics-evolution/kinetics-evolution.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kmean++/kmeanpp.ipynb` | Validated (30s rule) | 2026-03-22 | Convergence-mean aggregation fixed for variable-length Lloyd curves; add seed-sensitivity boxplot. |
| `python/kmeans/kmeans.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kriging/kriging.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/kubo-matrix-mean/kubo-matrix-mean.ipynb` | Validated (30s rule) | 2026-03-22 | Mathtext labels fixed (`\sharp`); add 3x3 SPD example to broaden intuition. |
| `python/lagrange-hermite/lagrange-hermite.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/lagrangian-flows/lagrangian-flows.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/lagrangian-vs-eulerian/lagrangian-vs-eulerian.ipynb` | Validated (30s rule) | 2026-03-22 | Matplotlib compatibility fix applied (`streamplot` alpha removed); add side-by-side time-parameter sweep snapshots. |
| `python/laplacian-eigenmaps/laplacian-eigenmaps.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/laplacian-pyramid/laplacian-pyramid.ipynb` | Validated (30s rule) | 2026-03-22 | Execute with 30s-per-cell rule and embed outputs. |
| `python/laplacian-spectrum/laplacian-spectrum.ipynb` | Validated (30s rule) | 2026-03-22 | Add eigenvalue-gap diagnostics across multiple graph families. |
| `python/laplacian-weighted/laplacian-weighted.ipynb` | Validated (30s rule) | 2026-03-22 | Add a side-by-side weight-kernel parameter sweep with consistent color scales. |
| `python/lda-qda/lda-qda.ipynb` | Validated (30s rule) | 2026-03-22 | Add covariance-regularization sensitivity and decision-boundary comparison. |
| `python/legendre/legendre.ipynb` | Validated (30s rule) | 2026-03-22 | Add degree-growth stability plots and orthogonality numerical error diagnostics. |
| `python/sinkhorn-distance/sinkhorn-distance.ipynb` | Validated (30s rule) | 2026-03-22 | Add an epsilon-scaling panel showing plan sharpness vs numerical stability. |
| `python/unbalanced-ot/unbalanced-ot.ipynb` | Validated (30s rule) | 2026-03-22 | Add a mass-penalty sweep to clarify balanced/unbalanced behavior transition. |
| `python/wasserstein-barycenters/wasserstein-barycenters.ipynb` | Validated (30s rule) | 2026-03-22 | Add a weights-interpolation grid to better expose barycenter geometry changes. |
| `python/sliced-wasserstein/sliced-wasserstein.ipynb` | Validated (30s rule) | 2026-03-22 | Add projection-count sensitivity with error/runtime tradeoff curves. |
| `python/schrodinger-bridge/schrodinger-bridge.ipynb` | Validated (30s rule) | 2026-03-22 | Add diffusion-strength comparison to separate stochastic vs deterministic transport effects. |
| `python/mean-curvature-flow/mean-curvature-flow.ipynb` | Validated (30s rule) | 2026-03-22 | Add timestep sensitivity and area-decay diagnostics for numerical consistency. |
| `python/eikonal-fast-marching/eikonal-fast-marching.ipynb` | Validated (30s rule) | 2026-03-22 | Add obstacle/metric variation examples to compare travel-time geometry. |
| `python/allen-cahn-cahn-hilliard/allen-cahn-cahn-hilliard.ipynb` | Validated (30s rule) | 2026-03-22 | Add side-by-side phase-field evolution snapshots for parameter changes. |
| `python/reaction-diffusion-turing/reaction-diffusion-turing.ipynb` | Validated (30s rule) | 2026-03-22 | Add parameter-map thumbnails to classify stripe/spot regimes. |
| `python/wave-equation-dispersion/wave-equation-dispersion.ipynb` | Validated (30s rule) | 2026-03-22 | Add dispersion-relation overlays for multiple discretization choices. |
| `python/hamiltonian-symplectic/hamiltonian-symplectic.ipynb` | Validated (30s rule) | 2026-03-22 | Reworked to a periodic 2D N-body Hamiltonian simulation with Euler vs velocity-Verlet comparison; optional next step: add interactive slider for dt and particle count. |
| `python/fem-1d-2d/fem-1d-2d.ipynb` | Validated (30s rule) | 2026-03-22 | Add mesh-refinement convergence rates and boundary-condition variants. |
| `python/poisson-meshes/poisson-meshes.ipynb` | Validated (30s rule) | 2026-03-22 | Add boundary-data perturbation examples and residual/error field visualizations. |
| `python/level-set-methods/level-set-methods.ipynb` | Validated (30s rule) | 2026-03-22 | Add reinitialization-frequency sweep to quantify interface distortion effects. |
| `python/compressed-sensing-basis-pursuit/compressed-sensing-basis-pursuit.ipynb` | Validated (30s rule) | 2026-03-22 | Add phase-transition heatmaps over sparsity and sampling ratios. |
| `python/orthogonal-matching-pursuit/orthogonal-matching-pursuit.ipynb` | Validated (30s rule) | 2026-03-22 | Add support-recovery precision/recall diagnostics under noise. |
| `python/admm-first-principles/admm-first-principles.ipynb` | Validated (30s rule) | 2026-03-22 | Add rho-parameter sweep with primal/dual residual balance visualization. |
| `python/pdhg-chambolle-pock/pdhg-chambolle-pock.ipynb` | Validated (30s rule) | 2026-03-22 | Add step-size condition stress tests and objective-gap trajectories. |
| `python/bfgs-lbfgs/bfgs-lbfgs.ipynb` | Validated (30s rule) | 2026-03-22 | Add memory-size sweep for L-BFGS with convergence/runtime comparison. |
| `python/trust-region-methods/trust-region-methods.ipynb` | Validated (30s rule) | 2026-03-22 | Add trust-radius adaptation diagnostics and acceptance-ratio histograms. |
| `python/newton-fractals-complex/newton-fractals-complex.ipynb` | Validated (30s rule) | 2026-03-22 | Add polynomial-family comparisons (root multiplicity, clustered roots) for basin sensitivity. |
| `python/chebyshev-minimax/chebyshev-minimax.ipynb` | Validated (30s rule) | 2026-03-22 | Add explicit equioscillation diagnostics and a lightweight Remez comparison. |
| `python/runge-kutta-stability/runge-kutta-stability.ipynb` | Validated (30s rule) | 2026-03-22 | Add stiff test-equation trajectories to connect regions with time-domain behavior. |
| `python/markov-chains-mixing/markov-chains-mixing.ipynb` | Validated (30s rule) | 2026-03-22 | Add spectral-gap vs empirical mixing-rate overlay for multiple chain families. |
| `python/hmm-forward-backward/hmm-forward-backward.ipynb` | Validated (30s rule) | 2026-03-22 | Add backward-smoothing curves to complement filtering and Viterbi paths. |
| `python/particle-filters-smc/particle-filters-smc.ipynb` | Validated (30s rule) | 2026-03-22 | Add particle-count sweep showing ESS and tracking RMSE tradeoffs. |
| `python/variational-inference-gmm/variational-inference-gmm.ipynb` | Validated (30s rule) | 2026-03-22 | Add uncertainty ellipses and EM-side baseline for tighter pedagogical contrast. |
| `python/gaussian-processes-2d/gaussian-processes-2d.ipynb` | Validated (30s rule) | 2026-03-22 | Add length-scale and noise sweeps with calibrated uncertainty interpretation. |
| `python/normalizing-flows-2d/normalizing-flows-2d.ipynb` | Validated (30s rule) | 2026-03-22 | Add log-density contour reconstruction to accompany sample visualization. |
| `python/diffusion-models-toy/diffusion-models-toy.ipynb` | Validated (30s rule) | 2026-03-22 | Add multi-step reverse chain snapshots rather than single-step denoise proxy. |
| `python/tsne-umap-comparison/tsne-umap-comparison.ipynb` | Validated (30s rule) | 2026-03-22 | Add neighborhood-preservation metrics (trustworthiness/continuity) per embedding. |
| `python/spectral-graph-wavelets/spectral-graph-wavelets.ipynb` | Validated (30s rule) | 2026-03-22 | Add localization-width diagnostics across scales and graph topologies. |
| `python/pagerank-random-walks/pagerank-random-walks.ipynb` | Validated (30s rule) | 2026-03-22 | Add power-iteration convergence curves and teleportation personalization variants. |
| `python/gnn-message-passing-toy/gnn-message-passing-toy.ipynb` | Validated (30s rule) | 2026-03-22 | Add oversmoothing depth study with separation metrics by layer count. |
| `python/riemannian-optimization-stiefel/riemannian-optimization-stiefel.ipynb` | Validated (30s rule) | 2026-03-22 | Add stepsize sweep and tangent-norm decay plots for optimization diagnostics. |
| `python/matrix-completion-nuclear-norm/matrix-completion-nuclear-norm.ipynb` | Validated (30s rule) | 2026-03-22 | Add sampling-ratio phase plot for recovery probability. |
| `python/robust-pca-lowrank-sparse/robust-pca-lowrank-sparse.ipynb` | Validated (30s rule) | 2026-03-22 | Add corruption-level sensitivity and singular-value spectrum comparisons. |
| `python/persistent-homology-topology/persistent-homology-topology.ipynb` | Validated (30s rule) | 2026-03-22 | Add explicit barcode rendering and a one-cycle ($H_1$) toy example. |
| `python/spherical-harmonics-signals/spherical-harmonics-signals.ipynb` | Validated (30s rule) | 2026-03-22 | Add coefficient-energy spectrum and reconstruction truncation study. |
| `python/finite-groups-fft-cyclic/finite-groups-fft-cyclic.ipynb` | Validated (30s rule) | 2026-03-22 | Add character orthogonality verification and convolution theorem residual plots. |

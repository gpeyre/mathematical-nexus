# Notebook Correction and Validation Report

_Last updated: 7 August 2026_

## Scope and protocol

All 138 notebooks currently under `python/` were reviewed against `method.md`, freshly executed in their own directories, and saved in place so that static outputs remain embedded. Batch execution used a 30-second per-cell timeout, `NBEXECUTE=1`, and skipped only cells tagged `interactive`; those tagged cells remain available when a reader opens the notebook.

The final saved-state audit records:

- **138/138 valid notebooks**, with no schema or Python compilation failures.
- **138/138 successful executions**, with no saved errors or warnings.
- **392 embedded visual outputs**, with at least one in every notebook.
- **12.954 seconds** for the slowest recorded cell, below the 30-second ceiling.
- **50 interactive cells** correctly tagged for nonblocking batch execution.
- **0 unexecuted noninteractive cells**, **0 code cells lacking preceding exposition**, and **0 code cells longer than 60 lines**.
- **0 missing bibliographies**, **0 source-material references outside legitimate bibliography titles**, and **0 output artifacts written to the repository root**.

## Corrections made

- Strengthened short openings with the mathematical problem, governing equation, interpretation, and reading guide.
- Added focused primary references and textbooks where bibliographies were absent.
- Corrected unstable or misleading mathematics in the generalized extreme-value, Gibbs, exact line-search, graph-distance, spectral, and PDE examples.
- Removed all reproducible runtime, syntax, deprecation, future, and layout warnings.
- Split multi-purpose code cells into conceptual stages, each introduced by explanatory mathematics.
- Restored intermediate figures in diffusion, farthest-point sampling, Bayesian inference, Frank-Wolfe, Boltzmann dynamics, and flow comparisons instead of postponing all results.
- Added or repaired batch-safe sliders for approximation, brachistochrone, Bayesian prior sensitivity, and foveated filtering.
- Replaced the foveation notebook's external image dependency with a bundled Matplotlib sample and removed duplicate imports.
- Redirected persistent figures to notebook-local directories so execution never pollutes the repository root.
- Regenerated `database.xlsx`, `database.json`, and `database.js` after the notebook pass.

## Notebook ledger

| Notebook | Result | Review or correction |
|---|---|---|
| [python/ada-boost/ada-boost.ipynb](python/ada-boost/ada-boost.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/admm-first-principles/admm-first-principles.ipynb](python/admm-first-principles/admm-first-principles.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/advection/advection.ipynb](python/advection/advection.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/allen-cahn-cahn-hilliard/allen-cahn-cahn-hilliard.ipynb](python/allen-cahn-cahn-hilliard/allen-cahn-cahn-hilliard.ipynb) | Pass | opening exposition strengthened; topic bibliography added. |
| [python/alpha-shapes/alpha-shapes.ipynb](python/alpha-shapes/alpha-shapes.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/apolonian/apolonian.ipynb](python/apolonian/apolonian.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/approximation/approximation.ipynb](python/approximation/approximation.ipynb) | Pass | opening exposition strengthened; interactive cell made batch-safe. |
| [python/arithmetico-geometric/arithmetico-geometric.ipynb](python/arithmetico-geometric/arithmetico-geometric.ipynb) | Pass | opening exposition strengthened. |
| [python/autoregressive/autoregressive.ipynb](python/autoregressive/autoregressive.ipynb) | Pass | opening exposition strengthened. |
| [python/backprojection-radon/backprojection-radon.ipynb](python/backprojection-radon/backprojection-radon.ipynb) | Pass | opening exposition strengthened. |
| [python/bayesian/bayesian.ipynb](python/bayesian/bayesian.ipynb) | Pass | opening exposition strengthened; rendering/output placement improved; interactive cell made batch-safe. |
| [python/bernouilli-tcl/bernouilli-tcl.ipynb](python/bernouilli-tcl/bernouilli-tcl.ipynb) | Pass | opening exposition strengthened. |
| [python/bifurcation/bifurcation.ipynb](python/bifurcation/bifurcation.ipynb) | Pass | opening exposition strengthened. |
| [python/bilateral-filtering/bilateral-filtering.ipynb](python/bilateral-filtering/bilateral-filtering.ipynb) | Pass | opening exposition strengthened. |
| [python/boltzmann/boltzmann.ipynb](python/boltzmann/boltzmann.ipynb) | Pass | opening exposition strengthened; rendering/output placement improved. |
| [python/brachistochrone/brachistochrone.ipynb](python/brachistochrone/brachistochrone.ipynb) | Pass | opening exposition strengthened; interactive cell made batch-safe. |
| [python/bregman-flow/bregman-flow.ipynb](python/bregman-flow/bregman-flow.ipynb) | Pass | long computation split pedagogically. |
| [python/brownian/brownian.ipynb](python/brownian/brownian.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/burgers/burgers.ipynb](python/burgers/burgers.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/cellular/cellular.ipynb](python/cellular/cellular.ipynb) | Pass | long computation split pedagogically. |
| [python/chebyshev-minimax/chebyshev-minimax.ipynb](python/chebyshev-minimax/chebyshev-minimax.ipynb) | Pass | opening exposition strengthened; topic bibliography added. |
| [python/compressed-sensing-basis-pursuit/compressed-sensing-basis-pursuit.ipynb](python/compressed-sensing-basis-pursuit/compressed-sensing-basis-pursuit.ipynb) | Pass | opening exposition strengthened; topic bibliography added. |
| [python/conjugate-gradient/conjugate-gradient.ipynb](python/conjugate-gradient/conjugate-gradient.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/de-casteljau/de-casteljau.ipynb](python/de-casteljau/de-casteljau.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/diffusion-models-toy/diffusion-models-toy.ipynb](python/diffusion-models-toy/diffusion-models-toy.ipynb) | Pass | rendering/output placement improved. |
| [python/dijkstra/dijkstra.ipynb](python/dijkstra/dijkstra.ipynb) | Pass | mathematical/warning correction; long computation split pedagogically; outputs made notebook-local. |
| [python/dtw/dtw.ipynb](python/dtw/dtw.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/dykstra/dykstra.ipynb](python/dykstra/dykstra.ipynb) | Pass | long computation split pedagogically. |
| [python/edge-detection/edge-detection.ipynb](python/edge-detection/edge-detection.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/eikonal-fast-marching/eikonal-fast-marching.ipynb](python/eikonal-fast-marching/eikonal-fast-marching.ipynb) | Pass | long computation split pedagogically; outputs made notebook-local. |
| [python/error-diffusion/error-diffusion.ipynb](python/error-diffusion/error-diffusion.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/extreme-values/extreme-values.ipynb](python/extreme-values/extreme-values.ipynb) | Pass | mathematical/warning correction. |
| [python/farthest-point/farthest-point.ipynb](python/farthest-point/farthest-point.ipynb) | Pass | rendering/output placement improved. |
| [python/fem-1d-2d/fem-1d-2d.ipynb](python/fem-1d-2d/fem-1d-2d.ipynb) | Pass | outputs made notebook-local. |
| [python/fixed-point/fixed-point.ipynb](python/fixed-point/fixed-point.ipynb) | Pass | mathematical/warning correction. |
| [python/flocking/flocking.ipynb](python/flocking/flocking.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/floyd-warshall/floyd-warshall.ipynb](python/floyd-warshall/floyd-warshall.ipynb) | Pass | opening exposition strengthened; topic bibliography added; outputs made notebook-local. |
| [python/fluids/fluids.ipynb](python/fluids/fluids.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/fourier-atoms/fourier-atoms.ipynb](python/fourier-atoms/fourier-atoms.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/fourier-cristal/fourier-cristal.ipynb](python/fourier-cristal/fourier-cristal.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/fourier-curves/fourier-curves.ipynb](python/fourier-curves/fourier-curves.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/fourier-matrix/fourier-matrix.ipynb](python/fourier-matrix/fourier-matrix.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/fourier-signal/fourier-signal.ipynb](python/fourier-signal/fourier-signal.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/foveation/foveation.ipynb](python/foveation/foveation.ipynb) | Pass | opening exposition strengthened; topic bibliography added; rendering/output placement improved; interactive cell made batch-safe. |
| [python/frac-der-gaussian/frac-der-gaussian.ipynb](python/frac-der-gaussian/frac-der-gaussian.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/fraction-continued/fraction-continued.ipynb](python/fraction-continued/fraction-continued.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/fractional-laplacian/fractional-laplacian.ipynb](python/fractional-laplacian/fractional-laplacian.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/frank-wolfe/frank-wolfe.ipynb](python/frank-wolfe/frank-wolfe.ipynb) | Pass | rendering/output placement improved; outputs made notebook-local. |
| [python/game-theory/game-theory.ipynb](python/game-theory/game-theory.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/gauss-luca/gauss-luca.ipynb](python/gauss-luca/gauss-luca.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/gaussian-fisher/gaussian-fisher.ipynb](python/gaussian-fisher/gaussian-fisher.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/gaussian-prod-convol/gaussian-prod-convol.ipynb](python/gaussian-prod-convol/gaussian-prod-convol.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/gears-non-circ/gears-non-circ.ipynb](python/gears-non-circ/gears-non-circ.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/geodesic-heat/geodesic-heat.ipynb](python/geodesic-heat/geodesic-heat.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/gershgorin/gershgorin.ipynb](python/gershgorin/gershgorin.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/gibbs-oscillations/gibbs-oscillations.ipynb](python/gibbs-oscillations/gibbs-oscillations.ipynb) | Pass | mathematical/warning correction. |
| [python/gibbs-sampling/gibbs-sampling.ipynb](python/gibbs-sampling/gibbs-sampling.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/grad-desc-mirror/grad-desc-mirror.ipynb](python/grad-desc-mirror/grad-desc-mirror.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/grad-desc-momentum/grad-desc-momentum.ipynb](python/grad-desc-momentum/grad-desc-momentum.ipynb) | Pass | long computation split pedagogically. |
| [python/grad-desc-ode/grad-desc-ode.ipynb](python/grad-desc-ode/grad-desc-ode.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/grad-desc-quad/grad-desc-quad.ipynb](python/grad-desc-quad/grad-desc-quad.ipynb) | Pass | mathematical/warning correction. |
| [python/gradflow-metric/gradflow-metric.ipynb](python/gradflow-metric/gradflow-metric.ipynb) | Pass | opening exposition strengthened; topic bibliography added; outputs made notebook-local. |
| [python/graph-coloring/graph-coloring.ipynb](python/graph-coloring/graph-coloring.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/graph-laplacian/graph-laplacian.ipynb](python/graph-laplacian/graph-laplacian.ipynb) | Pass | opening exposition strengthened. |
| [python/graphical-lasso/graphical-lasso.ipynb](python/graphical-lasso/graphical-lasso.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/gravitation/gravitation.ipynb](python/gravitation/gravitation.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/gromov-wasserstein/gromov-wasserstein.ipynb](python/gromov-wasserstein/gromov-wasserstein.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/haar-walsh/haar-walsh.ipynb](python/haar-walsh/haar-walsh.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/hamiltonian-symplectic/hamiltonian-symplectic.ipynb](python/hamiltonian-symplectic/hamiltonian-symplectic.ipynb) | Pass | outputs made notebook-local. |
| [python/harmonic/harmonic.ipynb](python/harmonic/harmonic.ipynb) | Pass | mathematical/warning correction. |
| [python/heat-1d/heat-1d.ipynb](python/heat-1d/heat-1d.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/heat-polynomials/heat-polynomials.ipynb](python/heat-polynomials/heat-polynomials.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/heat-vs-tv/heat-vs-tv.ipynb](python/heat-vs-tv/heat-vs-tv.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/heavy-ball/heavy-ball.ipynb](python/heavy-ball/heavy-ball.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/hermite-function/hermite-function.ipynb](python/hermite-function/hermite-function.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/hilbert-curve/hilbert-curve.ipynb](python/hilbert-curve/hilbert-curve.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/hist-eq/hist-eq.ipynb](python/hist-eq/hist-eq.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/hmm-forward-backward/hmm-forward-backward.ipynb](python/hmm-forward-backward/hmm-forward-backward.ipynb) | Pass | opening exposition strengthened. |
| [python/holder-inequality/holder-inequality.ipynb](python/holder-inequality/holder-inequality.ipynb) | Pass | mathematical/warning correction. |
| [python/hopfield-network/hopfield-network.ipynb](python/hopfield-network/hopfield-network.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/hump-algebra/hump-algebra.ipynb](python/hump-algebra/hump-algebra.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/ica/ica.ipynb](python/ica/ica.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/icp/icp.ipynb](python/icp/icp.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/integral-lines/integral-lines.ipynb](python/integral-lines/integral-lines.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/interior-points/interior-points.ipynb](python/interior-points/interior-points.ipynb) | Pass | opening exposition strengthened. |
| [python/interpol-vizu/interpol-vizu.ipynb](python/interpol-vizu/interpol-vizu.ipynb) | Pass | opening exposition strengthened. |
| [python/interpolation-natural/interpolation-natural.ipynb](python/interpolation-natural/interpolation-natural.ipynb) | Pass | opening exposition strengthened. |
| [python/interpolation-rkhs/interpolation-rkhs.ipynb](python/interpolation-rkhs/interpolation-rkhs.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/interpolation-shepard/interpolation-shepard.ipynb](python/interpolation-shepard/interpolation-shepard.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/inverse-kinematics/inverse-kinematics.ipynb](python/inverse-kinematics/inverse-kinematics.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/ising-model/ising-model.ipynb](python/ising-model/ising-model.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/ista/ista.ipynb](python/ista/ista.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/iterated-polygons/iterated-polygons.ipynb](python/iterated-polygons/iterated-polygons.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/jko-flow/jko-flow.ipynb](python/jko-flow/jko-flow.ipynb) | Pass | mathematical/warning correction; outputs made notebook-local. |
| [python/joukowski/joukowski.ipynb](python/joukowski/joukowski.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/julia-sets/julia-sets.ipynb](python/julia-sets/julia-sets.ipynb) | Pass | mathematical/warning correction; rendering/output placement improved. |
| [python/k-nn/k-nn.ipynb](python/k-nn/k-nn.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/kaczmarz/kaczmarz.ipynb](python/kaczmarz/kaczmarz.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/kalman/kalman.ipynb](python/kalman/kalman.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/kernel-approx-1d/kernel-approx-1d.ipynb](python/kernel-approx-1d/kernel-approx-1d.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/kernel-pca/kernel-pca.ipynb](python/kernel-pca/kernel-pca.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/kernel-svm/kernel-svm.ipynb](python/kernel-svm/kernel-svm.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/kinetics-evolution/kinetics-evolution.ipynb](python/kinetics-evolution/kinetics-evolution.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/kmean++/kmeanpp.ipynb](python/kmean++/kmeanpp.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/kmeans/kmeans.ipynb](python/kmeans/kmeans.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/kriging/kriging.ipynb](python/kriging/kriging.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/kubo-matrix-mean/kubo-matrix-mean.ipynb](python/kubo-matrix-mean/kubo-matrix-mean.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/lagrange-hermite/lagrange-hermite.ipynb](python/lagrange-hermite/lagrange-hermite.ipynb) | Pass | long computation split pedagogically. |
| [python/lagrangian-flows/lagrangian-flows.ipynb](python/lagrangian-flows/lagrangian-flows.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/lagrangian-vs-eulerian/lagrangian-vs-eulerian.ipynb](python/lagrangian-vs-eulerian/lagrangian-vs-eulerian.ipynb) | Pass | long computation split pedagogically; rendering/output placement improved. |
| [python/laplacian-eigenmaps/laplacian-eigenmaps.ipynb](python/laplacian-eigenmaps/laplacian-eigenmaps.ipynb) | Pass | long computation split pedagogically. |
| [python/laplacian-pyramid/laplacian-pyramid.ipynb](python/laplacian-pyramid/laplacian-pyramid.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/laplacian-spectrum/laplacian-spectrum.ipynb](python/laplacian-spectrum/laplacian-spectrum.ipynb) | Pass | mathematical/warning correction. |
| [python/laplacian-weighted/laplacian-weighted.ipynb](python/laplacian-weighted/laplacian-weighted.ipynb) | Pass | long computation split pedagogically. |
| [python/lda-qda/lda-qda.ipynb](python/lda-qda/lda-qda.ipynb) | Pass | long computation split pedagogically. |
| [python/legendre/legendre.ipynb](python/legendre/legendre.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/level-set-methods/level-set-methods.ipynb](python/level-set-methods/level-set-methods.ipynb) | Pass | opening exposition strengthened. |
| [python/markov-chains-mixing/markov-chains-mixing.ipynb](python/markov-chains-mixing/markov-chains-mixing.ipynb) | Pass | opening exposition strengthened. |
| [python/matrix-completion-nuclear-norm/matrix-completion-nuclear-norm.ipynb](python/matrix-completion-nuclear-norm/matrix-completion-nuclear-norm.ipynb) | Pass | opening exposition strengthened. |
| [python/mean-curvature-flow/mean-curvature-flow.ipynb](python/mean-curvature-flow/mean-curvature-flow.ipynb) | Pass | outputs made notebook-local. |
| [python/newton-fractals-complex/newton-fractals-complex.ipynb](python/newton-fractals-complex/newton-fractals-complex.ipynb) | Pass | opening exposition strengthened. |
| [python/orthogonal-matching-pursuit/orthogonal-matching-pursuit.ipynb](python/orthogonal-matching-pursuit/orthogonal-matching-pursuit.ipynb) | Pass | outputs made notebook-local. |
| [python/pagerank-random-walks/pagerank-random-walks.ipynb](python/pagerank-random-walks/pagerank-random-walks.ipynb) | Pass | opening exposition strengthened. |
| [python/pdhg-chambolle-pock/pdhg-chambolle-pock.ipynb](python/pdhg-chambolle-pock/pdhg-chambolle-pock.ipynb) | Pass | opening exposition strengthened. |
| [python/persistent-homology-topology/persistent-homology-topology.ipynb](python/persistent-homology-topology/persistent-homology-topology.ipynb) | Pass | opening exposition strengthened. |
| [python/poisson-meshes/poisson-meshes.ipynb](python/poisson-meshes/poisson-meshes.ipynb) | Pass | opening exposition strengthened. |
| [python/reaction-diffusion-turing/reaction-diffusion-turing.ipynb](python/reaction-diffusion-turing/reaction-diffusion-turing.ipynb) | Pass | opening exposition strengthened; mathematical/warning correction; rendering/output placement improved. |
| [python/riemannian-optimization-stiefel/riemannian-optimization-stiefel.ipynb](python/riemannian-optimization-stiefel/riemannian-optimization-stiefel.ipynb) | Pass | opening exposition strengthened. |
| [python/robust-pca-lowrank-sparse/robust-pca-lowrank-sparse.ipynb](python/robust-pca-lowrank-sparse/robust-pca-lowrank-sparse.ipynb) | Pass | opening exposition strengthened. |
| [python/schrodinger-bridge/schrodinger-bridge.ipynb](python/schrodinger-bridge/schrodinger-bridge.ipynb) | Pass | opening exposition strengthened. |
| [python/sinkhorn-distance/sinkhorn-distance.ipynb](python/sinkhorn-distance/sinkhorn-distance.ipynb) | Pass | full execution and quality review; no targeted content edit required. |
| [python/sliced-wasserstein/sliced-wasserstein.ipynb](python/sliced-wasserstein/sliced-wasserstein.ipynb) | Pass | mathematical/warning correction; outputs made notebook-local. |
| [python/spectral-graph-wavelets/spectral-graph-wavelets.ipynb](python/spectral-graph-wavelets/spectral-graph-wavelets.ipynb) | Pass | opening exposition strengthened. |
| [python/spherical-harmonics-signals/spherical-harmonics-signals.ipynb](python/spherical-harmonics-signals/spherical-harmonics-signals.ipynb) | Pass | opening exposition strengthened. |
| [python/tsne-umap-comparison/tsne-umap-comparison.ipynb](python/tsne-umap-comparison/tsne-umap-comparison.ipynb) | Pass | opening exposition strengthened. |
| [python/unbalanced-ot/unbalanced-ot.ipynb](python/unbalanced-ot/unbalanced-ot.ipynb) | Pass | opening exposition strengthened. |
| [python/wasserstein-barycenters/wasserstein-barycenters.ipynb](python/wasserstein-barycenters/wasserstein-barycenters.ipynb) | Pass | opening exposition strengthened. |
| [python/wave-equation-dispersion/wave-equation-dispersion.ipynb](python/wave-equation-dispersion/wave-equation-dispersion.ipynb) | Pass | opening exposition strengthened. |

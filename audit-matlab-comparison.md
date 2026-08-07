# Audit of Python Notebooks against MATLAB and Vignettes

Audit date: 2026-08-07.

## Scope and decision rule

The repository currently contains **138** notebooks under `python/`, **332** content directories under `matlab/` (excluding support/result directories), and **806** media entries under `vignettes/`.

A notebook is classified as MATLAB-related when either:

- its directory name exactly matches a MATLAB content directory and that directory contains corresponding `.m` code; or
- its title, equations, algorithm, and experiment clearly match MATLAB material stored under a differently named directory.

The second criterion is intentionally conservative. Generic overlap such as “optimization,” “PCA,” “diffusion,” or “Wasserstein” is not enough. Partial matches are stated explicitly. For the vignette comparison, “video vignette” means an `.m4v` entry; related static `.png` or `.jpeg` entries are mentioned separately but do not count as video matches.

## Summary

| Category | Count |
|---|---:|
| Exact directory/topic match with MATLAB | 107 |
| Renamed or clearly close MATLAB match | 21 |
| No clear MATLAB counterpart, but related to a video vignette | 5 |
| No clear MATLAB counterpart and no clear video-vignette counterpart | 5 |
| **Total notebooks** | **138** |

Thus **128 of 138 notebooks** are clearly related to MATLAB content. The remaining **10** are not clear MATLAB translations or extensions; among those, **5** also lack a clear video-vignette counterpart.

## Exact MATLAB matches

For every entry below, `python/<name>/<notebook>.ipynb` has a matching `matlab/<name>/` directory containing one or more `.m` files on the same topic.

```text
ada-boost
advection
alpha-shapes
apolonian
approximation
arithmetico-geometric
autoregressive
backprojection-radon
bayesian
bernouilli-tcl
bifurcation
bilateral-filtering
boltzmann
brachistochrone
bregman-flow
brownian
burgers
cellular
conjugate-gradient
de-casteljau
dijkstra
dtw
dykstra
edge-detection
error-diffusion
extreme-values
farthest-point
fixed-point
flocking
floyd-warshall
fluids
fourier-atoms
fourier-cristal
fourier-curves
fourier-matrix
fourier-signal
foveation
frac-der-gaussian
fraction-continued
fractional-laplacian
frank-wolfe
game-theory
gauss-luca
gaussian-fisher
gaussian-prod-convol
gears-non-circ
geodesic-heat
gershgorin
gibbs-oscillations
gibbs-sampling
grad-desc-mirror
grad-desc-momentum
grad-desc-ode
grad-desc-quad
gradflow-metric
graph-coloring
graph-laplacian
graphical-lasso
gravitation
gromov-wasserstein
haar-walsh
harmonic
heat-1d
heat-polynomials
heat-vs-tv
heavy-ball
hermite-function
hilbert-curve
hist-eq
holder-inequality
hopfield-network
hump-algebra
ica
icp
integral-lines
interior-points
interpol-vizu
interpolation-natural
interpolation-rkhs
interpolation-shepard
inverse-kinematics
ising-model
ista
iterated-polygons
jko-flow
joukowski
julia-sets
k-nn
kaczmarz
kalman
kernel-approx-1d
kernel-pca
kernel-svm
kinetics-evolution
kmean++
kmeans
kriging
kubo-matrix-mean
lagrange-hermite
lagrangian-flows
lagrangian-vs-eulerian
laplacian-eigenmaps
laplacian-pyramid
laplacian-spectrum
laplacian-weighted
lda-qda
legendre
```

## Renamed or closely related MATLAB matches

These 21 notebooks do not have an identically named MATLAB directory, but the mathematical content clearly matches or extends the indicated MATLAB demo.

| Python notebook | MATLAB counterpart | Assessment |
|---|---|---|
| `chebyshev-minimax` | `runge-phenomenon/` | Same polynomial-interpolation instability; the notebook adds Chebyshev nodes as the remedy. |
| `eikonal-fast-marching` | `fast-marching-2d/` | Direct match: eikonal arrival times and the fast marching algorithm. |
| `hamiltonian-symplectic` | `verlet/` | Directly related particle dynamics and Verlet/leapfrog time integration; the notebook adds the Euler comparison. |
| `hmm-forward-backward` | `viterbi/` | Partial but clear HMM match: both cover latent-state decoding; the notebook additionally develops forward-backward smoothing. |
| `level-set-methods` | `level-sets/` | Direct match in implicit-interface representation and level-set evolution. |
| `markov-chains-mixing` | `markov-simplex/` | Same stochastic-matrix evolution, invariant distribution, contraction, and convergence viewpoint. |
| `mean-curvature-flow` | `meancurv-motion/` | Direct match in curvature-driven curve evolution. |
| `newton-fractals-complex` | `newton-fractal/` | Direct match in Newton basins for complex polynomial roots. |
| `orthogonal-matching-pursuit` | `matching-pursuit/` | Same greedy sparse approximation framework; the notebook uses the orthogonal refitting variant. |
| `pagerank-random-walks` | `page-rank/` | Direct match in PageRank, teleportation, and stationary random walks. |
| `persistent-homology-topology` | `alpha-shapes/BettiNumber.m` | Clear partial match: both track Betti numbers of scale-dependent simplicial complexes; the notebook formulates this as persistence. |
| `poisson-meshes` | `wave-heat-mesh/` and `poisson-fft/` | Clear numerical-PDE overlap: discrete Laplacians and Poisson solves, with the notebook specializing to a triangulated planar mesh. |
| `reaction-diffusion-turing` | `reaction-diffusion/` | Direct match in nonlinear reaction-diffusion pattern formation. |
| `riemannian-optimization-stiefel` | `brokett-flow/` | Clear manifold-optimization match: orthogonality-constrained eigen/PCA objectives and geometric gradient evolution. |
| `schrodinger-bridge` | `schrodinger-dynamic/` | Direct match in Schrödinger interpolation, Brownian priors, and entropic Sinkhorn scaling. |
| `sinkhorn-distance` | `sinkhorn/` | Direct match in entropically regularized optimal transport and matrix scaling. |
| `spherical-harmonics-signals` | `spherical-harmonics/` | Direct match in spherical-harmonic bases and approximation of signals on the sphere. |
| `tsne-umap-comparison` | `t-sne/` | Partial but clear match: the notebook contains a t-SNE-style embedding and broadens the comparison to graph-spectral/UMAP-style ideas. |
| `unbalanced-ot` | `wass-unbalanced/` | Direct match in transport with relaxed mass conservation. |
| `wasserstein-barycenters` | `wass-barycenters/` | Direct match in Wasserstein barycenter construction and interpolation. |
| `wave-equation-dispersion` | `pde-wave-heat-schro/` and `wave-heat/` | Same wave equation and Fourier/time discretization setting; the notebook focuses specifically on numerical dispersion. |

## No clear MATLAB counterpart, but related video vignettes

These five notebooks are not clear ports or close extensions of a MATLAB directory, but they do have a specific related `.m4v` vignette.

| Python notebook | Related video vignette(s) | Relationship |
|---|---|---|
| `admm-first-principles` | `548-lasso.m4v`, `714-basis-pursuit.m4v` | The notebook applies ADMM to the LASSO/sparse-recovery problem shown by the vignettes; no MATLAB ADMM demo was found. |
| `allen-cahn-cahn-hilliard` | `071-reaction-diffusion.m4v`, `711-parabolic-pdes.m4v`, `778-reaction-diffusion.m4v` | Closely related phase-field/parabolic PDE dynamics, but no Allen-Cahn or Cahn-Hilliard MATLAB implementation was found. |
| `compressed-sensing-basis-pursuit` | `714-basis-pursuit.m4v` | Direct topic match in sparse recovery and basis pursuit/LASSO, without a corresponding MATLAB directory. |
| `pdhg-chambolle-pock` | `260-chambolle-tv.m4v` | Closely related primal-dual TV optimization; the notebook uses Chambolle-Pock rather than the older Chambolle projection algorithm. |
| `spectral-graph-wavelets` | `324-spectral-graph.m4v` | Clear overlap in graph-Laplacian spectral filtering; the notebook adds multiscale wavelet kernels. |

## Neither MATLAB-related nor clearly tied to a video vignette

These five notebooks have no clear MATLAB counterpart and no sufficiently specific `.m4v` counterpart.

| Python notebook | Audit note |
|---|---|
| `diffusion-models-toy` | Score-based/DDPM forward and reverse diffusion is not represented by the older diffusion/PDE demos. |
| `fem-1d-2d` | No finite-element assembly or FEM solver was found in MATLAB or in a specific video vignette. |
| `matrix-completion-nuclear-norm` | Existing matrix-factorization/decomposition material does not implement nuclear-norm matrix completion. |
| `robust-pca-lowrank-sparse` | PCA and generic matrix-factorization entries do not cover principal-component pursuit or low-rank-plus-sparse separation. |
| `sliced-wasserstein` | Other Wasserstein entries do not cover random one-dimensional projections or sliced-Wasserstein descent. |

## Borderline cases intentionally excluded from MATLAB matching

- `matrix-completion-nuclear-norm` and `robust-pca-lowrank-sparse` were not matched to `matlab/matrix-decomp/`, because that MATLAB demo visualizes LU, QR, and Cholesky decompositions rather than low-rank convex recovery.
- `sliced-wasserstein` was not matched to generic Wasserstein MATLAB demos because none implements slicing by random projections.

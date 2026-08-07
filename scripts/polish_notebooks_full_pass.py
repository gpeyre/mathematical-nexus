#!/usr/bin/env python3
"""Apply conservative, repeatable quality fixes to the notebook collection."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
CHANGES: dict[str, list[str]] = {}


def note(path: str, message: str) -> None:
    CHANGES.setdefault(path, []).append(message)


def read(path: str):
    return nbformat.read(ROOT / path, as_version=4)


def write(path: str, nb) -> None:
    nbformat.validate(nb)
    nbformat.write(nb, ROOT / path)


def replace_text(path: str, old: str, new: str, message: str) -> None:
    nb = read(path)
    for cell in nb.cells:
        if old in cell.source:
            cell.source = cell.source.replace(old, new)
            write(path, nb)
            note(path, message)
            return
    if new not in "\n".join(cell.source for cell in nb.cells):
        raise ValueError(f"Text not found in {path}: {old[:80]!r}")


def replace_cell(path: str, starts_with: str, new_source: str, message: str) -> None:
    nb = read(path)
    for cell in nb.cells:
        if cell.source.lstrip().startswith(starts_with):
            if cell.source != new_source:
                cell.source = new_source
                if cell.cell_type == "code":
                    cell.outputs = []
                write(path, nb)
                note(path, message)
            return
    if any(cell.source == new_source for cell in nb.cells):
        return
    raise ValueError(f"Cell not found in {path}: {starts_with!r}")


def add_intro(path: str, paragraph: str) -> None:
    nb = read(path)
    for cell in nb.cells:
        if cell.cell_type == "markdown" and cell.source.strip():
            if paragraph not in cell.source:
                cell.source = cell.source.rstrip() + "\n\n" + paragraph.strip() + "\n"
                write(path, nb)
                note(path, "Expanded the opening motivation, governing equation, and reading guide.")
            return
    raise ValueError(f"No opening markdown in {path}")


def add_bibliography(path: str, body: str) -> None:
    nb = read(path)
    prose = "\n".join(cell.source for cell in nb.cells if cell.cell_type == "markdown")
    if re.search(r"^#{1,6}\s+(bibliograph|references|further reading)", prose, re.I | re.M):
        return
    nb.cells.append(nbformat.v4.new_markdown_cell("## Bibliographical resources\n\n" + body.strip()))
    write(path, nb)
    note(path, "Added topic-specific foundational references.")


def tag_interactive(path: str, marker: str) -> None:
    nb = read(path)
    for cell in nb.cells:
        if cell.cell_type == "code" and marker in cell.source:
            tags = list(cell.metadata.get("tags", []))
            if "interactive" not in tags:
                tags.append("interactive")
                cell.metadata["tags"] = tags
                write(path, nb)
                note(path, "Tagged the widget-only explorer as interactive for safe batch execution.")
            return
    raise ValueError(f"Interactive marker not found in {path}: {marker!r}")


def insert_after_markdown(path: str, heading: str, cells_to_insert: list) -> None:
    nb = read(path)
    inserted_sources = {cell.source for cell in cells_to_insert}
    if inserted_sources.issubset({cell.source for cell in nb.cells}):
        return
    for index, cell in enumerate(nb.cells):
        if cell.cell_type == "markdown" and cell.source.lstrip().startswith(heading):
            nb.cells[index + 1 : index + 1] = cells_to_insert
            write(path, nb)
            return
    raise ValueError(f"Markdown insertion point not found in {path}: {heading!r}")


def insert_after_code(path: str, starts_with: str, cells_to_insert: list) -> None:
    nb = read(path)
    inserted_sources = {cell.source for cell in cells_to_insert}
    if inserted_sources.issubset({cell.source for cell in nb.cells}):
        return
    for index, cell in enumerate(nb.cells):
        if cell.cell_type == "code" and cell.source.lstrip().startswith(starts_with):
            nb.cells[index + 1 : index + 1] = cells_to_insert
            write(path, nb)
            return
    raise ValueError(f"Code insertion point not found in {path}: {starts_with!r}")


def split_code_cell(path: str, starts_with: str, splits: list[tuple[str, str]]) -> None:
    nb = read(path)
    for index, cell in enumerate(nb.cells):
        if cell.cell_type != "code" or not cell.source.lstrip().startswith(starts_with):
            continue
        source = cell.source
        if any(markdown in "\n".join(c.source for c in nb.cells) for _, markdown in splits):
            return
        positions = []
        cursor = 0
        for marker, _ in splits:
            position = source.find(marker, cursor)
            if position < 0:
                raise ValueError(f"Split marker not found in {path}: {marker!r}")
            positions.append(position)
            cursor = position + len(marker)
        boundaries = [0, *positions, len(source)]
        code_parts = [source[a:b].strip() for a, b in zip(boundaries[:-1], boundaries[1:])]
        new_cells = []
        for part_index, code in enumerate(code_parts):
            new_code = nbformat.v4.new_code_cell(code)
            if part_index == 0:
                new_code.metadata = copy.deepcopy(cell.metadata)
            new_cells.append(new_code)
            if part_index < len(splits):
                new_cells.append(nbformat.v4.new_markdown_cell(splits[part_index][1]))
        nb.cells[index : index + 1] = new_cells
        write(path, nb)
        note(path, "Split a multi-purpose implementation cell into explained computational substeps.")
        return
    raise ValueError(f"Long code cell not found in {path}: {starts_with!r}")


INTRO_EXPANSIONS = {
    "python/allen-cahn-cahn-hilliard/allen-cahn-cahn-hilliard.ipynb": r"""Both equations decrease the diffuse-interface energy
$$E_\varepsilon(u)=\int_\Omega \frac{\varepsilon}{2}|\nabla u|^2+\frac{1}{\varepsilon}W(u)\,dx,$$
but in different geometries: Allen--Cahn is its $L^2$ gradient flow, whereas Cahn--Hilliard is an $H^{-1}$ flow that conserves total mass. The experiments emphasize this distinction through phase snapshots, energy decay, and coarsening behavior.""",
    "python/arithmetico-geometric/arithmetico-geometric.ipynb": r"""Starting from $a_0,b_0>0$, the iteration
$$a_{n+1}=\frac{a_n+b_n}{2},\qquad b_{n+1}=\sqrt{a_nb_n}$$
preserves the order $b_n\leq a_n$ and drives both sequences to the arithmetic--geometric mean. The plots make the invariant region and the strikingly rapid, essentially quadratic, collapse of the gap $a_n-b_n$ visible.""",
    "python/autoregressive/autoregressive.ipynb": r"""For an AR(2) recurrence, the roots of the characteristic polynomial determine everything: decay, oscillation frequency, and stability. Writing $z_{n+2}=a z_{n+1}+b z_n$ turns the dynamics into a two-dimensional linear map; the visualizations connect its eigenvalues to trajectories and correlation decay.""",
    "python/backprojection-radon/backprojection-radon.ipynb": r"""Tomography measures line integrals
$$\mathcal Rf(\theta,s)=\int_{x\cdot\theta=s}f(x)\,d\ell.$$
Naive backprojection smears each measurement across its acquisition line, while filtered backprojection compensates for the resulting low-frequency bias. The notebook separates acquisition, filtering, and reconstruction so that resolution and artifacts can be interpreted geometrically.""",
    "python/bayesian/bayesian.ipynb": r"""Bayes' rule combines information multiplicatively,
$$p(\theta\mid y)=\frac{p(y\mid\theta)p(\theta)}{\int p(y\mid u)p(u)\,du}.$$
The central question is not only where the posterior mode lies, but how prior location and uncertainty reshape posterior mass. Static comparisons and posterior moments make that tradeoff explicit.""",
    "python/bernouilli-tcl/bernouilli-tcl.ipynb": r"""Repeated convolution is the distributional counterpart of adding independent variables. After centering and scaling $S_n=X_1+\cdots+X_n$ by $\sqrt n$, the central limit theorem predicts convergence toward a Gaussian law. The staged histograms show both the discrete lattice structure and its progressive Gaussian envelope.""",
    "python/bifurcation/bifurcation.ipynb": r"""The logistic map $x_{n+1}=r x_n(1-x_n)$ is a minimal nonlinear system whose long-term behavior ranges from a stable fixed point to periodic cycles and chaos. By discarding transients and plotting the remaining orbit, the bifurcation diagram reveals period doubling and sensitive dependence as the control parameter $r$ varies.""",
    "python/bilateral-filtering/bilateral-filtering.ipynb": r"""The bilateral filter averages pixels using a product of spatial and photometric affinities,
$$w_{ij}\propto e^{-\|i-j\|^2/(2\sigma_s^2)}e^{-|u_i-u_j|^2/(2\sigma_r^2)}.$$
Unlike Gaussian blur, it suppresses mixing across strong edges. The comparisons isolate the roles of $\sigma_s$ and $\sigma_r$ in the smoothing-versus-edge-preservation compromise.""",
    "python/boltzmann/boltzmann.ipynb": r"""A gas-like macroscopic distribution can emerge from deterministic microscopic collisions. Equal-mass elastic impacts preserve total kinetic energy and momentum along the contact normal, while wall reflections preserve speed. The simulation checks overlap, displacement scale, and speed conservation before exposing the motion through optional playback.""",
    "python/brachistochrone/brachistochrone.ipynb": r"""For a graph $y(x)$ under gravity, travel time is the variational functional
$$T[y]=\int\frac{\sqrt{1+y'(x)^2}}{\sqrt{2g(y_0-y(x))}}\,dx.$$
The minimizing curve is a cycloid rather than a straight segment. The numerical comparisons distinguish geometric length from physical travel time and show where the cycloid gains its advantage.""",
    "python/chebyshev-minimax/chebyshev-minimax.ipynb": r"""Polynomial interpolation error depends as much on node placement as on degree. Uniform grids can amplify endpoint oscillations, whereas Chebyshev nodes cluster where the interpolation problem is most ill-conditioned. The experiments compare errors and Lebesgue amplification to explain why minimax-oriented sampling is stable.""",
    "python/compressed-sensing-basis-pursuit/compressed-sensing-basis-pursuit.ipynb": r"""Sparse recovery replaces an underdetermined linear system by the convex program
$$\min_x\frac12\|Ax-y\|_2^2+\lambda\|x\|_1.$$
ISTA alternates a gradient step with soft thresholding. Following the regularization path shows how $\lambda$ controls support size, data fidelity, and the transition from a null estimate to a detailed reconstruction.""",
    "python/floyd-warshall/floyd-warshall.ipynb": r"""Floyd--Warshall is dynamic programming over admissible intermediate vertices. Its recurrence
$$D^{(k)}_{ij}=\min\{D^{(k-1)}_{ij},D^{(k-1)}_{ik}+D^{(k-1)}_{kj}\}$$
builds all-pairs shortest paths in $O(n^3)$ time. Intermediate matrices and reconstructed paths clarify what information each stage adds.""",
    "python/foveation/foveation.ipynb": r"""Visual acuity decreases with eccentricity from the fixation point. We model this by a spatially varying blur scale $\sigma(x)$ that grows with radial distance, then interpolate between Gaussian scale-space levels. Multiple fixation points reveal how local detail is preserved while peripheral content is compressed.""",
    "python/gradflow-metric/gradflow-metric.ipynb": r"""A gradient depends on the geometry used to measure steepness. With a positive-definite metric $G(x)$, the flow becomes
$$\dot x=-G(x)^{-1}\nabla f(x).$$
Although each trajectory decreases the same objective, different metrics precondition directions and change the path and convergence speed. The comparison makes this coordinate dependence visible.""",
    "python/graph-laplacian/graph-laplacian.ipynb": r"""For weighted adjacency $W$ and degree matrix $D$, the graph Laplacian $L=D-W$ satisfies
$$x^\top Lx=\frac12\sum_{i,j}w_{ij}(x_i-x_j)^2.$$
Thus low-frequency eigenvectors vary slowly across strongly connected vertices. The experiments connect this quadratic energy to graph geometry, diffusion, and spectral coordinates.""",
    "python/hmm-forward-backward/hmm-forward-backward.ipynb": r"""A hidden Markov model couples latent transitions with noisy emissions. Forward messages compute filtered evidence, backward messages incorporate future observations, and their product yields smoothed marginals. Viterbi solves a different max-product problem, so comparing the decoded path with posterior probabilities exposes uncertainty that a single path hides.""",
    "python/interior-points/interior-points.ipynb": r"""Interior-point methods replace hard inequalities by a logarithmic barrier. For $Ax\leq b$, one solves
$$\min_x c^\top x-\mu\sum_i\log(b_i-a_i^\top x)$$
while decreasing $\mu$. The central path visualizations connect barrier curvature, Newton steps, feasibility, and convergence toward the boundary optimum.""",
    "python/interpol-vizu/interpol-vizu.ipynb": r"""Two-dimensional interpolation reconstructs a smooth field from samples by choosing a finite-dimensional model and a notion of locality. The notebook compares spline surfaces on a common dataset, making continuity, overshoot, boundary behavior, and sensitivity to sampling density visible rather than judging a method from one curve alone.""",
    "python/interpolation-natural/interpolation-natural.ipynb": r"""Natural-neighbor interpolation derives weights from the Voronoi cells stolen by a query point. These nonnegative, local weights form a partition of unity, reproduce constants, and adapt to irregular geometry. The visualizations contrast the sample tessellation with the resulting smooth interpolant and its boundary behavior.""",
    "python/level-set-methods/level-set-methods.ipynb": r"""An interface is represented implicitly as the zero set of $\phi(x,t)$. Advection obeys
$$\partial_t\phi+v\cdot\nabla\phi=0,$$
while reinitialization restores a signed-distance profile without intentionally moving the zero contour. The experiments track both interface motion and distortion of $|\nabla\phi|$.""",
    "python/markov-chains-mixing/markov-chains-mixing.ipynb": r"""A finite Markov chain evolves distributions by $p_{t+1}=p_tP$. Under irreducibility and aperiodicity, convergence to stationarity is governed by subdominant eigenvalues. The plots compare total-variation decay with spectral predictions, linking graph structure, spectral gap, and mixing time.""",
    "python/matrix-completion-nuclear-norm/matrix-completion-nuclear-norm.ipynb": r"""Matrix completion seeks a low-rank matrix from a subset of entries. Replacing rank by the nuclear norm gives the convex surrogate
$$\min_X\frac12\|P_\Omega(X-M)\|_F^2+\lambda\|X\|_*.$$
Singular-value thresholding then exposes how sampling density and regularization control rank and reconstruction error.""",
    "python/newton-fractals-complex/newton-fractals-complex.ipynb": r"""Newton's iteration $z_{k+1}=z_k-p(z_k)/p'(z_k)$ is locally attracted to simple roots, but its global basins have fractal boundaries. Coloring initial conditions by their limiting root and convergence time turns a root finder into a dynamical system and reveals sensitivity near basin boundaries.""",
    "python/pagerank-random-walks/pagerank-random-walks.ipynb": r"""PageRank is the stationary law of a random walk with teleportation,
$$p=\alpha P^\top p+(1-\alpha)v.$$
Teleportation guarantees a unique stable solution and controls how strongly graph links dominate the personalization vector. Iteration curves and graph views connect centrality to probability flow.""",
    "python/pdhg-chambolle-pock/pdhg-chambolle-pock.ipynb": r"""PDHG addresses saddle problems of the form
$$\min_x\max_y\;G(x)+\langle Kx,y\rangle-F^*(y)$$
with alternating proximal steps. Its stability condition $\tau\sigma\|K\|^2<1$ links step sizes to operator geometry. Objective and residual curves make convergence and instability distinguishable.""",
    "python/persistent-homology-topology/persistent-homology-topology.ipynb": r"""Persistent homology follows topological features across a filtration scale. Birth and death times separate robust components or cycles from short-lived sampling artifacts. The point-cloud, filtration, and barcode views are aligned so the algebraic intervals retain a direct geometric interpretation.""",
    "python/poisson-meshes/poisson-meshes.ipynb": r"""On a triangulated domain, the Poisson equation $-\Delta u=f$ becomes a sparse finite-element system. Piecewise-linear basis functions convert Dirichlet energy into stiffness and mass matrices. Mesh plots, solution fields, and residuals connect the weak formulation to the discrete solver.""",
    "python/reaction-diffusion-turing/reaction-diffusion-turing.ipynb": r"""Gray--Scott dynamics couple diffusion with nonlinear reactions,
$$u_t=D_u\Delta u-uv^2+F(1-u),\qquad v_t=D_v\Delta v+uv^2-(F+k)v.$$
Small perturbations can be amplified into spots or stripes. Temporal snapshots show that pattern selection is a dynamical instability, not a static texture filter.""",
    "python/riemannian-optimization-stiefel/riemannian-optimization-stiefel.ipynb": r"""The Stiefel constraint $X^\top X=I$ is nonlinear, so Euclidean steps leave the feasible set. Riemannian optimization projects gradients onto the tangent space and retracts trial points back to the manifold. Orthogonality error and objective decay verify both geometry and optimization.""",
    "python/robust-pca-lowrank-sparse/robust-pca-lowrank-sparse.ipynb": r"""Robust PCA models data as $M=L+S$, with coherent structure in a low-rank term and gross corruption in a sparse term. Principal component pursuit relaxes this decomposition using $\|L\|_*+\lambda\|S\|_1$. Singular spectra and component images show when the separation is identifiable.""",
    "python/schrodinger-bridge/schrodinger-bridge.ipynb": r"""A Schrodinger bridge finds the most likely stochastic evolution between two endpoint laws relative to a diffusion prior. Entropic regularization turns the problem into iterative scaling, interpolating between diffuse transport and nearly deterministic displacement as the noise level changes.""",
    "python/spectral-graph-wavelets/spectral-graph-wavelets.ipynb": r"""Spectral graph wavelets apply band-pass filters $g(sL)$ to localized impulses. The scale $s$ selects Laplacian frequencies and therefore controls spatial spread across the graph. Comparing scales makes the uncertainty tradeoff between spectral selectivity and vertex localization visible.""",
    "python/spherical-harmonics-signals/spherical-harmonics-signals.ipynb": r"""Spherical harmonics $Y_\ell^m$ diagonalize the Laplace--Beltrami operator on the sphere and provide a Fourier basis for directional data. Degree $\ell$ controls angular frequency. Reconstructions and energy spectra show how truncation smooths a signal and organizes multiscale content.""",
    "python/tsne-umap-comparison/tsne-umap-comparison.ipynb": r"""Both t-SNE and UMAP-style embeddings prioritize neighborhood structure rather than global Euclidean accuracy. Their objectives encode local affinities differently, so apparent clusters must be read alongside trustworthiness and continuity diagnostics. The comparison emphasizes stability across parameters rather than one attractive layout.""",
    "python/unbalanced-ot/unbalanced-ot.ipynb": r"""Unbalanced optimal transport relaxes exact marginal constraints by penalizing mass creation and destruction, often with a Kullback--Leibler divergence. Varying the mass penalty interpolates between local deletion and nearly balanced displacement, revealing when transport is cheaper than changing mass.""",
    "python/wasserstein-barycenters/wasserstein-barycenters.ipynb": r"""A Wasserstein barycenter minimizes $\sum_k\lambda_k W_2^2(\mu,\mu_k)$. In one dimension, quantile functions linearize this geometry, so the barycenter quantile is a weighted average of input quantiles. Weight sweeps reveal displacement interpolation rather than pointwise density blending.""",
    "python/wave-equation-dispersion/wave-equation-dispersion.ipynb": r"""A spatial discretization changes the wave relation from $\omega=c|k|$ to a numerical dispersion law. Consequently, different Fourier modes travel at different phase and group velocities. Comparing dispersion curves with propagated packets explains phase lag and shape distortion before they appear in a simulation.""",
}


BIBLIOGRAPHIES = {
    "python/allen-cahn-cahn-hilliard/allen-cahn-cahn-hilliard.ipynb": """- Allen, S. M. and Cahn, J. W. (1979). A microscopic theory for antiphase boundary motion and its application to antiphase domain coarsening. *Acta Metallurgica*, 27, 1085--1095.
- Cahn, J. W. and Hilliard, J. E. (1958). Free energy of a nonuniform system. I. Interfacial free energy. *Journal of Chemical Physics*, 28, 258--267.
- Bray, A. J. (1994). Theory of phase-ordering kinetics. *Advances in Physics*, 43, 357--459.""",
    "python/chebyshev-minimax/chebyshev-minimax.ipynb": """- Trefethen, L. N. (2013). *Approximation Theory and Approximation Practice*. SIAM.
- Berrut, J.-P. and Trefethen, L. N. (2004). Barycentric Lagrange interpolation. *SIAM Review*, 46, 501--517.
- Cheney, E. W. (1982). *Introduction to Approximation Theory*. AMS Chelsea.""",
    "python/compressed-sensing-basis-pursuit/compressed-sensing-basis-pursuit.ipynb": """- Chen, S. S., Donoho, D. L., and Saunders, M. A. (1998). Atomic decomposition by basis pursuit. *SIAM Journal on Scientific Computing*, 20, 33--61.
- Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. *Journal of the Royal Statistical Society B*, 58, 267--288.
- Beck, A. and Teboulle, M. (2009). A fast iterative shrinkage-thresholding algorithm for linear inverse problems. *SIAM Journal on Imaging Sciences*, 2, 183--202.""",
    "python/floyd-warshall/floyd-warshall.ipynb": """- Floyd, R. W. (1962). Algorithm 97: Shortest path. *Communications of the ACM*, 5, 345.
- Warshall, S. (1962). A theorem on Boolean matrices. *Journal of the ACM*, 9, 11--12.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., and Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.""",
    "python/foveation/foveation.ipynb": """- Burt, P. J. (1988). Smart sensing within a pyramid vision machine. *Proceedings of the IEEE*, 76, 1006--1015.
- Geisler, W. S. and Perry, J. S. (1998). A real-time foveated multiresolution system for low-bandwidth video communication. *SPIE Human Vision and Electronic Imaging III*, 3299.
- Perry, J. S. and Geisler, W. S. (2002). Gaze-contingent real-time simulation of arbitrary visual fields. *SPIE Human Vision and Electronic Imaging VII*, 4662.""",
    "python/gradflow-metric/gradflow-metric.ipynb": """- Ambrosio, L., Gigli, N., and Savare, G. (2008). *Gradient Flows in Metric Spaces and in the Space of Probability Measures*. Birkhauser.
- Jordan, R., Kinderlehrer, D., and Otto, F. (1998). The variational formulation of the Fokker--Planck equation. *SIAM Journal on Mathematical Analysis*, 29, 1--17.
- Santambrogio, F. (2017). Euclidean, metric, and Wasserstein gradient flows: an overview. *Bulletin of Mathematical Sciences*, 7, 87--154.""",
}


for notebook_path, expansion in INTRO_EXPANSIONS.items():
    add_intro(notebook_path, expansion)

SECOND_INTRO_EXPANSIONS = {
    "python/compressed-sensing-basis-pursuit/compressed-sensing-basis-pursuit.ipynb": "The central diagnostic is therefore a three-way balance: residual norm, coefficient sparsity, and support stability. Reading these quantities together prevents a visually plausible reconstruction from being mistaken for a faithful sparse recovery.",
    "python/foveation/foveation.ipynb": "A useful rendering must preserve the fixation neighborhood sharply while changing resolution smoothly enough to avoid visible rings. The parameter comparisons are designed to expose both requirements.",
    "python/gradflow-metric/gradflow-metric.ipynb": "Because objective values alone can hide this geometric effect, the trajectories are drawn on common level sets. Their shapes reveal how preconditioning redirects motion through anisotropic valleys.",
    "python/interpol-vizu/interpol-vizu.ipynb": "All methods are evaluated on identical samples and plotting scales. This common frame makes local smoothness and extrapolation artifacts comparable instead of allowing each method to choose a favorable view.",
    "python/markov-chains-mixing/markov-chains-mixing.ipynb": "The numerical experiment also separates asymptotic rate from short-time behavior. This matters because two chains with similar spectral gaps can still exhibit visibly different transients from a particular initial state.",
    "python/pagerank-random-walks/pagerank-random-walks.ipynb": "We check the fixed-point residual as well as the visual ranking. This ensures that apparent centrality differences reflect the stationary equation rather than insufficient power iterations.",
    "python/persistent-homology-topology/persistent-homology-topology.ipynb": "Scale is treated as a model parameter rather than a cosmetic slider. Stable intervals identify geometry that persists across a range of neighborhoods, whereas short bars signal noise or discretization.",
    "python/poisson-meshes/poisson-meshes.ipynb": "The same triangulation is used to display geometry, forcing, and solution. This alignment makes boundary conditions and local approximation error easier to diagnose.",
    "python/spectral-graph-wavelets/spectral-graph-wavelets.ipynb": "A shared color scale is used across wavelet scales so that apparent localization is quantitative rather than an artifact of independent normalization. The energy distribution complements the vertex-domain view.",
    "python/tsne-umap-comparison/tsne-umap-comparison.ipynb": "No embedding should be judged from appearance alone. Repeated views and neighborhood scores are used to distinguish reproducible local structure from layout-specific visual separation.",
}

for notebook_path, expansion in SECOND_INTRO_EXPANSIONS.items():
    add_intro(notebook_path, expansion)

for notebook_path, expansion in {
    "python/approximation/approximation.ipynb": "A shared coefficient budget and matched display scale make the visual comparison a controlled numerical experiment rather than a qualitative juxtaposition.",
    "python/chebyshev-minimax/chebyshev-minimax.ipynb": "Tracking the error over degree reveals not only which grid wins, but when endpoint instability begins to dominate additional polynomial resolution.",
}.items():
    add_intro(notebook_path, expansion)

for notebook_path, bibliography in BIBLIOGRAPHIES.items():
    add_bibliography(notebook_path, bibliography)


# Standalone image source for foveation.
replace_text(
    "python/foveation/foveation.ipynb",
    "# Foveation on a Cat Image\n\nWe apply eccentricity-dependent blur on a natural cat image resized to $256\\times256$.",
    "# Foveated Image Filtering\n\nWe apply eccentricity-dependent blur to a bundled reference photograph resized to $256\\times256$.",
    "Reframed the title and opening around the general foveation model.",
)
replace_cell(
    "python/foveation/foveation.ipynb",
    "## Load and resize cat image",
    "## Load and resize a bundled reference image\n\nMatplotlib ships a small reference photograph with the library, so the notebook remains self-contained and requires no repository-local data file.",
    "Removed the source-material reference from the image-loading explanation.",
)
replace_cell(
    "python/foveation/foveation.ipynb",
    "from pathlib import Path",
    '''from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.cbook import get_sample_data
from scipy.ndimage import gaussian_filter
from IPython import get_ipython
import ipywidgets as widgets

ip = get_ipython()
if ip is not None:
    ip.run_line_magic("matplotlib", "inline")

OUT = Path(".")
img = mpimg.imread(get_sample_data("grace_hopper.jpg", asfileobj=False)).astype(float)
if img.max() > 1:
    img /= 255.0
img = img[..., :3] if img.ndim == 3 else np.stack([img, img, img], axis=2)
h0, w0, _ = img.shape
ii = np.linspace(0, h0 - 1, 256).astype(int)
jj = np.linspace(0, w0 - 1, 256).astype(int)
img = img[np.ix_(ii, jj)]
H, W, _ = img.shape
Y, X = np.mgrid[0:H, 0:W]
print("shape", img.shape)''',
    "Loaded a single bundled reference image without duplicate imports or external files.",
)

foveation_widget = nbformat.v4.new_code_cell(
    '''def explore_foveation(cx=128, cy=128, radius=64):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(foveate(cx, cy, radius))
    ax.plot(cx, cy, "r+", ms=12, mew=2)
    ax.add_patch(
        plt.Circle((cx, cy), radius, edgecolor="red", facecolor="none", ls="--", lw=1.2)
    )
    ax.set_title(f"fixation=({cx}, {cy}), radius={radius}")
    ax.axis("off")
    plt.show()


widgets.interact(
    explore_foveation,
    cx=widgets.IntSlider(min=0, max=W - 1, value=W // 2, description="x"),
    cy=widgets.IntSlider(min=0, max=H - 1, value=H // 2, description="y"),
    radius=widgets.IntSlider(min=16, max=128, value=64, step=4, description="radius"),
);'''
)
foveation_widget.metadata["tags"] = ["interactive"]
insert_after_markdown(
    "python/foveation/foveation.ipynb",
    "## Interactive fixation/radius explorer",
    [foveation_widget],
)
note("python/foveation/foveation.ipynb", "Added a tagged fixation and foveal-radius slider explorer.")


# Pair the Bayesian posterior formula with both static comparisons and sliders.
bayesian_comparison_text = nbformat.v4.new_markdown_cell(
    r'''## Prior sensitivity at fixed likelihood

For a Gaussian likelihood $\mathcal N(m_\ell,\sigma_\ell^2)$ and prior
$\mathcal N(m_p,\sigma_p^2)$, the posterior is Gaussian with precision and mean

$$
\frac{1}{\sigma_{\mathrm{post}}^2}
=\frac{1}{\sigma_\ell^2}+\frac{1}{\sigma_p^2},
\qquad
m_{\mathrm{post}}
=\sigma_{\mathrm{post}}^2\left(
\frac{m_\ell}{\sigma_\ell^2}+\frac{m_p}{\sigma_p^2}
\right).
$$

The three panels hold the likelihood fixed and vary only the prior. A broad prior
leaves the data dominant; a concentrated prior pulls the posterior toward its mean.'''
)
bayesian_comparison_code = nbformat.v4.new_code_cell(
    r'''prior_settings = [(-1.5, 1.4), (1.2, 0.9), (2.4, 0.65)]
fig, axes = plt.subplots(1, 3, figsize=(13, 3.4), sharex=True, sharey=True,
                         constrained_layout=True)

for ax, (prior_mean, prior_std) in zip(axes, prior_settings):
    prior, post = posterior_from_prior(prior_mean, prior_std)
    ax.plot(t, likelihood, color="crimson", lw=2, label="likelihood")
    ax.plot(t, prior, color="steelblue", lw=2, label="prior")
    ax.fill_between(t, post, color="goldenrod", alpha=0.35, label="posterior")
    ax.set_title(fr"$m_p={prior_mean:.1f}, \sigma_p={prior_std:.2f}$")
    ax.set_xlabel(r"parameter $\theta$")
    ax.grid(alpha=0.2)

axes[0].set_ylabel("density")
axes[0].legend(frameon=False, fontsize=8)
plt.show()'''
)
if any(
    cell.cell_type == "code" and cell.source.lstrip().startswith("prior_settings =")
    for cell in read("python/bayesian/bayesian.ipynb").cells
):
    replace_cell(
        "python/bayesian/bayesian.ipynb",
        "prior_settings =",
        bayesian_comparison_code.source,
        "Normalized the prior-comparison mathtext string.",
    )
insert_after_code(
    "python/bayesian/bayesian.ipynb",
    "def posterior_from_prior",
    [bayesian_comparison_text, bayesian_comparison_code],
)

bayesian_widget = nbformat.v4.new_code_cell(
    '''def explore_prior(prior_mean=1.2, prior_std=0.9):
    prior, post = posterior_from_prior(prior_mean, prior_std)
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(t, likelihood, color="crimson", lw=2, label="likelihood")
    ax.plot(t, prior, color="steelblue", lw=2, label="prior")
    ax.fill_between(t, post, color="goldenrod", alpha=0.4, label="posterior")
    ax.set_xlabel(r"parameter $\theta$")
    ax.set_ylabel("density")
    ax.set_title("Prior-likelihood fusion")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    plt.show()


interact(
    explore_prior,
    prior_mean=FloatSlider(min=-2.0, max=4.0, step=0.1, value=1.2,
                           description="prior mean"),
    prior_std=FloatSlider(min=0.3, max=2.0, step=0.05, value=0.9,
                          description="prior std"),
);'''
)
bayesian_widget.metadata["tags"] = ["interactive"]
insert_after_markdown(
    "python/bayesian/bayesian.ipynb",
    "## Interactive prior influence",
    [bayesian_widget],
)
note("python/bayesian/bayesian.ipynb", "Added a static prior sweep and a tagged slider explorer.")


# Display both Frank-Wolfe diagnostics where they are introduced.
replace_text(
    "python/frank-wolfe/frank-wolfe.ipynb",
    'fig.savefig(OUT / "snippet.png", bbox_inches="tight")\nplt.close(fig)',
    'fig.savefig(OUT / "snippet.png", bbox_inches="tight")\nplt.show()\nplt.close(fig)',
    "Embedded the polytope trajectory comparison beside its derivation.",
)
replace_text(
    "python/frank-wolfe/frank-wolfe.ipynb",
    'ax2.grid(True, which="both", alpha=0.4)',
    'ax2.grid(True, which="both", alpha=0.4)\nplt.show()',
    "Made the convergence rendering explicit and reproducible.",
)


# Warning and mathematical-correctness repairs.
replace_text(
    "python/dijkstra/dijkstra.ipynb",
    'ax.set_title("(b) Distance map $d(s, \\cdot)$", fontsize=9)',
    'ax.set_title(r"(b) Distance map $d(s, \\cdot)$", fontsize=9)',
    "Made the mathtext title a raw string to remove the invalid escape warning.",
)
replace_text(
    "python/fixed-point/fixed-point.ipynb",
    'axes[1].set_xlabel("iteration $n$"); axes[1].set_ylabel("$|f\'(x^*)|^n \\cdot e_0$")',
    'axes[1].set_xlabel("iteration $n$"); axes[1].set_ylabel(r"$|f\'(x^*)|^n \\cdot e_0$")',
    "Made the convergence label a raw string to remove the invalid escape warning.",
)
replace_text(
    "python/holder-inequality/holder-inequality.ipynb",
    "label = f'$p={p:.1f},\\ q={q:.2f}$'",
    "label = fr'$p={p:.1f},\\ q={q:.2f}$'",
    "Made the conjugate-exponent label a raw f-string.",
)
replace_text(
    "python/harmonic/harmonic.ipynb",
    "levels=10, colors='k',   lw=0.7, alpha=0.5",
    "levels=10, colors='k', linewidths=0.7, alpha=0.5",
    "Corrected the Matplotlib contour linewidth keyword.",
)
replace_text(
    "python/laplacian-spectrum/laplacian-spectrum.ipynb",
    "T = diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')",
    "T = diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(n, n), format='csr', dtype=float)",
    "Made the finite-difference Laplacian dtype explicit and future-proof.",
)
replace_text(
    "python/sliced-wasserstein/sliced-wasserstein.ipynb",
    'cmap = cm.get_cmap("coolwarm")',
    'cmap = plt.get_cmap("coolwarm")',
    "Replaced the deprecated colormap accessor.",
)
replace_text(
    "python/jko-flow/jko-flow.ipynb",
    'label=f"$m={m},\\ t={t_s:.4f}$"',
    'label=fr"$m={m},\\ t={t_s:.4f}$"',
    "Made the interactive time label a raw f-string.",
)
replace_text(
    "python/reaction-diffusion-turing/reaction-diffusion-turing.ipynb",
    'fig, axes = plt.subplots(1, len(snap_ids), figsize=(12.5, 3.2))',
    'fig, axes = plt.subplots(1, len(snap_ids), figsize=(12.5, 3.2), layout="constrained")',
    "Used constrained layout for the multi-panel Turing-pattern figure.",
)
replace_text(
    "python/reaction-diffusion-turing/reaction-diffusion-turing.ipynb",
    "plt.tight_layout()\nfig.savefig(OUTPUT_DIR / \"snippet.png\"",
    "fig.savefig(OUTPUT_DIR / \"snippet.png\"",
    "Removed the incompatible tight-layout call.",
)


replace_cell(
    "python/extreme-values/extreme-values.ipynb",
    "def gev_cdf",
    '''def gev_cdf(x, xi):
    """GEV CDF with shape xi (location 0, scale 1)."""
    return genextreme.cdf(np.asarray(x, dtype=float), c=-xi)


def gev_pdf(x, xi):
    """GEV PDF; SciPy uses the opposite shape convention c = -xi."""
    return genextreme.pdf(np.asarray(x, dtype=float), c=-xi)


print("GEV functions ready (SciPy shape convention c = -xi).")''',
    "Replaced eager piecewise powers by SciPy's support-aware GEV implementation.",
)
replace_text(
    "python/extreme-values/extreme-values.ipynb",
    "import matplotlib.cm as cm",
    "import matplotlib.cm as cm\nfrom scipy.stats import genextreme",
    "Imported the numerically robust GEV distribution implementation.",
)

replace_text(
    "python/grad-desc-quad/grad-desc-quad.ipynb",
    """        g = A @ x
        tau = np.dot(g, g) / np.dot(g, A @ g)
        x = x - tau * g
        fvals.append(0.5*(mu*x[0]**2 + L*x[1]**2))""",
    """        g = A @ x
        grad_sq = np.dot(g, g)
        if grad_sq <= np.finfo(float).eps:
            fvals.extend([fvals[-1]] * (n_iter - len(fvals) + 1))
            break
        tau = grad_sq / np.dot(g, A @ g)
        x = x - tau * g
        fvals.append(0.5*(mu*x[0]**2 + L*x[1]**2))""",
    "Stopped exact line search cleanly once the quadratic gradient reaches machine precision.",
)

replace_cell(
    "python/julia-sets/julia-sets.ipynb",
    "def mandelbrot_escape",
    '''def mandelbrot_escape(n=300, n_iter=100, xlim=(-2.5, 1.0), ylim=(-1.3, 1.3)):
    tx = np.linspace(*xlim, n)
    ty = np.linspace(*ylim, n)
    Y, X = np.meshgrid(ty, tx)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    escape = np.full(C.shape, n_iter, dtype=float)
    escaped = np.zeros(C.shape, dtype=bool)
    for iteration in range(1, n_iter + 1):
        Z = Z**2 + C
        mask = (~escaped) & (np.abs(Z) >= 2)
        escape[mask] = iteration
        escaped |= mask
        Z[escaped] = 2.0
    return escape


M = mandelbrot_escape(n=300, n_iter=100)
c_inside = -0.5 + 0.5j
c_outside = -1.5 + 0j
c_boundary = -0.75225 + 0.1j
julia_cases = [
    (c_inside, r"$c \\in \\mathcal{M}$ (connected)", "inferno"),
    (c_outside, r"$c \\notin \\mathcal{M}$ (dust)", "plasma"),
    (c_boundary, "Near boundary", "hot"),
]

fig, axes = plt.subplots(1, 4, figsize=(14, 4), layout="constrained")
axes[0].imshow(
    np.log1p(M).T,
    cmap="Blues_r",
    origin="lower",
    extent=[-2.5, 1.0, -1.3, 1.3],
    aspect="equal",
)
for c_point, color in [(c_inside, "r"), (c_outside, "g"), (c_boundary, "y")]:
    axes[0].plot(c_point.real, c_point.imag, f"{color}*", ms=14)
axes[0].set_title("Mandelbrot set", fontsize=11)

for ax, (c_point, label, cmap_name) in zip(axes[1:], julia_cases):
    escape = julia_escape(c_point, n=200, n_iter=80)
    ax.imshow(np.log1p(escape).T, cmap=cmap_name, origin="lower", aspect="equal")
    ax.set_title(label, fontsize=9)
    ax.axis("off")

fig.savefig("julia_mandelbrot.png", dpi=100, bbox_inches="tight")
plt.show()''',
    "Rebuilt the Mandelbrot/Julia comparison on one consistent four-column layout.",
)


# Correct the Gibbs normalization for a unit-height box and avoid sin(0)/0.
gibbs_path = "python/gibbs-oscillations/gibbs-oscillations.ipynb"
nb = read(gibbs_path)
opening = nb.cells[0].source
old_gibbs = """For the step function $f(x) = \\mathbf{1}_{x > 0} - \\mathbf{1}_{x < 0}$ on $[-1/2, 1/2]$, the maximum of $f_N$ near $x = 0$ converges to
$$
\\lim_{N \\to \\infty} \\max_x f_N(x) = \\frac{2}{\\pi} \\int_0^\\pi \\frac{\\sin t}{t}\\, dt \\approx 1.178979\\ldots
$$
This is approximately $9\\%$ larger than the actual jump height of $1$. This $\\approx 9\\%$ overshoot **does not decrease** as $N \\to \\infty$ — the oscillation only compresses toward $x_0$, but its amplitude remains fixed."""
new_gibbs = """For the sign step $f(x)=\\mathbf{1}_{x>0}-\\mathbf{1}_{x<0}$, the limiting peak is
$$
\\frac{2}{\\pi}\\int_0^\\pi\\frac{\\sin t}{t}\\,dt\\approx1.178979.
$$
The excess above the upper plateau is $0.178979$, which is $8.949\\%$ of the jump size $2$. For the unit-height box used below, linear rescaling gives the limiting peak
$$
G=\\frac12+\\frac{1}{\\pi}\\int_0^\\pi\\frac{\\sin t}{t}\\,dt\\approx1.089490.
$$
The overshoot does not disappear as $N\\to\\infty$; only its spatial width shrinks toward the discontinuity."""
if old_gibbs in opening:
    nb.cells[0].source = opening.replace(old_gibbs, new_gibbs)
    note(gibbs_path, "Corrected the Gibbs overshoot normalization for sign and unit-height jumps.")
nb.cells[7].source = """## Maximum overshoot vs $N$

For the unit-height box, the asymptotic peak is
$$
G=\\frac12+\\frac{1}{\\pi}\\operatorname{Si}(\\pi)\\approx1.089490.
$$
We estimate the peak over increasing bandwidth and compare it with this limit."""
nb.cells[8].source = '''sample = np.linspace(0.0, np.pi, 10001)
si_pi = np.trapezoid(np.sinc(sample / np.pi), sample)
gibbs_limit = 0.5 + si_pi / np.pi
print(f"Unit-step Gibbs peak: {gibbs_limit:.6f}")

N_range = np.unique(np.round(np.logspace(0.4, 3, 60)).astype(int))
maxvals = []
for N in N_range:
    fN = fourier_partial_sum(f_box, N)
    maxvals.append(np.max(fN))

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.semilogx(N_range, maxvals, "b-o", ms=3, lw=2, label=r"$\\max f_N$")
ax.axhline(
    gibbs_limit,
    color="r",
    lw=1.5,
    ls="--",
    label=fr"unit-step limit $\\approx {gibbs_limit:.4f}$",
)
ax.axhline(1.0, color="gray", lw=1, ls=":", label="upper plateau")
ax.set_xlabel(r"$N$ (bandwidth)")
ax.set_ylabel(r"$\\max f_N$")
ax.set_title("Maximum overshoot converges to the Gibbs limit")
ax.legend(fontsize=9)
ax.grid(alpha=0.3, which="both")
plt.tight_layout()
plt.show()'''
nb.cells[8].outputs = []
write(gibbs_path, nb)
note(gibbs_path, "Removed the removable sin(0)/0 singularity in the Gibbs-limit computation.")


# Ensure intermediate numerical figures are displayed before closing them.
for cell_start in ("fig1, axes1", "t_norm  =", "bwd_lbls =", "seg_col_b ="):
    path = "python/diffusion-models-toy/diffusion-models-toy.ipynb"
    nb = read(path)
    for cell in nb.cells:
        if cell.cell_type == "code" and cell.source.lstrip().startswith(cell_start):
            if "plt.close(" in cell.source and "plt.show()\nplt.close(" not in cell.source:
                cell.source = cell.source.replace("plt.close(", "plt.show()\nplt.close(")
                write(path, nb)
                note(path, "Embedded an intermediate forward/backward diffusion figure near its computation.")
            break

for cell_start in ("N1 = 2000", "n2 = 200", "# Build weight image"):
    path = "python/farthest-point/farthest-point.ipynb"
    nb = read(path)
    for cell in nb.cells:
        if cell.cell_type == "code" and cell.source.lstrip().startswith(cell_start):
            old = "plt.close(fig)\nplt.show()"
            if old in cell.source:
                cell.source = cell.source.replace(old, "plt.show()\nplt.close(fig)")
                write(path, nb)
                note(path, "Restored a progressive farthest-point figure as an embedded output.")
            break

replace_text(
    "python/boltzmann/boltzmann.ipynb",
    "import numpy as np",
    "import os\nimport numpy as np",
    "Added a standard batch-execution environment check.",
)
replace_text(
    "python/boltzmann/boltzmann.ipynb",
    "STATIC_SNAPSHOT = False",
    'STATIC_SNAPSHOT = os.environ.get("NBEXECUTE") == "1"',
    "Enabled the static particle snapshot only during reproducible batch execution.",
)


# Notebook-local output paths, independent of the caller's working directory.
for path, old in {
    "python/eikonal-fast-marching/eikonal-fast-marching.ipynb": 'OUT = Path("python/eikonal-fast-marching"); OUT.mkdir(parents=True, exist_ok=True)',
    "python/floyd-warshall/floyd-warshall.ipynb": 'OUT = Path("python/floyd-warshall"); OUT.mkdir(parents=True, exist_ok=True)',
    "python/gradflow-metric/gradflow-metric.ipynb": 'OUT = Path("python/gradflow-metric"); OUT.mkdir(parents=True, exist_ok=True)',
    "python/frank-wolfe/frank-wolfe.ipynb": 'OUT = Path("python/frank-wolfe"); OUT.mkdir(parents=True, exist_ok=True)',
    "python/hamiltonian-symplectic/hamiltonian-symplectic.ipynb": 'OUTPUT_DIR = Path("python/hamiltonian-symplectic")\nOUTPUT_DIR.mkdir(parents=True, exist_ok=True)',
    "python/sliced-wasserstein/sliced-wasserstein.ipynb": 'OUT = Path("python/sliced-wasserstein")\nOUT.mkdir(parents=True, exist_ok=True)',
    "python/jko-flow/jko-flow.ipynb": 'OUT = Path("python/jko-flow")\nOUT.mkdir(parents=True, exist_ok=True)',
    "python/dijkstra/dijkstra.ipynb": 'OUT = Path("python/dijkstra")\nOUT.mkdir(parents=True, exist_ok=True)',
    "python/orthogonal-matching-pursuit/orthogonal-matching-pursuit.ipynb": 'OUT = Path("python/orthogonal-matching-pursuit")\nOUT.mkdir(parents=True, exist_ok=True)',
    "python/fem-1d-2d/fem-1d-2d.ipynb": 'OUT = Path("python/fem-1d-2d")\nOUT.mkdir(parents=True, exist_ok=True)',
    "python/mean-curvature-flow/mean-curvature-flow.ipynb": 'OUT = Path("python/mean-curvature-flow")\nOUT.mkdir(parents=True, exist_ok=True)',
}.items():
    variable = "OUTPUT_DIR" if old.startswith("OUTPUT_DIR") else "OUT"
    replace_text(path, old, f'{variable} = Path(".")', "Redirected persistent figures to the notebook's own directory.")


tag_interactive("python/approximation/approximation.ipynb", "interact(compare_budget")
tag_interactive("python/brachistochrone/brachistochrone.ipynb", "interact(show_time")


# Split long cells at genuine conceptual boundaries.
split_code_cell(
    "python/bregman-flow/bregman-flow.ipynb",
    "A = np.array",
    [("# Mirror descent on a linear objective", r"""## Entropic mirror descent on the simplex

For a linear objective $\langle c,x\rangle$ on the probability simplex, the entropy mirror map gives the multiplicative update
$$x_i^{k+1}\propto x_i^k e^{-\eta c_i}.$$
This second experiment isolates that geometry from the preceding continuous trajectories.""")],
)
split_code_cell(
    "python/cellular/cellular.ipynb",
    "def gol_step",
    [
        ("# ── Canonical patterns", "## Canonical finite patterns\n\nWe encode still lifes, oscillators, spaceships, and a long transient as small binary templates before placing them on the torus."),
        ("# ── Demonstration grid", "## Simultaneous evolution\n\nAll templates are evolved by the same local rule. Snapshots at separated times distinguish translation, periodicity, invariance, and transient complexity."),
    ],
)
split_code_cell(
    "python/dijkstra/dijkstra.ipynb",
    "from pathlib import Path",
    [
        ("# ── General graph Dijkstra", r"""## Dijkstra on an adjacency list

The priority queue always extracts the unsettled vertex with smallest tentative distance. Relaxing an edge $(u,v)$ applies
$$d(v)\leftarrow\min\{d(v),d(u)+w_{uv}\}."""),
        ("# ── Grid Dijkstra", r"""## Weighted grid specialization

A four-neighbor grid is a graph whose edge cost is the average cost of adjacent cells. Parent pointers retain the minimizing discrete geodesic."""),
    ],
)
split_code_cell(
    "python/dijkstra/dijkstra.ipynb",
    "# Hand-crafted graph",
    [("# Show three target paths side by side", "## Read several shortest paths\n\nUsing one source solve, we reconstruct paths to three targets and highlight both cumulative distance labels and the selected predecessor chain.")],
)
split_code_cell(
    "python/dijkstra/dijkstra.ipynb",
    "def build_maze",
    [
        ("nm = 61", "## Solve on a recursive maze\n\nWalls receive infinite cost, so Dijkstra explores only the free subgraph and parent pointers encode a winding feasible route."),
        ("# ── Plot", "## Maze distance and geodesic\n\nThe distance map displays the full value function, while the overlaid path is one minimizing backtrack from destination to source."),
    ],
)
split_code_cell(
    "python/dykstra/dykstra.ipynb",
    "def run_pocs",
    [
        ("# Sets: disk", "## Projection geometry\n\nWe compare a disk with a half-space, define their projectors, and choose several starting points outside the intersection."),
        ("fig, axes", "## Alternating projections versus Dykstra corrections\n\nThe trajectories show that Dykstra's residual corrections recover the Euclidean projection onto the intersection rather than merely a feasible point."),
    ],
)
split_code_cell(
    "python/grad-desc-momentum/grad-desc-momentum.ipynb",
    "def run_gd",
    [("# Compare for several condition numbers", r"""## Compare methods across conditioning

For each $\kappa=L/\mu$, we compare objective decay with the characteristic factors $(\kappa-1)/(\kappa+1)$ and $(\sqrt\kappa-1)/(\sqrt\kappa+1)$.""")],
)


# Factor the Godunov update out of the Fast Marching queue loop.
replace_cell(
    "python/eikonal-fast-marching/eikonal-fast-marching.ipynb",
    "def run_fmm",
    '''def godunov_update(T, F, i, j, h):
    """Solve the local two-dimensional upwind quadratic at node (i, j)."""
    n, m = T.shape
    a = min(T[i - 1, j] if i > 0 else np.inf,
            T[i + 1, j] if i + 1 < n else np.inf)
    b = min(T[i, j - 1] if j > 0 else np.inf,
            T[i, j + 1] if j + 1 < m else np.inf)
    h_over_f = h / F[i, j]
    if np.isinf(a) and np.isinf(b):
        return np.inf
    if np.isinf(a):
        return b + h_over_f
    if np.isinf(b):
        return a + h_over_f
    if abs(a - b) >= h_over_f:
        return min(a, b) + h_over_f
    discriminant = 2.0 * h_over_f**2 - (a - b)**2
    return 0.5 * (a + b + np.sqrt(max(discriminant, 0.0)))


def run_fmm(F, src, h, n, marks):
    """Accept nodes in increasing arrival time and retain front snapshots."""
    T = np.full((n, n), np.inf)
    visited = np.zeros((n, n), dtype=bool)
    T[src] = 0.0
    queue = [(0.0, src[0], src[1])]
    snapshots = {}
    marks = set(marks)

    while queue:
        _, i, j = heapq.heappop(queue)
        if visited[i, j]:
            continue
        visited[i, j] = True
        count = int(visited.sum())
        if count in marks:
            snapshots[count] = visited.copy()
        if marks and count >= max(marks) and len(snapshots) == len(marks):
            break
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ii, jj = i + di, j + dj
            if not (0 <= ii < n and 0 <= jj < n) or visited[ii, jj]:
                continue
            candidate = godunov_update(T, F, ii, jj, h)
            if candidate < T[ii, jj]:
                T[ii, jj] = candidate
                heapq.heappush(queue, (candidate, ii, jj))
    return T, visited, snapshots, int(visited.sum())''',
    "Factored the Godunov update from the Fast Marching queue loop.",
)
replace_cell(
    "python/eikonal-fast-marching/eikonal-fast-marching.ipynb",
    "T, vis, snaps, cnt",
    '''T, vis, snaps, cnt = run_fmm(F, src, h, n, marks)

print(f"FMM done. Nodes accepted: {cnt}")
print(f"T at destination: {T[dst]:.4f}")
finite = T[np.isfinite(T)]
print(f"T range (finite): [{finite.min():.3f}, {finite.max():.3f}]")
print(f"Snapshots captured: {sorted(snaps)}")''',
    "Restored a clean execution cell for the factored Fast Marching solver.",
)
split_code_cell(
    "python/lagrange-hermite/lagrange-hermite.ipynb",
    "def hermite_interp",
    [
        ("# Compare: Lagrange", "## Match polynomial degree fairly\n\nHermite uses values and derivatives at fewer nodes; Lagrange uses values at twice as many nodes so both interpolants have comparable degree."),
        ("fig, axes", "## Compare approximants and maximum error\n\nA common vertical scale makes endpoint oscillation and global error directly comparable."),
    ],
)
split_code_cell(
    "python/laplacian-eigenmaps/laplacian-eigenmaps.ipynb",
    "def build_laplacian",
    [("def laplacian_eigenmaps", r"""## Extract nontrivial spectral coordinates

After diagonalizing $L_{\mathrm{sym}}$, we discard the constant mode and map normalized eigenvectors back through $D^{-1/2}$.""")],
)
split_code_cell(
    "python/laplacian-weighted/laplacian-weighted.ipynb",
    "def weighted_laplacian_2d",
    [("n2d = 30", r"""## Compare two-dimensional weight fields

Uniform, localized, and stripe-shaped conductivities produce different eigenvalues and mode localization. We solve the same sparse eigenproblem for all three fields.""")],
)
split_code_cell(
    "python/lda-qda/lda-qda.ipynb",
    "def fisher_lda",
    [
        ("evals_f, evecs_f", r"""## Compute Fisher coordinates

The leading generalized eigenvectors maximize between-class variance relative to within-class variance. We project the data onto the two dominant directions."""),
        ("fig, axes", "## Interpret the discriminant projection\n\nThe original-space arrows and the projected class histograms show geometry and separation in complementary coordinates."),
    ],
)
# The long static render is cohesive, but isolate its invocation from its definition.
lag_path = "python/lagrangian-vs-eulerian/lagrangian-vs-eulerian.ipynb"
nb = read(lag_path)
has_static_renderer = any(
    cell.cell_type == "code" and cell.source.startswith("def render_static_comparison")
    for cell in nb.cells
)
if not has_static_renderer:
    for index, cell in enumerate(nb.cells):
        if cell.cell_type == "code" and cell.source.startswith("STATIC_SNAPSHOT = True"):
            lines = cell.source.splitlines()[3:]
            body = [line[4:] if line.startswith("    ") else line for line in lines]
            function_source = "def render_static_comparison():\n" + "\n".join(
                "    " + line if line else "" for line in body
            )
            nb.cells[index : index + 1] = [
                nbformat.v4.new_code_cell(function_source),
                nbformat.v4.new_markdown_cell(
                    "## Reproducible static comparison\n\n"
                    "The static fallback combines Eulerian streamlines, one Lagrangian tracer snapshot, "
                    "and final patch deformation without invoking the interactive controls."
                ),
                nbformat.v4.new_code_cell(
                    "STATIC_SNAPSHOT = True\n\nif STATIC_SNAPSHOT:\n    render_static_comparison()"
                ),
            ]
            write(lag_path, nb)
            note(lag_path, "Separated the long static renderer from its reproducible invocation.")
            break

nb = read(lag_path)
recursive_source = "def render_static_comparison():\n    render_static_comparison()"
cleaned_cells = [cell for cell in nb.cells if cell.source != recursive_source]
deduplicated = []
for cell in cleaned_cells:
    if (
        deduplicated
        and cell.cell_type == "markdown"
        and deduplicated[-1].cell_type == "markdown"
        and cell.source == deduplicated[-1].source
    ):
        continue
    deduplicated.append(cell)
if len(deduplicated) != len(nb.cells):
    nb.cells = deduplicated
    write(lag_path, nb)
    note(lag_path, "Removed duplicate wrapper cells introduced during static-render refactoring.")


Path("/private/tmp/nexus-polish-changes.json").write_text(
    json.dumps(CHANGES, indent=2, ensure_ascii=False), encoding="utf-8"
)
print(f"Updated {len(CHANGES)} notebooks with {sum(map(len, CHANGES.values()))} targeted changes.")

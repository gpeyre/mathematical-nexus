#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
PYTHON_DIR = ROOT / "python"
VIGNETTES_DIR = ROOT / "vignettes"
README = ROOT / "README.md"
MYDATA = VIGNETTES_DIR / "mydata.js"

DB_XLSX = ROOT / "database.xlsx"
DB_JSON = ROOT / "database.json"
DB_JS = ROOT / "database.js"


@dataclass
class Row:
    title: str
    content: str
    filename: str
    type: str
    related_notebook: str = ""


TITLE_STOP_WORDS = {
    "a",
    "an",
    "and",
    "by",
    "for",
    "from",
    "in",
    "of",
    "on",
    "the",
    "to",
    "via",
    "vs",
    "with",
}


# Filename stems are terse archival identifiers. These overrides expand the
# most opaque or ambiguous ones while keeping card titles compact.
VIGNETTE_TITLE_OVERRIDES = {
    "1d-dicrepancies": "One-Dimensional Probability Discrepancies",
    "a-trou": "A-Trous Wavelet Transform",
    "alex-net": "AlexNet Convolutional Network",
    "aniso-diffusion": "Anisotropic Diffusion",
    "approx-quantiz": "Approximation by Quantization",
    "arith-geom": "Arithmetic-Geometric Means",
    "assignement-pbm": "Assignment Problem",
    "astar": "A-Star Shortest-Path Search",
    "backprop": "Reverse-Mode Backpropagation",
    "barron": "Barron Approximation Rates",
    "barycoord": "Generalized Barycentric Coordinates",
    "bb-steps": "Barzilai-Borwein Step Sizes",
    "beckmann": "Beckmann Transport Formulation",
    "brenier": "Brenier Optimal Transport Theorem",
    "brownian": "Brownian Motion",
    "burger": "Burgers Shock Equation",
    "cas": "Hartley CAS Transform",
    "cfl": "CFL Stability Condition",
    "cizar": "Csiszar Divergences",
    "conformal": "Conformal Maps",
    "dikstra": "Dijkstra Shortest Paths",
    "dct": "Discrete Cosine Transform",
    "diffeo": "Flow-Generated Diffeomorphisms",
    "dublin": "Dubins Car Paths",
    "eikonale": "Eikonal Distance Equation",
    "eigenfaces": "Eigenfaces and PCA",
    "ellastic-net": "Elastic Net Regularization",
    "fields": "Electric and Magnetic Fields",
    "filtering": "Iterated Convolution Filtering",
    "fastmarching": "Fast Marching Method",
    "fineup": "Fienup Phase Retrieval",
    "fisher-rao": "Fisher-Rao Geometry",
    "fixedpoints": "Fixed-Point Dynamics",
    "foveation": "Foveated Image Filtering",
    "gabor": "Gabor Time-Frequency Atoms",
    "gasket": "Apollonian Gasket",
    "focuss": "FOCUSS Sparse Recovery",
    "fp-sampling": "Farthest-Point Sampling",
    "fw": "Frank-Wolfe Optimization",
    "gsm": "Gaussian Scale Mixtures",
    "hamming": "Hamming Error-Correcting Codes",
    "harris": "Harris Corner Detection",
    "huber": "Huber Robust Estimation",
    "hypercube": "High-Dimensional Hypercube",
    "implicitexplicit": "Explicit vs Implicit Descent",
    "isomap": "Isomap Manifold Embedding",
    "jko": "JKO Wasserstein Flow",
    "jpeg2k": "JPEG 2000 Wavelet Coding",
    "joukowski": "Joukowski Airfoil Transform",
    "julia": "Julia Fractal Sets",
    "kanitza": "Kanizsa Illusory Contours",
    "kerner": "Durand-Kerner Root Finding",
    "kubo-ando": "Kubo-Ando Matrix Means",
    "kuboando": "Kubo-Ando Matrix Means",
    "krigging": "Kriging with Gaussian Processes",
    "kringing": "Kriging with Gaussian Processes",
    "kmeans-plusplus": "K-Means++ Initialization",
    "kmeans-pp": "K-Means++ Initialization",
    "lattice": "Lattice Order Geometry",
    "lasso": "Lasso Sparse Regression",
    "leapfrog": "Leapfrog Symplectic Integration",
    "linsystems": "Linear Systems and Least Squares",
    "lotka": "Lotka-Volterra Dynamics",
    "lic": "Line Integral Convolution",
    "lll": "LLL Lattice Reduction",
    "lojasiewicz": "Kurdyka-Lojasiewicz Geometry",
    "lyapounov": "Lyapunov Stability Functions",
    "mar-pastur": "Marchenko-Pastur Law",
    "marr": "Marr-Hildreth Edge Detection",
    "maxcut": "MAX-CUT Semidefinite Relaxation",
    "mccann": "McCann Displacement Interpolation",
    "mle": "Maximum Likelihood Estimation",
    "metaballs": "Metaball Level Sets",
    "monge": "Monge Optimal Assignment",
    "monotone": "Monotone Operators",
    "moreau": "Moreau Envelope",
    "motzkin": "Motzkin Positive Polynomial",
    "multigrid": "Multigrid PDE Solver",
    "multipole": "Fast Multipole Interactions",
    "nlmeans": "Non-Local Means Denoising",
    "nl-means": "Non-Local Means Denoising",
    "nphard": "NP-Hardness and Completeness",
    "pagerank": "PageRank Random Walks",
    "parzen": "Parzen Kernel Density Estimation",
    "pendulum": "Nonlinear Pendulum Dynamics",
    "qr": "QR Matrix Factorization",
    "randommatrices": "Classical Random Matrix Laws",
    "rbf": "Radial Basis Functions",
    "rbf-nn": "RBF Neural Networks",
    "rkhs": "Reproducing Kernel Hilbert Spaces",
    "rosenbrok": "Rosenbrock Optimization Landscape",
    "schrodinger": "Schrodinger Bridge Transport",
    "sgd": "Stochastic Gradient Descent",
    "shannon": "Shannon Sampling Theorem",
    "shapeley": "Shapley-Folkman Convexification",
    "smacoff": "SMACOF Multidimensional Scaling",
    "sketching": "Random-Feature Kernel Sketching",
    "sobol": "Sobol Quasi-Monte Carlo",
    "softmax": "Softmax and Log-Sum-Exp",
    "som": "Self-Organizing Maps",
    "spirals": "String-Art Logarithmic Spirals",
    "ssim": "Structural Similarity Index",
    "stft": "Short-Time Fourier Transform",
    "sunflower": "Golden-Angle Sunflower Spirals",
    "sunflowers": "Golden-Angle Sunflower Spirals",
    "svd": "Singular Value Decomposition",
    "svm": "Support Vector Machines",
    "tcl": "Central Limit Theorem",
    "tarski": "Tarski Projection Theorem",
    "tsne": "t-SNE Dimensionality Reduction",
    "tsp": "Traveling Salesman Problem",
    "tv-denoise": "Total Variation Denoising",
    "verlet": "Verlet Symplectic Integration",
    "washall": "Floyd-Warshall Shortest Paths",
    "wienner": "Wiener-Kriging Interpolation",
    "wigner-ville": "Wigner-Ville Time-Frequency Analysis",
    "wirtinger": "Wirtinger Complex Derivatives",
    "zeta": "Riemann Zeta Zeros",
    "zonohedra": "Zonohedra and Linear Images",
    "cauchy-binnet": "Cauchy-Binet Formula",
    "convnets": "Convolutional Neural Networks",
    "de-casterljau": "De Casteljau Algorithm",
    "divergences": "Statistical Divergences",
    "gale-shapeley": "Gale-Shapley Stable Matching",
    "gerschgorin-paper": "Gershgorin Disk Theorem",
    "interpolations": "Interpolation Methods",
    "lorentz-attractor": "Lorenz Attractor",
    "mac-adam": "MacAdam Color Ellipses",
    "mcadam": "MacAdam Color Ellipses",
    "nestero-polyak": "Nesterov-Polyak Acceleration",
    "perron-frob": "Perron-Frobenius Theorem",
    "shatten-norms": "Schatten Norms",
    "voltera-lotka": "Lotka-Volterra Dynamics",
}


VIGNETTE_FILE_TITLE_OVERRIDES = {
    "074-bifurcation": "Logistic-Map Bifurcations",
    "184-gears": "Non-Circular Gears",
    "234-delaunay": "Delaunay Triangulation",
    "249-conformal": "Conformal Maps",
    "268-bcr-algo": "Beylkin-Coifman-Rokhlin Fast Operator",
    "294-zeta": "Riemann Zeta Zeros",
    "443-conformal": "Conformal Maps",
    "461-covariance": "Covariance Ellipsoids",
    "472-bernoulli": "Bernoulli Brachistochrone",
    "514-danzig": "Dantzig Simplex Method",
    "526-laplace": "Laplace Bayesian Inference",
    "548-lasso": "Lasso Sparse Regression",
    "556a-modelization-1": "Mathematical Modeling, Part 1",
    "578-mipmapping": "Mipmapping and Antialiasing",
    "590-verlet": "Verlet Symplectic Integration",
    "619-collisions": "Elastic Particle Collisions",
    "624-bernstein": "Bernstein Approximation Theorem",
    "628-noether": "Noether and Betti Numbers",
    "646-mandelbrot": "Mandelbrot and Julia Sets",
    "654-coarea": "Coarea Formula",
    "674-penrose": "Penrose Aperiodic Tilings",
    "712-canny": "Canny Edge Detection",
    "733-bernoulli": "Bernoulli Brachistochrone",
    "738-inpainting": "Exemplar-Based Image Inpainting",
    "751-pendulum": "Huygens Pendulum Dynamics",
    "773-bertrand": "Bertrand Central-Force Theorem",
    "787-optim": "Optimization Problem Taxonomy",
    "398-cannot-hear": "Isospectral Drums",
    "508-fourier-memoire": "Foundations of Fourier Analysis",
    "512-monge-memoire": "Foundations of Optimal Transport",
    "603-hear-shape-cat": "Laplacian Shape Spectrum",
    "770-fench-rock": "Fenchel-Rockafellar Duality",
}


VIGNETTE_TOKEN_TITLES = {
    "1d": "1D",
    "2d": "2D",
    "3d": "3D",
    "admm": "ADMM",
    "algo": "Algorithm",
    "aniso": "Anisotropic",
    "approx": "Approximation",
    "arith": "Arithmetic",
    "autom": "Automata",
    "bcr": "BCR",
    "bm3d": "BM3D",
    "cfl": "CFL",
    "clt": "CLT",
    "conj": "Conjugate",
    "cont": "Continuous",
    "contrac": "Contraction",
    "conv": "Convex",
    "convol": "Convolution",
    "coords": "Coordinates",
    "cov": "Covariance",
    "cpx": "Complex",
    "curv": "Curvature",
    "dct": "DCT",
    "desc": "Descent",
    "descr": "Descriptors",
    "dft": "DFT",
    "displ": "Displacement",
    "dist": "Distance",
    "dtw": "Dynamic Time Warping",
    "em": "Expectation-Maximization",
    "eq": "Equation",
    "equaliz": "Equalization",
    "evol": "Evolution",
    "fft": "Fast Fourier Transform",
    "fisher": "Fisher-Rao",
    "fmm": "Fast Marching",
    "frob": "Frobenius",
    "frobenus": "Frobenius",
    "func": "Function",
    "fwd": "Forward",
    "gauss": "Gaussian",
    "geom": "Geometric",
    "grad": "Gradient",
    "histo": "Histogram",
    "highdim": "High-Dimensional",
    "ica": "Independent Component Analysis",
    "icp": "Iterative Closest Point",
    "interp": "Interpolation",
    "ineq": "Inequality",
    "incompress": "Incompressible",
    "iter": "Iteration",
    "ista": "Iterative Soft Thresholding",
    "jl": "Johnson-Lindenstrauss",
    "kl": "Kullback-Leibler",
    "kanto": "Kantorovich",
    "kin": "Kinematics",
    "kmeans": "K-Means",
    "knn": "K-Nearest Neighbors",
    "lda": "Linear Discriminant Analysis",
    "lin": "Linear",
    "lapl": "Laplacian",
    "leastsquare": "Least Squares",
    "lp": "Lp",
    "meanval": "Mean-Value",
    "maxent": "Maximum Entropy",
    "mlp": "Multilayer Perceptrons",
    "nmf": "Nonnegative Matrix Factorization",
    "nonlin": "Nonlinear",
    "nurbs": "NURBS",
    "optim": "Optimization",
    "ortho": "Orthogonal",
    "ot": "Optimal Transport",
    "pbm": "Problem",
    "pca": "Principal Component Analysis",
    "pde": "PDE",
    "pdes": "PDEs",
    "poly": "Polynomial",
    "pp": "Plus Plus",
    "proj": "Projected",
    "proba": "Probability",
    "qda": "Quadratic Discriminant Analysis",
    "quantiz": "Quantization",
    "randmat": "Random Matrices",
    "reconstr": "Reconstruction",
    "regul": "Regularization",
    "relu": "ReLU",
    "schro": "Schrodinger",
    "sdp": "Semidefinite",
    "sift": "SIFT",
    "sir": "SIR",
    "sbm": "Stochastic Block Model",
    "sne": "Stochastic Neighbor Embedding",
    "sobol": "Sobol",
    "svm": "SVM",
    "spher": "Spherical Harmonics",
    "subdiv": "Subdivision",
    "surf": "Surface",
    "thm": "Theorem",
    "transf": "Transform",
    "tv": "Total Variation",
    "psd": "Positive Semidefinite",
    "nn": "Neural Network",
    "val": "Value",
    "vec": "Vector",
    "wass": "Wasserstein",
}


# Only direct topic matches are listed here. Keeping the relation explicit avoids
# attaching a notebook merely because it shares a broad word such as "flow".
RELATED_NOTEBOOK_TITLES = {
    "python/ada-boost/ada-boost.ipynb": ("Boosting Classification",),
    "python/advection/advection.ipynb": ("Advection Equation",),
    "python/alpha-shapes/alpha-shapes.ipynb": ("Alpha Shape", "Alpha Shapes"),
    "python/apolonian/apolonian.ipynb": ("Apollonian Gasket", "Apollonian Gaskets"),
    "python/arithmetico-geometric/arithmetico-geometric.ipynb": ("Arithmetic-Geometric Means",),
    "python/backprojection-radon/backprojection-radon.ipynb": ("Tomography Theorem", "Tomography Transform"),
    "python/bernouilli-tcl/bernouilli-tcl.ipynb": ("Bernoulli Distributions", "Central Limit Convolution"),
    "python/bifurcation/bifurcation.ipynb": ("Logistic-Map Bifurcations",),
    "python/bilateral-filtering/bilateral-filtering.ipynb": ("Bilateral Filter",),
    "python/boltzmann/boltzmann.ipynb": ("Boltzmann Equation",),
    "python/brachistochrone/brachistochrone.ipynb": ("Bernoulli Brachistochrone",),
    "python/bregman-flow/bregman-flow.ipynb": ("Bregman Algorithm", "Bregman Divergence"),
    "python/brownian/brownian.ipynb": ("Brownian Evolution", "Brownian Motion"),
    "python/burgers/burgers.ipynb": ("Burgers Equation", "Burgers Shock Equation"),
    "python/cellular/cellular.ipynb": ("Cellular Automata",),
    "python/compressed-sensing-basis-pursuit/compressed-sensing-basis-pursuit.ipynb": ("Basis Pursuit",),
    "python/conjugate-gradient/conjugate-gradient.ipynb": ("Conjugate Gradient",),
    "python/de-casteljau/de-casteljau.ipynb": ("De Casteljau Algorithm",),
    "python/dijkstra/dijkstra.ipynb": ("Dijkstra Algorithm", "Dijkstra Shortest Paths"),
    "python/dtw/dtw.ipynb": ("Dynamic Time Warping",),
    "python/dykstra/dykstra.ipynb": ("Dykstra Algorithm", "Dykstra Pocs"),
    "python/edge-detection/edge-detection.ipynb": ("Canny Edge Detection", "Edge Detectors", "Marr-Hildreth Edge Detection"),
    "python/eikonal-fast-marching/eikonal-fast-marching.ipynb": ("Eikonal Distance Equation", "Eikonal Equation", "Fast Marching", "Fast Marching Method", "Geodesics Fast Marching"),
    "python/error-diffusion/error-diffusion.ipynb": ("Error Diffusion",),
    "python/farthest-point/farthest-point.ipynb": ("Farthest Point", "Farthest-Point Sampling"),
    "python/fixed-point/fixed-point.ipynb": ("Banach Fixed Point", "Fixed-Point Dynamics"),
    "python/floyd-warshall/floyd-warshall.ipynb": ("Floyd Warshall", "Floyd-Warshall Shortest Paths"),
    "python/fluids/fluids.ipynb": ("Stable Fluids",),
    "python/fourier-curves/fourier-curves.ipynb": ("Fourier Curve", "Fourier Descriptors"),
    "python/fourier-matrix/fourier-matrix.ipynb": ("Fourier 2D",),
    "python/fourier-signal/fourier-signal.ipynb": ("Fourier Cat", "Fourier Low Approximation"),
    "python/foveation/foveation.ipynb": ("Foveated Image Filtering",),
    "python/frank-wolfe/frank-wolfe.ipynb": ("Frank-Wolfe Optimization",),
    "python/gears-non-circ/gears-non-circ.ipynb": ("Non-Circular Gears",),
    "python/gershgorin/gershgorin.ipynb": ("Gershgorin Disk", "Gershgorin Disk Theorem"),
    "python/gibbs-sampling/gibbs-sampling.ipynb": ("Gibbs Sampling", "Hastings Sampling", "Metropolis Hastings", "Metropolis Sampling"),
    "python/grad-desc-ode/grad-desc-ode.ipynb": ("Gradient Flow",),
    "python/grad-desc-quad/grad-desc-quad.ipynb": ("Gradient Descent",),
    "python/gradflow-metric/gradflow-metric.ipynb": ("Gradient Flows",),
    "python/graph-coloring/graph-coloring.ipynb": ("Chromatic Number",),
    "python/graphical-lasso/graphical-lasso.ipynb": ("Graphical Lasso",),
    "python/haar-walsh/haar-walsh.ipynb": ("Walsh Haar",),
    "python/harmonic/harmonic.ipynb": ("Harmonic Equation",),
    "python/heat-1d/heat-1d.ipynb": ("Scale Space", "Scale Space Filtering"),
    "python/heat-polynomials/heat-polynomials.ipynb": ("Heat Polynomial",),
    "python/heavy-ball/heavy-ball.ipynb": ("Heavy Ball",),
    "python/hist-eq/hist-eq.ipynb": ("Histogram Equalization",),
    "python/hopfield-network/hopfield-network.ipynb": ("Hopfield Networks",),
    "python/hump-algebra/hump-algebra.ipynb": ("Hump Algebra",),
    "python/ica/ica.ipynb": ("Independent Component Analysis",),
    "python/icp/icp.ipynb": ("Iterative Closest Point", "Iterative Closest Point Algorithm"),
    "python/interior-points/interior-points.ipynb": ("Interior Points",),
    "python/inverse-kinematics/inverse-kinematics.ipynb": ("Inverse Kinematics",),
    "python/ising-model/ising-model.ipynb": ("Ising Networks",),
    "python/ista/ista.ipynb": ("Iterative Soft Thresholding",),
    "python/jko-flow/jko-flow.ipynb": ("JKO Wasserstein Flow", "Porous Medium"),
    "python/joukowski/joukowski.ipynb": ("Joukowski Airfoil Transform",),
    "python/julia-sets/julia-sets.ipynb": ("Julia Fractal Sets", "Julia Set", "Mandelbrot and Julia Sets"),
    "python/k-nn/k-nn.ipynb": ("K-Nearest Neighbors",),
    "python/kaczmarz/kaczmarz.ipynb": ("Kaczmarz Algorithm",),
    "python/kalman/kalman.ipynb": ("Kalman Dynamics",),
    "python/kernel-svm/kernel-svm.ipynb": ("Kernel SVM",),
    "python/kmean++/kmeanpp.ipynb": ("K-Means++ Initialization",),
    "python/kmeans/kmeans.ipynb": ("K-Means Algorithm", "Lloyd Algorithm"),
    "python/kriging/kriging.ipynb": ("Kriging with Gaussian Processes", "Wiener-Kriging Interpolation"),
    "python/kubo-matrix-mean/kubo-matrix-mean.ipynb": ("Kubo-Ando Matrix Means",),
    "python/lagrange-hermite/lagrange-hermite.ipynb": ("Lagrange Hermite",),
    "python/laplacian-eigenmaps/laplacian-eigenmaps.ipynb": ("Laplacian Eigenmap", "Laplacian Eigenmaps"),
    "python/laplacian-pyramid/laplacian-pyramid.ipynb": ("Laplacian Pyramid",),
    "python/laplacian-spectrum/laplacian-spectrum.ipynb": ("Laplacian Shape Spectrum",),
    "python/mean-curvature-flow/mean-curvature-flow.ipynb": ("Mean Curvature",),
    "python/grad-desc-mirror/grad-desc-mirror.ipynb": ("Mirror Descent",),
    "python/pagerank-random-walks/pagerank-random-walks.ipynb": ("PageRank Random Walks",),
    "python/reaction-diffusion-turing/reaction-diffusion-turing.ipynb": ("Reaction Diffusion", "Turing Morpho"),
    "python/schrodinger-bridge/schrodinger-bridge.ipynb": ("Schrodinger Bridge Transport",),
    "python/sinkhorn-distance/sinkhorn-distance.ipynb": ("Sinkhorn Algorithm",),
    "python/spherical-harmonics-signals/spherical-harmonics-signals.ipynb": ("Harm Spherical Harmonics", "Sphere Harmonics"),
    "python/tsne-umap-comparison/tsne-umap-comparison.ipynb": ("t-SNE Dimensionality Reduction",),
    "python/wasserstein-barycenters/wasserstein-barycenters.ipynb": ("Optimal Transport Barycenters",),
}

RELATED_NOTEBOOK_BY_TITLE = {
    title.casefold(): notebook
    for notebook, titles in RELATED_NOTEBOOK_TITLES.items()
    for title in titles
}


SINGLE_WORD_DESCRIPTORS = (
    (r"\binequalit", "Inequality"),
    (r"\btheorem\b", "Theorem"),
    (r"\balgorithm\b", "Algorithm"),
    (r"\bequation\b", "Equation"),
    (r"\binterpolat", "Interpolation"),
    (r"\bdenois", "Denoising"),
    (r"\bclassif", "Classification"),
    (r"\bsampl", "Sampling"),
    (r"\bwavelet", "Wavelets"),
    (r"\btransform\b", "Transform"),
    (r"\bdivergence", "Divergence"),
    (r"\bdistance\b|\bmetric\b", "Geometry"),
    (r"\bgradient\b|\boptimization\b", "Optimization"),
    (r"\bnetwork", "Networks"),
    (r"\bmatrix|\bmatrices", "Matrices"),
    (r"\bdistribution", "Distributions"),
    (r"\bprobability", "Probability"),
    (r"\bcurve", "Curves"),
    (r"\bsurface", "Surfaces"),
    (r"\bgraph", "Graphs"),
    (r"\bdynamical|\bdynamics|\btrajectory", "Dynamics"),
    (r"\bpartial differential|\bpde\b", "PDE"),
    (r"\bfilter", "Filtering"),
    (r"\bmodel\b", "Model"),
)


def clean_text(s: str) -> str:
    # Remove inline/display LaTeX fragments so website card descriptions stay readable plain text.
    s = re.sub(r"\$\$.*?\$\$", " ", s, flags=re.S)
    s = re.sub(r"\$[^$]*\$", " ", s)
    s = re.sub(r"\\\((.*?)\\\)", r" \1 ", s)
    s = re.sub(r"\\\[(.*?)\\\]", r" \1 ", s, flags=re.S)
    s = s.replace("\\", " ")
    s = re.sub(r"`([^`]*)`", r"\1", s)
    # Preserve URLs when markdown links are present: [label](url) -> "label url"
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 \2", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    # Remove only heavy markdown markers, keep URL-critical characters like "_" and "#"
    s = re.sub(r"[*>$]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def polish_description(text: str) -> str:
    """Light editorial polish while staying semantically close to source text."""
    s = clean_text(text)

    def _polish_chunk(chunk: str) -> str:
        c = chunk
        # Gentle style cleanup
        c = re.sub(r"oldies but goldies\s*:", "Classic reference:", c, flags=re.I)
        c = re.sub(r"\baka\b", "also known as", c, flags=re.I)

        # Frequent typo / naming fixes found in source collection
        replacements = {
            "dikstra": "Dijkstra",
            "vornoi": "Voronoi",
            "krigging": "kriging",
            "subdivision shemes": "subdivision schemes",
            "dicrepancies": "discrepancies",
            "varyin": "varying",
        }
        for bad, good in replacements.items():
            c = re.sub(re.escape(bad), good, c, flags=re.I)

        # Normalize spacing around punctuation (text chunks only, no URLs)
        c = re.sub(r"\s+([,;:.!?])", r"\1", c)
        c = re.sub(r"([,;!?])([^\s])", r"\1 \2", c)
        c = re.sub(r"\s+", " ", c).strip()
        return c

    url_re = re.compile(r"https?://\S+")
    out_parts: List[str] = []
    last = 0
    for m in url_re.finditer(s):
        left = s[last : m.start()]
        if left:
            out_parts.append(_polish_chunk(left))
        out_parts.append(m.group(0))  # keep URLs untouched
        last = m.end()
    tail = s[last:]
    if tail:
        out_parts.append(_polish_chunk(tail))

    s2 = " ".join(p for p in out_parts if p).strip()
    s2 = re.sub(r"\s+", " ", s2).strip()

    # Capitalize first letter when possible
    if s2 and s2[0].isalpha():
        s2 = s2[0].upper() + s2[1:]

    # Ensure terminal punctuation for readability (unless ending with URL)
    if s2 and not re.search(r"(https?://\S+)$", s2) and s2[-1] not in ".!?":
        s2 += "."

    return s2


def title_from_path(path: str) -> str:
    stem = Path(path).stem
    return clean_text(stem.replace("-", " ").replace("_", " ").title())


def vignette_stem(path: str) -> str:
    stem = re.sub(r"^\d+[a-z]?[-_]*", "", Path(path).stem.lower())
    stem = re.sub(r"\.\d+$", "", stem)
    typo_fixes = {
        "dicrepancies": "discrepancies",
        "helmoltz": "helmholtz",
        "netwon": "newton",
        "poisso": "poisson",
        "vornoi": "voronoi",
        "woronoi": "voronoi",
    }
    for bad, good in typo_fixes.items():
        stem = re.sub(rf"(?<![a-z]){re.escape(bad)}(?![a-z])", good, stem)
    return stem


def curate_vignette_title(path: str, description: str) -> str:
    """Turn archival filename shorthand into a compact explanatory card title."""
    file_stem = Path(path).stem.lower()
    if file_stem in VIGNETTE_FILE_TITLE_OVERRIDES:
        return VIGNETTE_FILE_TITLE_OVERRIDES[file_stem]
    stem = vignette_stem(path)
    if stem in VIGNETTE_TITLE_OVERRIDES:
        return VIGNETTE_TITLE_OVERRIDES[stem]

    parts: List[str] = []
    for token in re.split(r"[-_]+", stem):
        if not token or token.isdigit():
            continue
        parts.extend(VIGNETTE_TOKEN_TITLES.get(token, token.title()).split())

    title = clean_text(" ".join(parts))
    if len(title.split()) == 1:
        lower_description = description.lower()
        for pattern, suffix in SINGLE_WORD_DESCRIPTORS:
            if re.search(pattern, lower_description) and suffix.lower() != title.lower():
                title = f"{title} {suffix}"
                break
    return title or f"Vignette {Path(path).name}"


def catalog_sort_key(row: Row) -> tuple[str, str, str, str]:
    words = re.findall(r"[A-Za-z0-9]+", row.title)
    first = next((word for word in words if word.lower() not in TITLE_STOP_WORDS), "")

    def normalize(value: str) -> str:
        value = unicodedata.normalize("NFKD", value)
        value = "".join(ch for ch in value if not unicodedata.combining(ch))
        return value.casefold()

    return normalize(first), normalize(row.title), row.type, normalize(row.filename)


def parse_readme_notebook_blurbs() -> Dict[str, Row]:
    text = README.read_text(encoding="utf-8")
    rows: Dict[str, Row] = {}
    pattern = re.compile(
        r"\|\s+\*\*(?P<title>.*?)\*\*<br>(?P<desc>.*?)\s+\|\s+.*?\((?P<nb>python/[^)]+\.ipynb)\)\s+\|"
    )
    for m in pattern.finditer(text):
        nb = m.group("nb").strip()
        rows[nb] = Row(
            title=clean_text(m.group("title").strip()),
            content=polish_description(m.group("desc").strip()),
            filename=nb,
            type="notebook",
        )
    return rows


def parse_notebook_fallback(nb_path: Path) -> Row:
    rel = nb_path.relative_to(ROOT).as_posix()
    try:
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
    except Exception:
        return Row(title=title_from_path(rel), content="", filename=rel, type="notebook")

    title = ""
    content = ""
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        src = "".join(cell.get("source", []))
        if not title:
            m = re.search(r"^\s*#\s+(.+)$", src, flags=re.M)
            if m:
                title = clean_text(m.group(1))
        if not content:
            chunks = [c.strip() for c in src.split("\n\n") if c.strip()]
            for chunk in chunks:
                if chunk.lstrip().startswith("#"):
                    continue
                content = clean_text(chunk)
                break
        if title and content:
            break

    if not title:
        title = title_from_path(rel)
    if not content:
        content = "Standalone educational notebook with mathematical exposition and visual experiments."
    content = polish_description(content)
    if len(content) > 260:
        content = content[:257].rstrip() + "..."
    return Row(title=title, content=content, filename=rel, type="notebook")


def parse_vignettes() -> List[Row]:
    text = MYDATA.read_text(encoding="utf-8")
    m = re.search(r"const\s+textData\s*=\s*`(.*)`\s*;\s*$", text, flags=re.S)
    if not m:
        raise RuntimeError("Could not parse textData from vignettes/mydata.js")

    blob = m.group(1).strip()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", blob) if b.strip()]
    out: List[Row] = []
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        date = lines[0]
        name = lines[1]
        desc = polish_description(" ".join(lines[2:])) if len(lines) > 2 else ""
        title = curate_vignette_title(name, desc)
        content = desc if desc else f"Vignette entry from {date}."
        related_notebook = RELATED_NOTEBOOK_BY_TITLE.get(title.casefold(), "")
        if related_notebook and not (ROOT / related_notebook).exists():
            related_notebook = ""
        if len(content) > 320:
            content = content[:317].rstrip() + "..."
        out.append(
            Row(
                title=title,
                content=content,
                filename=f"vignettes/{name}",
                type="vignette",
                related_notebook=related_notebook,
            )
        )
    return out


def main() -> None:
    readme_map = parse_readme_notebook_blurbs()
    rows: List[Row] = []

    for nb in sorted(PYTHON_DIR.glob("**/*.ipynb")):
        rel = nb.relative_to(ROOT).as_posix()
        if rel in readme_map:
            rows.append(readme_map[rel])
        else:
            rows.append(parse_notebook_fallback(nb))

    rows.extend(parse_vignettes())

    existing_rows: List[Row] = []
    dropped: List[str] = []
    for r in rows:
        if (ROOT / r.filename).exists():
            existing_rows.append(r)
        else:
            dropped.append(r.filename)

    existing_rows.sort(key=catalog_sort_key)
    df = pd.DataFrame(
        [r.__dict__ for r in existing_rows],
        columns=["title", "content", "filename", "type", "related_notebook"],
    )
    df.to_excel(DB_XLSX, index=False)
    DB_JSON.write_text(df.to_json(orient="records", force_ascii=False, indent=2), encoding="utf-8")
    DB_JS.write_text(
        "window.CATALOG_DATA = " + df.to_json(orient="records", force_ascii=False) + ";\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(df)} rows:")
    print(f" - {DB_XLSX.relative_to(ROOT)}")
    print(f" - {DB_JSON.relative_to(ROOT)}")
    print(f" - {DB_JS.relative_to(ROOT)}")
    if dropped:
        print(f"Dropped {len(dropped)} missing-file entries.")
        for name in dropped[:20]:
            print(f"   - {name}")


if __name__ == "__main__":
    main()

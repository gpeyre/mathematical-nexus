#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


REFS = {
    "sinkhorn-distance": [
        "M. Cuturi, \"Sinkhorn Distances: Lightspeed Computation of Optimal Transport\", NeurIPS, 2013.",
        "G. Peyré, M. Cuturi, *Computational Optimal Transport*, Foundations and Trends in ML, 2019.",
        "C. Villani, *Optimal Transport: Old and New*, Springer, 2009.",
    ],
    "unbalanced-ot": [
        "L. Chizat, G. Peyré, B. Schmitzer, F.-X. Vialard, \"Scaling Algorithms for Unbalanced Transport Problems\", Math. Comp., 2018.",
        "L. Chizat, G. Peyré, B. Schmitzer, F.-X. Vialard, \"Unbalanced Optimal Transport: Dynamic and Kantorovich Formulations\", JFA, 2018.",
        "G. Peyré, M. Cuturi, *Computational Optimal Transport*, 2019 (chapters on unbalanced OT).",
    ],
    "wasserstein-barycenters": [
        "M. Agueh, G. Carlier, \"Barycenters in the Wasserstein Space\", SIAM J. Math. Anal., 2011.",
        "M. Cuturi, A. Doucet, \"Fast Computation of Wasserstein Barycenters\", ICML, 2014.",
        "G. Peyré, M. Cuturi, *Computational Optimal Transport*, 2019.",
    ],
    "sliced-wasserstein": [
        "N. Bonneel, J. Rabin, G. Peyré, H. Pfister, \"Sliced and Radon Wasserstein Barycenters of Measures\", JMIV, 2015.",
        "J. Rabin, G. Peyré, J. Delon, M. Bernot, \"Wasserstein Barycenter and Its Application to Texture Mixing\", SSVM, 2011.",
        "G. Peyré, M. Cuturi, *Computational Optimal Transport*, 2019.",
    ],
    "schrodinger-bridge": [
        "C. Léonard, \"A Survey of the Schrödinger Problem and Some of Its Connections with Optimal Transport\", DCDS-A, 2014.",
        "Y. Chen, T. T. Georgiou, M. Pavon, \"Optimal Transport over a Linear Dynamical System\", IEEE TAC, 2016.",
        "J.-D. Benamou et al., \"Iterative Bregman Projections for Regularized Transportation Problems\", SIAM JSC, 2015.",
    ],
    "mean-curvature-flow": [
        "S. Osher, J. A. Sethian, \"Fronts Propagating with Curvature-Dependent Speed\", JCP, 1988.",
        "L. C. Evans, J. Spruck, \"Motion of Level Sets by Mean Curvature I\", JDE, 1991.",
        "G. Sapiro, *Geometric Partial Differential Equations and Image Analysis*, Cambridge Univ. Press, 2001.",
    ],
    "eikonal-fast-marching": [
        "J. A. Sethian, \"A Fast Marching Level Set Method for Monotonically Advancing Fronts\", PNAS, 1996.",
        "J. N. Tsitsiklis, \"Efficient Algorithms for Globally Optimal Trajectories\", IEEE TAC, 1995.",
        "J. A. Sethian, *Level Set Methods and Fast Marching Methods*, Cambridge Univ. Press, 1999.",
    ],
    "allen-cahn-cahn-hilliard": [
        "S. M. Allen, J. W. Cahn, \"A Microscopic Theory for Antiphase Boundary Motion\", Acta Metall., 1979.",
        "J. W. Cahn, J. E. Hilliard, \"Free Energy of a Nonuniform System I\", J. Chem. Phys., 1958.",
        "A. Novick-Cohen, \"The Cahn-Hilliard Equation\", Handbook of Differential Equations, 2008.",
    ],
    "reaction-diffusion-turing": [
        "A. M. Turing, \"The Chemical Basis of Morphogenesis\", Phil. Trans. Roy. Soc. B, 1952.",
        "J. D. Murray, *Mathematical Biology II: Spatial Models and Biomedical Applications*, Springer, 2003.",
        "P. Grindrod, *Patterns and Waves: The Theory and Applications of Reaction-Diffusion Equations*, Oxford Univ. Press, 1996.",
    ],
    "wave-equation-dispersion": [
        "R. J. LeVeque, *Finite Difference Methods for Ordinary and Partial Differential Equations*, SIAM, 2007.",
        "B. Gustafsson, H.-O. Kreiss, J. Oliger, *Time Dependent Problems and Difference Methods*, Wiley, 1995.",
        "L. N. Trefethen, *Spectral Methods in MATLAB*, SIAM, 2000.",
    ],
    "hamiltonian-symplectic": [
        "E. Hairer, C. Lubich, G. Wanner, *Geometric Numerical Integration*, Springer, 2006.",
        "B. Leimkuhler, S. Reich, *Simulating Hamiltonian Dynamics*, Cambridge Univ. Press, 2004.",
        "M. P. Allen, D. J. Tildesley, *Computer Simulation of Liquids*, Oxford Univ. Press, 2017.",
    ],
    "fem-1d-2d": [
        "S. C. Brenner, R. Scott, *The Mathematical Theory of Finite Element Methods*, Springer, 2008.",
        "D. Braess, *Finite Elements: Theory, Fast Solvers, and Applications*, Cambridge Univ. Press, 2007.",
        "S. Larsson, V. Thomée, *Partial Differential Equations with Numerical Methods*, Springer, 2003.",
    ],
    "poisson-meshes": [
        "M. Meyer, M. Desbrun, P. Schröder, A. H. Barr, \"Discrete Differential-Geometry Operators for Triangulated 2-Manifolds\", 2002.",
        "K. Crane, U. Pinkall, P. Schröder, \"Spin Transformations of Discrete Surfaces\", ACM TOG, 2011.",
        "M. Botsch et al., *Polygon Mesh Processing*, AK Peters, 2010.",
    ],
    "level-set-methods": [
        "S. Osher, R. Fedkiw, *Level Set Methods and Dynamic Implicit Surfaces*, Springer, 2003.",
        "J. A. Sethian, *Level Set Methods and Fast Marching Methods*, Cambridge Univ. Press, 1999.",
        "S. Osher, J. A. Sethian, \"Fronts Propagating with Curvature-Dependent Speed\", JCP, 1988.",
    ],
    "compressed-sensing-basis-pursuit": [
        "D. L. Donoho, \"Compressed Sensing\", IEEE TIT, 2006.",
        "E. J. Candès, J. Romberg, T. Tao, \"Robust Uncertainty Principles\", IEEE TIT, 2006.",
        "S. Boyd et al., \"Distributed Optimization and Statistical Learning via ADMM\", Foundations and Trends in ML, 2011.",
    ],
    "orthogonal-matching-pursuit": [
        "Y. C. Pati, R. Rezaiifar, P. S. Krishnaprasad, \"Orthogonal Matching Pursuit\", Asilomar, 1993.",
        "J. A. Tropp, A. C. Gilbert, \"Signal Recovery from Random Measurements via OMP\", IEEE TIT, 2007.",
        "S. Mallat, Z. Zhang, \"Matching Pursuits with Time-Frequency Dictionaries\", IEEE TSP, 1993.",
    ],
    "admm-first-principles": [
        "D. Gabay, B. Mercier, \"A Dual Algorithm for the Solution of Nonlinear Variational Problems\", 1976.",
        "R. Glowinski, A. Marrocco, \"Sur l'approximation ... par pénalisation-dualité\", 1975.",
        "S. Boyd et al., \"Distributed Optimization and Statistical Learning via ADMM\", Foundations and Trends in ML, 2011.",
    ],
    "pdhg-chambolle-pock": [
        "A. Chambolle, T. Pock, \"A First-Order Primal-Dual Algorithm for Convex Problems\", J. Math. Imaging Vis., 2011.",
        "A. Chambolle, T. Pock, \"An Introduction to Continuous Optimization for Imaging\", Acta Numerica, 2016.",
        "N. Parikh, S. Boyd, \"Proximal Algorithms\", Foundations and Trends in Optimization, 2014.",
    ],
    "bfgs-lbfgs": [
        "J. Nocedal, S. J. Wright, *Numerical Optimization*, Springer, 2006.",
        "R. Fletcher, \"A New Approach to Variable Metric Algorithms\", Computer Journal, 1970.",
        "D. C. Liu, J. Nocedal, \"On the Limited Memory BFGS Method\", Math. Programming, 1989.",
    ],
    "trust-region-methods": [
        "J. Nocedal, S. J. Wright, *Numerical Optimization*, Springer, 2006.",
        "A. R. Conn, N. I. M. Gould, P. L. Toint, *Trust Region Methods*, SIAM, 2000.",
        "Y. Yuan, \"Recent Advances in Trust Region Algorithms\", Math. Programming, 2015.",
    ],
    "newton-fractals-complex": [
        "J. Milnor, *Dynamics in One Complex Variable*, Princeton Univ. Press, 2006.",
        "H.-O. Peitgen, P. H. Richter, *The Beauty of Fractals*, Springer, 1986.",
        "L. V. Ahlfors, *Complex Analysis*, McGraw-Hill, 1979.",
    ],
    "chebyshev-minimax": [
        "L. N. Trefethen, *Approximation Theory and Approximation Practice*, SIAM, 2013.",
        "E. W. Cheney, *Introduction to Approximation Theory*, AMS Chelsea, 1998.",
        "J.-P. Boyd, *Chebyshev and Fourier Spectral Methods*, Dover, 2001.",
    ],
    "runge-kutta-stability": [
        "E. Hairer, S. P. Nørsett, G. Wanner, *Solving Ordinary Differential Equations I*, Springer, 1993.",
        "J. C. Butcher, *Numerical Methods for Ordinary Differential Equations*, Wiley, 2016.",
        "G. Dahlquist, Å. Björck, *Numerical Methods in Scientific Computing*, SIAM, 2008.",
    ],
    "markov-chains-mixing": [
        "D. A. Levin, Y. Peres, E. L. Wilmer, *Markov Chains and Mixing Times*, AMS, 2009.",
        "P. Bremaud, *Markov Chains: Gibbs Fields, Monte Carlo Simulation, and Queues*, Springer, 1999.",
        "J. R. Norris, *Markov Chains*, Cambridge Univ. Press, 1998.",
    ],
    "hmm-forward-backward": [
        "L. R. Rabiner, \"A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition\", Proc. IEEE, 1989.",
        "C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006.",
        "Z. Ghahramani, \"An Introduction to Hidden Markov Models and Bayesian Networks\", 2001.",
    ],
    "particle-filters-smc": [
        "A. Doucet, N. de Freitas, N. Gordon (eds.), *Sequential Monte Carlo Methods in Practice*, Springer, 2001.",
        "M. S. Arulampalam et al., \"A Tutorial on Particle Filters\", IEEE TSP, 2002.",
        "P. Del Moral, *Feynman-Kac Formulae: Genealogical and Interacting Particle Systems*, Springer, 2004.",
    ],
    "variational-inference-gmm": [
        "D. M. Blei, A. Kucukelbir, J. D. McAuliffe, \"Variational Inference: A Review for Statisticians\", JASA, 2017.",
        "C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006.",
        "M. I. Jordan et al., \"An Introduction to Variational Methods for Graphical Models\", Machine Learning, 1999.",
    ],
    "gaussian-processes-2d": [
        "C. E. Rasmussen, C. K. I. Williams, *Gaussian Processes for Machine Learning*, MIT Press, 2006.",
        "M. L. Stein, *Interpolation of Spatial Data*, Springer, 1999.",
        "A. G. Wilson, H. Nickisch, \"Kernel Interpolation for Scalable Structured Gaussian Processes\", ICML, 2015.",
    ],
    "normalizing-flows-2d": [
        "D. J. Rezende, S. Mohamed, \"Variational Inference with Normalizing Flows\", ICML, 2015.",
        "L. Dinh, J. Sohl-Dickstein, S. Bengio, \"Density Estimation using Real NVP\", ICLR, 2017.",
        "R. T. Q. Chen et al., \"Neural Ordinary Differential Equations\", NeurIPS, 2018.",
    ],
    "diffusion-models-toy": [
        "J. Ho, A. Jain, P. Abbeel, \"Denoising Diffusion Probabilistic Models\", NeurIPS, 2020.",
        "Y. Song et al., \"Score-Based Generative Modeling through Stochastic Differential Equations\", ICLR, 2021.",
        "Y. Song, S. Ermon, \"Generative Modeling by Estimating Gradients of the Data Distribution\", NeurIPS, 2019.",
    ],
    "tsne-umap-comparison": [
        "L. van der Maaten, G. Hinton, \"Visualizing Data using t-SNE\", JMLR, 2008.",
        "L. McInnes, J. Healy, J. Melville, \"UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction\", 2018.",
        "J. A. Lee, M. Verleysen, *Nonlinear Dimensionality Reduction*, Springer, 2007.",
    ],
    "spectral-graph-wavelets": [
        "D. K. Hammond, P. Vandergheynst, R. Gribonval, \"Wavelets on Graphs via Spectral Graph Theory\", ACHA, 2011.",
        "F. Chung, *Spectral Graph Theory*, AMS, 1997.",
        "D. I. Shuman et al., \"The Emerging Field of Signal Processing on Graphs\", IEEE SPM, 2013.",
    ],
    "pagerank-random-walks": [
        "S. Brin, L. Page, \"The Anatomy of a Large-Scale Hypertextual Web Search Engine\", 1998.",
        "A. N. Langville, C. D. Meyer, *Google's PageRank and Beyond*, Princeton Univ. Press, 2006.",
        "D. F. Gleich, \"PageRank Beyond the Web\", SIAM Review, 2015.",
    ],
    "gnn-message-passing-toy": [
        "T. N. Kipf, M. Welling, \"Semi-Supervised Classification with Graph Convolutional Networks\", ICLR, 2017.",
        "P. W. Battaglia et al., \"Relational Inductive Biases, Deep Learning, and Graph Networks\", 2018.",
        "M. M. Bronstein et al., \"Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges\", 2021.",
    ],
    "riemannian-optimization-stiefel": [
        "P.-A. Absil, R. Mahony, R. Sepulchre, *Optimization Algorithms on Matrix Manifolds*, Princeton Univ. Press, 2008.",
        "N. Boumal, *An Introduction to Optimization on Smooth Manifolds*, Cambridge Univ. Press, 2023.",
        "A. Edelman, T. A. Arias, S. T. Smith, \"The Geometry of Algorithms with Orthogonality Constraints\", SIMAX, 1998.",
    ],
    "matrix-completion-nuclear-norm": [
        "E. J. Candès, B. Recht, \"Exact Matrix Completion via Convex Optimization\", Foundations of Computational Mathematics, 2009.",
        "J.-F. Cai, E. J. Candès, Z. Shen, \"A Singular Value Thresholding Algorithm for Matrix Completion\", SIAM J. Optim., 2010.",
        "B. Recht, M. Fazel, P. A. Parrilo, \"Guaranteed Minimum-Rank Solutions via Nuclear Norm Minimization\", SIAM Review, 2010.",
    ],
    "robust-pca-lowrank-sparse": [
        "E. J. Candès, X. Li, Y. Ma, J. Wright, \"Robust Principal Component Analysis?\", JACM, 2011.",
        "Z. Lin, M. Chen, Y. Ma, \"The Augmented Lagrange Multiplier Method for Exact Recovery of Corrupted Low-Rank Matrices\", 2010.",
        "J. Wright et al., \"Robust Principal Component Analysis: Exact Recovery of Corrupted Low-Rank Matrices via Convex Optimization\", NeurIPS, 2009.",
    ],
    "persistent-homology-topology": [
        "H. Edelsbrunner, J. Harer, *Computational Topology: An Introduction*, AMS, 2010.",
        "R. Ghrist, \"Barcodes: The Persistent Topology of Data\", Bull. AMS, 2008.",
        "G. Carlsson, \"Topology and Data\", Bull. AMS, 2009.",
    ],
    "spherical-harmonics-signals": [
        "J. D. Driscoll, D. M. Healy, \"Computing Fourier Transforms and Convolutions on the 2-Sphere\", Adv. Appl. Math., 1994.",
        "F. J. Simons, F. A. Dahlen, M. A. Wieczorek, \"Spatiospectral Concentration on a Sphere\", SIAM Review, 2006.",
        "S. Helgason, *Groups and Geometric Analysis*, AMS, 2000.",
    ],
    "finite-groups-fft-cyclic": [
        "P. Diaconis, *Group Representations in Probability and Statistics*, IMS, 1988.",
        "T. W. Körner, *Fourier Analysis*, Cambridge Univ. Press, 1988.",
        "A. Terras, *Fourier Analysis on Finite Groups and Applications*, Cambridge Univ. Press, 1999.",
    ],
}


def format_biblio(items: list[str]) -> list[str]:
    lines = ["## Bibliographical Resources", ""]
    lines.extend([f"- {it}" for it in items])
    return [line + "\n" for line in lines]


def update_notebook(path: Path, items: list[str]) -> bool:
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb.get("cells", [])
    target_idx = None
    for i, c in enumerate(cells):
        if c.get("cell_type") != "markdown":
            continue
        txt = "".join(c.get("source", [])).lower()
        if "bibliographical resources" in txt or txt.strip().startswith("### references"):
            target_idx = i
    if target_idx is None:
        return False
    cells[target_idx]["source"] = format_biblio(items)
    nb["cells"] = cells
    path.write_text(json.dumps(nb, indent=2), encoding="utf-8")
    return True


def main() -> None:
    updated = 0
    missing = []
    for slug, items in REFS.items():
        p = ROOT / "python" / slug / f"{slug}.ipynb"
        if not p.exists():
            missing.append(slug)
            continue
        if update_notebook(p, items):
            updated += 1
    print(f"updated_notebooks={updated}")
    if missing:
        print("missing_slugs:")
        for s in missing:
            print(f" - {s}")


if __name__ == "__main__":
    main()


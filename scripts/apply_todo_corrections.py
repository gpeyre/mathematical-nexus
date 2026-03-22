#!/usr/bin/env python3
from __future__ import annotations

import json
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PY = ROOT / "python"


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "source": [ln + "\n" for ln in text.strip("\n").split("\n")],
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "outputs": [],
        "source": [ln + "\n" for ln in text.strip("\n").split("\n")],
    }


def nb(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.x"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


COMMON = """
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.grid"] = True
rng = np.random.default_rng(0)
"""


def write(slug: str, cells: list[dict]) -> None:
    path = PY / slug / f"{slug}.ipynb"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb(cells), indent=2), encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")


def build_jko() -> list[dict]:
    return [
        md(
            r"""
# JKO Flow and Porous Medium Equation

The porous medium equation
$$
\partial_t \rho = \Delta(\rho^m), \quad m>1
$$
is a Wasserstein gradient flow of an internal energy. This notebook shows a longer evolution so transport and spreading are clearly visible.
"""
        ),
        md("## Setup\nWe use a stable explicit finite-difference scheme with enough final time to make motion visible."),
        code(
            COMMON
            + """
OUT = Path("python/jko-flow"); OUT.mkdir(parents=True, exist_ok=True)
n = 170
x = np.linspace(-1.0, 1.0, n)
y = np.linspace(-1.0, 1.0, n)
X, Y = np.meshgrid(x, y)
dx = x[1] - x[0]
m = 2.0
rho = np.exp(-((X+0.35)**2 + (Y+0.05)**2)/0.02) + 0.65*np.exp(-((X-0.28)**2 + (Y-0.2)**2)/0.035)
rho = np.maximum(rho, 0)
rho /= rho.sum() * dx * dx
dt = 0.15 * dx * dx
n_steps = 950
snap_idx = [0, 180, 420, 700, 949]
snaps = []
for k in range(n_steps):
    q = rho**m
    lap = (np.roll(q,1,0)+np.roll(q,-1,0)+np.roll(q,1,1)+np.roll(q,-1,1)-4*q)/(dx*dx)
    rho = np.maximum(rho + dt*lap, 0)
    rho /= rho.sum() * dx * dx
    if k in snap_idx:
        snaps.append(rho.copy())
if len(snaps) < len(snap_idx):
    snaps.append(rho.copy())
"""
        ),
        md("## Evolution snapshots\nA long time horizon highlights the displacement and diffusion of mass."),
        code(
            """
fig, axes = plt.subplots(1, 5, figsize=(14.5, 3.2), constrained_layout=True)
for ax, R, k in zip(axes, snaps, snap_idx):
    im = ax.imshow(R, origin="lower", cmap="magma", extent=[-1,1,-1,1])
    ax.set_title(f"step {k}")
    ax.set_xticks([]); ax.set_yticks([])
fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.8)
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def build_omp() -> list[dict]:
    return [
        md(
            r"""
# Orthogonal Matching Pursuit with Gaussian Bump Dictionary

Given a dictionary $\Phi=[\phi_j]_{j=1}^M$ and a signal $y$, OMP iteratively selects atoms maximizing correlation with residuals:
$$
j_k = \arg\max_j |\langle r_{k-1}, \phi_j\rangle|,\qquad
r_k = y - \Phi_{S_k}\hat\alpha_{S_k}.
$$
We use a Gaussian bump dictionary and reconstruct a sparse smooth signal.
"""
        ),
        md("## Dictionary and target signal"),
        code(
            COMMON
            + """
OUT = Path("python/orthogonal-matching-pursuit"); OUT.mkdir(parents=True, exist_ok=True)
n = 350
t = np.linspace(0, 1, n)
centers = np.linspace(0.03, 0.97, 90)
sigmas = np.array([0.018, 0.03, 0.05])
atoms = []
for s in sigmas:
    for c in centers:
        g = np.exp(-0.5*((t-c)/s)**2)
        g /= np.linalg.norm(g) + 1e-12
        atoms.append(g)
Phi = np.column_stack(atoms)

coef_true = np.zeros(Phi.shape[1])
idx_true = [18, 76, 124, 186, 230]
coef_true[idx_true] = [1.2, -0.8, 1.0, 0.7, -1.1]
y0 = Phi @ coef_true
y = y0 + 0.02 * rng.normal(size=n)
"""
        ),
        md("## OMP iterations and approximation quality"),
        code(
            """
K = 18
res = y.copy()
S = []
coef = np.zeros(Phi.shape[1])
errs = []
for _ in range(K):
    corr = np.abs(Phi.T @ res)
    corr[S] = -1.0
    j = int(np.argmax(corr))
    S.append(j)
    A = Phi[:, S]
    cS, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ cS
    coef[:] = 0
    coef[S] = cS
    errs.append(np.linalg.norm(res) / (np.linalg.norm(y) + 1e-12))

y_hat = Phi @ coef

fig, axes = plt.subplots(2, 1, figsize=(10.5, 6.0), constrained_layout=True)
axes[0].plot(t, y, color="0.5", lw=1.4, label="observed")
axes[0].plot(t, y0, "k--", lw=1.4, label="true sparse signal")
axes[0].plot(t, y_hat, color="tab:blue", lw=2.0, label="OMP approximation")
axes[0].set_title("Gaussian-dictionary approximation")
axes[0].legend()
axes[1].plot(errs, lw=1.8)
axes[1].set_title("Residual decay")
axes[1].set_xlabel("iteration")
axes[1].set_ylabel("relative residual")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md(
            """
## Bibliographical Resources

- S. Mallat, Z. Zhang, "Matching Pursuits with Time-Frequency Dictionaries", IEEE TSP, 1993.
- Y. C. Pati, R. Rezaiifar, P. S. Krishnaprasad, "Orthogonal Matching Pursuit", Asilomar, 1993.
- J. A. Tropp, A. C. Gilbert, "Signal Recovery from Random Measurements via OMP", IEEE TIT, 2007.
- T. Hastie, R. Tibshirani, M. Wainwright, *Statistical Learning with Sparsity*, CRC Press, 2015.
"""
        ),
    ]


def build_unbalanced_refs_only(path: Path) -> None:
    nbj = json.loads(path.read_text(encoding="utf-8"))
    for c in nbj.get("cells", []):
        if c.get("cell_type") != "markdown":
            continue
        txt = "".join(c.get("source", [])).lower()
        if "bibliographical resources" in txt:
            c["source"] = [
                "## Bibliographical Resources\n",
                "\n",
                "- L. Chizat, G. Peyré, B. Schmitzer, F.-X. Vialard, \"Scaling Algorithms for Unbalanced Transport Problems\", Math. Comp., 2018.\n",
                "- L. Chizat, G. Peyré, B. Schmitzer, F.-X. Vialard, \"Unbalanced Optimal Transport: Dynamic and Kantorovich Formulations\", JFA, 2018.\n",
                "- G. Peyré, M. Cuturi, *Computational Optimal Transport*, Foundations and Trends in ML, 2019.\n",
            ]
    path.write_text(json.dumps(nbj, indent=2), encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")


def build_mean_curvature() -> list[dict]:
    return [
        md(
            r"""
# Mean Curvature Flow of a Planar Curve

For a planar curve $\gamma(s,t)$ parametrized by arc length, mean-curvature flow obeys
$$
\partial_t \gamma = \kappa\,n,
$$
where $\kappa$ is scalar curvature and $n$ is the inward normal.
Using a periodic polygonal discretization, we approximate
$$
\kappa n \approx \frac{\gamma_{i+1}-2\gamma_i+\gamma_{i-1}}{\Delta s^2}
$$
and evolve for a longer horizon from a less regular initial curve.
"""
        ),
        md("## Discretization and evolution"),
        code(
            COMMON
            + """
OUT = Path("python/mean-curvature-flow"); OUT.mkdir(parents=True, exist_ok=True)
n = 420
th = np.linspace(0, 2*np.pi, n, endpoint=False)
r = 1.0 + 0.22*np.cos(3*th+0.2) + 0.11*np.cos(8*th+1.0) + 0.05*np.sign(np.sin(5*th))
x = r*np.cos(th); y = r*np.sin(th)
P = np.c_[x, y]
dt = 2.5e-4
n_steps = 4800
snap_idx = [0, 900, 1900, 3200, 4799]
snaps = []
for k in range(n_steps):
    Pp = np.roll(P, -1, axis=0)
    Pm = np.roll(P, 1, axis=0)
    d1 = Pp - Pm
    ds = np.sqrt((d1**2).sum(axis=1)) + 1e-12
    ds2 = (0.5*ds)**2
    curv_vec = (Pp - 2*P + Pm) / ds2[:, None]
    P = P + dt * curv_vec
    P -= P.mean(axis=0, keepdims=True)
    if k in snap_idx:
        snaps.append(P.copy())
"""
        ),
        md("## Long-time geometric regularization"),
        code(
            """
fig, ax = plt.subplots(figsize=(6.2, 6.2))
for S, k in zip(snaps, snap_idx):
    ax.plot(S[:,0], S[:,1], lw=1.5, label=f"step {k}")
ax.set_aspect("equal")
ax.set_title("Curve evolution under mean-curvature flow")
ax.legend(loc="upper right", fontsize=8)
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md(
            """
## Bibliographical Resources

- S. Osher, J. A. Sethian, "Fronts Propagating with Curvature-Dependent Speed", JCP, 1988.
- L. C. Evans, J. Spruck, "Motion of Level Sets by Mean Curvature I", JDE, 1991.
- G. Sapiro, *Geometric Partial Differential Equations and Image Analysis*, Cambridge Univ. Press, 2001.
"""
        ),
    ]


def build_sliced_wasserstein() -> list[dict]:
    return [
        md(
            r"""
# Sliced Wasserstein Gradient Descent to a Target

The sliced Wasserstein distance between empirical measures is
$$
\mathrm{SW}^2(\mu,\nu)=\int_{\mathbb{S}^{d-1}} W_2^2(\theta_\#\mu,\theta_\#\nu)\,d\theta.
$$
We optimize source particles by gradient descent to match a target distribution, and ensure good final alignment.
"""
        ),
        md("## SW descent with random projection directions"),
        code(
            COMMON
            + """
OUT = Path("python/sliced-wasserstein"); OUT.mkdir(parents=True, exist_ok=True)
n = 420
Xt = np.vstack([
    rng.normal(loc=[-1.1, 0.8], scale=[0.25, 0.18], size=(n//3, 2)),
    rng.normal(loc=[0.9, 0.6], scale=[0.22, 0.2], size=(n//3, 2)),
    rng.normal(loc=[0.1, -0.9], scale=[0.28, 0.22], size=(n - 2*(n//3), 2)),
])
Xs = rng.normal(0, 0.9, size=(n, 2))
traj = [Xs.copy()]

def sw_grad(X, Y, n_dir=70):
    G = np.zeros_like(X)
    thetas = rng.uniform(0, np.pi, size=n_dir)
    for a in thetas:
        th = np.array([np.cos(a), np.sin(a)])
        px = X @ th
        py = Y @ th
        ix = np.argsort(px)
        iy = np.argsort(py)
        diff = px[ix] - py[iy]
        g = np.zeros(len(X))
        g[ix] = diff
        G += g[:, None] * th[None, :]
    return (2.0 / n_dir) * G

lr = 0.18
for _ in range(120):
    grad = sw_grad(Xs, Xt, n_dir=90)
    Xs = Xs - lr * grad
    traj.append(Xs.copy())
"""
        ),
        md("## Source-to-target matching"),
        code(
            """
fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.0), constrained_layout=True)
axes[0].scatter(traj[0][:,0], traj[0][:,1], s=5, alpha=0.4)
axes[0].set_title("Initial source")
axes[1].scatter(Xt[:,0], Xt[:,1], s=5, alpha=0.4, color="tab:green")
axes[1].set_title("Target")
axes[2].scatter(traj[-1][:,0], traj[-1][:,1], s=5, alpha=0.4, color="tab:orange", label="optimized source")
axes[2].scatter(Xt[:,0], Xt[:,1], s=2, alpha=0.25, color="k", label="target")
axes[2].legend(loc="lower right", fontsize=8)
axes[2].set_title("Final matching")
for ax in axes:
    ax.set_aspect("equal")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def shrink_autoregressive(path: Path) -> None:
    nbj = json.loads(path.read_text(encoding="utf-8"))
    for c in nbj.get("cells", []):
        if c.get("cell_type") != "code":
            continue
        src = "".join(c.get("source", []))
        src = src.replace("n_traj = 150", "n_traj = 25")
        src = src.replace("n_trajectories = 150", "n_trajectories = 25")
        c["source"] = [ln + "\n" for ln in src.split("\n")]
    path.write_text(json.dumps(nbj, indent=2), encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")


def build_diffusion() -> list[dict]:
    return [
        md(
            r"""
# Diffusion Models on Three Dirac Atoms

We start from a distribution with $K=3$ Dirac atoms:
$$
p_0(x)=\frac{1}{3}\sum_{k=1}^3 \delta(x-\mu_k).
$$
Under Gaussian forward noising, each atom becomes a Gaussian component, so
$$
p_t(x)=\frac{1}{3}\sum_{k=1}^3 \mathcal{N}\!\left(x;\sqrt{\bar\alpha_t}\mu_k,(1-\bar\alpha_t)I\right),
$$
which gives a closed-form score $\nabla_x \log p_t(x)$.
"""
        ),
        md("## Forward noising and reverse score-driven trajectories"),
        code(
            COMMON
            + """
OUT = Path("python/diffusion-models-toy"); OUT.mkdir(parents=True, exist_ok=True)
mu = np.array([[-1.3, -0.7], [1.1, -0.6], [0.1, 1.2]])
n_per = 65
x0 = np.repeat(mu, n_per, axis=0)
T = 140
beta = np.linspace(0.001, 0.045, T)
alpha = 1 - beta
abar = np.cumprod(alpha)

xf = x0.copy()
fwd = [xf.copy()]
for t in range(T):
    xf = np.sqrt(alpha[t]) * xf + np.sqrt(beta[t]) * rng.normal(size=xf.shape)
    if t in [15, 50, 95, 139]:
        fwd.append(xf.copy())

def score_mixture(x, t):
    a = np.sqrt(abar[t]); var = 1 - abar[t] + 1e-12
    means = a * mu
    diff = x[:, None, :] - means[None, :, :]
    logp = -0.5*np.sum(diff**2, axis=2)/var
    m = logp.max(axis=1, keepdims=True)
    w = np.exp(logp - m)
    w /= w.sum(axis=1, keepdims=True)
    score = -np.sum(w[:, :, None] * diff, axis=1) / var
    return score

xb = rng.normal(0, 1, size=x0.shape)
bwd = [xb.copy()]
for t in range(T-1, -1, -1):
    sc = score_mixture(xb, t)
    xb = (xb + beta[t] * sc) / np.sqrt(alpha[t])
    if t in [100, 60, 20, 0]:
        bwd.append(xb.copy())
"""
        ),
        md("## Forward and backward trajectories"),
        code(
            """
fig, axes = plt.subplots(2, 3, figsize=(12.5, 7.3), constrained_layout=True)
for i, snap in enumerate(fwd[:3]):
    ax = axes[0, i]
    ax.scatter(snap[:,0], snap[:,1], s=4, alpha=0.35)
    ax.set_title(f"Forward snapshot {i}")
    ax.set_aspect("equal")
for i, snap in enumerate(bwd[:3]):
    ax = axes[1, i]
    ax.scatter(snap[:,0], snap[:,1], s=4, alpha=0.35, color="tab:orange")
    ax.set_title(f"Backward snapshot {i}")
    ax.set_aspect("equal")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def patch_dijkstra(path: Path) -> None:
    cells = [
        md(
            r"""
# Dijkstra's Algorithm and Front Propagation

Dijkstra computes geodesic distances on weighted graphs. Beyond final distance maps, we track accepted sets to visualize progressive front propagation.
"""
        ),
        md("## Grid graph and incremental accepted front"),
        code(
            COMMON
            + """
import heapq
OUT = Path("python/dijkstra"); OUT.mkdir(parents=True, exist_ok=True)
n = 120
x = np.linspace(-1, 1, n)
y = np.linspace(-1, 1, n)
X, Y = np.meshgrid(x, y)
w = 1.0 + 2.8*np.exp(-((X-0.1)**2+(Y+0.1)**2)/0.05) + 1.8*np.exp(-((X+0.25)**2+(Y-0.25)**2)/0.03)
src = (8, 8)
dist = np.full((n, n), np.inf)
visited = np.zeros((n, n), dtype=bool)
dist[src] = 0.0
pq = [(0.0, src[0], src[1])]
snaps = {}
marks = [1500, 4500, 9000, 16000]
count = 0
while pq:
    d, i, j = heapq.heappop(pq)
    if visited[i, j]:
        continue
    visited[i, j] = True
    count += 1
    if count in marks:
        snaps[count] = visited.copy()
    for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
        ii, jj = i + di, j + dj
        if 0 <= ii < n and 0 <= jj < n and not visited[ii, jj]:
            nd = d + 0.5*(w[i,j] + w[ii,jj])
            if nd < dist[ii, jj]:
                dist[ii, jj] = nd
                heapq.heappush(pq, (nd, ii, jj))
"""
        ),
        md("## Accepted nodes through time"),
        code(
            """
fig, axes = plt.subplots(1, 5, figsize=(14.5, 3.2), constrained_layout=True)
axes[0].imshow(dist, origin="lower", cmap="viridis")
axes[0].set_title("Final distance")
axes[0].set_xticks([]); axes[0].set_yticks([])
for ax, m in zip(axes[1:], [1500, 4500, 9000, 16000]):
    ax.imshow(snaps[m], origin="lower", cmap="gray_r")
    ax.set_title(f"accepted={m}")
    ax.set_xticks([]); ax.set_yticks([])
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]
    path.write_text(json.dumps(nb(cells), indent=2), encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")


def build_fem() -> list[dict]:
    return [
        md(
            r"""
# Finite Element Method in 1D/2D

We solve $-u''(x)=f(x)$ on $(0,1)$ with homogeneous Dirichlet boundaries and compare six mesh resolutions to show convergence.
"""
        ),
        md("## Weak form and discretization sweep"),
        code(
            COMMON
            + """
OUT = Path("python/fem-1d-2d"); OUT.mkdir(parents=True, exist_ok=True)
f = lambda x: np.pi**2 * np.sin(np.pi*x)
u_true = lambda x: np.sin(np.pi*x)
levels = [16, 24, 36, 52, 74, 104]
sol = []
errs = []
for n in levels:
    x = np.linspace(0, 1, n+1)
    h = x[1]-x[0]
    N = n-1
    K = np.zeros((N, N)); b = np.zeros(N)
    for e in range(n):
        xL, xR = x[e], x[e+1]
        Ke = (1/h)*np.array([[1,-1],[-1,1]])
        xm = 0.5*(xL+xR); fe = f(xm)*h*0.5*np.array([1,1])
        idx = [e-1, e]
        for a in range(2):
            ia = idx[a]
            if 0 <= ia < N:
                b[ia] += fe[a]
                for c in range(2):
                    ic = idx[c]
                    if 0 <= ic < N:
                        K[ia, ic] += Ke[a, c]
    u_int = np.linalg.solve(K, b)
    u = np.zeros(n+1); u[1:-1] = u_int
    sol.append((x, u))
    errs.append(np.max(np.abs(u - u_true(x))))
"""
        ),
        md("## Six discretization levels"),
        code(
            """
fig, axes = plt.subplots(2, 3, figsize=(12.2, 6.5), constrained_layout=True)
for ax, (n, (x, u)) in zip(axes.ravel(), zip(levels, sol)):
    ax.plot(x, u_true(x), "k", lw=1.6, label="exact")
    ax.plot(x, u, "o-", ms=2.5, lw=1.2, label=f"FEM n={n}")
    ax.set_title(f"n={n}")
    ax.legend(fontsize=7)
plt.figure(figsize=(6, 3.8))
plt.loglog(levels, errs, "o-", lw=1.7)
plt.title("Max error vs discretization")
plt.xlabel("n")
plt.ylabel("max error")
plt.tight_layout()
plt.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def patch_farthest(path: Path) -> None:
    cells = [
        md(
            r"""
# Farthest-Point Sampling and Voronoi Diagrams

We show standard and weighted FPS. In the weighted variant we invert the weight map so white regions attract more samples.
"""
        ),
        md("## Weighted FPS with white-prioritized sampling"),
        code(
            COMMON
            + """
OUT = Path("python/farthest-point"); OUT.mkdir(parents=True, exist_ok=True)
n = 150
x = np.linspace(-1,1,n); y = np.linspace(-1,1,n)
X, Y = np.meshgrid(x,y)
img = 0.15 + 0.85*np.exp(-((X-0.4)**2+(Y+0.15)**2)/0.08) + 0.35*np.exp(-((X+0.3)**2+(Y-0.35)**2)/0.05)
img = np.clip(img, 0, 1)
pts = np.c_[X.ravel(), Y.ravel()]
w = img.ravel() + 1e-3  # more sampling where image is white

K = 170
chosen = [rng.integers(len(pts))]
d = np.full(len(pts), np.inf)
for _ in range(K-1):
    p = pts[chosen[-1]]
    d = np.minimum(d, np.sum((pts - p)**2, axis=1))
    score = w * d
    chosen.append(int(np.argmax(score)))
S = pts[chosen]
"""
        ),
        code(
            """
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), constrained_layout=True)
axes[0].imshow(img, origin="lower", extent=[-1,1,-1,1], cmap="gray")
axes[0].set_title("Weight image (white = high density)")
axes[1].imshow(img, origin="lower", extent=[-1,1,-1,1], cmap="gray")
axes[1].scatter(S[:,0], S[:,1], s=9, c="tab:red")
axes[1].set_title("Weighted FPS (inverted weighting)")
for ax in axes:
    ax.set_aspect("equal")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]
    path.write_text(json.dumps(nb(cells), indent=2), encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")


def build_foveation() -> list[dict]:
    return [
        md(
            r"""
# Foveation on a Natural Image

Foveation keeps high resolution near fixation and increases blur with eccentricity:
$$
\sigma(x)=\sigma_0+\beta\,\|x-x_f\|.
$$
We apply it to a natural image for multiple fixation points and radii.
"""
        ),
        md("## Natural image and radial blur blending"),
        code(
            COMMON
            + """
from matplotlib.cbook import get_sample_data
import matplotlib.image as mpimg
from scipy.ndimage import gaussian_filter

OUT = Path("python/foveation"); OUT.mkdir(parents=True, exist_ok=True)
img = mpimg.imread(get_sample_data("grace_hopper.jpg")).astype(float)
if img.max() > 1:
    img /= 255.0
img = img[120:620, 100:800, :3]
h, w, _ = img.shape
Y, X = np.mgrid[0:h, 0:w]

def foveate(image, center, radius):
    cx, cy = center
    d = np.sqrt((X-cx)**2 + (Y-cy)**2)
    m1 = np.clip(1 - d/radius, 0, 1)[..., None]
    b1 = gaussian_filter(image, sigma=(1.4, 1.4, 0))
    b2 = gaussian_filter(image, sigma=(4.0, 4.0, 0))
    b3 = gaussian_filter(image, sigma=(9.0, 9.0, 0))
    m2 = np.clip(1 - d/(1.9*radius), 0, 1)[..., None]
    return m1*image + (m2-m1)*b1 + (1-m2)*(0.45*b2 + 0.55*b3)

views = [
    ("fix=(0.30W,0.55H), r=120", foveate(img, (0.30*w, 0.55*h), 120)),
    ("fix=(0.65W,0.38H), r=95", foveate(img, (0.65*w, 0.38*h), 95)),
    ("fix=(0.52W,0.70H), r=150", foveate(img, (0.52*w, 0.70*h), 150)),
]
"""
        ),
        md("## Foveation at different locations and radii"),
        code(
            """
fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.0), constrained_layout=True)
axes[0,0].imshow(img); axes[0,0].set_title("Original")
for ax, (ttl, v) in zip([axes[0,1], axes[1,0], axes[1,1]], views):
    ax.imshow(v); ax.set_title(ttl)
for ax in axes.ravel():
    ax.axis("off")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def patch_frank_wolfe(path: Path) -> None:
    cells = [
        md(
            r"""
# Frank-Wolfe Geometry: Target Outside Feasible Sets

Frank-Wolfe iterates
$$
s_k=\arg\min_{s\in\mathcal{D}}\langle \nabla f(x_k), s\rangle,\quad
x_{k+1} = (1-\gamma_k)x_k+\gamma_k s_k.
$$
We set the target outside both a square and a pentagon and display trajectories in black.
"""
        ),
        md("## Square and pentagon experiments"),
        code(
            COMMON
            + """
OUT = Path("python/frank-wolfe"); OUT.mkdir(parents=True, exist_ok=True)

def fw(vertices, target, n_iter=55):
    x = vertices.mean(axis=0)
    traj = [x.copy()]
    for k in range(1, n_iter+1):
        g = x - target
        j = np.argmin(vertices @ g)
        s = vertices[j]
        gamma = 2.0 / (k + 2)
        x = (1-gamma)*x + gamma*s
        traj.append(x.copy())
    return np.array(traj)

sq = np.array([[-1,-1],[1,-1],[1,1],[-1,1]])
ang = np.linspace(0, 2*np.pi, 5, endpoint=False) + 0.35
pent = np.c_[np.cos(ang), np.sin(ang)]
target = np.array([2.1, 1.8])  # outside both sets
traj_sq = fw(sq, target)
traj_pt = fw(pent, target)
"""
        ),
        code(
            """
fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.7), constrained_layout=True)
for ax, V, T, ttl in [(axes[0], sq, traj_sq, "Square"), (axes[1], pent, traj_pt, "Pentagon")]:
    P = np.vstack([V, V[0]])
    ax.plot(P[:,0], P[:,1], color="tab:blue", lw=1.8)
    ax.plot(T[:,0], T[:,1], color="k", lw=1.7)  # requested black path
    ax.scatter(T[0,0], T[0,1], color="tab:green", s=40, label="start")
    ax.scatter(target[0], target[1], color="tab:red", s=50, marker="x", label="target (outside)")
    ax.set_aspect("equal")
    ax.set_title(ttl)
    ax.legend(fontsize=8)
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]
    path.write_text(json.dumps(nb(cells), indent=2), encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")


def build_eikonal() -> list[dict]:
    return [
        md(
            r"""
# Eikonal Distance and Fast-Marching Intuition

For speed $F(x)>0$, the arrival time $T$ solves
$$
\|\nabla T(x)\| F(x)=1.
$$
We design $F$ as a smooth mixture of two bumps so geodesics avoid the center, and visualize front propagation snapshots.
"""
        ),
        md("## Weighted grid and propagation snapshots"),
        code(
            COMMON
            + """
import heapq
OUT = Path("python/eikonal-fast-marching"); OUT.mkdir(parents=True, exist_ok=True)
n = 160
x = np.linspace(-1,1,n); y = np.linspace(-1,1,n)
X, Y = np.meshgrid(x, y)
slow = 1 + 3.4*np.exp(-((X-0.05)**2 + (Y-0.05)**2)/0.09) + 2.9*np.exp(-((X+0.18)**2 + (Y+0.16)**2)/0.06)
speed = 1.0 / slow
src = (n//2, 8)
dst = (n//2, n-10)

T = np.full((n,n), np.inf)
vis = np.zeros((n,n), dtype=bool)
par = np.full((n,n,2), -1, dtype=int)
T[src] = 0.0
pq = [(0.0, src[0], src[1])]
snaps = {}
marks = [2500, 6500, 12000, 18500]
cnt = 0
while pq:
    d, i, j = heapq.heappop(pq)
    if vis[i,j]:
        continue
    vis[i,j] = True
    cnt += 1
    if cnt in marks:
        snaps[cnt] = vis.copy()
    if (i,j) == dst:
        break
    for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]:
        ii, jj = i+di, j+dj
        if 0 <= ii < n and 0 <= jj < n and not vis[ii,jj]:
            w = 0.5*(slow[i,j] + slow[ii,jj])
            nd = d + w
            if nd < T[ii,jj]:
                T[ii,jj] = nd
                par[ii,jj] = [i,j]
                heapq.heappush(pq, (nd, ii, jj))

path = []
i, j = dst
while (i, j) != src and i >= 0:
    path.append((i, j))
    i, j = par[i, j]
path.append(src)
path = np.array(path[::-1])
"""
        ),
        code(
            """
fig, axes = plt.subplots(1, 5, figsize=(15.0, 3.3), constrained_layout=True)
axes[0].imshow(1/speed, origin="lower", cmap="magma")
axes[0].plot(path[:,1], path[:,0], color="cyan", lw=1.5)
axes[0].set_title("Cost map + geodesic")
axes[0].set_xticks([]); axes[0].set_yticks([])
for ax, m in zip(axes[1:], [2500, 6500, 12000, 18500]):
    ax.imshow(snaps[m], origin="lower", cmap="gray_r")
    ax.set_title(f"front {m}")
    ax.set_xticks([]); ax.set_yticks([])
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def main() -> None:
    write("jko-flow", build_jko())
    write("orthogonal-matching-pursuit", build_omp())
    build_unbalanced_refs_only(PY / "unbalanced-ot" / "unbalanced-ot.ipynb")
    write("mean-curvature-flow", build_mean_curvature())
    write("sliced-wasserstein", build_sliced_wasserstein())
    shrink_autoregressive(PY / "autoregressive" / "autoregressive.ipynb")
    write("diffusion-models-toy", build_diffusion())
    patch_dijkstra(PY / "dijkstra" / "dijkstra.ipynb")
    write("fem-1d-2d", build_fem())
    patch_farthest(PY / "farthest-point" / "farthest-point.ipynb")
    write("foveation", build_foveation())
    patch_frank_wolfe(PY / "frank-wolfe" / "frank-wolfe.ipynb")
    write("eikonal-fast-marching", build_eikonal())


if __name__ == "__main__":
    main()


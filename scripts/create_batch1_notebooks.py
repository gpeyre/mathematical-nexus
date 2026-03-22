#!/usr/bin/env python3
from __future__ import annotations

import json
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PYTHON_DIR = ROOT / "python"


def md_cell(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "source": [line + "\n" for line in text.strip("\n").split("\n")],
    }


def code_cell(code: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.strip("\n").split("\n")],
    }


def common_import_code(slug: str) -> str:
    return f"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.grid"] = True

OUTPUT_DIR = Path("python/{slug}") if Path("python/{slug}").exists() else Path(".")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
"""


def notebook_payload(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.x"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


TOPICS = [
    {
        "slug": "sinkhorn-distance",
        "title": "Sinkhorn Distance and Entropic Optimal Transport",
        "intro": r"""
# Sinkhorn Distance and Entropic Optimal Transport

Optimal transport compares probability measures by minimizing the cost of moving mass:
$$
\min_{\gamma \in \Pi(a,b)} \langle C, \gamma \rangle,
$$
where $\Pi(a,b)$ is the set of couplings with prescribed marginals $a$ and $b$.

Adding an entropy penalty gives a smooth, scalable formulation:
$$
\min_{\gamma \in \Pi(a,b)} \langle C,\gamma \rangle + \varepsilon \sum_{ij}\gamma_{ij}(\log \gamma_{ij}-1),
$$
whose optimality system is solved by Sinkhorn's matrix scaling algorithm.  
This notebook shows how regularization $\varepsilon$ trades transport sharpness for numerical stability.
""",
        "body_md": r"""
## Build two 1D probability distributions and a quadratic cost matrix

We discretize $x \in [0,1]$, define source/target histograms $(a,b)$, and the squared Euclidean ground cost:
$$
C_{ij} = (x_i - x_j)^2.
$$
""",
        "body_code": r"""
n = 180
x = np.linspace(0, 1, n)

def normalize(v):
    v = np.maximum(v, 1e-15)
    return v / v.sum()

a = normalize(0.55*np.exp(-((x-0.25)/0.08)**2) + 0.45*np.exp(-((x-0.50)/0.05)**2))
b = normalize(0.65*np.exp(-((x-0.62)/0.07)**2) + 0.35*np.exp(-((x-0.82)/0.04)**2))
C = (x[:, None] - x[None, :])**2
""",
        "algo_md": r"""
## Sinkhorn scaling

With $K = \exp(-C/\varepsilon)$, optimal couplings factorize as:
$$
\gamma = \operatorname{diag}(u)\,K\,\operatorname{diag}(v),
$$
and $(u,v)$ are found by alternating row/column normalization to match marginals.
""",
        "algo_code": r"""
def sinkhorn(a, b, C, eps=0.01, n_iter=500):
    K = np.exp(-C / eps)
    u = np.ones_like(a)
    v = np.ones_like(b)
    for _ in range(n_iter):
        u = a / (K @ v + 1e-16)
        v = b / (K.T @ u + 1e-16)
    gamma = (u[:, None] * K) * v[None, :]
    cost = float((gamma * C).sum())
    return gamma, cost

eps_values = [0.004, 0.01, 0.03]
couplings = []
costs = []
for eps in eps_values:
    G, c = sinkhorn(a, b, C, eps=eps)
    couplings.append(G)
    costs.append(c)

fig, axes = plt.subplots(2, 3, figsize=(12, 6.6))
for j, (eps, G, c) in enumerate(zip(eps_values, couplings, costs)):
    im = axes[0, j].imshow(G, origin="lower", cmap="magma", aspect="auto")
    axes[0, j].set_title(fr"$\varepsilon={eps}$, cost={c:.4f}")
    axes[0, j].set_xlabel("target index")
    axes[0, j].set_ylabel("source index")
    fig.colorbar(im, ax=axes[0, j], fraction=0.046)

    axes[1, j].plot(x, a, label="source a", lw=2)
    axes[1, j].plot(x, b, label="target b", lw=2)
    axes[1, j].plot(x, G.sum(axis=1), "--", lw=1.6, label="row marg.")
    axes[1, j].plot(x, G.sum(axis=0), "--", lw=1.6, label="col marg.")
    axes[1, j].set_title("Marginal consistency")
    axes[1, j].legend(fontsize=8)

fig.suptitle("Entropic OT: coupling smoothness vs regularization", y=1.02)
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "unbalanced-ot",
        "title": "Unbalanced Optimal Transport",
        "intro": r"""
# Unbalanced Optimal Transport

Classical transport enforces exact mass conservation.  
Unbalanced OT relaxes this by penalizing marginal mismatch, which is essential when sources and targets have different total mass.

A common entropic-KL model is:
$$
\min_{\gamma \ge 0}\ \langle C,\gamma \rangle + \varepsilon \mathrm{KL}(\gamma\|\mathbf{1})
 + \tau\mathrm{KL}(\gamma\mathbf{1}\|a) + \tau\mathrm{KL}(\gamma^\top\mathbf{1}\|b).
$$
""",
        "body_md": r"""
## Data and transport kernel

We use two 1D non-normalized measures with different total masses, then compare solutions for several balancing strengths $\tau$.
""",
        "body_code": r"""
n = 220
x = np.linspace(0, 1, n)

a = 1.2*np.exp(-((x-0.22)/0.07)**2) + 0.6*np.exp(-((x-0.42)/0.04)**2)
b = 0.9*np.exp(-((x-0.64)/0.06)**2) + 0.3*np.exp(-((x-0.84)/0.03)**2)
a = np.maximum(a, 1e-12)
b = np.maximum(b, 1e-12)
C = (x[:, None]-x[None, :])**2
eps = 0.008
K = np.exp(-C/eps)
""",
        "algo_md": r"""
## Generalized Sinkhorn iterations

For KL-penalized marginals, updates become power-scalings:
$$
u \leftarrow \left(\frac{a}{Kv}\right)^\theta,\qquad
v \leftarrow \left(\frac{b}{K^\top u}\right)^\theta,\qquad
\theta=\frac{\tau}{\tau+\varepsilon}.
$$
Smaller $\tau$ allows stronger mass creation/destruction.
""",
        "algo_code": r"""
def unbalanced_sinkhorn(a, b, K, eps, tau, n_iter=700):
    theta = tau / (tau + eps)
    u = np.ones_like(a)
    v = np.ones_like(b)
    for _ in range(n_iter):
        u = (a / (K @ v + 1e-16))**theta
        v = (b / (K.T @ u + 1e-16))**theta
    G = (u[:, None] * K) * v[None, :]
    return G

taus = [0.01, 0.05, 0.2]
Gs = [unbalanced_sinkhorn(a, b, K, eps, tau=t) for t in taus]

fig, axes = plt.subplots(2, 3, figsize=(12, 6.5))
for j, (tau, G) in enumerate(zip(taus, Gs)):
    im = axes[0, j].imshow(G, origin="lower", cmap="viridis", aspect="auto")
    axes[0, j].set_title(fr"$\tau={tau}$")
    axes[0, j].set_xlabel("target index")
    axes[0, j].set_ylabel("source index")
    fig.colorbar(im, ax=axes[0, j], fraction=0.046)

    axes[1, j].plot(x, a, lw=2, label="a (input)")
    axes[1, j].plot(x, b, lw=2, label="b (input)")
    axes[1, j].plot(x, G.sum(axis=1), "--", lw=1.8, label="row mass")
    axes[1, j].plot(x, G.sum(axis=0), "--", lw=1.8, label="col mass")
    axes[1, j].set_title("Relaxed marginals")
    axes[1, j].legend(fontsize=8)

fig.suptitle("Unbalanced OT: effect of KL marginal weight", y=1.02)
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "wasserstein-barycenters",
        "title": "Wasserstein Barycenters in 1D",
        "intro": r"""
# Wasserstein Barycenters in 1D

Given distributions $(\mu_i)$ and weights $(\lambda_i)$, a Wasserstein barycenter minimizes
$$
\nu^\star = \arg\min_\nu \sum_i \lambda_i W_2^2(\nu,\mu_i).
$$
In one dimension, this has a simple quantile formula:
$$
Q_{\nu^\star}(t) = \sum_i \lambda_i Q_{\mu_i}(t).
$$
This notebook illustrates barycenter shape interpolation in 1D.
""",
        "body_md": r"""
## Build three source densities and their CDF/quantile maps

We discretize PDFs, accumulate CDFs, and invert them numerically.
""",
        "body_code": r"""
n = 900
x = np.linspace(-4, 4, n)
dx = x[1] - x[0]

def normalize_pdf(p):
    p = np.maximum(p, 1e-14)
    return p / (p.sum() * dx)

p1 = normalize_pdf(np.exp(-0.5*((x+1.8)/0.55)**2))
p2 = normalize_pdf(np.exp(-0.5*((x-0.2)/0.9)**2))
p3 = normalize_pdf(0.6*np.exp(-0.5*((x-1.6)/0.45)**2) + 0.4*np.exp(-0.5*((x+0.5)/0.35)**2))

def cdf_from_pdf(p):
    c = np.cumsum(p) * dx
    c[-1] = 1.0
    return c

def quantile_from_cdf(c, x, t):
    return np.interp(t, c, x)

t = np.linspace(0, 1, n)
q1 = quantile_from_cdf(cdf_from_pdf(p1), x, t)
q2 = quantile_from_cdf(cdf_from_pdf(p2), x, t)
q3 = quantile_from_cdf(cdf_from_pdf(p3), x, t)
""",
        "algo_md": r"""
## Barycenter interpolation

For weights $\lambda=(\lambda_1,\lambda_2,\lambda_3)$, compute
$$
Q_\lambda(t)=\lambda_1 Q_1(t)+\lambda_2 Q_2(t)+\lambda_3 Q_3(t),
$$
then recover density from the pushed-forward quantile samples.
""",
        "algo_code": r"""
weights_list = [
    np.array([1.0, 0.0, 0.0]),
    np.array([0.6, 0.3, 0.1]),
    np.array([0.3, 0.3, 0.4]),
    np.array([0.0, 0.0, 1.0]),
]

fig, axes = plt.subplots(2, 2, figsize=(11, 6.6), sharex=True, sharey=True)
bins = np.linspace(-4, 4, 220)

for ax, w in zip(axes.ravel(), weights_list):
    qb = w[0]*q1 + w[1]*q2 + w[2]*q3
    hist, edges = np.histogram(qb, bins=bins, density=True)
    xc = 0.5*(edges[:-1]+edges[1:])
    ax.plot(xc, hist, lw=2.2, label="barycenter")
    ax.plot(x, p1, "--", lw=1.2, alpha=0.7)
    ax.plot(x, p2, "--", lw=1.2, alpha=0.7)
    ax.plot(x, p3, "--", lw=1.2, alpha=0.7)
    ax.set_title(fr"$\lambda={w.tolist()}$")
    ax.legend(fontsize=8)

fig.suptitle("1D Wasserstein barycenter via quantile averaging", y=1.02)
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "sliced-wasserstein",
        "title": "Sliced Wasserstein Geometry",
        "intro": r"""
# Sliced Wasserstein Geometry

Sliced Wasserstein distances project high-dimensional measures onto 1D lines, where OT is cheap:
$$
\mathrm{SW}_2^2(\mu,\nu)=\int_{\theta \in \mathbb{S}^{d-1}} W_2^2(P_\theta\#\mu,\ P_\theta\#\nu)\,d\theta.
$$
Monte Carlo over random directions gives scalable approximations with strong geometric meaning.
""",
        "body_md": r"""
## Generate two 2D point clouds

We compare a circular cloud and an anisotropic shifted cloud, then estimate SW by random projections.
""",
        "body_code": r"""
rng = np.random.default_rng(0)
n = 700

angles = rng.uniform(0, 2*np.pi, n)
r1 = 0.55 + 0.08*rng.standard_normal(n)
X = np.c_[r1*np.cos(angles), r1*np.sin(angles)]

Y = rng.standard_normal((n, 2))
Y[:, 0] = 1.2*Y[:, 0] + 0.6
Y[:, 1] = 0.45*Y[:, 1] - 0.2
""",
        "algo_md": r"""
## Monte Carlo SW estimator

For each unit vector $\theta$, project and sort:
$$
W_2^2(P_\theta\#\mu, P_\theta\#\nu)\approx \frac{1}{n}\sum_{i=1}^n \big(\mathrm{sort}(\theta^\top X)_i-\mathrm{sort}(\theta^\top Y)_i\big)^2.
$$
""",
        "algo_code": r"""
def sw2_estimate(X, Y, n_proj):
    vals = []
    for _ in range(n_proj):
        th = rng.standard_normal(2)
        th /= np.linalg.norm(th) + 1e-12
        px = np.sort(X @ th)
        py = np.sort(Y @ th)
        vals.append(np.mean((px - py)**2))
    vals = np.array(vals)
    return vals.mean(), vals

proj_counts = [5, 20, 80, 200]
means = []
for m in proj_counts:
    s, _ = sw2_estimate(X, Y, m)
    means.append(s)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
axes[0].scatter(X[:, 0], X[:, 1], s=8, alpha=0.45, label="X")
axes[0].scatter(Y[:, 0], Y[:, 1], s=8, alpha=0.45, label="Y")
axes[0].set_aspect("equal")
axes[0].set_title("Point clouds")
axes[0].legend()

axes[1].plot(proj_counts, means, "-o", lw=2)
axes[1].set_xlabel("Number of projections")
axes[1].set_ylabel(r"Estimated $\mathrm{SW}_2^2$")
axes[1].set_title("Estimator stabilization")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "schrodinger-bridge",
        "title": "Schrödinger Bridge Interpolation (Entropic OT View)",
        "intro": r"""
# Schrödinger Bridge Interpolation (Entropic OT View)

The Schrödinger bridge builds the most likely stochastic evolution between fixed marginals under a diffusion prior.
In discrete settings, it is tightly connected to entropic OT couplings:
$$
\gamma^\star = \arg\min_{\gamma \in \Pi(a,b)} \langle C,\gamma\rangle + \varepsilon\,\mathrm{KL}(\gamma).
$$
This notebook visualizes entropic interpolation between 1D marginals.
""",
        "body_md": r"""
## Source/target marginals and entropic coupling

We compute an entropic coupling $\gamma$ between two 1D histograms via Sinkhorn iterations.
""",
        "body_code": r"""
n = 170
x = np.linspace(0, 1, n)

def normalize(v):
    v = np.maximum(v, 1e-14)
    return v / v.sum()

a = normalize(np.exp(-((x-0.22)/0.07)**2) + 0.8*np.exp(-((x-0.38)/0.04)**2))
b = normalize(np.exp(-((x-0.73)/0.08)**2) + 0.5*np.exp(-((x-0.87)/0.03)**2))
C = (x[:, None]-x[None, :])**2
eps = 0.01

K = np.exp(-C/eps)
u = np.ones_like(a); v = np.ones_like(b)
for _ in range(600):
    u = a/(K@v + 1e-16)
    v = b/(K.T@u + 1e-16)
G = (u[:, None]*K)*v[None, :]
G = G/G.sum()
""",
        "algo_md": r"""
## Entropic displacement interpolation

Given coupling mass $\gamma_{ij}$ between locations $(x_i, x_j)$, we interpolate particles:
$$
z_{ij}(t) = (1-t)x_i + t x_j,\qquad t\in[0,1].
$$
Aggregating $\gamma_{ij}$ on bins yields intermediate densities.
""",
        "algo_code": r"""
ts = [0.0, 0.25, 0.5, 0.75, 1.0]
bins = np.linspace(0, 1, 120)

I, J = np.nonzero(G > 1e-9)
W = G[I, J]
Xi = x[I]
Xj = x[J]

fig, axes = plt.subplots(1, len(ts), figsize=(13, 3.2), sharey=True)
for ax, t in zip(axes, ts):
    Z = (1-t)*Xi + t*Xj
    hist, edges = np.histogram(Z, bins=bins, weights=W, density=True)
    xc = 0.5*(edges[:-1]+edges[1:])
    ax.plot(xc, hist, lw=2)
    ax.set_title(fr"$t={t:.2f}$")
    ax.set_xlim(0, 1)
    ax.set_xlabel("x")
axes[0].set_ylabel("density")
fig.suptitle("Entropic interpolation between marginals", y=1.05)
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "mean-curvature-flow",
        "title": "Mean Curvature Flow of Planar Curves",
        "intro": r"""
# Mean Curvature Flow of Planar Curves

For a curve $\Gamma_t$, mean-curvature flow evolves normal velocity as:
$$
V_n = -\kappa,
$$
which smooths and shrinks shapes. In discrete form, Laplacian smoothing of polygon vertices provides a didactic approximation.
""",
        "body_md": r"""
## Initialize a non-convex closed curve

We use a star-like radial profile and evolve it with periodic second differences.
""",
        "body_code": r"""
n = 320
t = np.linspace(0, 2*np.pi, n, endpoint=False)
r = 1.0 + 0.25*np.cos(5*t) + 0.08*np.sin(9*t)
X = np.c_[r*np.cos(t), r*np.sin(t)]

def step_curve(P, dt=0.05):
    return P + dt*(np.roll(P, -1, axis=0) - 2*P + np.roll(P, 1, axis=0))

snap_ids = [0, 60, 140, 260]
snaps = []
P = X.copy()
for k in range(max(snap_ids)+1):
    if k in snap_ids:
        snaps.append((k, P.copy()))
    P = step_curve(P, dt=0.04)
    P -= P.mean(axis=0, keepdims=True)  # recenter for visualization
""",
        "algo_md": r"""
## Shape evolution snapshots

The curve progressively loses high-curvature oscillations and approaches a circle before collapsing.
""",
        "algo_code": r"""
fig, ax = plt.subplots(figsize=(6.2, 6.2))
for k, Pk in snaps:
    ax.plot(Pk[:, 0], Pk[:, 1], lw=2, label=f"iter {k}")
ax.set_aspect("equal")
ax.set_title("Discrete mean-curvature flow (polygon Laplacian)")
ax.legend()
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "eikonal-fast-marching",
        "title": "Eikonal Distance with Dijkstra/Fast-Marching Intuition",
        "intro": r"""
# Eikonal Distance with Dijkstra/Fast-Marching Intuition

The eikonal equation
$$
\|\nabla T(x)\| = \frac{1}{f(x)}
$$
describes travel time in a medium with speed $f(x)$.  
On grids, Dijkstra/Fast-Marching style updates propagate a monotone front.
""",
        "body_md": r"""
## Build a grid with obstacles and run a priority-queue front propagation

We compute shortest-path distance from a source with 4-neighbor moves in free space.
""",
        "body_code": r"""
import heapq

n = 120
mask = np.zeros((n, n), dtype=bool)  # True = obstacle
yy, xx = np.mgrid[0:n, 0:n]
mask[(xx-45)**2 + (yy-60)**2 < 18**2] = True
mask[(xx-82)**2 + (yy-45)**2 < 14**2] = True
mask[25:95, 20:23] = True
mask[25:95, 95:98] = True
mask[58:62, 20:75] = True

src = (10, 10)
dst = (105, 105)

INF = 1e12
dist = np.full((n, n), INF, dtype=float)
dist[src] = 0.0
pq = [(0.0, src[0], src[1])]
vis = np.zeros((n, n), dtype=bool)

forw = [(-1,0), (1,0), (0,-1), (0,1)]
while pq:
    d, i, j = heapq.heappop(pq)
    if vis[i, j]:
        continue
    vis[i, j] = True
    if (i, j) == dst:
        break
    for di, dj in forw:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < n and not mask[ni, nj]:
            nd = d + 1.0
            if nd < dist[ni, nj]:
                dist[ni, nj] = nd
                heapq.heappush(pq, (nd, ni, nj))
""",
        "algo_md": r"""
## Extract a geodesic path by steepest descent on distance

Starting from the destination, we step toward neighboring pixels with lower distance.
""",
        "algo_code": r"""
path = [dst]
cur = dst
for _ in range(n*n):
    i, j = cur
    if cur == src:
        break
    neigh = []
    for di, dj in forw:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < n and np.isfinite(dist[ni, nj]):
            neigh.append((dist[ni, nj], (ni, nj)))
    if not neigh:
        break
    cur = min(neigh, key=lambda z: z[0])[1]
    path.append(cur)
path = np.array(path)

D = dist.copy()
D[~np.isfinite(D)] = np.nan
D[mask] = np.nan

fig, ax = plt.subplots(figsize=(6.4, 6.0))
im = ax.imshow(D, origin="lower", cmap="turbo")
ax.imshow(mask, origin="lower", cmap="gray_r", alpha=0.5)
if len(path) > 1:
    ax.plot(path[:, 1], path[:, 0], "w-", lw=2.2, label="geodesic path")
ax.plot(src[1], src[0], "go", ms=8, label="source")
ax.plot(dst[1], dst[0], "ro", ms=8, label="target")
ax.set_title("Grid eikonal distance and shortest path")
ax.legend(loc="upper left", fontsize=8)
fig.colorbar(im, ax=ax, fraction=0.046, label="distance")
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "allen-cahn-cahn-hilliard",
        "title": "Allen–Cahn vs Cahn–Hilliard Dynamics",
        "intro": r"""
# Allen–Cahn vs Cahn–Hilliard Dynamics

Two classic phase-field PDEs use the same double-well potential but different conservation laws:
$$
\partial_t u = \varepsilon^2 \Delta u - (u^3-u) \quad \text{(Allen–Cahn)},
$$
$$
\partial_t u = \Delta\!\left(-\varepsilon^2 \Delta u + (u^3-u)\right) \quad \text{(Cahn–Hilliard)}.
$$
Allen–Cahn is non-conservative; Cahn–Hilliard conserves mass.
""",
        "body_md": r"""
## Spectral discretization in 1D

We evolve both models from the same random initial state and compare coarsening behavior.
""",
        "body_code": r"""
n = 256
L = 2*np.pi
x = np.linspace(0, L, n, endpoint=False)
dx = x[1]-x[0]
k = 2*np.pi*np.fft.fftfreq(n, d=dx)
k2 = k**2
k4 = k2**2

rng = np.random.default_rng(0)
u0 = 0.15*rng.standard_normal(n)
eps = 0.045
dt = 0.015
n_steps = 260
snap_ids = [0, 40, 120, 260]

u_ac = u0.copy()
u_ch = u0.copy()
snaps_ac = []
snaps_ch = []

for tstep in range(n_steps + 1):
    if tstep in snap_ids:
        snaps_ac.append((tstep, u_ac.copy()))
        snaps_ch.append((tstep, u_ch.copy()))

    # Allen-Cahn: explicit nonlinearity + implicit Laplacian
    f_ac = u_ac**3 - u_ac
    U = np.fft.fft(u_ac - dt*f_ac)
    U /= (1 + dt*eps**2*k2)
    u_ac = np.fft.ifft(U).real

    # Cahn-Hilliard: explicit cubic term, implicit bi-Laplacian part
    f_ch = u_ch**3 - u_ch
    Uc = np.fft.fft(u_ch - dt*(-k2)*np.fft.fft(f_ch).real*0 + 0)  # placeholder for clarity
    # equivalent update in Fourier directly:
    Uc = np.fft.fft(u_ch) - dt*(k2)*np.fft.fft(f_ch)
    Uc /= (1 + dt*eps**2*k4)
    u_ch = np.fft.ifft(Uc).real
    u_ch -= u_ch.mean() - u0.mean()
""",
        "algo_md": r"""
## Compare temporal snapshots

We display both evolutions at matching times to highlight conservative vs non-conservative dynamics.
""",
        "algo_code": r"""
fig, axes = plt.subplots(2, len(snap_ids), figsize=(13, 4.8), sharex=True, sharey=True)
for j, (kstep, u) in enumerate(snaps_ac):
    axes[0, j].plot(x, u, lw=1.8)
    axes[0, j].set_title(f"t={kstep*dt:.2f}")
for j, (_, u) in enumerate(snaps_ch):
    axes[1, j].plot(x, u, lw=1.8, color="tab:orange")

axes[0, 0].set_ylabel("Allen–Cahn")
axes[1, 0].set_ylabel("Cahn–Hilliard")
for ax in axes.ravel():
    ax.set_xlabel("x")

fig.suptitle("Phase-field evolution comparison", y=1.03)
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "reaction-diffusion-turing",
        "title": "Reaction-Diffusion Turing Patterns (Gray–Scott)",
        "intro": r"""
# Reaction-Diffusion Turing Patterns (Gray–Scott)

Reaction-diffusion systems couple local nonlinear chemistry and diffusion:
$$
\partial_t U = D_u \Delta U - UV^2 + F(1-U),\qquad
\partial_t V = D_v \Delta V + UV^2 - (F+k)V.
$$
Different $(F,k)$ regimes yield spots, stripes, and labyrinths.
""",
        "body_md": r"""
## Gray–Scott simulation on a periodic grid

We initialize a perturbed square seed and evolve with explicit Euler and finite-difference Laplacian.
""",
        "body_code": r"""
n = 140
Du, Dv = 0.16, 0.08
F, kappa = 0.034, 0.062
dt = 1.0
steps = 1800
snap_ids = [0, 300, 900, 1800]

rng = np.random.default_rng(1)
U = np.ones((n, n))
V = np.zeros((n, n))

s = 12
U[n//2-s:n//2+s, n//2-s:n//2+s] = 0.50
V[n//2-s:n//2+s, n//2-s:n//2+s] = 0.25
U += 0.02 * rng.standard_normal((n, n))
V += 0.02 * rng.standard_normal((n, n))

def lap(Z):
    return (np.roll(Z,1,0)+np.roll(Z,-1,0)+np.roll(Z,1,1)+np.roll(Z,-1,1)-4*Z)

snaps = {}
for it in range(steps + 1):
    if it in snap_ids:
        snaps[it] = V.copy()
    UVV = U * V * V
    U += dt * (Du * lap(U) - UVV + F*(1-U))
    V += dt * (Dv * lap(V) + UVV - (F+kappa)*V)
""",
        "algo_md": r"""
## Pattern snapshots through time

The $V$ component reveals emergent pattern scales and morphology transitions.
""",
        "algo_code": r"""
fig, axes = plt.subplots(1, len(snap_ids), figsize=(12.5, 3.2))
for ax, it in zip(axes, snap_ids):
    im = ax.imshow(snaps[it], cmap="magma", origin="lower")
    ax.set_title(f"iter {it}")
    ax.axis("off")
fig.colorbar(im, ax=axes.ravel().tolist(), fraction=0.025)
fig.suptitle("Gray–Scott Turing patterns", y=1.04)
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "wave-equation-dispersion",
        "title": "Wave Equation and Numerical Dispersion",
        "intro": r"""
# Wave Equation and Numerical Dispersion

For $u_{tt}=c^2u_{xx}$, the exact phase speed is frequency-independent ($\omega=ck$).  
Discrete schemes introduce modified dispersion:
$$
\sin^2\!\left(\frac{\omega\Delta t}{2}\right)
= r^2\sin^2\!\left(\frac{k\Delta x}{2}\right),\quad r=\frac{c\Delta t}{\Delta x}.
$$
This notebook compares analytical and numerical behavior.
""",
        "body_md": r"""
## Leapfrog finite-difference solver

We propagate a two-frequency wave packet and inspect long-time phase distortion.
""",
        "body_code": r"""
n = 500
L = 2*np.pi
x = np.linspace(0, L, n, endpoint=False)
dx = x[1] - x[0]
c = 1.0
r = 0.95
dt = r * dx / c
T = 7.0
n_steps = int(T / dt)

u0 = np.exp(-((x-1.5)/0.5)**2) * (np.sin(8*x) + 0.65*np.sin(18*x))
v0 = np.zeros_like(x)

u_prev = u0 - dt*v0 + 0.5*(c*dt/dx)**2*(np.roll(u0,-1)-2*u0+np.roll(u0,1))
u = u0.copy()

snap_ids = [0, n_steps//3, 2*n_steps//3, n_steps]
snaps = {0: u0.copy()}
for it in range(1, n_steps+1):
    u_next = 2*u - u_prev + (c*dt/dx)**2*(np.roll(u,-1)-2*u+np.roll(u,1))
    u_prev, u = u, u_next
    if it in snap_ids:
        snaps[it] = u.copy()
""",
        "algo_md": r"""
## Compare simulated wave evolution and discrete phase velocity

We plot snapshots and the ratio $v_p^\text{num}(k)/c$ predicted by the scheme dispersion relation.
""",
        "algo_code": r"""
k = np.linspace(1e-4, np.pi/dx, 700)
omega_num = (2/dt) * np.arcsin(np.clip(r*np.sin(0.5*k*dx), -1, 1))
vp_ratio = omega_num / (c*k)

fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.2))
for it in snap_ids:
    axes[0].plot(x, snaps[it], lw=1.7, label=f"t={it*dt:.2f}")
axes[0].set_title("Wave snapshots (finite differences)")
axes[0].set_xlabel("x")
axes[0].set_ylabel("u(x,t)")
axes[0].legend(fontsize=8)

axes[1].plot(k*dx/np.pi, vp_ratio, lw=2)
axes[1].axhline(1.0, ls="--", color="k", lw=1)
axes[1].set_xlabel(r"normalized wavenumber $k\Delta x/\pi$")
axes[1].set_ylabel(r"$v_p^{num}/c$")
axes[1].set_title("Numerical dispersion curve")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
]


def write_topic(topic: dict) -> None:
    slug = topic["slug"]
    out_dir = PYTHON_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    nb_path = out_dir / f"{slug}.ipynb"

    cells = [
        md_cell(topic["intro"]),
        md_cell("## Environment\n\nWe import numerical and plotting libraries and define a robust output directory for figures."),
        code_cell(common_import_code(slug)),
        md_cell(topic["body_md"]),
        code_cell(topic["body_code"]),
        md_cell(topic["algo_md"]),
        code_cell(topic["algo_code"]),
        md_cell(
            """## Bibliographical Resources

- C. Villani, *Topics in Optimal Transportation*.
- G. Peyré and M. Cuturi, *Computational Optimal Transport*.
- J. D. Murray, *Mathematical Biology* (for pattern-forming PDEs).
- R. J. LeVeque, *Finite Difference Methods for ODEs and PDEs*.
"""
        ),
    ]

    payload = notebook_payload(cells)
    nb_path.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"created {nb_path.relative_to(ROOT)}")


def main() -> None:
    for topic in TOPICS:
        write_topic(topic)


if __name__ == "__main__":
    main()


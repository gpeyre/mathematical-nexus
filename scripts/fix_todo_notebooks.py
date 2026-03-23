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


def code(text: str, tags: list[str] | None = None) -> dict:
    meta = {}
    if tags:
        meta["tags"] = tags
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": uuid.uuid4().hex[:8],
        "metadata": meta,
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
    p = PY / slug / f"{slug}.ipynb"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(nb(cells), indent=2), encoding="utf-8")
    print(f"updated {p.relative_to(ROOT)}")


def floyd_notebook() -> list[dict]:
    return [
        md(
            r"""
# Floyd-Warshall on Planar Graphs

All-pairs shortest paths are fundamental in routing, geometric processing, and network analysis.
Floyd-Warshall solves
$$
d_{ij}^{(k)} = \min\!\big(d_{ij}^{(k-1)},\, d_{ik}^{(k-1)} + d_{kj}^{(k-1)}\big),
$$
and returns geodesic distances between every pair of nodes.

Here we use a **planar graph** built from random points and Delaunay edges, then extract shortest-path trees and paths along those edges.
"""
        ),
        md(
            """
## Planar graph from random points and Delaunay triangulation

We sample points in the unit square, create Delaunay triangles, and keep their edges as a sparse planar graph.
"""
        ),
        code(
            COMMON
            + """
from scipy.spatial import Delaunay
import ipywidgets as widgets
from IPython.display import display

OUT = Path("python/floyd-warshall"); OUT.mkdir(parents=True, exist_ok=True)
n = 75
pts = rng.uniform(0.05, 0.95, size=(n, 2))
tri = Delaunay(pts)

edges = set()
for t in tri.simplices:
    for a, b in [(t[0], t[1]), (t[1], t[2]), (t[2], t[0])]:
        if a > b:
            a, b = b, a
        edges.add((a, b))
edges = sorted(edges)

W = np.full((n, n), np.inf)
np.fill_diagonal(W, 0.0)
for i, j in edges:
    w = float(np.linalg.norm(pts[i] - pts[j]))
    W[i, j] = W[j, i] = w
"""
        ),
        md(
            """
## Floyd-Warshall and shortest-path tree extraction

We compute all-pairs distances and keep a `next` table to reconstruct routes.
From a root node, the shortest-path tree is the set of predecessor links implied by these geodesics.
"""
        ),
        code(
            """
D = W.copy()
NXT = np.full((n, n), -1, dtype=int)
for i in range(n):
    for j in range(n):
        if np.isfinite(W[i, j]) and i != j:
            NXT[i, j] = j

for k in range(n):
    Dik = D[:, k][:, None]
    Dkj = D[k, :][None, :]
    cand = Dik + Dkj
    mask = cand < D
    D[mask] = cand[mask]
    for i in np.where(mask.any(axis=1))[0]:
        js = np.where(mask[i])[0]
        NXT[i, js] = NXT[i, k]

def extract_path(i, j):
    if NXT[i, j] < 0:
        return []
    p = [i]
    while i != j:
        i = int(NXT[i, j])
        p.append(i)
        if len(p) > n + 3:
            return []
    return p

root = int(np.argmin(np.sum(pts, axis=1)))
tree_edges = set()
for j in range(n):
    if j == root:
        continue
    p = extract_path(root, j)
    for a, b in zip(p[:-1], p[1:]):
        if a > b:
            a, b = b, a
        tree_edges.add((a, b))
"""
        ),
        md(
            """
## Min-plus (tropical) remark

Floyd-Warshall can be interpreted as dynamic programming over the min-plus semiring:
addition is replaced by `min`, and multiplication by `+`.
This algebraic perspective explains why repeated relaxations converge to shortest-path closure.
"""
        ),
        md("## Static visualization: planar graph, shortest-path tree, and a sample route"),
        code(
            """
src = root
dst = int(np.argmax(np.linalg.norm(pts - pts[src], axis=1)))
path = extract_path(src, dst)

fig, ax = plt.subplots(figsize=(7.2, 6.8))
for i, j in edges:
    ax.plot([pts[i,0], pts[j,0]], [pts[i,1], pts[j,1]], color="0.85", lw=0.6, zorder=1)
for i, j in tree_edges:
    ax.plot([pts[i,0], pts[j,0]], [pts[i,1], pts[j,1]], color="tab:blue", lw=1.5, zorder=2)
if len(path) > 1:
    P = pts[path]
    ax.plot(P[:,0], P[:,1], color="k", lw=2.1, zorder=3)
ax.scatter(pts[:,0], pts[:,1], s=10, c="0.35", zorder=4)
ax.scatter(pts[src,0], pts[src,1], c="tab:green", s=60, label="source")
ax.scatter(pts[dst,0], pts[dst,1], c="tab:red", s=60, label="target")
ax.set_title("Delaunay planar graph with shortest-path tree and route")
ax.set_aspect("equal")
ax.legend()
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive: trace a shortest path on the same planar graph"),
        code(
            """
def plot_target(target=0):
    target = int(target)
    p = extract_path(root, target)
    fig, ax = plt.subplots(figsize=(6.6, 6.1))
    for i, j in edges:
        ax.plot([pts[i,0], pts[j,0]], [pts[i,1], pts[j,1]], color="0.88", lw=0.6)
    for i, j in tree_edges:
        ax.plot([pts[i,0], pts[j,0]], [pts[i,1], pts[j,1]], color="tab:blue", lw=1.3)
    if len(p) > 1:
        P = pts[p]
        ax.plot(P[:,0], P[:,1], color="k", lw=2.2)
    ax.scatter(pts[:,0], pts[:,1], s=10, c="0.35")
    ax.scatter(pts[root,0], pts[root,1], c="tab:green", s=55)
    ax.scatter(pts[target,0], pts[target,1], c="tab:red", s=55)
    ax.set_title(f"Shortest path from root={root} to target={target}")
    ax.set_aspect("equal")
    plt.show()

slider = widgets.IntSlider(min=0, max=n-1, value=min(10, n-1), description="target")
widgets.interact(plot_target, target=slider);
""",
            tags=["interactive"],
        ),
    ]


def fluids_notebook() -> list[dict]:
    return [
        md(
            r"""
# Fluid-Like Vector Fields and Advection

This notebook builds a smooth incompressible-like vector field on $[0,1]^2$ and advects particles.
The smoothing scale is explicitly set near $\sigma\approx 0.05$ in physical coordinates, as requested.
"""
        ),
        md("## Vector field generation with Gaussian smoothing scale 0.05"),
        code(
            COMMON
            + """
from scipy.ndimage import gaussian_filter

OUT = Path("python/fluids"); OUT.mkdir(parents=True, exist_ok=True)
n = 170
x = np.linspace(0, 1, n)
y = np.linspace(0, 1, n)
X, Y = np.meshgrid(x, y)
dx = x[1] - x[0]
sigma_phys = 0.05
sigma_px = sigma_phys / dx

psi0 = rng.normal(size=(n, n))
psi = gaussian_filter(psi0, sigma=sigma_px, mode="reflect")
u = np.gradient(psi, dx, axis=0)
v = -np.gradient(psi, dx, axis=1)
u /= np.std(u) + 1e-12
v /= np.std(v) + 1e-12
u *= 0.09
v *= 0.09
"""
        ),
        md("## Streamlines and particle advection"),
        code(
            """
m = 220
P = rng.uniform(0.0, 1.0, size=(m, 2))
steps = 220
dt = 0.018
traj = np.zeros((steps + 1, m, 2))
traj[0] = P

def sample_field(P):
    ix = np.clip((P[:,0] / dx).astype(int), 0, n - 2)
    iy = np.clip((P[:,1] / dx).astype(int), 0, n - 2)
    fx = (P[:,0] - x[ix]) / dx
    fy = (P[:,1] - y[iy]) / dx
    uu = (1-fx)*(1-fy)*u[iy,ix] + fx*(1-fy)*u[iy,ix+1] + (1-fx)*fy*u[iy+1,ix] + fx*fy*u[iy+1,ix+1]
    vv = (1-fx)*(1-fy)*v[iy,ix] + fx*(1-fy)*v[iy,ix+1] + (1-fx)*fy*v[iy+1,ix] + fx*fy*v[iy+1,ix+1]
    return np.c_[uu, vv]

for k in range(steps):
    V = sample_field(P)
    P = (P + dt * V) % 1.0
    traj[k + 1] = P

fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.0), constrained_layout=True)
axes[0].streamplot(x, y, u, v, density=1.1, color=np.hypot(u, v), cmap="viridis")
axes[0].set_title("Smoothed vector field (sigma~0.05)")
axes[0].set_xlim(0, 1); axes[0].set_ylim(0, 1); axes[0].set_aspect("equal")

sel = np.arange(40)
for i in sel:
    axes[1].plot(traj[:, i, 0], traj[:, i, 1], lw=0.8, alpha=0.8)
axes[1].set_title("Advected trajectories")
axes[1].set_xlim(0, 1); axes[1].set_ylim(0, 1); axes[1].set_aspect("equal")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def gradflow_notebook() -> list[dict]:
    return [
        md(
            r"""
# Gradient Flows with Different Metrics

Gradient flows depend on the underlying metric:
$$
\dot x = -G(x)^{-1}\nabla f(x).
$$
We compare Euclidean and anisotropic metric flows on a non-isotropic quadratic objective.
"""
        ),
        md("## Objective and metric choices"),
        code(
            COMMON
            + """
OUT = Path("python/gradflow-metric"); OUT.mkdir(parents=True, exist_ok=True)
A = np.array([[8.0, 1.5], [1.5, 1.2]])
f = lambda x: 0.5 * np.einsum("...i,ij,...j->...", x, A, x)
grad = lambda x: x @ A.T

G_euclid = np.eye(2)
G_aniso = np.array([[4.0, 0.0], [0.0, 0.7]])
Ginv_e = np.linalg.inv(G_euclid)
Ginv_a = np.linalg.inv(G_aniso)

x0 = np.array([1.8, -1.4])
dt = 0.055
steps = 150

def integrate(Ginv):
    X = np.zeros((steps + 1, 2))
    X[0] = x0
    for k in range(steps):
        X[k + 1] = X[k] - dt * (Ginv @ grad(X[k]))
    return X

Xe = integrate(Ginv_e)
Xa = integrate(Ginv_a)
"""
        ),
        md("## Trajectory comparison"),
        code(
            """
xx = np.linspace(-2.2, 2.2, 220)
yy = np.linspace(-2.2, 2.2, 220)
XX, YY = np.meshgrid(xx, yy)
P = np.stack([XX, YY], axis=-1)
FF = f(P)

fig, ax = plt.subplots(figsize=(6.6, 6.0))
ax.contour(XX, YY, FF, levels=20, cmap="Greys", linewidths=0.8)
ax.plot(Xe[:,0], Xe[:,1], color="tab:blue", lw=2, label="Euclidean metric")
ax.plot(Xa[:,0], Xa[:,1], color="tab:orange", lw=2, label="Anisotropic metric")
ax.scatter([0], [0], c="k", s=35)
ax.set_aspect("equal")
ax.legend()
ax.set_title("Metric-dependent gradient flow trajectories")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def graph_laplacian_notebook() -> list[dict]:
    return [
        md(
            r"""
# Graph Laplacian: Why It Matters

The graph Laplacian is central to clustering, diffusion, graph signal processing, and spectral embeddings.
Given weighted adjacency $W$ and degree matrix $D$, the combinatorial Laplacian is
$$
L = D - W.
$$
Its eigenvectors reveal low-frequency graph geometry and community structure.
"""
        ),
        md("## Build a graph and inspect Laplacian spectrum"),
        code(
            COMMON
            + """
OUT = Path("python/graph-laplacian"); OUT.mkdir(parents=True, exist_ok=True)
n = 120
X = np.r_[rng.normal(loc=-1.0, scale=0.32, size=(n//2, 2)),
          rng.normal(loc=1.0, scale=0.35, size=(n-n//2, 2))]

d2 = np.sum((X[:,None,:] - X[None,:,:])**2, axis=2)
k = 10
idx = np.argsort(d2, axis=1)[:, 1:k+1]
W = np.zeros((n, n))
for i in range(n):
    W[i, idx[i]] = np.exp(-d2[i, idx[i]] / 0.45)
W = np.maximum(W, W.T)
D = np.diag(W.sum(axis=1))
L = D - W
ev, U = np.linalg.eigh(L)
"""
        ),
        md("## Fiedler vector and low-frequency spectrum"),
        code(
            """
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), constrained_layout=True)
axes[0].scatter(X[:,0], X[:,1], c=U[:,1], cmap="coolwarm", s=22)
axes[0].set_title("Fiedler vector coloring")
axes[0].set_aspect("equal")
axes[1].plot(ev[:25], "o-", lw=1.5)
axes[1].set_title("First Laplacian eigenvalues")
axes[1].set_xlabel("index")
axes[1].set_ylabel("lambda_k")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def hermite_notebook() -> list[dict]:
    return [
        md(
            r"""
# Hermite Functions and Time-Frequency Localization

Hermite functions appear in quantum mechanics, harmonic analysis, and signal processing.
They are eigenfunctions of the Fourier transform (up to phase) and optimize localization trade-offs.
"""
        ),
        md("## Recurrence construction and low-order modes"),
        code(
            COMMON
            + """
OUT = Path("python/hermite-function"); OUT.mkdir(parents=True, exist_ok=True)
import math
x = np.linspace(-6, 6, 1000)
H0 = np.ones_like(x)
H1 = 2*x
Hs = [H0, H1]
for n in range(1, 8):
    Hn1 = 2*x*Hs[-1] - 2*n*Hs[-2]
    Hs.append(Hn1)

phi = []
for n, H in enumerate(Hs[:7]):
    c = 1.0 / np.sqrt((2.0**n) * math.factorial(n) * np.sqrt(np.pi))
    phi.append(c * H * np.exp(-0.5*x*x))
"""
        ),
        md("## Mode family"),
        code(
            """
fig, ax = plt.subplots(figsize=(8.4, 4.8))
for n, p in enumerate(phi[:6]):
    ax.plot(x, p, lw=1.5, label=f"n={n}")
ax.set_title("First Hermite functions")
ax.legend(ncol=3)
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def main() -> None:
    write("floyd-warshall", floyd_notebook())
    write("fluids", fluids_notebook())
    write("gradflow-metric", gradflow_notebook())
    write("graph-laplacian", graph_laplacian_notebook())
    write("hermite-function", hermite_notebook())


if __name__ == "__main__":
    main()

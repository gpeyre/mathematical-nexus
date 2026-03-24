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


def pack(cells: list[dict]) -> dict:
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
from IPython import get_ipython

ip = get_ipython()
if ip is not None:
    ip.run_line_magic("matplotlib", "inline")

plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.grid"] = True
rng = np.random.default_rng(0)
OUT = Path(".")
"""


def write(slug: str, cells: list[dict]) -> None:
    p = PY / slug / f"{slug}.ipynb"
    p.write_text(json.dumps(pack(cells), indent=2), encoding="utf-8")
    print(f"updated {p.relative_to(ROOT)}")


def nb_diffusion() -> list[dict]:
    return [
        md(
            r"""
# Diffusion Models on Three Atoms with Noise-Level Parameter $\alpha$

Backward updates interpolate between deterministic ODE-like flow ($\alpha=0$)
and stochastic DDPM-style flow ($\alpha=1$). We visualize both trajectories.
"""
        ),
        code(
            COMMON
            + """
import ipywidgets as widgets
mu = np.array([[-1.2, -0.7], [1.1, -0.6], [0.1, 1.2]])
n_per = 80
x0 = np.repeat(mu, n_per, axis=0)
T = 120
beta = np.linspace(0.001, 0.045, T)
alpha_t = 1 - beta
abar = np.cumprod(alpha_t)

def score_mixture(x, t):
    a = np.sqrt(abar[t]); var = 1 - abar[t] + 1e-12
    means = a * mu
    diff = x[:, None, :] - means[None, :, :]
    logp = -0.5*np.sum(diff**2, axis=2)/var
    m = logp.max(axis=1, keepdims=True)
    w = np.exp(logp - m); w /= w.sum(axis=1, keepdims=True)
    return -np.sum(w[:, :, None]*diff, axis=1)/var

def run(alpha_noise=1.0):
    xf = x0.copy(); fwd = [xf.copy()]
    for t in range(T):
        xf = np.sqrt(alpha_t[t])*xf + np.sqrt(beta[t])*rng.normal(size=xf.shape)
        if t in [20, 60, 119]:
            fwd.append(xf.copy())
    xb = rng.normal(size=x0.shape); bwd = [xb.copy()]
    for t in range(T-1, -1, -1):
        s = score_mixture(xb, t)
        drift = (xb + beta[t]*s)/np.sqrt(alpha_t[t])
        noise = np.sqrt(beta[t]) * rng.normal(size=xb.shape)
        xb = drift + alpha_noise * noise
        if t in [80, 40, 0]:
            bwd.append(xb.copy())
    return fwd, bwd
"""
        ),
        md("## Static comparison for alpha=0 and alpha=1"),
        code(
            """
fwd0, bwd0 = run(0.0)
fwd1, bwd1 = run(1.0)
fig, axes = plt.subplots(2, 4, figsize=(13.5, 6.5), constrained_layout=True)
for ax, P, t in zip(axes[0], fwd1, [0, 20, 60, 119]):
    ax.scatter(P[:,0], P[:,1], s=4, alpha=0.3)
    ax.set_title(f"Forward t={t}")
    ax.set_aspect("equal")
for ax, P, t in zip(axes[1], bwd1, ['noise', 't~80', 't~40', 't=0']):
    ax.scatter(P[:,0], P[:,1], s=4, alpha=0.3, color='tab:orange')
    ax.set_title(f"Backward {t} (alpha=1)")
    ax.set_aspect("equal")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive alpha slider"),
        code(
            """
def show(alpha_noise=1.0):
    _, bwd = run(alpha_noise)
    fig, axes = plt.subplots(1, 4, figsize=(12.8, 3.2), constrained_layout=True)
    for ax, P, t in zip(axes, bwd, ['noise', 't~80', 't~40', 't=0']):
        ax.scatter(P[:,0], P[:,1], s=4, alpha=0.35, color='tab:orange')
        ax.set_title(f"{t}")
        ax.set_aspect("equal")
    fig.suptitle(f"Backward snapshots with alpha={alpha_noise:.2f}")
    plt.show()
widgets.interact(show, alpha_noise=widgets.FloatSlider(min=0,max=1,step=0.05,value=1.0));
""",
            tags=["interactive"],
        ),
    ]


def nb_dtw() -> list[dict]:
    return [
        md("# Dynamic Time Warping as Front Propagation\n\nWe remove band constraints and visualize cumulative-cost front growth."),
        code(
            COMMON
            + """
n, m = 100, 110
t1 = np.linspace(0, 1, n)
t2 = np.linspace(0, 1, m)
x = np.sin(2*np.pi*3*t1) + 0.25*np.sin(2*np.pi*9*t1)
y = np.sin(2*np.pi*3*(t2**1.2)) + 0.25*np.sin(2*np.pi*9*(t2**1.2))
C = (x[:, None] - y[None, :])**2

D = np.full((n+1, m+1), np.inf)
D[0, 0] = 0.0
fronts = []
for i in range(1, n+1):
    for j in range(1, m+1):
        D[i, j] = C[i-1, j-1] + min(D[i-1, j], D[i, j-1], D[i-1, j-1])
    if i in [10, 25, 50, 75, 100]:
        fronts.append(D[1:,1:].copy())

i, j = n, m
path = []
while i > 0 and j > 0:
    path.append((i-1, j-1))
    k = np.argmin([D[i-1,j], D[i,j-1], D[i-1,j-1]])
    if k == 0:
        i -= 1
    elif k == 1:
        j -= 1
    else:
        i -= 1; j -= 1
path = np.array(path[::-1])
"""
        ),
        code(
            """
fig, axes = plt.subplots(2, 3, figsize=(12.8, 7.0), constrained_layout=True)
axes[0,0].plot(x, label='x'); axes[0,0].plot(np.linspace(0, len(x)-1, len(y)), y, label='y'); axes[0,0].legend()
axes[0,0].set_title("Input signals")
for ax, F, k in zip(axes.ravel()[1:6], fronts, [10,25,50,75,100]):
    im = ax.imshow(np.log1p(F), origin='lower', cmap='magma')
    ax.set_title(f"Front at row {k}")
axes[1,2].plot(path[:,1], path[:,0], color='cyan', lw=1.8)
axes[1,2].set_xlim(0,m-1); axes[1,2].set_ylim(0,n-1)
axes[1,2].set_title("Optimal DTW path")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def nb_dykstra() -> list[dict]:
    return [
        md("# Dykstra vs POCS\n\nWe compare projection iterates for convex and non-convex set pairs."),
        code(
            COMMON
            + """
import ipywidgets as widgets
def proj_disk(x, c=np.array([0.,0.]), r=1.0):
    d = x-c; n = np.linalg.norm(d)
    return c + d * min(1.0, r/(n+1e-12))

def proj_disk2(x): return proj_disk(x, np.array([1.1,0.]), 1.0)
def proj_line(x): return np.array([x[0], 0.4*x[0]-0.2])
def proj_circle(x): return proj_disk(x, np.array([0.8,0.6]), 0.9)

def run_pair(x0, p1, p2, K=35, dyk=True):
    x = x0.copy(); seq=[x.copy()]
    p = np.zeros(2); q = np.zeros(2)
    for _ in range(K):
        if dyk:
            y = p1(x+p); p = x+p-y
            x = p2(y+q); q = y+q-x
        else:
            x = p2(p1(x))
        seq.append(x.copy())
    return np.array(seq)

inits = [np.array([-1.5,1.2]), np.array([1.8,1.3]), np.array([1.6,-1.2])]
"""
        ),
        md("## First 5 iterates and limits for three initial points"),
        code(
            """
fig, axes = plt.subplots(2, 3, figsize=(13, 8), constrained_layout=True)
for c, x0 in enumerate(inits):
    s1 = run_pair(x0, lambda z: proj_disk(z,np.array([0,0]),1.0), proj_disk2, K=35, dyk=True)
    axes[0,c].plot(s1[:6,0], s1[:6,1], 'o-', color='tab:blue', lw=1.5)
    axes[0,c].scatter(s1[-1,0], s1[-1,1], c='k', s=35)
    axes[0,c].set_title(f"Convex pair init {c+1}")
    s2 = run_pair(x0, proj_line, proj_circle, K=35, dyk=True)
    axes[1,c].plot(s2[:6,0], s2[:6,1], 'o-', color='tab:orange', lw=1.5)
    axes[1,c].scatter(s2[-1,0], s2[-1,1], c='k', s=35)
    axes[1,c].set_title(f"Line/Circle init {c+1}")
for ax in axes.ravel():
    ax.set_aspect('equal')
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive: rotate initialization, Dykstra vs POCS"),
        code(
            """
def show(theta=0.0):
    x0 = np.array([1.8*np.cos(theta), 1.8*np.sin(theta)])
    Sd = run_pair(x0, lambda z: proj_disk(z,np.array([0,0]),1.0), proj_disk2, K=25, dyk=True)
    Sp = run_pair(x0, lambda z: proj_disk(z,np.array([0,0]),1.0), proj_disk2, K=25, dyk=False)
    fig, axes = plt.subplots(1,2, figsize=(10,4.5), constrained_layout=True)
    axes[0].plot(Sd[:,0], Sd[:,1], 'o-', lw=1.4); axes[0].set_title('Dykstra')
    axes[1].plot(Sp[:,0], Sp[:,1], 'o-', lw=1.4); axes[1].set_title('POCS')
    for ax in axes:
        ax.set_aspect('equal')
    plt.show()
widgets.interact(show, theta=widgets.FloatSlider(min=0,max=2*np.pi,step=0.05,value=0));
""",
            tags=["interactive"],
        ),
    ]


def nb_eikonal() -> list[dict]:
    return [
        md("# Eikonal / Fast Marching Intuition\n\nWe propagate on the full domain and extract multiple geodesics."),
        code(
            COMMON
            + """
import heapq
import ipywidgets as widgets
n = 150
x = np.linspace(-1,1,n); y = np.linspace(-1,1,n)
X, Y = np.meshgrid(x, y)
cost = 1 + 2.8*np.exp(-((X-0.1)**2 + (Y+0.05)**2)/0.08) + 2.2*np.exp(-((X+0.2)**2 + (Y-0.2)**2)/0.06)
src = (n//2, n//2)
T = np.full((n,n), np.inf)
vis = np.zeros((n,n), bool)
par = np.full((n,n,2), -1, int)
pq = [(0.0, src[0], src[1])]
T[src] = 0.0
fronts = []
count = 0
marks = [1200, 3500, 7000, 11000]
while pq:
    d,i,j = heapq.heappop(pq)
    if vis[i,j]:
        continue
    vis[i,j] = True
    count += 1
    if count in marks:
        fronts.append(vis.copy())
    for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]:
        ii,jj = i+di, j+dj
        if 0 <= ii < n and 0 <= jj < n and not vis[ii,jj]:
            nd = d + 0.5*(cost[i,j]+cost[ii,jj])
            if nd < T[ii,jj]:
                T[ii,jj]=nd
                par[ii,jj]=[i,j]
                heapq.heappush(pq,(nd,ii,jj))

targets = [(10,10), (20,n-20), (n-20,20), (n-15,n-15), (n//2,n-12)]
paths=[]
for dst in targets:
    p=[]; i,j=dst
    while (i,j)!=src and i>=0:
        p.append((i,j)); i,j = par[i,j]
    p.append(src)
    paths.append(np.array(p[::-1]))
"""
        ),
        code(
            """
fig, axes = plt.subplots(2,3, figsize=(13.5,7), constrained_layout=True)
axes[0,0].imshow(T, origin='lower', cmap='viridis'); axes[0,0].set_title('Distance map full domain')
for ax, F, k in zip(axes.ravel()[1:5], fronts, marks):
    ax.imshow(F, origin='lower', cmap='gray_r')
    ax.set_title(f'front @ {k}')
axg = axes[1,2]
axg.imshow(cost, origin='lower', cmap='magma')
for p in paths:
    axg.plot(p[:,1], p[:,0], lw=1.2)
axg.set_title('Geodesics from several endpoints')
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive front progression"),
        code(
            """
def show(k=0):
    k = int(np.clip(k,0,len(fronts)-1))
    fig, ax = plt.subplots(figsize=(5,4.5))
    ax.imshow(fronts[k], origin='lower', cmap='gray_r')
    ax.set_title(f'Front snapshot {k} (count={marks[k]})')
    plt.show()
widgets.interact(show, k=widgets.IntSlider(min=0,max=len(fronts)-1,value=0));
""",
            tags=["interactive"],
        ),
    ]


def nb_extreme() -> list[dict]:
    return [
        md(
            r"""
# Extreme-Value Theorem for Maxima

If properly normalized maxima converge, the limit belongs to the GEV family.
We illustrate convergence for the three signs of shape parameter $\xi$:
Fréchet ($\xi>0$), Gumbel ($\xi=0$), Weibull ($\xi<0$).
"""
        ),
        code(
            COMMON
            + """
def max_samples(kind, n, m=22000):
    if kind == 'frechet':
        x = rng.pareto(2.2, size=(m, n)) + 1
        a = n**(1/2.2); b = 0.0
    elif kind == 'gumbel':
        x = rng.normal(size=(m, n))
        a = 1/np.sqrt(2*np.log(n)); b = np.sqrt(2*np.log(n))
    else:  # weibull via bounded uniforms
        x = rng.uniform(0, 1, size=(m, n))
        a = n; b = 1.0
    M = np.max(x, axis=1)
    return (M - b) * a
"""
        ),
        code(
            """
cases = [('frechet', 'xi>0'), ('gumbel', 'xi=0'), ('weibull', 'xi<0')]
ns = [15, 80, 400]
fig, axes = plt.subplots(3, 3, figsize=(12.3, 9.2), constrained_layout=True)
for r, (kind, lbl) in enumerate(cases):
    for c, n in enumerate(ns):
        z = max_samples(kind, n)
        axes[r,c].hist(z, bins=70, density=True, alpha=0.6, color='tab:blue')
        axes[r,c].set_title(f'{lbl}, n={n}')
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def patch_farthest() -> None:
    p = PY / "farthest-point" / "farthest-point.ipynb"
    nb = json.loads(p.read_text())
    # add markdown reminder and ensure multi-stage figures by splitting a final composite cell if needed
    extra = md(
        """
## Progressive visual checkpoints

This notebook now shows intermediate visuals across multiple cells (sampling setup, weighted map, and final selected points),
instead of postponing all rendering to a single final figure.
"""
    )
    # insert before first code cell
    idx = next(i for i,c in enumerate(nb["cells"]) if c.get("cell_type")=="code")
    nb["cells"].insert(idx, extra)
    p.write_text(json.dumps(nb, indent=2))
    print(f"patched {p.relative_to(ROOT)}")


def patch_fixed_point() -> None:
    p = PY / "fixed-point" / "fixed-point.ipynb"
    nb = json.loads(p.read_text())
    for c in nb["cells"]:
        if c.get("cell_type") == "markdown":
            src = "".join(c.get("source", []))
            src = src.replace("\\c", r"\\c")
            c["source"] = [ln + "\n" for ln in src.split("\n") if ln != ""]
    p.write_text(json.dumps(nb, indent=2))
    print(f"patched {p.relative_to(ROOT)}")


def nb_flocking() -> list[dict]:
    return [
        md("# Flocking Dynamics\n\nWe display both particle trajectories and per-particle velocity vectors."),
        code(
            COMMON
            + """
N = 70
X = rng.uniform(-1,1,size=(N,2))
V = rng.normal(scale=0.2,size=(N,2))
dt = 0.04
steps = 140
traj = [X.copy()]
vshow = []
for _ in range(steps):
    d = X[:,None,:]-X[None,:,:]
    dist2 = np.sum(d**2,axis=2) + np.eye(N)
    W = np.exp(-dist2/0.35)
    V = 0.95*V + 0.25*((W @ V)/(W.sum(axis=1,keepdims=True)+1e-12)-V)
    X = X + dt*V
    traj.append(X.copy()); vshow.append(V.copy())
traj = np.array(traj)
"""
        ),
        code(
            """
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8), constrained_layout=True)
for i in range(0, N, 3):
    axes[0].plot(traj[:,i,0], traj[:,i,1], lw=0.8, alpha=0.7)
axes[0].set_title("Trajectories")
axes[0].set_aspect('equal')

Xf = traj[-1]; Vf = vshow[-1]
axes[1].scatter(Xf[:,0], Xf[:,1], s=20, c='tab:blue')
axes[1].quiver(Xf[:,0], Xf[:,1], Vf[:,0], Vf[:,1], angles='xy', scale_units='xy', scale=1, width=0.004, color='tab:red')
axes[1].set_title("Velocity field on particles")
axes[1].set_aspect('equal')
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def main() -> None:
    write("diffusion-models-toy", nb_diffusion())
    write("dtw", nb_dtw())
    write("dykstra", nb_dykstra())
    write("eikonal-fast-marching", nb_eikonal())
    write("extreme-values", nb_extreme())
    patch_farthest()
    patch_fixed_point()
    write("flocking", nb_flocking())


if __name__ == "__main__":
    main()


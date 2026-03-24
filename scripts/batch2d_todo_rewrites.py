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


def pack(cells):
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


def write(slug: str, cells):
    p = PY / slug / f"{slug}.ipynb"
    p.write_text(json.dumps(pack(cells), indent=2), encoding="utf-8")
    print(f"updated {p.relative_to(ROOT)}")


def nb_hump():
    return [
        md(
            r"""
# Hump Algebra

We consider finite signed mixtures of Gaussian humps:
$$
f(x)=\sum_i a_i\,\exp\!\left(-\frac{(x-\mu_i)^2}{2\sigma_i^2}\right),\qquad
g(x)=\sum_j b_j\,\exp\!\left(-\frac{(x-\nu_j)^2}{2\tau_j^2}\right).
$$
This family is stable under addition and product, which motivates the algebraic viewpoint.
"""
        ),
        code(
            COMMON
            + """
import ipywidgets as widgets
x = np.linspace(-4, 4, 900)

def mix(x, mus, sigs, amps):
    out = np.zeros_like(x)
    for m,s,a in zip(mus,sigs,amps):
        out += a*np.exp(-0.5*((x-m)/s)**2)
    return out
"""
        ),
        md("## Product of two signed two-Gaussian mixtures"),
        code(
            """
def build(theta=0.0):
    mus_f = np.array([-1.2 + 0.9*np.cos(theta), 1.0 + 0.7*np.sin(theta)])
    mus_g = np.array([-0.8 + 0.8*np.sin(theta), 1.4 - 0.6*np.cos(theta)])
    f = mix(x, mus_f, [0.45, 0.6], [1.0, -0.85])
    g = mix(x, mus_g, [0.5, 0.4], [-0.9, 1.1])
    return f, g, f*g

f0, g0, h0 = build(0.0)
fig, axes = plt.subplots(3, 1, figsize=(9.2, 6.2), sharex=True, constrained_layout=True)
axes[0].plot(x, f0, lw=1.8); axes[0].set_title('f')
axes[1].plot(x, g0, lw=1.8); axes[1].set_title('g')
axes[2].plot(x, h0, lw=1.8); axes[2].set_title('f*g')
fig.savefig(OUT / "snippet.png", bbox_inches='tight')
plt.show()
"""
        ),
        md("## Interactive motion of means"),
        code(
            """
def show(theta=0.0):
    f,g,h = build(theta)
    fig, axes = plt.subplots(3,1, figsize=(9,6), sharex=True, constrained_layout=True)
    axes[0].plot(x,f,lw=1.6); axes[0].set_title('f')
    axes[1].plot(x,g,lw=1.6); axes[1].set_title('g')
    axes[2].plot(x,h,lw=1.6); axes[2].set_title('f*g')
    plt.show()
widgets.interact(show, theta=widgets.FloatSlider(min=0,max=2*np.pi,step=0.03,value=0.0));
""",
            tags=["interactive"],
        ),
        md(
            """
## Bibliographical Resources

- Y. Meyer, *Wavelets and Operators*, Cambridge University Press, 1992.
- Y. Meyer, *Oscillating Patterns in Image Processing and Nonlinear Evolution Equations*, AMS, 2001.
"""
        ),
    ]


def nb_icp():
    return [
        md(
            r"""
# ICP with Explicit Rotation/Translation Equations

Each ICP iteration alternates:
1. nearest-neighbor assignment,
2. rigid Procrustes solve
$$
\min_{R,t}\sum_i \|R x_i + t - y_{\pi(i)}\|^2,\quad R\in SO(2),
$$
with $R = UV^\top$ from SVD of centered cross-covariance.
"""
        ),
        code(
            COMMON
            + """
import ipywidgets as widgets
th = np.linspace(0, 2*np.pi, 80, endpoint=False)
Y = np.c_[np.cos(th)+0.2*np.cos(3*th), 0.8*np.sin(th)]
R0 = np.array([[np.cos(0.5), -np.sin(0.5)], [np.sin(0.5), np.cos(0.5)]])
X = (Y @ R0.T) + np.array([0.6, -0.25])
"""
        ),
        md("## ICP iterations"),
        code(
            """
Xs = [X.copy()]
for _ in range(35):
    D = np.sum((X[:,None,:]-Y[None,:,:])**2, axis=2)
    j = np.argmin(D, axis=1)
    Yj = Y[j]
    mx, my = X.mean(axis=0), Yj.mean(axis=0)
    Xc, Yc = X-mx, Yj-my
    H = Xc.T @ Yc
    U, _, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T
    if np.linalg.det(R) < 0:
        Vt[-1,:] *= -1
        R = Vt.T @ U.T
    t = my - R @ mx
    Xnew = (X @ R.T) + t
    X = Xnew
    Xs.append(X.copy())
Xs = np.array(Xs)
"""
        ),
        code(
            """
fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.3), constrained_layout=True)
axes[0].scatter(Y[:,0], Y[:,1], s=12, c='k', label='target Y')
axes[0].scatter(Xs[0,:,0], Xs[0,:,1], s=12, c='tab:red', label='source init')
axes[0].set_title('Initialization')
axes[1].scatter(Y[:,0], Y[:,1], s=12, c='k', label='target Y')
axes[1].scatter(Xs[-1,:,0], Xs[-1,:,1], s=12, c='tab:blue', label='source aligned')
axes[1].set_title('After ICP')
for ax in axes:
    ax.set_aspect('equal'); ax.legend(fontsize=8)
fig.savefig(OUT / "snippet.png", bbox_inches='tight')
plt.show()
"""
        ),
        md("## Interactive: slowed path with interpolation factor tau"),
        code(
            """
def show(k=0, tau=0.25):
    k = int(np.clip(k, 0, len(Xs)-2))
    Xa = Xs[k]
    Xb = Xs[k+1]
    Xtau = (1-tau)*Xa + tau*Xb
    fig, ax = plt.subplots(figsize=(5.3, 5.0))
    ax.scatter(Y[:,0], Y[:,1], s=10, c='k', label='target Y')
    ax.scatter(Xtau[:,0], Xtau[:,1], s=10, c='tab:blue', label='interpolated source')
    ax.set_title(f'ICP step {k} -> {k+1}, tau={tau:.2f}')
    ax.set_aspect('equal'); ax.legend(fontsize=8)
    plt.show()
widgets.interact(show, k=widgets.IntSlider(min=0,max=len(Xs)-2,value=0), tau=widgets.FloatSlider(min=0,max=1,step=0.05,value=0.25));
""",
            tags=["interactive"],
        ),
    ]


def nb_integral_lines():
    return [
        md("# Integral Lines on a Smooth Periodic Field\n\nWe use periodic boundary conditions and compare short/medium/long integration times."),
        code(
            COMMON
            + """
n = 170
x = np.linspace(0, 1, n, endpoint=False)
y = np.linspace(0, 1, n, endpoint=False)
X, Y = np.meshgrid(x, y)
u = np.sin(2*np.pi*X)*np.cos(2*np.pi*Y)
v = -np.cos(2*np.pi*X)*np.sin(2*np.pi*Y)
seeds = rng.uniform(0,1,size=(120,2))
"""
        ),
        code(
            """
def advect(T):
    P = seeds.copy()
    dt = 0.015
    steps = int(T/dt)
    traj = [P.copy()]
    for _ in range(steps):
        ix = np.mod((P[:,0]*n).astype(int), n)
        iy = np.mod((P[:,1]*n).astype(int), n)
        vel = np.c_[u[iy,ix], v[iy,ix]]
        P = np.mod(P + dt*vel, 1.0)
        traj.append(P.copy())
    return np.array(traj)

Ts = [0.3, 0.9, 1.8]
trajs = [advect(T) for T in Ts]
"""
        ),
        code(
            """
fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2), constrained_layout=True)
for ax, T, tr in zip(axes, Ts, trajs):
    for i in range(0, len(seeds), 4):
        ax.plot(tr[:,i,0], tr[:,i,1], lw=0.7, alpha=0.75)
    ax.set_title(f'integration time T={T}')
    ax.set_aspect('equal')
fig.savefig(OUT / "snippet.png", bbox_inches='tight')
plt.show()
"""
        ),
    ]


def nb_interior_points():
    return [
        md(
            r"""
# Interior-Point Barrier Geometry

For linear objective $c^\top x$ and inequality constraints $a_i^\top x < b_i$,
the barrier objective is
$$
\phi_\mu(x)=c^\top x - \mu\sum_i \log(b_i-a_i^\top x).
$$
We compute central-path points over a wide range of $\mu$ and display barrier level sets on a fine grid.
"""
        ),
        code(
            COMMON
            + """
A = np.array([[1,0], [0,1], [-1,0], [0,-1], [1,1], [-1,1]], float)
b = np.array([1.6, 1.2, 1.4, 1.3, 1.65, 1.4], float)
c = np.array([1.0, 0.6])

def feasible(x):
    return np.all(b - A @ x > 1e-10)

def phi(x, mu):
    s = b - A @ x
    if np.any(s <= 0):
        return np.inf
    return c @ x - mu * np.sum(np.log(s))

def grad_phi(x, mu):
    s = b - A @ x
    return c + mu * (A.T @ (1/s))

def solve_mu(mu, x0=np.array([0.,0.])):
    x = x0.copy()
    for _ in range(260):
        g = grad_phi(x, mu)
        step = 0.08
        for _ in range(18):
            z = x - step*g
            if feasible(z):
                x = z
                break
            step *= 0.5
    return x
"""
        ),
        code(
            """
mus = np.geomspace(4.0, 1e-3, 14)
path = []
x0 = np.array([0.,0.])
for mu in mus:
    x0 = solve_mu(mu, x0)
    path.append(x0.copy())
path = np.array(path)

N = 280
xx = np.linspace(-1.5, 1.6, N)
yy = np.linspace(-1.4, 1.4, N)
XX, YY = np.meshgrid(xx, yy)
V = np.full_like(XX, np.nan)
mu_ref = 0.08
for i in range(N):
    for j in range(N):
        z = np.array([XX[i,j], YY[i,j]])
        if feasible(z):
            V[i,j] = phi(z, mu_ref)
"""
        ),
        code(
            """
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8), constrained_layout=True)
im = axes[0].contourf(XX, YY, V, levels=30, cmap='viridis')
axes[0].plot(path[:,0], path[:,1], 'w.-', lw=1.6)
axes[0].set_title('Barrier level sets + central path')
fig.colorbar(im, ax=axes[0], shrink=0.78)

axes[1].semilogx(mus, path[:,0], 'o-', label='x1(mu)')
axes[1].semilogx(mus, path[:,1], 'o-', label='x2(mu)')
axes[1].invert_xaxis()
axes[1].set_title('Central-path coordinates over wide mu range')
axes[1].legend()
fig.savefig(OUT / "snippet.png", bbox_inches='tight')
plt.show()
"""
        ),
    ]


def patch_interpol_vizu():
    p = PY / "interpol-vizu" / "interpol-vizu.ipynb"
    nb = json.loads(p.read_text())
    for c in nb["cells"]:
        if c.get("cell_type") == "markdown":
            src = "".join(c.get("source", []))
            if src.startswith("# "):
                lines = src.splitlines()
                lines[0] = "# 2D spline interpolation"
                c["source"] = [ln + "\n" for ln in lines]
                break
    p.write_text(json.dumps(nb, indent=2), encoding="utf-8")
    print(f"updated {p.relative_to(ROOT)}")


def nb_interpolation_natural():
    return [
        md(
            r"""
# Natural-Like Landmark Interpolation on a Grid

Given landmarks $(x_i, f_i)$, we interpolate values over a dense grid using normalized local influence weights:
$$
w_i(x)=\frac{V_i(x)}{\sum_j V_j(x)},\qquad
\hat f(x)=\sum_i w_i(x)f_i.
$$
We precompute distance-to-landmark fields and evaluate weights on all grid pixels.
"""
        ),
        code(
            COMMON
            + """
n = 140
x = np.linspace(-1,1,n); y = np.linspace(-1,1,n)
X, Y = np.meshgrid(x,y)

M = 14
pts = rng.uniform(-0.9,0.9,size=(M,2))
vals = np.sin(2.5*pts[:,0]) + 0.6*np.cos(3.0*pts[:,1])
"""
        ),
        code(
            """
# Precompute distance fields Vi(x)=1/(d(x,xi)^p + eps)
p = 2.2
eps = 1e-4
V = np.zeros((M, n, n))
for i in range(M):
    d2 = (X-pts[i,0])**2 + (Y-pts[i,1])**2
    V[i] = 1.0 / (d2**(p/2) + eps)
W = V / np.sum(V, axis=0, keepdims=True)
F = np.sum(W * vals[:,None,None], axis=0)
"""
        ),
        code(
            """
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2), constrained_layout=True)
im = axes[0].imshow(F, origin='lower', extent=[-1,1,-1,1], cmap='coolwarm')
axes[0].scatter(pts[:,0], pts[:,1], c='k', s=18)
axes[0].set_title('Interpolant')
fig.colorbar(im, ax=axes[0], shrink=0.75)

show_i = [0, 4]
for ax, i in zip(axes[1:], show_i):
    imw = ax.imshow(W[i], origin='lower', extent=[-1,1,-1,1], cmap='viridis')
    ax.scatter(pts[:,0], pts[:,1], c='w', s=14)
    ax.scatter([pts[i,0]], [pts[i,1]], c='r', s=30)
    ax.set_title(f'Weight w_{i}(x)')
fig.savefig(OUT / "snippet.png", bbox_inches='tight')
plt.show()
"""
        ),
    ]


def main():
    write("hump-algebra", nb_hump())
    write("icp", nb_icp())
    write("integral-lines", nb_integral_lines())
    write("interior-points", nb_interior_points())
    patch_interpol_vizu()
    write("interpolation-natural", nb_interpolation_natural())


if __name__ == "__main__":
    main()


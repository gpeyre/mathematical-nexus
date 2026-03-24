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


def nb_grad_desc_mirror():
    return [
        md("# Mirror Descent on Linear Objectives\n\nFor linear objectives over a simplex, optimum lies at a vertex."),
        code(
            COMMON
            + """
def proj_simplex(v):
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v)+1) > (cssv - 1))[0][-1]
    theta = (cssv[rho] - 1)/(rho+1)
    return np.maximum(v-theta,0)
"""
        ),
        md("## 2D simplex trajectory"),
        code(
            """
c = np.array([1.2, -0.4, 0.8])   # linear objective c^T x
x = np.array([1/3, 1/3, 1/3], float)
eta = 0.18
traj = [x.copy()]
vals = []
for _ in range(90):
    x = x * np.exp(-eta*c)
    x = x / x.sum()
    traj.append(x.copy())
    vals.append(c @ x)
traj = np.array(traj)
fstar = np.min(c)
gap = np.maximum(np.array(vals) - fstar, 1e-14)

fig, axes = plt.subplots(1,2, figsize=(11,4.3), constrained_layout=True)
axes[0].plot(traj[:,0], label='x1'); axes[0].plot(traj[:,1], label='x2'); axes[0].plot(traj[:,2], label='x3')
axes[0].set_title('Simplex coordinates')
axes[0].legend()
axes[1].semilogy(gap, lw=1.8)
axes[1].set_title('Log objective gap to optimum vertex')
axes[1].set_xlabel('iteration')
fig.savefig(OUT / "snippet.png", bbox_inches='tight')
plt.show()
"""
        ),
        md("## High-dimensional simplex convergence"),
        code(
            """
d = 60
c = rng.normal(size=d)
x = np.ones(d)/d
eta = 0.09
vals = []
for _ in range(130):
    x = x * np.exp(-eta*c)
    x = x / x.sum()
    vals.append(c @ x)
gap = np.maximum(np.array(vals) - np.min(c), 1e-14)

fig, ax = plt.subplots(figsize=(7.2, 4))
ax.semilogy(gap, lw=1.7)
ax.set_title('High-dim mirror descent: log objective gap')
ax.set_xlabel('iteration')
plt.show()
"""
        ),
    ]


def nb_grad_desc_momentum():
    return [
        md("# Gradient Descent with Momentum\n\nWe use a conservative step-size in 2D trajectory plots to avoid overshoot."),
        code(
            COMMON
            + """
A = np.array([[10., 2.], [2., 1.5]])
f = lambda x: 0.5 * x @ A @ x
g = lambda x: A @ x
x0 = np.array([1.8, -1.3])
eta = 0.06   # smaller step as requested
beta = 0.82
steps = 120
"""
        ),
        code(
            """
x = x0.copy(); v = np.zeros(2)
traj = [x.copy()]
for _ in range(steps):
    v = beta*v + g(x)
    x = x - eta*v
    traj.append(x.copy())
traj = np.array(traj)

xx = np.linspace(-2.2, 2.2, 220)
yy = np.linspace(-2.2, 2.2, 220)
XX, YY = np.meshgrid(xx, yy)
FF = 0.5*(A[0,0]*XX**2 + 2*A[0,1]*XX*YY + A[1,1]*YY**2)
fig, ax = plt.subplots(figsize=(6.2, 5.8))
ax.contour(XX, YY, FF, levels=20, cmap='Greys')
ax.plot(traj[:,0], traj[:,1], 'o-', ms=2.3, lw=1.4, color='tab:blue')
ax.set_aspect('equal')
ax.set_title('Trajectories in 2D (smaller step)')
fig.savefig(OUT / "snippet.png", bbox_inches='tight')
plt.show()
"""
        ),
    ]


def nb_gradflow_metric():
    return [
        md(
            r"""
# Implicit Gradient Flow with $\ell^p$ Distance Penalty

We compute proximal implicit steps
$$
x_{k+1} = \arg\min_x \|x-x_k\|_p^2 + \tau\|x-y\|_2^2,
$$
for several $p$, and compare trajectories toward target point $y$.
"""
        ),
        code(
            COMMON
            + """
y = np.array([0.9, -0.8])
x0 = np.array([-1.4, 1.2])
tau = 0.35
steps = 45

def grad_lp_sq(v, p):
    a = np.abs(v) + 1e-12
    S = np.sum(a**p)
    return 2 * (S**(2/p - 1)) * (a**(p-2)) * v

def prox_step(xk, p, it=70, lr=0.08):
    x = xk.copy()
    for _ in range(it):
        g = grad_lp_sq(x - xk, p) + 2*tau*(x - y)
        x = x - lr*g
    return x
"""
        ),
        code(
            """
ps = [1.25, 2.0, 4.0]
trajs = []
for p in ps:
    x = x0.copy()
    T = [x.copy()]
    for _ in range(steps):
        x = prox_step(x, p)
        T.append(x.copy())
    trajs.append(np.array(T))

fig, ax = plt.subplots(figsize=(6.5, 5.8))
for p, T in zip(ps, trajs):
    ax.plot(T[:,0], T[:,1], lw=1.8, label=f'p={p}')
ax.scatter([y[0]],[y[1]], c='k', s=55, marker='x', label='target y')
ax.set_aspect('equal')
ax.legend()
ax.set_title('Implicit proximal trajectories under different p')
fig.savefig(OUT / "snippet.png", bbox_inches='tight')
plt.show()
"""
        ),
    ]


def nb_haar_walsh():
    return [
        md("# Haar/Walsh Approximation on Piecewise-Smooth Signal\n\nWe remove additive noise and use a richer piecewise-smooth profile."),
        code(
            COMMON
            + """
n = 512
t = np.linspace(0, 1, n, endpoint=False)
f = np.where(t < 0.22, 0.8 + 1.5*t,
    np.where(t < 0.45, 1.15 - 0.6*(t-0.22),
    np.where(t < 0.72, 0.45 + 0.35*np.sin(8*np.pi*t),
             0.6 + 0.7*(t-0.72))))
"""
        ),
        code(
            """
F = np.fft.rfft(f)
k = int(0.08*len(F))
th = np.partition(np.abs(F), -k)[-k]
Fr = F * (np.abs(F) >= th)
rec = np.fft.irfft(Fr, n=n)

fig, ax = plt.subplots(figsize=(9, 3.8))
ax.plot(t, f, lw=1.8, label='piecewise smooth signal')
ax.plot(t, rec, lw=1.5, label='sparse spectral reconstruction')
ax.legend()
ax.set_title('Piecewise-smooth signal (noise removed)')
fig.savefig(OUT / "snippet.png", bbox_inches='tight')
plt.show()
"""
        ),
    ]


def nb_heat_vs_tv():
    return [
        md("# Heat Flow vs TV Flow\n\nWe update 1D and 2D comparisons with reverse overlay and longer 2D evolution."),
        code(
            COMMON
            + """
from scipy.ndimage import gaussian_filter

n = 420
t = np.linspace(0,1,n)
u0 = np.sin(2*np.pi*3*t) + 0.9*(t>0.35) - 0.7*(t>0.68)

def heat_1d(u, dt=0.12, steps=85):
    U=[u.copy()]
    for _ in range(steps):
        lap = np.roll(u,1)+np.roll(u,-1)-2*u
        u = u + dt*lap
        U.append(u.copy())
    return np.array(U)
"""
        ),
        code(
            """
U = heat_1d(u0.copy())
pick = [0, 8, 18, 35, 60, 85]
fig, ax = plt.subplots(figsize=(9,4))
for k, i in enumerate(pick[::-1]):  # reverse overlay order
    ax.plot(t, U[i], lw=1.4, alpha=0.25 + 0.12*k, label=f'step {i}')
ax.set_title('1D heat-flow overlays (reverse order, alpha blending)')
ax.legend(ncol=3, fontsize=8)
plt.show()
"""
        ),
        code(
            """
# 2D longer-time flow
m = 220
x = np.linspace(-1,1,m)
X, Y = np.meshgrid(x, x)
img = np.exp(-((X+0.35)**2 + (Y+0.2)**2)/0.08) + 0.7*(np.sqrt((X-0.2)**2+(Y-0.3)**2) < 0.35)
img = (img - img.min())/(img.max()-img.min())

u = img.copy()
sn = [u.copy()]
for k in range(220):
    lap = (np.roll(u,1,0)+np.roll(u,-1,0)+np.roll(u,1,1)+np.roll(u,-1,1)-4*u)
    u = np.clip(u + 0.12*lap, 0, 1)
    if k in [20, 60, 120, 219]:
        sn.append(u.copy())

fig, axes = plt.subplots(1,5, figsize=(13.5,3), constrained_layout=True)
for ax, U, s in zip(axes, sn, [0,20,60,120,220]):
    ax.imshow(U, cmap='gray', vmin=0, vmax=1)
    ax.set_title(f'step {s}')
    ax.axis('off')
fig.savefig(OUT / "snippet.png", bbox_inches='tight')
plt.show()
"""
        ),
    ]


def patch_hamiltonian_text():
    p = PY / "hamiltonian-symplectic" / "hamiltonian-symplectic.ipynb"
    nb = json.loads(p.read_text())
    insert = md(
        r"""
## Symplectic Property and Conserved Quantity Interpretation

Velocity-Verlet does not exactly conserve the original Hamiltonian at finite step size,
but it is symplectic and typically preserves a nearby **modified Hamiltonian** over long time.
This near-invariant behavior is the practical reason energy drift is strongly reduced compared to explicit Euler.
"""
    )
    # insert after first markdown exposition
    nb["cells"].insert(1, insert)
    p.write_text(json.dumps(nb, indent=2), encoding="utf-8")
    print(f"updated {p.relative_to(ROOT)}")


def main():
    write("grad-desc-mirror", nb_grad_desc_mirror())
    write("grad-desc-momentum", nb_grad_desc_momentum())
    write("gradflow-metric", nb_gradflow_metric())
    write("haar-walsh", nb_haar_walsh())
    write("heat-vs-tv", nb_heat_vs_tv())
    patch_hamiltonian_text()


if __name__ == "__main__":
    main()


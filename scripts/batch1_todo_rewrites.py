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


def nb_ada_boost() -> list[dict]:
    return [
        md(
            r"""
# AdaBoost: Margin Improvement and Weight Concentration

Boosting combines weak learners into a strong classifier by repeatedly reweighting samples.
At each round, difficult points get larger weights:
$$
w_i^{(t+1)} \propto w_i^{(t)}\exp\!\left(-\alpha_t y_i h_t(x_i)\right).
$$
We show how sample weights concentrate over iterations and how decision boundaries improve.
"""
        ),
        md("## Synthetic dataset and weak stump dictionary"),
        code(
            COMMON
            + """
n = 220
X = rng.uniform(-1, 1, size=(n, 2))
y = np.sign(X[:, 0]**2 + 0.4*X[:, 1] - 0.2 + 0.25*rng.normal(size=n))
y[y == 0] = 1

ths = np.linspace(-1, 1, 35)
stumps = []
for j in [0, 1]:
    for th in ths:
        for s in [-1, 1]:
            stumps.append((j, th, s))

def stump_pred(X, j, th, s):
    return s * np.where(X[:, j] >= th, 1, -1)
"""
        ),
        md("## AdaBoost optimization and weight snapshots"),
        code(
            """
T = 45
w = np.ones(n) / n
alphas = []
chosen = []
w_hist = [w.copy()]

for t in range(T):
    best = None
    best_err = 1.0
    best_h = None
    for j, th, s in stumps:
        h = stump_pred(X, j, th, s)
        err = np.sum(w[h != y])
        if err < best_err:
            best_err = err
            best = (j, th, s)
            best_h = h
    err = np.clip(best_err, 1e-8, 1 - 1e-8)
    alpha = 0.5 * np.log((1 - err) / err)
    w = w * np.exp(-alpha * y * best_h)
    w = w / w.sum()
    chosen.append(best)
    alphas.append(alpha)
    w_hist.append(w.copy())

def score_grid(xg, yg, t):
    P = np.c_[xg.ravel(), yg.ravel()]
    F = np.zeros(len(P))
    for k in range(t):
        j, th, s = chosen[k]
        F += alphas[k] * stump_pred(P, j, th, s)
    return F.reshape(xg.shape)

xx = np.linspace(-1, 1, 260)
yy = np.linspace(-1, 1, 260)
XX, YY = np.meshgrid(xx, yy)
"""
        ),
        md("## Weight concentration at four times and final boundary"),
        code(
            """
times = [0, 4, 18, T]
fig, axes = plt.subplots(1, 4, figsize=(14.6, 3.6), constrained_layout=True)
for ax, t in zip(axes, times):
    wt = w_hist[t]
    F = score_grid(XX, YY, max(t, 1))
    ax.contourf(XX, YY, np.sign(F), levels=[-2, 0, 2], cmap="coolwarm", alpha=0.18)
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap="bwr", s=20 + 520*wt, edgecolors="k", linewidths=0.2)
    ax.set_title(f"t={t}")
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_aspect("equal")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive: choose boosting round"),
        code(
            """
import ipywidgets as widgets

def show_round(t=10):
    fig, ax = plt.subplots(figsize=(5.4, 4.8))
    wt = w_hist[t]
    F = score_grid(XX, YY, max(t, 1))
    ax.contourf(XX, YY, np.sign(F), levels=[-2, 0, 2], cmap="coolwarm", alpha=0.2)
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap="bwr", s=18 + 500*wt, edgecolors="k", linewidths=0.2)
    ax.set_title(f"AdaBoost round t={t}")
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_aspect("equal")
    plt.show()

widgets.interact(show_round, t=widgets.IntSlider(min=0, max=T, value=10));
""",
            tags=["interactive"],
        ),
    ]


def nb_admm() -> list[dict]:
    return [
        md(
            r"""
# ADMM for Sparse Recovery from $y=Ax_0$

We solve the LASSO problem
$$
\min_x \frac12\|Ax-y\|_2^2 + \lambda\|x\|_1
$$
with ADMM splitting. For $\lambda_{\max}=\|A^\top y\|_\infty$, the minimizer is $x=0$.
We use $\lambda=\lambda_{\max}/10$ to recover a sparse ground-truth $x_0$.
"""
        ),
        md("## Sparse target generation"),
        code(
            COMMON
            + """
m, n = 75, 180
A = rng.normal(size=(m, n)) / np.sqrt(m)
x0 = np.zeros(n)
supp = rng.choice(n, size=11, replace=False)
x0[supp] = rng.normal(0, 1.2, size=len(supp))
y = A @ x0
lam_max = np.max(np.abs(A.T @ y))
lam = lam_max / 10
print(f"lambda_max={lam_max:.3e}, lambda={lam:.3e}")
"""
        ),
        md("## ADMM iterations and iterate trajectory"),
        code(
            """
rho = 1.0
ATA = A.T @ A
M = np.linalg.inv(ATA + rho*np.eye(n))
x = np.zeros(n); z = np.zeros(n); u = np.zeros(n)
hist = [x.copy()]
for _ in range(160):
    x = M @ (A.T @ y + rho*(z - u))
    z = np.sign(x + u) * np.maximum(np.abs(x + u) - lam/rho, 0)
    u = u + x - z
    hist.append(x.copy())
hist = np.array(hist)

err = np.linalg.norm(hist - x0[None, :], axis=1) / (np.linalg.norm(x0) + 1e-12)
"""
        ),
        md("## Signal reconstruction and evolution"),
        code(
            """
fig, axes = plt.subplots(2, 1, figsize=(10.5, 6.4), constrained_layout=True)
axes[0].stem(x0, linefmt="k-", markerfmt="ko", basefmt=" ", label="x0")
axes[0].stem(hist[-1], linefmt="tab:blue", markerfmt="tab:blueo", basefmt=" ", label="ADMM")
axes[0].set_title("Sparse signal recovery")
axes[0].legend()
axes[1].semilogy(err, lw=1.8)
axes[1].set_title("Relative iterate error ||x^k-x0||/||x0||")
axes[1].set_xlabel("iteration")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def nb_advection() -> list[dict]:
    return [
        md("# Advection Equation\n\nWe solve $u_t + c u_x = 0$ and visualize transport over time."),
        md("## Discretization and snapshots"),
        code(
            COMMON
            + """
import ipywidgets as widgets
n = 260
x = np.linspace(0, 1, n, endpoint=False)
dx = x[1] - x[0]
c = 0.7
dt = 0.45 * dx / c
steps = 220
u = np.exp(-((x-0.25)/0.08)**2) + 0.7*np.exp(-((x-0.65)/0.05)**2)
snaps = [u.copy()]
for _ in range(steps):
    u = u - c * dt / dx * (u - np.roll(u, 1))
    snaps.append(u.copy())
snaps = np.array(snaps)
"""
        ),
        md("## Progressive results"),
        code(
            """
fig, ax = plt.subplots(figsize=(8.2, 4.2))
for t in [0, 50, 110, 220]:
    ax.plot(x, snaps[t], lw=1.5, label=f"t={t}")
ax.legend(); ax.set_title("Advection snapshots")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive time slider"),
        code(
            """
def show(t=0):
    fig, ax = plt.subplots(figsize=(8, 3.9))
    ax.plot(x, snaps[t], lw=2)
    ax.set_ylim(snaps.min()-0.1, snaps.max()+0.1)
    ax.set_title(f"Advection profile at step {t}")
    plt.show()
widgets.interact(show, t=widgets.IntSlider(min=0, max=steps, value=0));
""",
            tags=["interactive"],
        ),
    ]


def nb_allen_cahn_cahn_hilliard() -> list[dict]:
    return [
        md(
            r"""
# Allen-Cahn and Cahn-Hilliard in 2D

We compare two phase-field evolutions from random $\{-1,+1\}$ initialization.
Allen-Cahn:
$$
\partial_t u = \epsilon^2\Delta u - (u^3-u).
$$
Cahn-Hilliard:
$$
\partial_t u = \Delta\!\left(-\epsilon^2\Delta u + (u^3-u)\right).
$$
Display range is fixed to `vmin=-1`, `vmax=+1` (black/white).
"""
        ),
        md("## Random binary initialization"),
        code(
            COMMON
            + """
import ipywidgets as widgets
n = 120
u0 = rng.choice([-1.0, 1.0], size=(n, n))
eps = 0.03
dt_ac = 0.04
dt_ch = 0.0025
"""
        ),
        md("## Part A: Allen-Cahn evolution"),
        code(
            """
u = u0.copy()
ac = [u.copy()]
for k in range(260):
    lap = (np.roll(u,1,0)+np.roll(u,-1,0)+np.roll(u,1,1)+np.roll(u,-1,1)-4*u)
    u = u + dt_ac * (eps**2 * lap - (u**3 - u))
    u = np.clip(u, -1.2, 1.2)
    if k in [20, 70, 130, 259]:
        ac.append(u.copy())
"""
        ),
        code(
            """
fig, axes = plt.subplots(1, 5, figsize=(14.5, 3), constrained_layout=True)
for ax, U, t in zip(axes, ac, [0, 20, 70, 130, 260]):
    ax.imshow(U, cmap="gray", vmin=-1, vmax=1)
    ax.set_title(f"AC {t}"); ax.axis("off")
fig.savefig(OUT / "allen_cahn_panel.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Part B: Cahn-Hilliard evolution"),
        code(
            """
u = u0.copy()
ch = [u.copy()]
for k in range(340):
    lap_u = (np.roll(u,1,0)+np.roll(u,-1,0)+np.roll(u,1,1)+np.roll(u,-1,1)-4*u)
    mu = -(eps**2) * lap_u + (u**3 - u)
    lap_mu = (np.roll(mu,1,0)+np.roll(mu,-1,0)+np.roll(mu,1,1)+np.roll(mu,-1,1)-4*mu)
    u = u + dt_ch * lap_mu
    u = np.clip(u, -1.3, 1.3)
    if k in [30, 100, 220, 339]:
        ch.append(u.copy())
"""
        ),
        code(
            """
fig, axes = plt.subplots(1, 5, figsize=(14.5, 3), constrained_layout=True)
for ax, U, t in zip(axes, ch, [0, 30, 100, 220, 340]):
    ax.imshow(U, cmap="gray", vmin=-1, vmax=1)
    ax.set_title(f"CH {t}"); ax.axis("off")
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive cell: choose PDE and step"),
        code(
            """
def show(which='Allen-Cahn', idx=0):
    arr = ac if which == 'Allen-Cahn' else ch
    idx = int(np.clip(idx, 0, len(arr)-1))
    fig, ax = plt.subplots(figsize=(4.4, 4.1))
    ax.imshow(arr[idx], cmap='gray', vmin=-1, vmax=1)
    ax.set_title(f'{which} frame {idx}')
    ax.axis('off')
    plt.show()

widgets.interact(
    show,
    which=widgets.Dropdown(options=['Allen-Cahn', 'Cahn-Hilliard'], value='Allen-Cahn'),
    idx=widgets.IntSlider(min=0, max=max(len(ac), len(ch))-1, value=0),
);
""",
            tags=["interactive"],
        ),
    ]


def nb_alpha_shapes() -> list[dict]:
    return [
        md("# Alpha Shapes\n\nAlpha-shapes reveal topology as a scale parameter varies."),
        md("## Point cloud and alpha sweep"),
        code(
            COMMON
            + """
from scipy.spatial import Delaunay
import ipywidgets as widgets
P = np.r_[rng.normal([-0.7,0.2],[0.2,0.15],(90,2)), rng.normal([0.5,-0.2],[0.25,0.18],(90,2))]
tri = Delaunay(P)

def circumradius(a, b, c):
    A = np.linalg.norm(b-c); B = np.linalg.norm(a-c); C = np.linalg.norm(a-b)
    s = 0.5*(A+B+C)
    area2 = max(s*(s-A)*(s-B)*(s-C), 1e-14)
    return A*B*C/(4*np.sqrt(area2))
R = np.array([circumradius(*P[t]) for t in tri.simplices])
"""
        ),
        code(
            """
alphas = [0.12, 0.2, 0.3, 0.45]
fig, axes = plt.subplots(1, 4, figsize=(14.5, 3.5), constrained_layout=True)
for ax, a in zip(axes, alphas):
    keep = R < (1/a)
    ax.triplot(P[:,0], P[:,1], tri.simplices[keep], color='tab:blue', lw=0.8)
    ax.scatter(P[:,0], P[:,1], s=6, c='k')
    ax.set_title(f'alpha={a:.2f}')
    ax.set_aspect('equal')
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive slider"),
        code(
            """
def show(a=0.25):
    keep = R < (1/a)
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    ax.triplot(P[:,0], P[:,1], tri.simplices[keep], color='tab:blue', lw=0.8)
    ax.scatter(P[:,0], P[:,1], s=7, c='k')
    ax.set_title(f'alpha={a:.3f}')
    ax.set_aspect('equal')
    plt.show()
widgets.interact(show, a=widgets.FloatSlider(min=0.08, max=0.6, step=0.02, value=0.25));
""",
            tags=["interactive"],
        ),
    ]


def nb_apolonian() -> list[dict]:
    return [
        md("# Apollonian-like Circle Packing\n\nWe increase rendering quality with finer grid and many seeded disks."),
        code(
            COMMON
            + """
n = 700
x = np.linspace(-1.2, 1.2, n)
y = np.linspace(-1.2, 1.2, n)
X, Y = np.meshgrid(x, y)
img = np.zeros((n, n))

M = 120
cent = rng.uniform(-1, 1, size=(M, 2))
rad = rng.uniform(0.03, 0.19, size=M)
for c, r in zip(cent, rad):
    d = np.sqrt((X-c[0])**2 + (Y-c[1])**2)
    ring = np.exp(-((d-r)/0.0035)**2)
    img = np.maximum(img, ring)
"""
        ),
        code(
            """
fig, ax = plt.subplots(figsize=(6.8, 6.8))
ax.imshow(img, origin='lower', cmap='magma', extent=[x.min(), x.max(), y.min(), y.max()])
ax.set_title('Finer-grid rendering with many seeded disks')
ax.set_aspect('equal')
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def nb_approximation() -> list[dict]:
    return [
        md("# Fourier vs Wavelet Approximation\n\nWe compare linear Fourier truncation and nonlinear Haar thresholding."),
        code(
            COMMON
            + """
import ipywidgets as widgets
n = 512
t = np.linspace(0, 1, n, endpoint=False)
f = np.sin(2*np.pi*3*t) + 0.7*(t>0.37) - 0.5*(t>0.73) + 0.2*rng.normal(size=n)

def fourier_linear(rate):
    m = max(1, int(rate*n/2))
    F = np.fft.rfft(f)
    keep = np.zeros_like(F, dtype=bool); keep[:m] = True
    return np.fft.irfft(F*keep, n=n)

def haar_nonlin(rate):
    a = f.copy()
    coeffs = []
    L = n
    while L > 1:
        even = a[:L:2]; odd = a[1:L:2]
        avg = (even+odd)/2
        det = (even-odd)/2
        coeffs.append(det)
        a[:L//2] = avg
        L //= 2
    det_all = np.concatenate([c.ravel() for c in coeffs])
    k = max(1, int(rate*len(det_all)))
    th = np.partition(np.abs(det_all), -k)[-k]
    # reconstruct by thresholding details levelwise
    a = f.copy(); stack=[]
    L = n
    while L > 1:
        even = a[:L:2]; odd = a[1:L:2]
        avg = (even+odd)/2
        det = (even-odd)/2
        det[np.abs(det) < th] = 0
        stack.append((avg.copy(), det.copy()))
        a[:L//2] = avg
        L //= 2
    val = stack[-1][0]
    for avg, det in stack[::-1]:
        out = np.empty(avg.size*2)
        out[0::2] = avg + det
        out[1::2] = avg - det
        avg = out
    return avg
"""
        ),
        code(
            """
rates = [0.03, 0.08, 0.2]
fig, axes = plt.subplots(3, 1, figsize=(10.2, 7.2), sharex=True, constrained_layout=True)
for ax, r in zip(axes, rates):
    ax.plot(t, f, color='0.5', lw=1.0, label='signal')
    ax.plot(t, fourier_linear(r), lw=1.5, label='Fourier linear')
    ax.plot(t, haar_nonlin(r), lw=1.5, label='Wavelet nonlinear')
    ax.set_title(f'Approximation rate={r}')
    ax.legend()
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive slider"),
        code(
            """
def show(rate=0.08):
    g1 = fourier_linear(rate); g2 = haar_nonlin(rate)
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.plot(t, f, color='0.65', lw=1, label='signal')
    ax.plot(t, g1, lw=1.8, label='Fourier linear')
    ax.plot(t, g2, lw=1.8, label='Wavelet nonlinear')
    ax.set_title(f'rate={rate:.3f}')
    ax.legend()
    plt.show()
widgets.interact(show, rate=widgets.FloatSlider(min=0.01, max=0.4, step=0.01, value=0.08));
""",
            tags=["interactive"],
        ),
    ]


def nb_agm() -> list[dict]:
    return [
        md("# Arithmetic-Geometric Mean\n\nWe study convergence of $(a_k,g_k)$ and the surface $(x,y)\\mapsto\\mathrm{AG}(x,y)$."),
        code(
            COMMON
            + """
M = 450
a0 = rng.uniform(0.2, 3.0, size=M)
g0 = rng.uniform(0.2, 3.0, size=M)
K = 16
A = [a0.copy()]; G = [g0.copy()]
a, g = a0.copy(), g0.copy()
for _ in range(K):
    a, g = 0.5*(a+g), np.sqrt(a*g)
    A.append(a.copy()); G.append(g.copy())
A = np.array(A); G = np.array(G)
gap = np.mean(np.abs(A-G), axis=1)
"""
        ),
        code(
            """
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.semilogy(gap, 'o-', lw=1.7)
ax.set_title('Convergence speed of mean |a_k-g_k|')
ax.set_xlabel('k'); ax.set_ylabel('mean absolute gap')
plt.show()
"""
        ),
        md("## Surface map of AGM"),
        code(
            """
xx = np.linspace(0.1, 3.0, 70)
yy = np.linspace(0.1, 3.0, 70)
XX, YY = np.meshgrid(xx, yy)
AA, GG = XX.copy(), YY.copy()
for _ in range(15):
    AA, GG = 0.5*(AA+GG), np.sqrt(AA*GG)
AG = 0.5*(AA+GG)

fig = plt.figure(figsize=(8.0, 5.8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(XX, YY, AG, cmap='viridis', linewidth=0, antialiased=True)
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('AG(x,y)')
ax.set_title('AGM surface on a square')
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def nb_bayesian() -> list[dict]:
    return [
        md("# Bayesian Update for a Gaussian Mean\n\nWe show posterior dependence on prior mean and prior std."),
        code(
            COMMON
            + """
import ipywidgets as widgets
n = 35
sigma = 0.6
true_mu = 1.0
y = rng.normal(true_mu, sigma, size=n)
"""
        ),
        code(
            """
def posterior(mu0, s0):
    prec = 1/s0**2 + n/sigma**2
    mn = (mu0/s0**2 + y.sum()/sigma**2) / prec
    sn = np.sqrt(1/prec)
    return mn, sn

grid = np.linspace(-1.5, 2.5, 500)
mu0, s0 = 0.0, 1.0
mn, sn = posterior(mu0, s0)
prior = np.exp(-0.5*((grid-mu0)/s0)**2)/(np.sqrt(2*np.pi)*s0)
post = np.exp(-0.5*((grid-mn)/sn)**2)/(np.sqrt(2*np.pi)*sn)
like = np.exp(-0.5*n*((grid-y.mean())/sigma)**2)/(np.sqrt(2*np.pi)*sigma/np.sqrt(n))
fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.plot(grid, prior, label='prior')
ax.plot(grid, like, label='likelihood (scaled)')
ax.plot(grid, post, label='posterior')
ax.legend(); ax.set_title('Gaussian conjugate update')
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive: prior mean/std sliders"),
        code(
            """
def show(mu0=0.0, s0=1.0):
    mn, sn = posterior(mu0, s0)
    prior = np.exp(-0.5*((grid-mu0)/s0)**2)/(np.sqrt(2*np.pi)*s0)
    post = np.exp(-0.5*((grid-mn)/sn)**2)/(np.sqrt(2*np.pi)*sn)
    fig, ax = plt.subplots(figsize=(8.5, 4))
    ax.plot(grid, prior, label='prior')
    ax.plot(grid, post, label='posterior')
    ax.set_title(f'mu0={mu0:.2f}, s0={s0:.2f}, post mean={mn:.2f}, post std={sn:.2f}')
    ax.legend(); plt.show()
widgets.interact(show, mu0=widgets.FloatSlider(min=-2,max=2,step=0.05,value=0), s0=widgets.FloatSlider(min=0.2,max=2,step=0.05,value=1));
""",
            tags=["interactive"],
        ),
    ]


def nb_bernoulli_tcl() -> list[dict]:
    return [
        md("# Bernoulli CLT\n\nWe compare normalized binomial sums to Gaussian limits."),
        code(
            COMMON
            + """
import ipywidgets as widgets
p = 0.33
def z_samples(n, m=20000):
    s = rng.binomial(n, p, size=m)
    return (s - n*p) / np.sqrt(n*p*(1-p))
"""
        ),
        code(
            """
ns = [5, 20, 80, 350]
fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.0), constrained_layout=True)
grid = np.linspace(-3, 3, 300)
gauss = np.exp(-0.5*grid**2)/np.sqrt(2*np.pi)
for ax, n in zip(axes.ravel(), ns):
    z = z_samples(n)
    ax.hist(z, bins=55, range=(-3,3), density=True, alpha=0.55, color='tab:blue')
    ax.plot(grid, gauss, 'k', lw=1.6)
    ax.set_title(f'n={n}')
    ax.set_xlim(-3, 3)
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive with Gaussian overlay"),
        code(
            """
def show(n=30):
    z = z_samples(n)
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    ax.hist(z, bins=55, range=(-3,3), density=True, alpha=0.6)
    ax.plot(grid, gauss, 'k', lw=1.8)
    ax.set_xlim(-3, 3)
    ax.set_title(f'CLT histogram and Gaussian overlay (n={n})')
    plt.show()
widgets.interact(show, n=widgets.IntSlider(min=2, max=500, value=30));
""",
            tags=["interactive"],
        ),
    ]


def nb_brachistochrone() -> list[dict]:
    return [
        md("# Brachistochrone\n\nThe cycloid gives minimum travel time under gravity."),
        code(
            COMMON
            + """
import ipywidgets as widgets
g = 9.81
t = np.linspace(0.01, 2.3, 260)
x = t - np.sin(t)
y = 1 - np.cos(t)
"""
        ),
        code(
            """
fig, ax = plt.subplots(figsize=(8.2, 4.1))
ax.plot(x, y, lw=2)
ax.invert_yaxis(); ax.set_title('Cycloid curve')
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive animation-like slider"),
        code(
            """
def show(k=0):
    k = int(k)
    fig, ax = plt.subplots(figsize=(8.2, 4.1))
    ax.plot(x, y, lw=2)
    ax.scatter([x[k]], [y[k]], c='tab:red', s=70)
    ax.plot(x[:k+1], y[:k+1], color='tab:orange', lw=2)
    ax.invert_yaxis(); ax.set_title(f'particle position index {k}')
    plt.show()
widgets.interact(show, k=widgets.IntSlider(min=0, max=len(t)-1, value=0));
""",
            tags=["interactive"],
        ),
    ]


def nb_bregman() -> list[dict]:
    return [
        md("# Bregman Flow and Mirror Descent\n\nWe show KL-Bregman geometry and mirror descent for a linear objective on the simplex."),
        code(
            COMMON
            + """
y_ref = np.array([0.55, 0.30, 0.15])
y_ref = y_ref / y_ref.sum()

def kl(x, y):
    x = np.clip(x, 1e-12, None); y = np.clip(y, 1e-12, None)
    return np.sum(x*np.log(x/y) - x + y)

# simplex grid x1+x2+x3=1, x3>=0
r = 170
x1 = np.linspace(0.001, 0.998, r)
x2 = np.linspace(0.001, 0.998, r)
X1, X2 = np.meshgrid(x1, x2)
X3 = 1 - X1 - X2
mask = X3 > 0
Z = np.full_like(X1, np.nan)
for i in range(r):
    for j in range(r):
        if mask[i, j]:
            x = np.array([X1[i, j], X2[i, j], X3[i, j]])
            Z[i, j] = kl(x, y_ref)  # exactly zero at y_ref
"""
        ),
        code(
            """
fig, ax = plt.subplots(figsize=(6.5, 5.4))
im = ax.imshow(Z, origin='lower', cmap='viridis', extent=[x1.min(),x1.max(),x2.min(),x2.max()])
ax.scatter([y_ref[0]], [y_ref[1]], c='r', s=50, label='y_ref (KL=0)')
ax.set_title('Bregman divergence on simplex chart')
ax.legend()
fig.colorbar(im, ax=ax)
plt.show()
"""
        ),
        md("## Mirror descent on a 2D linear objective"),
        code(
            """
# linear objective c^T x on simplex
c = np.array([1.2, -0.2, 0.5])
x = np.array([1/3, 1/3, 1/3], dtype=float)
traj = [x.copy()]
eta = 0.12
for _ in range(80):
    x = x * np.exp(-eta * c)
    x = x / x.sum()
    traj.append(x.copy())
traj = np.array(traj)

fig, ax = plt.subplots(figsize=(7.6, 4.0))
ax.plot(traj[:,0], label='x1'); ax.plot(traj[:,1], label='x2'); ax.plot(traj[:,2], label='x3')
ax.set_title('Mirror descent on linear objective in simplex')
ax.legend()
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def nb_cellular() -> list[dict]:
    return [
        md("# Cellular Automata\n\nWe study elementary 1D rules with progressive visual checkpoints."),
        md("## Rule and initialization"),
        code(
            COMMON
            + """
rule = 110
bits = np.array(list(np.binary_repr(rule, width=8)), dtype=int)
n = 260
T = 180
state = np.zeros(n, dtype=int)
state[n//2] = 1
S = [state.copy()]
"""
        ),
        md("## Time stepping"),
        code(
            """
for _ in range(T):
    left = np.roll(state, 1)
    right = np.roll(state, -1)
    idx = 4*left + 2*state + right
    state = bits[7 - idx]
    S.append(state.copy())
S = np.array(S)
"""
        ),
        md("## Result visualization"),
        code(
            """
fig, ax = plt.subplots(figsize=(9, 5.3))
ax.imshow(S, cmap='binary', origin='lower', aspect='auto')
ax.set_title(f'Rule {rule}')
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def nb_chebyshev() -> list[dict]:
    return [
        md(
            r"""
# Chebyshev Nodes vs Uniform Nodes for Interpolation

Uniform interpolation can exhibit Runge oscillations for rational-like functions.
We compare interpolation of
$$
f(x)=\frac{1}{\kappa^2+x^2}
$$
using uniform nodes and Chebyshev nodes.
"""
        ),
        code(
            COMMON
            + """
import ipywidgets as widgets
kappa = 0.15
f = lambda x: 1.0 / (kappa**2 + x**2)
xg = np.linspace(-1, 1, 1000)
yg = f(xg)
"""
        ),
        md("## Chebyshev polynomial on [-1,1]"),
        code(
            """
T6 = np.cos(6*np.arccos(np.clip(xg, -1, 1)))
fig, ax = plt.subplots(figsize=(8.4, 3.6))
ax.plot(xg, T6, lw=1.8)
ax.set_title('Chebyshev polynomial T6 on [-1,1]')
plt.show()
"""
        ),
        md("## Small / medium / large interpolation sizes"),
        code(
            """
sizes = [8, 16, 32]
fig, axes = plt.subplots(1, 3, figsize=(14.5, 3.6), constrained_layout=True)
for ax, n in zip(axes, sizes):
    xu = np.linspace(-1, 1, n)
    xc = np.cos((2*np.arange(n)+1)/(2*n)*np.pi)
    pu = np.poly1d(np.polyfit(xu, f(xu), n-1))
    pc = np.poly1d(np.polyfit(xc, f(xc), n-1))
    ax.plot(xg, yg, 'k', lw=1.6, label='f')
    ax.plot(xg, pu(xg), lw=1.2, label='uniform nodes')
    ax.plot(xg, pc(xg), lw=1.2, label='chebyshev nodes')
    ax.set_title(f'n={n}')
axes[0].legend(fontsize=8)
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
        md("## Interactive slider: node count and node type"),
        code(
            """
def show(n=14, nodes='uniform'):
    x = np.linspace(-1,1,n) if nodes=='uniform' else np.cos((2*np.arange(n)+1)/(2*n)*np.pi)
    p = np.poly1d(np.polyfit(x, f(x), n-1))
    fig, ax = plt.subplots(figsize=(8.8, 3.6))
    ax.plot(xg, yg, 'k', lw=1.6, label='f')
    ax.plot(xg, p(xg), lw=1.6, label=f'{nodes} interpolation')
    ax.scatter(x, f(x), s=22, c='tab:red')
    ax.legend(); ax.set_title(f'n={n}, nodes={nodes}')
    plt.show()

widgets.interact(
    show,
    n=widgets.IntSlider(min=4, max=60, step=2, value=14),
    nodes=widgets.ToggleButtons(options=['uniform', 'chebyshev']),
);
""",
            tags=["interactive"],
        ),
    ]


def nb_cs_basis() -> list[dict]:
    return [
        md("# Basis Pursuit / LASSO Regularization Path\n\nWe track solutions as $\\lambda$ varies in $\\min_x \\frac12\\|Ax-y\\|_2^2 + \\lambda\\|x\\|_1$."),
        code(
            COMMON
            + """
m, n = 60, 120
A = rng.normal(size=(m, n)) / np.sqrt(m)
x0 = np.zeros(n)
supp = rng.choice(n, size=9, replace=False)
x0[supp] = rng.normal(size=9)
y = A @ x0 + 0.02*rng.normal(size=m)
lam_max = np.max(np.abs(A.T @ y))
"""
        ),
        code(
            """
def ista(lam, n_iter=250, step=0.9):
    x = np.zeros(n)
    L = np.linalg.norm(A, 2)**2
    tau = step / L
    for _ in range(n_iter):
        g = A.T @ (A @ x - y)
        z = x - tau * g
        x = np.sign(z) * np.maximum(np.abs(z) - lam*tau, 0)
    return x

lams = np.geomspace(lam_max, lam_max*1e-2, 24)
X = np.array([ista(lam) for lam in lams])
"""
        ),
        md("## Regularization path"),
        code(
            """
fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.3), constrained_layout=True)
for j in supp[:6]:
    axes[0].plot(lams/lam_max, X[:, j], lw=1.5)
axes[0].set_xscale('log')
axes[0].set_title('Selected coefficient paths vs lambda/lambda_max')
axes[0].set_xlabel('lambda/lambda_max')

nnz = np.sum(np.abs(X) > 1e-3, axis=1)
axes[1].plot(lams/lam_max, nnz, 'o-', lw=1.6)
axes[1].set_xscale('log')
axes[1].set_title('Sparsity level along path')
axes[1].set_xlabel('lambda/lambda_max')
fig.savefig(OUT / "snippet.png", bbox_inches="tight")
plt.show()
"""
        ),
    ]


def main() -> None:
    write("ada-boost", nb_ada_boost())
    write("admm-first-principles", nb_admm())
    write("advection", nb_advection())
    write("allen-cahn-cahn-hilliard", nb_allen_cahn_cahn_hilliard())
    write("alpha-shapes", nb_alpha_shapes())
    write("apolonian", nb_apolonian())
    write("approximation", nb_approximation())
    write("arithmetico-geometric", nb_agm())
    write("bayesian", nb_bayesian())
    write("bernouilli-tcl", nb_bernoulli_tcl())
    write("brachistochrone", nb_brachistochrone())
    write("bregman-flow", nb_bregman())
    write("cellular", nb_cellular())
    write("chebyshev-minimax", nb_chebyshev())
    write("compressed-sensing-basis-pursuit", nb_cs_basis())


if __name__ == "__main__":
    main()


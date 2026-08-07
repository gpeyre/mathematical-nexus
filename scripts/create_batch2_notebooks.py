#!/usr/bin/env python3
from __future__ import annotations

import json
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PYTHON_DIR = ROOT / "python"
RETIRED_SLUGS = {"trust-region-methods"}


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
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.x"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


TOPICS = [
    {
        "slug": "hamiltonian-symplectic",
        "title": "Hamiltonian Dynamics and Symplectic Integrators",
        "intro": r"""
# Hamiltonian Dynamics and Symplectic Integrators

For a state $(q,p)$, Hamiltonian dynamics follows
$$
\dot q = \nabla_p H(q,p),\qquad \dot p = -\nabla_q H(q,p).
$$
We illustrate this on a periodic 2D $N$-body system and compare explicit Euler against velocity-Verlet (leapfrog).
Symplectic methods preserve geometric structure and better control long-time energy drift.
""",
        "code": r"""
rng = np.random.default_rng(4)
N = 36
L = 1.0
mass = 1.0
eps = 0.012
sigma = 0.11
dt = 0.006
T = 4.8
n_steps = int(T / dt)

q0 = rng.uniform(0.0, L, size=(N, 2))
v0 = rng.normal(0.0, 1.0, size=(N, 2))
v0 -= v0.mean(axis=0, keepdims=True)
speed_scale = 0.22 / np.sqrt((v0**2).sum(axis=1).mean())
v0 *= speed_scale

def minimum_image(dq, box_size):
    return dq - box_size * np.round(dq / box_size)

def accel_and_potential(q):
    a = np.zeros_like(q)
    U = 0.0
    for i in range(N - 1):
        dq = q[i] - q[i + 1 :]
        dq = minimum_image(dq, L)
        r2 = np.sum(dq * dq, axis=1)
        w = np.exp(-0.5 * r2 / (sigma**2))
        U += np.sum(eps * w)
        f = (eps / (sigma**2)) * w[:, None] * dq
        a[i] += np.sum(f, axis=0) / mass
        a[i + 1 :] -= f / mass
    return a, U

def total_energy(q, v):
    _, U = accel_and_potential(q)
    K = 0.5 * mass * np.sum(v * v)
    return K + U

def integrate_euler(q_init, v_init):
    q = q_init.copy()
    v = v_init.copy()
    traj = np.zeros((n_steps + 1, N, 2))
    E = np.zeros(n_steps + 1)
    traj[0] = q
    E[0] = total_energy(q, v)
    for k in range(n_steps):
        a, _ = accel_and_potential(q)
        v = v + dt * a
        q = (q + dt * v) % L
        traj[k + 1] = q
        E[k + 1] = total_energy(q, v)
    return traj, E

def integrate_verlet(q_init, v_init):
    q = q_init.copy()
    v = v_init.copy()
    a, _ = accel_and_potential(q)
    traj = np.zeros((n_steps + 1, N, 2))
    E = np.zeros(n_steps + 1)
    traj[0] = q
    E[0] = total_energy(q, v)
    for k in range(n_steps):
        v_half = v + 0.5 * dt * a
        q = (q + dt * v_half) % L
        a_new, _ = accel_and_potential(q)
        v = v_half + 0.5 * dt * a_new
        a = a_new
        traj[k + 1] = q
        E[k + 1] = total_energy(q, v)
    return traj, E

traj_e, E_e = integrate_euler(q0, v0)
traj_v, E_v = integrate_verlet(q0, v0)
t = dt * np.arange(n_steps + 1)
rel_e = (E_e - E_e[0]) / (abs(E_e[0]) + 1e-12)
rel_v = (E_v - E_v[0]) / (abs(E_v[0]) + 1e-12)

fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))
for i in range(min(10, N)):
    axes[0].plot(traj_e[:, i, 0], traj_e[:, i, 1], lw=0.8, alpha=0.85)
axes[0].set_title("Explicit Euler trajectories")
axes[0].set_xlim(0, L); axes[0].set_ylim(0, L); axes[0].set_aspect("equal")
axes[0].set_xlabel("x"); axes[0].set_ylabel("y")

for i in range(min(10, N)):
    axes[1].plot(traj_v[:, i, 0], traj_v[:, i, 1], lw=0.8, alpha=0.85)
axes[1].set_title("Velocity-Verlet trajectories")
axes[1].set_xlim(0, L); axes[1].set_ylim(0, L); axes[1].set_aspect("equal")
axes[1].set_xlabel("x"); axes[1].set_ylabel("y")

plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(8.0, 4.2))
ax.plot(t, rel_e, lw=1.4, label="Euler")
ax.plot(t, rel_v, lw=1.6, label="Velocity-Verlet")
ax.set_title("Relative energy drift")
ax.set_xlabel("time")
ax.set_ylabel(r"$(H(t)-H(0))/(|H(0)|+10^{-12})$")
ax.legend()
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "fem-1d-2d",
        "title": "Finite Elements in 1D (Didactic Core)",
        "intro": r"""
# Finite Elements in 1D (Didactic Core)

We solve $-u''(x)=f(x)$ on $(0,1)$ with Dirichlet boundary conditions using piecewise-linear finite elements.
The weak form reads
$$
\int_0^1 u'(x)v'(x)\,dx = \int_0^1 f(x)v(x)\,dx \quad \forall v\in H_0^1.
$$
""",
        "code": r"""
n = 80
x = np.linspace(0, 1, n+1)
h = x[1]-x[0]

f = lambda z: np.pi**2*np.sin(np.pi*z)  # exact u=sin(pi x)
u_exact = np.sin(np.pi*x)

N = n-1  # interior dof
K = np.zeros((N, N))
b = np.zeros(N)

for e in range(n):
    xL, xR = x[e], x[e+1]
    Ke = (1/h)*np.array([[1, -1], [-1, 1]])
    # midpoint quadrature on each basis contribution
    xm = 0.5*(xL+xR)
    fe = f(xm)*h*0.5*np.array([1, 1])
    idx = [e-1, e]  # map to interior indexing
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

fig, ax = plt.subplots(figsize=(7.2, 4.4))
ax.plot(x, u_exact, lw=2, label="exact")
ax.plot(x, u, "o-", ms=3, lw=1.5, label="FEM")
ax.set_title("1D Poisson with linear finite elements")
ax.legend()
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "poisson-meshes",
        "title": "Poisson Equation on Triangulated Meshes",
        "intro": r"""
# Poisson Equation on Triangulated Meshes

On a graph/mesh discretization, a Poisson problem can be written as
$$
L u = f,
$$
with fixed boundary values. This notebook demonstrates harmonic/Poisson solves on a 2D triangulated square.
""",
        "code": r"""
import matplotlib.tri as mtri

m = 26
xx = np.linspace(0, 1, m)
yy = np.linspace(0, 1, m)
X, Y = np.meshgrid(xx, yy)
pts = np.c_[X.ravel(), Y.ravel()]
tri = mtri.Triangulation(pts[:,0], pts[:,1])
N = len(pts)

bnd = (np.isclose(pts[:,0],0) | np.isclose(pts[:,0],1) | np.isclose(pts[:,1],0) | np.isclose(pts[:,1],1))

adj = [set() for _ in range(N)]
for t in tri.triangles:
    for i in range(3):
        a=t[i]
        b=t[(i+1)%3]
        c=t[(i+2)%3]
        adj[a].add(b); adj[a].add(c)

L = np.zeros((N, N))
for i in range(N):
    if bnd[i]:
        L[i, i] = 1.0
    else:
        ng = sorted(adj[i])
        L[i, i] = len(ng)
        for j in ng:
            L[i, j] = -1.0

u_bc = np.sin(2*np.pi*pts[:,0]) * (bnd.astype(float))
f = np.zeros(N)
rhs = f.copy()
rhs[bnd] = u_bc[bnd]
u = np.linalg.solve(L, rhs)

fig, ax = plt.subplots(figsize=(6.3, 5.2))
tpc = ax.tripcolor(tri, u, shading="gouraud", cmap="coolwarm")
ax.triplot(tri, color="k", lw=0.15, alpha=0.3)
ax.set_aspect("equal"); ax.set_title("Poisson/Dirichlet solve on triangulation")
fig.colorbar(tpc, ax=ax)
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "level-set-methods",
        "title": "Level Set Advection and Reinitialization",
        "intro": r"""
# Level Set Advection and Reinitialization

A moving interface $\Gamma_t$ can be represented as $\{\phi(\cdot,t)=0\}$.
Under advection velocity $v$, the level-set PDE is
$$
\partial_t \phi + v\cdot\nabla\phi = 0.
$$
We illustrate transport of an implicit curve and periodic reinitialization to signed-distance shape.
""",
        "code": r"""
n = 170
x = np.linspace(-1, 1, n)
y = np.linspace(-1, 1, n)
X, Y = np.meshgrid(x, y)
dx = x[1]-x[0]

phi = np.sqrt((X+0.25)**2 + (Y+0.15)**2) - 0.27
vx = -Y
vy = X
dt = 0.002

def grad_central(Z):
    zx = (np.roll(Z,-1,1)-np.roll(Z,1,1))/(2*dx)
    zy = (np.roll(Z,-1,0)-np.roll(Z,1,0))/(2*dx)
    return zx, zy

snap_ids = [0, 80, 180, 320]
snaps = {}
for k in range(max(snap_ids)+1):
    if k in snap_ids:
        snaps[k] = phi.copy()
    phix, phiy = grad_central(phi)
    phi = phi - dt*(vx*phix + vy*phiy)
    if k % 30 == 0 and k > 0:
        g = np.sqrt(phix**2 + phiy**2) + 1e-12
        phi = phi / g  # light reinit heuristic

fig, axes = plt.subplots(2, 2, figsize=(8.2, 8.2))
for ax, sid in zip(axes.ravel(), snap_ids):
    cs = ax.contour(X, Y, snaps[sid], levels=[0], colors="tab:blue", linewidths=2)
    ax.set_title(f"step {sid}")
    ax.set_aspect("equal")
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "compressed-sensing-basis-pursuit",
        "title": "Compressed Sensing and Basis Pursuit",
        "intro": r"""
# Compressed Sensing and Basis Pursuit

Recover sparse $x^\star$ from underdetermined measurements $y=Ax^\star$ by solving
$$
\min_x \|x\|_1 \quad \text{s.t.}\quad Ax=y
$$
or its penalized version (LASSO):
$$
\min_x \tfrac12\|Ax-y\|_2^2+\lambda\|x\|_1.
$$
""",
        "code": r"""
rng = np.random.default_rng(0)
m, n = 90, 260
s = 14
A = rng.standard_normal((m, n))/np.sqrt(m)
x_true = np.zeros(n)
idx = rng.choice(n, size=s, replace=False)
x_true[idx] = rng.standard_normal(s)
y = A @ x_true

lam = 0.03
L = np.linalg.norm(A, 2)**2
tau = 1.0/L

def soft(z, t):
    return np.sign(z)*np.maximum(np.abs(z)-t, 0.0)

x = np.zeros(n)
errs = []
for _ in range(450):
    x = soft(x - tau*(A.T@(A@x - y)), lam*tau)
    errs.append(np.linalg.norm(x-x_true)/np.linalg.norm(x_true))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].stem(x_true, linefmt="C0-", markerfmt="C0o", basefmt="k-", label="true")
axes[0].stem(x, linefmt="C1-", markerfmt="C1x", basefmt="k-", label="recovered")
axes[0].set_title("Sparse support recovery"); axes[0].legend(fontsize=8)
axes[1].plot(errs, lw=2); axes[1].set_yscale("log")
axes[1].set_title("Relative error decay"); axes[1].set_xlabel("iteration")
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "orthogonal-matching-pursuit",
        "title": "Orthogonal Matching Pursuit",
        "intro": r"""
# Orthogonal Matching Pursuit

OMP greedily builds sparse approximations by repeatedly selecting the atom most correlated with the residual and refitting coefficients by least squares.
At step $k$:
$$
j_k=\arg\max_j |\langle a_j, r_{k-1}\rangle|,\qquad
x_{S_k}=\arg\min_z\|A_{S_k}z-y\|_2^2.
$$
""",
        "code": r"""
rng = np.random.default_rng(1)
m, n = 90, 280
s = 12
A = rng.standard_normal((m, n)); A /= np.linalg.norm(A, axis=0, keepdims=True) + 1e-12
x_true = np.zeros(n)
supp = rng.choice(n, s, replace=False)
x_true[supp] = rng.standard_normal(s)
y = A @ x_true

S = []
r = y.copy()
x = np.zeros(n)
res = []
for _ in range(35):
    j = int(np.argmax(np.abs(A.T @ r)))
    if j not in S:
        S.append(j)
    As = A[:, S]
    coef, *_ = np.linalg.lstsq(As, y, rcond=None)
    x[:] = 0
    x[np.array(S)] = coef
    r = y - A @ x
    res.append(np.linalg.norm(r))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].stem(x_true, linefmt="C0-", markerfmt="C0o", basefmt="k-", label="true")
axes[0].stem(x, linefmt="C2-", markerfmt="C2x", basefmt="k-", label="OMP")
axes[0].set_title("Recovered sparse vector"); axes[0].legend(fontsize=8)
axes[1].plot(res, "-o", lw=1.8, ms=3); axes[1].set_yscale("log")
axes[1].set_title("Residual norm decay"); axes[1].set_xlabel("iteration")
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "admm-first-principles",
        "title": "ADMM from First Principles (LASSO Example)",
        "intro": r"""
# ADMM from First Principles (LASSO Example)

For
$$
\min_x \tfrac12\|Ax-y\|_2^2 + \lambda\|x\|_1,
$$
split $x=z$ and apply ADMM updates:
$$
x^{k+1}=\arg\min_x \tfrac12\|Ax-y\|_2^2+\frac{\rho}{2}\|x-z^k+u^k\|_2^2,
$$
$$
z^{k+1}=\operatorname{soft}(x^{k+1}+u^k,\lambda/\rho),\quad
u^{k+1}=u^k+x^{k+1}-z^{k+1}.
$$
""",
        "code": r"""
rng = np.random.default_rng(2)
m, n = 85, 230
A = rng.standard_normal((m, n))/np.sqrt(m)
x_true = np.zeros(n)
supp = rng.choice(n, 13, replace=False)
x_true[supp] = rng.standard_normal(13)
y = A @ x_true + 0.01*rng.standard_normal(m)

lam = 0.06
rho = 1.0
AtA = A.T @ A
P = np.linalg.inv(AtA + rho*np.eye(n))
Aty = A.T @ y

x = np.zeros(n); z = np.zeros(n); u = np.zeros(n)
primal=[]; dual=[]; obj=[]
for _ in range(260):
    x = P @ (Aty + rho*(z-u))
    z_old = z.copy()
    z = np.sign(x+u)*np.maximum(np.abs(x+u)-lam/rho, 0)
    u = u + x - z
    primal.append(np.linalg.norm(x-z))
    dual.append(np.linalg.norm(rho*(z-z_old)))
    obj.append(0.5*np.linalg.norm(A@x-y)**2 + lam*np.linalg.norm(z,1))

fig, axes = plt.subplots(1,2, figsize=(11,4.2))
axes[0].plot(obj, lw=2); axes[0].set_title("Objective decrease")
axes[1].plot(primal, label="primal res")
axes[1].plot(dual, label="dual res")
axes[1].set_yscale("log"); axes[1].legend(fontsize=8)
axes[1].set_title("ADMM residuals")
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "pdhg-chambolle-pock",
        "title": "Primal-Dual Hybrid Gradient (Chambolle–Pock)",
        "intro": r"""
# Primal-Dual Hybrid Gradient (Chambolle–Pock)

For problems $\min_x f(Kx)+g(x)$, PDHG updates
$$
y^{k+1}=\operatorname{prox}_{\sigma f^\*}(y^k+\sigma K\bar x^k),\quad
x^{k+1}=\operatorname{prox}_{\tau g}(x^k-\tau K^\top y^{k+1}),
$$
with extrapolation $\bar x^{k+1}=x^{k+1}+\theta(x^{k+1}-x^k)$.
We demonstrate denoising with TV-like finite differences.
""",
        "code": r"""
n = 260
xgrid = np.linspace(0,1,n)
u0 = np.sin(4*np.pi*xgrid) + 0.3*np.sign(np.sin(13*np.pi*xgrid))
rng = np.random.default_rng(0)
yobs = u0 + 0.22*rng.standard_normal(n)

lam = 0.12
tau = 0.25
sigma = 0.25
theta = 1.0

def D(u):
    return np.roll(u,-1) - u
def DT(p):
    return p - np.roll(p,1)

x = yobs.copy()
xbar = x.copy()
p = np.zeros_like(x)

for _ in range(360):
    p = p + sigma*D(xbar)
    p = p / np.maximum(1.0, np.abs(p)/lam)  # prox of indicator of |p|<=lam
    x_old = x.copy()
    x = (x + tau*(DT(p) + yobs)) / (1 + tau)  # prox for 0.5||x-y||^2
    xbar = x + theta*(x - x_old)

fig, ax = plt.subplots(figsize=(8.2,4.1))
ax.plot(xgrid, yobs, alpha=0.45, label="noisy")
ax.plot(xgrid, u0, lw=2, label="ground truth")
ax.plot(xgrid, x, lw=2, label="PDHG denoised")
ax.set_title("PDHG denoising with 1D TV regularization")
ax.legend(fontsize=8)
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "bfgs-lbfgs",
        "title": "BFGS vs Gradient Descent",
        "intro": r"""
# BFGS vs Gradient Descent

BFGS builds curvature information through rank-two Hessian-inverse updates:
$$
H_{k+1}=(I-\rho s y^\top)H_k(I-\rho y s^\top)+\rho ss^\top,\quad \rho=\frac1{y^\top s}.
$$
This often accelerates convergence on ill-conditioned smooth objectives.
""",
        "code": r"""
def f(x):
    x1, x2 = x
    return 100*(x2-x1**2)**2 + (1-x1)**2
def grad(x):
    x1, x2 = x
    return np.array([-400*x1*(x2-x1**2)-2*(1-x1), 200*(x2-x1**2)])

x0 = np.array([-1.4, 1.6], dtype=float)
n_it = 120

# Gradient descent
xg = x0.copy()
traj_g=[xg.copy()]
for _ in range(n_it):
    g = grad(xg)
    alpha = 0.0018
    xg = xg - alpha*g
    traj_g.append(xg.copy())

# BFGS
xb = x0.copy()
H = np.eye(2)
traj_b=[xb.copy()]
for _ in range(n_it):
    g = grad(xb)
    p = -H @ g
    alpha = 0.004
    xn = xb + alpha*p
    s = xn - xb
    y = grad(xn) - g
    ys = y @ s
    if ys > 1e-12:
        rho = 1.0/ys
        I = np.eye(2)
        H = (I-rho*np.outer(s,y)) @ H @ (I-rho*np.outer(y,s)) + rho*np.outer(s,s)
    xb = xn
    traj_b.append(xb.copy())

traj_g = np.array(traj_g); traj_b = np.array(traj_b)

X1 = np.linspace(-2, 2, 260)
X2 = np.linspace(-1, 3, 260)
XX1, XX2 = np.meshgrid(X1, X2)
ZZ = 100*(XX2-XX1**2)**2 + (1-XX1)**2

fig, ax = plt.subplots(figsize=(6.6,5.5))
ax.contour(XX1, XX2, np.log10(ZZ+1), levels=28, cmap="gray")
ax.plot(traj_g[:,0], traj_g[:,1], "-o", ms=2, lw=1.2, label="GD")
ax.plot(traj_b[:,0], traj_b[:,1], "-o", ms=2, lw=1.2, label="BFGS")
ax.set_title("Rosenbrock minimization trajectories")
ax.legend()
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
    },
    {
        "slug": "trust-region-methods",
        "title": "Trust-Region Methods on Nonconvex Objectives",
        "intro": r"""
# Trust-Region Methods on Nonconvex Objectives

Trust-region methods solve local quadratic models
$$
\min_{\|p\|\le \Delta_k}\ m_k(p)=f(x_k)+g_k^\top p+\tfrac12 p^\top B_k p,
$$
and adapt radius $\Delta_k$ using agreement ratio between actual and predicted decrease.
""",
        "code": r"""
def f(x):
    x1, x2 = x
    return 0.5*(4*x1**2 + 0.4*x2**2) + 2*np.sin(1.7*x1)*np.cos(1.2*x2)

def grad(x):
    x1, x2 = x
    return np.array([
        4*x1 + 3.4*np.cos(1.7*x1)*np.cos(1.2*x2),
        0.4*x2 - 2.4*np.sin(1.7*x1)*np.sin(1.2*x2)
    ])

def hess_fd(x, h=1e-4):
    n = len(x)
    H = np.zeros((n,n))
    for i in range(n):
        e = np.zeros(n); e[i]=1
        H[:, i] = (grad(x + h*e) - grad(x - h*e))/(2*h)
    return H

x = np.array([1.8, -1.7], dtype=float)
Delta = 0.6
traj=[x.copy()]

for _ in range(70):
    g = grad(x)
    B = hess_fd(x)
    # unconstrained Newton-like step then clipped to ball
    try:
        p = -np.linalg.solve(B + 1e-4*np.eye(2), g)
    except np.linalg.LinAlgError:
        p = -g
    nrm = np.linalg.norm(p)
    if nrm > Delta:
        p = p * (Delta / (nrm + 1e-12))

    mk0 = f(x)
    mkp = mk0 + g@p + 0.5*p@(B@p)
    ared = f(x) - f(x+p)
    pred = mk0 - mkp
    rho = ared / (pred + 1e-12)

    if rho > 0.1:
        x = x + p
        traj.append(x.copy())
    if rho > 0.75:
        Delta = min(1.5*Delta, 1.4)
    elif rho < 0.25:
        Delta = max(0.5*Delta, 0.05)

traj = np.array(traj)
X1 = np.linspace(-3, 3, 280)
X2 = np.linspace(-3, 3, 280)
XX1, XX2 = np.meshgrid(X1, X2)
ZZ = 0.5*(4*XX1**2 + 0.4*XX2**2) + 2*np.sin(1.7*XX1)*np.cos(1.2*XX2)

fig, ax = plt.subplots(figsize=(6.6,5.6))
ax.contour(XX1, XX2, ZZ, levels=32, cmap="viridis")
ax.plot(traj[:,0], traj[:,1], "-o", ms=3, lw=1.4, color="crimson")
ax.set_title("Trust-region trajectory on nonconvex landscape")
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
        md_cell("## Environment\n\nWe load numerical tools and define a notebook-local output directory for generated figures."),
        code_cell(common_import_code(slug)),
        md_cell("## Numerical Experiment\n\nWe implement the core algorithm and generate comparative visuals to expose behavior clearly."),
        code_cell(topic["code"]),
        md_cell(
            """## Bibliographical Resources

- J. Nocedal and S. Wright, *Numerical Optimization*.
- L. N. Trefethen, *Finite Difference and Spectral Methods* (lecture notes).
- D. P. Bertsekas, *Nonlinear Programming*.
"""
        ),
    ]

    payload = notebook_payload(cells)
    nb_path.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"created {nb_path.relative_to(ROOT)}")


def main() -> None:
    for topic in TOPICS:
        if topic["slug"] in RETIRED_SLUGS:
            continue
        write_topic(topic)


if __name__ == "__main__":
    main()

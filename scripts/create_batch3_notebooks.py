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


def common_import(slug: str) -> str:
    return f"""
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.grid"] = True
plt.rcParams["font.size"] = 11

OUTPUT_DIR = Path("python/{slug}") if Path("python/{slug}").exists() else Path(".")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(0)
"""


TOPICS = [
    {
        "slug": "newton-fractals-complex",
        "title": "Newton Fractals in the Complex Plane",
        "intro": r"""
# Newton Fractals in the Complex Plane

For a polynomial $p(z)$, Newton's method iterates
$$
z_{k+1} = z_k - \frac{p(z_k)}{p'(z_k)}.
$$
Each initial point converges to a root (when it converges), and the basin partition creates a fractal boundary.
This notebook visualizes both the attraction basins and convergence speed.
""",
        "body": r"""
roots = np.array([1.0, np.exp(2j*np.pi/3), np.exp(4j*np.pi/3)])

def p(z):
    return z**3 - 1

def dp(z):
    return 3*z**2

n = 320
x = np.linspace(-1.6, 1.6, n)
y = np.linspace(-1.6, 1.6, n)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

max_iter = 35
tol = 1e-5
idx = np.zeros(Z.shape, dtype=int)
it_count = np.zeros(Z.shape, dtype=int)
W = Z.copy()

for k in range(max_iter):
    W = W - p(W) / (dp(W) + 1e-12)
    d = np.abs(W[..., None] - roots[None, None, :])
    nearest = np.argmin(d, axis=2)
    done = np.min(d, axis=2) < tol
    just_done = (it_count == 0) & done
    it_count[just_done] = k + 1
    idx = nearest

it_count[it_count == 0] = max_iter

fig, axes = plt.subplots(1, 2, figsize=(11, 4.7))
axes[0].imshow(idx, origin="lower", extent=[x.min(), x.max(), y.min(), y.max()], cmap="tab10")
axes[0].set_title("Attraction basins")
axes[0].set_xlabel("Re(z)")
axes[0].set_ylabel("Im(z)")

im = axes[1].imshow(it_count, origin="lower", extent=[x.min(), x.max(), y.min(), y.max()], cmap="magma")
axes[1].set_title("Convergence iterations")
axes[1].set_xlabel("Re(z)")
axes[1].set_ylabel("Im(z)")
fig.colorbar(im, ax=axes[1], fraction=0.046)

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- J. Hubbard, B. Hubbard, *Vector Calculus, Linear Algebra, and Differential Forms* (Newton iteration and complex dynamics notes).
- H.-O. Peitgen, P. Richter, *The Beauty of Fractals*.
""",
    },
    {
        "slug": "chebyshev-minimax",
        "title": "Chebyshev Approximation and Minimax Polynomials",
        "intro": r"""
# Chebyshev Approximation and Minimax Polynomials

Uniform approximation seeks $p_n$ minimizing
$$
\|f-p_n\|_{\infty,[-1,1]}.
$$
Chebyshev interpolation is near-minimax in many practical settings and avoids Runge oscillations.
We compare Taylor and Chebyshev polynomial approximations.
""",
        "body": r"""
def f(x):
    return np.exp(x)

n = 12
x_dense = np.linspace(-1, 1, 1000)
y_true = f(x_dense)

# Taylor around 0
coef_taylor = np.array([1 / math.factorial(k) for k in range(n + 1)])
V_t = np.vstack([x_dense**k for k in range(n + 1)])
y_taylor = coef_taylor @ V_t

# Chebyshev interpolation nodes
k = np.arange(n + 1)
x_cheb = np.cos((2*k + 1) * np.pi / (2*(n + 1)))
y_cheb = f(x_cheb)
coef_poly = np.polyfit(x_cheb, y_cheb, n)
y_cheb_interp = np.polyval(coef_poly, x_dense)

err_t = np.abs(y_true - y_taylor)
err_c = np.abs(y_true - y_cheb_interp)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
axes[0].plot(x_dense, y_true, "k", lw=2, label="exact")
axes[0].plot(x_dense, y_taylor, lw=1.6, label="Taylor")
axes[0].plot(x_dense, y_cheb_interp, lw=1.6, label="Chebyshev interp.")
axes[0].set_title("Approximants of exp(x)")
axes[0].legend()

axes[1].semilogy(x_dense, err_t + 1e-16, label="Taylor error")
axes[1].semilogy(x_dense, err_c + 1e-16, label="Chebyshev error")
axes[1].set_title("Pointwise absolute errors")
axes[1].legend()

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- L. N. Trefethen, *Approximation Theory and Approximation Practice*.
- E. W. Cheney, *Introduction to Approximation Theory*.
""",
    },
    {
        "slug": "runge-kutta-stability",
        "title": "Runge-Kutta Methods and Stability Regions",
        "intro": r"""
# Runge-Kutta Methods and Stability Regions

For the test equation $\dot y=\lambda y$, a one-step method induces
$$
y_{n+1}=R(z) y_n,\qquad z=h\lambda.
$$
Absolute stability requires $|R(z)|\leq 1$. We compare Euler, RK2, and RK4 stability regions.
""",
        "body": r"""
def R_euler(z):
    return 1 + z

def R_rk2(z):
    return 1 + z + 0.5*z**2

def R_rk4(z):
    return 1 + z + z**2/2 + z**3/6 + z**4/24

nx = 350
x = np.linspace(-4, 2, nx)
y = np.linspace(-3.5, 3.5, nx)
X, Y = np.meshgrid(x, y)
Z = X + 1j*Y

M1 = np.abs(R_euler(Z))
M2 = np.abs(R_rk2(Z))
M4 = np.abs(R_rk4(Z))

fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))
for ax, M, name in zip(axes, [M1, M2, M4], ["Euler", "RK2", "RK4"]):
    ax.contourf(X, Y, M <= 1, levels=[-0.1, 0.5, 1.1], cmap="Blues")
    ax.contour(X, Y, M, levels=[1.0], colors="k", linewidths=1.2)
    ax.axhline(0, color="gray", lw=0.7)
    ax.axvline(0, color="gray", lw=0.7)
    ax.set_title(name)
    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")
    ax.set_aspect("equal")

fig.suptitle("Absolute stability regions")
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- E. Hairer, S. P. Nørsett, G. Wanner, *Solving Ordinary Differential Equations I*.
- J. C. Butcher, *Numerical Methods for Ordinary Differential Equations*.
""",
    },
    {
        "slug": "markov-chains-mixing",
        "title": "Markov Chains and Mixing Times",
        "intro": r"""
# Markov Chains and Mixing Times

For a stochastic matrix $P$, the distribution evolves as
$$
\pi_{t+1} = \pi_t P.
$$
Mixing speed is linked to the spectral gap $1-|\lambda_2|$. We compare total variation decay from different starts.
""",
        "body": r"""
n = 25
P = np.zeros((n, n))
for i in range(n):
    P[i, i] += 0.2
    P[i, (i-1) % n] += 0.4
    P[i, (i+1) % n] += 0.4

eigvals, eigvecs = np.linalg.eig(P.T)
idx = np.argmin(np.abs(eigvals - 1))
pi = np.real(eigvecs[:, idx])
pi = np.abs(pi)
pi /= pi.sum()

starts = [0, n//3, n//2]
T = 80
tvd = []
for s in starts:
    mu = np.zeros(n); mu[s] = 1.0
    curve = []
    for _ in range(T):
        curve.append(0.5*np.sum(np.abs(mu - pi)))
        mu = mu @ P
    tvd.append(curve)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
for s, curve in zip(starts, tvd):
    axes[0].plot(curve, label=f"start={s}")
axes[0].set_title("Total variation distance to stationarity")
axes[0].set_xlabel("step")
axes[0].set_ylabel("TV distance")
axes[0].legend()

axes[1].stem(np.arange(n), pi, basefmt=" ")
axes[1].set_title("Stationary distribution")
axes[1].set_xlabel("state")
axes[1].set_ylabel(r"$\pi(i)$")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- D. A. Levin, Y. Peres, E. L. Wilmer, *Markov Chains and Mixing Times*.
- N. L. Johnson, S. Kotz, *Discrete Distributions* (foundational Markov material).
""",
    },
    {
        "slug": "hmm-forward-backward",
        "title": "Hidden Markov Models: Forward-Backward and Viterbi",
        "intro": r"""
# Hidden Markov Models: Forward-Backward and Viterbi

An HMM has latent states $x_t$ and observations $y_t$ with
$$
p(x_{1:T},y_{1:T}) = p(x_1)\prod_{t=2}^{T}p(x_t|x_{t-1})\prod_{t=1}^{T}p(y_t|x_t).
$$
We compute filtering probabilities and the most likely latent path.
""",
        "body": r"""
T = 80
A = np.array([[0.93, 0.07], [0.12, 0.88]])  # transitions
pi0 = np.array([0.5, 0.5])
means = np.array([-1.0, 1.2])
sigmas = np.array([0.45, 0.45])

states = np.zeros(T, dtype=int)
obs = np.zeros(T)
states[0] = rng.choice(2, p=pi0)
obs[0] = rng.normal(means[states[0]], sigmas[states[0]])
for t in range(1, T):
    states[t] = rng.choice(2, p=A[states[t-1]])
    obs[t] = rng.normal(means[states[t]], sigmas[states[t]])

def emis_prob(y):
    vals = []
    for k in range(2):
        v = np.exp(-0.5*((y-means[k])/sigmas[k])**2)/(np.sqrt(2*np.pi)*sigmas[k])
        vals.append(v)
    return np.array(vals)

alpha = np.zeros((T, 2))
scale = np.zeros(T)
alpha[0] = pi0 * emis_prob(obs[0])
scale[0] = alpha[0].sum(); alpha[0] /= scale[0]
for t in range(1, T):
    alpha[t] = (alpha[t-1] @ A) * emis_prob(obs[t])
    scale[t] = alpha[t].sum(); alpha[t] /= scale[t]

# Viterbi
delta = np.zeros((T, 2))
psi = np.zeros((T, 2), dtype=int)
delta[0] = np.log(pi0 + 1e-16) + np.log(emis_prob(obs[0]) + 1e-16)
for t in range(1, T):
    e = np.log(emis_prob(obs[t]) + 1e-16)
    for j in range(2):
        vals = delta[t-1] + np.log(A[:, j] + 1e-16)
        psi[t, j] = np.argmax(vals)
        delta[t, j] = vals[psi[t, j]] + e[j]

path = np.zeros(T, dtype=int)
path[-1] = np.argmax(delta[-1])
for t in range(T-2, -1, -1):
    path[t] = psi[t+1, path[t+1]]

fig, axes = plt.subplots(2, 1, figsize=(10.5, 5.7), sharex=True)
axes[0].plot(obs, lw=1.2, color="tab:blue")
axes[0].set_title("Observations")
axes[0].set_ylabel("y_t")
axes[1].plot(states, lw=2, label="true state")
axes[1].plot(path, "--", lw=1.6, label="Viterbi path")
axes[1].plot(alpha[:, 1], lw=1.2, label=r"filter prob $p(x_t=1|y_{1:t})$")
axes[1].set_ylim(-0.1, 1.2)
axes[1].set_xlabel("time")
axes[1].set_title("Latent inference")
axes[1].legend(loc="upper right")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- L. R. Rabiner, "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition", *Proc. IEEE*, 1989.
- C. M. Bishop, *Pattern Recognition and Machine Learning*.
""",
    },
    {
        "slug": "particle-filters-smc",
        "title": "Particle Filters and Sequential Monte Carlo",
        "intro": r"""
# Particle Filters and Sequential Monte Carlo

Particle filters approximate $p(x_t|y_{1:t})$ by weighted particles
$$
\sum_{i=1}^N w_t^{(i)} \delta(x_t-x_t^{(i)}).
$$
We illustrate importance weighting, effective sample size, and systematic resampling.
""",
        "body": r"""
T = 120
q = 0.06
r = 0.12

x_true = np.zeros(T)
y = np.zeros(T)
for t in range(1, T):
    x_true[t] = 0.93 * x_true[t-1] + 0.35*np.sin(0.08*t) + rng.normal(0, np.sqrt(q))
y = x_true + rng.normal(0, np.sqrt(r), size=T)

N = 220
xp = rng.normal(0, 0.6, size=N)
w = np.ones(N) / N
est = np.zeros(T)
ess = np.zeros(T)

def systematic_resample(w):
    n = len(w)
    u0 = rng.uniform(0, 1/n)
    u = u0 + np.arange(n)/n
    cdf = np.cumsum(w)
    return np.searchsorted(cdf, u)

for t in range(T):
    if t > 0:
        xp = 0.93 * xp + 0.35*np.sin(0.08*t) + rng.normal(0, np.sqrt(q), size=N)
    ll = np.exp(-0.5*((y[t]-xp)**2)/r) / np.sqrt(2*np.pi*r)
    w *= ll
    w_sum = w.sum() + 1e-16
    w /= w_sum
    est[t] = np.sum(w * xp)
    ess[t] = 1.0 / np.sum(w**2)
    if ess[t] < 0.5 * N:
        idx = systematic_resample(w)
        xp = xp[idx]
        w.fill(1.0 / N)

fig, axes = plt.subplots(2, 1, figsize=(10.5, 5.8), sharex=True)
axes[0].plot(x_true, lw=2, label="true state")
axes[0].plot(y, ".", ms=2.2, alpha=0.4, label="observations")
axes[0].plot(est, lw=1.7, label="particle estimate")
axes[0].set_title("Nonlinear state tracking")
axes[0].legend()
axes[1].plot(ess, lw=1.5)
axes[1].axhline(0.5*N, color="tab:red", ls="--", lw=1.2, label="resample threshold")
axes[1].set_title("Effective sample size")
axes[1].set_xlabel("time")
axes[1].set_ylabel("ESS")
axes[1].legend()

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- A. Doucet, N. de Freitas, N. Gordon (eds.), *Sequential Monte Carlo Methods in Practice*.
- M. S. Arulampalam et al., "A tutorial on particle filters", *IEEE TSP*, 2002.
""",
    },
    {
        "slug": "variational-inference-gmm",
        "title": "Variational Inference for Gaussian Mixtures",
        "intro": r"""
# Variational Inference for Gaussian Mixtures

Mean-field VI maximizes an ELBO
$$
\mathcal{L}(q)=\mathbb{E}_q[\log p(X,Z,\Theta)]-\mathbb{E}_q[\log q(Z,\Theta)].
$$
For didactic clarity we run soft-EM style coordinate updates and monitor the objective.
""",
        "body": r"""
n = 420
mu_true = np.array([[-1.8, -0.4], [0.2, 1.8], [2.1, -0.2]])
cov = np.array([[0.28, 0.06], [0.06, 0.24]])
X = np.vstack([rng.multivariate_normal(m, cov, size=n//3) for m in mu_true])

K = 3
N = len(X)
mu = X[rng.choice(N, size=K, replace=False)].copy()
pi = np.ones(K) / K
sigma2 = np.ones(K) * 0.45

elbo_like = []
for _ in range(45):
    # E-step responsibilities
    log_r = np.zeros((N, K))
    for k in range(K):
        d2 = np.sum((X - mu[k])**2, axis=1)
        log_r[:, k] = np.log(pi[k] + 1e-16) - 0.5*(2*np.log(2*np.pi*sigma2[k]) + d2/sigma2[k])
    log_r -= log_r.max(axis=1, keepdims=True)
    r = np.exp(log_r)
    r /= r.sum(axis=1, keepdims=True)

    Nk = r.sum(axis=0) + 1e-12
    pi = Nk / N
    mu = (r.T @ X) / Nk[:, None]
    for k in range(K):
        d2 = np.sum((X - mu[k])**2, axis=1)
        sigma2[k] = (r[:, k] @ d2) / (2*Nk[k]) + 1e-6

    ll = np.sum(np.log(np.sum(np.exp(log_r), axis=1) + 1e-16) + log_r.max(axis=1))
    ent = -np.sum(r * np.log(r + 1e-16))
    elbo_like.append(ll + ent)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].scatter(X[:, 0], X[:, 1], c=np.argmax(r, axis=1), s=8, cmap="tab10", alpha=0.8)
axes[0].scatter(mu[:, 0], mu[:, 1], c="k", s=90, marker="x", lw=2)
axes[0].set_title("Soft assignments and learned centers")
axes[0].set_xlabel("x1")
axes[0].set_ylabel("x2")

axes[1].plot(elbo_like, lw=1.8)
axes[1].set_title("ELBO surrogate across VI iterations")
axes[1].set_xlabel("iteration")
axes[1].set_ylabel("objective")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- D. M. Blei, A. Kucukelbir, J. D. McAuliffe, "Variational Inference: A Review for Statisticians", *JASA*, 2017.
- C. M. Bishop, *Pattern Recognition and Machine Learning*.
""",
    },
    {
        "slug": "gaussian-processes-2d",
        "title": "Gaussian Processes in Higher Dimension",
        "intro": r"""
# Gaussian Processes in Higher Dimension

A Gaussian process prior is
$$
f \sim \mathcal{GP}(0, k_\theta(\cdot,\cdot)).
$$
Posterior mean and variance are computed with kernel matrices. We illustrate 2D regression with uncertainty maps.
""",
        "body": r"""
def k_rbf(X1, X2, ell=0.35, sig=1.0):
    d2 = np.sum((X1[:, None, :] - X2[None, :, :])**2, axis=2)
    return sig*np.exp(-0.5*d2/(ell**2))

n_train = 80
Xtr = rng.uniform(-1, 1, size=(n_train, 2))
ftrue = lambda X: np.sin(2.2*X[:, 0]) * np.cos(1.8*X[:, 1])
ytr = ftrue(Xtr) + 0.08*rng.normal(size=n_train)

g = 55
xx = np.linspace(-1, 1, g)
yy = np.linspace(-1, 1, g)
GX, GY = np.meshgrid(xx, yy)
Xte = np.c_[GX.ravel(), GY.ravel()]

K = k_rbf(Xtr, Xtr) + 0.08**2 * np.eye(n_train)
Ks = k_rbf(Xtr, Xte)
Kss = k_rbf(Xte, Xte)
alpha = np.linalg.solve(K, ytr)
m = Ks.T @ alpha
v = np.diag(Kss - Ks.T @ np.linalg.solve(K, Ks))
v = np.maximum(v, 0)

fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6))
im0 = axes[0].imshow(m.reshape(g, g), origin="lower", extent=[-1, 1, -1, 1], cmap="viridis")
axes[0].scatter(Xtr[:, 0], Xtr[:, 1], c="w", s=8, alpha=0.7)
axes[0].set_title("Posterior mean")
fig.colorbar(im0, ax=axes[0], fraction=0.046)

im1 = axes[1].imshow(np.sqrt(v).reshape(g, g), origin="lower", extent=[-1, 1, -1, 1], cmap="magma")
axes[1].set_title("Posterior standard deviation")
fig.colorbar(im1, ax=axes[1], fraction=0.046)

for ax in axes:
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- C. E. Rasmussen, C. K. I. Williams, *Gaussian Processes for Machine Learning*.
- M. Stein, *Interpolation of Spatial Data*.
""",
    },
    {
        "slug": "normalizing-flows-2d",
        "title": "Normalizing Flows in 2D",
        "intro": r"""
# Normalizing Flows in 2D

A normalizing flow composes invertible maps
$$
z_{k+1} = T_k(z_k),\qquad
\log p_X(x)=\log p_Z(z)-\sum_k \log|\det J_{T_k}(z_k)|.
$$
We build a didactic affine-coupling flow and visualize transformed samples.
""",
        "body": r"""
N = 2200
z = rng.normal(size=(N, 2))

def coupling(x, a=0.7, b=0.4):
    y = x.copy()
    y[:, 0] = x[:, 0]
    scale = np.exp(a * np.tanh(x[:, 0]))
    shift = b * np.sin(2.0 * x[:, 0])
    y[:, 1] = scale * x[:, 1] + shift
    logdet = np.log(scale)
    return y, logdet

def rotate(x, theta=0.55):
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]])
    return x @ R.T

x1, ld1 = coupling(z, a=0.9, b=0.55)
x2 = rotate(x1, theta=0.8)
x3, ld2 = coupling(x2[:, ::-1], a=-0.7, b=0.35)
x = x3[:, ::-1]

fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.5))
axes[0].scatter(z[:, 0], z[:, 1], s=2, alpha=0.22)
axes[0].set_title("Base Gaussian samples")
axes[1].scatter(x[:, 0], x[:, 1], s=2, alpha=0.22, color="tab:orange")
axes[1].set_title("Flow-transformed samples")
for ax in axes:
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_aspect("equal")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- D. Rezende, S. Mohamed, "Variational Inference with Normalizing Flows", *ICML*, 2015.
- L. Dinh, J. Sohl-Dickstein, S. Bengio, "Density Estimation using Real NVP", *ICLR*, 2017.
""",
    },
    {
        "slug": "diffusion-models-toy",
        "title": "Diffusion Models on Toy Distributions",
        "intro": r"""
# Diffusion Models on Toy Distributions

In discrete-time diffusion,
$$
x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon,\qquad \epsilon\sim\mathcal N(0,I).
$$
We illustrate forward noising and a simple denoising proxy on a 2D ring distribution.
""",
        "body": r"""
N = 1800
theta = rng.uniform(0, 2*np.pi, size=N)
r = 1.0 + 0.08*rng.normal(size=N)
x0 = np.c_[r*np.cos(theta), r*np.sin(theta)]

T = 20
beta = np.linspace(0.001, 0.05, T)
alpha = 1 - beta
abar = np.cumprod(alpha)

def forward_sample(x, t):
    e = rng.normal(size=x.shape)
    return np.sqrt(abar[t]) * x + np.sqrt(1 - abar[t]) * e

x5 = forward_sample(x0, 5)
x19 = forward_sample(x0, 19)

# Simple denoise proxy using known x0 relation for didactic visualization.
e_hat = (x19 - np.sqrt(abar[19]) * x0) / np.sqrt(1 - abar[19] + 1e-12)
x_rec = (x19 - np.sqrt(1 - abar[19]) * e_hat) / np.sqrt(abar[19] + 1e-12)

fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.2))
axes[0].scatter(x0[:, 0], x0[:, 1], s=2, alpha=0.24)
axes[0].set_title(r"$x_0$ data")
axes[1].scatter(x5[:, 0], x5[:, 1], s=2, alpha=0.24, color="tab:green")
axes[1].set_title(r"$x_5$ (moderate noise)")
axes[2].scatter(x19[:, 0], x19[:, 1], s=2, alpha=0.24, color="tab:red")
axes[2].scatter(x_rec[:, 0], x_rec[:, 1], s=1, alpha=0.14, color="k")
axes[2].set_title(r"$x_{19}$ and denoise proxy")
for ax in axes:
    ax.set_aspect("equal")
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- J. Ho, A. Jain, P. Abbeel, "Denoising Diffusion Probabilistic Models", *NeurIPS*, 2020.
- Y. Song et al., "Score-Based Generative Modeling through SDEs", *ICLR*, 2021.
""",
    },
    {
        "slug": "tsne-umap-comparison",
        "title": "t-SNE and UMAP-Style Embedding Comparison",
        "intro": r"""
# t-SNE and UMAP-Style Embedding Comparison

Dimensionality reduction balances neighborhood preservation and global geometry.
We compare PCA, a t-SNE-like neighborhood embedding objective, and a graph-spectral embedding in a didactic pipeline.
""",
        "body": r"""
n = 400
t = rng.uniform(0, 4*np.pi, size=n)
X3 = np.c_[np.cos(t), np.sin(t), t/(2*np.pi)] + 0.08*rng.normal(size=(n, 3))

# PCA baseline
Xc = X3 - X3.mean(axis=0)
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
Xpca = Xc @ Vt[:2].T

# Graph spectral embedding (UMAP-like neighborhood graph perspective)
k = 12
d2 = np.sum((X3[:, None, :] - X3[None, :, :])**2, axis=2)
idx = np.argsort(d2, axis=1)[:, 1:k+1]
W = np.zeros((n, n))
for i in range(n):
    W[i, idx[i]] = np.exp(-d2[i, idx[i]] / 0.12)
W = np.maximum(W, W.T)
D = np.diag(W.sum(axis=1))
L = D - W
evals, evecs = np.linalg.eigh(L)
Xspec = evecs[:, 1:3]

fig = plt.figure(figsize=(13.0, 4.1))
ax1 = fig.add_subplot(1, 3, 1, projection="3d")
ax1.scatter(X3[:, 0], X3[:, 1], X3[:, 2], c=t, s=6, cmap="viridis")
ax1.set_title("3D data")
ax2 = fig.add_subplot(1, 3, 2)
ax2.scatter(Xpca[:, 0], Xpca[:, 1], c=t, s=7, cmap="viridis")
ax2.set_title("PCA")
ax3 = fig.add_subplot(1, 3, 3)
ax3.scatter(Xspec[:, 0], Xspec[:, 1], c=t, s=7, cmap="viridis")
ax3.set_title("Graph-spectral embedding")
for ax in [ax2, ax3]:
    ax.set_xlabel("dim 1")
    ax.set_ylabel("dim 2")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- L. van der Maaten, G. Hinton, "Visualizing Data using t-SNE", *JMLR*, 2008.
- L. McInnes, J. Healy, J. Melville, "UMAP: Uniform Manifold Approximation and Projection", 2018.
""",
    },
    {
        "slug": "spectral-graph-wavelets",
        "title": "Spectral Graph Wavelets",
        "intro": r"""
# Spectral Graph Wavelets

For graph Laplacian $L=U\Lambda U^\top$, spectral filtering applies
$$
g(L) = U g(\Lambda) U^\top.
$$
Wavelets localize by choosing band-pass kernels at multiple scales. We show scale effects on a ring graph signal.
""",
        "body": r"""
n = 90
W = np.zeros((n, n))
for i in range(n):
    W[i, (i-1) % n] = 1
    W[i, (i+1) % n] = 1
    W[i, (i+4) % n] = 0.35
    W[i, (i-4) % n] = 0.35
D = np.diag(W.sum(axis=1))
L = D - W
evals, U = np.linalg.eigh(L)

f = np.zeros(n)
f[8:16] = 1.0
f[52:58] = -0.9

def wavelet_filter(lam, s):
    return (s * lam) * np.exp(-s * lam)

scales = [0.5, 1.5, 3.5]
filtered = []
for s in scales:
    g = wavelet_filter(evals, s)
    fs = U @ (g * (U.T @ f))
    filtered.append(fs)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].plot(f, lw=2, color="k", label="input signal")
for fs, s in zip(filtered, scales):
    axes[0].plot(fs, lw=1.5, label=f"scale={s}")
axes[0].set_title("Graph wavelet filtered signals")
axes[0].legend()

axes[1].plot(evals, np.zeros_like(evals), "k.", alpha=0.35)
for s in scales:
    axes[1].plot(evals, wavelet_filter(evals, s), lw=1.5, label=f"scale={s}")
axes[1].set_title("Spectral kernels g_s(lambda)")
axes[1].set_xlabel("Laplacian eigenvalue")
axes[1].legend()

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- D. K. Hammond, P. Vandergheynst, R. Gribonval, "Wavelets on Graphs via Spectral Graph Theory", *Applied and Computational Harmonic Analysis*, 2011.
- F. Chung, *Spectral Graph Theory*.
""",
    },
    {
        "slug": "pagerank-random-walks",
        "title": "PageRank and Random Walks on Graphs",
        "intro": r"""
# PageRank and Random Walks on Graphs

PageRank is the stationary distribution of
$$
\pi = \alpha P^\top \pi + (1-\alpha) v,
$$
where teleportation vector $v$ guarantees ergodicity. We study ranking changes with $\alpha$.
""",
        "body": r"""
n = 14
A = np.zeros((n, n))
edges = [
    (0,1),(0,2),(1,2),(1,4),(2,3),(2,4),(3,0),(3,5),(4,5),(4,6),
    (5,6),(5,7),(6,8),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,8)
]
for i, j in edges:
    A[i, j] = 1
out = A.sum(axis=1)
P = np.zeros_like(A)
for i in range(n):
    if out[i] > 0:
        P[i] = A[i] / out[i]
    else:
        P[i] = np.ones(n) / n

v = np.ones(n) / n
alphas = [0.75, 0.85, 0.95]
ranks = []
for a in alphas:
    pi = np.ones(n) / n
    for _ in range(200):
        pi = a * (P.T @ pi) + (1-a) * v
    pi /= pi.sum()
    ranks.append(pi)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
for a, pi in zip(alphas, ranks):
    axes[0].plot(pi, marker="o", lw=1.3, label=fr"$\alpha={a}$")
axes[0].set_title("PageRank vector vs teleportation")
axes[0].set_xlabel("node")
axes[0].set_ylabel("score")
axes[0].legend()

top = np.argsort(ranks[1])[::-1][:8]
axes[1].bar(np.arange(len(top)), ranks[1][top], color="tab:orange")
axes[1].set_xticks(np.arange(len(top)))
axes[1].set_xticklabels([f"node {i}" for i in top], rotation=30)
axes[1].set_title("Top nodes for alpha=0.85")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- S. Brin, L. Page, "The Anatomy of a Large-Scale Hypertextual Web Search Engine", 1998.
- A. N. Langville, C. D. Meyer, *Google's PageRank and Beyond*.
""",
    },
    {
        "slug": "gnn-message-passing-toy",
        "title": "Graph Neural Networks: Message Passing Toy Model",
        "intro": r"""
# Graph Neural Networks: Message Passing Toy Model

A basic message passing layer reads
$$
H^{(\ell+1)} = \sigma(\tilde D^{-1/2}\tilde A\tilde D^{-1/2} H^{(\ell)} W^{(\ell)}).
$$
We run a small two-layer GCN-style propagation and inspect feature separation.
""",
        "body": r"""
n = 110
X = rng.normal(size=(n, 2))
y = ((X[:, 0] * X[:, 1]) > 0).astype(int)

# Build k-NN graph
k = 8
d2 = np.sum((X[:, None, :] - X[None, :, :])**2, axis=2)
idx = np.argsort(d2, axis=1)[:, 1:k+1]
A = np.zeros((n, n))
for i in range(n):
    A[i, idx[i]] = 1
A = np.maximum(A, A.T)
A_tilde = A + np.eye(n)
D = np.diag(np.sum(A_tilde, axis=1))
Dmh = np.diag(1.0 / np.sqrt(np.diag(D) + 1e-12))
S = Dmh @ A_tilde @ Dmh

H0 = np.c_[X, np.ones(n)]
W1 = rng.normal(scale=0.5, size=(3, 8))
W2 = rng.normal(scale=0.5, size=(8, 2))
H1 = np.tanh(S @ H0 @ W1)
H2 = S @ H1 @ W2

fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
axes[0].scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm", s=16)
axes[0].set_title("Input features and labels")
axes[1].scatter(H2[:, 0], H2[:, 1], c=y, cmap="coolwarm", s=16)
axes[1].set_title("After message passing layers")
for ax in axes:
    ax.set_xlabel("dim 1")
    ax.set_ylabel("dim 2")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- T. Kipf, M. Welling, "Semi-Supervised Classification with Graph Convolutional Networks", *ICLR*, 2017.
- M. Bronstein et al., "Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges", 2021.
""",
    },
    {
        "slug": "riemannian-optimization-stiefel",
        "title": "Riemannian Optimization on Stiefel and Grassmann",
        "intro": r"""
# Riemannian Optimization on Stiefel and Grassmann

On the Stiefel manifold $St(p,n)=\{X\in\mathbb R^{n\times p}:X^\top X=I\}$,
we optimize with tangent projection and retraction:
$$
X_{k+1} = \mathrm{qf}(X_k - \eta \,\mathrm{grad} f(X_k)).
$$
We solve a PCA-style objective under orthogonality constraints.
""",
        "body": r"""
n, p = 20, 3
M = rng.normal(size=(n, n))
C = M.T @ M

Q, _ = np.linalg.qr(rng.normal(size=(n, p)))
X = Q
eta = 0.18
vals = []

for _ in range(140):
    # maximize tr(X^T C X) => minimize -tr(...)
    G = -2 * C @ X
    sym = 0.5 * (X.T @ G + G.T @ X)
    Rgrad = G - X @ sym  # tangent projection
    Y = X - eta * Rgrad
    X, _ = np.linalg.qr(Y)  # QR retraction
    vals.append(np.trace(X.T @ C @ X))

evals = np.linalg.eigvalsh(C)[::-1]
opt = np.sum(evals[:p])

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
axes[0].plot(vals, lw=1.8, label="Riemannian ascent")
axes[0].axhline(opt, color="tab:red", ls="--", lw=1.2, label="global optimum")
axes[0].set_title("Constrained objective progression")
axes[0].set_xlabel("iteration")
axes[0].set_ylabel(r"$\mathrm{tr}(X^T C X)$")
axes[0].legend()

axes[1].imshow(X.T @ X, cmap="viridis", vmin=0, vmax=1)
axes[1].set_title(r"Orthogonality check: $X^T X$")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- P.-A. Absil, R. Mahony, R. Sepulchre, *Optimization Algorithms on Matrix Manifolds*.
- N. Boumal, *An Introduction to Optimization on Smooth Manifolds*.
""",
    },
    {
        "slug": "matrix-completion-nuclear-norm",
        "title": "Matrix Completion via Nuclear Norm",
        "intro": r"""
# Matrix Completion via Nuclear Norm

Matrix completion solves
$$
\min_X \frac12\|P_\Omega(X-M)\|_F^2 + \lambda \|X\|_*.
$$
The proximal step of $\|\cdot\|_*$ is singular-value soft-thresholding.
We recover a low-rank matrix from random missing entries.
""",
        "body": r"""
n = 52
r = 4
U = rng.normal(size=(n, r))
V = rng.normal(size=(n, r))
M = U @ V.T

mask = rng.uniform(size=(n, n)) < 0.3
Obs = np.where(mask, M, 0.0)

X = np.zeros((n, n))
lam = 0.22
tau = 1.2
errs = []

for _ in range(90):
    G = np.where(mask, X - Obs, 0.0)
    Y = X - tau * G
    Ux, s, Vx = np.linalg.svd(Y, full_matrices=False)
    s = np.maximum(s - lam * tau, 0.0)
    X = (Ux * s) @ Vx
    errs.append(np.linalg.norm(X - M, "fro") / np.linalg.norm(M, "fro"))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
axes[0].plot(errs, lw=1.8)
axes[0].set_title("Relative reconstruction error")
axes[0].set_xlabel("iteration")
axes[0].set_ylabel("rel. Frobenius error")
axes[1].imshow(np.abs(M - X), cmap="magma")
axes[1].set_title("Absolute error map")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- E. Candès, B. Recht, "Exact Matrix Completion via Convex Optimization", *Found. Comput. Math.*, 2009.
- J.-F. Cai, E. Candès, Z. Shen, "A Singular Value Thresholding Algorithm for Matrix Completion", *SIAM J. Optim.*, 2010.
""",
    },
    {
        "slug": "robust-pca-lowrank-sparse",
        "title": "Robust PCA: Low-Rank + Sparse Decomposition",
        "intro": r"""
# Robust PCA: Low-Rank + Sparse Decomposition

Principal component pursuit solves
$$
\min_{L,S}\ \|L\|_* + \lambda\|S\|_1 \quad \text{s.t.} \quad M=L+S.
$$
We use an inexact augmented Lagrangian style iteration to separate structured and sparse components.
""",
        "body": r"""
m, n = 65, 65
r = 3
L0 = rng.normal(size=(m, r)) @ rng.normal(size=(r, n))
S0 = np.zeros((m, n))
idx = rng.choice(m*n, size=int(0.08*m*n), replace=False)
S0.flat[idx] = rng.normal(0, 6.0, size=len(idx))
M = L0 + S0

L = np.zeros_like(M)
S = np.zeros_like(M)
Y = np.zeros_like(M)
mu = 1.0 / np.linalg.norm(M, 2)
lam = 1.0 / np.sqrt(max(m, n))
errs = []

for _ in range(80):
    U, s, Vt = np.linalg.svd(M - S + (1/mu)*Y, full_matrices=False)
    s_th = np.maximum(s - 1/mu, 0)
    L = (U * s_th) @ Vt
    R = M - L + (1/mu)*Y
    S = np.sign(R) * np.maximum(np.abs(R) - lam/mu, 0)
    Y = Y + mu * (M - L - S)
    errs.append(np.linalg.norm(M - L - S, "fro") / np.linalg.norm(M, "fro"))

fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.2))
axes[0].imshow(M, cmap="viridis"); axes[0].set_title("Observed matrix M")
axes[1].imshow(L, cmap="viridis"); axes[1].set_title("Low-rank part L")
axes[2].imshow(np.abs(S), cmap="magma"); axes[2].set_title("Sparse magnitude |S|")
for ax in axes:
    ax.set_xticks([]); ax.set_yticks([])

plt.figure(figsize=(5.6, 3.8))
plt.plot(errs, lw=1.8)
plt.title("Constraint residual")
plt.xlabel("iteration")
plt.ylabel(r"$\|M-L-S\|_F/\|M\|_F$")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- E. Candès, X. Li, Y. Ma, J. Wright, "Robust Principal Component Analysis?", *JACM*, 2011.
- Z. Lin, M. Chen, Y. Ma, "The Augmented Lagrange Multiplier Method for Exact Recovery of Corrupted Low-Rank Matrices", 2010.
""",
    },
    {
        "slug": "persistent-homology-topology",
        "title": "Persistent Homology and Topological Signatures",
        "intro": r"""
# Persistent Homology and Topological Signatures

Persistent homology tracks birth/death of topological features across scales.
For connected components ($H_0$), bar lengths are related to MST edge lengths.
We illustrate $H_0$ persistence on point clouds with two clusters.
""",
        "body": r"""
n1, n2 = 55, 55
X1 = 0.18*rng.normal(size=(n1, 2)) + np.array([-0.9, 0.0])
X2 = 0.18*rng.normal(size=(n2, 2)) + np.array([0.9, 0.15])
X = np.vstack([X1, X2])
N = len(X)

D = np.sqrt(np.sum((X[:, None, :] - X[None, :, :])**2, axis=2))
edges = []
for i in range(N):
    for j in range(i + 1, N):
        edges.append((D[i, j], i, j))
edges.sort()

parent = np.arange(N)
size = np.ones(N, dtype=int)

def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a

bars = []
for w, i, j in edges:
    ri, rj = find(i), find(j)
    if ri != rj:
        if size[ri] < size[rj]:
            ri, rj = rj, ri
        parent[rj] = ri
        size[ri] += size[rj]
        bars.append(w)
    if len(bars) == N - 1:
        break

bars = np.array(bars)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
axes[0].scatter(X[:, 0], X[:, 1], s=15)
axes[0].set_title("Point cloud")
axes[0].set_aspect("equal")

axes[1].plot(np.sort(bars)[::-1], lw=1.8)
axes[1].set_title("H0 persistence proxy (MST merge scales)")
axes[1].set_xlabel("merge index")
axes[1].set_ylabel("scale")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- H. Edelsbrunner, J. Harer, *Computational Topology: An Introduction*.
- R. Ghrist, "Barcodes: The persistent topology of data", *Bull. AMS*, 2008.
""",
    },
    {
        "slug": "spherical-harmonics-signals",
        "title": "Spherical Harmonics and Signals on the Sphere",
        "intro": r"""
# Spherical Harmonics and Signals on the Sphere

Spherical harmonics form an orthonormal basis on $\mathbb S^2$:
$$
f(\theta,\phi)=\sum_{\ell=0}^{\infty}\sum_{m=-\ell}^{\ell} c_{\ell m}Y_\ell^m(\theta,\phi).
$$
We use low-order real harmonics to synthesize and visualize a band-limited signal.
""",
        "body": r"""
n_theta, n_phi = 90, 170
theta = np.linspace(0, np.pi, n_theta)
phi = np.linspace(0, 2*np.pi, n_phi)
Th, Ph = np.meshgrid(theta, phi, indexing="ij")

# Real low-order harmonics (up to l=2) in closed form.
Y00 = 0.5 / np.sqrt(np.pi) * np.ones_like(Th)
Y10 = np.sqrt(3/(4*np.pi)) * np.cos(Th)
Y11c = np.sqrt(3/(4*np.pi)) * np.sin(Th) * np.cos(Ph)
Y11s = np.sqrt(3/(4*np.pi)) * np.sin(Th) * np.sin(Ph)
Y20 = np.sqrt(5/(16*np.pi)) * (3*np.cos(Th)**2 - 1)

f = 0.8*Y00 + 0.9*Y10 - 0.7*Y11c + 0.4*Y11s + 0.6*Y20

X = np.sin(Th) * np.cos(Ph)
Y = np.sin(Th) * np.sin(Ph)
Z = np.cos(Th)

fig = plt.figure(figsize=(11.5, 4.8))
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax1.plot_surface(X, Y, Z, facecolors=plt.cm.coolwarm((f - f.min())/(f.max() - f.min() + 1e-12)),
                 rstride=2, cstride=2, linewidth=0, antialiased=False, shade=False)
ax1.set_title("Signal on the sphere")
ax1.set_axis_off()

ax2 = fig.add_subplot(1, 2, 2)
im = ax2.imshow(f, origin="lower", aspect="auto", cmap="coolwarm",
                extent=[0, 2*np.pi, 0, np.pi])
ax2.set_title(r"Equirectangular view $f(\theta,\phi)$")
ax2.set_xlabel(r"$\phi$")
ax2.set_ylabel(r"$\theta$")
fig.colorbar(im, ax=ax2, fraction=0.046)

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- D. S. Slepian, "On bandwidth", *Proc. IEEE*, 1976.
- J. D. Driscoll, D. M. Healy, "Computing Fourier transforms and convolutions on the 2-sphere", *Adv. Appl. Math.*, 1994.
""",
    },
    {
        "slug": "finite-groups-fft-cyclic",
        "title": "Finite Group Representations and FFT on Cyclic Groups",
        "intro": r"""
# Finite Group Representations and FFT on Cyclic Groups

On the cyclic group $\mathbb Z_n$, irreducible characters are
$$
\chi_k(t)=e^{-2\pi i kt/n}.
$$
The DFT diagonalizes circular convolution, which is the group algebra product.
""",
        "body": r"""
n = 96
t = np.arange(n)
f = np.exp(-0.5*((t-20)/6)**2) + 0.7*np.exp(-0.5*((t-62)/9)**2)
g = np.exp(-0.5*((t-0)/5)**2)
g = np.roll(g, 8)

conv_time = np.fft.ifft(np.fft.fft(f) * np.fft.fft(g)).real

k = np.arange(n)
Chi = np.exp(-2j*np.pi*np.outer(k, t)/n) / np.sqrt(n)
F = Chi @ f

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
axes[0].plot(f, lw=1.6, label="f")
axes[0].plot(g, lw=1.6, label="g")
axes[0].plot(conv_time, lw=1.6, label="f * g (circular)")
axes[0].set_title("Signals on Z_n and convolution")
axes[0].legend()

axes[1].stem(np.arange(30), np.abs(F[:30]), basefmt=" ")
axes[1].set_title("DFT amplitudes |<chi_k, f>|")
axes[1].set_xlabel("frequency k")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "snippet.png", bbox_inches="tight")
plt.show()
""",
        "biblio": """
### References

- T. W. Körner, *Fourier Analysis*.
- P. Diaconis, *Group Representations in Probability and Statistics*.
""",
    },
]


def create_notebook(spec: dict) -> None:
    slug = spec["slug"]
    title = spec["title"]
    nb_path = PYTHON_DIR / slug / f"{slug}.ipynb"
    nb_path.parent.mkdir(parents=True, exist_ok=True)

    cells = [
        md_cell(spec["intro"]),
        md_cell(
            f"""
## Environment and Imports

We prepare numerical and visualization tools. The notebook writes a square representative image to
`python/{slug}/snippet.png` so the search homepage can display it directly.
"""
        ),
        code_cell(common_import(slug)),
        md_cell(
            rf"""
## Core Construction

We now implement the main ideas for **{title}**, with equations and plots designed to expose both the model and the numerical behavior.
"""
        ),
        code_cell(spec["body"]),
        md_cell(spec["biblio"]),
    ]

    nb = notebook_payload(cells)
    nb_path.write_text(json.dumps(nb, indent=2))
    print(f"created {nb_path.relative_to(ROOT)}")


def main() -> None:
    for spec in TOPICS:
        create_notebook(spec)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from pathlib import Path
import nbformat as nbf


def md(text: str):
    return nbf.v4.new_markdown_cell(text.strip() + "\n")


def code(text: str, tags=None):
    c = nbf.v4.new_code_cell(text.strip() + "\n")
    if tags:
        c.metadata["tags"] = tags
    return c


def rewrite_gears():
    out = Path("python/gears-non-circ/gears-non-circ.ipynb")
    nb = nbf.v4.new_notebook()
    nb.cells = [
        md(
            r"""
# Non-Circular Gears and Conjugate Pitch Curves

Non-circular gears are designed to realize a prescribed, non-constant transmission ratio.
At the pitch level, two planar curves roll without slip around fixed centers separated by distance $L$.
If the first pitch radius is $r_1(\theta)$, the second must satisfy
$$
r_2(\theta)=L-r_1(\theta), \qquad
\frac{d\phi}{d\theta}=\frac{r_1(\theta)}{L-r_1(\theta)},
$$
where $\phi(\theta)$ is the accumulated rotation of gear 2 relative to gear 1.

This notebook focuses on **geometrically correct pitch-curve meshing**:
for each contact direction $\theta$, both curves touch at one point with a common tangent and no interpenetration.
"""
        ),
        md(
            r"""
We use the closure condition
$$
\int_0^{2\pi} \frac{r_1(\theta)}{L-r_1(\theta)}\,d\theta = 2\pi
$$
to determine $L$ by bisection.
"""
        ),
        code(
            """
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider, Dropdown

plt.rcParams["figure.dpi"] = 120
"""
        ),
        code(
            """
def solve_center_distance(theta, r1):
    dtheta = theta[1] - theta[0]
    rmax = np.max(r1)
    L_lo, L_hi = rmax * 1.001, rmax * 8.0

    def F(L):
        return np.sum(r1 / (L - r1)) * dtheta - 2 * np.pi

    for _ in range(80):
        L_mid = 0.5 * (L_lo + L_hi)
        if F(L_mid) > 0:
            L_lo = L_mid
        else:
            L_hi = L_mid
    return 0.5 * (L_lo + L_hi)


def angle_map(theta, r1, L):
    dtheta = theta[1] - theta[0]
    dphi = r1 / (L - r1) * dtheta
    phi = np.concatenate([[0.0], np.cumsum(dphi)])
    return phi[:-1]  # same length as theta


def contact_pair(theta0, r1_fun, L):
    r1 = r1_fun(theta0)
    p1 = np.array([r1 * np.cos(theta0), r1 * np.sin(theta0)])
    p2 = np.array([L - (L - r1) * np.cos(theta0), -(L - r1) * np.sin(theta0)])
    pc = 0.5 * (p1 + p2)
    return p1, p2, pc
"""
        ),
        md(
            r"""
We define a few driver pitch profiles $r_1(\theta)$ and compute conjugate profiles
$r_2(\theta)=L-r_1(\theta)$.
"""
        ),
        code(
            """
n = 800
theta = np.linspace(0, 2 * np.pi, n, endpoint=False)

def r_ellipse(t): return 1.0 + 0.32 * np.cos(t)
def r_trilobe(t): return 1.0 + 0.24 * np.cos(3 * t)
def r_limacon(t): return 1.0 + 0.30 * np.cos(t) + 0.14 * np.cos(2 * t)
def r_fivelobe(t): return 1.0 + 0.12 * np.cos(5 * t)

profiles = {
    "ellipse": r_ellipse,
    "3-lobe": r_trilobe,
    "limacon": r_limacon,
    "5-lobe": r_fivelobe,
}

fig, axes = plt.subplots(2, 2, figsize=(11, 11), constrained_layout=True)
for ax, (name, rfun) in zip(axes.ravel(), profiles.items()):
    r1 = rfun(theta)
    L = solve_center_distance(theta, r1)
    r2 = L - r1

    x1, y1 = r1 * np.cos(theta), r1 * np.sin(theta)
    x2 = L - r2 * np.cos(theta)
    y2 = -r2 * np.sin(theta)

    ax.fill(x1, y1, alpha=0.25, color="royalblue")
    ax.plot(x1, y1, color="royalblue", lw=2, label="$r_1$")
    ax.fill(x2, y2, alpha=0.25, color="tomato")
    ax.plot(x2, y2, color="tomato", lw=2, label="$r_2$")
    ax.plot([0, L], [0, 0], "k--", lw=1, alpha=0.6)
    ax.plot([0, L], [0, 0], "k.", ms=7)
    ax.set_title(f"{name},  L={L:.3f}")
    ax.set_aspect("equal")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
plt.show()
"""
        ),
        md(
            r"""
The instantaneous speed ratio is
$$
\frac{\omega_2}{\omega_1}=\frac{r_1(\theta)}{L-r_1(\theta)}.
$$
"""
        ),
        code(
            """
fig, ax = plt.subplots(figsize=(9, 4.5))
for name, rfun in profiles.items():
    r1 = rfun(theta)
    L = solve_center_distance(theta, r1)
    ratio = r1 / (L - r1)
    ax.plot(np.degrees(theta), ratio, lw=2, label=name)
ax.axhline(1.0, color="k", ls="--", lw=1, alpha=0.7, label="circular ratio")
ax.set_xlabel(r"contact direction $\\theta$ (degrees)")
ax.set_ylabel(r"$\\omega_2/\\omega_1$")
ax.set_title("Non-constant transmission ratio from pitch geometry")
ax.grid(alpha=0.25)
ax.legend(fontsize=8)
plt.show()
"""
        ),
        md(
            r"""
For each angle $\theta_0$, we display the two contact points
$$
p_1(\theta_0)=r_1(\theta_0)\,e(\theta_0), \qquad
p_2(\theta_0)=\big(L,0\big)-(L-r_1(\theta_0))\,e(\theta_0),
$$
and their midpoint $p_c$ (which is the contact location in the pitch construction).
"""
        ),
        code(
            """
def show_contact(profile="ellipse", theta_deg=0):
    rfun = profiles[profile]
    r1 = rfun(theta)
    L = solve_center_distance(theta, r1)
    r2 = L - r1

    x1, y1 = r1 * np.cos(theta), r1 * np.sin(theta)
    x2 = L - r2 * np.cos(theta)
    y2 = -r2 * np.sin(theta)

    th0 = np.deg2rad(theta_deg)
    p1, p2, pc = contact_pair(th0, rfun, L)
    et = np.array([-np.sin(th0), np.cos(th0)])  # tangent direction

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.fill(x1, y1, alpha=0.22, color="royalblue")
    ax.plot(x1, y1, color="royalblue", lw=2, label="driver pitch")
    ax.fill(x2, y2, alpha=0.22, color="tomato")
    ax.plot(x2, y2, color="tomato", lw=2, label="conjugate pitch")
    ax.plot([0, L], [0, 0], "k--", lw=1, alpha=0.6)
    ax.plot([0, L], [0, 0], "k.", ms=7)

    ax.plot(p1[0], p1[1], "o", color="royalblue", ms=8)
    ax.plot(p2[0], p2[1], "o", color="tomato", ms=8)
    ax.plot(pc[0], pc[1], "ko", ms=6, label="contact")
    ax.plot([pc[0] - 0.35 * et[0], pc[0] + 0.35 * et[0]],
            [pc[1] - 0.35 * et[1], pc[1] + 0.35 * et[1]],
            color="black", lw=2, alpha=0.8, label="common tangent")

    ax.set_title(f"{profile},  contact direction = {theta_deg}°")
    ax.set_aspect("equal")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8, loc="upper right")
    plt.show()

interact(
    show_contact,
    profile=Dropdown(options=list(profiles.keys()), value="ellipse", description="profile"),
    theta_deg=IntSlider(value=0, min=0, max=359, step=2, description=r"$\\theta$"),
);
""",
            tags=["interactive"],
        ),
        md(
            r"""
## Bibliographical Resources

- F. L. Litvin and A. Fuentes, *Gear Geometry and Applied Theory*, Cambridge University Press, 2nd ed., 2004.
- M. C. Smith, “Synthesis of Noncircular Gears for Function Generation,” *Journal of Mechanical Design*, 2003.
- B. H. Tongue, *Principles of Vibration*, Oxford University Press, transmission sections with variable-ratio mechanisms.
"""
        ),
    ]
    out.write_text(nbf.writes(nb), encoding="utf-8")
    print(f"updated {out}")


def rewrite_geodesic():
    out = Path("python/geodesic-heat/geodesic-heat.ipynb")
    nb = nbf.v4.new_notebook()
    nb.cells = [
        md(
            r"""
# Geodesic Distances with a Stable Heat Method on the Torus

We compute geodesic-like distance maps on a periodic square domain $\Omega=[0,1)^2$
using the heat-method pipeline:
$$
(I - t\Delta)u=\delta_{x_0}, \qquad
X=-\frac{\nabla u}{\|\nabla u\|+\eta}, \qquad
\Delta \phi=\nabla\cdot X.
$$
The final field $\phi$ approximates the distance to the source after shifting $\min \phi=0$.
Using a spectral periodic discretization keeps the computation smooth and avoids high-frequency artifacts.
"""
        ),
        md(
            r"""
The periodic Laplacian eigenvalues are
$$
\lambda_{k,\ell}=4\pi^2\left(k^2+\ell^2\right),
$$
which makes both the heat and Poisson solves explicit in Fourier space.
"""
        ),
        code(
            """
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, IntSlider

plt.rcParams["figure.dpi"] = 120
"""
        ),
        code(
            """
def spectral_operators(n):
    x = np.arange(n) / n
    X, Y = np.meshgrid(x, x, indexing="ij")
    k = np.fft.fftfreq(n, d=1 / n)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    lam = 4 * np.pi**2 * (KX**2 + KY**2)
    return X, Y, KX, KY, lam


def solve_heat_periodic(delta, t, lam):
    u_hat = np.fft.fft2(delta) / (1.0 + t * lam)
    return np.real(np.fft.ifft2(u_hat))


def grad_periodic(u):
    ux = np.roll(u, -1, axis=0) - np.roll(u, 1, axis=0)
    uy = np.roll(u, -1, axis=1) - np.roll(u, 1, axis=1)
    return 0.5 * ux, 0.5 * uy


def div_periodic(vx, vy):
    dx = np.roll(vx, -1, axis=0) - np.roll(vx, 1, axis=0)
    dy = np.roll(vy, -1, axis=1) - np.roll(vy, 1, axis=1)
    return 0.5 * dx + 0.5 * dy


def solve_poisson_periodic(rhs, lam):
    rhs_hat = np.fft.fft2(rhs)
    phi_hat = np.zeros_like(rhs_hat)
    mask = lam > 0
    phi_hat[mask] = rhs_hat[mask] / lam[mask]
    phi = np.real(np.fft.ifft2(phi_hat))
    return phi - phi.min()


def heat_distance(n, src_i, src_j, t=2e-4):
    _, _, _, _, lam = spectral_operators(n)
    delta = np.zeros((n, n))
    delta[src_i % n, src_j % n] = 1.0
    u = solve_heat_periodic(delta, t, lam)
    ux, uy = grad_periodic(u)
    norm = np.sqrt(ux**2 + uy**2) + 1e-10
    vx, vy = -ux / norm, -uy / norm
    rhs = div_periodic(vx, vy)
    phi = solve_poisson_periodic(rhs, lam)
    return u, phi
"""
        ),
        md(
            r"""
We first compare several values of the heat time $t$.
Larger $t$ oversmooths near the source; smaller $t$ captures sharper local behavior but can become noisy if too small.
"""
        ),
        code(
            """
n = 140
src = (n // 2, n // 2)
t_vals = [8e-4, 3e-4, 1.5e-4, 7e-5]

fig, axes = plt.subplots(1, 4, figsize=(14, 3.8), constrained_layout=True)
for ax, t in zip(axes, t_vals):
    _, d = heat_distance(n, src[0], src[1], t=t)
    dn = d / (d.max() + 1e-14)
    ax.imshow(dn.T, origin="lower", cmap="magma", vmin=0, vmax=1)
    ax.contour(dn.T, levels=12, colors="white", linewidths=0.5, alpha=0.7)
    ax.plot(src[0], src[1], "c*", ms=10)
    ax.set_title(f"t = {t:.1e}")
    ax.axis("off")
plt.show()
"""
        ),
        md(
            r"""
To evaluate quality, we compare the periodic Euclidean distance
$$
d_{\mathbb{T}^2}(x,x_0)=\sqrt{\min(|\Delta x|,1-|\Delta x|)^2 + \min(|\Delta y|,1-|\Delta y|)^2}
$$
against the heat-method approximation.
"""
        ),
        code(
            """
X, Y, *_ = spectral_operators(n)
x0, y0 = src[0] / n, src[1] / n
dx = np.minimum(np.abs(X - x0), 1 - np.abs(X - x0))
dy = np.minimum(np.abs(Y - y0), 1 - np.abs(Y - y0))
d_true = np.sqrt(dx**2 + dy**2)
_, d_heat = heat_distance(n, src[0], src[1], t=2e-4)

dtn = d_true / d_true.max()
dhn = d_heat / d_heat.max()
err = np.abs(dhn - dtn)

fig, axes = plt.subplots(1, 3, figsize=(13, 4.1), constrained_layout=True)
axes[0].imshow(dtn.T, origin="lower", cmap="viridis")
axes[0].set_title("Periodic Euclidean distance"); axes[0].axis("off")
axes[1].imshow(dhn.T, origin="lower", cmap="viridis")
axes[1].set_title("Heat-method distance"); axes[1].axis("off")
im = axes[2].imshow(err.T, origin="lower", cmap="inferno")
axes[2].set_title("Absolute error"); axes[2].axis("off")
fig.colorbar(im, ax=axes[2], fraction=0.046, pad=0.04)
plt.show()
"""
        ),
        md(
            r"""
With multiple sources, we compute one distance field per source and assign each point to the closest one,
which yields a geodesic Voronoi tessellation on the periodic domain.
"""
        ),
        code(
            """
rng = np.random.default_rng(4)
srcs = rng.integers(0, n, size=(7, 2))

D_stack = []
for i, j in srcs:
    _, d = heat_distance(n, int(i), int(j), t=2e-4)
    D_stack.append(d)
D_stack = np.stack(D_stack, axis=2)
labels = np.argmin(D_stack, axis=2)
dmin = np.min(D_stack, axis=2)
dmin = dmin / (dmin.max() + 1e-14)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)
axes[0].imshow(dmin.T, origin="lower", cmap="plasma")
axes[0].contour(dmin.T, levels=12, colors="white", linewidths=0.5, alpha=0.6)
for i, j in srcs:
    axes[0].plot(i, j, "w*", ms=9)
axes[0].set_title("Distance to closest source"); axes[0].axis("off")

axes[1].imshow(labels.T, origin="lower", cmap="tab10", vmin=0, vmax=9)
for i, j in srcs:
    axes[1].plot(i, j, "w*", ms=9)
axes[1].set_title("Geodesic Voronoi partition"); axes[1].axis("off")
plt.show()
"""
        ),
        md(
            r"""
Interactive exploration of the source position and heat time.
"""
        ),
        code(
            """
def interactive_distance(src_x=70, src_y=70, t=2e-4):
    u, d = heat_distance(n, src_x, src_y, t=t)
    un = u / (u.max() + 1e-14)
    dn = d / (d.max() + 1e-14)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)
    axes[0].imshow(un.T, origin="lower", cmap="cividis")
    axes[0].plot(src_x, src_y, "r*", ms=10)
    axes[0].set_title("Heat field $u$"); axes[0].axis("off")

    axes[1].imshow(dn.T, origin="lower", cmap="magma", vmin=0, vmax=1)
    axes[1].contour(dn.T, levels=12, colors="white", linewidths=0.5, alpha=0.7)
    axes[1].plot(src_x, src_y, "c*", ms=10)
    axes[1].set_title("Distance approximation $\\phi$"); axes[1].axis("off")
    plt.show()

interact(
    interactive_distance,
    src_x=IntSlider(value=70, min=0, max=n - 1, step=2, description="src x"),
    src_y=IntSlider(value=70, min=0, max=n - 1, step=2, description="src y"),
    t=FloatSlider(value=2e-4, min=5e-5, max=9e-4, step=5e-5, readout_format=".1e", description="t"),
);
""",
            tags=["interactive"],
        ),
        md(
            r"""
## Bibliographical Resources

- K. Crane, C. Weischedel, M. Wardetzky, “Geodesics in Heat,” *ACM Transactions on Graphics*, 2013.
- G. Peyré and M. Cuturi, *Computational Optimal Transport*, Foundations and Trends in Machine Learning, 2019.
- J. A. Sethian, *Level Set Methods and Fast Marching Methods*, Cambridge University Press, 1999.
"""
        ),
    ]
    out.write_text(nbf.writes(nb), encoding="utf-8")
    print(f"updated {out}")


if __name__ == "__main__":
    rewrite_gears()
    rewrite_geodesic()

#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load_nb(rel: str):
    p = ROOT / rel
    return p, json.loads(p.read_text(encoding="utf-8"))


def save_nb(path: Path, nb):
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")


def set_source(cell, text: str):
    cell["source"] = [line + ("\n" if not line.endswith("\n") else "") for line in text.splitlines()]


def patch_hump():
    p, nb = load_nb("python/hump-algebra/hump-algebra.ipynb")

    # Title + intro cleanup
    md0 = """# Hump Algebra

## Overview

Gaussian humps $G_z(x)=e^{-\\|x-z\\|^2/(2\\sigma^2)}$ provide a flexible basis for smooth signed fields.
Finite signed sums
$$
f(x)=\\sum_i a_i G_{z_i}(x),\\qquad g(x)=\\sum_j b_j G_{w_j}(x)
$$
are stable under **sum** and **product**, so they form a practical algebraic model class.

## Product identity

For two Gaussians, the product is another Gaussian up to a scalar factor:
$$
G_{z_1}(x)G_{z_2}(x)=C(z_1,z_2)\\,\\widetilde G_{z_1,z_2}(x).
$$
This notebook focuses on that closure property and on signed-mixture interactions.

We do not develop the Fourier-side algebra here, but recall that pointwise products correspond to convolutions after Fourier transform.
"""
    set_source(nb["cells"][0], md0)

    # Section title + wording
    set_source(
        nb["cells"][5],
        """### Product of two signed mixtures

We compute $P = M_1\\cdot M_2$ for two signed mixtures and inspect how positive/negative components interact under multiplication.
""",
    )

    # Minimal code tweak: use two signed bumps in each field, not random 4-bump sets.
    c6 = "".join(nb["cells"][6]["source"])
    c6 = c6.replace("n_bumps = 4", "n_bumps = 2")
    c6 = c6.replace("signs1 = rng2.choice([-1, 1], n_bumps)", "signs1 = np.array([1, -1])")
    c6 = c6.replace("signs2 = rng2.choice([-1, 1], n_bumps)", "signs2 = np.array([1, -1])")
    c6 = c6.replace("# Theoretical midpoints\nmidpoints = [(c1 + c2) / 2 for c1 in centers1 for c2 in centers2]\n", "")
    c6 = c6.replace("for mp in midpoints:\n    axes[2].plot(mp.real, mp.imag, 'g+', ms=10, mew=2)\n", "")
    c6 = c6.replace("plt.suptitle('Gaussian Bump Algebra: Product = Midpoints', fontsize=13)", "plt.suptitle('Signed two-Gaussian mixtures and their product', fontsize=13)")
    nb["cells"][6]["source"] = c6.splitlines(keepends=True)

    # Remove "Parametric bump patterns" section and its code cell, keep notebook richer elsewhere.
    del nb["cells"][7:9]

    # Update interactive section title
    set_source(nb["cells"][7], "### Interactive: move means in two signed mixtures")

    # Bibliography update with Yves Meyer reference.
    set_source(
        nb["cells"][-1],
        """## Takeaways

- Signed Gaussian mixtures are closed under addition and produce rich smooth fields.
- Products of two signed mixtures remain structured and interpretable.
- This viewpoint is useful for kernels, approximation, and harmonic analysis.

## Bibliography

- Y. Meyer, *Wavelets and Operators*, Cambridge University Press, 1992.
- Y. Meyer, *Ondelettes et Opérateurs*, Hermann, 1990.
- S. Mallat, *A Wavelet Tour of Signal Processing*, Academic Press, 1999.
""",
    )

    save_nb(p, nb)
    print(f"patched {p}")


def patch_icp():
    p, nb = load_nb("python/icp/icp.ipynb")

    # Remove sensitivity section (markdown + code)
    del nb["cells"][9:11]

    # Update interactive markdown
    set_source(
        nb["cells"][9],
        """### Interactive: step through ICP iterations (damped display)

For readability, we display a damped transition
$$
X_{k,\\tau}=(1-\\tau)X_k+\\tau\\,T(X_k),\\qquad \\tau\\in(0,1],
$$
between current points and the rigidly updated points.
""",
    )

    # Replace interactive code with damped path display.
    code = """def show_icp_step(iteration=0, tau=0.25):
    k = min(iteration, len(history)-2)
    h = history[k]
    h_next = history[k+1]
    X_blend = (1 - tau) * h['X'] + tau * h_next['X']

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(*target.T, 'b.', ms=4, alpha=0.7, label='Target')
    axes[0].plot(*X_blend.T, 'r.', ms=4, alpha=0.8, label='Damped source')
    axes[0].set_title(f'Iteration {iteration}, tau={tau:.2f}, MSE={h[\"err\"]:.5f}')
    axes[0].set_aspect('equal'); axes[0].legend()

    errs = [hh['err'] for hh in history]
    axes[1].semilogy(errs, 'b-o', ms=4)
    axes[1].axvline(iteration, color='r', linestyle='--')
    axes[1].set_xlabel('Iteration'); axes[1].set_ylabel('MSE'); axes[1].set_title('Error curve')
    plt.tight_layout(); plt.show()

interact(show_icp_step,
         iteration=IntSlider(min=0, max=len(history)-2, step=1, value=0),
         tau=FloatSlider(min=0.05, max=1.0, step=0.05, value=0.25, description='tau'));
"""
    nb["cells"][10]["source"] = code.splitlines(keepends=True)
    nb["cells"][10].setdefault("metadata", {}).setdefault("tags", [])
    if "interactive" not in nb["cells"][10]["metadata"]["tags"]:
        nb["cells"][10]["metadata"]["tags"].append("interactive")

    save_nb(p, nb)
    print(f"patched {p}")


def patch_integral_lines():
    p, nb = load_nb("python/integral-lines/integral-lines.ipynb")

    # Enforce periodic smoothing and shorter integrations.
    c4 = "".join(nb["cells"][4]["source"])
    c4 = c4.replace("gaussian_filter(rng.standard_normal((n, n)), sigma=sigma)", "gaussian_filter(rng.standard_normal((n, n)), sigma=sigma, mode='wrap')")
    c4 = c4.replace("gaussian_filter(rng.standard_normal((n, n)), sigma=sigma)", "gaussian_filter(rng.standard_normal((n, n)), sigma=sigma, mode='wrap')", 1)
    nb["cells"][4]["source"] = c4.splitlines(keepends=True)

    c6 = "".join(nb["cells"][6]["source"])
    c6 = c6.replace("dt=0.4, n_steps=100", "dt=0.35, n_steps=45")
    c6 = c6.replace("dt=0.4, n_steps=100", "dt=0.35, n_steps=45", 1)
    nb["cells"][6]["source"] = c6.splitlines(keepends=True)

    # Replace LIC modulation by short/medium/long integration-time comparison.
    c8 = """def lic(vx, vy, n_steps=15, dt=1.0, seed=0):
    rng_l = np.random.default_rng(seed)
    noise = rng_l.uniform(0, 1, vx.shape)
    n = vx.shape[0]
    Y, X = np.mgrid[0:n, 0:n]
    pos = np.column_stack([X.ravel().astype(float), Y.ravel().astype(float)])
    accum = np.zeros(n * n)
    for sign in [1, -1]:
        p = pos.copy()
        for _ in range(n_steps):
            vel = interp_vfield(vx * sign, vy * sign, p)
            p = (p + dt * vel) % n
            accum += map_coordinates(noise, p.T, order=1, mode='wrap')
    return (accum / (2 * n_steps)).reshape(n, n)

n_lic = 100
vx_s, vy_s = make_vector_field(n_lic, sigma=12, seed=99)
lic_short = lic(vx_s, vy_s, n_steps=6, dt=0.8)
lic_med = lic(vx_s, vy_s, n_steps=12, dt=0.8)
lic_long = lic(vx_s, vy_s, n_steps=24, dt=0.8)
lic_img = lic_med

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
for ax, img, ttl in zip(axes, [lic_short, lic_med, lic_long], ['short', 'medium', 'long']):
    ax.imshow(img, cmap='gray', origin='lower')
    ax.set_title(f'LIC ({ttl} integration time)')
    ax.axis('off')
plt.tight_layout(); plt.savefig('lic.png', dpi=100, bbox_inches='tight'); plt.show()
"""
    nb["cells"][8]["source"] = c8.splitlines(keepends=True)

    # Remove unwanted reference from takeaways/biblio.
    md13 = "".join(nb["cells"][13]["source"])
    md13 = md13.replace(
        "- For accuracy beyond Euler stepping, Runge–Kutta (RK4) integration is preferred.\n",
        "- Integration horizon and boundary handling strongly affect streamline quality.\n",
    )
    md13 = md13.replace("- R. McLachlan & G. Quispel, *Geometric integrators for ODEs*, J. Phys. A 39, 2006.\n", "")
    nb["cells"][13]["source"] = md13.splitlines(keepends=True)

    save_nb(p, nb)
    print(f"patched {p}")


def patch_interior_points():
    p, nb = load_nb("python/interior-points/interior-points.ipynb")

    set_source(
        nb["cells"][0],
        """# Interior Point Method for Linear Programming

## Linear programming

A linear program minimizes $c^\\top x$ under affine inequalities
$$
A x \\le b.
$$
Interior-point methods solve a sequence of smooth barrier problems
$$
\\phi_\\mu(x)=c^\\top x-\\mu\\sum_i \\log\\bigl(b_i-a_i^\\top x\\bigr),
$$
and track the central path as $\\mu\\downarrow 0$.
""",
    )

    # Finer grid and broader mu range.
    c4 = "".join(nb["cells"][4]["source"]).replace("g = 200", "g = 260")
    nb["cells"][4]["source"] = c4.splitlines(keepends=True)

    c6 = "".join(nb["cells"][6]["source"])
    c6 = c6.replace("mu_list = np.logspace(0, -3, 30)", "mu_list = np.logspace(1, -5, 60)")
    nb["cells"][6]["source"] = c6.splitlines(keepends=True)

    # Level-set span correction.
    c10 = "".join(nb["cells"][10]["source"])
    c10 = c10.replace("mu_show = [1.0, 0.3, 0.1, 0.03, 0.01, 0.003]", "mu_show = [3.0, 1.0, 0.3, 0.1, 0.03, 0.01]")
    c10 = c10.replace("v_low = np.percentile(finite_vals, 2)", "v_low = np.percentile(finite_vals, 1)")
    c10 = c10.replace("v_high = np.percentile(finite_vals, 60)", "v_high = np.percentile(finite_vals, 95)")
    nb["cells"][10]["source"] = c10.splitlines(keepends=True)

    save_nb(p, nb)
    print(f"patched {p}")


def patch_interpol_vizu():
    p, nb = load_nb("python/interpol-vizu/interpol-vizu.ipynb")
    set_source(nb["cells"][0], "# 2D spline interpolation")
    save_nb(p, nb)
    print(f"patched {p}")


def patch_interpolation_natural():
    p, nb = load_nb("python/interpolation-natural/interpolation-natural.ipynb")

    set_source(
        nb["cells"][0],
        """# Natural Neighbor Interpolation

We interpolate scattered values on fixed landmarks.
For each evaluation point $x$, approximate natural-neighbor weights $w_i(x)$ are computed from local Voronoi occupancy,
then
$$
f(x)\\approx\\sum_i w_i(x) f(z_i),\\qquad \\sum_i w_i(x)=1,\\; w_i(x)\\ge 0.
$$
""",
    )

    c6 = "".join(nb["cells"][6]["source"])
    c6 = c6.replace("f_nn = np.zeros(g * g)", "weights = np.zeros((g * g, m))\nf_nn = np.zeros(g * g)")
    c6 = c6.replace("f_nn[p_idx] = w @ f_vals", "weights[p_idx] = w\n    f_nn[p_idx] = w @ f_vals")
    c6 += "\nweights_grid = weights.reshape(g, g, m)\n"
    nb["cells"][6]["source"] = c6.splitlines(keepends=True)

    # Insert weight-visualization markdown + code before interactive block.
    md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Visualizing selected weight functions $w_i(x)$\n",
            "\n",
            "We display a few weight maps. In each panel, all landmarks are shown and the associated landmark is highlighted.\n",
        ],
    }
    code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "sel = [0, min(2, m-1), min(5, m-1)]\n",
            "fig, axes = plt.subplots(1, len(sel), figsize=(4*len(sel), 4.2))\n",
            "if len(sel) == 1:\n",
            "    axes = [axes]\n",
            "for ax, i in zip(axes, sel):\n",
            "    Wi = weights_grid[:, :, i]\n",
            "    im = ax.contourf(Xg, Yg, Wi, levels=20, cmap='viridis')\n",
            "    ax.scatter(pts[:,0], pts[:,1], c='white', s=30, edgecolors='k')\n",
            "    ax.scatter([pts[i,0]], [pts[i,1]], c='red', s=120, edgecolors='k')\n",
            "    ax.set_title(f'$w_{{{i}}}(x)$')\n",
            "    ax.set_aspect('equal')\n",
            "    plt.colorbar(im, ax=ax, fraction=0.046)\n",
            "plt.tight_layout(); plt.show()\n",
        ],
    }
    nb["cells"].insert(9, md)
    nb["cells"].insert(10, code)

    save_nb(p, nb)
    print(f"patched {p}")


def main():
    patch_hump()
    patch_icp()
    patch_integral_lines()
    patch_interior_points()
    patch_interpol_vizu()
    patch_interpolation_natural()


if __name__ == "__main__":
    main()


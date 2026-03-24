#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load(slug: str):
    p = ROOT / "python" / slug / f"{slug}.ipynb"
    return p, json.loads(p.read_text(encoding="utf-8"))


def save(path: Path, nb):
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")


def md_text(c):
    return "".join(c.get("source", []))


def set_src(cell, text: str):
    cell["source"] = [ln + ("\n" if not ln.endswith("\n") else "") for ln in text.splitlines()]


def tag_interactive(nb):
    for i, c in enumerate(nb["cells"]):
        if c.get("cell_type") == "markdown" and "Interactive" in md_text(c):
            if i + 1 < len(nb["cells"]) and nb["cells"][i + 1].get("cell_type") == "code":
                meta = nb["cells"][i + 1].setdefault("metadata", {})
                tags = meta.setdefault("tags", [])
                if "interactive" not in tags:
                    tags.append("interactive")


def patch_ada_boost():
    p, nb = load("ada-boost")
    c12 = md_text(nb["cells"][12])
    c12 = c12.replace("for ax, Dcur, title in zip(axes, [D0, Dend], ['Initial weights', 'Final weights']):",
                      "check_idx = [0, 10, 60, len(boost['D_hist'])-1]\nfig, axes = plt.subplots(1, 4, figsize=(14, 3.8), constrained_layout=True)\nfor ax, it in zip(axes, check_idx):\n    Dcur = boost['D_hist'][it]\n    title = f'weights @ iter {it}'")
    nb["cells"][12]["source"] = c12.splitlines(keepends=True)
    c14 = md_text(nb["cells"][14])
    if "interact(" not in c14:
        c14 += """
from ipywidgets import interact, IntSlider
interact(show_round, it=IntSlider(min=1, max=len(grid_scores), step=1, value=min(120, len(grid_scores))));
"""
    nb["cells"][14]["source"] = c14.splitlines(keepends=True)
    tag_interactive(nb)
    save(p, nb)


def patch_approximation():
    p, nb = load("approximation")
    c10 = md_text(nb["cells"][10])
    if "interact(compare_budget" not in c10:
        c10 += "\nfrom ipywidgets import interact, IntSlider\ninteract(compare_budget, b=IntSlider(min=6, max=56, step=2, value=24, description='budget'));\n"
    nb["cells"][10]["source"] = c10.splitlines(keepends=True)
    tag_interactive(nb)
    save(p, nb)


def patch_apolonian():
    p, nb = load("apolonian")
    c4 = md_text(nb["cells"][4]).replace("n=280", "n=360")
    nb["cells"][4]["source"] = c4.splitlines(keepends=True)
    c12 = md_text(nb["cells"][12]).replace("n_iter=24", "n_iter=36")
    nb["cells"][12]["source"] = c12.splitlines(keepends=True)
    tag_interactive(nb)
    save(p, nb)


def patch_arithmetico_geometric():
    p, nb = load("arithmetico-geometric")
    c4 = md_text(nb["cells"][4]).replace("A0 = X\nG0 = Y", "rng = np.random.default_rng(0)\nA0 = 0.2 + 0.8*rng.random_like(X)\nG0 = 0.2 + 0.8*rng.random_like(Y)")
    nb["cells"][4]["source"] = c4.splitlines(keepends=True)
    c10 = md_text(nb["cells"][10])
    if "AG surface" not in c10:
        c10 += """

# Surface rendering of the final AGM field
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
Af, Gf = hist[-1]
AG = 0.5 * (Af + Gf)
fig = plt.figure(figsize=(6.5, 5))
ax = fig.add_subplot(111, projection='3d')
skip = 12
ax.plot_surface(X[::skip,::skip], Y[::skip,::skip], AG[::skip,::skip], cmap='viridis', linewidth=0, antialiased=True)
ax.set_title('AG surface on (x,y)')
plt.show()
"""
    nb["cells"][10]["source"] = c10.splitlines(keepends=True)
    save(p, nb)


def patch_bernouilli_tcl():
    p, nb = load("bernouilli-tcl")
    c8 = md_text(nb["cells"][8]).replace("ax.set_xlim(-2.2, 2.2)", "sigma = np.sqrt(np.sum((u**2)*x) - (np.sum(u*x))**2 + 1e-14)\n    ax.set_xlim(-3*sigma, 3*sigma)")
    if "Gaussian limit overlay" not in c8:
        c8 += """
    g = np.exp(-0.5*(u/sigma)**2) / (np.sqrt(2*np.pi)*sigma)
    g = g / np.sum(g) * np.sum(x)
    ax.plot(u, g, 'k-', lw=1.5, alpha=0.8, label='Gaussian limit overlay')
    ax.legend(fontsize=8)
"""
    if "interact(" not in c8:
        c8 += "\nfrom ipywidgets import interact, IntSlider\ninteract(show_conv, n=IntSlider(min=1, max=len(hist), value=min(20, len(hist))));\n"
    nb["cells"][8]["source"] = c8.splitlines(keepends=True)
    c10 = md_text(nb["cells"][10])
    if "small/medium/large/very large" not in c10:
        c10 += """

fig, axes = plt.subplots(1, 4, figsize=(14, 3.2), constrained_layout=True)
for ax, n_show, ttl in zip(axes, [2, 8, 24, min(len(hist), 60)], ['small','medium','large','very large']):
    uu, xx = hist[n_show-1]
    sigma = np.sqrt(np.sum((uu**2)*xx) - (np.sum(uu*xx))**2 + 1e-14)
    gg = np.exp(-0.5*(uu/sigma)**2) / (np.sqrt(2*np.pi)*sigma)
    gg = gg / np.sum(gg) * np.sum(xx)
    ax.bar(uu, xx, width=max(0.03, 1.5/np.sqrt(n_show)), alpha=0.5)
    ax.plot(uu, gg, 'r-', lw=1.7)
    ax.set_title(f'{ttl} n={n_show}')
    ax.set_xlim(-3*sigma, 3*sigma)
plt.show()
"""
    nb["cells"][10]["source"] = c10.splitlines(keepends=True)
    tag_interactive(nb)
    save(p, nb)


def patch_brachistochrone():
    p, nb = load("brachistochrone")
    c12 = md_text(nb["cells"][12])
    if "interact(show_time" not in c12:
        c12 += "\nfrom ipywidgets import interact, IntSlider\ninteract(show_time, k=IntSlider(min=0, max=q-1, step=1, value=min(35, q-1), description='particle-position'));\n"
    nb["cells"][12]["source"] = c12.splitlines(keepends=True)
    tag_interactive(nb)
    save(p, nb)


def patch_bregman_flow():
    p, nb = load("bregman-flow")
    c6 = md_text(nb["cells"][6]).replace("D = bregman_div(G1, G2, *y_ref, a)", "D = bregman_div(G1, G2, *y_ref, a)\n    D = np.maximum(D - bregman_div(y_ref[0], y_ref[1], *y_ref, a), 0.0)")
    nb["cells"][6]["source"] = c6.splitlines(keepends=True)
    c8 = md_text(nb["cells"][8])
    if "linear objective on simplex" not in c8:
        c8 += """

# Mirror descent on a linear objective over simplex (minimal add-on)
c_lin = np.array([1.1, -0.3, 0.7])
x = np.array([1/3, 1/3, 1/3], float)
eta = 0.18
traj_lin = [x.copy()]
for _ in range(80):
    x = x * np.exp(-eta * c_lin)
    x /= x.sum()
    traj_lin.append(x.copy())
traj_lin = np.array(traj_lin)
fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.plot(traj_lin[:,0], label='x1'); ax.plot(traj_lin[:,1], label='x2'); ax.plot(traj_lin[:,2], label='x3')
ax.set_title('Mirror descent on linear objective on simplex')
ax.legend(fontsize=8)
plt.show()
"""
    nb["cells"][8]["source"] = c8.splitlines(keepends=True)
    save(p, nb)


def patch_dtw():
    p, nb = load("dtw")
    # Replace Sakoe section by DP front propagation section
    set_src(nb["cells"][9], "## Front propagation of the DTW dynamic program")
    nb["cells"][10]["source"] = [
        "D_prog = np.full_like(C, np.inf)\n",
        "snap = []\n",
        "for i in range(n):\n",
        "    for j in range(n):\n",
        "        prev = [D_prog[i-1,j-1] if i>0 and j>0 else np.inf,\n",
        "                D_prog[i-1,j] if i>0 else np.inf,\n",
        "                D_prog[i,j-1] if j>0 else np.inf]\n",
        "        D_prog[i,j] = C[i,j] + (0.0 if (i==0 and j==0) else min(prev))\n",
        "    if i in [5, 15, 40, 90, 160, n-1]:\n",
        "        snap.append((i, D_prog.copy()))\n",
        "fig, axes = plt.subplots(2, 3, figsize=(12, 7), constrained_layout=True)\n",
        "for ax, (i, Di) in zip(axes.ravel(), snap):\n",
        "    M = np.where(np.isfinite(Di), Di, np.nan)\n",
        "    ax.imshow(M.T, origin='lower', aspect='auto', cmap='viridis')\n",
        "    ax.set_title(f'after row i={i}')\n",
        "    ax.axis('off')\n",
        "plt.show()\n",
    ]
    # remove custom interactive section
    del nb["cells"][11:13]
    save(p, nb)


def patch_dykstra():
    p, nb = load("dykstra")
    set_src(nb["cells"][7], "## Three initializations on convex and non-convex configurations")
    nb["cells"][8]["source"] = [
        "# Convex case: two overlapping disks\n",
        "c1 = np.array([-0.5, 0.0]); r1 = 1.2\n",
        "c2 = np.array([ 0.5, 0.0]); r2 = 1.2\n",
        "Pa = lambda x: proj_disk(x, c1, r1)\n",
        "Pb = lambda x: proj_disk(x, c2, r2)\n",
        "# Non-convex surrogate pair: line and circle boundary projection pair\n",
        "line_n = np.array([1.0, -0.35]); line_n = line_n / np.linalg.norm(line_n)\n",
        "Pline = lambda x: proj_hyperplane(x, line_n)\n",
        "Pcircle = lambda x: proj_disk(x, np.array([0.2,0.2]), 1.0)\n",
        "starts = [np.array([2.5, 1.8]), np.array([-2.2, 1.4]), np.array([1.6,-2.0])]\n",
        "fig, axes = plt.subplots(2, 3, figsize=(13, 7), constrained_layout=True)\n",
        "for j, x0 in enumerate(starts):\n",
        "    T = run_dykstra(Pa, Pb, x0, 30)\n",
        "    axes[0,j].plot(T[:6,0], T[:6,1], 'o-', lw=1.6, ms=4)\n",
        "    axes[0,j].plot(T[-1,0], T[-1,1], 'r*', ms=10)\n",
        "    axes[0,j].set_title(f'convex init {j+1}')\n",
        "    T2 = run_dykstra(Pline, Pcircle, x0, 30)\n",
        "    axes[1,j].plot(T2[:6,0], T2[:6,1], 'o-', lw=1.6, ms=4)\n",
        "    axes[1,j].plot(T2[-1,0], T2[-1,1], 'r*', ms=10)\n",
        "    axes[1,j].set_title(f'non-convex init {j+1}')\n",
        "for ax in axes.ravel():\n",
        "    ax.grid(alpha=0.3); ax.set_aspect('equal')\n",
        "plt.show()\n",
    ]
    set_src(nb["cells"][9], "## Interactive: rotating initialization, Dykstra vs POCS")
    nb["cells"][10]["source"] = [
        "def show_rot(theta_deg=0, niter=24):\n",
        "    th = np.deg2rad(theta_deg)\n",
        "    x0 = np.array([2.2*np.cos(th), 2.2*np.sin(th)])\n",
        "    P1 = lambda x: proj_disk(x, np.array([-0.5,0.0]), 1.2)\n",
        "    P2 = lambda x: proj_disk(x, np.array([0.5,0.0]), 1.2)\n",
        "    Tp = run_pocs(P1, P2, x0, niter)\n",
        "    Td = run_dykstra(P1, P2, x0, niter)\n",
        "    fig, axes = plt.subplots(1,2, figsize=(10,4.5), constrained_layout=True)\n",
        "    for ax, T, ttl in zip(axes, [Tp, Td], ['POCS', 'Dykstra']):\n",
        "        ax.plot(T[:,0], T[:,1], 'o-', ms=3, lw=1.4)\n",
        "        ax.set_title(ttl); ax.set_aspect('equal'); ax.grid(alpha=0.3)\n",
        "    plt.show()\n",
        "from ipywidgets import interact, IntSlider\n",
        "interact(show_rot, theta_deg=IntSlider(min=0,max=355,step=5,value=0), niter=IntSlider(min=4,max=50,step=2,value=24));\n",
    ]
    nb["cells"][10].setdefault("metadata", {}).setdefault("tags", [])
    if "interactive" not in nb["cells"][10]["metadata"]["tags"]:
        nb["cells"][10]["metadata"]["tags"].append("interactive")
    save(p, nb)


def patch_eikonal():
    p, nb = load("eikonal-fast-marching")
    # Add progressive full-domain front viewer + interactive.
    md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## Progressive full-domain fronts and interactive viewer\n"],
    }
    code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"tags": ["interactive"]},
        "outputs": [],
        "source": [
            "def show_front(idx=0):\n",
            "    idx = int(np.clip(idx, 0, len(marks)-1))\n",
            "    m = marks[idx]\n",
            "    fig, ax = plt.subplots(figsize=(5.5,4.6))\n",
            "    ax.imshow(snaps[m].T, origin='lower', cmap='gray_r', extent=[-1,1,-1,1], aspect='auto')\n",
            "    ax.set_title(f'front snapshot @ mark {m:,}')\n",
            "    ax.set_xticks([]); ax.set_yticks([])\n",
            "    plt.show()\n",
            "from ipywidgets import interact, IntSlider\n",
            "interact(show_front, idx=IntSlider(min=0, max=len(marks)-1, step=1, value=len(marks)-1));\n",
        ],
    }
    nb["cells"].insert(9, md)
    nb["cells"].insert(10, code)
    save(p, nb)


def patch_extreme():
    p, nb = load("extreme-values")
    # Remove sections requested
    del nb["cells"][13:15]  # interactive
    del nb["cells"][11:13]  # continuous sweep
    del nb["cells"][7:9]    # tail behavior
    # Add maxima-CLT extension
    md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## Maxima-CLT style extension across three $\\xi$ regimes\n"],
    }
    code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "rng2 = np.random.default_rng(123)\n",
            "n_block = 180\n",
            "n_blocks = 2500\n",
            "# xi<0 (bounded): Beta tail surrogate\n",
            "wb = rng2.beta(2.5, 2.0, size=(n_blocks, n_block)).max(axis=1)\n",
            "# xi=0: exponential\n",
            "gb = rng2.exponential(1.0, size=(n_blocks, n_block)).max(axis=1) - np.log(n_block)\n",
            "# xi>0: Pareto heavy tail\n",
            "pb = (rng2.pareto(2.0, size=(n_blocks, n_block)) + 1).max(axis=1) / n_block**0.5\n",
            "fig, axes = plt.subplots(1,3, figsize=(12,3.6), constrained_layout=True)\n",
            "for ax, z, ttl in zip(axes, [wb, gb, pb], ['xi<0 (bounded)', 'xi=0 (Gumbel-like)', 'xi>0 (Fréchet-like)']):\n",
            "    ax.hist(z, bins=60, density=True, alpha=0.75)\n",
            "    ax.set_title(ttl)\n",
            "    ax.grid(alpha=0.25)\n",
            "plt.show()\n",
        ],
    }
    nb["cells"].insert(11, md)
    nb["cells"].insert(12, code)
    save(p, nb)


def patch_floyd():
    p, nb = load("floyd-warshall")
    c4 = md_text(nb["cells"][4])
    if "D_snaps" not in c4:
        c4 = c4.replace("for k in range(n):", "D_snaps = []\nfor k in range(n):")
        c4 = c4.replace("        NXT[i, js] = NXT[i, k]", "        NXT[i, js] = NXT[i, k]\n    if k in [0, 2, 5, 10, n-1]:\n        D_snaps.append((k, D.copy()))")
    nb["cells"][4]["source"] = c4.splitlines(keepends=True)
    md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## Progressive filling of the Floyd–Warshall distance matrix\n"],
    }
    code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, axes = plt.subplots(1, len(D_snaps), figsize=(3.1*len(D_snaps), 3.2), constrained_layout=True)\n",
            "if len(D_snaps) == 1:\n",
            "    axes = [axes]\n",
            "for ax, (k, DD) in zip(axes, D_snaps):\n",
            "    M = np.where(np.isfinite(DD), DD, np.nan)\n",
            "    ax.imshow(M, cmap='viridis', aspect='auto')\n",
            "    ax.set_title(f'k={k}')\n",
            "    ax.axis('off')\n",
            "plt.show()\n",
        ],
    }
    nb["cells"].insert(6, md)
    nb["cells"].insert(7, code)
    save(p, nb)


def patch_fourier_cristal():
    p, nb = load("fourier-cristal")
    c10 = md_text(nb["cells"][10])
    c10 = c10.replace("radial = np.array([F.ravel()[r==ri].mean() for ri in range(r_max+1)])",
                      "radial = np.array([F.ravel()[r==ri].mean() for ri in range(r_max+1)])\nradial[0] = radial[1]  # avoid DC spike dominating the profile")
    nb["cells"][10]["source"] = c10.splitlines(keepends=True)
    save(p, nb)


def patch_graph_laplacian():
    p, nb = load("graph-laplacian")
    set_src(
        nb["cells"][0],
        """# Graph Laplacian and Spectral Graph Theory

Graph Laplacians are a core bridge between geometry, probability, and learning:
they encode smoothness on graphs, define graph Fourier modes, and appear as precision operators in Gaussian Markov models.
This notebook explores these roles from one computational pipeline.
""",
    )
    save(p, nb)


def patch_hermite():
    p, nb = load("hermite-function")
    m0 = md_text(nb["cells"][0])
    if "localization in space and frequency" not in m0.lower():
        m0 += "\n## Why this matters\nHermite functions provide sharp localization in space and frequency and serve as canonical bases for uncertainty-principle examples.\n"
    nb["cells"][0]["source"] = m0.splitlines(keepends=True)
    c4 = md_text(nb["cells"][4]).replace("np.trapezoid", "np.trapezoid")
    nb["cells"][4]["source"] = c4.splitlines(keepends=True)
    save(p, nb)


def patch_grad_desc_mirror():
    p, nb = load("grad-desc-mirror")
    c5 = md_text(nb["cells"][5])
    c5 = c5.replace("f = lambda x: (x[0]-0.15)**2 + (x[1]-0.8)**2 + 0.35*(x[2]-0.05)**2",
                    "f = lambda x: 1.2*x[0] - 0.4*x[1] + 0.8*x[2]")
    c5 += "\n# objective-gap diagnostics\nfstar = min(1.2, -0.4, 0.8)\ngap = np.maximum(np.array(f_hist) - fstar, 1e-14)\n"
    nb["cells"][5]["source"] = c5.splitlines(keepends=True)
    save(p, nb)


def patch_grad_desc_momentum():
    p, nb = load("grad-desc-momentum")
    c3 = md_text(nb["cells"][3]).replace("tau = 0.16", "tau = 0.06")
    nb["cells"][3]["source"] = c3.splitlines(keepends=True)
    save(p, nb)


def patch_gradflow_metric():
    p, nb = load("gradflow-metric")
    set_src(nb["cells"][0], "# Gradient Flows with Different Metrics\n\nWe compare implicit proximal steps with metric term $\\|x-x_k\\|_p^2$ for several $p$.")
    c3 = md_text(nb["cells"][3])
    if "argmin" not in c3:
        c3 += "\n# implicit-prox interpretation: x_{k+1}=argmin ||x-x_k||_p^2 + tau||x-y||_2^2\n"
    nb["cells"][3]["source"] = c3.splitlines(keepends=True)
    save(p, nb)


def patch_haar():
    p, nb = load("haar-walsh")
    c7 = md_text(nb["cells"][7]).replace("+ 0.12 * rng.standard_normal(n)", "")
    nb["cells"][7]["source"] = c7.splitlines(keepends=True)
    save(p, nb)


def patch_heat_vs_tv():
    p, nb = load("heat-vs-tv")
    c3 = md_text(nb["cells"][3]).replace("for i, col in zip([0, 20, 60, 120], colors):",
                                         "for i, col in zip([120, 60, 20, 0], colors):")
    c3 = c3.replace("alpha=0.85", "alpha=0.55")
    nb["cells"][3]["source"] = c3.splitlines(keepends=True)
    c5 = md_text(nb["cells"][5]).replace("n = 220", "n = 280").replace("for it in [0, 20, 60, 120, 200]:", "for it in [0, 30, 90, 180, 280]:")
    nb["cells"][5]["source"] = c5.splitlines(keepends=True)
    save(p, nb)


def mark_all_interactive_tags():
    slugs = [
        "ada-boost","advection","alpha-shapes","apolonian","approximation","arithmetico-geometric","bayesian",
        "bernouilli-tcl","brachistochrone","bregman-flow","cellular","diffusion-models-toy","dtw","dykstra",
        "eikonal-fast-marching","extreme-values","farthest-point","flocking","floyd-warshall","fluids",
        "fourier-cristal","grad-desc-mirror","grad-desc-momentum","gradflow-metric","graph-laplacian",
        "haar-walsh","heat-vs-tv","hermite-function"
    ]
    for s in slugs:
        p, nb = load(s)
        tag_interactive(nb)
        save(p, nb)


def main():
    patch_ada_boost()
    patch_apolonian()
    patch_approximation()
    patch_arithmetico_geometric()
    patch_bernouilli_tcl()
    patch_brachistochrone()
    patch_bregman_flow()
    patch_dtw()
    patch_dykstra()
    patch_eikonal()
    patch_extreme()
    patch_floyd()
    patch_fourier_cristal()
    patch_graph_laplacian()
    patch_hermite()
    patch_grad_desc_mirror()
    patch_grad_desc_momentum()
    patch_gradflow_metric()
    patch_haar()
    patch_heat_vs_tv()
    mark_all_interactive_tags()
    print("minimal todo wave2 patches applied")


if __name__ == "__main__":
    main()


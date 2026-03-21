#!/usr/bin/env python3
"""Generate a simple packed-disks graph logo for Mathematical Nexus."""

from __future__ import annotations

from pathlib import Path

from matplotlib.collections import LineCollection
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / "logo.png"

    rng = np.random.default_rng(12)

    fig, ax = plt.subplots(figsize=(8, 8), dpi=320, facecolor="white")
    ax.set_facecolor("white")
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")

    # Poisson-like packing by rejection sampling with variable radii.
    pts = []
    rad = []
    attempts = 0
    target = 48
    while len(pts) < target and attempts < 160000:
        attempts += 1
        rr = float(rng.uniform(0.05, 0.13))
        x = float(rng.uniform(-0.88, 0.88))
        y = float(rng.uniform(-0.88, 0.88))
        if x * x + y * y > (0.92 - rr) ** 2:
            continue
        ok = True
        for (px, py), pr in zip(pts, rad):
            if (x - px) ** 2 + (y - py) ** 2 < (rr + pr + 0.003) ** 2:
                ok = False
                break
        if ok:
            pts.append((x, y))
            rad.append(rr)

    pts = np.array(pts, dtype=float)
    rad = np.array(rad, dtype=float)

    # Build edges between touching / near-touching circles.
    segs = []
    widths = []
    cols = []
    n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(pts[i] - pts[j])
            t = rad[i] + rad[j]
            if d <= t + 0.075:
                segs.append([pts[i], pts[j]])
                closeness = max(0.0, 1.0 - (d - t + 0.075) / 0.075)
                widths.append(1.2 + 3.8 * closeness)
                cols.append(plt.cm.viridis((rad[i] + rad[j] - rad.min() * 2) / (2 * (rad.max() - rad.min()) + 1e-9)))

    lc = LineCollection(segs, colors=cols, linewidths=widths, alpha=0.62, zorder=1, capstyle="round")
    ax.add_collection(lc)

    # Draw circles with colorful fills and crisp white halo.
    order = np.argsort(rad)
    for k in order:
        x, y = pts[k]
        r = rad[k]
        c = plt.cm.turbo((r - rad.min()) / (rad.max() - rad.min() + 1e-9))
        ax.add_patch(Circle((x, y), r * 1.02, facecolor="white", edgecolor="none", alpha=0.95, zorder=2))
        ax.add_patch(Circle((x, y), r, facecolor=c, edgecolor=(0.2, 0.2, 0.2, 0.35), linewidth=0.8, alpha=0.95, zorder=3))

    # Soft boundary ring for cohesion.
    boundary = Circle((0, 0), 0.95, facecolor="none", edgecolor=(0.1, 0.1, 0.1, 0.12), linewidth=2.0, zorder=0)
    ax.add_patch(boundary)

    fig.savefig(out_path, dpi=320, bbox_inches="tight", pad_inches=0.0, facecolor="white")
    plt.close(fig)
    print(out_path)


if __name__ == "__main__":
    main()

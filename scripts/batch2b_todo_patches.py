#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load(slug: str):
    p = ROOT / "python" / slug / f"{slug}.ipynb"
    return p, json.loads(p.read_text())


def save(path: Path, nb: dict):
    path.write_text(json.dumps(nb, indent=2), encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")


def patch_fourier_cristal():
    p, nb = load("fourier-cristal")
    for c in nb["cells"]:
        if c.get("cell_type") != "code":
            continue
        src = "".join(c.get("source", []))
        if "radial" in src.lower() and "profile" in src.lower():
            src = src.replace("r = np.arange(len(radial_profile))", "r = np.arange(len(radial_profile))\nradial_profile[0] = np.nan  # remove central Dirac for readability")
            c["source"] = [ln + "\n" for ln in src.split("\n") if ln != ""]
    save(p, nb)


def patch_fourier_curves():
    p, nb = load("fourier-curves")
    out = []
    skip_next_code = False
    for c in nb["cells"]:
        if c.get("cell_type") == "markdown":
            txt = "".join(c.get("source", [])).lower()
            if "power spectrum of curves" in txt:
                skip_next_code = True
                continue
        if skip_next_code and c.get("cell_type") == "code":
            skip_next_code = False
            continue
        out.append(c)
    nb["cells"] = out
    save(p, nb)


def patch_fourier_matrix():
    p, nb = load("fourier-matrix")
    out = []
    skip_next_code = False
    for c in nb["cells"]:
        if c.get("cell_type") == "markdown":
            txt = "".join(c.get("source", [])).lower()
            if "computational complexity" in txt and "dft" in txt and "fft" in txt:
                skip_next_code = True
                continue
        if skip_next_code and c.get("cell_type") == "code":
            skip_next_code = False
            continue
        out.append(c)
    nb["cells"] = out
    save(p, nb)


def patch_fourier_signal():
    p, nb = load("fourier-signal")
    cat_path = "matlab/fourier-curves/cat.png"
    replaced = False
    for c in nb["cells"]:
        if c.get("cell_type") != "code":
            continue
        src = "".join(c.get("source", []))
        if "2D image Fourier approximation" in src or "imshow" in src and "fft2" in src:
            src = src.replace("from matplotlib.cbook import get_sample_data\nimport matplotlib.image as mpimg\n", "import matplotlib.image as mpimg\n")
            src = src.replace('img = mpimg.imread(get_sample_data("grace_hopper.jpg"))', f'img = mpimg.imread("{cat_path}")')
            src = src.replace("img = img[..., :3]", "img = img[..., :3] if img.ndim==3 else np.stack([img,img,img],axis=2)")
            replaced = True
            c["source"] = [ln + "\n" for ln in src.split("\n") if ln != ""]
    if not replaced:
        # append a dedicated 2D-cat section if not found
        nb["cells"].extend(
            [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## 2D image Fourier approximation on a natural cat image\n",
                        "\n",
                        "We use a natural cat image from the repository and keep the strongest Fourier coefficients.\n",
                    ],
                    "id": "catimgsec1",
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "execution_count": None,
                    "outputs": [],
                    "id": "catimgsec2",
                    "source": [
                        "import matplotlib.image as mpimg\n",
                        "img = mpimg.imread('matlab/fourier-curves/cat.png')\n",
                        "img = img[..., :3] if img.ndim==3 else np.stack([img,img,img],axis=2)\n",
                        "gray = img.mean(axis=2)\n",
                        "F = np.fft.fft2(gray)\n",
                        "M = np.abs(F)\n",
                        "k = int(0.06 * gray.size)\n",
                        "thr = np.partition(M.ravel(), -k)[-k]\n",
                        "Fr = F * (M >= thr)\n",
                        "rec = np.real(np.fft.ifft2(Fr))\n",
                        "fig, axes = plt.subplots(1,2, figsize=(9.5,4.0), constrained_layout=True)\n",
                        "axes[0].imshow(gray, cmap='gray'); axes[0].set_title('Cat image'); axes[0].axis('off')\n",
                        "axes[1].imshow(rec, cmap='gray'); axes[1].set_title('Fourier sparse approximation'); axes[1].axis('off')\n",
                        "fig.savefig(OUT / 'snippet.png', bbox_inches='tight')\n",
                        "plt.show()\n",
                    ],
                },
            ]
        )
    save(p, nb)


def patch_foveation():
    p, nb = load("foveation")
    cat_path = "matlab/fourier-curves/cat.png"
    for c in nb["cells"]:
        if c.get("cell_type") != "code":
            continue
        src = "".join(c.get("source", []))
        if "img =" in src and "grace_hopper" in src:
            src = src.replace('img = mpimg.imread(get_sample_data("grace_hopper.jpg")).astype(float)', f'img = mpimg.imread("{cat_path}").astype(float)')
            src = src.replace("img = img[120:620, 100:800, :3]", "img = img[..., :3] if img.ndim==3 else np.stack([img,img,img], axis=2)")
            src += "\n# resize to 256x256 by simple index sampling\nh0,w0,_ = img.shape\nii = np.linspace(0, h0-1, 256).astype(int)\njj = np.linspace(0, w0-1, 256).astype(int)\nimg = img[np.ix_(ii, jj)]\n"
            c["source"] = [ln + "\n" for ln in src.split("\n") if ln != ""]
    save(p, nb)


def patch_gaussian_prod_convol():
    p, nb = load("gaussian-prod-convol")
    for c in nb["cells"]:
        if c.get("cell_type") != "markdown":
            continue
        txt = "".join(c.get("source", [])).lower()
        if "bibliographical resources" in txt or "references" in txt:
            c["source"] = [
                "## Bibliographical Resources\n",
                "\n",
                "- Y. Meyer, *Wavelets and Operators*, Cambridge University Press, 1992 (Gaussian hump algebra perspective and functional-analytic context).\n",
                "- Y. Meyer, *Oscillating Patterns in Image Processing and Nonlinear Evolution Equations*, AMS, 2001.\n",
                "- C. E. Rasmussen, C. K. I. Williams, *Gaussian Processes for Machine Learning*, MIT Press, 2006 (Gaussian product/convolution identities in kernel modeling).\n",
            ]
    save(p, nb)


def main():
    patch_fourier_cristal()
    patch_fourier_curves()
    patch_fourier_matrix()
    patch_fourier_signal()
    patch_foveation()
    patch_gaussian_prod_convol()


if __name__ == "__main__":
    main()


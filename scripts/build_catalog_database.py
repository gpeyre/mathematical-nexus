#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
PYTHON_DIR = ROOT / "python"
VIGNETTES_DIR = ROOT / "vignettes"
README = ROOT / "README.md"
MYDATA = VIGNETTES_DIR / "mydata.js"

DB_XLSX = ROOT / "database.xlsx"
DB_JSON = ROOT / "database.json"
DB_JS = ROOT / "database.js"


@dataclass
class Row:
    title: str
    content: str
    filename: str
    type: str


def clean_text(s: str) -> str:
    s = re.sub(r"`([^`]*)`", r"\1", s)
    # Preserve URLs when markdown links are present: [label](url) -> "label url"
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 \2", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    # Remove only heavy markdown markers, keep URL-critical characters like "_" and "#"
    s = re.sub(r"[*>$]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def polish_description(text: str) -> str:
    """Light editorial polish while staying semantically close to source text."""
    s = clean_text(text)

    def _polish_chunk(chunk: str) -> str:
        c = chunk
        # Gentle style cleanup
        c = re.sub(r"oldies but goldies\s*:", "Classic reference:", c, flags=re.I)
        c = re.sub(r"\baka\b", "also known as", c, flags=re.I)

        # Frequent typo / naming fixes found in source collection
        replacements = {
            "dikstra": "Dijkstra",
            "vornoi": "Voronoi",
            "krigging": "kriging",
            "subdivision shemes": "subdivision schemes",
            "dicrepancies": "discrepancies",
            "varyin": "varying",
        }
        for bad, good in replacements.items():
            c = re.sub(re.escape(bad), good, c, flags=re.I)

        # Normalize spacing around punctuation (text chunks only, no URLs)
        c = re.sub(r"\s+([,;:.!?])", r"\1", c)
        c = re.sub(r"([,;!?])([^\s])", r"\1 \2", c)
        c = re.sub(r"\s+", " ", c).strip()
        return c

    url_re = re.compile(r"https?://\S+")
    out_parts: List[str] = []
    last = 0
    for m in url_re.finditer(s):
        left = s[last : m.start()]
        if left:
            out_parts.append(_polish_chunk(left))
        out_parts.append(m.group(0))  # keep URLs untouched
        last = m.end()
    tail = s[last:]
    if tail:
        out_parts.append(_polish_chunk(tail))

    s2 = " ".join(p for p in out_parts if p).strip()
    s2 = re.sub(r"\s+", " ", s2).strip()

    # Capitalize first letter when possible
    if s2 and s2[0].isalpha():
        s2 = s2[0].upper() + s2[1:]

    # Ensure terminal punctuation for readability (unless ending with URL)
    if s2 and not re.search(r"(https?://\S+)$", s2) and s2[-1] not in ".!?":
        s2 += "."

    return s2


def title_from_path(path: str) -> str:
    stem = Path(path).stem
    return clean_text(stem.replace("-", " ").replace("_", " ").title())


def parse_readme_notebook_blurbs() -> Dict[str, Row]:
    text = README.read_text(encoding="utf-8")
    rows: Dict[str, Row] = {}
    pattern = re.compile(
        r"\|\s+\*\*(?P<title>.*?)\*\*<br>(?P<desc>.*?)\s+\|\s+.*?\((?P<nb>python/[^)]+\.ipynb)\)\s+\|"
    )
    for m in pattern.finditer(text):
        nb = m.group("nb").strip()
        rows[nb] = Row(
            title=clean_text(m.group("title").strip()),
            content=polish_description(m.group("desc").strip()),
            filename=nb,
            type="notebook",
        )
    return rows


def parse_notebook_fallback(nb_path: Path) -> Row:
    rel = nb_path.relative_to(ROOT).as_posix()
    try:
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
    except Exception:
        return Row(title=title_from_path(rel), content="", filename=rel, type="notebook")

    title = ""
    content = ""
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        src = "".join(cell.get("source", []))
        if not title:
            m = re.search(r"^\s*#\s+(.+)$", src, flags=re.M)
            if m:
                title = clean_text(m.group(1))
        if not content:
            chunks = [c.strip() for c in src.split("\n\n") if c.strip()]
            for chunk in chunks:
                if chunk.lstrip().startswith("#"):
                    continue
                content = clean_text(chunk)
                break
        if title and content:
            break

    if not title:
        title = title_from_path(rel)
    if not content:
        content = "Standalone educational notebook with mathematical exposition and visual experiments."
    content = polish_description(content)
    if len(content) > 260:
        content = content[:257].rstrip() + "..."
    return Row(title=title, content=content, filename=rel, type="notebook")


def parse_vignettes() -> List[Row]:
    text = MYDATA.read_text(encoding="utf-8")
    m = re.search(r"const\s+textData\s*=\s*`(.*)`\s*;\s*$", text, flags=re.S)
    if not m:
        raise RuntimeError("Could not parse textData from vignettes/mydata.js")

    blob = m.group(1).strip()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", blob) if b.strip()]
    out: List[Row] = []
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        date = lines[0]
        name = lines[1]
        desc = polish_description(" ".join(lines[2:])) if len(lines) > 2 else ""
        stem = re.sub(r"^\d+[-_]*", "", Path(name).stem)
        stem = stem.replace(".", " ")
        title = clean_text(stem.replace("-", " ").replace("_", " ").title())
        if not title:
            title = f"Vignette {name}"
        content = desc if desc else f"Vignette entry from {date}."
        if len(content) > 320:
            content = content[:317].rstrip() + "..."
        out.append(
            Row(
                title=title,
                content=content,
                filename=f"vignettes/{name}",
                type="vignette",
            )
        )
    return out


def main() -> None:
    readme_map = parse_readme_notebook_blurbs()
    rows: List[Row] = []

    for nb in sorted(PYTHON_DIR.glob("**/*.ipynb")):
        rel = nb.relative_to(ROOT).as_posix()
        if rel in readme_map:
            rows.append(readme_map[rel])
        else:
            rows.append(parse_notebook_fallback(nb))

    rows.extend(parse_vignettes())

    existing_rows: List[Row] = []
    dropped: List[str] = []
    for r in rows:
        if (ROOT / r.filename).exists():
            existing_rows.append(r)
        else:
            dropped.append(r.filename)

    df = pd.DataFrame([r.__dict__ for r in existing_rows], columns=["title", "content", "filename", "type"])
    df.to_excel(DB_XLSX, index=False)
    DB_JSON.write_text(df.to_json(orient="records", force_ascii=False, indent=2), encoding="utf-8")
    DB_JS.write_text(
        "window.CATALOG_DATA = " + df.to_json(orient="records", force_ascii=False) + ";\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(df)} rows:")
    print(f" - {DB_XLSX.relative_to(ROOT)}")
    print(f" - {DB_JSON.relative_to(ROOT)}")
    print(f" - {DB_JS.relative_to(ROOT)}")
    if dropped:
        print(f"Dropped {len(dropped)} missing-file entries.")
        for name in dropped[:20]:
            print(f"   - {name}")


if __name__ == "__main__":
    main()

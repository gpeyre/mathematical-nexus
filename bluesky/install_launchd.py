#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
LABEL = "com.mathematical-nexus.bluesky"


def main() -> None:
    parser = argparse.ArgumentParser(description="Render or install the macOS launchd scheduler.")
    parser.add_argument("--install", action="store_true", help="Install and bootstrap the LaunchAgent")
    args = parser.parse_args()
    template = (HERE / f"{LABEL}.plist.template").read_text(encoding="utf-8")
    rendered = template.replace("__PYTHON__", sys.executable).replace("__REPO_ROOT__", str(HERE.parent))
    preview = HERE / f"{LABEL}.plist"
    preview.write_text(rendered, encoding="utf-8")
    print(f"Rendered {preview}")
    if not args.install:
        print("Preview only. Re-run with --install after reviewing batch 1 and testing credentials.")
        return
    agents = Path.home() / "Library" / "LaunchAgents"
    agents.mkdir(parents=True, exist_ok=True)
    target = agents / f"{LABEL}.plist"
    target.write_text(rendered, encoding="utf-8")
    domain = f"gui/{os.getuid()}"
    subprocess.run(["launchctl", "bootout", domain, str(target)], check=False)
    subprocess.run(["launchctl", "bootstrap", domain, str(target)], check=True)
    print(f"Installed and bootstrapped {target}")


if __name__ == "__main__":
    main()

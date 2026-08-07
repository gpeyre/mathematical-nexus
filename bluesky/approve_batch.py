#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys

from common import read_schedule_rows, schedule_path, set_row_values


def main() -> None:
    parser = argparse.ArgumentParser(description="Approve one reviewed batch of Bluesky posts.")
    parser.add_argument("--batch", required=True, type=int)
    parser.add_argument("--force", action="store_true", help="Also re-approve error/skipped rows")
    args = parser.parse_args()
    subprocess.run([sys.executable, "validate_schedule.py", "--batch", str(args.batch)], check=True)
    wb, ws, rows = read_schedule_rows()
    selected = [row for row in rows if int(row["batch_id"]) == args.batch]
    if not selected:
        raise SystemExit(f"Batch {args.batch} does not exist")
    changed = 0
    for row in selected:
        if row["status"] == "review" or (args.force and row["status"] in {"error", "skipped"}):
            set_row_values(ws, row["_excel_row"], {"status": "approved", "last_error": ""})
            changed += 1
    wb.save(schedule_path())
    print(f"Approved {changed} rows in batch {args.batch} ({len(selected)} total rows)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from common import ROOT, grapheme_len, load_config, parse_local_timestamp, read_schedule_rows


ALLOWED_STATUSES = {"review", "approved", "posted", "error", "skipped"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Bluesky Excel queue.")
    parser.add_argument("--batch", type=int, help="Validate only one batch")
    args = parser.parse_args()
    config = load_config()
    _, _, rows = read_schedule_rows()
    if args.batch:
        rows = [row for row in rows if int(row["batch_id"]) == args.batch]
    errors: list[str] = []
    warnings: list[str] = []
    previous_date = None
    for row in rows:
        prefix = f"queue {row['queue_id']} ({row['filename']})"
        media = ROOT / str(row["filename"])
        if not media.exists():
            errors.append(f"{prefix}: missing media file")
        if grapheme_len(str(row["comment"] or "")) > int(config["max_graphemes"]):
            errors.append(f"{prefix}: comment exceeds {config['max_graphemes']} graphemes")
        if row["status"] not in ALLOWED_STATUSES:
            errors.append(f"{prefix}: invalid status {row['status']!r}")
        timezone_name = str(row["timezone"])
        local_dt = parse_local_timestamp(str(row["scheduled_at_local"]), timezone_name)
        local_date = local_dt.astimezone(ZoneInfo(timezone_name)).date()
        if local_dt.strftime("%H:%M") != str(row["publication_time"]):
            errors.append(f"{prefix}: local timestamp and publication_time disagree")
        if previous_date and not args.batch and local_date - previous_date != timedelta(days=1):
            errors.append(f"{prefix}: schedule is not exactly one local day after previous row")
        previous_date = local_date
        if media.exists() and row["media_type"] == "image" and media.stat().st_size > 2_000_000:
            warnings.append(f"{prefix}: image will be recompressed before upload ({media.stat().st_size} bytes)")
        if media.exists() and row["media_type"] == "video" and media.stat().st_size > 50 * 1024 * 1024:
            errors.append(f"{prefix}: video exceeds the 50 MiB PDS blob limit")
    print(f"Validated {len(rows)} rows: {len(errors)} errors, {len(warnings)} warnings")
    for warning in warnings:
        print("WARNING:", warning)
    for error in errors:
        print("ERROR:", error)
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()

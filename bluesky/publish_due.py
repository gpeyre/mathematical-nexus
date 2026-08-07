#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from client import BlueskyClient
from common import HERE, ROOT, load_config, parse_local_timestamp, read_schedule_rows, schedule_path, set_row_values


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish approved Bluesky posts that are due.")
    parser.add_argument("--publish", action="store_true", help="Actually publish; otherwise print a dry run")
    parser.add_argument("--max-posts", type=int, default=1, help="Safety cap per invocation")
    parser.add_argument("--batch", type=int, help="Restrict to one approved batch")
    args = parser.parse_args()
    config = load_config()
    now = datetime.now(ZoneInfo(config["timezone"]))
    lock_path = HERE / "publish.lock"
    lock_path.touch(exist_ok=True)
    with lock_path.open("r+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        wb, ws, rows = read_schedule_rows()
        due = [
            row for row in rows
            if row["status"] == "approved"
            and (not args.batch or int(row["batch_id"]) == args.batch)
            and parse_local_timestamp(str(row["scheduled_at_local"]), str(row["timezone"])) <= now
        ]
        due.sort(key=lambda row: int(row["queue_id"]))
        due = due[: max(0, args.max_posts)]
        if not due:
            print(f"No approved post is due at {now.isoformat(timespec='minutes')}")
            return
        if not args.publish:
            for row in due:
                print(f"DRY RUN queue={row['queue_id']} batch={row['batch_id']} file={row['filename']}")
                print(row["comment"])
            return

        client = BlueskyClient()
        log_dir = HERE / "logs"
        log_dir.mkdir(exist_ok=True)
        for row in due:
            try:
                result = client.publish(row, ROOT / str(row["filename"]))
                posted = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
                updates = {
                    "status": "posted",
                    "posted_at_utc": posted,
                    "post_uri": result.get("uri", ""),
                    "post_cid": result.get("cid", ""),
                    "last_error": "",
                }
                print(f"POSTED queue={row['queue_id']} {updates['post_uri']}")
            except Exception as exc:
                updates = {"status": "error", "last_error": f"{type(exc).__name__}: {exc}"}
                print(f"ERROR queue={row['queue_id']}: {updates['last_error']}")
            set_row_values(ws, row["_excel_row"], updates)
            with (log_dir / "publish.jsonl").open("a", encoding="utf-8") as stream:
                stream.write(json.dumps({"queue_id": row["queue_id"], **updates}, ensure_ascii=False) + "\n")
            wb.save(schedule_path())


if __name__ == "__main__":
    main()

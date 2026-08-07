# Mathematical Nexus on Bluesky

This directory contains a reviewable, timezone-aware publishing queue for the vignettes in `vignettes/`.
The schedule starts on **2026-07-12 at 07:00 Europe/Paris**, with one post per day.

## Why the scheduler runs locally

The AT Protocol creates a post as soon as `com.atproto.repo.createRecord` is called. A future `createdAt`
value is not a scheduling mechanism. Therefore, `bluesky_schedule.xlsx` is the source of truth and
`publish_due.py` calls the API only when an approved row is due.

## Files

- `bluesky_schedule.xlsx`: master schedule, editorial text, approval state, and API result fields.
- `batches/batch_NNN.xlsx`: review sheets containing 20 consecutive posts (19 in the final batch).
- `batches/batch_NNN.json`: machine-readable snapshots of the same batches.
- `build_schedule.py`: rebuilds dates and batch files while preserving edited comments and statuses.
- `validate_schedule.py`: checks dates, comments, files, statuses, and Bluesky media limits.
- `approve_batch.py`: moves a reviewed batch from `review` to `approved`.
- `publish_due.py`: dry-runs or publishes the oldest approved due row, at most one by default.
- `client.py`: authentication, image preparation, video processing, facets, and idempotent post creation.

## Credentials

Create an app password in Bluesky, then:

```bash
cd bluesky
cp .env.example .env
# Edit .env; never commit it.
python3 -m pip install -r requirements.txt
```

## Review and approve 20 posts

Open `batches/batch_001.xlsx`, correct comments or dates there, import those edits into the master schedule,
validate, then approve the batch:

```bash
cd bluesky
python3 import_batch.py --batch 1
python3 validate_schedule.py --batch 1
python3 approve_batch.py --batch 1
python3 publish_due.py --batch 1        # dry run
```

Actual publication is deliberately explicit:

```bash
python3 publish_due.py --publish --max-posts 1
```

The deterministic `record_key` prevents duplicate records if a run is repeated after a network interruption.

## Daily automation on macOS

The launchd template checks the queue once per minute; timezone gating inside `publish_due.py` ensures the post
becomes eligible at 07:00 Europe/Paris even if the computer's display timezone changes. Render a local preview,
and install it only after the first batch has been reviewed and credentials have been tested:

```bash
cd bluesky
python3 install_launchd.py
python3 install_launchd.py --install
```

If the computer is asleep at 07:00, the oldest due approved item is posted on the next run. The one-post safety
cap prevents a burst of missed posts.

## Media handling

- Images are stripped of metadata and compressed below 1.9 MB before upload.
- `.m4v` files are sent as `video/mp4` to Bluesky's video preprocessing service, then embedded in the post.
- Video publication requires a verified Bluesky account email and is subject to account-level daily limits.

## API references

- https://docs.bsky.app/docs/tutorials/creating-a-post
- https://docs.bsky.app/docs/tutorials/video
- https://docs.bsky.app/docs/advanced-guides/posts

from __future__ import annotations

import io
import mimetypes
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image

from common import HERE, URL_RE, load_config, load_dotenv


class BlueskyClient:
    def __init__(self) -> None:
        load_dotenv()
        self.handle = os.environ.get("BLUESKY_HANDLE", "")
        self.password = os.environ.get("BLUESKY_APP_PASSWORD", "")
        self.pds_url = os.environ.get("BLUESKY_PDS_URL", "https://bsky.social").rstrip("/")
        if not self.handle or not self.password:
            raise RuntimeError("Set BLUESKY_HANDLE and BLUESKY_APP_PASSWORD in bluesky/.env")
        self.http = requests.Session()
        response = self.http.post(
            f"{self.pds_url}/xrpc/com.atproto.server.createSession",
            json={"identifier": self.handle, "password": self.password},
            timeout=30,
        )
        response.raise_for_status()
        self.session = response.json()

    @property
    def auth_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.session['accessJwt']}"}

    def upload_blob(self, payload: bytes, content_type: str) -> dict:
        response = self.http.post(
            f"{self.pds_url}/xrpc/com.atproto.repo.uploadBlob",
            headers={**self.auth_headers, "Content-Type": content_type},
            data=payload,
            timeout=180,
        )
        response.raise_for_status()
        return response.json()["blob"]

    def prepare_image(self, path: Path, max_bytes: int) -> tuple[bytes, str, tuple[int, int]]:
        with Image.open(path) as source:
            image = source.convert("RGBA")
            width, height = image.size
            if image.mode == "RGBA":
                background = Image.new("RGB", image.size, "white")
                background.paste(image, mask=image.getchannel("A"))
                image = background
            for quality in (92, 86, 80, 74, 68, 60):
                output = io.BytesIO()
                image.save(output, format="JPEG", quality=quality, optimize=True, progressive=True)
                if output.tell() <= max_bytes:
                    return output.getvalue(), "image/jpeg", (width, height)
            scale = 0.85
            while scale > 0.3:
                resized = image.resize((int(width * scale), int(height * scale)), Image.Resampling.LANCZOS)
                output = io.BytesIO()
                resized.save(output, format="JPEG", quality=74, optimize=True, progressive=True)
                if output.tell() <= max_bytes:
                    return output.getvalue(), "image/jpeg", resized.size
                scale *= 0.85
        raise RuntimeError(f"Could not compress {path} below {max_bytes} bytes")

    def upload_video_service(self, path: Path, timeout_seconds: int) -> dict:
        host = urlparse(self.pds_url).hostname
        auth = self.http.get(
            f"{self.pds_url}/xrpc/com.atproto.server.getServiceAuth",
            headers=self.auth_headers,
            params={
                "aud": f"did:web:{host}",
                "lxm": "com.atproto.repo.uploadBlob",
                "exp": int(time.time()) + 30 * 60,
            },
            timeout=30,
        )
        auth.raise_for_status()
        token = auth.json()["token"]
        upload = self.http.post(
            "https://video.bsky.app/xrpc/app.bsky.video.uploadVideo",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "video/mp4"},
            params={"did": self.session["did"], "name": path.name},
            data=path.read_bytes(),
            timeout=300,
        )
        payload = upload.json()
        if not upload.ok and not payload.get("blob"):
            upload.raise_for_status()
        blob = payload.get("blob")
        job_id = payload.get("jobId")
        deadline = time.time() + timeout_seconds
        while not blob and job_id and time.time() < deadline:
            time.sleep(2)
            status = self.http.get(
                "https://video.bsky.app/xrpc/app.bsky.video.getJobStatus",
                params={"jobId": job_id},
                timeout=30,
            )
            status.raise_for_status()
            job = status.json().get("jobStatus", status.json())
            blob = job.get("blob")
            if job.get("state") in {"JOB_STATE_FAILED", "failed"}:
                raise RuntimeError(f"Video processing failed: {job}")
        if not blob:
            raise TimeoutError(f"Video processing did not finish within {timeout_seconds}s")
        return blob

    @staticmethod
    def url_facets(text: str) -> list[dict]:
        facets = []
        for match in URL_RE.finditer(text):
            start = len(text[: match.start()].encode("utf-8"))
            end = len(text[: match.end()].encode("utf-8"))
            facets.append({
                "index": {"byteStart": start, "byteEnd": end},
                "features": [{"$type": "app.bsky.richtext.facet#link", "uri": match.group(0)}],
            })
        return facets

    def publish(self, row: dict, media_path: Path) -> dict:
        config = load_config()
        if row["media_type"] == "image":
            image, mime, (width, height) = self.prepare_image(media_path, int(config["image_max_bytes"]))
            blob = self.upload_blob(image, mime)
            embed = {
                "$type": "app.bsky.embed.images",
                "images": [{
                    "alt": str(row["alt_text"] or ""),
                    "image": blob,
                    "aspectRatio": {"width": width, "height": height},
                }],
            }
        else:
            if config["video_upload_mode"] == "video_service":
                blob = self.upload_video_service(media_path, int(config["video_processing_timeout_seconds"]))
            else:
                blob = self.upload_blob(media_path.read_bytes(), "video/mp4")
            embed = {
                "$type": "app.bsky.embed.video",
                "video": blob,
                "alt": str(row["alt_text"] or ""),
            }

        now = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        text = str(row["comment"])
        record = {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": now,
            "langs": [config["post_language"]],
            "embed": embed,
        }
        facets = self.url_facets(text)
        if facets:
            record["facets"] = facets
        payload = {
            "repo": self.session["did"],
            "collection": "app.bsky.feed.post",
            "rkey": str(row["record_key"]),
            "record": record,
        }
        response = self.http.post(
            f"{self.pds_url}/xrpc/com.atproto.repo.createRecord",
            headers={**self.auth_headers, "Content-Type": "application/json"},
            json=payload,
            timeout=60,
        )
        if response.status_code == 400 and "already" in response.text.lower():
            existing = self.http.get(
                f"{self.pds_url}/xrpc/com.atproto.repo.getRecord",
                params={"repo": self.session["did"], "collection": "app.bsky.feed.post", "rkey": row["record_key"]},
                timeout=30,
            )
            existing.raise_for_status()
            return existing.json()
        response.raise_for_status()
        return response.json()

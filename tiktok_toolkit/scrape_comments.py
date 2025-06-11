import pandas as pd
import re
import os
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "extern" / "tiktokcomment"))
from tiktokcomment import TiktokComment
from tiktokcomment.typing import Comments
from loguru import logger


def get_downloaded_ids(output_dir: str) -> set[str]:
    """Gibt Video-IDs zurück, zu denen eine .mp4-Datei existiert, aber keine entsprechende Kommentar-JSON."""
    output_path = Path(output_dir)
    mp4_pattern = re.compile(r"tiktok_(\d{8,})_video\.mp4")
    comment_pattern = re.compile(r"tiktok_(\d{8,})_comments\.json")

    mp4_ids = set()
    comment_ids = set()

    for file in output_path.iterdir():
        if file.suffix == ".mp4":
            match = mp4_pattern.search(file.name)
            if match:
                mp4_ids.add(match.group(1))
        elif file.suffix == ".json":
            match = comment_pattern.search(file.name)
            if match:
                comment_ids.add(match.group(1))
    print(len(mp4_ids - comment_ids))
    return mp4_ids - comment_ids


def scrape_comments_batch(
    video_ids: list[str],
    output_dir: str = "comments/",
    start_index: int = 0,
):
    """Scraped Kommentare für eine Liste von Video-IDs."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tc = TiktokComment()

    for i, video_id in enumerate(video_ids[start_index:], start=start_index):
        try:
            logger.info(f"[{i}] Starte Kommentar-Scraping für Video-ID: {video_id}")
            comments: Comments = tc(aweme_id=video_id)
            output_file = os.path.join(output_dir, f"tiktok_{video_id}_comments.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(comments.dict, f, ensure_ascii=False, indent=2)
            logger.success(f"Gespeichert: {output_file}")
        except Exception as e:
            logger.error(f"Fehler bei {video_id}: {e}")

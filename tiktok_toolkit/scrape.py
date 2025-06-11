import pandas as pd
import re
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "extern" / "TT_Scraper"))
from TT_Scraper import TT_Scraper


def get_downloaded_ids(output_dir: str) -> set[str]:
    """Liest bereits vorhandene Video-IDs im Output-Verzeichnis anhand von Dateinamen."""
    existing_ids = set()
    id_pattern = re.compile(r"(\d{8,})")
    for file in os.listdir(output_dir):
        if (
            file.endswith(".mp4")
            or file.endswith(".json")
            or os.path.isdir(os.path.join(output_dir, file))
        ):
            match = id_pattern.search(file)
            if match:
                existing_ids.add(match.group(1))
    return existing_ids


def extract_video_ids_from_csv(file_path: str) -> list[str]:
    """Extrahiert alle TikTok Video-IDs aus einer CSV-Datei."""
    df = pd.read_csv(file_path)
    pattern = re.compile(r"/video/(\d+)")
    video_ids = set()

    for col in df.columns:
        for cell in df[col].dropna():
            matches = pattern.findall(str(cell))
            video_ids.update(matches)

    return sorted(video_ids)


def scrape_video_list(
    video_ids: list[str],
    output_dir: str = "downloads/",
    start_index: int = 0,
    wait_time: float = 0.3,
    clear_console: bool = True,
):
    """Scraped eine Liste von Video-IDs."""
    if not video_ids:
        print("✅ Keine Video-IDs übergeben.")
        return

    print(f"🆕 Starte Scraping von {len(video_ids)} Video(s)...")
    scraper = TT_Scraper(wait_time=wait_time, output_files_fp=output_dir)
    scraper.scrape_list(ids=video_ids, scrape_content=True, clear_console=clear_console)


def scrape_user_profile(
    username: str,
    output_dir: str = "downloads/",
    wait_time: float = 0.3,
    download_metadata: bool = True,
):
    """Scraped ein gesamtes TikTok-Profil (z. B. Maximilian Pütz)."""
    scraper = TT_Scraper(wait_time=wait_time, output_files_fp=output_dir)
    scraper.scrape_user(
        username=username,
        download_metadata=download_metadata,
    )

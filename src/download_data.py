"""
download_data.py
----------------
Downloads UniMorph TSV files for English, Spanish, and Swedish
from the official UniMorph GitHub repositories.

Usage:
    python src/download_data.py
"""

import os
import requests

UNIMORPH_URLS = {
    "eng": "https://raw.githubusercontent.com/unimorph/eng/master/eng",
    "spa": "https://raw.githubusercontent.com/unimorph/spa/master/spa",
    "swe": "https://raw.githubusercontent.com/unimorph/swe/master/swe",
}

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def download(lang: str, url: str) -> None:
    dest_dir = os.path.join(DATA_DIR, lang)
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, f"{lang}.tsv")

    if os.path.exists(dest_file):
        size_mb = os.path.getsize(dest_file) / 1e6
        print(f"[{lang}] Already exists ({size_mb:.1f} MB) — skipping. Delete to re-download.")
        return

    print(f"[{lang}] Downloading from {url} ...")
    response = requests.get(url, timeout=60, stream=True)
    response.raise_for_status()

    total = int(response.headers.get("content-length", 0))
    downloaded = 0
    with open(dest_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 64):
            f.write(chunk)
            downloaded += len(chunk)
            if total:
                pct = downloaded / total * 100
                print(f"\r[{lang}] {pct:.1f}%  ({downloaded/1e6:.1f}/{total/1e6:.1f} MB)", end="", flush=True)

    size_mb = os.path.getsize(dest_file) / 1e6
    print(f"\r[{lang}] Done — {size_mb:.1f} MB saved to {dest_file}")


if __name__ == "__main__":
    for lang, url in UNIMORPH_URLS.items():
        download(lang, url)
    print("\nAll datasets ready.")

"""
download_datasets.py
--------------------
Downloads UniMorph TSV files for English, Spanish, Swedish, and Finnish
from the official UniMorph GitHub repositories.

Finnish is split upstream into fin.1 + fin.2; those are concatenated into fin.tsv.

Usage:
    python src/download_datasets.py
"""

import os
import requests

# Single-file languages: raw GitHub path → data/<lang>/<lang>.tsv
UNIMORPH_URLS = {
    "eng": "https://raw.githubusercontent.com/unimorph/eng/master/eng",
    "spa": "https://raw.githubusercontent.com/unimorph/spa/master/spa",
    "swe": "https://raw.githubusercontent.com/unimorph/swe/master/swe",
}

# Finnish is published as two parts that together form the full table
FIN_PART_URLS = [
    "https://raw.githubusercontent.com/unimorph/fin/master/fin.1",
    "https://raw.githubusercontent.com/unimorph/fin/master/fin.2",
]

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _stream_to_file(url: str, dest_file: str, label: str) -> None:
    print(f"[{label}] Downloading from {url} ...")
    response = requests.get(url, timeout=120, stream=True)
    response.raise_for_status()

    total = int(response.headers.get("content-length", 0))
    downloaded = 0
    with open(dest_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 64):
            f.write(chunk)
            downloaded += len(chunk)
            if total:
                pct = downloaded / total * 100
                print(
                    f"\r[{label}] {pct:.1f}%  ({downloaded / 1e6:.1f}/{total / 1e6:.1f} MB)",
                    end="",
                    flush=True,
                )
    size_mb = os.path.getsize(dest_file) / 1e6
    print(f"\r[{label}] Done — {size_mb:.1f} MB saved to {dest_file}")


def download(lang: str, url: str) -> None:
    dest_dir = os.path.join(DATA_DIR, lang)
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, f"{lang}.tsv")

    if os.path.exists(dest_file):
        size_mb = os.path.getsize(dest_file) / 1e6
        print(f"[{lang}] Already exists ({size_mb:.1f} MB) — skipping. Delete to re-download.")
        return

    _stream_to_file(url, dest_file, lang)


def download_finnish() -> None:
    dest_dir = os.path.join(DATA_DIR, "fin")
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, "fin.tsv")

    if os.path.exists(dest_file):
        size_mb = os.path.getsize(dest_file) / 1e6
        print(f"[fin] Already exists ({size_mb:.1f} MB) — skipping. Delete to re-download.")
        return

    part_paths = []
    for i, url in enumerate(FIN_PART_URLS, start=1):
        part_path = os.path.join(dest_dir, f"fin.{i}.part")
        _stream_to_file(url, part_path, f"fin.{i}")
        part_paths.append(part_path)

    print("[fin] Concatenating fin.1 + fin.2 → fin.tsv ...")
    with open(dest_file, "wb") as out:
        for part_path in part_paths:
            with open(part_path, "rb") as inp:
                out.write(inp.read())
            os.remove(part_path)

    size_mb = os.path.getsize(dest_file) / 1e6
    print(f"[fin] Done — {size_mb:.1f} MB saved to {dest_file}")


if __name__ == "__main__":
    for lang, url in UNIMORPH_URLS.items():
        download(lang, url)
    download_finnish()
    print("\nAll datasets ready.")

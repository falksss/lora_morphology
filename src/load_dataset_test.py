import pandas as pd
import requests
from io import StringIO

# UniMorph TSV files are hosted directly on GitHub
# Format per row: lemma \t features \t surface_form
UNIMORPH_URLS = {
    "eng": "https://raw.githubusercontent.com/unimorph/eng/master/eng",
    "spa": "https://raw.githubusercontent.com/unimorph/spa/master/spa",
    "swe": "https://raw.githubusercontent.com/unimorph/swe/master/swe",
}

def load_unimorph(lang: str) -> pd.DataFrame:
    url = UNIMORPH_URLS[lang]
    print(f"Fetching {lang} from {url} ...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    df = pd.read_csv(
        StringIO(response.text),
        sep="\t",
        header=None,
        names=["lemma", "surface_form", "features"],
        comment="#",       # skip comment lines if any
    )
    df = df.dropna()
    return df

if __name__ == "__main__":
    for lang in ["eng", "spa", "swe"]:
        df = load_unimorph(lang)
        print(f"\n=== {lang.upper()} — {len(df):,} rows ===")
        print(df.head(5).to_string(index=False))

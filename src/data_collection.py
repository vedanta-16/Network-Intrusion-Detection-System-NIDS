from pathlib import Path

import pandas as pd

try:
    from src.config import DATA_RAW_PATH
except ModuleNotFoundError:  # direct execution fallback
    from config import DATA_RAW_PATH

RAW_PATH = DATA_RAW_PATH


def load_raw_data(path=RAW_PATH):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Generate the included demo dataset with:\n"
            "  python -m src.generate_sample_data"
        )
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Dataset is empty: {path}")
    return df


def save_raw_data(df, path=RAW_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    df = load_raw_data()
    print(f"Loaded {len(df):,} traffic records from {RAW_PATH}")
    print(df.head())

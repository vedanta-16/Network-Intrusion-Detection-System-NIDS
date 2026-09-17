"""
Generate a synthetic network-flow dataset for local development and testing.

This is NEW — it did not exist in the original project. train.py expects a
CSV at data/raw/traffic.csv with a 'Label' column, but nothing in the
original code produced that file, so the pipeline could not be run
end-to-end. Run this once to create a realistic-looking sample dataset,
or replace data/raw/traffic.csv with a real capture (e.g. CICIDS2017/
CICFlowMeter export) using the same column names.

Usage:
    python -m src.generate_sample_data
    python -m src.generate_sample_data --rows 20000 --attack-ratio 0.25
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.feature_extraction import DEFAULT_FEATURES

RAW_PATH = Path("data/raw/traffic.csv")

ATTACK_TYPES = ["PortScan", "DoS", "Bruteforce", "DDoS", "Botnet"]


def _benign_rows(n, rng):
    return pd.DataFrame({
        "Flow Duration": rng.normal(500000, 150000, n).clip(1000),
        "Total Fwd Packets": rng.poisson(12, n) + 1,
        "Total Backward Packets": rng.poisson(10, n) + 1,
        "Total Length of Fwd Packets": rng.normal(1200, 400, n).clip(60),
        "Total Length of Bwd Packets": rng.normal(1500, 500, n).clip(60),
        "Fwd Packet Length Mean": rng.normal(100, 30, n).clip(20),
        "Bwd Packet Length Mean": rng.normal(150, 40, n).clip(20),
        "Flow Bytes/s": rng.normal(3000, 1000, n).clip(10),
        "Flow Packets/s": rng.normal(20, 8, n).clip(1),
        "SYN Flag Count": rng.poisson(1, n),
        "ACK Flag Count": rng.poisson(8, n),
        "RST Flag Count": rng.poisson(0.2, n),
        "Label": "BENIGN",
    })


def _attack_rows(n, rng):
    labels = rng.choice(ATTACK_TYPES, size=n)
    return pd.DataFrame({
        "Flow Duration": rng.normal(20000, 8000, n).clip(100),
        "Total Fwd Packets": rng.poisson(150, n) + 5,
        "Total Backward Packets": rng.poisson(2, n),
        "Total Length of Fwd Packets": rng.normal(400, 150, n).clip(40),
        "Total Length of Bwd Packets": rng.normal(80, 40, n).clip(0),
        "Fwd Packet Length Mean": rng.normal(40, 15, n).clip(10),
        "Bwd Packet Length Mean": rng.normal(30, 15, n).clip(0),
        "Flow Bytes/s": rng.normal(50000, 20000, n).clip(100),
        "Flow Packets/s": rng.normal(400, 150, n).clip(5),
        "SYN Flag Count": rng.poisson(40, n),
        "ACK Flag Count": rng.poisson(2, n),
        "RST Flag Count": rng.poisson(15, n),
        "Label": labels,
    })


def generate(rows=10000, attack_ratio=0.2, seed=42):
    rng = np.random.default_rng(seed)
    n_attack = int(rows * attack_ratio)
    n_benign = rows - n_attack

    df = pd.concat([_benign_rows(n_benign, rng), _attack_rows(n_attack, rng)], ignore_index=True)

    # Add a couple of identifying columns the dashboard likes to display.
    ip_pool = [f"192.168.1.{i}" for i in range(2, 60)]
    df["Source IP"] = rng.choice(ip_pool, size=len(df))
    df["Destination IP"] = rng.choice(ip_pool, size=len(df))
    df["Protocol"] = rng.choice(["TCP", "UDP", "ICMP"], size=len(df))

    ordered_cols = ["Source IP", "Destination IP", "Protocol"] + DEFAULT_FEATURES + ["Label"]
    df = df[ordered_cols].sample(frac=1, random_state=seed).reset_index(drop=True)
    return df


def main():
    parser = argparse.ArgumentParser(description="Generate a synthetic NIDS training dataset.")
    parser.add_argument("--rows", type=int, default=10000, help="Total number of flow records.")
    parser.add_argument("--attack-ratio", type=float, default=0.2, help="Fraction of rows labeled as attacks.")
    parser.add_argument("--out", type=str, default=str(RAW_PATH), help="Output CSV path.")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    df = generate(rows=args.rows, attack_ratio=args.attack_ratio, seed=args.seed)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df):,} synthetic flow records to {out_path}")
    print(df["Label"].value_counts())


if __name__ == "__main__":
    main()

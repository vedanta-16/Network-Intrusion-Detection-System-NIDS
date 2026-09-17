from pathlib import Path

import joblib
import pandas as pd

try:
    from src.config import MODEL_PATH
except ModuleNotFoundError:  # direct execution fallback
    from config import MODEL_PATH


def load_model():
    model_path = Path(MODEL_PATH)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Trained model not found: {model_path}\n"
            "Train it first with:\n"
            "  python -m src.train"
        )
    return joblib.load(model_path)


def predict_traffic(df):
    bundle = load_model()
    model = bundle["model"]
    features = bundle["features"]

    missing = [feature for feature in features if feature not in df.columns]
    if missing:
        raise ValueError(
            "The uploaded CSV is missing required model features: " + ", ".join(missing)
        )

    X = df[features].copy()
    # The model expects numeric network-flow features.
    for column in features:
        X[column] = pd.to_numeric(X[column], errors="coerce")

    if X.isna().any().any():
        bad = X.columns[X.isna().any()].tolist()
        raise ValueError(f"Non-numeric or missing values found in feature columns: {bad}")

    result = df.copy()
    result["prediction"] = model.predict(X)

    if hasattr(model, "predict_proba"):
        result["confidence"] = model.predict_proba(X).max(axis=1)

    return result

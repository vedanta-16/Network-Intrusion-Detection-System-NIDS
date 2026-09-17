from pathlib import Path

import pandas as pd

from src.generate_sample_data import generate
from src.feature_extraction import DEFAULT_FEATURES
from src.predict import predict_traffic


def test_generated_data_has_required_features():
    df = generate(rows=100, attack_ratio=0.2)
    assert all(feature in df.columns for feature in DEFAULT_FEATURES)
    assert "Label" in df.columns
    assert len(df) == 100


def test_prediction_with_trained_artifact(tmp_path, monkeypatch):
    from src import train as train_module

    data_path = tmp_path / "traffic.csv"
    model_path = tmp_path / "nids_model.pkl"
    generate(rows=200, attack_ratio=0.2).to_csv(data_path, index=False)

    monkeypatch.setattr(train_module, "MODEL_PATH", model_path)
    monkeypatch.setattr(train_module, "load_raw_data", lambda: pd.read_csv(data_path))
    train_module.train()

    from src import predict as predict_module
    monkeypatch.setattr(predict_module, "MODEL_PATH", model_path)
    result = predict_module.predict_traffic(pd.read_csv(data_path).head(10))

    assert len(result) == 10
    assert set(result["prediction"]).issubset({"BENIGN", "ATTACK"})
    assert "confidence" in result.columns

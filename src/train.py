"""Train the NIDS binary intrusion-detection model."""
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

try:  # Works with both `python src/train.py` and `python -m src.train`.
    from src.config import MODEL_PATH, RANDOM_STATE, TARGET_COLUMN, TEST_SIZE
    from src.data_collection import load_raw_data
    from src.feature_extraction import DEFAULT_FEATURES, select_network_features
    from src.preprocessing import clean_data
except ModuleNotFoundError:  # pragma: no cover - fallback for unusual invocation
    from config import MODEL_PATH, RANDOM_STATE, TARGET_COLUMN, TEST_SIZE
    from data_collection import load_raw_data
    from feature_extraction import DEFAULT_FEATURES, select_network_features
    from preprocessing import clean_data


def train():
    df = load_raw_data()
    df = clean_data(df)

    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Target column '{TARGET_COLUMN}' not found. "
            f"Available columns: {list(df.columns)}"
        )

    # Train only on the fixed numeric network-flow features. This prevents
    # IP/protocol strings from being encoded inconsistently between training
    # and prediction.
    X = select_network_features(df)
    missing = [c for c in DEFAULT_FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required network features: {missing}")

    y = df[TARGET_COLUMN].astype(str).apply(
        lambda value: "BENIGN" if value.strip().upper() == "BENIGN" else "ATTACK"
    )

    if y.nunique() < 2:
        raise ValueError("Training requires at least two classes: BENIGN and ATTACK.")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_STATE,
        class_weight="balanced",
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print(f"Training samples: {len(X_train):,}")
    print(f"Testing samples:  {len(X_test):,}")
    print(f"Features:         {len(X.columns)}")
    print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
    print("\nClassification Report:\n", classification_report(y_test, predictions))
    print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))

    Path(MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "features": list(X.columns),
            "classes": list(model.classes_),
        },
        MODEL_PATH,
    )
    print(f"\nModel saved to: {MODEL_PATH}")
    return model


if __name__ == "__main__":
    train()

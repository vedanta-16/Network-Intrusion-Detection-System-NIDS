import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_data(df):
    data = df.copy()
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.drop_duplicates()
    data = data.dropna()
    return data

def encode_features(X):
    X = X.copy()
    encoders = {}
    for col in X.select_dtypes(include=["object", "category"]).columns:
        encoder = LabelEncoder()
        X[col] = encoder.fit_transform(X[col].astype(str))
        encoders[col] = encoder
    return X, encoders

def preprocess(df, target_column="Label"):
    data = clean_data(df)
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found.")
    y = data[target_column].astype(str)
    X = data.drop(columns=[target_column])
    X, encoders = encode_features(X)
    return X, y, encoders

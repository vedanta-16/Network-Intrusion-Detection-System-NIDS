DEFAULT_FEATURES = [
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Fwd Packet Length Mean",
    "Bwd Packet Length Mean",
    "Flow Bytes/s",
    "Flow Packets/s",
    "SYN Flag Count",
    "ACK Flag Count",
    "RST Flag Count",
]

def select_network_features(df, features=None):
    features = features or DEFAULT_FEATURES
    available = [f for f in features if f in df.columns]
    if not available:
        raise ValueError("None of the expected network features were found.")
    return df[available].copy()

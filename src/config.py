"""
Centralized configuration.

NEW module. Paths and constants were previously hard-coded separately in
data_collection.py, predict.py, and train.py. This does not change those
files — it just gives new code (and any future refactor) a single place
to change paths/thresholds instead of editing multiple files.
"""
from pathlib import Path

# --- Paths -------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW_PATH = PROJECT_ROOT / "data" / "raw" / "traffic.csv"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_PATH = PROJECT_ROOT / "models" / "nids_model.pkl"
ALERT_LOG_PATH = PROJECT_ROOT / "logs" / "alerts_log.csv"
APP_LOG_PATH = PROJECT_ROOT / "logs" / "nids.log"

# --- Modeling ------------------------------------------------------------
TARGET_COLUMN = "Label"
BENIGN_LABEL = "BENIGN"
ATTACK_LABEL = "ATTACK"
TEST_SIZE = 0.2
RANDOM_STATE = 42

# --- Alerting thresholds --------------------------------------------------
HIGH_SEVERITY_CONFIDENCE = 0.90  # matches the threshold already used in alert.py

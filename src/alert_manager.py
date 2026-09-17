"""
Persist alerts to disk so they survive past a single Streamlit session.

This is NEW. src/alert.py builds a single alert dict from one row but
nothing in the original project ever stores it, so there was no way to
review past detections (the README's pipeline ends at "Investigation &
Report", which needs a history to investigate). This module appends
alerts to a CSV log and exposes a loader used by the new
dashboard/pages/1_Alert_History.py page.

It does not modify alert.py — it only consumes the dict that
alert.create_alert() already returns.
"""
from pathlib import Path
import pandas as pd

from src.alert import create_alert

LOG_PATH = Path("logs/alerts_log.csv")

ALERT_COLUMNS = ["time", "source_ip", "destination_ip", "protocol", "prediction", "confidence", "severity"]


def log_alert(row):
    """Build an alert from a result row (via alert.create_alert) and append it to the log."""
    alert = create_alert(row)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame([alert], columns=ALERT_COLUMNS)
    write_header = not LOG_PATH.exists()
    df.to_csv(LOG_PATH, mode="a", header=write_header, index=False)
    return alert


def log_alerts_bulk(rows_df):
    """Vectorized version of log_alert for a DataFrame of ATTACK-labeled rows."""
    if rows_df.empty:
        return 0
    alerts = [create_alert(row) for _, row in rows_df.iterrows()]
    out = pd.DataFrame(alerts, columns=ALERT_COLUMNS)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_header = not LOG_PATH.exists()
    out.to_csv(LOG_PATH, mode="a", header=write_header, index=False)
    return len(out)


def load_alert_history():
    """Return all previously logged alerts, most recent first."""
    if not LOG_PATH.exists():
        return pd.DataFrame(columns=ALERT_COLUMNS)
    df = pd.read_csv(LOG_PATH)
    return df.iloc[::-1].reset_index(drop=True)


def clear_alert_history():
    if LOG_PATH.exists():
        LOG_PATH.unlink()

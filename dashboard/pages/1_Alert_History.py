"""
NEW dashboard page. Streamlit automatically turns any file placed in
dashboard/pages/ into an extra tab in the sidebar, so this sits alongside
dashboard/app.py without requiring any edit to app.py itself.

It reads logs/alerts_log.csv, which is written by src/alert_manager.py.
For this page to show data, alerts need to be logged somewhere in the
main flow — see docs/SETUP_AND_RUN_GUIDE.pdf for the exact snippet to
add to app.py if you want live uploads to populate this history.
"""
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.alert_manager import load_alert_history, clear_alert_history

st.set_page_config(page_title="Alert History", page_icon="Clipboard", layout="wide")
st.title("Alert History")
st.caption("Persisted record of past security alerts, logged across sessions.")

history = load_alert_history()

if history.empty:
    st.info(
        "No alerts logged yet. Alerts are recorded via src/alert_manager.log_alerts_bulk(); "
        "see docs/SETUP_AND_RUN_GUIDE.pdf for how to wire this into the main dashboard."
    )
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Logged Alerts", f"{len(history):,}")
    c2.metric("High Severity", f"{int((history['severity'] == 'HIGH').sum()):,}")
    c3.metric("Medium Severity", f"{int((history['severity'] == 'MEDIUM').sum()):,}")

    st.subheader("All Alerts")
    st.dataframe(history, use_container_width=True)

    st.download_button(
        "Download alert log (CSV)",
        data=history.to_csv(index=False).encode("utf-8"),
        file_name="alerts_log.csv",
        mime="text/csv",
    )

    if st.button("Clear alert history", type="secondary"):
        clear_alert_history()
        st.rerun()

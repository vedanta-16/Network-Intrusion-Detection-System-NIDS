import sys
from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.predict import predict_traffic

st.set_page_config(page_title="NIDS Dashboard", page_icon="Shield", layout="wide")
st.title("Network Intrusion Detection System")
st.caption("ML-based network traffic monitoring and security investigation dashboard")

uploaded = st.file_uploader("Upload network-flow CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.subheader("Traffic Overview")
    st.write(f"Records: **{len(df):,}**")

    try:
        results = predict_traffic(df)
        benign = int((results["prediction"] == "BENIGN").sum())
        malicious = int((results["prediction"] == "ATTACK").sum())

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Traffic", f"{len(results):,}")
        c2.metric("Normal", f"{benign:,}")
        c3.metric("Malicious", f"{malicious:,}")

        st.subheader("Detection Distribution")
        st.bar_chart(results["prediction"].value_counts())

        st.subheader("Security Alerts")
        alerts = results[results["prediction"] == "ATTACK"].copy()
        if not alerts.empty:
            cols = [c for c in ["Source IP", "Destination IP", "Protocol", "prediction", "confidence"] if c in alerts.columns]
            st.dataframe(alerts[cols], use_container_width=True)
        else:
            st.success("No malicious traffic detected.")

        if not alerts.empty:
            st.subheader("Investigation")
            selected = st.number_input("Select alert row", 0, len(alerts)-1, 0)
            st.json(alerts.iloc[int(selected)].to_dict())

    except Exception as exc:
        st.error(str(exc))
else:
    st.info("Upload a compatible network-flow CSV to start detection.")

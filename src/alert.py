from datetime import datetime

def create_alert(row):
    prediction = str(row.get("prediction", "UNKNOWN")).upper()
    confidence = float(row.get("confidence", 0))
    severity = "LOW" if prediction == "BENIGN" else ("HIGH" if confidence >= 0.90 else "MEDIUM")

    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_ip": row.get("Source IP", "N/A"),
        "destination_ip": row.get("Destination IP", "N/A"),
        "protocol": row.get("Protocol", "N/A"),
        "prediction": prediction,
        "confidence": round(confidence, 4),
        "severity": severity,
    }

def generate_alerts(trust_score, anomalies, profile=None):
    """Generate severity-classified alert notifications.

    Each alert is returned as a tuple of (severity, message) where
    severity is one of: 'critical', 'moderate', 'minor'.

    Args:
        trust_score: The overall trust score (0-100).
        anomalies: The anomaly counts dictionary from anomaly.detect_anomalies().
        profile: Optional data profile dictionary for additional alert checks.

    Returns:
        list[tuple]: List of (severity, message) tuples, sorted critical-first.
    """
    alerts = []

    # Trust score alerts
    if trust_score < 50:
        alerts.append(("critical", "Trust score below 50 — data is unreliable for any decision-making"))
    elif trust_score < 70:
        alerts.append(("critical", "Low trust score — decisions based on this data carry significant risk"))

    # Anomaly alerts
    total_anomalies = sum(anomalies.values())
    if total_anomalies > 50:
        alerts.append(("critical", f"Extreme anomaly count ({total_anomalies}) — possible data corruption or collection failure"))
    elif total_anomalies > 10:
        alerts.append(("moderate", f"Elevated anomaly count ({total_anomalies}) — investigate before drawing conclusions"))
    elif total_anomalies > 0:
        alerts.append(("minor", f"{total_anomalies} minor anomalies detected — likely within acceptable range"))

    if profile:
        # Missing data alerts — per-column severity
        severe_missing = {k: v for k, v in profile["missing"].items() if v > 50}
        moderate_missing = {k: v for k, v in profile["missing"].items() if 20 < v <= 50}
        minor_missing = {k: v for k, v in profile["missing"].items() if 5 < v <= 20}

        for col, pct in severe_missing.items():
            alerts.append(("critical", f"'{col}' is {pct:.0f}% missing — column is unreliable for analysis"))

        if moderate_missing:
            cols = ', '.join(f"'{k}' ({v:.0f}%)" for k, v in moderate_missing.items())
            alerts.append(("moderate", f"Significant missing data in: {cols}"))

        if minor_missing:
            cols = ', '.join(f"'{k}' ({v:.0f}%)" for k, v in minor_missing.items())
            alerts.append(("minor", f"Minor missing data in: {cols}"))

        # Duplicate alerts
        if profile["duplicates"] > 0:
            dup_pct = profile["duplicates"] / profile["rows"] * 100 if profile["rows"] > 0 else 0
            if dup_pct > 10:
                alerts.append(("critical", f"{dup_pct:.1f}% of rows are duplicates — likely data entry or collection issue"))
            elif dup_pct > 1:
                alerts.append(("moderate", f"{profile['duplicates']} duplicate rows ({dup_pct:.1f}%) — review data pipeline"))
            else:
                alerts.append(("minor", f"{profile['duplicates']} duplicate rows found — minimal impact"))

    # Sort: critical first, then moderate, then minor
    severity_order = {"critical": 0, "moderate": 1, "minor": 2}
    alerts.sort(key=lambda x: severity_order.get(x[0], 3))

    return alerts

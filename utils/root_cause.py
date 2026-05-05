def find_root_causes(df, anomalies):
    """Identify root causes behind detected anomalies.

    Analyzes anomalous columns to determine WHY anomalies exist,
    not just THAT they exist. Currently checks for extreme high
    values relative to the column mean.

    Args:
        df: A pandas DataFrame containing the data.
        anomalies: The anomaly counts dictionary from anomaly.detect_anomalies().

    Returns:
        list: A list of human-readable root cause descriptions.
    """
    causes = []

    for col, count in anomalies.items():
        if count > 0:
            mean = df[col].mean()
            max_val = df[col].max()
            min_val = df[col].min()

            if mean != 0 and max_val > mean * 3:
                causes.append(f"{col}: Extreme high values causing spikes (max={max_val:.2f}, mean={mean:.2f})")

            if mean != 0 and min_val < mean * -3:
                causes.append(f"{col}: Extreme low values detected (min={min_val:.2f}, mean={mean:.2f})")

    return causes

def calculate_trust(profile, anomalies, total_rows):
    """Calculate a trust score for the dataset (0-100).

    Uses an aggressive, intelligent scoring model that properly
    penalizes critical data quality issues:
    - Missing values (120% weight) — most impactful, especially
      columns with severe missingness get extra penalties.
    - Anomalies/outliers (30% weight)
    - Duplicate rows (20% weight)

    The formula also applies a "worst-column penalty" — if ANY single
    column exceeds 50% missing, an additional deduction is applied.
    This prevents a dataset with one catastrophically bad column from
    scoring misleadingly high.

    Args:
        profile: The data profile dictionary from profiler.profile_data().
        anomalies: The anomaly counts dictionary from anomaly.detect_anomalies().
        total_rows: Total number of rows in the dataset.

    Returns:
        float: A trust score between 0 and 100, rounded to 2 decimal places.
    """
    # Average missing percentage across all columns
    missing_pct = sum(profile["missing"].values()) / len(profile["missing"]) if len(profile["missing"]) > 0 else 0

    # Duplicate percentage
    duplicate_pct = profile["duplicates"] / total_rows * 100 if total_rows > 0 else 0

    # Anomaly percentage
    anomaly_pct = sum(anomalies.values()) / total_rows * 100 if total_rows > 0 else 0

    # Core penalty — increased missing weight from 0.5 → 1.2
    score = 100 - (missing_pct * 1.2 + anomaly_pct * 0.3 + duplicate_pct * 0.2)

    # Worst-column penalty: if any column has >50% missing, apply extra deduction
    severe_cols = [v for v in profile["missing"].values() if v > 50]
    if severe_cols:
        worst = max(severe_cols)
        score -= worst * 0.15  # e.g. 77% missing → -11.55 extra

    return round(max(score, 0), 2)

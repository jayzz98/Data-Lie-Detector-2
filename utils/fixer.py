def suggest_fixes(profile, anomalies=None):
    """Generate actionable fix suggestions based on detected issues.

    Analyzes the data profile and anomalies to produce specific,
    prioritized recommendations for improving data quality.

    Args:
        profile: The data profile dictionary from profiler.profile_data().
        anomalies: Optional anomaly counts dictionary.

    Returns:
        list: A list of human-readable fix suggestion strings.
    """
    fixes = []

    if profile["duplicates"] > 0:
        fixes.append(f"🔄 Remove {profile['duplicates']} duplicate rows using df.drop_duplicates()")

    missing_cols = [k for k, v in profile["missing"].items() if v > 0]
    if missing_cols:
        high_missing = [k for k, v in profile["missing"].items() if v > 50]
        low_missing = [k for k, v in profile["missing"].items() if 0 < v <= 50]

        if high_missing:
            fixes.append(f"🗑️ Consider dropping columns with >50% missing: {', '.join(high_missing)}")
        if low_missing:
            fixes.append(f"🔧 Fill missing values in: {', '.join(low_missing)} (use mean/median for numeric, mode for categorical)")

    if anomalies:
        anomaly_cols = [k for k, v in anomalies.items() if v > 0]
        if anomaly_cols:
            fixes.append(f"📉 Review outliers in: {', '.join(anomaly_cols)} — consider capping or investigating")

    return fixes

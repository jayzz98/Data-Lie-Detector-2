def generate_explanation(score, profile, anomalies):
    """Generate an authoritative, decision-focused data quality explanation.

    Produces sharp, business-grade language that sounds like a senior
    data analyst wrote it. Avoids generic filler. Every sentence adds
    actionable insight. Opens with a "decision safety verdict" that
    frames the entire analysis.

    Args:
        score: The trust score (0-100).
        profile: The data profile dictionary from profiler.profile_data().
        anomalies: The anomaly counts dictionary from anomaly.detect_anomalies().

    Returns:
        str: A space-separated summary of all detected issues and assessments.
    """
    summary = []

    # Detect issues first to inform the opening statement
    missing_cols = [k for k, v in profile["missing"].items() if v > 10]
    severe_missing = [k for k, v in profile["missing"].items() if v > 50]
    anomaly_cols = [k for k, v in anomalies.items() if v > 0]
    has_issues = bool(missing_cols or anomaly_cols or profile["duplicates"] > 0)

    # Decision safety verdict — the killer opening line
    if score >= 85 and not has_issues:
        summary.append("✅ This dataset is safe for both exploratory and decision-critical analysis.")
    elif score >= 85 and has_issues:
        summary.append("⚠️ This dataset is safe for exploratory analysis, but not for high-stakes decisions without addressing the issues below.")
    elif score >= 70:
        summary.append("⚠️ Decisions based on this dataset may be unreliable unless the flagged quality gaps are resolved.")
    elif score >= 50:
        summary.append("🚨 This dataset carries significant risk. Do not use for business-critical decisions without major cleanup.")
    else:
        summary.append("🚨 This dataset is not fit for any decision-making. Immediate remediation required.")

    # Specific findings — sharp, actionable language
    if severe_missing:
        cols_detail = ', '.join(f"'{c}' ({profile['missing'][c]:.0f}%)" for c in severe_missing)
        summary.append(f"Critical gap: {cols_detail} — these columns are effectively unusable in their current state.")
    elif missing_cols:
        cols_detail = ', '.join(f"'{c}'" for c in missing_cols)
        summary.append(f"Missing data in {cols_detail} may introduce bias if not handled properly.")

    if profile["duplicates"] > 0:
        dup_pct = profile["duplicates"] / profile["rows"] * 100 if profile["rows"] > 0 else 0
        summary.append(f"{profile['duplicates']} duplicate rows ({dup_pct:.1f}%) detected — this inflates metrics and skews analysis.")

    if anomaly_cols:
        summary.append(f"Statistical outliers in {', '.join(anomaly_cols)} — verify these represent real-world values before proceeding.")

    return " ".join(summary)


def generate_decision_verdict(score, has_severe_missing):
    """Generate the one-liner decision safety verdict for the dashboard.

    This is the "killer line" shown prominently at the top of the analysis.

    Args:
        score: The trust score (0-100).
        has_severe_missing: Whether any column has >50% missing data.

    Returns:
        tuple: (verdict_text, verdict_class) for rendering.
    """
    if score >= 85 and not has_severe_missing:
        return ("This dataset is safe for exploratory and decision-critical analysis.", "verdict-safe")
    elif score >= 70:
        return ("This dataset is safe for exploratory analysis, but not for high-stakes decisions.", "verdict-caution")
    elif score >= 50:
        return ("This dataset carries risk — verify findings before acting on them.", "verdict-warning")
    else:
        return ("This dataset is not fit for decision-making without major remediation.", "verdict-danger")

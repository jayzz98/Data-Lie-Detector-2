def decision_risk(trust_score):
    """Assess the decision risk level based on the trust score.

    Maps the trust score to a human-readable risk category
    that helps users decide whether to act on this data.

    Args:
        trust_score: The overall trust score (0-100).

    Returns:
        str: A risk level string with emoji indicator.
    """
    if trust_score > 85:
        return "Low Risk ✅"
    elif trust_score > 70:
        return "Medium Risk ⚠️"
    else:
        return "High Risk 🚨"

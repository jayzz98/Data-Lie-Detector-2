def column_trust_score(df):
    """Calculate individual trust scores for each column in the dataset.

    Scores are based on two factors:
    - Missing value percentage (60% weight)
    - Unique value ratio / diversity (40% weight)

    Args:
        df: A pandas DataFrame to analyze.

    Returns:
        dict: A dictionary mapping column names to trust scores (0-100).
    """
    scores = {}

    for col in df.columns:
        missing = df[col].isnull().mean() * 100
        unique = df[col].nunique() / len(df) if len(df) > 0 else 0

        score = 100 - (missing * 0.6 + (1 - unique) * 40)
        scores[col] = round(max(score, 0), 2)

    return scores

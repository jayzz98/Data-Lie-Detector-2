def detect_suspicious_patterns(df, numeric_cols):
    """Detect suspicious patterns that may indicate data manipulation.

    Checks for two key manipulation signals:
    1. Extremely low unique-value ratios (< 1%) suggesting repetitive/fabricated data.
    2. Perfectly uniform increments suggesting synthetic/auto-generated sequences.

    Args:
        df: A pandas DataFrame containing the data.
        numeric_cols: List of numeric column names to analyze.

    Returns:
        list: A list of human-readable warning strings for each detected pattern.
    """
    flags = []

    for col in numeric_cols:
        unique_ratio = df[col].nunique() / len(df) if len(df) > 0 else 0

        # Too repetitive values
        if unique_ratio < 0.01:
            flags.append(f"{col}: Too repetitive (possible manipulation)")

        # Too perfect increments
        diffs = df[col].diff().dropna()
        if len(diffs) > 0 and diffs.nunique() == 1:
            flags.append(f"{col}: Perfect pattern detected")

    return flags

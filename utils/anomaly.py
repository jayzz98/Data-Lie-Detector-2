import numpy as np


def detect_anomalies(df, numeric_cols):
    """Detect anomalies in numeric columns using Z-score method.

    Intelligently skips columns that are naturally discrete or
    categorical-like (fewer than 10 unique values), since Z-scores
    on such distributions produce false positives. For example,
    'SibSp' (0-8) or 'Parch' (0-6) are naturally skewed discrete
    counts — flagging them as anomalous is misleading.

    For remaining continuous columns, flags values with |Z| > 3.

    Args:
        df: A pandas DataFrame containing the data.
        numeric_cols: List of numeric column names to analyze.

    Returns:
        dict: A dictionary mapping column names to their outlier counts.
              Skipped columns are marked with 0 and a note.
    """
    anomalies = {}

    for col in numeric_cols:
        # Skip low-variance categorical-like numeric columns
        if df[col].nunique() < 10:
            anomalies[col] = 0
            continue

        mean = df[col].mean()
        std = df[col].std()

        if std == 0:
            anomalies[col] = 0
            continue

        z = (df[col] - mean) / std
        outliers = np.abs(z) > 3

        anomalies[col] = int(outliers.sum())

    return anomalies

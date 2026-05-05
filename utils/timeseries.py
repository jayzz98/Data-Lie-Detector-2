import pandas as pd


def detect_timeseries_anomalies(df, date_col, value_col):
    """Detect time-series anomalies using rolling window statistics.

    Calculates a rolling mean and standard deviation over a 7-period
    window. Values exceeding 2 standard deviations from the rolling
    mean are flagged as anomalies.

    Args:
        df: A pandas DataFrame containing the data.
        date_col: Name of the column containing date/time values.
        value_col: Name of the numeric column to analyze.

    Returns:
        pd.DataFrame: The input DataFrame augmented with rolling_mean,
                       rolling_std, upper/lower bounds, and an anomaly flag.
    """
    df = df.copy()

    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])

    df = df.sort_values(date_col)

    df["rolling_mean"] = df[value_col].rolling(window=7).mean()
    df["rolling_std"] = df[value_col].rolling(window=7).std()

    df["upper"] = df["rolling_mean"] + 2 * df["rolling_std"]
    df["lower"] = df["rolling_mean"] - 2 * df["rolling_std"]

    df["anomaly"] = (df[value_col] > df["upper"]) | (df[value_col] < df["lower"])

    return df

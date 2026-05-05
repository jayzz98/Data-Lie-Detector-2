import pandas as pd


def auto_fix_data(df, profile, anomalies=None):
    """Automatically fix detected data quality issues.

    Applies fixes in priority order:
    1. Remove duplicate rows
    2. Fill missing numeric values with median
    3. Fill missing categorical values with mode
    4. Cap outliers at 3 standard deviations

    Args:
        df: The original pandas DataFrame.
        profile: The data profile dictionary.
        anomalies: Optional anomaly counts dictionary.

    Returns:
        tuple: (fixed_df, fix_log) — the cleaned DataFrame and a list
               of human-readable descriptions of changes made.
    """
    fixed = df.copy()
    log = []

    # 1. Remove duplicates
    if profile["duplicates"] > 0:
        before = len(fixed)
        fixed = fixed.drop_duplicates()
        removed = before - len(fixed)
        log.append(f"✅ Removed {removed} duplicate rows")

    # 2. Fill missing numeric values with median
    for col in profile["numeric_cols"]:
        missing_count = fixed[col].isnull().sum()
        if missing_count > 0:
            median_val = fixed[col].median()
            fixed[col] = fixed[col].fillna(median_val)
            log.append(f"✅ Filled {missing_count} missing values in '{col}' with median ({median_val:.2f})")

    # 3. Fill missing categorical values with mode
    for col in profile["categorical_cols"]:
        missing_count = fixed[col].isnull().sum()
        if missing_count > 0:
            mode_val = fixed[col].mode()
            if len(mode_val) > 0:
                fixed[col] = fixed[col].fillna(mode_val[0])
                log.append(f"✅ Filled {missing_count} missing values in '{col}' with mode ('{mode_val[0]}')")
            else:
                fixed[col] = fixed[col].fillna("UNKNOWN")
                log.append(f"✅ Filled {missing_count} missing values in '{col}' with 'UNKNOWN'")

    # 4. Cap outliers at 3 standard deviations
    if anomalies:
        for col, count in anomalies.items():
            if count > 0 and col in fixed.columns:
                mean = fixed[col].mean()
                std = fixed[col].std()
                if std > 0:
                    lower = mean - 3 * std
                    upper = mean + 3 * std
                    capped = ((fixed[col] < lower) | (fixed[col] > upper)).sum()
                    fixed[col] = fixed[col].clip(lower=lower, upper=upper)
                    if capped > 0:
                        log.append(f"✅ Capped {capped} outliers in '{col}' to [{lower:.2f}, {upper:.2f}]")

    if not log:
        log.append("✅ No fixes needed — data is already clean")

    return fixed, log

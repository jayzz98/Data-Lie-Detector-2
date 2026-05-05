def profile_data(df):
    """Profile a DataFrame to extract structural and quality metadata.

    Analyzes the DataFrame to determine its shape, column types,
    missing value percentages, and duplicate row count.

    Args:
        df: A pandas DataFrame to profile.

    Returns:
        dict: A dictionary containing:
            - rows (int): Number of rows.
            - cols (int): Number of columns.
            - numeric_cols (list): Names of numeric columns.
            - categorical_cols (list): Names of categorical/object columns.
            - missing (dict): Percentage of missing values per column.
            - duplicates (int): Count of duplicate rows.
    """
    profile = {}

    profile["rows"], profile["cols"] = df.shape

    profile["numeric_cols"] = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    profile["categorical_cols"] = df.select_dtypes(include=['object']).columns.tolist()

    profile["missing"] = (df.isnull().mean() * 100).to_dict()
    profile["duplicates"] = df.duplicated().sum()

    return profile

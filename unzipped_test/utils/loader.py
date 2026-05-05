import pandas as pd


def load_file(file):
    """Load a CSV file and return a DataFrame.

    Attempts to read the uploaded file using latin1 encoding
    to handle a wide range of character sets.

    Args:
        file: A file-like object (e.g., from Streamlit's file_uploader).

    Returns:
        pd.DataFrame or None: The loaded DataFrame, or None if loading fails.
    """
    try:
        return pd.read_csv(file, encoding='latin1')
    except Exception:
        return None

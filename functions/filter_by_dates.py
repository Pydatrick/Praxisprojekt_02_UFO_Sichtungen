import pandas as pd

def filter_by_interval(df:pd.DataFrame, start_date:str = None, end_date:str = None) ->pd.DataFrame:
    """Sortiert und gibt einen Ufo-DataFrame in einem Datetime-Intervall zurück.
    start_date, end_date im ISO-Format yyyy-mm-dd."""

    df["date_only"] = pd.to_datetime(df["datetime"]).dt.date  # YYYY-MM-DD ist default

    date1 = pd.to_datetime(start_date).date() if start_date else df["date_only"].min()
    date2 = pd.to_datetime(end_date).date() if end_date else df["date_only"].max()

    filtered_df = df[(df["date_only"] >= date1) & (df["date_only"] <= date2)]
    filtered_df = filtered_df.sort_values(by="datetime")

    return filtered_df

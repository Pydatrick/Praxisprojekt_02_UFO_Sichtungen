import pandas as pd

def load_ufo_df(path:str):
    """Lädt die Ufo CSV in ein Pandas DataFrame und stellt die Datetime Spalten als Datetime-Objekte zu Verfügung."""

    df = pd.read_csv(path)
    df["datetime"]    = pd.to_datetime(df["datetime"])
    df["date_posted"] = pd.to_datetime(df["date_posted"])
    return df


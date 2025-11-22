import pandas as pd
import numpy as np


# Zeile datetime in Datetime-Format umwandeln
def clean_datetime_column(df, datetime_column="datetime"):
    datetime_clean = pd.to_datetime(df[datetime_column], format="mixed", errors="coerce")
    return datetime_clean



# Jahreszeiten filtern
def get_season(month):
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "sommer"
    else:
        return "autumn"
    

# Tageszeit filtern  
def kategorisiere_tageszeit(df, datetime_column):
   
    # zieht die Stunden
    hour = df[datetime_column].dt.hour

    # Bedingungen für die Tageszeit-Kategorisierung
    conditions = [
        (hour >= 6) & (hour < 12),   # Vormittag (Tag)
        (hour >= 12) & (hour < 14),  # Mittag
        (hour >= 14) & (hour < 18),  # Nachmittag (Tag)
        (hour >= 18) | (hour < 6)    # Nacht
    ]

    # Labels für die Kategorien
    labels = ["Vormittag", "Mittag", "Nachmittag", "Nacht"]

    # Fügt Spalte 'zeitkategorie' zum DataFrame hinzu
    df["zeitkategorie"] = np.select(conditions, labels, default="Unbekannt")

    return df
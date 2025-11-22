import pandas as pd
import os
import sys
import html

print("data_cleanup gestartet")

ROOT_DIR = sys.argv[1]

path_to_data_raw = os.path.join(ROOT_DIR, "data", "data_raw", "ufo_sightings_scrubbed.csv")

ufo_df = pd.read_csv(path_to_data_raw, dtype = str)
print("Schmutzige CSV-Datei hat dtypes:")
print(ufo_df.dtypes)

# Spaltennamen ohne Leerzeichen:
ufo_df.columns = ['datetime', 'city', 'state', 'country', 'shape', 'duration_seconds',            # einige spalten hatten leerzeichen und andere "unsichtbare" zeichen
       'duration_hour_min', 'comments', 'date_posted', 'latitude',
       'longitude']
print(f"Spaltennamen geändert zu {ufo_df.columns}")

# Spalte duration_seconds bereinigen und von string nach numeric wandeln:
ufo_df["duration_seconds"] = ufo_df["duration_seconds"].str.replace(r"\D", "", regex = True) # nicht Zahlen entfernen . z.b. '2´'
ufo_df["duration_seconds"] = pd.to_numeric(ufo_df["duration_seconds"])      # HIER GEHEN ZAHLEN VERLOREN AB ZEILE 65535, wenn die csv oben nicht als dtype str eingelesen wurde
ufo_df["duration_seconds"].dtype
print(f"Spalte 'duration_seconds' bereinigt.")

# Spalte latitude und longitude bereinigen:
ufo_df["latitude"]  = ufo_df["latitude"].str.replace(r"[^\d.-]", "", regex = True)
ufo_df["latitude"]  = pd.to_numeric(ufo_df["latitude"])              # HIER GEHEN ZAHLEN VERLOREN AB ZEILE 65535, wenn die csv oben nicht als dtype str eingelesen wurde
ufo_df["longitude"] = pd.to_numeric(ufo_df["longitude"])
print(f"Spalten 'latitude' und 'longitude' bereinigt.")

# Spalte commments bereinigen. Sehr viele html codes im Text:
nan_count = ufo_df["comments"].isna().sum()
ufo_df["comments"] = ufo_df["comments"].fillna("")
print(f"{nan_count} NaN-Werte in Spalte 'comments' durch leeren String ersetzt.")

ufo_df["comments"] = ufo_df["comments"].apply(html.unescape)
print("Spalte 'comments' von html code befreit.")

# Die beiden Spalten mit Datums hatten keine Probleme

# Abspeichern als neue csv in data\data_clean
path_to_data_clean = os.path.join(ROOT_DIR, "data", "data_clean", "ufo_sightings_scrubbed_clean.csv")

ufo_df.to_csv(path_to_data_clean, index=False)
print(f"Bereinigte CSV-Datei erstellt: {path_to_data_clean}")

ufo_clean_df = pd.read_csv(path_to_data_clean)
print("Bereinigte CSV-Datei hat dtypes:")
print(ufo_clean_df.dtypes)

print("data_cleanup beendet")
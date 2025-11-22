import pandas as pd
import os
import sys

folder = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(folder, "..")
sys.path.append(ROOT_DIR)

from functions import haversine

def filter_sightings_by_radius(df:pd.DataFrame, lat:float, lon:float, radius_km:int) ->pd.DataFrame:
    """
    Filtert UFO-Sichtungen innerhalb eines bestimmten Radius um eine gegebene Koordinate.
    """
    # Falls die Koordinaten von Area 51 nicht gefunden wurden, stoppen wir hier
    if lat is None or lon is None:
        print("Area 51-Koordinaten sind nicht verfügbar. Keine Sichtungen gefiltert.")
        return pd.DataFrame()

    df["distance_km"] = df.apply(lambda row: haversine.distance(lat, lon, row["latitude"], row["longitude"]), axis=1)
    filtered_df = df[df["distance_km"] <= radius_km]

    print(f"Anzahl der Sichtungen im Umkreis von {radius_km} km um ({lat}, {lon}): {len(filtered_df)}")
    return filtered_df
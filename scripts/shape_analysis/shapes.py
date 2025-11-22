# Importe
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import geopandas as gpd
from shapely.geometry import Point
import sys

ROOT_DIR = sys.argv[1]
sys.path.append(ROOT_DIR)

from functions import ufo_df_loader

##### DATENSATZ-ZIEHEN #####
ufo_path = os.path.join(ROOT_DIR, "data", "data_clean", "ufo_sightings_scrubbed_clean.csv") # ufodaten laden
ufo_df = ufo_df_loader.load_ufo_df(ufo_path)
################################################################################################################
# Grafiken-Ordner festlegen
grafiken_ordner = os.path.join(ROOT_DIR, "data", "data_visualisation", "shape_analysis")
################################################################################################################

## Sichtungsdauer je Form ####

# Vorbereitung
# Spalte "Shape" in Strings formatieren 

shape_string = ufo_df.iloc[:, 5].astype("string")

# Gruppierung der Sichtungsform und Berechnung der durchschn. Dauer
average_duration = ufo_df.groupby("shape")["duration_seconds"].mean().reset_index()

# Sortierung nach duration_seconds
average_duration_sorted = average_duration.sort_values(by="duration_seconds", ascending=False)

# Plot erstellen -- Durchschnittliche Dauer von UFO-Sichtungen nach Form
average_duration_sorted.plot(
    kind= "bar",        # Diagrammtyp
    figsize= (10, 6),     # Größe des Diagrammes festlegen
    x= "shape",             # x-Achse
    y= "duration_seconds"
)

# Grafik

plt.title("Durchschnittliche Dauer von UFO-Sichtungen nach Form", fontsize=16, fontweight='bold')  # Titel anpassen
plt.xlabel("Sichtungsform", fontsize=14)               # x-Achsen-Beschriftung anpassen
plt.ylabel("Dauer in Sekunden", fontsize=14)  # y-Achsen-Beschriftung anpassen
plt.xticks(rotation=45)                         # Drehen der Beschriftung
plt.tight_layout()                              # Optimiert das Layout
plt.grid(axis='y', linestyle='--', alpha=0.7)   # Gitterlinien für die y-Achse
plt.gca().xaxis.grid(False)                     # Deaktiviert Gitternetzlinien auf der x-Achse


# Diagramm speichern
plt.savefig(os.path.join(grafiken_ordner, "shapes_per_second.png"))

################################################################################################################

# Dauer der Sichtung je Form in Summe #

# Aggregiere die Dauer in Sekunden je Form
duration_by_shape = ufo_df.groupby('shape')['duration_seconds'].sum().reset_index()

# Sortierung nach duration_seconds
average_duration_sorted_sum = duration_by_shape.sort_values(by="duration_seconds", ascending=False)

average_duration_sorted_sum

duration_by_shape = pd.DataFrame(duration_by_shape)

# Balkendiagramm erstellen
plt.figure(figsize=(12, 8))
sns.barplot(data=duration_by_shape, x='shape', y='duration_seconds', palette='viridis')

# Diagrammtitel und Achsenbeschriftungen
plt.title("Average Duration of UFO Sightings by Shape", fontsize=16)
plt.xlabel("Shapes", fontsize=14)
plt.ylabel("Duration in Seconds", fontsize=14)

# Achsenanpassungen
plt.xticks(rotation=45)
plt.tight_layout()

# Diagramm anzeigen
plt.savefig(os.path.join(grafiken_ordner, "shape_by_duration.png"))

################################################################################################################

# UFO-Datensatz in einen GeoDataFrame (gdf) umwandeln
ufo_df['geometry'] = ufo_df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1) # neue spalte erstellen, die long und lat kombiniert (gdf)
ufo_gdf = gpd.GeoDataFrame(ufo_df, geometry='geometry', crs="EPSG:4326") # df in gdf umwandeln
# Weltkarte laden
path_to_countries_shp = os.path.join(ROOT_DIR, "data", "shapes_from_natural_earth", "ne_10m_admin_0_countries", "ne_10m_admin_0_countries.shp")
world = gpd.read_file(path_to_countries_shp)
world = world.to_crs("EPSG:4326")  # gdf erstellen und mit Koordinatenreferenzsystem (CRS) verbinden (ist so :D)

# Räumliche Verknüpfung durchführen
joined_gdf = gpd.sjoin(ufo_gdf, world, how="left", predicate="within") # statt .apply von df/pandas

# Ländernamen extrahieren und dem ursprünglichen DataFrame hinzufügen
ufo_df['geo_country'] = joined_gdf['NAME']

# Ergebnis anzeigen
"""print(ufo_df.head())"""

################################################################################################################

# welche shapes in welchen ländern

# amerika ziehen

ufo_usa = ufo_df[ufo_df["geo_country"] == "United States of America"]

shape_per_country = ufo_usa.groupby('shape').size().reset_index(name='count')

shapes_usa = shape_per_country.sort_values("count", ascending=False).head(10)

"""print(shapes_usa)"""

#sortierung nach häufigkeit
# davon top 10 head(10)

# Grafik
plt.figure(figsize=(10, 6))  # Größe des Diagramms
sns.barplot(data=shape_per_country, x='count', y='shape', palette='viridis')
plt.title('Häufigste UFO-Formen in den USA', fontsize=16)
plt.xlabel('Anzahl der Sichtungen', fontsize=12)
plt.ylabel('UFO-Form', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(grafiken_ordner, "shapes_usa.png"))

#--------------


# Deutschland ziehen

ufo_germany = ufo_df[ufo_df["geo_country"] == "Germany"]

shape_per_country = ufo_germany.groupby('shape').size().reset_index(name='count')

shapes_germany = shape_per_country.sort_values("count", ascending=False).head(10)

"""print(shapes_germany)"""

# Grafik
plt.figure(figsize=(10, 6))  # Größe des Diagramms
sns.barplot(data=shapes_germany, x='count', y='shape', palette='viridis')
plt.title('Häufigste UFO-Formen in Deutschland', fontsize=16)
plt.xlabel('Anzahl der Sichtungen', fontsize=12)
plt.ylabel('UFO-Form', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(grafiken_ordner, "shapes_germany.png"))

################################################################################################################

# häufigste Shapes über die Jahre

#---------------------------
#lauras funktion -> kann später raus, wenn du funktikonen für alle gehen

# Zeile datetime in Datetime-Format umwandeln
def clean_datetime_column(df, datetime_column="datetime"):
    datetime_clean = pd.to_datetime(df[datetime_column], format="mixed", errors="coerce")
    return datetime_clean

#------------------------

#saubere datetime ziehen
ufo_df["datetime_clean"] = clean_datetime_column(ufo_df, "datetime")


#jahre ziehen (alle)
# shapes ziehen -> count davon 

# Jahr extrahieren
ufo_df["year"] = ufo_df["datetime_clean"].dt.year

# Gruppieren nach Jahr und Shape und zählen
shapes_per_year = ufo_df.groupby(["year", "shape"]).size().reset_index(name="count")

top_shapes = ufo_df["shape"].value_counts().head(10).index
shapes_per_year = ufo_df[ufo_df["shape"].isin(top_shapes)].groupby(["year", "shape"]).size().reset_index(name="count")

# Pivot-Tabelle erstellen, um Shapes über die Jahre zu vergleichen
pivot_table = shapes_per_year.pivot(index="year", columns="shape", values="count").fillna(0)

# Visualisierung
plt.figure(figsize=(12, 8))
for shape in top_shapes:
    subset = shapes_per_year[shapes_per_year["shape"] == shape]
    plt.plot(subset["year"], subset["count"], label=shape)

plt.title("Trends der UFO-Shapes über die Jahre")
plt.xlabel("Jahr")
plt.ylabel("Anzahl der Sichtungen")
plt.legend(title="Shape", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(grafiken_ordner, "shapes_jahre.png"))


#------------------------
# jahre ziehen ab 1990


# Jahr extrahieren
ufo_df["year"] = ufo_df["datetime_clean"].dt.year
close_up_df = ufo_df[ufo_df["year"] >= 1990]

# Gruppieren nach Jahr und Shape und zählen
shapes_per_year = close_up_df.groupby(["year", "shape"]).size().reset_index(name="count")

top_shapes = close_up_df["shape"].value_counts().head(10).index
shapes_per_year = close_up_df[close_up_df["shape"].isin(top_shapes)].groupby(["year", "shape"]).size().reset_index(name="count")

# Pivot-Tabelle erstellen, um Shapes über die Jahre zu vergleichen
pivot_table = shapes_per_year.pivot(index="year", columns="shape", values="count").fillna(0)

# Visualisierung
plt.figure(figsize=(12, 8))
for shape in top_shapes:
    subset = shapes_per_year[shapes_per_year["shape"] == shape]
    plt.plot(subset["year"], subset["count"], label=shape)

plt.title("Trends der UFO-Shapes ab 1990")
plt.xlabel("Jahr")
plt.ylabel("Anzahl der Sichtungen")
plt.legend(title="Shape", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(grafiken_ordner, "shapes_jahre_ab_1990.png"))

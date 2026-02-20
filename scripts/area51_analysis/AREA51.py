import pandas as pd
import os
import numpy as np
from geopy.geocoders import Nominatim
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import holidays
import ephem


ROOT_DIR = sys.argv[1]
sys.path.append(ROOT_DIR)
path_to_data_visualisation = os.path.join(ROOT_DIR, "data", "data_visualisation", "area51_analysis")
fig1 = os.path.join(ROOT_DIR, "data", "data_visualisation", "area51_analysis", "UFO_Tageszeit.png")
fig2 = os.path.join(ROOT_DIR, "data", "data_visualisation", "area51_analysis", "UFO_Sichtungen_in_Area_51_über_die_Jahre.png")
fig3 = os.path.join(ROOT_DIR, "data", "data_visualisation", "area51_analysis", "heatmap.png")
fig4 = os.path.join(ROOT_DIR, "data", "data_visualisation", "area51_analysis", "UFO_Mondphase")

from functions import ufo_df_loader
from functions import filter_sightings

# Lade die UFO-Daten
path_to_data_clean_read = os.path.join(ROOT_DIR, "data", "data_clean", "ufo_sightings_scrubbed_clean.csv")
df = ufo_df_loader.load_ufo_df(path_to_data_clean_read)

# Geokoordinaten für Area 51 ermitteln
geolokalisierer = Nominatim(user_agent="ufo_sightings_analysis")

try:
    standort = geolokalisierer.geocode("Area 51, Nevada, USA")
    if standort:
        area51_lat = standort.latitude
        area51_lon = standort.longitude
        print(f"Breitengrad: {area51_lat}, Längengrad: {area51_lon}")
    else:
        raise ValueError("Standort nicht gefunden.")
except Exception as e:
    print(f"Fehler bei der Geokodierung von Area 51: {e}")
    area51_lat, area51_lon = None, None

# Radius von 30 km um Area 51 festlegen
radius_km = 30  

# UFO-Sichtungen um Area 51 filtern
df_area51 = filter_sightings.filter_sightings_by_radius(df, area51_lat, area51_lon, radius_km)

# Sicherstellen, dass es gefilterte Daten gibt, bevor fortgefahren wird
if df_area51.empty:
    print("Keine UFO-Sichtungen in diesem Bereich gefunden.")
else:
    # Erste Zeilen der gefilterten Daten anzeigen
    print(df_area51[["datetime", "shape", "latitude", "longitude", "distance_km"]].head())

    # Dauer in Stunden umrechnen
    df_area51["duration_hour"] = df_area51["duration_seconds"] / 3600
    print(df_area51[["duration_seconds", "duration_hour"]].head())

    # Stelle sicher, dass datetime ein DateTime-Objekt ist
    df_area51["datetime"] = pd.to_datetime(df_area51["datetime"], errors="coerce")

    # Extrahiere die Stunde der Sichtung
    df_area51["hour"] = df_area51["datetime"].dt.hour

    # Weise die Tageszeit basierend auf der Sichtungsstunde zu
    df_area51["time_of_day"] = df_area51["hour"].apply(lambda x: "Tag" if 6 <= x < 18 else "Nacht")

    # Überprüfe das Ergebnis
    print(df_area51[["datetime", "duration_seconds", "time_of_day"]].head())

    # Zähle die Sichtungen für "Tag" und "Nacht"
    time_counts = df_area51["time_of_day"].value_counts()

    plt.figure(figsize=(6, 4))

    # Manuelle Reihenfolge: Erst "Tag", dann "Nacht"
    time_counts = time_counts.reindex(["Tag", "Nacht"])

    # Balkendiagramm 
    time_counts.plot(kind="bar", color=["orange", "darkblue"])

    # Achsenbeschriftungen und Titel 
    plt.xlabel("Tageszeit")
    plt.ylabel("Anzahl der Sichtungen")
    plt.title("UFO-Sichtungen nach Tageszeit in Area 51")

    # X-Achsen-Beschriftung waagerecht ausrichten
    plt.xticks(rotation=0)

    plt.savefig(fig1)
    # plt.show()

    # Wir holen uns aus datetime nur das Jahr
    df_area51["year"] = df_area51["datetime"].dt.year

    # Wir zählen, wie oft jedes Jahr eine Sichtung registriert wurde
    df_trend = df_area51.groupby("year").size().reset_index(name="count")

    plt.figure(figsize=(12, 6))
    plt.plot(df_trend["year"], df_trend["count"], marker="o", linestyle="-", color="blue")

    plt.xlabel("Jahr")
    plt.ylabel("Anzahl der Sichtungen")
    plt.title("UFO-Sichtungen in Area 51 über die Jahre")
    plt.grid(True)

    plt.savefig(fig2)
    # plt.show()

    # Hole das Jahr und die Stunde aus der datetime-Spalte
    df_area51["year"] = df_area51["datetime"].dt.year  # Holt das Jahr der Sichtung
    df_area51["hour"] = df_area51["datetime"].dt.hour  # Holt die Stunde der Sichtung (0-23)

    # Pivot-Tabelle erstellen, um die Sichtungshäufigkeit nach Jahr und Stunde darzustellen
    heatmap_data = df_area51.pivot_table(
        index="hour",  # Stunden als Zeilen (0 bis 23)
        columns="year",  # Jahre als Spalten
        aggfunc="size",  # Zählt die Anzahl der Sichtungen
        fill_value=0  # Falls keine Sichtungen existieren, trage eine 0 ein
    )

    # Heatmap
    plt.figure(figsize=(12, 6))  # Größe des Diagramms festlegen
    sns.heatmap(
        heatmap_data,  # Die erstellte Pivot-Tabelle als Datenquelle
        cmap="coolwarm",  # Farbskala: Blau für wenig, Rot für viele Sichtungen
        annot=False,  # Keine Werte direkt in die Zellen schreiben (kann auf True gesetzt werden)
        linewidths=0.5  # Feine Linien zwischen den Zellen für bessere Lesbarkeit
    )

    # Diagrammbeschriftung hinzufügen
    plt.xlabel("Jahr")  # X-Achsen-Beschriftung
    plt.ylabel("Stunde des Tages")  # Y-Achsen-Beschriftung
    plt.title("Heatmap der UFO-Sichtungen in Area 51 (Jahr vs. Stunde)")  # Titel der Heatmap

    plt.savefig(fig3)
    # plt.show()
    
#Mondphase pip install ephem
def calculate_moon_phase(date):
    """
    Berechnet die Mondphase für ein gegebenes Datum.
    0 = Neumond, 0.5 = Halbmond, 1 = Vollmond.
    """
    moon = ephem.Moon(date)
    return moon.phase / 29.5  # 0 bis 1 Skala
 # Mondzyklus, der etwa 29,5 Tage dauert


# Berechnung der Mondphase für jede UFO-Sichtung
df_area51["moon_phase"] = df_area51["datetime"].apply(lambda x: calculate_moon_phase(x) if pd.notnull(x) else None)

# Anzeige der ersten Zeilen mit Mondphasen
print(df_area51[["datetime", "moon_phase"]].head())

# Diagramm der Mondphasenverteilung
plt.figure(figsize=(8, 5))
sns.histplot(df_area51["moon_phase"], bins=10, kde=True, color="purple")
plt.xlabel("Mondphase (0 = Neumond, 1 = Vollmond)")
plt.ylabel("Anzahl der Sichtungen")
plt.title("Verteilung der UFO-Sichtungen nach Mondphase")
plt.grid(True)
plt.savefig(fig4)
#plt.show()

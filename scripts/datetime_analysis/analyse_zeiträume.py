#   DATENSATZ LADEN
import os
import sys
import pandas as pd #dataframes und datetime
import numpy as np #tageszeit berechnen
import matplotlib.pyplot as plt #basis-diagramme
import matplotlib.dates as mdates  # für Datumsformatierung in Zeitstrahl
import calendar # Monatsnummern in Monatsnamen umwandeln
import seaborn as sns #heatmap
import holidays #für feiertagsanalyse

if len(sys.argv) > 1:
    ROOT_DIR = sys.argv[1]
else:
    folder = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(folder, "..", ".."))

sys.path.append(ROOT_DIR)
path = os.path.join(ROOT_DIR, "data", "data_clean", "ufo_sightings_scrubbed_clean.csv")
ufo_sightings_df = pd.read_csv(path)


from functions import laura_functions

### Ordner für alle Grafiken
grafiken_ordner = os.path.join(ROOT_DIR, "data", "data_visualisation", "datetime_analysis")

################################################################################################################

#   SPALTE DATETIME BEREINIGEN

def clean_datetime_column(df, datetime_column="datetime"):
    datetime_clean = pd.to_datetime(df[datetime_column], format="mixed", errors="coerce")
    return datetime_clean

# format mixed -> alle angaben (mit und ohne sekunden) können verwendet werden
# errors coerce -> erstellt NaNs aus allen unpassenden daten

datetime_clean = clean_datetime_column(ufo_sightings_df)
################################################################################################################
#   JAHRE

# nach Jahren filtern
ufo_sightings_df["years"] = datetime_clean.dt.year
years_df = ufo_sightings_df["years"]

# Sichtungen pro Jahr
sightings_per_year = ufo_sightings_df.groupby("years").size()

# Grafik alle Jahre
sightings_per_year.plot(kind='line', figsize=(12, 6), marker='o', color='green', linestyle='-')
plt.title('UFO-Sichtungen über die Jahre')
plt.xlabel('Jahr')
plt.ylabel('Anzahl der Sichtungen')
plt.grid(True)  # Gitternetzlinien hinzufügen
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "jahre.png"))

# --------------------------

# ab 1990 filtern -- close up
close_up_df = ufo_sightings_df[ufo_sightings_df["years"] >= 1990]

# Sichtungen Close Up
sightings_close_up = close_up_df.groupby("years").size()

# Grafik Close Up

plt.figure(figsize=(14, 6)) 
plt.plot(sightings_close_up.index, sightings_close_up.values, marker='o', color='green', linestyle='-', label='Sichtungen pro Jahr')
plt.xticks(sightings_close_up.index, rotation=90) 
plt.title('UFO-Sichtungen ab 1990', fontsize=16)
plt.xlabel('Jahr', fontsize=14)
plt.ylabel('Anzahl der Sichtungen', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "jahre_close_up.png"))

################################################################################################################

#   MONATE

# nach Monaten filtern
ufo_sightings_df["months"] = datetime_clean.dt.month
months_df = ufo_sightings_df["months"]

# Sichtungen pro Monat
sightings_per_month =  ufo_sightings_df.groupby("months").size()

# Grafik 
sightings_per_month.index = sightings_per_month.index.map(lambda x: calendar.month_abbr[x]) # Monatsnummern in Monatsnamen umwandeln

plt.figure(figsize=(10, 6))
sns.barplot(x=sightings_per_month.index, y=sightings_per_month.values, palette="viridis")
plt.title('UFO-Sichtungen pro Monat')
plt.xlabel('Monat')
plt.ylabel('Anzahl der Sichtungen')
plt.xticks(rotation=45)
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "monate.png"))

################################################################################################################

#   JAHRESZEITEN

# Funktion zur Bestimmung der Jahreszeit
def get_season(month):
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"  
    
# Sortierung
seasons_sorted = ["spring", "summer", "autumn", "winter"]

# Monat extrahieren und Jahreszeit zuweisen
ufo_sightings_df["season"] = ufo_sightings_df["months"].map(get_season)
seasons_df = ufo_sightings_df["season"]

# Erstelle eine kategorische Spalte mit der gewünschten Sortierung
ufo_sightings_df["season"] = pd.Categorical(ufo_sightings_df["season"], categories=seasons_sorted, ordered=True)

# Sichtungen pro Jahreszeit 
sightings_per_season = ufo_sightings_df.groupby("season").size().reset_index(name="sightings")

# Grafik Jahreszeit
plt.figure(figsize=(10, 6))  # Größe des Diagramms anpassen
sns.barplot(x='season', y='sightings', data=sightings_per_season, palette="viridis")

plt.title('UFO-Sichtungen pro Saison', fontsize=16)
plt.xlabel('Saison', fontsize=14)
plt.ylabel('Anzahl der Sichtungen', fontsize=14)

# Werte über den Balken anzeigen
for i, value in enumerate(sightings_per_season['sightings']):
    plt.text(i, value + 0.1, str(value), ha='center', va='bottom', fontsize=12)

plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "jahreszeiten.png"))

################################################################################################################

#   TAGE (Datum)

# nach Tagen filtern
ufo_sightings_df["days"] = datetime_clean.dt.day

# Sichtungen pro Tag
sightings_per_day = ufo_sightings_df.groupby("days").size()

# Tag mit den meisten Sichtungen ziehen
most_sightings_day = sightings_per_day.idxmax()
most_sightings_count = sightings_per_day.max()

# Grafik Tage

plt.figure(figsize=(10, 6))
sns.barplot(x=sightings_per_day.index, y=sightings_per_day.values, palette="viridis")
plt.title('UFO-Sichtungen pro Tag des Monats', fontsize=16)
plt.xlabel('Tag des Monats', fontsize=14)
plt.ylabel('Anzahl der Sichtungen', fontsize=14)
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "tage_datum.png"))

################################################################################################################

#   TAGE (Wochentag)

# nach Wochentag filtern
ufo_sightings_df["weekday"] = datetime_clean.dt.weekday

# Tage benennen zur Übersicht
weekday_names = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
ufo_sightings_df["weekday_name"] = ufo_sightings_df["weekday"].map(lambda x: weekday_names[x])


# Sichtung Wochentag
sightings_per_weekday = ufo_sightings_df.groupby("weekday_name").size()

# Sortierung der Wochentage
sightings_per_weekday = sightings_per_weekday.reindex(weekday_names)

# Grafik Wochentag

plt.figure(figsize=(10, 6))
sns.barplot(x=sightings_per_weekday.index, y=sightings_per_weekday.values, palette="viridis")

plt.title('UFO-Sichtungen pro Wochentag', fontsize=16)
plt.xlabel('Wochentag', fontsize=14)
plt.ylabel('Anzahl der Sichtungen', fontsize=14)

# Werte über den Balken anzeigen
for i, value in enumerate(sightings_per_weekday.values):
    plt.text(i, value + 0.1, str(value), ha='center', va='bottom', fontsize=12)

plt.xticks(rotation=45)
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "tage_wochentag.png"))

################################################################################################################

#   TAGESZEIT

# Stunden ziehen
hour = datetime_clean.dt.hour

# Tageszeit-Kategorisierung
conditions = [
    (hour >= 6) & (hour < 12),   # Vormittag (Tag)
    (hour >= 12) & (hour < 14),  # Mittag
    (hour >= 14) & (hour < 18),  # Nachmittag (Tag)
    (hour >= 18) | (hour < 6)    # Nacht
]

# Labels für die Kategorien
labels = ["Vormittag", "Mittag", "Nachmittag", "Nacht"]

# neue Spalte ins df
ufo_sightings_df["zeitkategorie"] = np.select(conditions, labels, default="Unbekannt")

'''kategorisierte_zeit.head() wäre dann mit implementierter def'''

# --------------------------

# nach Stunde und Wochentag filtern
ufo_sightings_df["hour"] = datetime_clean.dt.hour
ufo_sightings_df["weekday"] = datetime_clean.dt.day_name()  # Name des Wochentags

# Konvertiere die Wochentage in eine kategorische Spalte mit der gewünschten Reihenfolge
ufo_sightings_df["weekday"] = pd.Categorical(     # HAT NUR NAN, DESWEGEN KOMMEN DIE NULLEN
    ufo_sightings_df["weekday_name"], 
    categories=weekday_names, 
    ordered=True
)

# Pivot-Tabelle für Heatmap
heatmap_data = ufo_sightings_df.pivot_table(
    index="zeitkategorie",         
    columns="weekday",         # Kommentar Patrick : columns="weekday_name" könnte helfen 
    values="datetime",    # Werte für die Heatmap (z. B. Anzahl der Sichtungen)
    aggfunc="count",      # Anzahl der Sichtungen
    fill_value=0          # Fülle fehlende Werte mit 0
)

"""# zur übersicht hier nochmal wochentage benennen
weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
heatmap_data = heatmap_data[weekday_names]"""

# Grafik Tageszeiten
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap="viridis", annot=True, fmt="d", linewidths=0.5)
plt.title("UFO-Sichtungen nach Stunde und Wochentag", fontsize=16)
plt.xlabel("Wochentag", fontsize=14)
plt.ylabel("Stunde des Tages", fontsize=14)
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "tageszeit.png"))

################################################################################################################

# ZUSAMMENHANG TAG UND MONAT

# Nach Tag.Monat filtern
ufo_sightings_df["datetime"] = datetime_clean
ufo_sightings_df["datetime"] = ufo_sightings_df["datetime"].dt.date

# value_counts ziehen
date_counts = ufo_sightings_df["datetime"].value_counts()
top10_date_counts = date_counts.head(10)

# Grafik Tag.Monat
plt.figure(figsize=(10, 6))
sns.barplot(x=top10_date_counts.index, y=top10_date_counts.values, palette="viridis")
plt.title('Top 10 Datumsangaben mit den meisten UFO-Sichtungen', fontsize=16)
plt.xlabel('Datum', fontsize=14)
plt.ylabel('Anzahl der Sichtungen', fontsize=14)

#Werte über den Balken anzeigen
for i, value in enumerate(top10_date_counts.values):
    plt.text(i, value + 0.5, str(value), ha='center', va='bottom', fontsize=12)

plt.xticks(rotation=45)
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "tag_monat.png"))

################################################################################################################

#   ENTWICKLUNG MELDUNGEN PRO LAND

# nach Jahren filtern
"""ufo_sightings_df["years"] = datetime_clean.dt.year
years_df = ufo_sightings_df["years"]"""

# Sichtungen pro Jahr und Land
sightings_per_year_country = ufo_sightings_df.groupby(["years", "country"]).size().unstack()

# Grafik Jahr und Land

# Länder zur Leserlichkeit umbenannt
sightings_per_year_country = sightings_per_year_country.rename(columns={
    "au": "Australien",
    "ca": "Canada",
    "gb": "Großbrittanien",
    "de": "Deutschland",
    "us": "USA",
})

# Entwicklung der Meldungen pro Land
sightings_per_year_country.plot(kind='line', figsize=(12, 8), marker='o')
plt.title('Entwicklung der UFO-Meldungen pro Land über die Jahre', fontsize=16)
plt.xlabel('Jahr', fontsize=14)
plt.ylabel('Anzahl der Meldungen', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Land')
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "jahre_land.png"))

# --------------------------

# CLOSE UP

# ab 1990 filtern
close_up_df = ufo_sightings_df[ufo_sightings_df["years"] >= 1990]

# Jahre aus dem gefilterten df ziehen
sightings_close_up_country = close_up_df.groupby(["years", "country"]).size().unstack()

# Grafik Close Up

# Länder zur Leserlichkeit umbenannt
sightings_close_up_country = sightings_close_up_country.rename(columns={
    "au": "Australien",
    "ca": "Canada",
    "gb": "Großbrittanien",
    "de": "Deutschland",
    "us": "USA",
})

# Entwicklung der Meldungen pro Land
sightings_close_up_country.plot(kind='line', figsize=(12, 8), marker='o')
plt.title('Entwicklung der UFO-Meldungen pro Land seit 1990', fontsize=16)
plt.xlabel('Jahr', fontsize=14)
plt.ylabel('Anzahl der Meldungen', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Land')
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "jahre_land_close_up.png"))


################################################################################################################

#   UFO-SICHTUNGEN IM KONTEXT VON US-FEIERTAGEN

# Feiertage für die USA in Variable packen
us_holidays = holidays.US()

# nach USA filtern 
us_sightings = ufo_sightings_df[ufo_sightings_df["country"] == "us"]

# nach Datum filtern
us_sightings["datetime"] = datetime_clean # bereinigte Spalte nutzen
us_sightings["date"] = us_sightings["datetime"].dt.date #ohne Uhrzeit

# Zeitraum für die Feiertage ermitteln
min_date = us_sightings["date"].min()
max_date = us_sightings["date"].max()

# Feiertags-Objekt für USA auf Zeitraum anwenden
us_holidays = holidays.US(years=range(min_date.year, max_date.year + 1))

# Konvertiere die Feiertage in ein Set für schnellen Abgleich
us_holidays_set = set(us_holidays.keys())

# Feiertags-Spalten hinzufügen
us_sightings["is_holiday"] = us_sightings["date"].isin(us_holidays_set)
us_sightings["holiday_name"] = us_sightings["date"].apply(lambda x: us_holidays.get(x))

# Nur Feiertage
holiday_sightings = us_sightings[us_sightings["is_holiday"]]

# Anzahl der Sichtungen pro Feiertag zählen
holiday_counts = holiday_sightings["holiday_name"].value_counts()

# Grafik Feiertage

plt.figure(figsize=(10, 6))
sns.barplot(x=holiday_counts.index, y=holiday_counts.values, palette="viridis")

plt.title("UFO-Sichtungen an US-Feiertagen", fontsize=16)
plt.xlabel("Feiertag", fontsize=12)
plt.ylabel("Anzahl der Sichtungen", fontsize=12)
plt.xticks(rotation=45, ha="right")  # Feiertagsnamen drehen, um Lesbarkeit zu verbessern

plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "holidays.png"))

################################################################################################################

#   PERSEIDEN

# in dt umwandeln
ufo_sightings_df["datetime"] = datetime_clean


# filtern nach Monat und Tag
ufo_sightings_df["month"] = ufo_sightings_df["datetime"].dt.month
ufo_sightings_df["day"] = ufo_sightings_df["datetime"].dt.day

# Zeitraum 17. Juli bis 24. August ziehen
# Juli: Monat = 7, August: Monat = 8
perseiden_zeitraum = ufo_sightings_df[
    ((ufo_sightings_df["month"] == 7) & (ufo_sightings_df["day"] >= 17)) |  # Juli: ab dem 17.
    ((ufo_sightings_df["month"] == 8) & (ufo_sightings_df["day"] <= 24))    # August: bis zum 24.
]

# Grafik Perseiden

# Neue Spalte für dt-Format "tag.monat" 
perseiden_zeitraum["date_str"] = perseiden_zeitraum["datetime"].dt.strftime("%d.%m.")

# chronologisch sortieren
perseiden_zeitraum = perseiden_zeitraum.sort_values("datetime")

# Zählen der Sichtungen pro Datum
sightings_per_date = perseiden_zeitraum.groupby("date_str").size().reset_index(name="count")
#.reset_index(name="count")
#Serie, die durch .size() erzeugt wurde, wird zurück in einen DataFrame konvertiert
# Dabei wird die Spalte mit den gezählten Werten (Anzahl der Sichtungen) in eine neue Spalte namens "count" umgewandelt.

# Neue Spalte für die Sortierung basierend auf dem datetime-Objekt
sightings_per_date["sort_key"] = pd.to_datetime(sightings_per_date["date_str"], format="%d.%m.")

# Sortierung nach der neuen Sortierschlüsselspalte
sightings_per_date = sightings_per_date.sort_values("sort_key")

# Plot
plt.figure(figsize=(12, 6))
sns.lineplot(x="date_str", y="count", data=sightings_per_date, marker="o", color="green")
plt.title("UFO-Sichtungen im Perseiden-Zeitraum (17.07. – 24.08.)")
plt.xlabel("Datum")
plt.ylabel("Anzahl der Sichtungen")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "perseiden.png"))
from bs4 import BeautifulSoup
import os
import pandas as pd
import sys

print("scrape_launch_dates gestartet.")
# absoluter Pfad zum Root Verzeichnis:
ROOT_DIR = sys.argv[1]
                                # Root/data/data_raw/htm
path_to_htm = os.path.join(ROOT_DIR, "data", "data_raw", "htm")      # Ordner mit HTML-Dateien

all_dates = []

print("Scraping beginnt.")

for filename in os.listdir(path_to_htm):

    if filename.endswith(".htm"):                                                           # Für alle Dateien mit htm Endung

        with open(os.path.join(path_to_htm, filename), "r", encoding = "utf-8") as file:    # Öffnen der htm-Dateien
            soup       = BeautifulSoup(file, "lxml")                                        # lxml Parser schneller als html Parser
            date_cells = soup.find_all("td", class_ = "column-1")                           # Finde die gesuchten Einträge
            dates      = [cell.get_text(strip = True) for cell in date_cells]               # ggfs Bereinigung der Einträge
            all_dates.extend(dates)                                                         # Sammeln der Einträge

print("Scraping endet.")

launch_dates_df = pd.DataFrame(all_dates, columns=["launch_dates"])

launch_dates_clean_path = os.path.join(ROOT_DIR, "data", "data_clean", "cape_canaveral_launch_chronology.csv")
launch_dates_df.to_csv(launch_dates_clean_path, index=False)
print(f"Bereinigte CSV-Datei erstellt: {launch_dates_clean_path}")

print("scrape_launch_dates beendet.")
import subprocess
import os
import sys

ROOT_DIR = sys.argv[1]

# Starte data_cleanup.py
path_to_data_cleanup_script = os.path.join(ROOT_DIR, "scripts", "data_cleanup", "data_cleanup.py")
print("data_cleanup Skript startet.")
subprocess.run(["python", path_to_data_cleanup_script, ROOT_DIR])
print("data_cleanup Skript abgeschlossen.")

### Für die Demo deaktiviert ###
# # Starte scrape_launch_dates.py
# path_to_scrape_launch_dates = os.path.join(ROOT_DIR, "scripts", "data_cleanup", "scrape_launch_dates.py")
# print("scrape_launch_dates Skript startet.")
# subprocess.run(["python", path_to_scrape_launch_dates, ROOT_DIR])
# print("scrape_launch_dates Skript abgeschlossen.")

# Starte extract_comments.py
path_to_extract_comments = os.path.join(ROOT_DIR, "scripts", "comments_analysis", "extract_comments.py")
print("extract_comments Skript startet.")
subprocess.run(["python", path_to_extract_comments, ROOT_DIR])
print("extract_comments Skript abgeschlossen.")
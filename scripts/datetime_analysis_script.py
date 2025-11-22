import subprocess
import os
import sys

ROOT_DIR = sys.argv[1]

# Starte analyse_zeiträume.py
path_analyse_zeiträume = os.path.join(ROOT_DIR, "scripts", "datetime_analysis", "analyse_zeiträume.py")
print("analyse_zeiträume.py Skript startet.")
subprocess.run(["python", path_analyse_zeiträume, ROOT_DIR])
print("create_inanalyse_zeiträumeteractive_maps.py abgeschlossen.")
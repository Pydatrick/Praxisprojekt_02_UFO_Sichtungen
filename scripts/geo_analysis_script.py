import subprocess
import os
import sys

ROOT_DIR = sys.argv[1]

# Starte create_interactive_maps.py
path_create_interactive_maps = os.path.join(ROOT_DIR, "scripts", "geo_analysis", "create_interactive_maps.py")
print("create_interactive_maps.py Skript startet.")
subprocess.run(["python", path_create_interactive_maps, ROOT_DIR])
print("create_interactive_maps.py abgeschlossen.")
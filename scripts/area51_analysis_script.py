import subprocess
import os
import sys

ROOT_DIR = sys.argv[1]

# Starte create_interactive_maps.py
path_AREA51 = os.path.join(ROOT_DIR, "scripts", "area51_analysis", "AREA51.py")
print("AREA51.py Skript startet.")
subprocess.run(["python", path_AREA51, ROOT_DIR])
print("AREA51.py abgeschlossen.")
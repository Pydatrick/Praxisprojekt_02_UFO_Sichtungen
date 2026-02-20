import subprocess
import os
import sys

ROOT_DIR = sys.argv[1]

# Starte UFO_Theo_Final.py
path_to_UFO_Theo_Final = os.path.join(ROOT_DIR, "scripts", "duration_analysis", "UFO_Theo_Final.py")
print("UFO_Theo_Final.py Skript startet.")
subprocess.run(["python", path_to_UFO_Theo_Final, ROOT_DIR])
print("UFO_Theo_Final.py abgeschlossen.")
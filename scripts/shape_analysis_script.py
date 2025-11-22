import subprocess
import os
import sys

ROOT_DIR = sys.argv[1]

# Starte shapes.py
path_shapes = os.path.join(ROOT_DIR, "scripts", "shape_analysis", "shapes.py")
print("shapes.py Skript startet.")
subprocess.run(["python", path_shapes, ROOT_DIR])
print("shapes.py abgeschlossen.")

# # Starte duration_shape.py
# path_duration_shape = os.path.join(ROOT_DIR, "scripts", "shape_analysis", "duration_shape.py")
# print("duration_shape.py Skript startet.")
# subprocess.run(["python", path_duration_shape, ROOT_DIR])
# print("duration_shape.py abgeschlossen.")



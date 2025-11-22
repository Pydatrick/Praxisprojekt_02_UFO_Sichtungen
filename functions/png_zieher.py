import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt  # für die Darstellung aller Bilder in einem Panel

def erstelle_zusammenfassung(quell_ordner, ziel_ordner, ausgabe_dateiname="zusammenfassung.png"):
    # Alle Bilder in eine Liste (Suche nach ".png")
    grafiken_liste = [f for f in os.listdir(quell_ordner) if f.endswith('.png')]

    # Anzahl der Bilder berechnen
    anzahl_bilder = len(grafiken_liste)

    if anzahl_bilder == 0:
        print("⚠ Keine Bilder gefunden!")
        return

    # Rastergröße berechnen (ca. Quadrat zur Orientierung)
    spalten = int(np.ceil(np.sqrt(anzahl_bilder)))  # Aufrunden zur nächsten ganzen Zahl
    zeilen = int(np.ceil(anzahl_bilder / spalten))  # Berechne Zeilen basierend auf Spalten

    # Panel erstellen
    fig, axes = plt.subplots(zeilen, spalten, figsize=(20, 20))
    fig.suptitle("Zusammenfassung", fontsize=16)

    # Sicherstellen, dass axes ein 2D-Array ist
    axes = np.atleast_2d(axes)

    # Bilder in den Subplots anzeigen
    for i, datei in enumerate(grafiken_liste):
        # Bild laden
        bild_pfad = os.path.join(quell_ordner, datei)
        bild = Image.open(bild_pfad)

        # Subplot auswählen
        ax = axes[i // spalten, i % spalten]

        # Bild im Subplot anzeigen
        ax.imshow(bild)
        ax.axis('off')  # Achsen ausblenden

    # Leere Subplots ausblenden
    for i in range(anzahl_bilder, zeilen * spalten):
        axes[i // spalten, i % spalten].axis('off')

    # Layout anpassen und Grafik speichern
    plt.tight_layout()
    plt.savefig(os.path.join(ziel_ordner, ausgabe_dateiname))
    plt.close()  # Schließe das Figure-Objekt, um Speicher freizugeben



"""
# Beispielaufruf der Funktion
quell_ordner = os.path.join(os.path.dirname(__file__), 'grafiken')
ziel_ordner = os.path.join(os.path.dirname(__file__), 'zusammenfassungen')
erstelle_zusammenfassung(quell_ordner, ziel_ordner)

"""


#### ORIGINALCODE #####
"""
# Pfad zum Ordner "grafiken" relativ zum aktuellen Skript
grafiken_ordner = os.path.join(os.path.dirname(__file__), 'grafiken')

# alle Bilder in eine Liste (Suche nach ".png")
grafiken_liste= [f for f in os.listdir(grafiken_ordner) if f.endswith('.png')]

# Anzahl der Bilder berechnen
anzahl_bilder = len(grafiken_liste)

# Rastergröße berechnen (ca. Quadrat zur Orientierung)
spalten = int(anzahl_bilder**0.5)  # Wurzel aus der Anzahl der Bilder
zeilen = (anzahl_bilder // spalten) + (1 if anzahl_bilder % spalten != 0 else 0) #ganzzahlige Division + Rest

# Panel erstellen
fig, axes = plt.subplots(zeilen, spalten, figsize=(20, 20
))
fig.suptitle("Zusammenfassung", fontsize=16)

# Bilder in den Subplots anzeigen
for i, datei in enumerate(grafiken_liste):
    # Bild laden
    bild_pfad = os.path.join(grafiken_ordner, datei)
    bild = Image.open(bild_pfad)

    # Subplot auswählen
    ax = axes[i // spalten][i % spalten] if zeilen > 1 else axes[i % spalten]

    # Bild im Subplot anzeigen
    ax.imshow(bild)
    ax.axis('off')  # Achsen ausblenden

# Leere Subplots ausblenden
for i in range(anzahl_bilder, zeilen * spalten):
    ax = axes[i // spalten][i % spalten] if zeilen > 1 else axes[i % spalten]
    ax.axis('off')

# Layout anpassen und Grafik anzeigen
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(grafiken_ordner, "zusammenfassung"))"""
import numpy as np

def distance(lat1, lon1, lat2, lon2):
    """Berechnet die Orthodrome zwischen zwei Koordinaten im Format xxx.xxxxxxx.
    Sie ist die kürzeste Verbindung zweier Punkte auf einer Kugeloberfläche.
    'half the value of the versed sine' -> haversine"""

    R = 6371                                                            # mittlerer Erdradius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])  # Grad in Radiant umrechnen

    dlat = lat2 - lat1                                                  # Differenz der zwei Punkte
    dlon = lon2 - lon1                                                  # Differenz der zwei Punkte

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2     # haversine - Formel

    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))                                      # haversine - Formel    

    return R * c                                                        # Entfernung in Kilometern
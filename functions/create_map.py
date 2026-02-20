import folium
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
import pandas as pd
import os
from functions import filter_by_dates
from functions import haversine

def create_cluster_heat_map(df:pd.DataFrame,
                            filename:str, 
                            mapdir, 
                            start_date:str = None, 
                            end_date:str   = None,  
                            radius:int     = None, 
                            map_type:str   = "cluster"
                           ) -> None:
    """Erstellt eine Cluster Map mit map_type = "cluster",
    eine OPNV Map mit map_type ="opnv" 
    oder eine Heat Map mit map_type = "heat" mit Folium.
    Dabei kann optional ein Datetime Intervall und ein Radius um Cape Caneveral angegeben werden.
    Die fertige Map wird im Ordner 'mapdir' mit dem namen 'filename'.hmtl abgelegt"""

    # Zeitliches Interval:
    if start_date or end_date:
        df = filter_by_dates.filter_by_interval(df, start_date, end_date)

    # Radius:
    if radius:
        distances = haversine.distance(28.3922, -80.6077, df["latitude"], df["longitude"])  # Fixpunkt ist Cape Caneveral
        df = df[distances <= radius]

    center_lat = df["latitude"].mean()
    center_lon = df["longitude"].mean()

    map = folium.Map(location=[center_lat, center_lon], zoom_start = 5)             # Erzeuge Map mit Folium

    folium.Marker(location = [28.3922, -80.6077],                                   # Cape Canaveral Koordinaten
                  popup    = "🚀 Cape Canaveral Spaceport",
                  icon     = folium.Icon(color="red", icon="rocket", prefix="fa")   # Rotes Symbol mit Rakete
                 ).add_to(map)
    
    if map_type == "heat":                                                          # für Hitzkarte

            map_data = list(zip(df["latitude"], df["longitude"]))     
            HeatMap(map_data,
                    radius      = 12,           # Standard ist 10, größere Werte machen größere Flecken
                    blur        = 12,           # Standard ist 15, kleinere Werte machen schärfere Flecken
                    min_opacity = 0.5,          # Standard ist 0.2, höhere Werte machen schwache Punkte sichtbarer
                    gradient    = {'0':'Navy', '0.2':'Blue', '0.4':'Green', '0.6':'Yellow', '0.8':'Orange', '1':'Red'}
                   ).add_to(map)

    if map_type == "cluster" or map_type == "opnv":                                 # cluster map or cluster opnv map

        # JavaScript-Funktion zur Anpassung der Clusterfarben
        custom_cluster = """
        function(cluster) {
            var count = cluster.getChildCount();
            var color = count < 100 ? 'rgba(0, 200, 0, 0.7)' : 
                        count < 500 ? 'rgba(255, 200, 0, 0.8)' : 
                        count < 1000 ? 'rgba(255, 100, 0, 0.9)' : 
                        'rgba(200, 0, 0, 1)';

            return new L.DivIcon({
                html: '<div style="background-color:' + color + 
                    '; width: 35px; height: 35px; border-radius: 50%;' +
                    'display: flex; justify-content: center; align-items: center;' +
                    'font-size: 14px; font-weight: bold; color: white;">' + count + '</div>',
                className: 'custom-cluster',
                iconSize: [40, 40]
            });
        }
        """                             
        marker_cluster = MarkerCluster(icon_create_function = custom_cluster).add_to(map)       # Erstelle Cluster damit nicht 80000 Punkte einzelt auf der Map sind

        for lat, lon in zip(df["latitude"], df["longitude"]):
            folium.Marker([lat, lon]).add_to(marker_cluster)    

        if map_type == "opnv":

            folium.Marker(
                location = [37.2448, -115.8176], 
                popup    = "👽 Area 51 - Top Secret",
                icon     = folium.CustomIcon(icon_image = "https://www.svgrepo.com/show/41570/ufo.svg",     # UFO-Icon
                                             icon_size  = (80, 80)                                          # Größe anpassen 
                                            )     
                        ).add_to(map)
                                                                                            
            folium.TileLayer(tiles = "https://tile.memomaps.de/tilegen/{z}/{x}/{y}.png",       # Lädt andere Tiles mit Flughäfen und anderen ÖPNVs
                              attr  = "© OpenStreetMap-Mitwirkende, Memomaps",
                              name  = "ÖPNV-Karte"
                             ).add_to(map)
            folium.LayerControl().add_to(map)
    
    map_filename = f"{filename}.html"                                               # Filenamen zusammensetzen
    path_to_data_map = os.path.join(mapdir, map_filename)                           # wo soll die map gespeichert werden
    map.save(path_to_data_map)                                                      # Speichern der map mit map_filename
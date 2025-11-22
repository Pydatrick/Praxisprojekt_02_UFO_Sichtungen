import geopandas as gpd
from shapely.geometry import Point

def add_country_to_ufo_df(ufo_df, world_shapefile_path):
    """
    Fügt dem UFO-Datensatz eine Spalte mit dem Ländernamen hinzu, basierend auf den Koordinaten.

    :param ufo_df: Pandas DataFrame mit den Spalten 'latitude' und 'longitude'.
    :param world_shapefile_path: Pfad zur Shapefile-Datei der Weltkarte (Ländergrenzen).
    :return: Pandas DataFrame mit einer zusätzlichen Spalte 'geo_country'.
    """
    # UFO-Datensatz in einen GeoDataFrame (gdf) umwandeln
    ufo_df['geometry'] = ufo_df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)  # Neue Spalte erstellen, die long und lat kombiniert
    ufo_gdf = gpd.GeoDataFrame(ufo_df, geometry='geometry', crs="EPSG:4326")  # DataFrame in GeoDataFrame umwandeln

    # Weltkarte laden
    world = gpd.read_file(world_shapefile_path)  # Shapefile der Weltkarte laden
    world = world.to_crs("EPSG:4326")  # Koordinatenreferenzsystem (CRS) auf EPSG:4326 setzen

    # Räumliche Verknüpfung durchführen
    joined_gdf = gpd.sjoin(ufo_gdf, world, how="left", predicate="within")  # Räumliche Verknüpfung mit Ländergrenzen

    # Ländernamen extrahieren und dem ursprünglichen DataFrame hinzufügen
    ufo_df['geo_country'] = joined_gdf['NAME']

    # Ergebnis zurückgeben
    return ufo_df

"""# Beispielaufruf der Funktion
if __name__ == "__main__":
    # Pfad zur Shapefile-Datei der Weltkarte
    world_shapefile_path = r"C:\Users\Admin\Documents\Projekt_Ufo\Projekt_UFO\data\shapes_from_natural_earth\ne_10m_admin_0_countries\ne_10m_admin_0_countries.shp"

    # Beispiel-UFO-Datensatz (angenommen, ufo_df ist bereits geladen)
    # ufo_df = pd.read_csv("ufo_sightings.csv")  # Beispiel: Laden des UFO-Datensatzes

    # Funktion aufrufen
    ufo_df_with_countries = add_country_to_ufo_df(ufo_df, world_shapefile_path)

    # Ergebnis anzeigen
    print(ufo_df_with_countries.head())"""
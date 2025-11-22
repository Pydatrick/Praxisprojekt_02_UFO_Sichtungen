import os
import sys


if len(sys.argv) > 1:
    ROOT_DIR = sys.argv[1]
else:
    folder = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(folder, "..", ".."))
sys.path.append(ROOT_DIR)

from functions import create_map
from functions import ufo_df_loader

path_to_data_map = os.path.join(ROOT_DIR, "data", "data_map")
path_to_data_clean_read = os.path.join(ROOT_DIR, "data", "data_clean", "ufo_sightings_scrubbed_clean.csv")

ufo_df = ufo_df_loader.load_ufo_df(path_to_data_clean_read)

# All 11. Nov 1908 - 08. May 2014 Cluster
create_map.create_cluster_heat_map(ufo_df, 
                                   filename   = "all_1908-2014_Cluster", 
                                   mapdir     = path_to_data_map, 
                                  )

# All 11. Nov 1908 - 08. May 2014 Heat
create_map.create_cluster_heat_map(ufo_df, 
                                   filename   = "all_1908-2014_Heat", 
                                   mapdir     = path_to_data_map,
                                   map_type   = "heat" 
                                  )

# Leoniden 16./17. Nov 1999 Cluster Map
create_map.create_cluster_heat_map(ufo_df, 
                                   filename   = "Leoniden_1617_11_1999_Cluster", 
                                   mapdir     = path_to_data_map, 
                                   start_date = "1999-11-16", 
                                   end_date   = "1999-11-17", 
                                   map_type   = "cluster"
                                  )

# Leoniden 16./17. Nov 1999 Heat Map
create_map.create_cluster_heat_map(ufo_df, 
                                   filename   = "Leoniden_1617_11_1999_Heat", 
                                   mapdir     = path_to_data_map, 
                                   start_date = "1999-11-16", 
                                   end_date   = "1999-11-17", 
                                   map_type   = "heat"
                                  )

# Independence Day 04. Jul 2010
create_map.create_cluster_heat_map(ufo_df, 
                                   filename   = "Independence_Day_04_07_2010_Cluster", 
                                   mapdir     = path_to_data_map, 
                                   start_date = "2010-07-04", 
                                   end_date   = "2010-07-04", 
                                   map_type   = "cluster"
                                  )

# Perseiden 17. Jul - 24. Aug 2010 Cluster Map
create_map.create_cluster_heat_map(ufo_df, 
                                   filename   = "Perseiden_1707-2408_2010_Cluster", 
                                   mapdir     = path_to_data_map, 
                                   start_date = "2010-07-17", 
                                   end_date   = "2010-08-24", 
                                   map_type   = "cluster"
                                  )

# Perseiden 17. Jul - 24. Aug 2010 Heat Map
create_map.create_cluster_heat_map(ufo_df, 
                                   filename   = "Perseiden_1707-2408_2010_Heat", 
                                   mapdir     = path_to_data_map, 
                                   start_date = "2010-07-17", 
                                   end_date   = "2010-08-24", 
                                   map_type   = "heat"
                                  )
# Area 51 OPNV Map
create_map.create_cluster_heat_map(ufo_df, 
                                   filename   = "Area51_OPNV", 
                                   mapdir     = path_to_data_map,
                                   map_type   = "opnv",
                                   radius     = 2000
                                  )
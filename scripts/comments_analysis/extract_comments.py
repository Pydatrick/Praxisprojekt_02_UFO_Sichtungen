import pandas as pd
import os
import sys

print("extract_comments gestartet.")

ROOT_DIR = sys.argv[1]

path_to_data_clean_read = os.path.join(ROOT_DIR, "data", "data_clean", "ufo_sightings_scrubbed_clean.csv")

ufo_df = pd.read_csv(path_to_data_clean_read)

print("Auslesen aller Wörter und deren Häufigkeiten.")
#words               = ufo_df["comments"].str.findall(r"\b\w+\b")                # mit Zahlen
words               = ufo_df["comments"].str.findall(r"\b[a-zA-Z]+\b")   # ohne Zahlen 
word_series         = pd.Series(words.explode(), name = "words")
word_counts         = word_series.value_counts().reset_index()
word_counts.columns = ["word", "count"]

path_to_data_clean_write = os.path.join(ROOT_DIR, "data", "data_clean", "word_count.csv")
word_counts.to_csv(path_to_data_clean_write,index=False)
print(f"Wörter und Häufigkeiten als CSV-Datei erstellt: {path_to_data_clean_write}")

print("extract_comments beendet.")

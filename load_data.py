import csv
from typing import List, Any


def load_csv_data(filepaths: List[str]) -> List[List[Any]]:
    """
    Lädt Daten aus einer oder mehreren CSV-Dateien in ein Array von Arrays.

    Args:
        filepaths: Eine Liste mit Pfaden zu CSV-Dateien

    Returns:
        Eine Liste, wobei jedes Element eine Zeile aus der CSV-Datei repräsentiert
    """
    all_data = []

    for filepath in filepaths:
        with open(filepath, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            # Überspringe die Header-Zeile
            next(csv_reader, None)

            # Füge jede Zeile zum Ergebnis hinzu
            for row in csv_reader:
                all_data.append(row)

    return all_data

# Example usage:
if __name__ == "__main__":
    # Specify the paths to your CSV files
    filepaths = ["cosmetic_archive/2019-Oct.csv", "cosmetic_archive/2019-Nov.csv"]
    data = load_csv_data(filepaths)

    # Print the first few elements of the loaded data
    for i in range(min(10, len(data))):
        print(data[i])
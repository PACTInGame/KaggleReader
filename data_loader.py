import csv
from typing import List, Any


class DataLoader:
    """Lädt Daten aus CSV-Dateien"""

    @staticmethod
    def load_csv_data(filepaths: List[str]) -> List[List[Any]]:
        """
        Lädt Daten aus einer oder mehreren CSV-Dateien

        Args:
            filepaths: Liste von CSV-Dateipfaden

        Returns:
            Liste von Datenzeilen
        """
        all_data = []

        for filepath in filepaths:
            with open(filepath, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                # Überspringe Header
                next(csv_reader, None)

                for row in csv_reader:
                    all_data.append(row)

        return all_data
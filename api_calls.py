import time
from typing import List, Any, Dict, Optional
import re
from datetime import datetime

import requests


def send_data_to_api(data: List[List[Any]]) -> None:
    """
    Sendet Daten an eine API, basierend auf dem Event-Typ.

    Args:
        data: Eine Liste von Zeilen aus der CSV-Datei
    """
    api_endpoints = {
        "view": "http://localhost:8080/view",
        "cart": "http://localhost:8080/cart",
        "remove_from_cart": "http://localhost:8080/remove_from_cart",
        "purchase": "http://localhost:8080/purchase"
    }

    for row in data:
        # Überprüfe, ob der Event-Typ (Index 1) existiert und einer der relevanten Typen ist
        if len(row) > 1 and row[1] and row[1] in api_endpoints:
            event_type = row[1]
            endpoint = api_endpoints[event_type]

            # Erstelle ein Payload-Dictionary für die API
            payload = {
                # "event_time": row[0],
                # "event_type": row[1],
                "product_id": row[2],
                "category_id": row[3],
                "category_code": row[4],
                "brand": row[5],
                "price": row[6],
                "user_id": row[7],
                "user_session": row[8] if len(row) > 8 else None
            }

            try:
                # Sende die Daten an den entsprechenden API-Endpunkt
                print(f"Sending {event_type} event to {endpoint}")
                response = requests.post(endpoint, json=payload)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error sending data to API: {e}")


def replay_events(data: List[List[Any]], speed_factor: float = 1.0) -> None:
    """
    Spielt die Events aus den CSV-Daten in zeitlicher Abfolge ab.

    Args:
        data: Eine Liste von Zeilen aus der CSV-Datei
        speed_factor: Faktor, mit dem die Replay-Geschwindigkeit angepasst wird (default: 1.0)
                     Ein Wert von 2.0 würde die Events doppelt so schnell abspielen.
    """
    # Sortiere die Daten nach dem Zeitstempel (falls sie nicht bereits sortiert sind)
    sorted_data = sorted(data, key=lambda x: x[0] if x[0] else "")

    # Speichere die Startzeit des ersten Events
    first_event_time = None
    start_replay_time = time.time()

    for row in sorted_data:
        # Ignoriere Datensätze mit leerem event_type (Index 1)
        if len(row) <= 1 or not row[1]:
            continue

        try:
            # Verarbeite verschiedene Zeitstempelformate
            timestamp_str = row[0]

            # Prüfe, ob der Zeitstempel im Format '2019-10-06 19:42:21 UTC' ist
            if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC', timestamp_str):
                # Konvertiere in ein Format, das datetime verstehen kann
                timestamp_str = timestamp_str.replace(' UTC', '')
                current_event_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            else:
                # Versuche ISO-Format
                current_event_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

            # Wenn dies das erste gültige Event ist, setze first_event_time
            if first_event_time is None:
                first_event_time = current_event_time
                print(f"Starting replay at {current_event_time}")
            else:
                # Berechne die Zeitdifferenz zum ersten Event
                time_diff = (current_event_time - first_event_time).total_seconds()

                # Berechne, wie viel Zeit seit Beginn des Replays vergangen sein sollte
                elapsed_target = time_diff / speed_factor

                # Berechne, wie viel Zeit tatsächlich vergangen ist
                elapsed_actual = time.time() - start_replay_time

                # Warte, falls notwendig
                if elapsed_target > elapsed_actual:
                    time.sleep(elapsed_target - elapsed_actual)


            event_type = row[1]
            print(f"Replaying {event_type} event at {current_event_time}")
            send_single_event_to_api(row)

        except Exception as e:
            print(f"Error processing event: {e} for timestamp: {row[0]}")
            continue


def send_single_event_to_api(row: List[Any]) -> None:
    """
    Sendet ein einzelnes Event an die API.

    Args:
        row: Eine Zeile aus der CSV-Datei
    """
    api_endpoints = {
        "view": "http://localhost:8080/view",
        "cart": "http://localhost:8080/cart",
        "remove_from_cart": "http://localhost:8080/remove_from_cart",
        "purchase": "http://localhost:8080/purchase"
    }

    if len(row) > 1 and row[1] and row[1] in api_endpoints:
        event_type = row[1]
        endpoint = api_endpoints[event_type]

        payload = {
            # "event_time": row[0],
            # "event_type": row[1],
            "product_id": row[2],
            "category_id": row[3],
            "category_code": row[4],
            "brand": row[5],
            "price": row[6],
            "user_id": row[7],
            "user_session": row[8] if len(row) > 8 else None
        }

        try:
            print(f"Sending {event_type} event to {endpoint}")
            print(payload)
            response = requests.post(endpoint, json=payload)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error sending data to API: {e}")
import time
import re
from datetime import datetime
from typing import List, Any, Optional
from api_client import APIClient
from performance_tracker import PerformanceTracker
from statistics_generator import StatisticsGenerator


class EventSender:
    """Orchestriert die verschiedenen Modi zum Senden von Events"""

    def __init__(self):
        self.api_client = APIClient()
        self.performance_tracker = PerformanceTracker()
        self.statistics_generator = StatisticsGenerator()

    def send_all_fast(self, data: List[List[Any]], show_statistics: bool = True) -> None:
        """
        Sendet alle Daten so schnell wie möglich mit Performance-Tracking

        Args:
            data: CSV-Daten
            show_statistics: Ob Statistiken angezeigt werden sollen
        """
        print("Sending all data as fast as possible...")
        self.performance_tracker.clear()

        start_time = time.perf_counter()

        for row in data:
            result = self.api_client.send_single_request(row, track_performance=True)
            if result:
                self.performance_tracker.add_result(result)

        end_time = time.perf_counter()
        total_time = end_time - start_time

        print(f"Completed sending all data in {total_time:.2f} seconds")

        if show_statistics:
            stats = self.performance_tracker.get_statistics()
            self.statistics_generator.print_statistics(stats)
            self.statistics_generator.generate_plots(self.performance_tracker, stats)

    def send_single_event(self, row: List[Any]) -> None:
        """
        Sendet ein einzelnes Event (ohne Performance-Tracking)

        Args:
            row: Einzelne Datenzeile
        """
        print("Sending single event...")
        self.api_client.send_single_request(row, track_performance=False)

    def replay_events(self, data: List[List[Any]], speed_factor: float = 1.0) -> None:
        """
        Spielt Events in zeitlicher Abfolge ab (ohne Performance-Tracking)

        Args:
            data: CSV-Daten
            speed_factor: Geschwindigkeitsfaktor für Replay
        """
        print(f"Replaying events with speed factor {speed_factor}...")

        # Sortiere die Daten nach Zeitstempel
        sorted_data = sorted(data, key=lambda x: x[0] if x[0] else "")

        first_event_time = None
        start_replay_time = time.time()

        for row in sorted_data:
            if len(row) <= 1 or not row[1]:
                continue

            try:
                timestamp_str = row[0]

                # Verarbeite Zeitstempel
                if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC', timestamp_str):
                    timestamp_str = timestamp_str.replace(' UTC', '')
                    current_event_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                else:
                    current_event_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

                if first_event_time is None:
                    first_event_time = current_event_time
                    print(f"Starting replay at {current_event_time}")
                else:
                    # Timing-Logik
                    time_diff = (current_event_time - first_event_time).total_seconds()
                    elapsed_target = time_diff / speed_factor
                    elapsed_actual = time.time() - start_replay_time

                    if elapsed_target > elapsed_actual:
                        time.sleep(elapsed_target - elapsed_actual)

                event_type = row[1]
                print(f"Replaying {event_type} event at {current_event_time}")
                self.api_client.send_single_request(row, track_performance=False)

            except Exception as e:
                print(f"Error processing event: {e} for timestamp: {row[0]}")
                continue
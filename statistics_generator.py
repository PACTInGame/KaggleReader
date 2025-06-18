import matplotlib.pyplot as plt
import numpy as np
from typing import List
from performance_tracker import PerformanceStats, PerformanceTracker


class StatisticsGenerator:
    """Generator für Statistiken und Visualisierungen"""

    @staticmethod
    def print_statistics(stats: PerformanceStats) -> None:
        """Gibt Statistiken in der Konsole aus"""
        print("\n" + "=" * 50)
        print("PERFORMANCE STATISTIKEN")
        print("=" * 50)
        print(f"Gesamtanzahl Requests: {stats.total_requests}")
        print(f"Gesamtdauer: {stats.total_duration:.2f} Sekunden")
        print(f"Durchschnittliche Dauer pro Request: {stats.avg_duration:.4f} Sekunden")
        print(f"Schnellste Ausführung: {stats.min_duration:.4f} Sekunden")
        print(f"Langsamste Ausführung: {stats.max_duration:.4f} Sekunden")
        print(f"Erfolgsrate: {stats.success_rate:.1f}%")

        print("\nEndpoint-spezifische Statistiken:")
        print("-" * 50)
        for event_type, endpoint_data in stats.endpoint_stats.items():
            print(f"\n{event_type.upper()}:")
            print(f"  Endpoint: {endpoint_data['endpoint']}")
            print(f"  Anzahl Requests: {endpoint_data['count']}")
            print(f"  Durchschnittliche Dauer: {endpoint_data['avg_duration']:.4f} Sekunden")
            print(f"  Schnellste Ausführung: {endpoint_data['min_duration']:.4f} Sekunden")
            print(f"  Langsamste Ausführung: {endpoint_data['max_duration']:.4f} Sekunden")
            print(f"  Erfolgsrate: {endpoint_data['success_rate']:.1f}%")

    @staticmethod
    def generate_plots(tracker: PerformanceTracker, stats: PerformanceStats) -> None:
        """Erstellt Visualisierungen der Performance-Daten"""
        if not tracker.results:
            print("Keine Daten für Plots verfügbar")
            return

        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('API Performance Analyse', fontsize=16)

        # 1. Histogram der Response-Zeiten
        durations = [r.duration for r in tracker.results]
        axes[0, 0].hist(durations, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Verteilung der Response-Zeiten')
        axes[0, 0].set_xlabel('Dauer (Sekunden)')
        axes[0, 0].set_ylabel('Anzahl Requests')
        axes[0, 0].axvline(stats.avg_duration, color='red', linestyle='--',
                           label=f'Durchschnitt: {stats.avg_duration:.4f}s')
        axes[0, 0].legend()

        # 2. Response-Zeiten über Zeit
        axes[0, 1].plot(durations, alpha=0.7, color='green')
        axes[0, 1].set_title('Response-Zeiten über Zeit')
        axes[0, 1].set_xlabel('Request Nummer')
        axes[0, 1].set_ylabel('Dauer (Sekunden)')
        axes[0, 1].axhline(stats.avg_duration, color='red', linestyle='--',
                           label=f'Durchschnitt: {stats.avg_duration:.4f}s')
        axes[0, 1].legend()

        # 3. Durchschnittliche Dauer pro Endpoint
        endpoint_names = list(stats.endpoint_stats.keys())
        endpoint_durations = [stats.endpoint_stats[name]['avg_duration'] for name in endpoint_names]

        axes[1, 0].bar(endpoint_names, endpoint_durations, color='orange', alpha=0.7)
        axes[1, 0].set_title('Durchschnittliche Dauer pro Endpoint')
        axes[1, 0].set_xlabel('Event Type')
        axes[1, 0].set_ylabel('Durchschnittliche Dauer (Sekunden)')
        axes[1, 0].tick_params(axis='x', rotation=45)

        # 4. Erfolgsrate pro Endpoint
        success_rates = [stats.endpoint_stats[name]['success_rate'] for name in endpoint_names]

        axes[1, 1].bar(endpoint_names, success_rates, color='lightgreen', alpha=0.7)
        axes[1, 1].set_title('Erfolgsrate pro Endpoint')
        axes[1, 1].set_xlabel('Event Type')
        axes[1, 1].set_ylabel('Erfolgsrate (%)')
        axes[1, 1].set_ylim(0, 105)
        axes[1, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()
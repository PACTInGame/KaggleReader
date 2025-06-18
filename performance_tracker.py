from typing import List, Dict, Any
from dataclasses import dataclass
from api_client import RequestResult


@dataclass
class PerformanceStats:
    """Sammlung von Performance-Statistiken"""
    total_requests: int
    total_duration: float
    avg_duration: float
    min_duration: float
    max_duration: float
    success_rate: float
    endpoint_stats: Dict[str, Dict[str, Any]]


class PerformanceTracker:
    """Tracker für Performance-Messungen"""

    def __init__(self):
        self.results: List[RequestResult] = []

    def add_result(self, result: RequestResult) -> None:
        """Fügt ein Request-Ergebnis hinzu"""
        self.results.append(result)

    def get_statistics(self) -> PerformanceStats:
        """Berechnet Statistiken aus den gesammelten Daten"""
        if not self.results:
            return PerformanceStats(0, 0.0, 0.0, 0.0, 0.0, 0.0, {})

        durations = [r.duration for r in self.results]
        successful_requests = [r for r in self.results if r.success]

        # Allgemeine Statistiken
        total_requests = len(self.results)
        total_duration = sum(durations)
        avg_duration = total_duration / total_requests
        min_duration = min(durations)
        max_duration = max(durations)
        success_rate = len(successful_requests) / total_requests * 100

        # Endpoint-spezifische Statistiken
        endpoint_stats = {}
        endpoints = set(r.endpoint for r in self.results)

        for endpoint in endpoints:
            endpoint_results = [r for r in self.results if r.endpoint == endpoint]
            endpoint_durations = [r.duration for r in endpoint_results]
            endpoint_successful = [r for r in endpoint_results if r.success]

            event_types = set(r.event_type for r in endpoint_results)
            event_type = list(event_types)[0] if event_types else "unknown"

            endpoint_stats[event_type] = {
                'endpoint': endpoint,
                'count': len(endpoint_results),
                'avg_duration': sum(endpoint_durations) / len(endpoint_durations),
                'min_duration': min(endpoint_durations),
                'max_duration': max(endpoint_durations),
                'success_rate': len(endpoint_successful) / len(endpoint_results) * 100 if endpoint_results else 0
            }

        return PerformanceStats(
            total_requests=total_requests,
            total_duration=total_duration,
            avg_duration=avg_duration,
            min_duration=min_duration,
            max_duration=max_duration,
            success_rate=success_rate,
            endpoint_stats=endpoint_stats
        )

    def clear(self) -> None:
        """Löscht alle gesammelten Daten"""
        self.results.clear()
import time
import requests
from typing import List, Any, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class RequestResult:
    """Ergebnis eines API-Requests mit Performance-Daten"""
    endpoint: str
    event_type: str
    duration: float
    success: bool
    status_code: Optional[int] = None
    error: Optional[str] = None


class APIClient:
    """Client für API-Requests mit Performance-Tracking"""

    def __init__(self):
        self.api_endpoints = {
            "view": "http://localhost:8080/view",
            "cart": "http://localhost:8080/cart",
            "remove_from_cart": "http://localhost:8080/remove_from_cart",
            "purchase": "http://localhost:8080/purchase"
        }

    def send_single_request(self, row: List[Any], track_performance: bool = False) -> Optional[RequestResult]:
        """
        Sendet einen einzelnen Request an die API

        Args:
            row: Datenzeile aus CSV
            track_performance: Ob Performance gemessen werden soll

        Returns:
            RequestResult wenn track_performance=True, sonst None
        """
        if len(row) <= 1 or not row[1] or row[1] not in self.api_endpoints:
            return None

        event_type = row[1]
        endpoint = self.api_endpoints[event_type]

        payload = {
            "product_id": row[2],
            "category_id": row[3],
            "category_code": row[4],
            "brand": row[5],
            "price": row[6],
            "user_id": row[7],
            "user_session": row[8] if len(row) > 8 else None
        }

        start_time = time.perf_counter() if track_performance else None

        try:
            response = requests.post(endpoint, json=payload)
            success = response.status_code == 200
            status_code = response.status_code
            error = None

            if not track_performance:
                print(f"Sending {event_type} event to {endpoint}")
                print(f"Response: {response}")

        except Exception as e:
            success = False
            status_code = None
            error = str(e)

            if not track_performance:
                print(f"Error sending data to API: {e}")

        if track_performance:
            duration = time.perf_counter() - start_time
            return RequestResult(
                endpoint=endpoint,
                event_type=event_type,
                duration=duration,
                success=success,
                status_code=status_code,
                error=error
            )

        return None
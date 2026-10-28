"""In-memory data store for the Vehicle Service API.

Keeps vehicle records in a simple dict keyed by integer id. Seeded with the
same sample data used in the Postman collection examples so responses match.
"""
from __future__ import annotations

from threading import Lock
from typing import Any, Dict, List


class VehicleNotFound(Exception):
    """Raised when a vehicle id does not exist."""


class VehicleAlreadyExists(Exception):
    """Raised when creating a vehicle with a VIN that already exists."""


# Fields that make up a vehicle record (besides the server-assigned id).
VEHICLE_FIELDS = ("nickName", "vin", "make", "model", "year", "miles")


class VehicleStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._next_id = 1
        self._vehicles: Dict[int, Dict[str, Any]] = {}
        self._seed()

    def _seed(self) -> None:
        """Seed with the sample vehicles from the collection examples."""
        self.create(
            {
                "nickName": "The Lisa Marie",
                "vin": "4M2DV11W4RDJ53329",
                "make": "Mercury",
                "model": "Villager",
                "year": "1994",
                "miles": 159864,
            }
        )
        self.create(
            {
                "nickName": "Dolly",
                "vin": "JN8AZ2KR1AT169594",
                "make": "Nissan",
                "model": "Cube",
                "year": "2010",
                "miles": 59000,
            }
        )

    def list_all(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._vehicles.values())

    def get(self, vehicle_id: int) -> Dict[str, Any]:
        with self._lock:
            vehicle = self._vehicles.get(vehicle_id)
            if vehicle is None:
                raise VehicleNotFound(vehicle_id)
            return vehicle

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            vin = data.get("vin")
            if vin is not None and any(
                v.get("vin") == vin for v in self._vehicles.values()
            ):
                raise VehicleAlreadyExists(vin)

            vehicle = {"id": self._next_id}
            for field in VEHICLE_FIELDS:
                if field in data:
                    vehicle[field] = data[field]

            self._vehicles[self._next_id] = vehicle
            self._next_id += 1
            return vehicle

    def update(self, vehicle_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            vehicle = self._vehicles.get(vehicle_id)
            if vehicle is None:
                raise VehicleNotFound(vehicle_id)

            for field in VEHICLE_FIELDS:
                if field in data:
                    vehicle[field] = data[field]
            return vehicle

    def delete(self, vehicle_id: int) -> None:
        with self._lock:
            if vehicle_id not in self._vehicles:
                raise VehicleNotFound(vehicle_id)
            del self._vehicles[vehicle_id]

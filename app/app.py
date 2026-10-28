"""Vehicle Service API.

A Flask implementation of the Vehicle Service API as defined in the
"Vehicle Service Collection" Postman collection.

Endpoints:
    GET    /vehicles        -> list all vehicles
    POST   /vehicles        -> create a vehicle
    GET    /vehicles/<id>   -> retrieve a vehicle
    PATCH  /vehicles/<id>   -> update a vehicle
    DELETE /vehicles/<id>   -> delete a vehicle
"""
from __future__ import annotations

from flask import Flask, jsonify, request

from store import VehicleStore, VehicleNotFound, VehicleAlreadyExists

app = Flask(__name__)
store = VehicleStore()

# Fields required when creating a vehicle.
REQUIRED_FIELDS = ("nickName", "vin", "make", "model", "year")


@app.get("/vehicles")
def get_all_vehicles():
    """Return the full list of vehicles."""
    return jsonify(store.list_all()), 200


@app.get("/vehicles/<int:vehicle_id>")
def retrieve_vehicle(vehicle_id: int):
    """Return a single vehicle by id."""
    try:
        return jsonify(store.get(vehicle_id)), 200
    except VehicleNotFound:
        return jsonify({"error": "Vehicle not found"}), 404


@app.post("/vehicles")
def create_vehicle():
    """Create a new vehicle."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
    if missing:
        return (
            jsonify(
                {
                    "error": "Missing required attribute",
                    "missing": missing,
                }
            ),
            400,
        )

    try:
        vehicle = store.create(data)
    except VehicleAlreadyExists:
        return jsonify({"error": "Vehicle already exists"}), 409

    return jsonify(vehicle), 201


@app.patch("/vehicles/<int:vehicle_id>")
def update_vehicle(vehicle_id: int):
    """Update an existing vehicle."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Bad request body"}), 400

    try:
        vehicle = store.update(vehicle_id, data)
    except VehicleNotFound:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify(vehicle), 200


@app.delete("/vehicles/<int:vehicle_id>")
def delete_vehicle(vehicle_id: int):
    """Delete a vehicle."""
    try:
        store.delete(vehicle_id)
    except VehicleNotFound:
        return jsonify({"error": "Vehicle not found"}), 404

    return "", 204


@app.errorhandler(500)
def internal_error(_err):
    return jsonify({"error": "Unexpected error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4500, debug=True)

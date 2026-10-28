# Vehicle Service API

A Python (Flask) implementation of the **Vehicle Service Collection** API.

## Endpoints

| Method | Path            | Description          | Success |
|--------|-----------------|----------------------|---------|
| GET    | `/vehicles`     | List all vehicles    | 200     |
| GET    | `/vehicles/<id>`| Retrieve a vehicle   | 200     |
| POST   | `/vehicles`     | Create a vehicle     | 201     |
| PATCH  | `/vehicles/<id>`| Update a vehicle     | 200     |
| DELETE | `/vehicles/<id>`| Delete a vehicle     | 204     |

### Error responses
- `400` – missing required attribute / bad request body
- `404` – vehicle not found
- `409` – vehicle already exists (duplicate VIN)
- `500` – unexpected error

## Vehicle object

```json
{
  "id": 1,
  "nickName": "The Lisa Marie",
  "vin": "4M2DV11W4RDJ53329",
  "make": "Mercury",
  "model": "Villager",
  "year": "1994",
  "miles": 159864
}
```

## Running locally

```bash
cd app
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The server listens on **http://localhost:4500** — the same base URL used by the
Vehicle Service Collection and its mock, so you can point the collection at this
running app and run the existing status-code tests against it.

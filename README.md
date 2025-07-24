# Drones Tracker System

A Django REST application for real-time tracking of drone flights, fetching drone information, and managing flight logs/history. The system integrates with MQTT for live drone telemetry and provides a robust API for querying drone status, locations, and flight paths.

## Features

- **Real-time Drone Tracking:** Receives and processes live drone telemetry via MQTT (supports public brokers like [broker.emqx.io](https://www.hivemq.com/demos/websocket-client/)).
- **RESTful API Endpoints:**
  - List all drones, search by (part of) serial.
  - Retrieve a single drone by serial.
  - Get all online drones (active within the last 30 seconds).
  - Find drones within a 5km radius of a given point (uses haversine distance).
  - Fetch a drone’s recent flight path as GeoJSON (points or lines, last 5 hours).
  - List dangerous drones (height > 500m or horizontal speed > 10 m/s).
- **Flight Logs:** Stores all incoming drone telemetry as logs, with timestamped JSON payloads.
- **Design Patterns:**
  - **Strategy Pattern:** For flexible GeoJSON flight path generation.
  - **Repository Pattern:** For clean separation of data access logic.
  - **Factory Pattern:** For path strategy instantiation.
- **Validation & Error Handling:** Clear error messages for invalid requests and data.
- **Swagger/OpenAPI Documentation:** Interactive API docs available at `/swagger/` and `/redoc/`.
- **Testing:** Includes unit and feature tests for models and API endpoints.

## Notes
- **Flight Path Logic:** Fetches a drone’s recent flight path as GeoJSON (points or lines) using all logs within a time window (default 5 hours) before the latest log timestamp, splitting flights if any gap between logs exceeds 30 seconds.
- **Dangerous Drones Logic:** Lists drones as dangerous if their height exceeds 500 meters or horizontal speed exceeds 10 m/s.

## Data Model

- **Drone:**
  - `serial` (ID), `height`, `home_distance`, `horizontal_speed`, `vertical_speed`, `latitude`, `longitude`, `last_seen`
  - `is_online` property (online if last packet within 30 seconds)
- **DroneLog:**
  - `id`, `drone` (FK), `payload` (JSON), `timestamp`

## MQTT Integration

- **Broker:** Uses public MQTT broker (e.g., `broker.emqx.io`).
- **Topic Format:** `thing/product/<drone_serial>/osd`
- **Sample Payload:**
  ```json
  {
    "elevation": 0,
    "gear": 1,
    "height": 17.2,
    "home_distance": 0.15,
    "horizontal_speed": 0,
    "vertical_speed": 0,
    "latitude": 31.97837,
    "longitude": 35.83092
    // ... other fields ...
  }
  ```
- **Testing:** Use [HiveMQ Websocket Client](https://www.hivemq.com/demos/websocket-client/) to publish test messages.

## API Endpoints

| Endpoint                                 | Description                                      |
|-------------------------------------------|--------------------------------------------------|
| `/api/v1/drones/`                        | List all drones or filter by serial              |
| `/api/v1/drones/online/`                  | List all online drones                           |
| `/api/v1/drones/range/?range&latitude&longitude`    | Drones within 5km of a point                     |
| `/api/v1/drones/<serial>/path/?path-type` | Drone’s flight path as GeoJSON                   |
| `/api/v1/drones/dangerous/`               | List dangerous drones (height/speed criteria)     |

Full interactive docs:
- Swagger: `/swagger/`
- Redoc: `/redoc/`

## Database Setup (PostGIS/PostgreSQL)

This project requires a PostgreSQL database with PostGIS extension for geospatial support. The easiest way is to use Docker:

```bash
docker run --name drone_postgis -e POSTGRES_DB=drone_flight_planner_db \
  -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=secret-password \
  -p 5432:5432 -d postgis/postgis
```

- Default DB name: `drone_flight_planner_db`
- Default user: `postgres`
- Default password: `secret-password`

You can change these in your `.env` file (see below).

## Environment Variables (.env)

Create a `.env` file in the project root with the following variables (example values shown):

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_DB_ENGINE=django.contrib.gis.db.backends.postgis
DJANGO_DB_NAME=drone_flight_planner_db
DJANGO_DB_USER=postgres
DJANGO_DB_PASSWORD=secret-password
DJANGO_DB_HOST=localhost
DJANGO_DB_PORT=5432
MQTT_SERVER=broker.emqx.io
MQTT_PORT=1883
MQTT_KEEPALIVE=60
MQTT_USER=
MQTT_PASSWORD=
IS_ONLINE_DELTA=30                # Seconds: minimum recent activity to consider a drone online
DRONE_FLIGHT_MAX_TIME=5           # Hours: time window (before latest log) to fetch logs for a drone's latest flight
DRONE_PACKETS_TIMESTAMP_DELTA=30  # Seconds: max gap between logs to consider them part of the same flight
```

## Running the Project

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure environment:**
   - Create and fill out your `.env` file as above.
3. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Start the server (recommended):**
   ```bash
   python manage.py runserver --noreload
   ```
   > Using `--noreload` avoids unwanted triggered events during development.
5. **Access API docs:**
   - Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
   - Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Testing

- **Run all tests:**
  ```bash
  python manage.py test
  ```
- **Test MQTT Integration:**
  - Use [HiveMQ Websocket Client](https://www.hivemq.com/demos/websocket-client/) to publish messages to topic `thing/product/<drone_serial>/osd` with the sample payload above.
  - Observe drone status and logs update in the API responses.

## Notes

- Uses PostGIS for geospatial queries.
- All endpoints return clear validation errors on bad input.
- Implements Strategy, Repository, and Factory design patterns for clean, maintainable code.
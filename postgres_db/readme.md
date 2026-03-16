# Database Schema

This project uses a PostgreSQL database with two tables:

- `request`
- `observation`

The schema is designed so that **each API request can contain multiple observations**.

---

# Tables

## Request Table

The `request` table stores metadata about each API request made by the backend ETL pipeline.

| Column | Type | Description |
|------|------|-------------|
| `id` | `SERIAL` | Auto-generated primary key |
| `request_timestamp` | `TIMESTAMP` | Timestamp when the request was made |
| `recordcount` | `INTEGER` | Number of records returned by the API |

Example:

| id | request_timestamp | recordcount |
|---|---|---|
| 1 | 2026-03-12 10:00:00 | 120 |

---

## Observation Table

The `observation` table stores the actual observation data retrieved from the API.

| Column | Type | Description |
|------|------|-------------|
| `id` | `TEXT` | Unique observation identifier (provided by the API) |
| `request_id` | `INTEGER` | Foreign key referencing `request.id` |
| `observation_type` | `TEXT` | Type of observation |
| `location_code` | `TEXT` | Location/station identifier |
| `observation_time` | `TIMESTAMP` | Timestamp of the observation |
| `observation_value` | `DOUBLE PRECISION` | Numeric observation value |

Example:

| id | request_id | observation_type | location_code | observation_time | observation_value |
|---|---|---|---|---|---|
| obs_001 | 1 | temperature | DK001 | 2026-03-12 09:00:00 | 6.2 |

---

# Relationship

The relationship between the tables is **one-to-many**.
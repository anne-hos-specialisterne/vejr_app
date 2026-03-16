
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime
from db_utils.connect_db import get_connection
import os


def insert_request(cursor, recordcount):
    """
    Insert a new request row and return the generated id.
    """
    query = """
    INSERT INTO request (request_timestamp, recordcount)
    VALUES (%s, %s)
    RETURNING id;
    """

    cursor.execute(query, (datetime.utcnow(), recordcount))
    request_id = cursor.fetchone()[0]

    return request_id


def insert_observations(cursor, observations, request_id):
    """
    Insert multiple observations related to a request.
    """

    query = """
    INSERT INTO observation (
        id,
        request_id,
        observation_type,
        location_code,
        observation_time,
        observation_value
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    data = [
        (
            obs["id"],
            request_id,
            obs["observation_type"],
            obs["location_code"],
            obs["observation_time"],
            obs["observation_value"],
        )
        for obs in observations
    ]

    execute_batch(cursor, query, data)


def insert_request_with_observations(observations):
    """
    Main ETL loader function.
    Inserts request metadata and all observations in one transaction.
    """

    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cursor:

                # Step 1: Insert request
                request_id = insert_request(cursor, len(observations))

                # Step 2: Insert observations
                insert_observations(cursor, observations, request_id)

                print(f"Inserted request {request_id} with {len(observations)} observations")

    except Exception as e:
        print("Database insert failed:", e)

    finally:
        conn.close()


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":

    observations = [
        {
            "id": "obs_001",
            "observation_type": "temperature",
            "location_code": "DK001",
            "observation_time": datetime(2026, 3, 12, 9, 0),
            "observation_value": 6.2,
        },
        {
            "id": "obs_002",
            "observation_type": "temperature",
            "location_code": "DK002",
            "observation_time": datetime(2026, 3, 12, 9, 0),
            "observation_value": 5.8,
        },
    ]

    insert_request_with_observations(observations)
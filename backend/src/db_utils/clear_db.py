
import os
from src.db_utils.postgres_db import PostgresDB

def clear_observations():

    DB_CONFIG = {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT")),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        }

    db = PostgresDB(db_config = DB_CONFIG)


    conn = db.get_connection()
    cur = conn.cursor()

    try: 
        cur.execute("DELETE FROM observation")
        conn.commit()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    
    return "observations deleted"

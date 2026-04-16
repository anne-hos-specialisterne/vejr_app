

from dotenv import load_dotenv
from pathlib import Path
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_utils.postgres_db import PostgresDB

project_root = Path(__file__).resolve().parents[3]


envpath = os.path.join(project_root, '.env')


load_dotenv(dotenv_path=envpath)


DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT")),
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
}

def get_observation():
    db = PostgresDB(db_config = DB_CONFIG)


    conn = db.get_connection()
    cur = conn.cursor()

    try: 
        cur.execute("SELECT * FROM observation LIMIT 20")
        res = cur.fetchall()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return res
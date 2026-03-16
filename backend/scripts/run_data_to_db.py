import os
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vejrdata.db_utils.postgres_db import PostgresDB


project_root = Path(__file__).resolve().parents[2]
print(project_root)

envpath = os.path.join(project_root, '.env')

load_dotenv(dotenv_path=envpath)


DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT")),
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
}

#print(DB_CONFIG)

db = PostgresDB(DB_CONFIG)

conn = db.get_connection()

def insert_request_info_in_db(df, conn):

    rows = len(df)

    query = f"""INSERT INTO request (request_timestamp, recordcount)
            VALUES (%s, %s)
            RETURNING id;
            """
    
    cur = conn.cursor()

    now = datetime.now()#.strftime("%Y-%m-%d %H:%M:%S")
    
    cur.execute(query, (now, rows))
    new_id = cur.fetchone()[0]
   
    conn.commit()
    return new_id

def append_df_to_postgres(df, table_name, conn):
    """
    Append a pandas DataFrame to a PostgreSQL table.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data
    table_name : str
        Target table name
    conn : psycopg2 connection
        Active PostgreSQL connection
    """

    if df.empty:
        return

    cols = list(df.columns)
    columns = ",".join(cols)

    values = [tuple(x) for x in df.to_numpy()]

    #print(values)

    query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES %s
        ON CONFLICT ON CONSTRAINT uq_observation DO NOTHING
    """

    with conn.cursor() as cur:
        execute_values(cur, query, values)

    conn.commit()

def write_api_output_to_db(pandas_df):

    print('called write_api_output_to_db function')

    request_id = insert_request_info_in_db(df = pandas_df, conn = conn)

    pandas_df['request_id'] = request_id
    append_df_to_postgres(df=pandas_df, table_name='observation', conn=conn)
    
    return 'Succes!!'
    

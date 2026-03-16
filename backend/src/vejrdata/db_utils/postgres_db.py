
import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values

project_root = Path(__file__).resolve().parents[4]
print(project_root)

envpath = os.path.join(project_root, '.env')

load_dotenv(dotenv_path=envpath)


class PostgresDB:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_connection(self):
        """
        Returns a new database connection.
        """
        try:
            conn = psycopg2.connect(
                host=self.db_config["host"],
                port=self.db_config["port"],
                dbname=self.db_config["dbname"],
                user=self.db_config["user"],
                password=self.db_config["password"]
            )
            return conn
        
        except Exception as e:
            print("Error while connecting to database:", e)
            raise



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

    query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES %s
    """

    with conn.cursor() as cur:
        execute_values(cur, query, values)

    conn.commit()

import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime


class PostgresDB:
    def __init__(self, db_config):
        self.db_config = db_config
        print(self.db_config)

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

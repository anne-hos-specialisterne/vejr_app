
import json
import sys
import os
from pathlib import Path
import time
#from dotenv import load_dotenv

import asyncio
from datetime import datetime

#from run_fetch_data import get_data_from_api
#from run_data_transform import transform_data_to_db_format
#from run_data_to_db import write_api_output_to_db

from dmi_pipeline import dmi_pipeline
from spac_pipeline import spac_pipeline


#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.vejrdata.db_utils.postgres_db import PostgresDB



DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# variables from user:
data_from = '2026-03-13T00:00:00Z'
data_source = 'dmi'
data_type = 'humidity'
data_id = '06181' # data id is station id for dmi and instrument from spac
INTERVAL = 10  # seconds

print('this is my weather app')
print('test')
print(DB_CONFIG)

db = PostgresDB(DB_CONFIG)

#time.sleep(10)

conn = db.get_connection()


async def task1():
    while True:
        print(f"{datetime.now()} - Running task1")

        dmi_pipeline(timefrom=data_from, parameter='humidity', location=data_id, conn=conn)


        await asyncio.sleep(100)


async def task2():
    while True:
        print(f"{datetime.now()} - Running task2")

        dmi_pipeline(timefrom=data_from, parameter='temp_dry', location=data_id, conn=conn)

        await asyncio.sleep(100)

async def task3():
    while True:
        print(f"{datetime.now()} - Running task3")

        spac_pipeline(timefrom=data_from, conn=conn)

        await asyncio.sleep(INTERVAL)


async def main():
    await asyncio.gather(
        task1(),
        task2(),
        task3(),
    )

if __name__ == "__main__":
    asyncio.run(main())


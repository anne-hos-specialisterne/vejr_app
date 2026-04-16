
import os
import asyncio
from datetime import datetime
import time

'''
from dotenv import load_dotenv
from pathlib import Path
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from backend.src.db_utils.postgres_db import PostgresDB

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

'''
from scripts.dmi_pipeline import dmi_pipeline
#from backend.scripts.spac_pipeline import spac_pipeline

from src.db_utils.postgres_db import PostgresDB


async def dmi_humidity(data_from, data_id, conn, stop_event):
 #   while True:
    while not stop_event.is_set():
        print(f"{datetime.now()} - Running dmi_humidity")
        dmi_pipeline(timefrom=data_from, parameter='humidity', location=data_id, conn=conn)
        await asyncio.sleep(5)


async def dmi_temp(data_from, data_id, conn, stop_event):
#    while True:
    while not stop_event.is_set():
        print(f"{datetime.now()} - Running dmi_temp")

        dmi_pipeline(timefrom=data_from, parameter='temp_dry', location=data_id, conn=conn)

        await asyncio.sleep(5)

async def dmi_pressure(data_from, data_id, conn, stop_event):
    while not stop_event.is_set():
        print(f"{datetime.now()} - Running dmi_pressure")

        dmi_pipeline(timefrom=data_from, parameter='pressure', location=data_id, conn=conn)

        await asyncio.sleep(5)
'''
async def spac(data_from, conn):
    while True:
        print(f"{datetime.now()} - Running spac")

        spac_pipeline(timefrom=data_from, conn=conn)

        await asyncio.sleep(120)
'''

async def run_data_fetch(stop_event):
    #print('this is my weather app')
    
    DB_CONFIG = {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT")),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }
    
    
    
    # variables from user:
    data_from = '2026-03-13T00:00:00Z'
    data_id = '06181' # data id is station id for dmi data

    db = PostgresDB(DB_CONFIG)

    conn = db.get_connection()
    
    await asyncio.gather(
        dmi_humidity(data_from=data_from, data_id=data_id, conn=conn, stop_event=stop_event),
        dmi_pressure(data_from=data_from, data_id=data_id, conn=conn, stop_event=stop_event),
        dmi_temp(data_from=data_from, data_id=data_id, conn=conn, stop_event=stop_event),
        #spac(data_from=data_from, conn=conn)
    )

    conn.close()


import os
import asyncio
from datetime import datetime

from dmi_pipeline import dmi_pipeline
from spac_pipeline import spac_pipeline

from src.db_utils.postgres_db import PostgresDB


async def dmi_humidity(data_from, data_id, conn):
    while True:
        print(f"{datetime.now()} - Running dmi_humidity")
        dmi_pipeline(timefrom=data_from, parameter='humidity', location=data_id, conn=conn)
        await asyncio.sleep(600)


async def dmi_temp(data_from, data_id, conn):
    while True:
        print(f"{datetime.now()} - Running dmi_temp")

        dmi_pipeline(timefrom=data_from, parameter='temp_dry', location=data_id, conn=conn)

        await asyncio.sleep(600)

async def dmi_pressure(data_from, data_id, conn):
    while True:
        print(f"{datetime.now()} - Running dmi_pressure")

        dmi_pipeline(timefrom=data_from, parameter='pressure', location=data_id, conn=conn)

        await asyncio.sleep(600)

async def spac(data_from, conn):
    while True:
        print(f"{datetime.now()} - Running spac")

        spac_pipeline(timefrom=data_from, conn=conn)

        await asyncio.sleep(120)


async def main():

    print('this is my weather app')

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
        dmi_humidity(data_from=data_from, data_id=data_id, conn=conn),
        dmi_pressure(data_from=data_from, data_id=data_id, conn=conn),
        dmi_temp(data_from=data_from, data_id=data_id, conn=conn),
        spac(data_from=data_from, conn=conn)
    )

    conn.close()

if __name__ == "__main__":
    asyncio.run(main())


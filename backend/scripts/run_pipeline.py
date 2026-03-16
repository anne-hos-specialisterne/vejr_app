
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import json

import asyncio
from datetime import datetime

from run_fetch_data import get_data_from_api
from run_data_transform import transform_data_to_db_format
from run_data_to_db import write_api_output_to_db


# variables from user:
data_from = '2026-03-13T00:00:00Z'
data_source = 'dmi'
data_type = 'humidity'
data_id = '06181' # data id is station id for dmi and instrument from spac
INTERVAL = 10  # 10 minutes in seconds

print('this is my weather app')


async def task1():
    while True:
        print(f"{datetime.now()} - Running task1")

        #### FETCH DATA FROM API

        api_out_json = get_data_from_api(data_from=data_from, data_source=data_source, data_type=data_type, data_id=data_id)


        #### TRANSFORM DATA
        api_out_pandas = transform_data_to_db_format(data_source=data_source, api_out_json=api_out_json)


        #### WRITE DATA TO DATABASE
        result = write_api_output_to_db(api_out_pandas)
        print(result)   


        await asyncio.sleep(INTERVAL)


async def task2():
    while True:
        print(f"{datetime.now()} - Running task2")
        print('other async streams can run here')
        # your code here
        await asyncio.sleep(INTERVAL)


async def main():
    await asyncio.gather(
        task1(),
        task2()
    )

if __name__ == "__main__":
    asyncio.run(main())



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
import time
from datetime import datetime
import asyncio

from backend.scripts.run_pipeline import run_data_fetch
from backend.src.display_data.api_server import get_observation

app = FastAPI()

# for allowing front-end to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# shared state for data fetching
worker_thread = None
stop_event = threading.Event()


# define data fetch function
def etl_worker():
    print("worker started")
    asyncio.run(run_data_fetch(stop_event))
    print("worker stopped")



@app.get("/data")
async def get_data():
    
    res = get_observation()
    return res

@app.get("/start-etl")
def start_etl():

    global worker_thread

    if worker_thread and worker_thread.is_alive():
        return {"status": "already running"}

    stop_event.clear()
    worker_thread = threading.Thread(target=etl_worker, daemon=True)
    worker_thread.start()

    result = {"message": "ETL started!", "value": 42}
    return result


@app.get("/stop-etl")
def stop_etl():

    stop_event.set()

    result = {"message": "ETL stopped!", "value": 27}
    return result


@app.get("/resume-etl")
def resume_etl():

    # run your python logic here
    result = {"message": "ETL resumed!", "value": 43}
    return result

@app.get("/clear-db")
def clear_db():

    # run your python logic here
    result = {"message": "All data removed!", "value": 100}
    return result

import asyncio

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from accounting.broker.connection import get_rmq_broker

app = FastAPI()

event_queue = asyncio.Queue()
broker = get_rmq_broker()

origins = [
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.on_event('startup')
async def start_up():
    loop = asyncio.get_running_loop()
    loop.create_task(broker.start())

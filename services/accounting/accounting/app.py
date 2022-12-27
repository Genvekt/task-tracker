import asyncio

from fastapi import FastAPI

from accounting.broker.connection import Consumer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

event_queue = asyncio.Queue()
consumer = Consumer(event_queue=event_queue)

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
    loop.create_task(consumer.start())

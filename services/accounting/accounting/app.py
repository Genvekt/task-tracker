import asyncio

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from accounting.tasts import daily_notify_salary_payment
from accounting.transaction.views import router as transaction_router

from accounting.broker.connection import get_rmq_broker

app = FastAPI()
app.include_router(transaction_router)

event_queue = asyncio.Queue()
broker = get_rmq_broker(event_queue=event_queue)

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
    loop.create_task(daily_notify_salary_payment(event_queue=event_queue))

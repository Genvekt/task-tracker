import asyncio

from fastapi import FastAPI
import logging

from task_admin.broker.connection import get_rmq_broker
from task_admin.tasks.views import router as task_router
from task_admin.auth.views import router as user_router
from fastapi.middleware.cors import CORSMiddleware
logging.config.fileConfig('task_admin/logging.conf', disable_existing_loggers=False)

app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)

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


@app.on_event('shutdown')
async def start_up():
    broker.stop()

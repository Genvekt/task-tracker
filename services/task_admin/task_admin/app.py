import asyncio

from fastapi import FastAPI

from task_admin.broker.connection import Consumer
from task_admin.tasks.views import router as task_router, event_queue
from task_admin.auth.views import router as user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)
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

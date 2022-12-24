import asyncio

from fastapi import FastAPI

from auth.broker.connection import Publisher
from auth.views import user_router, auth_router, event_queue
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
rmq_publisher = Publisher(event_queue=event_queue)

from auth.services.user import add_admin_user
add_admin_user()

app.include_router(user_router)
app.include_router(auth_router)

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


@app.on_event('startup')
async def start_up():
    loop = asyncio.get_running_loop()
    loop.create_task(rmq_publisher.start())


@app.on_event('shutdown')
async def start_up():
    loop = asyncio.get_running_loop()
    task = loop.create_task(rmq_publisher.stop())
    await task

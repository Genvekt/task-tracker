import asyncio

from fastapi import FastAPI

from auth.broker.connection import get_rmq_broker
from auth.views import user_router, auth_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
broker = get_rmq_broker()

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
    loop.create_task(broker.start())


@app.on_event('shutdown')
async def start_up():
    broker.stop()

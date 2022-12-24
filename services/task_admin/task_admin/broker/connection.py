import asyncio
import json

import aio_pika
from aio_pika.message import AbstractIncomingMessage
from aio_pika.exchange import ExchangeType

from task_admin.auth.models import User
from task_admin.db.connection import SessionLocal
from task_admin.db.repository import UserRepository
from task_admin.settings import RABBITMQ_URL, USER_EVENTS_EXCHANGE, USER_EVENTS_QUEUE


class Consumer:
    async def start(self):
        self._is_stopped = asyncio.Future()
        connection = await aio_pika.connect(
            RABBITMQ_URL
        )
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        exchange = await channel.declare_exchange(
            name=USER_EVENTS_EXCHANGE,
            type=ExchangeType.FANOUT
        )
        # Declaring queue
        queue = await channel.declare_queue(USER_EVENTS_QUEUE, auto_delete=False)
        await queue.bind(exchange)

        asyncio.create_task(queue.consume(self.process_message))

    async def process_message(self, message: AbstractIncomingMessage):
        async with message.process(requeue=True, ignore_processed=True):
            if message.routing_key == "UserCreatedEvent":
                try:
                    message_json = json.loads(message.body.decode())
                    db = SessionLocal()
                    user_repo = UserRepository(db)
                    existing_user = user_repo.get(email=message_json["email"])
                    if existing_user is None:
                        new_user = User(
                            public_id=message_json["public_id"],
                            name=message_json["name"],
                            email=message_json["email"],
                        )
                        user_repo.add(new_user)
                        db.commit()
                        print(f"New user added! {new_user.__dict__}")
                    db.close()
                except Exception as e:
                    await message.reject(requeue=True)

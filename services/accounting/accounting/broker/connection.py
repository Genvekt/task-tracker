import asyncio
import json

import aio_pika
from aio_pika.message import AbstractIncomingMessage
from aio_pika.exchange import ExchangeType

from accounting.settings import RABBITMQ_URL, TASK_EVENTS_EXCHANGE, TASK_EVENTS_QUEUE


class Consumer:
    def __init__(self, event_queue: asyncio.Queue):
        self._is_stopped = asyncio.Future()
        self._is_stopped.set_result(True)
        self._queue = event_queue

    async def start(self):
        self._is_stopped = asyncio.Future()
        connection = await aio_pika.connect(
            RABBITMQ_URL
        )
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        exchange = await channel.declare_exchange(
            name=TASK_EVENTS_EXCHANGE,
            type=ExchangeType.FANOUT
        )
        # Declaring queue
        queue = await channel.declare_queue(TASK_EVENTS_QUEUE, auto_delete=False)
        await queue.bind(exchange)
        asyncio.create_task(queue.consume(self.process_message))
        #await self.run_publisher(connection=connection)

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

    # async def run_publisher(self, connection: aio_pika.connection.AbstractConnection):
    #     channel = await connection.channel()
    #     exchange = await channel.declare_exchange(
    #         name=TASK_EVENTS_EXCHANGE,
    #         type=ExchangeType.FANOUT
    #     )
    #     while not self._is_stopped.done():
    #         finished, unfinished = await asyncio.wait([
    #             self._is_stopped,
    #             asyncio.create_task(self._queue.get())
    #         ], return_when=asyncio.FIRST_COMPLETED)
    #         for task in finished:
    #             event = task.result()
    #             if isinstance(event, bool):
    #                 continue
    #             await exchange.publish(
    #                 aio_pika.Message(body=f"{json.dumps(event.dict())}".encode()),
    #                 routing_key=event.__class__.__name__,
    #             )
    #             print(f"Message was published {event}")

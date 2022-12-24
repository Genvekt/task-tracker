import asyncio
import json

import aio_pika
from aio_pika.exchange import ExchangeType

from auth.settings import RABBITMQ_URL, USER_EVENTS_EXCHANGE


class Publisher:
    def __init__(self, event_queue: asyncio.Queue):
        self._is_stopped = asyncio.Future()
        self._is_stopped.set_result(True)
        self._queue = event_queue

    def stop(self):
        self._is_stopped.set_result(True)

    async def start(self):
        self._is_stopped = asyncio.Future()
        connection = await aio_pika.connect(
                RABBITMQ_URL
            )
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(name=USER_EVENTS_EXCHANGE, type=ExchangeType.FANOUT)
            while not self._is_stopped.done():
                finished, unfinished = await asyncio.wait([
                   self._is_stopped,
                   asyncio.create_task(self._queue.get())
                ], return_when=asyncio.FIRST_COMPLETED)
                for task in finished:
                    event = task.result()
                    if isinstance(event, bool):
                        continue
                    await exchange.publish(
                        aio_pika.Message(body=f"{json.dumps(event.dict())}".encode()),
                        routing_key=event.__class__.__name__,
                    )

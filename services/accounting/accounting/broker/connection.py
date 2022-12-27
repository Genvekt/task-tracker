import asyncio
import json
import random
from datetime import datetime

import aio_pika
from aio_pika.message import AbstractIncomingMessage
from aio_pika.exchange import ExchangeType

from accounting.auth.models import User
from accounting.db.connection import SessionLocal
from accounting.db.repositories import UserRepository, TransactionRepository
from accounting.settings import (
    RABBITMQ_URL,
    TASK_EVENTS_EXCHANGE,
    TASK_EVENTS_QUEUE,
    USER_EVENTS_EXCHANGE,
    USER_EVENTS_QUEUE
)
from accounting.transaction.models import Transaction, TransactionType


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
        channel1 = await connection.channel()
        await channel1.set_qos(prefetch_count=10)
        exchange1 = await channel1.declare_exchange(
            name=TASK_EVENTS_EXCHANGE,
            type=ExchangeType.FANOUT
        )
        # Declaring queue
        queue1 = await channel1.declare_queue(TASK_EVENTS_QUEUE, auto_delete=False)
        await queue1.bind(exchange1)
        asyncio.create_task(queue1.consume(self.process_message))

        channel2 = await connection.channel()
        await channel2.set_qos(prefetch_count=10)
        exchange2 = await channel2.declare_exchange(
            name=USER_EVENTS_EXCHANGE,
            type=ExchangeType.FANOUT
        )
        # Declaring queue
        queue2 = await channel2.declare_queue(USER_EVENTS_QUEUE, auto_delete=False)
        await queue2.bind(exchange2)
        asyncio.create_task(queue2.consume(self.process_message))

        #await self.run_publisher(connection=connection)

    async def process_message(self, message: AbstractIncomingMessage):
        async with message.process(requeue=True, ignore_processed=True):
            print()
            if message.routing_key == "TaskCompletedEvent":
                try:
                    message_json = json.loads(message.body.decode())

                    db = SessionLocal()
                    user_repo = UserRepository(db)
                    existing_user = user_repo.get(public_id=message_json["assignee_public_id"])
                    if existing_user is None:
                        print(f"Unable to find user: {message_json}")
                    else:
                        trans_repo = TransactionRepository(db)
                        new_transaction = Transaction(
                            user=existing_user,
                            type_=TransactionType.task_completed,
                            amount=random.uniform(20, 40),
                            ts=datetime.fromisoformat(message_json["ts"]),
                            extra={
                                "title": message_json["title"],
                                "description": message_json["description"],
                            }
                        )
                        trans_repo.add(new_transaction)
                        db.commit()
                        print(f"New transaction added! {new_transaction.__dict__}")
                    db.close()
                except Exception as e:
                    await message.reject(requeue=True)

            elif message.routing_key == "TaskAssignedEvent":
                try:
                    message_json = json.loads(message.body.decode())

                    db = SessionLocal()
                    user_repo = UserRepository(db)
                    existing_user = user_repo.get(public_id=message_json["assignee_public_id"])
                    if existing_user is None:
                        print(f"Unable to find user: {message_json}")
                    else:
                        trans_repo = TransactionRepository(db)
                        new_transaction = Transaction(
                            user=existing_user,
                            type_=TransactionType.task_assigned,
                            amount=-1 * random.uniform(10, 20),
                            ts=datetime.fromisoformat(message_json["ts"]),
                            extra={
                                "title": message_json["title"],
                                "description": message_json["description"],
                            }
                        )
                        trans_repo.add(new_transaction)
                        db.commit()
                        print(f"New transaction added! {new_transaction.__dict__}")
                    db.close()
                except Exception as e:
                    print(e)
                    await message.reject(requeue=True)
            elif message.routing_key == "UserCreatedEvent":
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
                    print(e)
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

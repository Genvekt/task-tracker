import asyncio
import logging

from auth import settings
from library.rmq_broker.broker import RMQBroker
from library.rmq_broker.events import Event, UserCreatedEvent
from marshmallow_dataclass import class_schema

publisher_event_queue = asyncio.Queue[Event]()


def get_rmq_broker() -> RMQBroker:
    broker_logger = logging.getLogger("rmq_broker")
    broker = RMQBroker(
        rmq_url=settings.RABBITMQ_URL,
        logger=broker_logger,
    )
    broker.set_publisher(
        exchange_name=settings.USER_EVENTS_EXCHANGE,
        event_queue=publisher_event_queue,
        schemas={
            UserCreatedEvent.__name__: class_schema(UserCreatedEvent)(),
        }
    )
    return broker

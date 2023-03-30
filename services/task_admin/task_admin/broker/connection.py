import asyncio
import logging
from aio_pika.exchange import ExchangeType

from library.rmq_broker.broker import RMQBroker
from library.rmq_broker.events import UserCreatedEvent, TaskAssignedEvent, TaskCompletedEvent
from task_admin import settings
from task_admin.auth.models import User
from task_admin.db.connection import SessionLocal
from task_admin.db.repository import UserRepository
from marshmallow_dataclass import class_schema

publisher_event_queue = asyncio.Queue()


def get_rmq_broker() -> RMQBroker:
    broker_logger = logging.getLogger("rmq_broker")
    broker = RMQBroker(
        rmq_url=settings.RABBITMQ_URL,
        logger=broker_logger,
    )
    broker.add_consumer(
        exchange_name=settings.USER_EVENTS_EXCHANGE,
        exchange_type=ExchangeType.FANOUT,
        queue_name=settings.USER_EVENTS_QUEUE,
        routing_key="*",
        handlers={
            UserCreatedEvent.__name__: handle_user_created
        },
        schemas={
            UserCreatedEvent.__name__: class_schema(UserCreatedEvent)()
        }
    )
    broker.set_publisher(
        exchange_name=settings.TASK_EVENTS_EXCHANGE,
        event_queue=publisher_event_queue,
        schemas={
            TaskAssignedEvent.__name__: class_schema(TaskAssignedEvent)(),
            TaskCompletedEvent.__name__: class_schema(TaskCompletedEvent)()
        },
        queue_names=[settings.ACCOUNTING_QUEUE],
        routing_key="*"
    )
    return broker


def handle_user_created(event: UserCreatedEvent, logger: logging.Logger):
    """
    Handles UserCreatedEvent by creating new user in db.
    Args:
        event (UserCreatedEvent): Event of user creation with its data.
        logger (Logger): broker logger
    """

    db = SessionLocal()
    user_repo = UserRepository(db)
    existing_user = user_repo.get(email=event.email)
    if existing_user is None:
        new_user = User(
            public_id=event.public_id,
            name=event.name,
            email=event.email,
        )
        user_repo.add(new_user)
        db.commit()
        logger.info(f"New user added! {new_user.__dict__}")
    db.close()

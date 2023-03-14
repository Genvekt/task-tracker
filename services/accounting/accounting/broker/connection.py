import asyncio
import logging
import random

from aio_pika.exchange import ExchangeType

from accounting.transaction.models import Transaction, TransactionType
from library.rmq_broker.broker import RMQBroker
from library.rmq_broker.events import UserCreatedEvent, TaskAssignedEvent, TaskCompletedEvent, SalaryPaymentEvent
from accounting import settings
from accounting.auth.models import User
from accounting.db.connection import SessionLocal
from accounting.db.repositories import TransactionRepository, UserRepository
from marshmallow_dataclass import class_schema

publisher_event_queue = asyncio.Queue()


def get_rmq_broker(event_queue: asyncio.Queue) -> RMQBroker:
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
    broker.add_consumer(
        exchange_name=settings.TASK_EVENTS_EXCHANGE,
        exchange_type=ExchangeType.FANOUT,
        queue_name=settings.TASK_EVENTS_QUEUE,
        routing_key="*",
        handlers={
            TaskAssignedEvent.__name__: handle_task_assigned,
            TaskCompletedEvent.__name__: handle_task_completed,
        },
        schemas={
            TaskAssignedEvent.__name__: class_schema(TaskAssignedEvent)(),
            TaskCompletedEvent.__name__: class_schema(TaskCompletedEvent)(),
        }
    )
    broker.set_publisher(
        exchange_name=settings.NOTIFICATION_EXCHANGE,
        event_queue=event_queue,
        schemas={
            SalaryPaymentEvent.__name__: class_schema(SalaryPaymentEvent)(),
        },
        queue_name=settings.NOTIFICATION_QUEUE,
        routing_key="*",
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


def handle_task_assigned(event: TaskAssignedEvent, logger: logging.Logger):
    """
    Handles UserCreatedEvent by creating new user in db.
    Args:
        event (UserCreatedEvent): Event of user creation with its data.
        logger (Logger): broker logger
    """

    db = SessionLocal()
    user_repo = UserRepository(db)
    existing_user = user_repo.get(public_id=event.assignee_public_id)
    if existing_user is None:
        logger.error(f"Unable to find user with public_id: {event.assignee_public_id}")
    else:
        trans_repo = TransactionRepository(db)
        new_transaction = Transaction(
            user=existing_user,
            type_=TransactionType.task_assigned,
            amount=-1 * random.uniform(10, 20),
            ts=event.ts,
            extra={
                "title": event.title,
                "description": event.description,
            }
        )
        trans_repo.add(new_transaction)
        db.commit()
        logger.info(f"New transaction added! {new_transaction.__dict__}")
    db.close()


def handle_task_completed(event: TaskCompletedEvent, logger: logging.Logger):
    """
    Handles TaskCompletedEvent by creating new user in db.
    Args:
        event (UserCreatedEvent): Event of user creation with its data.
        logger (Logger): broker logger
    """

    db = SessionLocal()
    user_repo = UserRepository(db)
    existing_user = user_repo.get(public_id=event.assignee_public_id)
    if existing_user is None:
        logger.error(f"Unable to find user: {event.assignee_public_id}")
    else:
        trans_repo = TransactionRepository(db)
        new_transaction = Transaction(
            user=existing_user,
            type_=TransactionType.task_completed,
            amount=random.uniform(20, 40),
            ts=event.ts,
            extra={
                "title": event.title,
                "description": event.description,
            }
        )
        trans_repo.add(new_transaction)
        db.commit()
        logger.info(f"New transaction added! {new_transaction.__dict__}")
    db.close()

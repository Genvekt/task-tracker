import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgrespw@localhost:55000/accounting"
)

RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL",
    "amqp://guest:guest@127.0.0.1:5672"
)

TASK_EVENTS_EXCHANGE = os.getenv(
    "TASK_EVENTS_EXCHANGE",
    "task_events_exchange"
)

TASK_EVENTS_QUEUE = os.getenv(
    "USER_EVENTS_QUEUE",
    "accounting_task_consumer"
)

USER_EVENTS_EXCHANGE = os.getenv(
    "USER_EVENTS_EXCHANGE",
    "user_events_exchange"
)

USER_EVENTS_QUEUE = os.getenv(
    "USER_EVENTS_QUEUE",
    "accounting_user_consumer"
)

NOTIFICATION_EXCHANGE = os.getenv(
    "NOTIFICATION_EXCHANGE",
    "notification_exchange"
)

NOTIFICATION_QUEUE = os.getenv(
    "NOTIFICATION_QUEUE",
    "notification_salary"
)
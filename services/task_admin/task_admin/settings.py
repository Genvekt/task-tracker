import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgrespw@localhost:55000/task-admin"
)

RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL",
    "amqp://guest:guest@rabbitmq:5672"
)

USER_EVENTS_EXCHANGE = os.getenv(
    "USER_EVENTS_EXCHANGE",
    "user_events_exchange"
)

USER_EVENTS_QUEUE = os.getenv(
    "USER_EVENTS_QUEUE",
    "task_admin_consumer"
)

TASK_EVENTS_EXCHANGE = os.getenv(
    "TASK_EVENTS_EXCHANGE",
    "task_events_exchange"
)
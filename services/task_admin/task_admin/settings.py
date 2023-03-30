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
    "auth_user_events"
)

USER_EVENTS_QUEUE = os.getenv(
    "USER_EVENTS_QUEUE",
    "task_admin_consumer"
)

TASK_EVENTS_EXCHANGE = os.getenv(
    "TASK_EVENTS_EXCHANGE",
    "task_admin_task_events"
)

ACCOUNTING_QUEUE = os.getenv(
    "TASK_EVENTS_QUEUE",
    "accounting_consumer"
)
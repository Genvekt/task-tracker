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
    "task_admin_task_events"
)

TASK_EVENTS_QUEUE = os.getenv(
    "TASK_EVENTS_QUEUE",
    "accounting_consumer"
)

USER_EVENTS_EXCHANGE = os.getenv(
    "USER_EVENTS_EXCHANGE",
    "auth_user_events"
)

USER_EVENTS_QUEUE = os.getenv(
    "USER_EVENTS_QUEUE",
    "accounting_consumer"
)

ACCOUNTING_EXCHANGE = os.getenv(
    "NOTIFICATION_EXCHANGE",
    "accounting_events"
)

NOTIFICATION_QUEUE = os.getenv(
    "NOTIFICATION_QUEUE",
    "notification_consumer"
)

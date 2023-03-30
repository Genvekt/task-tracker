import json
import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgrespw@localhost:55000/auth"
)

ACCESS_TOKEN_EXPIRES = int(os.getenv(
    "ACCESS_TOKEN_EXPIRES",
    300
))

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
PRIVATE_KEY_PATH = os.getenv(
    "PRIVATE_KEY_PATH",
    "/Users/genvekt/PycharmProjects/task-tracker/services/auth/auth/data/jwt-key"
)

PUBLIC_KEY_PATH = os.getenv(
    "PUBLIC_KEY_PATH",
    "/Users/genvekt/PycharmProjects/task-tracker/services/auth/auth/data/jwt-key.pub"
)

RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL",
    "amqp://guest:guest@rabbitmq:5672"
)

USER_EVENTS_EXCHANGE = os.getenv(
    "USER_EVENTS_EXCHANGE",
    "auth_user_events"
)

USER_EVENTS_QUEUES = json.loads(os.getenv(
    "USER_EVENTS_QUEUES",
    '["task_admin_consumer", "accounting_consumer"]'
))

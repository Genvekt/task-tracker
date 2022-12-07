import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgrespw@localhost:55000/task-admin"
)
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
JWT_SECRET = os.getenv("JWT_SECRET")
PRIVATE_KEY_PATH = os.getenv(
    "PRIVATE_KEY_PATH",
    "/Users/genvekt/PycharmProjects/task-tracker/services/auth/auth/data/jwt-key"
)

PUBLIC_KEY_PATH = os.getenv(
    "PRIVATE_KEY_PATH",
    "/Users/genvekt/PycharmProjects/task-tracker/services/auth/auth/data/jwt-key.pub"
)

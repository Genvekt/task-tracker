from sqlalchemy.orm import registry, relationship

from accounting.auth.models import User
from accounting.db.tables import users_table, transaction_table
from accounting.transaction.models import Transaction

mapper_registry = registry()

mapper_registry.map_imperatively(
    User,
    users_table
)

mapper_registry.map_imperatively(
    Transaction,
    transaction_table,
    properties={
        "user": relationship(User, backref="users", lazy="joined")
    },
)
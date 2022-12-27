from sqlalchemy import Table, MetaData, Column, ForeignKey, BigInteger, String, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
import sqlalchemy.types as types

from accounting.transaction.models import TransactionType

metadata = MetaData()


class StrEnum(types.TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """
    impl = types.String(100)
    cache_ok = True

    def __init__(self, enumtype, *args, **kwargs):
        super(StrEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


users_table = Table(
    "users",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("public_id", String(100), unique=True),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False, unique=True)
)

transaction_table = Table('transactions', metadata,
    Column('id', BigInteger, autoincrement=True, primary_key=True),
    Column('user_id', BigInteger, ForeignKey('users.id', ondelete="CASCADE")),
    Column('type', StrEnum(TransactionType), nullable=False),
    Column('amount', Float, nullable=False),
    Column('ts', DateTime, nullable=False),
    Column('extra', JSONB, nullable=False)
)
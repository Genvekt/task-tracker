from sqlalchemy import Table, MetaData, Column, ForeignKey, BigInteger, String, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
metadata = MetaData()


users_table = Table(
    "users",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("public_id", BigInteger, unique=True),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False, unique=True)
)

transaction_table = Table('transactions', metadata,
    Column('id', BigInteger, autoincrement=True, primary_key=True),
    Column('user_id', BigInteger, ForeignKey('users.id', ondelete="CASCADE")),
    Column('type', String(100), nullable=False),
    Column('amount', Float, nullable=False),
    Column('ts', DateTime, nullable=False),
    Column('extra', JSONB, nullable=False)
)
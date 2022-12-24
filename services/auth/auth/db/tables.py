from sqlalchemy import Table, MetaData, Column, ForeignKey, BigInteger, Integer, String
metadata = MetaData()

user_to_role_table = Table('user_to_role', metadata,
    Column('user_id', BigInteger, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('role_id', BigInteger, ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True)
)

roles_table = Table("roles", metadata,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(100), nullable=False, unique=True),
)

users_table = Table("users", metadata,
    Column("id", BigInteger, primary_key=True),
    Column("public_id", String(100), nullable=False, unique=True),
    Column("name", String(100), nullable=False),
    Column("email", String(150), nullable=False, unique=True),
    Column("password", String(100), nullable=False),
)
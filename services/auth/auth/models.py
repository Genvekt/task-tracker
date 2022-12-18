from auth.db.tables import users_table, roles_table, user_to_role_table
from sqlalchemy.orm import mapper, relationship

from auth.services.hash import get_password_hash


class Role:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            other.name == self.name
        )


class User:
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = get_password_hash(password)
        self.roles: list[Role] = []

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            other.name == self.name,
            other.email == self.email,
            other.password == self.password,
            other.roles == self.roles
        )


class Token:
    def __init__(self, access_token: str, token_type: str = 'bearer',):
        self.access_token = access_token
        self.token_type = token_type
        self.user = None


mapper(Role, roles_table)
mapper(
    User, users_table,
    properties={
        "roles": relationship(Role, order_by=lambda: Role.name, secondary=user_to_role_table)
    }
)


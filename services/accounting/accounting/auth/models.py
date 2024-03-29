import uuid


class User:
    def __init__(self, name: str, email: str, public_id: str = None, id: int = None):
        """User initialisation."""
        self.id = id
        self.name = name
        self.email = email
        if public_id is None:
            self.public_id = str(uuid.uuid4())
        else:
            self.public_id = public_id

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and other.name == self.name
            and other.email == self.email
            and other.public_id == other.public_id
        )

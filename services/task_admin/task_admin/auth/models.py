class User:
    def __init__(self, name: str):
        """User initialisation."""
        self.name = name

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            other.name == self.name
        )

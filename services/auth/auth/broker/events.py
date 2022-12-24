from dataclasses import dataclass, asdict


@dataclass
class UserCreatedEvent:
    public_id: str
    name: str
    email: str

    dict = asdict

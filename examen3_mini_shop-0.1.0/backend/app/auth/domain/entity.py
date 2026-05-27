from dataclasses import dataclass


@dataclass
class UserEntity:
    id: int
    email: str
    username: str
    is_admin: bool

from dataclasses import dataclass


@dataclass
class UserEntity:
    id: int
    surname: str
    name: str
    patronymic: str
    login: str
    role: str

    @property
    def full_name(self) -> str:
        parts = [self.surname, self.name, self.patronymic]
        return " ".join(p for p in parts if p).strip()

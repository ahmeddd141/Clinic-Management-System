from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name: str, phone: str) -> None:
        self.name = name
        self.phone = phone

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if len(value.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        self._name = value.strip()

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        value = value.strip()
        if not value.isdigit() or len(value) < 11:
            raise ValueError("Phone number must be at least 11 digits")
        self._phone = value

    @abstractmethod
    def role(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.role()}: {self.name}"

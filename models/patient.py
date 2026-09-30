from models.person import Person


class Patient(Person):
    def __init__(self, name: str, phone: str, age: int) -> None:
        super().__init__(name, phone)
        self.age = age

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Age must be a positive number")
        self._age = value

    def role(self) -> str:
        return "Patient"

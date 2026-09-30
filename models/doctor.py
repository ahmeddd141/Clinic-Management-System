from models.person import Person


class Doctor(Person):
    def __init__(self, name: str, phone: str, base_fee: float) -> None:
        super().__init__(name, phone)
        self.base_fee = base_fee

    @property
    def base_fee(self) -> float:
        return self._base_fee

    @base_fee.setter
    def base_fee(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Fee must be a positive number")
        self._base_fee = float(value)

    def role(self) -> str:
        return "Doctor"

    def calculate_fee(self) -> float:
        return self.base_fee


class General(Doctor):
    def role(self) -> str:
        return "General Practitioner"


class Specialist(Doctor):
    ALLOWED_SPECIALTIES = [
        "Cardiology",
        "Dermatology",
        "Pediatrics",
        "Neurology",
        "Orthopedics",
    ]

    def __init__(self, name: str, phone: str, base_fee: float, specialty: str) -> None:
        super().__init__(name, phone, base_fee)
        self.specialty = specialty

    @property
    def specialty(self) -> str:
        return self._specialty

    @specialty.setter
    def specialty(self, value: str) -> None:
        formatted_value = value.strip().title()
        if formatted_value not in self.ALLOWED_SPECIALTIES:
            raise ValueError(f"Invalid specialty. Choose from: {', '.join(self.ALLOWED_SPECIALTIES)}")
        self._specialty = formatted_value

    def role(self) -> str:
        return f"{self.specialty} Specialist"

    def calculate_fee(self) -> float:
        return self.base_fee * 1.5

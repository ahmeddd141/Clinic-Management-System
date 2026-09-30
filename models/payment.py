from datetime import datetime
from typing import Optional

from models.appointment import Appointment


class Payment:
    METHODS = ("cash", "card")

    def __init__(self, appointment: Appointment, method: str = "cash", amount: Optional[float] = None) -> None:
        if not isinstance(appointment, Appointment):
            raise TypeError("Appointment must be an Appointment object")
        if appointment.status == Appointment.STATUS_CANCELLED:
            raise ValueError("Cannot pay for a cancelled appointment")

        self.appointment = appointment                  # composition
        self.method = method
        self.amount = appointment.fee() if amount is None else amount
        self.paid_at = datetime.now()

    @property
    def method(self) -> str:
        return self._method

    @method.setter
    def method(self, value: str) -> None:
        value = value.strip().lower()
        if value not in self.METHODS:
            raise ValueError(f"Payment method must be one of: {', '.join(self.METHODS)}")
        self._method = value

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Amount must be greater than zero")
        self._amount = float(value)

    def __str__(self) -> str:
        return (
            f"{self.paid_at:%Y-%m-%d %H:%M} | {self.appointment.patient.name} | "
            f"{self.amount} EGP | {self.method}"
        )

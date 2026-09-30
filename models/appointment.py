from datetime import datetime

from models.doctor import Doctor
from models.patient import Patient


class Appointment:
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"

    def __init__(self, doctor: Doctor, patient: Patient, time: datetime) -> None:
        if not isinstance(doctor, Doctor):
            raise TypeError("Doctor must be a Doctor object")
        if not isinstance(patient, Patient):
            raise TypeError("Patient must be a Patient object")

        self.doctor = doctor
        self.patient = patient
        self.time = time
        self._status = self.STATUS_CONFIRMED

    @property
    def time(self) -> datetime:
        return self._time

    @time.setter
    def time(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise TypeError("Time must be a datetime object")
        if value < datetime.now():
            raise ValueError("Cannot book an appointment in the past")
        self._time = value

    @property
    def status(self) -> str:
        return self._status

    def is_active(self) -> bool:
        return self._status == self.STATUS_CONFIRMED

    def cancel(self) -> None:
        if self._status == self.STATUS_CANCELLED:
            raise ValueError("Appointment is already cancelled")
        self._status = self.STATUS_CANCELLED

    def reschedule(self, new_time: datetime) -> None:
        if self._status == self.STATUS_CANCELLED:
            raise ValueError("Cannot reschedule a cancelled appointment")
        self.time = new_time

    def fee(self) -> float:
        return self.doctor.calculate_fee()

    def __str__(self) -> str:
        return (
            f"{self.time:%Y-%m-%d %H:%M} | "
            f"Patient: {self.patient.name} with Dr. {self.doctor.name} | "
            f"Fee: {self.fee()} EGP | Status: {self._status}"
        )

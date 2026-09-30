from datetime import datetime

from models.doctor import Doctor
from models.patient import Patient


class MedicalRecord:
    def __init__(self, patient: Patient, doctor: Doctor, diagnosis: str, notes: str = "") -> None:
        if not isinstance(patient, Patient):
            raise TypeError("Patient must be a Patient object")
        if not isinstance(doctor, Doctor):
            raise TypeError("Doctor must be a Doctor object")

        self.patient = patient          # composition
        self.doctor = doctor            # composition
        self.diagnosis = diagnosis
        self.notes = notes
        self.visit_date = datetime.now()

    @property
    def diagnosis(self) -> str:
        return self._diagnosis

    @diagnosis.setter
    def diagnosis(self, value: str) -> None:
        if len(value.strip()) < 2:
            raise ValueError("Diagnosis must be at least 2 characters")
        self._diagnosis = value.strip()

    def __str__(self) -> str:
        return (
            f"{self.visit_date:%Y-%m-%d %H:%M} | {self.patient.name} "
            f"seen by Dr. {self.doctor.name} | Diagnosis: {self.diagnosis}"
        )

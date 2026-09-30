from datetime import datetime

from models.appointment import Appointment
from models.doctor import Doctor
from models.patient import Patient


class Clinic:
    def __init__(self, name: str) -> None:
        self.name = name
        self.doctors: list[Doctor] = []
        self.patients: list[Patient] = []
        self.appointments: list[Appointment] = []

    def add_doctor(self, doctor: Doctor) -> None:
        self.doctors.append(doctor)

    def add_patient(self, patient: Patient) -> None:
        self.patients.append(patient)

    def book_appointment(self, doctor: Doctor, patient: Patient, time: datetime) -> Appointment:
        for appt in self.appointments:
            if appt.doctor is doctor and appt.time == time and appt.is_active():
                raise ValueError("This time slot is already booked")

        appointment = Appointment(doctor, patient, time)
        self.appointments.append(appointment)
        return appointment

    def cancel_appointment(self, appointment: Appointment) -> None:
        appointment.cancel()

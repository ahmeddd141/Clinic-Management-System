import json
import os
from datetime import datetime

from models.appointment import Appointment
from models.doctor import General, Specialist
from models.patient import Patient
from services.service import Clinic

TIME_FORMAT = "%Y-%m-%d %H:%M"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "clinic.json")
REPORT_FILE = os.path.join(DATA_DIR, "report.txt")


def save(clinic: Clinic, filename: str = DATA_FILE) -> None:
    data = {
        "name": clinic.name,
        "doctors": [],
        "patients": [],
        "appointments": [],
    }

    for d in clinic.doctors:
        item = {"name": d.name, "phone": d.phone, "fee": d.base_fee}
        if isinstance(d, Specialist):
            item["specialty"] = d.specialty
        data["doctors"].append(item)

    for p in clinic.patients:
        data["patients"].append({"name": p.name, "phone": p.phone, "age": p.age})

    for a in clinic.appointments:
        data["appointments"].append({
            "doctor": a.doctor.phone,
            "patient": a.patient.phone,
            "time": a.time.strftime(TIME_FORMAT),
            "status": a.status,
        })

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load(filename: str = DATA_FILE) -> Clinic:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return Clinic("MediBook")   # no file yet: start empty

    clinic = Clinic(data["name"])

    for d in data["doctors"]:
        if "specialty" in d:
            clinic.add_doctor(Specialist(d["name"], d["phone"], d["fee"], d["specialty"]))
        else:
            clinic.add_doctor(General(d["name"], d["phone"], d["fee"]))

    for p in data["patients"]:
        clinic.add_patient(Patient(p["name"], p["phone"], p["age"]))

    for a in data["appointments"]:
        doctor = next(d for d in clinic.doctors if d.phone == a["doctor"])
        patient = next(p for p in clinic.patients if p.phone == a["patient"])
        time = datetime.strptime(a["time"], TIME_FORMAT)

        # bypass the "past date" check for old appointments
        appt = Appointment.__new__(Appointment)
        appt.doctor = doctor
        appt.patient = patient
        appt._time = time
        appt._status = a["status"]
        clinic.appointments.append(appt)

    return clinic


def export_report(clinic: Clinic, filename: str = REPORT_FILE) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{clinic.name} - Appointments Report\n")
        f.write("=" * 40 + "\n")
        for a in clinic.appointments:
            f.write(str(a) + "\n")

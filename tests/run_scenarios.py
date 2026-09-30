"""Runs the scenarios documented in test_scenarios.txt.
Run from the project root:  python tests/run_scenarios.py
"""
import os
import sys
import tempfile
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_manager import file_manager
from models.doctor import General, Specialist
from models.patient import Patient
from services.service import Clinic

results = []


def check(name, action, expect_error=None):
    try:
        action()
        ok = expect_error is None
        detail = "no error" if ok else f"expected: {expect_error}"
    except ValueError as e:
        ok = expect_error is not None and expect_error in str(e)
        detail = f"error: {e}"
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} -> {detail}")


def setup():
    clinic = Clinic("Test")
    doctor = General("Ahmed", "01012345678", 200)
    patient = Patient("Ali", "01212345678", 25)
    clinic.add_doctor(doctor)
    clinic.add_patient(patient)
    return clinic, doctor, patient


tomorrow = datetime.now().replace(second=0, microsecond=0) + timedelta(days=1)

print("--- Normal scenarios ---")
clinic, doctor, patient = setup()
check("N1 book a valid appointment", lambda: clinic.book_appointment(doctor, patient, tomorrow))
spec = Specialist("Sara", "01112345678", 200, "Cardiology")
results.append(spec.calculate_fee() == 300.0)
print(f"[{'PASS' if results[-1] else 'FAIL'}] N2 specialist fee is 1.5x -> {spec.calculate_fee()}")

print("--- Business-rule violations ---")
check("B1 double booking same doctor/time", lambda: clinic.book_appointment(doctor, patient, tomorrow), "already booked")
check("B2 booking in the past", lambda: clinic.book_appointment(doctor, patient, datetime.now() - timedelta(days=1)), "past")

print("--- Edge cases ---")
appt = clinic.appointments[0]
appt.cancel()
check("E1 cancel an already cancelled appointment", appt.cancel, "already cancelled")
check("E2 phone shorter than 11 digits", lambda: Patient("Ali", "0101", 20), "at least 11")
check("E3 book again after cancel frees the slot", lambda: clinic.book_appointment(doctor, patient, tomorrow))
check("E4 invalid specialty", lambda: Specialist("Sara", "01112345678", 200, "Magic"), "Invalid specialty")

print("--- File handling ---")
tmp = os.path.join(tempfile.mkdtemp(), "t.json")
file_manager.save(clinic, tmp)
loaded = file_manager.load(tmp)
ok = len(loaded.doctors) == 1 and len(loaded.appointments) == 2
results.append(ok)
print(f"[{'PASS' if ok else 'FAIL'}] F1 save then load keeps data")
missing = file_manager.load(os.path.join(tempfile.mkdtemp(), "none.json"))
#AI بالكامل 
ok = len(missing.doctors) == 0
results.append(ok)
print(f"[{'PASS' if ok else 'FAIL'}] F2 load missing file starts empty")

print(f"\n{sum(results)}/{len(results)} scenarios passed")
#AI بالكامل 

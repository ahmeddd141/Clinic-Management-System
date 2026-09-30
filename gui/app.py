import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk, messagebox

from file_manager import file_manager as storage
from models.doctor import General, Specialist
from models.patient import Patient

TIME_FORMAT = "%Y-%m-%d %H:%M"
FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")

GREEN = "#2e7d5b"
RED = "#c0392b"
BLUE = "#2f6fab"


class ClinicApp:
    def __init__(self) -> None:
        self.clinic = storage.load()

        self.root = tk.Tk()
        self.root.title("MediBook - Clinic Management System")
        self.root.geometry("900x560")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # ---------- style ----------
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=28, font=FONT)
        style.configure("Treeview.Heading", font=FONT_BOLD)
        style.configure("TNotebook.Tab", padding=(16, 6), font=FONT)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.build_doctors_tab(notebook)
        self.build_patients_tab(notebook)
        self.build_appointments_tab(notebook)
        self.refresh_all()

    # ---------- helpers ----------
    def safe(self, action) -> None:
        """Run an action and show any error in a message box."""
        try:
            action()
        except (ValueError, TypeError) as e:
            messagebox.showerror("Error", str(e))

    def make_tree(self, parent: tk.Widget, columns: list[str]) -> ttk.Treeview:
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            width = 220 if col in ("Name", "Doctor", "Patient") else 120
            tree.column(col, width=width, anchor="center")
        tree.tag_configure("odd", background="#f3f6f9")
        tree.tag_configure("cancelled", foreground=RED)
        tree.pack(fill="both", expand=True, padx=8, pady=8)
        return tree

    def make_entry(self, parent: tk.Widget, label: str, col: int) -> tk.Entry:
        tk.Label(parent, text=label, font=FONT).grid(row=0, column=col, padx=4)
        entry = tk.Entry(parent, width=14, font=FONT)
        entry.grid(row=1, column=col, padx=4)
        return entry

    def make_button(self, parent: tk.Widget, text: str, command, color: str = GREEN) -> tk.Button:
        return tk.Button(
            parent, text=text, bg=color, fg="white", activebackground=color,
            activeforeground="white", font=FONT_BOLD, relief="flat",
            padx=12, pady=4, cursor="hand2", command=lambda: self.safe(command),
        )

    # ---------- doctors tab ----------
    def build_doctors_tab(self, notebook: ttk.Notebook) -> None:
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Doctors")

        form = tk.Frame(tab)
        form.pack(pady=8)
        self.d_name = self.make_entry(form, "Name", 0)
        self.d_phone = self.make_entry(form, "Phone", 1)
        self.d_fee = self.make_entry(form, "Base Fee", 2)

        tk.Label(form, text="Type", font=FONT).grid(row=0, column=3, padx=4)
        self.d_type = ttk.Combobox(form, values=["General", "Specialist"], state="readonly", width=12)
        self.d_type.current(0)
        self.d_type.grid(row=1, column=3, padx=4)

        tk.Label(form, text="Specialty", font=FONT).grid(row=0, column=4, padx=4)
        self.d_specialty = ttk.Combobox(form, values=Specialist.ALLOWED_SPECIALTIES, state="disabled", width=14)
        self.d_specialty.grid(row=1, column=4, padx=4)

        # enable the specialty box only when the type is Specialist
        self.d_type.bind("<<ComboboxSelected>>", self.on_type_change)

        self.make_button(form, "Add Doctor", self.add_doctor).grid(row=1, column=5, padx=8)

        self.doctors_tree = self.make_tree(tab, ["Name", "Phone", "Role", "Fee"])

    def on_type_change(self, event=None) -> None:
        if self.d_type.get() == "Specialist":
            self.d_specialty.configure(state="readonly")
        else:
            self.d_specialty.set("")
            self.d_specialty.configure(state="disabled")

    def add_doctor(self) -> None:
        try:
            fee = float(self.d_fee.get())
        except ValueError:
            raise ValueError("Fee must be a number")

        name, phone = self.d_name.get(), self.d_phone.get()
        if self.d_type.get() == "Specialist":
            doctor = Specialist(name, phone, fee, self.d_specialty.get())
        else:
            doctor = General(name, phone, fee)

        self.clinic.add_doctor(doctor)
        for entry in (self.d_name, self.d_phone, self.d_fee):
            entry.delete(0, tk.END)
        self.refresh_all()

    # ---------- patients tab ----------
    def build_patients_tab(self, notebook: ttk.Notebook) -> None:
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Patients")

        form = tk.Frame(tab)
        form.pack(pady=8)
        self.p_name = self.make_entry(form, "Name", 0)
        self.p_phone = self.make_entry(form, "Phone", 1)
        self.p_age = self.make_entry(form, "Age", 2)
        self.make_button(form, "Add Patient", self.add_patient).grid(row=1, column=3, padx=8)

        self.patients_tree = self.make_tree(tab, ["Name", "Phone", "Age"])

    def add_patient(self) -> None:
        try:
            age = int(self.p_age.get())
        except ValueError:
            raise ValueError("Age must be a whole number")

        patient = Patient(self.p_name.get(), self.p_phone.get(), age)
        self.clinic.add_patient(patient)
        for entry in (self.p_name, self.p_phone, self.p_age):
            entry.delete(0, tk.END)
        self.refresh_all()

    # ---------- appointments tab ----------
    def build_appointments_tab(self, notebook: ttk.Notebook) -> None:
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Appointments")

        form = tk.Frame(tab)
        form.pack(pady=8)

        tk.Label(form, text="Doctor", font=FONT).grid(row=0, column=0, padx=4)
        self.a_doctor = ttk.Combobox(form, state="readonly", width=24)
        self.a_doctor.grid(row=1, column=0, padx=4)

        tk.Label(form, text="Patient", font=FONT).grid(row=0, column=1, padx=4)
        self.a_patient = ttk.Combobox(form, state="readonly", width=24)
        self.a_patient.grid(row=1, column=1, padx=4)

        tk.Label(form, text="Time (YYYY-MM-DD HH:MM)", font=FONT).grid(row=0, column=2, padx=4)
        self.a_time = tk.Entry(form, width=20, font=FONT)
        tomorrow = (datetime.now() + timedelta(days=1)).replace(hour=10, minute=0)
        self.a_time.insert(0, tomorrow.strftime(TIME_FORMAT))
        self.a_time.grid(row=1, column=2, padx=4)

        buttons = tk.Frame(tab)
        buttons.pack()
        self.make_button(buttons, "Book", self.book).pack(side="left", padx=4)
        self.make_button(buttons, "Cancel Selected", self.cancel, RED).pack(side="left", padx=4)
        self.make_button(buttons, "Export Report", self.export, BLUE).pack(side="left", padx=4)

        self.appts_tree = self.make_tree(tab, ["Time", "Doctor", "Patient", "Fee", "Status"])

    def book(self) -> None:
        d_index = self.a_doctor.current()
        p_index = self.a_patient.current()
        if d_index < 0 or p_index < 0:
            raise ValueError("Please select a doctor and a patient")

        try:
            time = datetime.strptime(self.a_time.get().strip(), TIME_FORMAT)
        except ValueError:
            raise ValueError("Time format must be YYYY-MM-DD HH:MM")

        self.clinic.book_appointment(self.clinic.doctors[d_index], self.clinic.patients[p_index], time)
        self.refresh_all()

    def cancel(self) -> None:
        selected = self.appts_tree.selection()
        if not selected:
            raise ValueError("Please select an appointment first")

        appointment = self.clinic.appointments[int(selected[0])]
        self.clinic.cancel_appointment(appointment)
        self.refresh_all()

    def export(self) -> None:
        storage.export_report(self.clinic)
        messagebox.showinfo("Done", "Report saved to data/report.txt")

    # ---------- refresh ----------
    def refresh_all(self) -> None:
        for tree in (self.doctors_tree, self.patients_tree, self.appts_tree):
            tree.delete(*tree.get_children())

        for i, d in enumerate(self.clinic.doctors):
            self.doctors_tree.insert(
                "", "end",
                values=(d.name, d.phone, d.role(), d.calculate_fee()),
                tags=("odd",) if i % 2 else (),
            )

        for i, p in enumerate(self.clinic.patients):
            self.patients_tree.insert(
                "", "end",
                values=(p.name, p.phone, p.age),
                tags=("odd",) if i % 2 else (),
            )

        for i, a in enumerate(self.clinic.appointments):
            tags = []
            if i % 2:
                tags.append("odd")
            if a.status == "cancelled":
                tags.append("cancelled")
            self.appts_tree.insert(
                "", "end", iid=str(i),
                values=(a.time.strftime(TIME_FORMAT), a.doctor.name, a.patient.name, a.fee(), a.status),
                tags=tuple(tags),
            )

        self.a_doctor["values"] = [f"{d.name} - {d.role()}" for d in self.clinic.doctors]
        self.a_patient["values"] = [f"{p.name} - {p.phone}" for p in self.clinic.patients]

    # ---------- lifecycle ----------
    def on_close(self) -> None:
        storage.save(self.clinic)
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()

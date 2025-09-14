from tkinter import *
from tkinter import messagebox, ttk
from database import Database
from datetime import datetime

class AttendanceApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Student Attendance System")
        self.root.resizable(False, False)
        self.root.geometry("1100x650")
        self.root.configure(bg="#e6f3fa")

        self.db = Database()

        self.students = [
            "Ahmed Ali",
            "Sara Mohamed",
            "Khaled Hassan",
            "Fatima Omar",
            "Youssef Amr",
            "Laila Ehab",
            "Mona Zaki"
        ]

        header_frame = Frame(self.root, bg="#3498db", pady=10)
        header_frame.pack(fill=X)
        header_label = Label(header_frame, text="STUDENT ATTENDANCE", 
                            bg="#3498db", fg="#ffffff", font=("Arial", 26, "bold"))
        header_label.pack()

        self.setup_students_panel()
        self.setup_attendance_panel()
        self.setup_report_panel()

        self.root.mainloop()

    def setup_students_panel(self):
        if hasattr(self, 'students_panel'):
            self.students_panel.destroy()

        self.students_panel = Frame(self.root, bg="#ffffff", bd=3, relief=RAISED)
        self.students_panel.place(x=20, y=80, width=250, height=550)
        students_title = Label(self.students_panel, text="Students", 
                              font=("Arial", 18, "bold"), fg="#2c3e50", bg="#ffffff")
        students_title.pack(side=TOP, fill=X, pady=8)

        for student in self.students:
            student_frame = Frame(self.students_panel, bg="#ffffff")
            student_frame.pack(fill=X, padx=10, pady=4)
            Label(student_frame, text=student, font=("Arial", 14), bg="#ffffff", 
                  anchor='w').pack(side=LEFT)

        btn_frame = Frame(self.students_panel, bg="#ffffff")
        btn_frame.pack(fill=X, pady=10)
        Button(btn_frame, text="Add Student", font=("Arial", 12, "bold"), bg="#3498db", 
               fg="white", width=10, command=self.add_student).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Delete Student", font=("Arial", 12, "bold"), bg="#e74c3c", 
               fg="white", width=10, command=self.delete_student).pack(side=LEFT, padx=5)

    def setup_attendance_panel(self):
        if hasattr(self, 'attendance_panel'):
            self.attendance_panel.destroy()

        self.attendance_panel = Frame(self.root, bg="#ffffff", bd=3, relief=RAISED)
        self.attendance_panel.place(x=290, y=80, width=450, height=550)

        self.status_vars = {}
        for i, student_name in enumerate(self.students):
            Label(self.attendance_panel, font=("Arial", 14), text=student_name, fg="#2c3e50", 
                  bg="#ffffff", padx=8, pady=6).grid(row=i, column=0, sticky='w')
            self.status_vars[student_name] = StringVar(value="Present")
            Radiobutton(self.attendance_panel, text="Present", font=("Arial", 11), 
                        bg="#ffffff", variable=self.status_vars[student_name], 
                        value="Present").grid(row=i, column=1, padx=2)
            Radiobutton(self.attendance_panel, text="Absent", font=("Arial", 11), 
                        bg="#ffffff", variable=self.status_vars[student_name], 
                        value="Absent").grid(row=i, column=2, padx=2)
            Radiobutton(self.attendance_panel, text="Late", font=("Arial", 11), 
                        bg="#ffffff", variable=self.status_vars[student_name], 
                        value="Late").grid(row=i, column=3, padx=2)

        btn_panel = Frame(self.attendance_panel, bg="#ffffff")
        btn_panel.grid(row=len(self.students), column=0, columnspan=4, pady=10)
        Button(btn_panel, text="Clear", font=("Arial", 12, "bold"), bg="#e74c3c", 
               fg="white", width=8, command=self.clear_selections).grid(row=0, column=0, padx=5)
        Button(btn_panel, text="Record", font=("Arial", 12, "bold"), bg="#2ecc71", 
               fg="white", width=8, command=self.record_attendance).grid(row=0, column=1, padx=5)
        Button(btn_panel, text="View Report", font=("Arial", 12, "bold"), bg="#f1c40f", 
               fg="black", width=10, command=self.db.show_attendance).grid(row=0, column=2, padx=5)

    def setup_report_panel(self):
        report_panel = Frame(self.root, bg="#ffffff", bd=3, relief=RAISED)
        report_panel.place(x=760, y=80, width=320, height=550)
        Label(report_panel, text="Attendance Report", font=("Arial", 18, "bold"), 
              bg="#ffffff", fg="#2c3e50").pack(side=TOP, fill=X, pady=8)
        self.report_display = Text(report_panel, font=("Courier New", 11), bg="#f0f4f8", 
                                  height=28, width=40)
        self.report_display.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def add_student(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Student")
        add_window.geometry("300x150")
        add_window.configure(bg="#e6f3fa")

        Label(add_window, text="Student Name:", font=("Arial", 12), bg="#e6f3fa").pack(pady=10)
        name_entry = Entry(add_window, font=("Arial", 12), width=20)
        name_entry.pack(pady=5)

        def submit():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a valid name.")
                return
            if name in self.students:
                messagebox.showerror("Error", "Student already exists.")
                return
            self.students.append(name)
            self.setup_students_panel()
            self.setup_attendance_panel()
            add_window.destroy()
            messagebox.showinfo("Success", f"Student {name} added successfully!")

        Button(add_window, text="Add", font=("Arial", 12, "bold"), bg="#2ecc71", 
               fg="white", command=submit).pack(pady=10)

    def delete_student(self):
        delete_window = Toplevel(self.root)
        delete_window.title("Delete Student")
        delete_window.geometry("300x150")
        delete_window.configure(bg="#e6f3fa")

        Label(delete_window, text="Select Student:", font=("Arial", 12), bg="#e6f3fa").pack(pady=10)
        student_combobox = ttk.Combobox(delete_window, values=self.students, font=("Arial", 12), state="readonly")
        student_combobox.pack(pady=5)
        student_combobox.set(self.students[0] if self.students else "")

        def submit():
            if not self.students:
                messagebox.showerror("Error", "No students to delete.")
                delete_window.destroy()
                return
            name = student_combobox.get()
            self.students.remove(name)
            self.db.delete_student_records(name)
            self.setup_students_panel()
            self.setup_attendance_panel()
            delete_window.destroy()
            messagebox.showinfo("Success", f"Student {name} deleted successfully!")

        Button(delete_window, text="Delete", font=("Arial", 12, "bold"), bg="#e74c3c", 
               fg="white", command=submit).pack(pady=10)

    def clear_selections(self):
        for var in self.status_vars.values():
            var.set("Present")
        self.report_display.delete(1.0, END)

    def record_attendance(self):
        self.report_display.delete(1.0, END)
        self.report_display.insert(END, f"{'Student':<20}{'Status':<10}\n")
        self.report_display.insert(END, "-" * 35 + "\n")

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for student in self.students:
            status = self.status_vars[student].get()
            self.report_display.insert(END, f"{student:<20}{status:<10}\n")
            self.db.add_attendance(student, status, current_time)

        self.report_display.insert(END, "-" * 35 + "\n")
        self.report_display.insert(END, f"Recorded at: {current_time}\n")
        self.report_display.insert(END, "Attendance recorded successfully!")

    def launch(self):
        self.root.mainloop()
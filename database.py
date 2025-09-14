import sqlite3
from tkinter import Toplevel, Text, Scrollbar, RIGHT, Y, BOTH, END

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('attendance.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS attendance
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           student TEXT, status TEXT, date DATETIME)''')
        self.conn.commit()

    def add_attendance(self, student, status, date):
        self.c.execute("INSERT INTO attendance (student, status, date) VALUES (?, ?, ?)",
                       (student, status, date))
        self.conn.commit()

    def delete_student_records(self, student):
        self.c.execute("DELETE FROM attendance WHERE student = ?", (student,))
        self.conn.commit()

    def show_attendance(self):
        history_window = Toplevel()
        history_window.title("Attendance History")
        history_window.geometry("700x600")
        history_window.configure(bg="#e6f3fa")

        scroll = Scrollbar(history_window)
        scroll.pack(side=RIGHT, fill=Y)

        history_text = Text(history_window, font=("Courier New", 10), bg="#ffffff", 
                           yscrollcommand=scroll.set, height=35, width=70)
        history_text.pack(fill=BOTH, expand=True, padx=10, pady=10)
        scroll.config(command=history_text.yview)

        self.c.execute("SELECT DISTINCT date FROM attendance ORDER BY date DESC")
        dates = self.c.fetchall()

        if not dates:
            history_text.insert(END, "No attendance records found in the database.")
            return

        for date in dates:
            history_text.insert(END, "\n" + "=" * 60 + "\n")
            history_text.insert(END, f"Date: {date[0]}\n")
            history_text.insert(END, "=" * 60 + "\n\n")
            history_text.insert(END, f"{'Student':<20}{'Status':<10}\n")
            history_text.insert(END, "-" * 35 + "\n")
            self.c.execute("""
                    SELECT student, status 
                    FROM attendance 
                    WHERE date = ?
                    ORDER BY id""", (date[0],))
            records = self.c.fetchall()

            present_count = sum(1 for record in records if record[1] == "Present")
            absent_count = sum(1 for record in records if record[1] == "Absent")
            late_count = sum(1 for record in records if record[1] == "Late")

            for record in records:
                history_text.insert(END, f"{record[0]:<20}{record[1]:<10}\n")
            history_text.insert(END, "-" * 35 + "\n")
            history_text.insert(END, f"{'Summary:':<20}\n")
            history_text.insert(END, f"{'Present:':<20}{present_count}\n")
            history_text.insert(END, f"{'Absent:':<20}{absent_count}\n")
            history_text.insert(END, f"{'Late:':<20}{late_count}\n")
            history_text.insert(END, "\nAttendance recorded successfully!\n")

        history_text.config(state="disabled")

    def close(self):
        self.conn.close()
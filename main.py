# import psycopg2
# from errors import *
#
# class SMS:
#     def __init__(self):
#         self.conn = psycopg2.connect(database="Student", host="localhost", user="postgres", password="root", port=5432)
#         self.cursor = self.conn.cursor()
#         self.login()
#
#     def __del__(self):
#         self.cursor.close()
#         self.conn.close()
#
#     def login(self):
#         print("Login: ")
#         print("Student ( Press 1 )")
#         print("Admin ( Press 2 )")
#         choice = int(input())
#         if choice == 1:
#             self.user = Student(self.cursor)
#
# class Student:
#     def __init__(self, cursor):
#         self.cursor = cursor
#         self.login()
#
#     def login(self):
#         while True:
#             Enrollment_no = int(input("Enter Login id (Enrollment no. ): "))
#             password = input("Enter password: ")
#             self.cursor.execute(f"SELECT COUNT(*) FROM login_credentials WHERE enrollment_no = {Enrollment_no};")
#             count = self.cursor.fetchone()[0]
#             self.cursor.execute(f"SELECT password FROM login_credentials WHERE enrollment_no = {Enrollment_no};")
#             match = self.cursor.fetchone()
#             try:
#                 if count == 0:
#                     raise EnrollmentError("Invalid enrollment number!")
#                 if match is None or match[0] != password:
#                     raise PasswordError("Invalid password!")
#             except (EnrollmentError, PasswordError) as e:
#                 print(e.message)
#             else:
#                 self.details(Enrollment_no)
#                 break
#
#     def details(self, Enrollment_no):
#         self.cursor.execute(f"SELECT Name FROM details WHERE enrollment_no = {Enrollment_no};")
#         name = self.cursor.fetchone()[0]
#
#         self.cursor.execute(f"SELECT Department FROM details WHERE enrollment_no = {Enrollment_no};")
#         dept = self.cursor.fetchone()[0]
#
#         self.cursor.execute(f"SELECT Branch FROM details WHERE enrollment_no = {Enrollment_no};")
#         branch = self.cursor.fetchone()[0]
#
#         self.cursor.execute(f"SELECT Batch FROM details WHERE enrollment_no = {Enrollment_no};")
#         batch = self.cursor.fetchone()[0]
#
#         self.cursor.execute(f"SELECT Roll_no FROM details WHERE enrollment_no = {Enrollment_no};")
#         roll_no = self.cursor.fetchone()[0]
#
#         self.cursor.execute(f"SELECT Rank FROM details WHERE enrollment_no = {Enrollment_no};")
#         rank = self.cursor.fetchone()[0]
#
#         print(f"""
#         Personal info :
#         Name : {name}
#         Enrollment no : {Enrollment_no}
#         Department : {dept}
#         Branch : {branch}
#         Batch : {batch}
#         Roll No : {roll_no}
#         Rank : {rank}
#         """)
#
#
#


import tkinter as tk
from tkinter import messagebox
import psycopg2
from errors import *


class SMSApp:
    def __init__(self):
        self.conn = psycopg2.connect(database="Student", host="localhost", user="postgres", password="root", port=5432)
        self.cursor = self.conn.cursor()

        self.root = tk.Tk()
        self.root.title("SMS Login")
        self.root.geometry("300x200")

        self.login_label = tk.Label(self.root, text="Login:")
        self.login_label.pack()

        self.student_button = tk.Button(self.root, text="Student", command=self.student_login)
        self.student_button.pack()

        self.admin_button = tk.Button(self.root, text="Admin (Not Implemented)")
        self.admin_button.pack()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def student_login(self):
        self.root.withdraw()  # Hide the main window
        student_login_window = tk.Toplevel(self.root)
        student_login_window.title("Student Login")
        student_login_window.geometry("300x200")

        self.enrollment_label = tk.Label(student_login_window, text="Enter Enrollment No:")
        self.enrollment_label.pack()

        self.enrollment_entry = tk.Entry(student_login_window)
        self.enrollment_entry.pack()

        self.password_label = tk.Label(student_login_window, text="Enter Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(student_login_window, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(student_login_window, text="Login", command=self.validate_student_login)
        self.login_button.pack()

        self.back_button = tk.Button(student_login_window, text="Back", command=self.back_to_main)
        self.back_button.pack()

    def validate_student_login(self):
        enrollment_no = self.enrollment_entry.get()
        password = self.password_entry.get()

        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM login_credentials WHERE enrollment_no = {enrollment_no};")
            count = self.cursor.fetchone()[0]

            if count == 0:
                raise EnrollmentError("Invalid enrollment number!")

            self.cursor.execute(f"SELECT password FROM login_credentials WHERE enrollment_no = {enrollment_no};")
            match = self.cursor.fetchone()

            if match is None or match[0] != password:
                raise PasswordError("Invalid password!")

            self.show_student_details(enrollment_no)

        except (EnrollmentError, PasswordError) as e:
            tk.messagebox.showerror("Error", e.message)

    def show_student_details(self, enrollment_no):
        self.cursor.execute(f"SELECT Name, Department, Branch, Batch, Roll_no, Rank FROM details WHERE enrollment_no = {enrollment_no};")
        details = self.cursor.fetchone()

        details_window = tk.Toplevel(self.root)
        details_window.title("Student Details")
        details_window.geometry("300x200")

        details_text = f"""
        Personal info : 
        Name : {details[0]}
        Enrollment no : {enrollment_no}
        Department : {details[1]}
        Branch : {details[2]}
        Batch : {details[3]}
        Roll No : {details[4]}
        Rank : {details[5]}
        """

        details_label = tk.Label(details_window, text=details_text)
        details_label.pack()

    def back_to_main(self):
        self.root.deiconify()  # Show the main window
        self.enrollment_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = SMSApp()
    app.root.mainloop()



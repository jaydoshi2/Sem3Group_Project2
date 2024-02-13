import tkinter as tk
from errors import *
import psycopg2
from tkinter import messagebox


root = tk.Tk()
root.geometry("500x600")
root.title("Tkinter Hub (Student Management System)")

bg_color = '#273b7a'

login_student_icon = tk.PhotoImage(file="login_student_img.png")
login_admin_icon = tk.PhotoImage(file="admin_img.png")
locked_icon = tk.PhotoImage(file='locked.png')
unlocked_icon = tk.PhotoImage(file='unlocked.png')
back_button = tk.PhotoImage(file='back_button.png')


def welcome_page():

    def forward_to_student_login_page():
        welcome_page_fm.destroy()
        root.update()
        student_login_page()

    def forward_to_admin_login_page():
        welcome_page_fm.destroy()
        root.update()
        admin_login_page()

    welcome_page_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness=3)

    heading_lb = tk.Label(
        welcome_page_fm, text="Welcome to\nCollege Management Portal", bg = bg_color, fg = 'white' , font=('Bold',18)
    )
    heading_lb.place(x=0,y=0,width=400)

    student_login_btn = tk.Button(welcome_page_fm, text="Login Student", bg = bg_color, fg = 'white', font = ("Bold", 15), bd = 0, command= forward_to_student_login_page)
    student_login_btn.place(x=100,y=200, width = 200)

    student_login_img = tk.Button(welcome_page_fm, image=login_student_icon, bd = 0)
    student_login_img.place(x=160,y=100)

    admin_login_btn = tk.Button(welcome_page_fm, text="Login admin", bg = bg_color, fg = 'white', font = ("Bold", 15), bd = 0, command= forward_to_admin_login_page)
    admin_login_btn.place(x=100,y=400, width = 200)

    admin_login_img = tk.Button(welcome_page_fm, image=login_admin_icon, bd = 0 )
    admin_login_img.place(x=160,y=300)

    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=400, height=500)

def student_login_page():
    conn = psycopg2.connect(database="Student", host="localhost", user="postgres", password="root", port=5432)
    cursor = conn.cursor()
    def show_hide_password():
        if password_ent['show'] == '*':
            password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            password_ent.config(show = '*')
            show_hide_btn.config(image=locked_icon)

    def forward_to_welcome_page():
        student_login_page_fm.destroy()
        root.update()
        welcome_page()


    student_login_page_fm  = tk.Frame(root, highlightbackground = bg_color, highlightthickness=3)

    heading_lb = tk.Label(student_login_page_fm, text="Student login Page", bg = bg_color, fg = "white", font=('Bold', 10))
    heading_lb.place(x=0,y=0,width = 400)

    back_icon = tk.Button(student_login_page_fm, image= back_button, bd=0, command=forward_to_welcome_page)
    back_icon.place(x = 5, y=40)

    student_icon_lb = tk.Label(student_login_page_fm, image=login_student_icon)
    student_icon_lb.place(x =  150, y=40)

    id_number_lb = tk.Label(student_login_page_fm, text="Enter enrollment number:", font= ('Bold' , 15), fg = bg_color)
    id_number_lb.place(x=80, y=140)

    id_number_ent = tk.Entry(student_login_page_fm, font=('Bold', 15), justify=tk.CENTER, highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    id_number_ent.place (x =80, y=190)

    password_lb = tk.Label(student_login_page_fm, text="Enter your password:", font = ('Bold', 15), fg = bg_color)
    password_lb.place(x=90, y=240)

    password_ent = tk.Entry(student_login_page_fm, font=('Bold', 15), justify=tk.CENTER, highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2, show="*")
    password_ent.place (x =80, y=290)

    show_hide_btn = tk.Button(student_login_page_fm, image=locked_icon, bd = 0, command= show_hide_password)
    show_hide_btn.place(x=310, y = 280)

    def loginn_validation():
        enrollment_no = id_number_ent.get()
        password = password_ent.get()
        try:
            cursor.execute(f"SELECT COUNT(*) FROM login_credentials WHERE enrollment_no = {enrollment_no};")
            count = cursor.fetchone()[0]

            if count == 0:
                id_number_ent.delete(0, tk.END)
                raise EnrollmentError("Invalid enrollment number!")

            cursor.execute(f"SELECT password FROM login_credentials WHERE enrollment_no = {enrollment_no};")
            match = cursor.fetchone()

            if match is None or match[0] != password:
                password_ent.delete(0, tk.END)
                raise PasswordError("Invalid password!")

        except (EnrollmentError, PasswordError) as e:
            tk.messagebox.showerror("Error", e.message)

    login_btn = tk.Button(student_login_page_fm, text = "Login", font=('Bold', 15), bg= bg_color, fg='white', command=loginn_validation)
    login_btn.place(x=95, y=400, width = 200, height = 40)

    student_login_page_fm.pack(pady = 30)
    student_login_page_fm.pack_propagate(False)
    student_login_page_fm.configure(width=400,height=500)


def admin_login_page():
    conn = psycopg2.connect(database="admin", host="localhost", user="postgres", password="root", port=5432)
    cursor = conn.cursor()
    def show_hide_password():
        if password_ent['show'] == '*':
            password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            password_ent.config(show = '*')
            show_hide_btn.config(image=locked_icon)

    def forward_to_welcome_page():
        admin_login_page_fm.destroy()
        root.update()
        welcome_page()


    admin_login_page_fm  = tk.Frame(root, highlightbackground = bg_color, highlightthickness=3)

    heading_lb = tk.Label(admin_login_page_fm, text="Admin login Page", bg = bg_color, fg = "white", font=('Bold', 10))
    heading_lb.place(x=0,y=0,width = 400)

    back_icon = tk.Button(admin_login_page_fm, image= back_button, bd=0, command=forward_to_welcome_page)
    back_icon.place(x = 5, y=40)

    admin_icon_lb = tk.Label(admin_login_page_fm, image=login_admin_icon)
    admin_icon_lb.place(x =  150, y=40)

    email_lb = tk.Label(admin_login_page_fm, text="Enter your email:", font= ('Bold' , 15), fg = bg_color)
    email_lb.place(x=120, y=140)

    email_ent = tk.Entry(admin_login_page_fm, font=('Bold', 15), justify=tk.CENTER, highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    email_ent.place (x =80, y=190)

    password_lb = tk.Label(admin_login_page_fm, text="Enter your password:", font = ('Bold', 15), fg = bg_color)
    password_lb.place(x=90, y=240)

    password_ent = tk.Entry(admin_login_page_fm, font=('Bold', 15), justify=tk.CENTER, highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2, show="*")
    password_ent.place (x =80, y=290)

    show_hide_btn = tk.Button(admin_login_page_fm, image=locked_icon, bd = 0, command= show_hide_password)
    show_hide_btn.place(x=310, y = 280)

    def loginn_validation():
        email = email_ent.get()
        password = password_ent.get()
        try:
            cursor.execute(f"SELECT COUNT(*) FROM login_credentials WHERE email = '{email}';")
            count = cursor.fetchone()[0]

            if count == 0:
                email_ent.delete(0, tk.END)
                password_ent.delete(0, tk.END)
                raise EnrollmentError("Invalid email address!")

            cursor.execute(f"SELECT password FROM login_credentials WHERE email = '{email}';")
            match = cursor.fetchone()

            if match is None or match[0] != password:
                email_ent.delete(0, tk.END)
                password_ent.delete(0, tk.END)
                raise PasswordError("Invalid password!")

        except (EnrollmentError, PasswordError) as e:
            tk.messagebox.showerror("Error", e.message)

    login_btn = tk.Button(admin_login_page_fm, text = "Login", font=('Bold', 15), bg= bg_color, fg='white', command=loginn_validation)
    login_btn.place(x=95, y=400, width = 200, height = 40)

    admin_login_page_fm.pack(pady = 30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=400,height=500)

welcome_page()
root.mainloop()
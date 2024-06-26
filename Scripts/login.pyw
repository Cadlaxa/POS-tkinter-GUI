from pathlib import Path as P

# from tkinter import *
# Explicit imports to satisfy Flake8
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, ttk
from ruamel.yaml import YAML
import subprocess
import os
import sys

OUTPUT_PATH = P().parent
ASSETS_PATH = OUTPUT_PATH / P(r"Assets/login_frame")
ACCOUNTS_DIR = P('./Accounts')
ACCOUNTS_DIR.mkdir(exist_ok=True)
USERS_FILE = ACCOUNTS_DIR / 'users.yaml'
ICON = P('./Assets/logour.png')
yaml = YAML()

# Global variable to store logged-in user
logged_in_user = None

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2) - 30
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to read user data from the YAML file
def read_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as file:
            return yaml.load(file) or {}
    return {}

def relative_to_assets(path: str) -> P:
    return ASSETS_PATH / P(path)

def delete_yaml_file(file_path):
    try:
        os.remove(file_path)
        print(f"The file {file_path} has been successfully deleted.")
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")

def get_login_data():
    username_or_email_from_login = entry_1.get()
    password_from_login = entry_2.get()
    data = {'username_or_email': username_or_email_from_login, 'password': password_from_login}
    with open('Accounts/login_data.yaml', 'w') as file:
        yaml.dump(data, file)

def login():
    global logged_in_user
    username_or_email = entry_1.get()  # Get the entered username or email
    password = entry_2.get()
    users = read_users()

    # Check if the entered username or email exists in users and if the password matches
    for user_name, user_data in users.items():
        if ('username' in user_data and user_data['username'] == username_or_email and user_data['password'] == password) or \
           ('email' in user_data and user_data['email'] == username_or_email and user_data['password'] == password):
            messagebox.showinfo("Login", "Login successful!")
            # Remove the previously logged-in user if exists
            if logged_in_user in users:
                users[logged_in_user]['logged'] = False  # Set previous user's 'logged' key to False
            # Set the logged-in user
            logged_in_user = user_name
            user_data['logged'] = True  # Add 'logged' key to indicate current user is logged in
            # Set 'logged' to False for other users
            for other_user_name, other_user_data in users.items():
                if other_user_name != logged_in_user:
                    other_user_data['logged'] = False
            # Update the YAML file with the new user data
            with open(USERS_FILE, "w") as file:
                yaml.dump(users, file)
            delete_yaml_file("Accounts/login_data.yaml")
            window.destroy()
            categ_script()
            return
    messagebox.showerror("Login", "Invalid username or email or password,\nCreate an Arti-san Account first before loggin in")

def login_key(event):
    login()

def signup_script():
        script_path = "Scripts/signup.pyw"
        subprocess.Popen([sys.executable, script_path])
def forgot_script():
        script_path = "Scripts/I_forgot.pyw"
        subprocess.Popen([sys.executable, script_path])
def categ_script():
        script_path = "Scripts/categories.pyw"
        subprocess.Popen([sys.executable, script_path])

def icon(window):
    img = PhotoImage(file=ICON)
    window.tk.call('wm', 'iconphoto', window._w, img)

window = Tk()
window.geometry("1080x616")
window.configure(bg = "#FFFFFF")
window.title("Welcome to Arti-san")

canvas = Canvas(window, bg = "#FFFFFF", height = 616, width = 1080, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0, 0.0, 1080.0, 616.0, fill="#FFFFFF", outline="")

login_bg = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image( 806.3641967773438, 307.2890625, image=login_bg)

gradient_bg = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(273.60693359375, 307.2890625, image=gradient_bg)

gray_grad = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(273.60693359375, 307.2890625, image=gray_grad)

hello_bg = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(275.0, 202.0, image=hello_bg)

canvas.create_text(105.95953369140625, 153.43359375, anchor="nw",
    text="Hello,", fill="#06D6A0", font=("Montserrat Regular", 40 * -1)
)
canvas.create_text(105.95953369140625, 191.6097412109375, anchor="nw",
    text="Welcome!", fill="#06D6A0", font=("Montserrat Black", 48 * -1)
)
canvas.create_text(152.0, 75.0, anchor="nw",
    text="Arti-san\n", fill="#000000", font=("Montserrat ExtraBold", 24 * -1)
)

# Email Entry
canvas.create_text(90.63092041015625, 285.0645446777344, anchor="nw",
    text="Email/Username", fill="#000000", font=("Montserrat SemiBold", 13 * -1))
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(275.3185272216797, 329.35618591308594, image=entry_image_1)
entry_1 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_1.place(x=94.95953369140625, y=306.79254150390625, width=360.7179870605469, height=43.127288818359375)

# Pass Entry
canvas.create_text(90.63092041015625, 363.61956787109375, anchor="nw",
    text="Password", fill="#000000", font=("Montserrat SemiBold", 13 * -1))
entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(275.3185272216797, 407.9111785888672, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
entry_2.place(x=94.95953369140625, y=385.3475341796875, width=360.7179870605469, height=43.127288818359375)

# Login Button
login_b = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=login_b, borderwidth=0, highlightthickness=0, command=login, relief="flat")
button_1.place(x=90.63092041015625, y=453.8741149902344, width=177.36907958984375, height=41.78453063964844)
login_hover = PhotoImage(file=relative_to_assets("button_hover_1.png"))
def button_1_hover(e):
    button_1.config(
        image=login_hover
    )
def button_1_leave(e):
    button_1.config(
        image=login_b
    )
button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)
window.bind("<Return>", login_key)

# Signup Button
signup_b = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=signup_b, borderwidth=0, highlightthickness=0, command=signup_script, relief="flat")
button_2.place(x=285.0, y=454.0, width=177.36907958984375, height=41.78453063964844)
signup_hover = PhotoImage(file=relative_to_assets("button_hover_2.png"))
def button_2_hover(e):
    button_2.config(
        image=signup_hover
    )
    get_login_data()
def button_2_leave(e):
    button_2.config(
        image=signup_b
    )
button_2.bind('<Enter>', button_2_hover)
button_2.bind('<Leave>', button_2_leave)

# Forgot Button
I_forgor = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=I_forgor, borderwidth=0, highlightthickness=0, command=forgot_script, relief="flat")
button_3.place(x=91.0, y=511.0, width=371.0, height=41.78453063964844)
forgor_hover = PhotoImage(file=relative_to_assets("button_hover_3.png"))
def button_3_hover(e):
    button_3.config(
        image=forgor_hover
    )
def button_3_leave(e):
    button_3.config(
        image=I_forgor
    )
button_3.bind('<Enter>', button_3_hover)
button_3.bind('<Leave>', button_3_leave)

# logo
logo = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(114.52020263671875, 94.23126220703125, image=logo)

image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(807.0, 45.0, image=image_image_6)

canvas.create_text(773.0, 33.0, anchor="nw",
    text="Arti-san\n", fill="#FFFFFF", font=("Montserrat ExtraBold", 15 * -1)
)

see_pass = PhotoImage(file=relative_to_assets("see_button.png"))
unsee_pass = PhotoImage(file=relative_to_assets("unsee_button.png"))

# State flag to track visibility ng password entry
is_visible = False
def toggle_password():
    global is_visible
    if is_visible:
        entry_2.config(show="*")
        button_4.config(image=unsee_pass)
        is_visible = False
    else:
        entry_2.config(show="")
        button_4.config(image=see_pass)
        is_visible = True
button_4 = Button(image=unsee_pass, borderwidth=0, highlightthickness=0, command=toggle_password, relief="flat")
button_4.place(x=419.0, y=389.0, width=37.0, height=37.0)

window.bind("<Escape>", quit)
icon(window)
center_window(window)
window.resizable(False, False)
window.mainloop()
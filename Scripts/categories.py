
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path as P

# from tkinter import *
# Explicit imports to satisfy Flake8
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, ttk
from ruamel.yaml import YAML
import subprocess


OUTPUT_PATH = P().parent
ASSETS_PATH = OUTPUT_PATH / P(r"Assets/categ_frame")
ACCOUNTS_DIR = P('./Accounts')
ACCOUNTS_DIR.mkdir(exist_ok=True)
USERS_FILE = ACCOUNTS_DIR / 'users.yaml'
ICON = P('./Assets/logour.png')
yaml = YAML()


# Function to read user data from the YAML file
def read_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as file:
            return yaml.load(file) or {}
    return {}

def relative_to_assets(path: str) -> P:
    return ASSETS_PATH / P(path)


def signup_script():
        script_path = "Scripts/signup.py"
        subprocess.run(['python', script_path])
def forgot_script():
        script_path = "Scripts/I_forgot.py"
        subprocess.run(['python', script_path])

def icon(window):
    img = PhotoImage(file=ICON)
    window.tk.call('wm', 'iconphoto', window._w, img)

window = Tk()
window.geometry("1143x619")
window.configure(bg = "#FFFFFF")
window.title("Welcome to Arti-san")
icon(window)

canvas = Canvas(window, bg = "#FFFFFF", height = 619, width = 1143, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0, 0.0, 1143.0, 619.3824462890625, fill="#FFFFFF", outline="")
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    570.9906005859375,
    60.4459228515625,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    571.0,
    365.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    571.0,
    396.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    63.9810791015625,
    60.89190673828125,
    image=image_image_4
)

canvas.create_text(
    96.0,
    41.0,
    anchor="nw",
    text="Arti-san",
    fill="#FFFFFF",
    font=("Montserrat Black", 32 * -1)
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    990.0,
    60.0,
    image=image_image_5
)

canvas.create_text(
    927.0,
    40.0,
    anchor="nw",
    text="Items on cart:",
    fill="#FFFFFF",
    font=("Montserrat SemiBold", 16 * -1)
)

canvas.create_text(
    1039.0,
    40.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("Montserrat SemiBold", 16 * -1)
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    914.0,
    60.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    572.0,
    64.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    571.0,
    61.0,
    image=image_image_8
)

canvas.create_text(
    451.0,
    41.0,
    anchor="nw",
    text="Hello There!",
    fill="#FFFFFF",
    font=("Montserrat SemiBold", 32 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=577.0,
    y=211.0,
    width=531.0,
    height=178.0
)

button_image_hover_1 = PhotoImage(
    file=relative_to_assets("button_hover_1.png"))

def button_1_hover(e):
    button_1.config(
        image=button_image_hover_1
    )
def button_1_leave(e):
    button_1.config(
        image=button_image_1
    )

button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)


button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=36.0,
    y=211.0,
    width=527.0,
    height=178.0
)

button_image_hover_2 = PhotoImage(
    file=relative_to_assets("button_hover_2.png"))

def button_2_hover(e):
    button_2.config(
        image=button_image_hover_2
    )
def button_2_leave(e):
    button_2.config(
        image=button_image_2
    )

button_2.bind('<Enter>', button_2_hover)
button_2.bind('<Leave>', button_2_leave)


button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=577.0,
    y=401.0,
    width=531.0,
    height=178.0
)

button_image_hover_3 = PhotoImage(
    file=relative_to_assets("button_hover_3.png"))

def button_3_hover(e):
    button_3.config(
        image=button_image_hover_3
    )
def button_3_leave(e):
    button_3.config(
        image=button_image_3
    )

button_3.bind('<Enter>', button_3_hover)
button_3.bind('<Leave>', button_3_leave)


button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=37.0,
    y=402.0,
    width=527.0,
    height=178.0
)

button_image_hover_4 = PhotoImage(
    file=relative_to_assets("button_hover_4.png"))

def button_4_hover(e):
    button_4.config(
        image=button_image_hover_4
    )
def button_4_leave(e):
    button_4.config(
        image=button_image_4
    )

button_4.bind('<Enter>', button_4_hover)
button_4.bind('<Leave>', button_4_leave)

window.resizable(False, False)
window.mainloop()
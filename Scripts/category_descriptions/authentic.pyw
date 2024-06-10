
from pathlib import Path as P

# from tkinter import *
# Explicit imports to satisfy Flake8
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, ttk
from ruamel.yaml import YAML
import subprocess


OUTPUT_PATH = P().parent
ASSETS_PATH = OUTPUT_PATH / P(r"Assets/categ_desc/authentic")
ACCOUNTS_DIR = P('./Accounts')
ACCOUNTS_DIR.mkdir(exist_ok=True)
USERS_FILE = ACCOUNTS_DIR / 'users.yaml'
ICON = P('./Assets/logour.png')
yaml = YAML()

def relative_to_assets(path: str) -> P:
    return ASSETS_PATH / P(path)

def icon(window):
    img = PhotoImage(file=ICON)
    window.tk.call('wm', 'iconphoto', window._w, img)

window = Tk()
window.geometry("573x545")
window.configure(bg = "#FFFFFF")
window.title("Authentoc (Original) Figures")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 545,
    width = 573,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    573.0,
    545.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    11.0,
    13.0,
    561.0,
    535.0,
    fill="#F0F3F6",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    286.0,
    371.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_hover_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=23.0,
    y=26.0,
    width=527.0,
    height=178.0
)

button_image_hover_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

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

window.bind("<Escape>", quit)
icon(window)
window.resizable(False, False)
window.mainloop()

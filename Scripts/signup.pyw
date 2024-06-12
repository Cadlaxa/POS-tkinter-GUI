from pathlib import Path as P

# from tkinter import *
# Explicit imports to satisfy Flake8
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, ttk
from ruamel.yaml import YAML
import subprocess
import os

OUTPUT_PATH = P().parent
ASSETS_PATH = OUTPUT_PATH / P(r"Assets/signup_frame")
ACCOUNTS_DIR = P('./Accounts')
ACCOUNTS_DIR.mkdir(exist_ok=True)
USERS_FILE = ACCOUNTS_DIR / 'users.yaml'
ICON = P('./Assets/logour.png')
yaml = YAML()

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2) - 30
    window.geometry(f'{width}x{height}+{x}+{y}')

def relative_to_assets(path: str) -> P:
    return ASSETS_PATH / P(path)

def icon(window):
    img = PhotoImage(file=ICON)
    window.tk.call('wm', 'iconphoto', window._w, img)

# Function to read user data from the YAML file
def read_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as file:
            return yaml.load(file) or {}
    return {}

# Function to write user data to the YAML file
def write_users(users):
    with open(USERS_FILE, 'w') as file:
        yaml.dump(users, file, default_flow_style=False)

def read_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, 'r') as file:
            return yaml.load(file) or {}
    return {}

def write_users(users):
    with open(USERS_FILE, 'w') as file:
        yaml.dump(users, file)

# Function to validate and insert data
def validate_and_insert():
    
    # Load login data from YAML file
    with open('Accounts/login_data.yaml', 'r') as file:
        login_data = yaml.load(file)
    
    # Strip any leading/trailing whitespace
    username_or_email = login_data.get('username_or_email', '')
    password1 = login_data.get('password', '')
    
    if '@' in username_or_email or '.com' in username_or_email:
        # If the input contains '@' or '.com', treat it as email
        email.delete(0, tk.END)
        email.insert(0, username_or_email)
    else:
        # Otherwise, treat it as username
        nname.delete(0, tk.END)
        nname.insert(0, username_or_email)

    # Insert password into password entry widget
    password.delete(0, tk.END)
    password.insert(0, password1)

def delete_yaml_file(file_path):
    try:
        os.remove(file_path)
        print(f"The file {file_path} has been successfully deleted.")
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")

def create_account():
    new_lname = lname.get()
    new_fname = fname.get()
    new_cont = contact.get()
    new_email = email.get()
    new_address = address.get()
    new_house = house.get()
    new_username = nname.get()
    new_password = password.get()
    confirm_password = password_confirm.get()
    
    # Check if all required fields are filled
    if not new_username or not new_password or not new_email or not new_fname or not new_lname or not new_cont or not new_address or not new_house:
        messagebox.showerror("Signup", "All fields are required.")
        return
    # Check password length
    if len(new_password) < 8 or len(new_password) > 15:
        password.config(fg='red')
        messagebox.showerror("Error", "Password must be highter than 8 and lower than 15 characters.")
        return
    else:
        password.config(fg='black')
        #password_length_label.config(text="")
    if new_password != confirm_password:
        messagebox.showerror("Signup", "Passwords do not match.")
    else:
        users = read_users()
        if new_username in users:
            messagebox.showerror("Signup", "Username already exists.")
        else:
            users[new_username] = {
                'username': new_username,
                'password': new_password,
                'email': new_email,
                'first_name': new_fname,
                'last_name': new_lname,
                'contact_number': new_cont,
                'address': new_address,
                'house_number': new_house
            }
            write_users(users)
            messagebox.showinfo("Signup", "Account created successfully!")
            delete_yaml_file("Accounts/login_data.yaml")
            window.destroy()

def create_account_key(event):
    create_account()

window = Tk()
window.geometry("1080x616")
window.configure(bg = "#FFFFFF")
window.title("Welcome to Arti-san")

canvas = Canvas(window, bg = "#FFFFFF", height = 616, width = 1079, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0, 0.0, 1079.169677734375, 616.0, fill="#FFFFFF", outline="")

gradient_bg = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(273.0, 307.0, image=gradient_bg)

gray_overlay = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(273.0, 307.0, image=gray_overlay)

hello_bg = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(267.0, 167.0, image=hello_bg)

gradient_bg1 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(806.0, 307.0, image=gradient_bg1)

gray_overlay1 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(806.0, 307.0, image=gray_overlay1)

canvas.create_text(142.479736328125, 43.5, anchor="nw",
    text="Arti-san\n", fill="#000000", font=("Montserrat ExtraBold", 24 * -1))

logo = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(105.0, 63.0, image=logo)

canvas.create_text(97.0, 117.0, anchor="nw",
    text="Hello,", fill="#06D6A0", font=("Montserrat Regular", 40 * -1))
canvas.create_text(97.0, 155.1761474609375, anchor="nw",
    text="New User!", fill="#06D6A0", font=("Montserrat Black", 48 * -1))

# Last name entry
lname_img = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(165.83489990234375, 282.5636444091797, image=lname_img)
lname = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
lname.place(x=86.0, y=260.0, width=159.6697998046875, height=43.127288818359375)
canvas.create_text(81.0, 241.0, anchor="nw",
                   text="Last name", fill="#000000", font=("Montserrat SemiBold", 13 * -1))

# Email address
email_img = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(266.21571350097656, 442.53604316711426, image=email_img)
email = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
email.place(x=86.0, y=419.98974609375, width=360.4314270019531, height=43.092594146728516)
canvas.create_text( 81.9063720703125, 398.0, anchor="nw", 
                   text="Email Address", fill="#000000", font=("Montserrat SemiBold", 13 * -1))

# First name
fname_img = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(358.5, 282.5636444091797, image=fname_img)
fname = Entry(bd=0, bg="#FFFFFF", fg="#000716",highlightthickness=0)
fname.place(x=271.0, y=260.0, width=175.0, height=43.127288818359375)
canvas.create_text(268.0, 241.0, anchor="nw", 
                   text="First name", fill="#000000", font=("Montserrat SemiBold", 13 * -1))

# Contact no
contact_img = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(267.21571350097656, 362.561372756958, image=contact_img)
contact = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
contact.place(x=87.0, y=340.01507568359375, width=360.4314270019531, height=43.092594146728516)
canvas.create_text(82.4658203125, 319.0, anchor="nw", 
                   text="Contact Number", fill="#000000", font=("Montserrat SemiBold", 13 * -1))

def address_placeholder(address, placeholder_text):
    address.insert(0, placeholder_text)
    address.config(fg='grey')
    address.bind("<FocusIn>", lambda event: clear_address(event, address, placeholder_text))
    address.bind("<FocusOut>", lambda event: restore_address(event, address, placeholder_text))

def clear_address(event, address, placeholder_text):
    if address.get() == placeholder_text:
        address.delete(0, tk.END)
        address.config(fg='black')

def restore_address(event, address, placeholder_text):
    if not address.get():
        address.insert(0, placeholder_text)
        address.config(fg='grey')

# Address
address_img = PhotoImage(file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(268.21571350097656, 522.5360431671143, image=address_img)
address = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
address.place(x=88.0, y=499.98974609375, width=360.4314270019531, height=43.092594146728516)
address_placeholder(address, "Blk, lot, Phase, Subd, Brgy, City")
canvas.create_text( 83.9063720703125, 478.0, anchor="nw",
                   text="Address", fill="#000000", font=("Montserrat SemiBold", 13 * -1))

# House Description
house_img = PhotoImage(file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(805.2157135009766, 108.56137275695801,image=house_img)
house = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
house.place(x=625.0, y=86.01507568359375, width=360.4314270019531, height=43.092594146728516)
canvas.create_text(620.4658203125, 65.0, anchor="nw",
                   text="House Description", fill="#000000", font=("Montserrat SemiBold", 13 * -1))

# Username
nname_img = PhotoImage(file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(804.2157135009766, 188.53604316711426, image=nname_img)
nname = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
nname.place(x=624.0, y=165.98974609375, width=360.4314270019531, height=43.092594146728516)
canvas.create_text(619.9063720703125, 144.0, anchor="nw",
                   text="Username", fill="#000000", font=("Montserrat SemiBold", 13 * -1))

# Password
password_img = PhotoImage(file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(806.2157135009766, 268.53604316711426, image=password_img)
password = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
password.place(x=626.0, y=245.98974609375, width=360.4314270019531, height=43.092594146728516)
canvas.create_text(621.9063720703125, 224.0, anchor="nw",
                   text="Password", fill="#000000",font=("Montserrat SemiBold", 13 * -1))

# Confirm Password
password_img1 = PhotoImage(file=relative_to_assets("entry_8.png"))
entry_bg_9 = canvas.create_image(806.2157135009766, 350, image=password_img1)
password_confirm = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
password_confirm.place(x=626.0, y=328, width=360.4314270019531, height=43.092594146728516)
canvas.create_text(621.9063720703125, 305.0, anchor="nw",
                   text="Confirm Password", fill="#000000",font=("Montserrat SemiBold", 13 * -1))

signup_img = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=signup_img, borderwidth=0, highlightthickness=0, command=create_account, relief="flat")
button_1.place(x=621.0, y=504.0, width=371.0, height=41.78453063964844)
button_image_hover_1 = PhotoImage(file=relative_to_assets("button_hover_1.png"))

def button_1_hover(e):
    button_1.config(
        image=button_image_hover_1
    )
def button_1_leave(e):
    button_1.config(
        image=signup_img
    )
button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)
window.bind("<Return>", create_account_key)
validate_and_insert()
window.bind("<Escape>", quit)
icon(window)
center_window(window)
window.resizable(False, False)
window.mainloop()
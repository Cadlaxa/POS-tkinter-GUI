import tkinter as tk
from tkinter import messagebox, ttk
from ruamel.yaml import YAML
from Assets.modules.sv_ttk import sv_ttk
from PIL import Image, ImageTk, ImageDraw
import os
from pathlib import Path as P

# Initialize YAML
yaml = YAML()

# Directories
LOGIN_PIC = P('./Assets/vivid-blurred-colorful-background.png')
ACCOUNTS_DIR = P('./Accounts')
ACCOUNTS_DIR.mkdir(exist_ok=True)
USERS_FILE = ACCOUNTS_DIR / 'users.yaml'

# Function to read user data from the YAML file
def read_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as file:
            return yaml.load(file) or {}
    return {}

# Function to write user data to the YAML file
def write_users(users):
    with open(USERS_FILE, "w") as file:
        yaml.dump(users, file)

# Function to create a rounded image
def create_rounded_image(image_path, size, radius):
    img = Image.open(image_path).convert("RGBA")
    img = img.resize((size, size), Image.LANCZOS)
    
    # Create a mask to create rounded corners
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (size, size)], radius=radius, fill=255)
    
    img.putalpha(mask)
    return ImageTk.PhotoImage(img)

class POS(tk.Tk):
    def __init__(self):
        super().__init__()
        sv_ttk.set_theme("light")
        self.title("Login")
        self.geometry("800x400")
        self.resizable(True, True)
        self.create_login_widgets()

    def create_login_widgets(self):
        # Main container
        main_frame = ttk.Frame(self, padding=20, style='Card.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)

        # Left column with image
        self.image = create_rounded_image(LOGIN_PIC, size=200, radius=30)
        image_label = ttk.Label(main_frame, image=self.image)
        image_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Right column with login/signup
        right_frame = ttk.Frame(main_frame, padding=20, style='Card.TFrame')
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)

        label_username = ttk.Label(right_frame, text="Username")
        label_username.grid(row=0, column=0, pady=5, sticky="ew")
        self.entry_username = ttk.Entry(right_frame)
        self.entry_username.grid(row=1, column=0, pady=5, sticky="ew")

        label_password = ttk.Label(right_frame, text="Password")
        label_password.grid(row=2, column=0, pady=5, sticky="ew")
        self.entry_password = ttk.Entry(right_frame, show="*")
        self.entry_password.grid(row=3, column=0, pady=5, sticky="ew")

        button_login = ttk.Button(right_frame, text="Login", command=self.login)
        button_login.grid(row=4, column=0, pady=20, sticky="ew")

        button_signup = ttk.Button(right_frame, text="Signup", command=self.signup)
        button_signup.grid(row=5, column=0, pady=5, sticky="ew")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        users = read_users()

        if username in users and users[username] == password:
            messagebox.showinfo("Login", "Login successful!")
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    def signup(self):
        signup_window = tk.Toplevel(self)
        signup_window.title("Signup")
        signup_window.geometry("300x250")

        label_new_username = ttk.Label(signup_window, text="Username")
        label_new_username.pack(pady=5)
        entry_new_username = ttk.Entry(signup_window)
        entry_new_username.pack(pady=5)

        label_new_password = ttk.Label(signup_window, text="Password")
        label_new_password.pack(pady=5)
        entry_new_password = ttk.Entry(signup_window, show="*")
        entry_new_password.pack(pady=5)

        label_confirm_password = ttk.Label(signup_window, text="Confirm Password")
        label_confirm_password.pack(pady=5)
        entry_confirm_password = ttk.Entry(signup_window, show="*")
        entry_confirm_password.pack(pady=5)

        def create_account():
            new_username = entry_new_username.get()
            new_password = entry_new_password.get()
            confirm_password = entry_confirm_password.get()

            if new_password != confirm_password:
                messagebox.showerror("Signup", "Passwords do not match.")
            else:
                users = read_users()
                if new_username in users:
                    messagebox.showerror("Signup", "Username already exists.")
                else:
                    users[new_username] = new_password
                    write_users(users)
                    messagebox.showinfo("Signup", "Account created successfully!")
                    signup_window.destroy()

        button_create_account = ttk.Button(signup_window, text="Create Account", command=create_account)
        button_create_account.pack(pady=20)

if __name__ == "__main__":
    app = POS()
    app.mainloop()

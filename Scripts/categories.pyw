from pathlib import Path as P
import tkinter as tk
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
from ruamel.yaml import YAML
import subprocess
import time
from PIL import Image, ImageTk
import sys

OUTPUT_PATH = P().parent
ASSETS_PATH = OUTPUT_PATH / P(r"Assets/categ_frame")
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

# Function to read user data from the YAML file
def read_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as file:
            return yaml.load(file) or {}
    return {}

def relative_to_assets(path: str) -> P:
    return ASSETS_PATH / P(path)


class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, event, text):
        if self.tip_window or not event:
            return
        x = event.x_root + 20
        y = event.y_root + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=text, justify=tk.LEFT,
                         background="#F0F3F6", relief=tk.SOLID, borderwidth=1,
                         font=("Montserrat SemiBold", 10))
        label.pack(ipadx=1)

    def hide_tip(self, event):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

    def update_position(self, event):
        if self.tip_window:
            x = event.x_root + 20
            y = event.y_root + 20
            self.tip_window.wm_geometry("+%d+%d" % (x, y))

def get_username_from_yaml():
    try:
        yaml = YAML()
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            account_data = yaml.load(file) or {}
        for username, details in account_data.items():
            if details.get('logged', False):
                return username
        return None
    except FileNotFoundError:
        messagebox.showinfo("Notice", "Accounts file not found.")
        return None
    except Exception as e:
        messagebox.showinfo("Error", f"Error loading account details: {e}")
        return None

def load_user_data(username):
    try:
        yaml = YAML()
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            user_data = yaml.load(file) or {}
        return user_data.get(username, {})
    except FileNotFoundError:
        print(f"User '{username}' file not found in account details.")
        return {}
    except Exception as e:
        print(f"Error loading user data for '{username}': {e}")
        return {}

def count_items_in_cart():    # use this function sa cart text     (count_items_in_cart())
    # Path to the cart YAML file
    CART_FILE = P('./Accounts/cart.yaml')
    try:
        yaml = YAML()
        with open(CART_FILE, 'r', encoding='utf-8') as file:
            cart_data = yaml.load(file)

        user_name = get_username_from_yaml()
        user_data = load_user_data(user_name)
        if user_data.get('logged', False):
            cname = user_name

        # Initialize the total quantity counter
        total_quantity = 0
        
        # Loop through items in the cart and count the total quantity
        if 'cart' in cart_data and cname in cart_data['cart'] and 'items' in cart_data['cart'][cname]:
            for item in cart_data['cart'][cname]['items']:
                quantity = item.get('Item Instance', 0)
                total_quantity += int(quantity)

        # Update the cart label text with the current total items and quantity
        canvas.itemconfig(cart_label, text=f"Items on cart:  {total_quantity}")
        # Schedule the function to run again after 1 seconds
        window.after(1000, count_items_in_cart)
    except FileNotFoundError:
        # If cart file is not found or empty, schedule the function to run again after 1 seconds
        window.after(1000, count_items_in_cart)

def cartoon_script(event):
    script_path = "Scripts/category_descriptions/cartoon.pyw"
    subprocess.Popen([sys.executable, script_path])
def nendo_script(event):
    script_path = "Scripts/category_descriptions/nendoroid.pyw"
    subprocess.Popen([sys.executable, script_path])
def authentic_script(event):
    script_path = "Scripts/category_descriptions/authentic.pyw"
    subprocess.Popen([sys.executable, script_path])
def resin_script(event):
    script_path = "Scripts/category_descriptions/resin.pyw"
    subprocess.Popen([sys.executable, script_path])
def authentic_product():
    script_path = "Scripts/authentic.pyw"
    subprocess.Popen([sys.executable, script_path])
def nendo_product():
    script_path = "Scripts/nendoroid.pyw"
    subprocess.Popen([sys.executable, script_path])
def resin_product():
    script_path = "Scripts/resin.pyw"
    subprocess.Popen([sys.executable, script_path])
def cartoon_product():
    script_path = "Scripts/cartoon.pyw"
    subprocess.Popen([sys.executable, script_path])

def logout(event):
    logout_mech()
def logout_mech():
    def get_username_from_yaml():
        try:
            yaml = YAML()
            with open(USERS_FILE, 'r', encoding='utf-8') as file:
                account_data = yaml.load(file) or {}
            
            # Check if there is a user logged in
            for username, details in account_data.items():
                if details.get('logged', False):
                    print("Username found:", username)
                    return username
            
            print("No logged-in user found.")
            return None
        except FileNotFoundError:
            messagebox.showinfo("Notice", "Accounts file not found.")
            return None
        except Exception as e:
            messagebox.showinfo("Error", f"Error loading account details: {e}")
            return None

    def load_user_data(username):
        try:
            yaml = YAML()
            user_file_path = USERS_FILE
            with open(user_file_path, 'r', encoding='utf-8') as file:
                user_data = yaml.load(file) or {}
            return user_data.get(username, {})
        except FileNotFoundError:
            print(f"User '{username}' file not found in account details.")
            return {}
        except Exception as e:
            print(f"Error loading user data for '{username}': {e}")
            return {}
    
    user_name = get_username_from_yaml()
    user_data = load_user_data(user_name)

    if not user_data:
        print(f"User '{user_name}' not found in account details.")
        return

    if user_data.get('logged', True):
        # Use username if logged in
        nname = user_name
    ae_n_s_er = messagebox.askyesno("Loging out", f"Do you want to log out {nname}?")
    if ae_n_s_er:
        window.destroy()
        script_path = "Scripts/login.pyw"
        subprocess.Popen([sys.executable, script_path])
    else:
        return    
    
def name_on_header():
    def get_username_from_yaml():
        try:
            yaml = YAML()
            with open(USERS_FILE, 'r', encoding='utf-8') as file:
                account_data = yaml.load(file) or {}
            for username, details in account_data.items():
                if details.get('logged', False):
                    print("Username found:", username)
                    return username
            print("No logged-in user found.")
            return None
        except FileNotFoundError:
            messagebox.showinfo("Notice", "Accounts file not found.")
            return None
        except Exception as e:
            messagebox.showinfo("Error", f"Error loading account details: {e}")
            return None

    def load_user_data(username):
        try:
            yaml = YAML()
            user_file_path = USERS_FILE
            with open(user_file_path, 'r', encoding='utf-8') as file:
                user_data = yaml.load(file) or {}
            return user_data.get(username, {})
        except FileNotFoundError:
            print(f"User '{username}' file not found in account details.")
            return {}
        except Exception as e:
            print(f"Error loading user data for '{username}': {e}")
            return {}

    user_name = get_username_from_yaml()
    if not user_name:
        return "There!"
    user_data = load_user_data(user_name)
    if not user_data:
        print(f"User '{user_name}' not found in account details.")
        return "There!"
    if user_data.get('logged', False):
        return f"Hello {user_name}!"
    return "There!"

def resize_image_if_needed(canvas, text_id, image_path, padding=50):
    text_bbox = canvas.bbox(text_id)
    text_width = text_bbox[2] - text_bbox[0]
    
    image = Image.open(image_path)
    image_width, image_height = image.size

    if text_width + padding > image_width:
        new_image_width = text_width + padding
        left_part = image.crop((0, 0, image_width // 3, image_height))
        middle_part = image.crop((image_width // 3, 0, 2 * image_width // 3, image_height))
        right_part = image.crop((2 * image_width // 3, 0, image_width, image_height))

        new_middle_width = new_image_width - (left_part.width + right_part.width)
        middle_part = middle_part.resize((new_middle_width, image_height))

        new_image = Image.new("RGBA", (new_image_width, image_height))
        new_image.paste(left_part, (0, 0))
        new_image.paste(middle_part, (left_part.width, 0))
        new_image.paste(right_part, (left_part.width + middle_part.width, 0))

        return ImageTk.PhotoImage(new_image)
    return ImageTk.PhotoImage(image)

def icon(window):
    img = PhotoImage(file=ICON)
    window.tk.call('wm', 'iconphoto', window._w, img)

window = Tk()
window.geometry("1143x619")
window.configure(bg="#FFFFFF")
window.title("Welcome to Arti-san")

# Checkout and Remove Items keyboard shortcut
def checkout_script(event):
    script_path = "Scripts/checkout.pyw"
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup_info.wShowWindow = subprocess.SW_HIDE
    try:
        subprocess.Popen(['python', script_path], startupinfo=startup_info)
    except Exception as e:
        print("Error executing checkout script:", e)
def remove_script(event):
    script_path = "Scripts/remove_items.pyw"
    subprocess.Popen([sys.executable, script_path])
window.bind("<Return>", checkout_script)
window.bind("<BackSpace>", remove_script)

canvas = Canvas(window, bg="#FFFFFF", height=619, width=1143, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(0.0, 0.0, 1143.0, 619.3824462890625, fill="#FFFFFF", outline="")

grad_header = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(570.9906005859375, 60.4459228515625, image=grad_header)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(571.0, 365.0, image=image_image_2)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(571.0, 396.0, image=image_image_3)

logo = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(63.9810791015625, 60.89190673828125, image=logo)

canvas.create_text(110.0, 38.0, anchor="nw", text="Arti-san", fill="#FFFFFF", font=("Montserrat Black", 32 * -1))

# Items on Cart
items_img = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(990.0, 60.0, image=items_img)
cart_label = canvas.create_text(935.0, 47.0, anchor="nw", text="Items on cart:", fill="#FFFFFF", font=("Montserrat SemiBold", 16 * -1))
# Numbers on cart
canvas.create_text(1060.0, 47.0, anchor="nw", text=count_items_in_cart(), fill="#FFFFFF", font=("Montserrat SemiBold", 16 * -1))
cart_img = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(914.0, 60.0, image=cart_img)

# Header text
nickname = canvas.create_text(0, 0, anchor="nw", text=name_on_header(), fill="#FFFFFF", font=("Montserrat SemiBold", 32 * -1))
canvas.update_idletasks()
canvas_width = canvas.winfo_width()
text_bbox = canvas.bbox(nickname)
text_width = text_bbox[2] - text_bbox[0]
x = (canvas_width - text_width) / 2
canvas.coords(nickname, x, 37)

# Resize image if needed based on text width
image_image_71 = file=relative_to_assets("image_7.png")
image_image_81 = file=relative_to_assets("image_8.png")
image_image_7 = resize_image_if_needed(canvas, nickname, image_image_71, padding=130)
image_image_8 = resize_image_if_needed(canvas, nickname, image_image_81, padding=50)
image_7 = canvas.create_image(572.0, 64.0, image=image_image_7)
image_8 = canvas.create_image(571.0, 61.0, image=image_image_8)
canvas.tag_raise(nickname)

# Class A (Resin)
resin_img = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=resin_img, borderwidth=0, highlightthickness=0, command=resin_product, relief="flat")
button_1.place(x=577.0, y=211.0, width=531.0, height=178.0)
button_image_hover_1 = PhotoImage(file=relative_to_assets("button_hover_1.png"))
def button_1_hover(e):
    button_1.config(image=button_image_hover_1)
def button_1_leave(e):
    button_1.config(image=resin_img)
button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)
button_1.bind('<Button-3>', resin_script)
# Create and bind the tooltip
tooltip_1 = ToolTip(button_1)
def on_enter_1(event):
    button_1_hover(event)
    tooltip_1.show_tip(event, "Resin Copy Figurines are stunning replicas \nthat was crafted from High-Quality resin\n\n(Right click for more info!)")
def on_leave_1(event):
    button_1_leave(event)
    tooltip_1.hide_tip(event)
def on_motion_1(event):
    tooltip_1.update_position(event)
button_1.bind('<Enter>', on_enter_1)
button_1.bind('<Leave>', on_leave_1)
button_1.bind('<Motion>', on_motion_1)

# Original (authentic)
orig_img = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=orig_img, borderwidth=0, highlightthickness=0, command=authentic_product, relief="flat")
button_2.place(x=36.0, y=211.0, width=527.0, height=178.0)
button_image_hover_2 = PhotoImage(file=relative_to_assets("button_hover_2.png"))
def button_2_hover(e):
    button_2.config(image=button_image_hover_2)
def button_2_leave(e):
    button_2.config(image=orig_img)
button_2.bind('<Enter>', button_2_hover)
button_2.bind('<Leave>', button_2_leave)
button_2.bind('<Button-3>', authentic_script)
# Create and bind the tooltip
tooltip_2 = ToolTip(button_2)
def on_enter_2(event):
    button_2_hover(event)
    tooltip_2.show_tip(event, "Authentic Figurines are crafted \nwith exceptional attention to \ncarefully detail each model\n\n(Right click for more info!)")
def on_leave_2(event):
    button_2_leave(event)
    tooltip_2.hide_tip(event)
def on_motion_2(event):
    tooltip_2.update_position(event)
button_2.bind('<Enter>', on_enter_2)
button_2.bind('<Leave>', on_leave_2)
button_2.bind('<Motion>', on_motion_2)

# Cartoon
cartoon_img = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=cartoon_img, borderwidth=0, highlightthickness=0, command=cartoon_product, relief="flat")
button_3.place(x=577.0, y=401.0, width=531.0, height=178.0)
button_image_hover_3 = PhotoImage(file=relative_to_assets("button_hover_3.png"))
def button_3_hover(e):
    button_3.config(image=button_image_hover_3)
def button_3_leave(e):
    button_3.config(image=cartoon_img)
button_3.bind('<Enter>', button_3_hover)
button_3.bind('<Leave>', button_3_leave)
button_3.bind('<Button-3>', cartoon_script)
# Create and bind the tooltip
tooltip_3 = ToolTip(button_3)
def on_enter_3(event):
    button_3_hover(event)
    tooltip_3.show_tip(event, "The Cartoon Figures feature cute, and adorable\ncompanions in collectible form!\n\n(Right click for more info!)")
def on_leave_3(event):
    button_3_leave(event)
    tooltip_3.hide_tip(event)
def on_motion_3(event):
    tooltip_3.update_position(event)
button_3.bind('<Enter>', on_enter_3)
button_3.bind('<Leave>', on_leave_3)
button_3.bind('<Motion>', on_motion_3)

# Nendoroid
nendo_img = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=nendo_img, borderwidth=0, highlightthickness=0, command=nendo_product, relief="flat")
button_4.place(x=37.0, y=402.0, width=527.0, height=178.0)
button_image_hover_4 = PhotoImage(file=relative_to_assets("button_hover_4.png"))
def button_4_hover(e):
    button_4.config(image=button_image_hover_4)
def button_4_leave(e):
    button_4.config(image=nendo_img)
button_4.bind('<Enter>', button_4_hover)
button_4.bind('<Leave>', button_4_leave)
button_4.bind('<Button-3>', nendo_script)
# Create and bind the tooltip
tooltip_4 = ToolTip(button_4)
def on_enter_4(event):
    button_4_hover(event)
    tooltip_4.show_tip(event, "The Nendoroid series features cute,\nchibi-style figures that fit in the\npalm of your hand\n\n(Right click for more info!).")
def on_leave_4(event):
    button_4_leave(event)
    tooltip_4.hide_tip(event)
def on_motion_4(event):
    tooltip_4.update_position(event)
button_4.bind('<Enter>', on_enter_4)
button_4.bind('<Leave>', on_leave_4)
button_4.bind('<Motion>', on_motion_4)

window.bind("<Escape>", logout)
window.protocol("WM_DELETE_WINDOW", logout_mech)

logout_b = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(image=logout_b, borderwidth=0, highlightthickness=0, command= logout_mech, relief="flat")
button_5.place(x=823.0, y=35.0, width=47.0, height=47.0)

icon(window)
center_window(window)
window.resizable(False, False)
window.mainloop()
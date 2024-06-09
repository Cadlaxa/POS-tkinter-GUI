from pathlib import Path as P
import tkinter as tk
from tkinter import Tk, Canvas, Button, PhotoImage
from ruamel.yaml import YAML
from PIL import Image, ImageTk
import subprocess

OUTPUT_PATH = P().parent
ASSETS_PATH = OUTPUT_PATH / P(r"Assets/authentic_frame")
ACCOUNTS_DIR = P('./Accounts')
ACCOUNTS_DIR.mkdir(exist_ok=True)
USERS_FILE = ACCOUNTS_DIR / 'users.yaml'
ICON = P('./Assets/logour.png')
yaml = YAML()
type = "Authentic (Original) Figures"
textheader = "Authentic"


def relative_to_assets(path: str) -> P:
    return ASSETS_PATH / P(path)

def icon(window):
    img = PhotoImage(file=ICON)
    window.tk.call('wm', 'iconphoto', window._w, img)

def load_and_resize_image(path, scale_factor):
    # Load the image using Pillow
    image = Image.open(path)
    # Calculate new dimensions
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)
scale_factor = 0.97

def count_items_in_cart():    # use this function sa cart text     (count_items_in_cart())
    # Path to the cart YAML file
    CART_FILE = P('./Accounts/cart.yaml')
    try:
        yaml = YAML()
        with open(CART_FILE, 'r', encoding='utf-8') as file:
            cart_data = yaml.load(file)

        # Initialize the total quantity counter
        total_quantity = 0
        
        # Loop through items in the cart and count the total quantity
        if 'cart' in cart_data and 'items' in cart_data['cart']:
            for item in cart_data['cart']['items']:
                quantity = item.get('Quantity', 0)  # Assuming 'quantity' is the key
                total_quantity += int(quantity)

        # Update the cart label text with the current total items and quantity
        canvas.itemconfig(cart_label, text=f"Items on cart:  {total_quantity}")
        # Schedule the function to run again after 1 seconds
        window.after(1000, count_items_in_cart)
    except FileNotFoundError:
        # If cart file is not found or empty, schedule the function to run again after 1 seconds
        window.after(1000, count_items_in_cart)

# Products
def castoria():
    script_path = "Scripts/product_frames/authentic_castoria.pyw"
    subprocess.Popen(['pythonw', script_path], startupinfo=subprocess.STARTUPINFO())
def ahri():
    script_path = "Scripts/product_frames/authentic_ahri.pyw"
    subprocess.Popen(['pythonw', script_path], startupinfo=subprocess.STARTUPINFO())
def chainsaw():
    script_path = "Scripts/product_frames/authentic_chainsaw.pyw"
    subprocess.Popen(['pythonw', script_path], startupinfo=subprocess.STARTUPINFO())
def saitama():
    script_path = "Scripts/product_frames/authentic_saitama.pyw"
    subprocess.Popen(['pythonw', script_path], startupinfo=subprocess.STARTUPINFO())

window = Tk()
window.geometry("1143x619")
window.configure(bg = "#FFFFFF")
window.title(type)

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
    subprocess.Popen(['pythonw', script_path], startupinfo=subprocess.STARTUPINFO())
window.bind("<Return>", checkout_script)
window.bind("<BackSpace>", remove_script)

canvas = Canvas(window, bg = "#FFFFFF", height = 619, width = 1143, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0, 0.0, 1143.0, 619.3824462890625, fill="#FFFFFF", outline="")

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image( 570.0, 60.0, image=image_image_1)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(571.0, 365.0, image=image_image_2)
image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(571.0, 396.0, image=image_image_3)
image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(145.9810791015625, 60.89190673828125, image=image_image_4)

# Product 1 (Castoria)
castoria_img = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=castoria_img, borderwidth=0, highlightthickness=0, command=castoria, relief="flat")
button_1.place(x=43.0, y=220.0, width=245.59054565429688, height=352.1675720214844)
button_hover_1 = load_and_resize_image("Assets/authentic_frame/button_1.png", scale_factor)
def button_1_hover(e):
    button_1.config(
        image=button_hover_1
    )
def button_1_leave(e):
    button_1.config(
        image=castoria_img
    )
button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)

# Product 2 (Ahri)
ahri_img = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=ahri_img, borderwidth=0, highlightthickness=0, command=ahri, relief="flat")
button_2.place(x=314.0, y=220.0, width=245.59054565429688, height=352.1675720214844)
button_hover_2 = load_and_resize_image("Assets/authentic_frame/button_2.png", scale_factor)
def button_2_hover(e):
    button_2.config(
        image=button_hover_2
    )
def button_2_leave(e):
    button_2.config(
        image=ahri_img
    )
button_2.bind('<Enter>', button_2_hover)
button_2.bind('<Leave>', button_2_leave)

# Product 3 (Chainsaw man)
chainsaw_img = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=chainsaw_img, borderwidth=0, highlightthickness=0, command=chainsaw, relief="flat")
button_3.place(x=585.0, y=220.0, width=245.59054565429688, height=352.1675720214844)
button_hover_3 = load_and_resize_image("Assets/authentic_frame/button_3.png", scale_factor)
def button_3_hover(e):
    button_3.config(
        image=button_hover_3
    )
def button_3_leave(e):
    button_3.config(
        image=chainsaw_img
    )
button_3.bind('<Enter>', button_3_hover)
button_3.bind('<Leave>', button_3_leave)

# Product 4 (saitama)
saitama_img = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=saitama_img, borderwidth=0, highlightthickness=0, command=saitama, relief="flat")
button_4.place(x=856.0, y=220.0, width=245.59054565429688, height=352.1675720214844)
button_hover_4 = load_and_resize_image("Assets/authentic_frame/button_4.png", scale_factor)
def button_4_hover(e):
    button_4.config(
        image=button_hover_4
    )
def button_4_leave(e):
    button_4.config(
        image=saitama_img
    )
button_4.bind('<Enter>', button_4_hover)
button_4.bind('<Leave>', button_4_leave)

# Cart
image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(990.0, 60.0,image=image_image_5)
cart_label = canvas.create_text(937.0, 47.0, anchor="nw",
                   text="Items on cart:", fill="#FFFFFF", font=("Montserrat SemiBold", 16 * -1))
canvas.create_text(1059.0, 47.0, anchor="nw",
                   text=count_items_in_cart(), fill="#FFFFFF", font=("Montserrat SemiBold", 16 * -1))
image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(914.0, 60.0, image=image_image_6)

image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(572.0, 64.0, image=image_image_7)

image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(571.0, 61.0, image=image_image_8)

canvas.create_text(487.0, 36.0, anchor="nw",
                   text=textheader, fill="#FFFFFF", font=("Montserrat SemiBold", 32 * -1))
icon(window)
window.resizable(False, False)
window.mainloop()
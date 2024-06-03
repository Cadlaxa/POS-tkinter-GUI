
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
ASSETS_PATH = OUTPUT_PATH / P(r"Assets/products/authentic_castoria")
ACCOUNTS_DIR = P('./Accounts')
ACCOUNTS_DIR.mkdir(exist_ok=True)
CART_FILE = ACCOUNTS_DIR / 'cart.yaml'
ICON = P('./Assets/logour.png')
yaml = YAML()

Product = "Fate Grand Order: Caster/Altria Caster (3rd Ascension)"

# Remove the commas and convert to an integer kasi mag e-error sya
brand_new = 10345
pre_owned = 9310

no_box = -200
box_price = 200
clampshell_price = 300

def relative_to_assets(path: str) -> P:
    return ASSETS_PATH / P(path)

def icon(window):
    img = PhotoImage(file=ICON)
    window.tk.call('wm', 'iconphoto', window._w, img)

# Function to write data to a YAML file
def write_to_yaml(data):
    yaml = YAML()
    with open(CART_FILE, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

def remove_items_on_cart():
    def load_cart_items(tree):
        try:
            with open(CART_FILE, 'r', encoding='utf-8') as file:
                cart_data = yaml.load(file)
            # Clear existing items in treeview
            tree.delete(*tree.get_children())
            # Populate treeview with items from cart
            if 'cart' in cart_data and 'items' in cart_data['cart']:
                for item in cart_data['cart']['items']:
                    name = item.get('Name', '')
                    price = item.get('Item Price (Brand New)', '')
                    quantity = item.get('quantity', '')
                    tree.insert('', 'end', values=(name, price, quantity))
        except FileNotFoundError:
            print("Cart file not found.")

    def remove_selected_item(tree):
        selected_item = tree.selection()
        if selected_item:
            # Remove selected item from treeview
            tree.delete(selected_item)
            update_cart_file(tree)

    def update_cart_file(tree):
        cart_data = {'cart': {'items': []}}
        for item in tree.get_children():
            name, price, quantity = tree.item(item, 'values')
            cart_data['cart']['items'].append({'Name': name, 'Item Price (Brand New)': price, 'quantity': quantity})
        with open(CART_FILE, 'w', encoding='utf-8') as file:
            yaml.dump(cart_data, file)

    def remove_item_window():
        remove_window = tk.Toplevel()
        remove_window.title("Remove Item/s")
        # Add treeview to display selected item
        remove_tree = ttk.Treeview(remove_window, columns=('Name', 'Price', 'Quantity'), show='headings')
        remove_tree.heading('Name', text='Name')
        remove_tree.heading('Price', text='Price (Brand New)')
        remove_tree.heading('Quantity', text='Quantity')
        remove_tree.pack()
        # Load items from cart into the treeview
        load_cart_items(remove_tree)
        # Button to remove selected item
        remove_button = Button(remove_window, text="Remove Item/s", bg="#31F5C2", font=("Montserrat ExtraBold", 10), command=lambda: remove_selected_item(remove_tree))
        remove_button.pack()
        icon(remove_window)
    remove_item_window()

# Command function for the "Buy brand new" button
def buy_brand_new():
    def add_to_cart(quantity, packaging_type):
        if packaging_type == 0:  # No box
            total_price = brand_new + no_box
        elif packaging_type == 1:  # Box
            total_price = brand_new + box_price
        elif packaging_type == 2:  # Clampshell
            total_price = brand_new + clampshell_price
        data = {
            'cart': {
                'items': [
                    {'Name': Product, 'Item Price (Brand New)': f'₱{brand_new}', 'Total Price (with or w/o box)': f'₱{total_price * quantity}', 'quantity': quantity}
                ]
            }
        }
        write_to_yaml(data)
        messagebox.showinfo("Item Added", f"{quantity}x Brand new Figure added to cart")

    def update_quantity(change):
        nonlocal quantity
        quantity += change
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, str(quantity))

    def confirm_quantity():
        quantity = int(quantity_entry.get())
        packaging_type = packaging_var.get()
        add_to_cart(quantity, packaging_type)
        quantity_window.destroy()

    quantity = 1
    quantity_window = tk.Toplevel()
    quantity_window.title("Add Quantity")

    center_frame = ttk.Frame(quantity_window)
    center_frame.grid(row=0, column=0, padx=10, pady=10)

    instruction_label = ttk.Label(center_frame, text="Enter quantity:", font=("Montserrat SemiBold", 10))
    instruction_label.grid(row=0, column=0, padx=5)

    quantity_entry = Entry(center_frame, width=15, font=("Montserrat SemiBold", 10))
    quantity_entry.insert(0, str(quantity))
    quantity_entry.grid(row=0, column=1, padx=5)

    plus_button = Button(center_frame, text="+", command=lambda: update_quantity(1), bg="#31F5C2", font=("Montserrat ExtraBold", 10))
    plus_button.grid(row=0, column=3, padx=10, sticky="we")

    minus_button = Button(center_frame, text="-", command=lambda: update_quantity(-1), bg="#31F5C2", font=("Montserrat ExtraBold", 10))
    minus_button.grid(row=0, column=2, sticky="we")

    confirm_button = Button(center_frame, text="Confirm", command=confirm_quantity, bg="#FFD166", font=("Montserrat ExtraBold", 10))
    confirm_button.grid(row=1, column=0, columnspan=4, pady=(20,5), sticky="we")

    # Create a frame for the radio buttons
    radio_frame = ttk.Frame(center_frame)
    radio_frame.grid(row=2, column=0, columnspan=4, pady=(5,0))

    # Define IntVar to hold the selected packaging type
    packaging_var = tk.IntVar()
    packaging_var.set(0) 

    # Radio buttons for packaging type
    ttk.Radiobutton(radio_frame, text="No box (-₱200 on base price)", variable=packaging_var, value=0).grid(row=0, column=0, padx=10)
    ttk.Radiobutton(radio_frame, text="Box (+₱200)", variable=packaging_var, value=1).grid(row=0, column=1, padx=10)
    ttk.Radiobutton(radio_frame, text="Clampshell (+₱300)", variable=packaging_var, value=2).grid(row=0, column=2, padx=10)
    icon(quantity_window)

window = Tk()
window.geometry("1148x622")
window.configure(bg = "#FFFFFF")
window.title(Product)

canvas = Canvas(window,bg = "#FFFFFF", height = 622, width = 1148, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0, 0.0, 1148.4010009765625, 622.3092041015625, fill="#FFFFFF", outline="")

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image( 571.3822021484375, 361.59954833984375, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(571.0, 61.0, image=image_image_2)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(145.990478515625, 61.44598388671875, image=image_image_3)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(189.66064453125, 362.67041015625, image=image_image_4)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(190.971923828125, 344.98175048828125, image=image_image_5)

image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(537.0, 242.0, image=image_image_6)

image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(537.0, 474.0, image=image_image_7)

# Remove Item on Cart
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0,
    command=remove_items_on_cart, relief="flat")
button_1.place(x=694.0, y=35.69354248046875, width=220.06515502929688, height=51.21247863769531)
button_image_hover_1 = PhotoImage(file=relative_to_assets("button_hover_1.png"))
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

# Check Out
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_2 clicked"), relief="flat")
button_2.place(x=929.583984375, y=35.69354248046875, width=180.01962280273438, height=51.21247863769531)
button_image_hover_2 = PhotoImage( file=relative_to_assets("button_hover_2.png"))
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

# Buy brand new
button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=button_image_3, borderwidth=0, highlightthickness=0, command=buy_brand_new, relief="flat")
button_3.place(x=745.0, y=527.0, width=170.00001525878906,height=39.08679962158203)

# Buy pre-owned
button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=button_image_4, borderwidth=0,highlightthickness=0,
    command=lambda: print("button_4 clicked"), relief="flat")
button_4.place(x=923.0, y=527.0, width=171.0, height=39.08679962158203)

image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(919.0, 363.0, image=image_image_8)

icon(window)
window.resizable(False, False)
window.mainloop()
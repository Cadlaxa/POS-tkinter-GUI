from pathlib import Path as P

# from tkinter import *
# Explicit imports to satisfy Flake8
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, ttk
from ruamel.yaml import YAML
import subprocess
from PIL import Image, ImageTk

OUTPUT_PATH = P().parent
ASSETS_PATH = OUTPUT_PATH / P(r"Assets/products/cartoon_anna")
ACCOUNTS_DIR = P('./Accounts')
ACCOUNTS_DIR.mkdir(exist_ok=True)
CART_FILE = ACCOUNTS_DIR / 'cart.yaml'
ICON = P('./Assets/logour.png')
yaml = YAML()

Product = "Anna of Arendelle: A Frozen Adventure Solo Figurine"

# Remove the commas and convert to an integer kasi mag e-error sya
brand_new = 9750
pre_owned = 5999

no_box = -200
box_price = 200
clampshell_price = 300

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

# Function to write data to a YAML file
def write_to_yaml(data):
    yaml = YAML()
    with open(CART_FILE, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

def checkout_script():
    script_path = "Scripts/checkout.pyw"
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup_info.wShowWindow = subprocess.SW_HIDE
    try:
        subprocess.Popen(['python', script_path], startupinfo=startup_info)
    except Exception as e:
        print("Error executing checkout script:", e)

def remove_item_script():
        script_path = "Scripts/remove_items.pyw"
        subprocess.Popen(['pythonw', script_path], startupinfo=subprocess.STARTUPINFO())


# Command function for the "Buy brand new/Pre-owned" button
def load_cart_items(tree):
    try:
        with open(CART_FILE, 'r', encoding='utf-8') as file:
            cart_data = yaml.load(file)

        # Clear existing items in treeview
        tree.delete(*tree.get_children())

        # Populate treeview with items from cart
        if 'cart' in cart_data and 'items' in cart_data['cart']:
            for idx, item in enumerate(cart_data['cart']['items'], start=1):
                name = item.get('Name', '')
                product_type = item.get('Product Type', 'Unknown')
                packaging = item.get('Packaging', '')
                quantity = item.get('Item Instance', 1)
                quantity1 = item.get('Quantity', 1)
                tree.insert('', 'end', values=(name, product_type, packaging, quantity, quantity1))
    except FileNotFoundError:
        print("Cart file not found.")
        return

def remove_last_item(tree):
    try:
        with open(CART_FILE, 'r', encoding='utf-8') as file:
            cart_data = yaml.load(file)

        if 'cart' in cart_data and 'items' in cart_data['cart'] and cart_data['cart']['items']:
            # Remove the last item from the cart
            cart_data['cart']['items'].pop()

            # Update the YAML file
            write_to_yaml(cart_data)

            # Reload the treeview
            load_cart_items(tree)
    except FileNotFoundError:
        print("Cart file not found.")
        return

def update_last_quantity(change, tree):
    try:
        with open(CART_FILE, 'r', encoding='utf-8') as file:
            cart_data = yaml.load(file)

        if 'cart' in cart_data and 'items' in cart_data['cart'] and cart_data['cart']['items']:
            last_item = cart_data['cart']['items'][-1]
            last_item['Item Instance'] += change
            if last_item['Item Instance'] < 1:
                last_item['Item Instance'] = 1  # Prevent quantity from going below 1
            if last_item['Quantity'] < 1:
                last_item['Quantity'] = 1
            # Update the YAML file
            write_to_yaml(cart_data)

            # Reload the treeview
            load_cart_items(tree)
    except FileNotFoundError:
        print("Cart file not found.")
        return

def buy_product(is_brand_new):
    packaging_options = {
        0: "No box",
        1: "Boxed",
        2: "Clampshell"
    }
    def add_to_cart(quantity, packaging_type):
        product_type = 'Brand New' if is_brand_new else 'Pre-owned'
        if is_brand_new:
            base_price = brand_new
            product_type = "Brand New"
        else:
            base_price = pre_owned
            product_type = "Pre-Owned"

        if packaging_type == 0:  # No box
            packaging_price = no_box
        elif packaging_type == 1:  # Box
            packaging_price = box_price
        elif packaging_type == 2:  # Clampshell
            packaging_price = clampshell_price

        cart_data = {'cart': {'items': []}}
        if CART_FILE.exists():
            with open(CART_FILE, 'r', encoding='utf-8') as file:
                cart_data = yaml.load(file)

        # Check if the item already exists in the cart
        item_exists = False
        for item in cart_data['cart']['items']:
            if item['Name'] == Product and item['Product Type'] == product_type and item['Packaging'] == packaging_options[packaging_type]:
                # Item already exists, update its quantity
                item['Quantity'] += 1
                item_exists = True
                break

        if not item_exists:
            # Item doesn't exist, initialize quantity_add to 1
            quantity_add = 1
            # Check if the item already exists in the cart and update quantity_add accordingly
            for item in cart_data['cart']['items']:
                if item['Name'] == Product and item['Product Type'] == product_type and item['Packaging'] == packaging_options[packaging_type]:
                    quantity_add = item['Quantity'] + 1
                    break
            total_price = (base_price + packaging_price) * quantity_add
            
            # Append the item to the cart with the updated quantity_add
            cart_data['cart']['items'].append({
                'Name': Product,
                'Product Type': product_type,
                'Item Price': f'₱{base_price}',
                'Packaging': packaging_options[packaging_type],
                'Total Price (with or w/o box)': f'₱{total_price}',
                'Item Instance': 1,
                'Quantity': quantity_add
            })
        else:
            # Item exists, update its quantity and total price
            for item in cart_data['cart']['items']:
                if item['Name'] == Product and item['Product Type'] == product_type and item['Packaging'] == packaging_options[packaging_type]:
                    item['Total Price (with or w/o box)'] = f'₱{(base_price + packaging_price) * item["Quantity"]}'
                    break
                
        write_to_yaml(cart_data)
        load_cart_items(tree)

    def update_quantity(change):
        nonlocal quantity
        quantity += change
        if quantity < 1:
            quantity = 0
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, str(quantity))
        if change > 0:
            add_to_cart(quantity, packaging_var.get())
        else:
            remove_last_item(tree)

    def on_packaging_change():
        update_quantity(1)
    
    def confirm_and_notify():
        message = f"Added {quantity} item(s) of {Product} with {packaging_options[packaging_var.get()]} packaging to the cart."
        messagebox.showinfo("Item Added", message)
        quantity_window.destroy()

    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, item['values'][4])

    quantity = 0
    quantity_window = tk.Toplevel()
    quantity_window.title("Add Quantity")
    quantity_window.grid_columnconfigure(0, weight=1)

    center_frame = ttk.Frame(quantity_window)
    center_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    center_frame.grid_columnconfigure(0, weight=1)

    instruction_label = ttk.Label(center_frame, text="Enter quantity:", font=("Montserrat SemiBold", 10))
    instruction_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    quantity_entry = tk.Entry(center_frame, width=15, font=("Montserrat SemiBold", 10))
    quantity_entry.insert(0, str(quantity))
    quantity_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

    plus_button = tk.Button(center_frame, text="  +  ", command=lambda: update_quantity(1), bg="#31F5C2", font=("Montserrat ExtraBold", 10))
    plus_button.grid(row=0, column=3, padx=5, pady=5, sticky="we")

    minus_button = tk.Button(center_frame, text="  -  ", command=lambda: update_quantity(-1), bg="#31F5C2", font=("Montserrat ExtraBold", 10))
    minus_button.grid(row=0, column=2, padx=5, pady=5, sticky="we")

    remove_button = tk.Button(center_frame, text="Remove Last Item", command=lambda: update_quantity(-1), bg="#FF6347", font=("Montserrat ExtraBold", 10))
    remove_button.grid(row=1, column=0, columnspan=4, pady=(10, 5), padx=5, sticky="we")

    confirm_button = tk.Button(center_frame, text="Confirm", command=confirm_and_notify, bg="#FFD166", font=("Montserrat ExtraBold", 10))
    confirm_button.grid(row=2, column=0, columnspan=4, pady=(10, 5), padx=5, sticky="we")

    # Create a frame for the radio buttons
    radio_frame = ttk.Frame(center_frame)
    radio_frame.grid(row=3, column=0, columnspan=4, pady=(5,0))

    # Define IntVar to hold the selected packaging type
    packaging_var = tk.IntVar()
    packaging_var.set(1)  # Set "box" as default

    # Radio buttons for packaging type
    ttk.Radiobutton(radio_frame, text="No box (-₱200 on base price)", variable=packaging_var, value=0, command=on_packaging_change).grid(row=0, column=0, padx=10)
    ttk.Radiobutton(radio_frame, text="Boxed (+₱200)", variable=packaging_var, value=1, command=on_packaging_change).grid(row=0, column=1, padx=10)
    ttk.Radiobutton(radio_frame, text="Clampshell (+₱300)", variable=packaging_var, value=2, command=on_packaging_change).grid(row=0, column=2, padx=10)

    # Create Treeview to display items
    tree = ttk.Treeview(quantity_window, columns=('Name', 'Product Type', 'Packaging', 'Item Instance', 'Quantity'), show='headings')
    tree.heading('Name', text='Item Name')
    tree.heading('Product Type', text='Product Type')
    tree.heading('Packaging', text='Package Type')
    tree.heading('Item Instance', text='Item Instance')
    tree.heading('Quantity', text='Quantity')
    tree.column('Name', width=290, anchor='w')
    tree.column('Product Type', width=80, anchor='c')
    tree.column('Packaging', width=80, anchor='c')
    tree.column('Item Instance', width=80, anchor='c')
    tree.column('Quantity', width=80, anchor='c')
    tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
    tree.bind('<<TreeviewSelect>>', on_tree_select)

    load_cart_items(tree)
    icon(quantity_window)

window = Tk()
window.geometry("1148x622")
window.configure(bg = "#FFFFFF")
window.title(Product)

# Checkout and Remove Items keyboard shortcut
def checkout_script_key(event):
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
window.bind("<Return>", checkout_script_key)
window.bind("<BackSpace>", remove_script)

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

# Product Images
image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(190.971923828125, 344.98175048828125, image=image_image_5)

image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(537.0, 242.0, image=image_image_6)

image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(537.0, 474.0, image=image_image_7)

# Remove Item on Cart
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0,
    command=remove_item_script, relief="flat")
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
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=checkout_script, relief="flat")
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
button_3 = Button(image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: buy_product(True), relief="flat")
button_3.place(x=745.0, y=527.0, width=170.00001525878906,height=39.08679962158203)

# Buy pre-owned
button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=button_image_4, borderwidth=0,highlightthickness=0,
    command=lambda: buy_product(False), relief="flat")
button_4.place(x=923.0, y=527.0, width=171.0, height=39.08679962158203)

image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(919.0, 363.0, image=image_image_8)

icon(window)
window.resizable(False, False)
window.mainloop()
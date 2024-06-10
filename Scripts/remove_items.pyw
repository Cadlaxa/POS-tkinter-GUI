from pathlib import Path as P
import tkinter as tk
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox, ttk, Entry, filedialog
from ruamel.yaml import YAML
from PIL import Image, ImageTk
import subprocess

OUTPUT_PATH = P().parent
ACCOUNTS_DIR = P('./Accounts')
ACCOUNTS_DIR.mkdir(exist_ok=True)
CART_FILE = ACCOUNTS_DIR / 'cart.yaml'
ICON = P('./Assets/logour.png')
yaml = YAML()
title = "Remove Item/s"

def icon(window):
    img = PhotoImage(file=ICON)
    window.tk.call('wm', 'iconphoto', window._w, img)

window = Tk()
window.title(title)

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
                product_type = item.get('Product Type', '')
                price = item.get('Item Price', '')
                price1 = item.get('Total Price (with or w/o box)', '')
                packaging = item.get('Packaging', '')
                instance = item.get('Item Instance', '')
                quantity = item.get('Quantity', '')
                tree.insert('', 'end', values=(name, product_type, packaging, price, price1, instance ,quantity))
    except FileNotFoundError:
        print("Cart file not found.")

def remove_selected_item(tree):
    selected_items = tree.selection()
    if selected_items:
        for item in selected_items:
            tree.delete(item)
        update_cart_file(tree)

def update_cart_file(tree):
    cart_data = {'cart': {'items': []}}
    for item in tree.get_children():
        name, product_type, packaging, price, price1, instance, quantity = tree.item(item, 'values')
        cart_data['cart']['items'].append({
            'Name': name,
            'Product Type': product_type,
            'Item Price': price,
            'Packaging': packaging,
            'Total Price (with or w/o box)': price1,
            'Item Instance': instance,
            'Quantity': quantity
        })
    with open(CART_FILE, 'w', encoding='utf-8') as file:
        yaml.dump(cart_data, file)

def remove_item_window():
    # Add treeview to display selected item
    remove_tree = ttk.Treeview(window, columns=('Name', 'Product Type', 'Packaging', 'Price', 'Total Price', 'Item Instance', 'Quantity'), show='headings')
    remove_tree.heading('Name', text='Name')
    remove_tree.heading('Product Type', text='Product Type')
    remove_tree.heading('Packaging', text='Packaging Type')
    remove_tree.heading('Price', text='Price')
    remove_tree.heading('Total Price', text='Total Price')
    remove_tree.heading('Item Instance', text='Item Instance')
    remove_tree.heading('Quantity', text='Quantity')
    remove_tree.column('Name', width=300, anchor='w')
    remove_tree.column('Product Type', width=100, anchor='w')
    remove_tree.column('Price', width=80, anchor='c')
    remove_tree.column('Total Price', width=80, anchor='c')
    remove_tree.column('Packaging', width=120, anchor='c')
    remove_tree.column('Item Instance', width=80, anchor='c')
    remove_tree.column('Quantity', width=80, anchor='c')
    remove_tree.pack(fill='both')
    # Load items from cart into the treeview
    load_cart_items(remove_tree)
    # Button to remove selected item
    remove_button = Button(window, text="Remove Item/s", bg="#31F5C2", font=("Montserrat ExtraBold", 10), command=lambda: remove_selected_item(remove_tree))
    remove_button.pack(fill='x')
remove_item_window()

window.bind("<Escape>", quit)
icon(window)
window.mainloop()

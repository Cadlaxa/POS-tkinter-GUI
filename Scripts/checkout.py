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
title = "Checkout Items"

def icon(window):
    img = PhotoImage(file=ICON)
    window.tk.call('wm', 'iconphoto', window._w, img)

window = Tk()
window.title(title)

def load_cart_items(tree):
    try:
        with open(CART_FILE, 'r', encoding='utf-8') as file:
            cart_data = yaml.load(file) or {}

        # Clear existing items in treeview
        tree.delete(*tree.get_children())

        # Populate treeview with items from cart
        if 'cart' in cart_data and 'items' in cart_data['cart']:
            for item in cart_data['cart']['items']:
                name = item.get('Name', '')
                price = item.get('Item Price', '')
                packaging = item.get('Packaging', '')
                total_price = item.get('Total Price (with or w/o box)', '')
                quantity = item.get('quantity', '')
                tree.insert('', 'end', values=(name, price, packaging, total_price, quantity))
    except FileNotFoundError:
        print("Cart file not found.")
        return
    except Exception as e:
        print(f"Error loading cart items: {e}")
        return



# Add treeview to display cart items
checkout_tree = ttk.Treeview(window, columns=('Name', 'Price', 'Packaging', 'Total Price', 'Quantity'), show='headings')
checkout_tree.heading('Name', text='Name')
checkout_tree.heading('Price', text='Price')
checkout_tree.heading('Total Price', text='Total Price')
checkout_tree.heading('Packaging', text='Packaging')
checkout_tree.heading('Quantity', text='Quantity')
checkout_tree.column('Name', width=300, anchor='w')
checkout_tree.column('Price', width=80, anchor='c')
checkout_tree.column('Total Price', width=80, anchor='c')
checkout_tree.column('Packaging', width=120, anchor='c')
checkout_tree.column('Quantity', width=60, anchor='c')
checkout_tree.pack()

# Payment entry
payment_label = ttk.Label(window, text="Enter payment amount:", font=("Montserrat SemiBold", 10))
payment_label.pack()
payment_entry = Entry(window, font=("Montserrat SemiBold", 10))
payment_entry.pack()

# Total price label
total_price_label = ttk.Label(window, text="Total Price: ₱0.00", font=("Montserrat SemiBold", 10))
total_price_label.pack()

def update_total_price(tree):
    total_price = 0.0
    for item in tree.get_children():
        price_str = tree.item(item, 'values')[3]  # Extract total price string
        price_str = price_str.replace('₱', '')  # Remove peso sign
        total_price += float(price_str)
    total_price_label.config(text=f"Total Price: ₱{total_price:.2f}")
# Load cart items into treeview
load_cart_items(checkout_tree)
update_total_price(checkout_tree)  # Update total price label

# Amount paid label
amount_paid_label = ttk.Label(window, text="Amount Paid: ₱0.00", font=("Montserrat SemiBold", 10))
amount_paid_label.pack()

def update_payment_status(payment_amount, total_price):
    if payment_amount >= total_price:
        receipt_button.config(state=tk.NORMAL)
    else:
        receipt_button.config(state=tk.DISABLED)

def print_receipt(tree):
    receipt_text = "Receipt:\n\n"
    for item in tree.get_children():
        name, price, packaging, total_price, quantity = tree.item(item, 'values')
        receipt_text += f"Name: {name}\nPrice: {price}\nPackaging: {packaging}\nTotal Price: {total_price}\nQuantity: {quantity}\n\n"

    # Ask user to select a file location
    file_path = filedialog.asksaveasfilename(initialfile="receipt.txt", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        # Save receipt to a UTF-8 encoded text file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(receipt_text)
        messagebox.showinfo("Receipt Saved", f"The receipt has been saved to:\n{file_path}")

def add_amount():
    try:
        amount_to_add = float(payment_entry.get())
        if amount_to_add >= 0:
            current_amount = float(amount_paid_label.cget("text").replace("Amount Paid: ₱", "").replace(",", ""))
            updated_amount = current_amount + amount_to_add
            amount_paid_label.config(text=f"Amount Paid: ₱{updated_amount:.2f}")
        else:
            raise ValueError("Negative amount not allowed.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount to add.")

def confirm_purchase():
    try:
        payment_amount = float(payment_entry.get())
        total_price_str = total_price_label.cget("text").replace("Total Price: ₱", "")
        total_price = float(total_price_str.replace(",", ""))  # Remove comma if present
        if payment_amount >= 0:
            amount_paid_label.config(text=f"Amount Paid: ₱{payment_amount:.2f}")
            update_payment_status(payment_amount, total_price)
        else:
            raise ValueError("Negative amount not allowed.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid payment amount.")
        
    current_amount = float(amount_paid_label.cget("text").replace("Amount Paid: ₱", "").replace(",", ""))
    if current_amount >= total_price:
        save_receipt = messagebox.askyesno("Save Receipt", "Purchase successful. Do you want to save the receipt?")
        if save_receipt:
            print_receipt(checkout_tree)
        else:
            messagebox.showinfo("Purchase Confirmed", "Purchase confirmed. Receipt not saved.")
        
        # Close the window
        window.destroy()
        
        # Clear the YAML file contents
        try:
            with open(CART_FILE, 'w', encoding='utf-8') as file:
                yaml.dump({}, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear cart file: {e}")
    else:
        messagebox.showerror("Insufficient Payment", "Please complete the payment before confirming the purchase.")

# Create a frame for buttons and place them at the bottom
button_frame = ttk.Frame(window)
button_frame.pack(side=tk.BOTTOM, pady=20)

# Button to add amount
add_amount_button = Button(button_frame, text="Add Amount", command=add_amount, bg="#FFD166", font=("Montserrat ExtraBold", 10))
add_amount_button.pack(side=tk.LEFT, padx=10)

# Button to confirm purchase
confirm_purchase_button = Button(button_frame, text="Confirm Purchase", command=confirm_purchase, bg="#31F5C2", font=("Montserrat ExtraBold", 10))
confirm_purchase_button.pack(side=tk.RIGHT, padx=10)

# Button to save receipt
receipt_button = Button(button_frame, text="Save Receipt", command=lambda: print_receipt(checkout_tree), bg="#FFD166", font=("Montserrat ExtraBold", 10))
receipt_button.pack(side=tk.LEFT, padx=10)
receipt_button.config(state=tk.DISABLED)  # Disable save receipt button initially

icon(window)
window.mainloop()


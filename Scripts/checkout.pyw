from pathlib import Path as P
import tkinter as tk
from tkinter import Tk, Entry, Button, PhotoImage, messagebox, ttk, filedialog
import datetime
from ruamel.yaml import YAML
from PIL import Image, ImageTk
import qrcode
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import socket
import re
import http.server
import socketserver
import webbrowser
import os

OUTPUT_PATH = P().parent
ACCOUNTS_DIR = P('./Accounts')
ACCOUNTS_DIR.mkdir(exist_ok=True)
CART_FILE = ACCOUNTS_DIR / 'cart.yaml'
ACCOUNTS_FILE = ACCOUNTS_DIR / 'users.yaml'
ICON = P('./Assets/logour.png')
yaml = YAML()
title = "Checkout Items"
tax_value = 0.010


#payment_link = 'http://192.168.1.1:5500/payment.html'

# Function to get the local IP address (IP address of the connected Wi-Fi)
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 1))  # doesn't have to be reachable
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error fetching local IP: {e}")
        return None

# Function to generate payment link using public IP address
def generate_payment_link():
    ip_address = get_local_ip()
    if ip_address:
        payment_link = f'http://{ip_address}:5500/payment.html'
        return payment_link
    else:
        return None

# Function to generate payment link using local IP address
def generate_host_link():
    local_ip = get_local_ip()
    if local_ip:
        host_link = local_ip
        return host_link
    else:
        return None

def update_post_url_in_html(html_file_path, payment_link):
    try:
        with open(html_file_path, 'r') as file:
            html_content = file.read()
        updated_html_content = re.sub(r'http://[a-zA-Z0-9.-]+(:[0-9]+)?/payment.html', payment_link, html_content)
        with open(html_file_path, 'w') as file:
            file.write(updated_html_content)
        print("POST URL in HTML file updated successfully.")
    except FileNotFoundError:
        print("HTML file not found.")
    except Exception as e:
        print("Error:", e)

# Usage
payment_link = generate_payment_link()
html_file_path = 'payment.html'
update_post_url_in_html(html_file_path, payment_link)
if payment_link:
    print(f"Payment link: {payment_link}")
else:
    print("Failed to generate payment link.")

host_num = generate_host_link()

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
                ptype = item.get('Product Type', '')
                price = item.get('Item Price', '')
                packaging = item.get('Packaging', '')
                total_price = item.get('Total Price (with or w/o box)', '')
                quantity = item.get('Quantity', '')
                tree.insert('', 'end', values=(name, ptype, price, packaging, total_price, quantity))
    except FileNotFoundError:
        print("Cart file not found.")
        return
    except Exception as e:
        print(f"Error loading cart items: {e}")
        return

# Add treeview to display cart items
checkout_tree = ttk.Treeview(window, columns=('Name', 'Product Type', 'Price', 'Packaging', 'Total Price', 'Quantity'), show='headings')
checkout_tree.heading('Name', text='Name')
checkout_tree.heading('Product Type', text='Product Type')
checkout_tree.heading('Price', text='Price')
checkout_tree.heading('Total Price', text='Total Price')
checkout_tree.heading('Packaging', text='Packaging')
checkout_tree.heading('Quantity', text='Quantity')
checkout_tree.column('Name', width=300, anchor='w')
checkout_tree.column('Product Type', width=80, anchor='c')
checkout_tree.column('Price', width=80, anchor='c')
checkout_tree.column('Total Price', width=120, anchor='c')
checkout_tree.column('Packaging', width=80, anchor='c')
checkout_tree.column('Quantity', width=60, anchor='c')
checkout_tree.pack()

# Payment entry
payment_label = ttk.Label(window, text="Enter payment amount:", font=("Montserrat SemiBold", 10))
payment_label.pack()
payment_entry = Entry(window, font=("Montserrat SemiBold", 10))
payment_entry.pack()

# Total price label
total_price_label = ttk.Label(window, text="Total Price (Tax Included): ₱0.00", font=("Montserrat SemiBold", 10))
total_price_label.pack()

def update_total_price(tree):
    total_price = 0.0
    for item in tree.get_children():
        total_price_str = tree.item(item, 'values')[4]  # Extract total price string
        total_price_str = total_price_str.replace('₱', '').replace(',', '')
        total_price += float(total_price_str)
    # Calculate tax
    tax = total_price * tax_value
    # Add tax to the total price
    total_price_with_tax = total_price + tax
    total_price_label.config(text=f"Total Price (Tax Included): ₱{total_price_with_tax:,.2f}")

# Load cart items into treeview
load_cart_items(checkout_tree)
update_total_price(checkout_tree)  # Update total price label

# Amount paid label
amount_paid_label = ttk.Label(window, text="Amount Paid: ₱0.00", font=("Montserrat SemiBold", 10))
amount_paid_label.pack()

def update_payment_status(payment_amount, total_price):
    amount_paid_label.config(text=f"Amount Paid: ₱{payment_amount:,.2f}")
    if payment_amount >= total_price:
        receipt_button.config(state=tk.NORMAL)
    else:
        receipt_button.config(state=tk.DISABLED)
        
def get_username_from_yaml():
    try:
        yaml = YAML()
        with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as file:
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
        user_file_path = ACCOUNTS_FILE
        with open(user_file_path, 'r', encoding='utf-8') as file:
            user_data = yaml.load(file) or {}
        print("User data loaded successfully:", user_data)
        return user_data.get(username, {})
    except FileNotFoundError:
        print(f"User '{username}' file not found in account details.")
        return {}
    except Exception as e:
        print(f"Error loading user data for '{username}': {e}")
        return {}

def print_receipt(tree, change):
    try:
        # Load account details
        user_name = get_username_from_yaml()
        user_data = load_user_data(user_name)

        if not user_data:
            print(f"User '{user_name}' not found in account details.")
            return

        if user_data.get('logged', True):
            # Use username if logged in
            name = user_name
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            fname = f"{last_name}, {first_name}"
        else:
            # Use account name if not logged in
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            name = f"{last_name}, {first_name}"

        # Get contact number from user data and validate
        contact_number = user_data.get('contact_number', '')

        address = user_data.get('address', '')

        # Validate contact number format
        if not contact_number.isdigit() or len(contact_number) != 10:
            contact_number = 'Invalid contact number'

        # Initialize receipt text with header and user details
        order_date = datetime.datetime.now().strftime("%Y-%m-%d")
        order_time = datetime.datetime.now().strftime("%H:%M:%S")
        receipt_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        receipt_text = f"""
    ------------------------------------------------------
                        Arti-San Receipt
    ------------------------------------------------------
    Order Date: {order_date}
    Order Time: {order_time}
    Receipt Number: {receipt_number}
    -----------------------------------------------------
    Order For: ({name}) {fname}
    Contact Number: {contact_number}
    Shipping Address: {address}
    ----------------------------------------------------
    Customer Contact: {contact_number}
    Phone: (8) 7-000
    Email: artisanoshop@gmail.com
    -----------------------------------------------------
          Description                      Price   
    -----------------------------------------------------
    """

        # Add item details to the receipt text
        total_package_cost = 0  # Initialize total packaging cost

        for item in tree.get_children():
            values = tree.item(item, 'values')
            if len(values) == 6:  # Ensure the correct number of values is obtained
                name, ptype, price, packaging, total_price, quantity = values  # Unpack the values

                # Adjust packaging cost based on packaging type
                if packaging == 'No box':
                    packaging_cost = -200
                elif packaging == 'Boxed':
                    packaging_cost = 200
                elif packaging == 'Clampshell':
                    packaging_cost = 300
                else:
                    packaging_cost = 0  # Default value if packaging type is not recognized

                # Accumulate packaging cost for each item type
                total_package_cost += packaging_cost * int(quantity)
                print(f"Total Packaging Cost: ₱{total_package_cost}")

                # Add item details to receipt text
                receipt_text += f"""
    Item: {name}:       Price: {price}
    Product Type: {ptype}
    Quantity: {quantity}
    Packaging Type: {packaging}
    """
        # Calculate subtotal, packaging cost, tax, and total
        # Initialize variables
        subtotal = 0.0
        total_package = 0.0
        
        # Calculate subtotal
        for item in tree.get_children():
            total_price_str = tree.item(item, 'values')[4]
            # Convert total price to float, excluding packaging cost
            subtotal += float(total_price_str.replace('₱', '').replace(',', '')) - total_package_cost
        
        total_package = total_package_cost * len(tree.get_children())
        tax = (subtotal + total_package) * tax_value
        total = subtotal + total_package + tax

        # Add subtotal, packaging cost, tax, change, and total to the receipt text
        receipt_text += f"""
    ------------------------------------------------------
    Subtotal: ₱{subtotal:,.2f}
    Total Packaging Cost: ₱{total_package:,.2f}
    Tax (10%): ₱{tax:,.2f}
    Change: ₱{change:,.2f}
    ------------------------------------------------------
    Total: ₱{total:,.2f} (including VAT)
    Payment Method: Online Payment                          
    ------------------------------------------------------
                Thank you for Choosing Arti-San!
                    Please Come Again!
    ------------------------------------------------------
    """

        # Ask user to select a file location
        file_path = filedialog.asksaveasfilename(initialfile="Arti-San Receipt.txt", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            # Save receipt to a UTF-8 encoded text file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(receipt_text)
            response = messagebox.askquestion("Receipt Saved", f"The receipt has been saved to:\n{file_path}\nDo you want to view your receipt?")
            if response == "yes":
                try:
                    # Open the file using default application
                    import os
                    os.startfile(file_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Unable to open the file: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the receipt: {e}")

def add_amount():
    try:
        amount_to_add = float(payment_entry.get())
        if amount_to_add >= 0:
            current_amount = float(amount_paid_label.cget("text").replace("Amount Paid: ₱", "").replace(",", ""))
            updated_amount = current_amount + amount_to_add
            amount_paid_label.config(text=f"Amount Paid: ₱{updated_amount:,.2f}")
            update_payment_status(updated_amount, float(total_price_label.cget("text").replace("Total Price (Tax Included): ₱", "").replace(",", "")))
        else:
            raise ValueError("Negative amount not allowed.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount to add.")

def reset_amount():
    amount_paid_label.config(text="Amount Paid: ₱0.00")
    update_payment_status(0, float(total_price_label.cget("text").replace("Total Price (Tax Included): ₱", "").replace(",", "")))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def serve_directory(directory, port=8080):
    os.chdir(directory)  # Change directory to the one you want to serve
    handler = MyHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving directory '{directory}' at http://{host_num}:{port}")
        #webbrowser.open_new_tab(f"http://{host_num}:{port}")
        httpd.serve_forever()

def start_server():
    serve_directory("\POS-tkinter-GUI")

# Call the function to start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/payment.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('payment.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        payment_info = json.loads(post_data)
        
        payment_amount = payment_info.get('total_price', 0)
        
        # Here, you can implement payment processing logic
        # For demonstration purposes, let's assume the payment is always confirmed
        payment_confirmed = True
        # Update payment status label
        update_payment_server(payment_amount)
        # Confirm the purchase
        confirm_purchase()
        
        response = {
            'payment_confirmed': payment_confirmed,
            'total_amount': payment_amount
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

def update_payment_server(payment_amount):
    try:
        payment_amount = int(payment_amount)
        amount_paid_label.config(text=f"Amount Paid: ₱{payment_amount:,.2f}")
    except ValueError:
        print("Error: Paid amount is not an integer.")


def run(server_class=HTTPServer, handler_class=RequestHandler, host=host_num, port=5500):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on {host}:{port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Server interrupted. Closing...')
        httpd.server_close()

# Define a function to start the server in a separate thread
def start_server():
    run()

# Call the function to start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True 
server_thread.start()

def display_qr_code(link):
    # Generate QR code with the payment link
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=7, border=4)
    qr.add_data(link)
    qr.make(fit=True)

    # Create image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Convert PIL Image to Tkinter PhotoImage
    qr_image_tk = ImageTk.PhotoImage(qr_image)

    # Create a new window to display the QR code
    qr_window = tk.Toplevel(window)
    qr_window.title("Payment QR Code")

    # Display the QR code on the new window
    qr_label = tk.Label(qr_window, image=qr_image_tk)
    qr_label.image = qr_image_tk
    qr_label.pack()
    icon(qr_window)

    # Close the QR window when the user closes it
    qr_window.protocol("WM_DELETE_WINDOW", qr_window.destroy)

def confirm_purchase():
    try:
        payment_amount_str = amount_paid_label.cget("text").replace("Amount Paid: ₱", "").replace(",", "")
        payment_amount = float(payment_amount_str)
        
        total_price_str = total_price_label.cget("text").replace("Total Price (Tax Included): ₱", "").replace(",", "")
        total_price = float(total_price_str)  # No need to remove commas, since float() handles it
        
        if payment_amount >= total_price:
            # Calculate change
            change = payment_amount - total_price
            
            save_receipt = messagebox.askyesno("Save Receipt", "Purchase successful. Do you want to save the receipt?")
            if save_receipt:
                print_receipt(checkout_tree, change)  # Pass change as an argument
            else:
                messagebox.showinfo("Purchase Confirmed", "Purchase confirmed. Receipt not saved.")
            
            # Clear the YAML file contents
            try:
                with open(CART_FILE, 'w', encoding='utf-8') as file:
                    cart_data = {'cart': {'items': []}}
                    yaml.dump(cart_data, file)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear cart file: {e}")
            
            # Close the window
            window.destroy()
        else:
            messagebox.showerror("Insufficient Payment", "Please complete the payment before confirming the purchase.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid payment amount.")

# Create a frame for buttons and place them at the bottom
button_frame = ttk.Frame(window)
button_frame.pack(side=tk.BOTTOM, pady=20)

# Button to add amount
add_amount_button = Button(button_frame, text="Add Amount", command=add_amount, bg="#FFD166", font=("Montserrat ExtraBold", 10))
add_amount_button.pack(side=tk.LEFT, padx=10)

# Button to reset amount
reset_amount_button = Button(button_frame, text="Reset Amount", command=reset_amount, bg="#EF476F", font=("Montserrat ExtraBold", 10))
reset_amount_button.pack(side=tk.LEFT, padx=10)

# Button to confirm purchase
confirm_purchase_button = Button(button_frame, text="Confirm Purchase", command=confirm_purchase, bg="#31F5C2", font=("Montserrat ExtraBold", 10))
confirm_purchase_button.pack(side=tk.RIGHT, padx=10)

# Button to show QR code
show_qr_button = tk.Button(button_frame, text="Pay with a device", command=lambda: display_qr_code(payment_link), bg="#46A9FF", font=("Montserrat ExtraBold", 10))
show_qr_button.pack(side=tk.LEFT, padx=10)

# Button to save receipt
receipt_button = Button(button_frame, text="Save Receipt", command=lambda: print_receipt(checkout_tree, 0), bg="#46A9FF", font=("Montserrat ExtraBold", 10))
receipt_button.pack(side=tk.LEFT, padx=10)
receipt_button.config(state=tk.DISABLED)  # Disable save receipt button initially

icon(window)
window.mainloop()
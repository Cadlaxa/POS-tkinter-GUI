import tkinter as tk
from tkinter import messagebox, ttk
from Assets.modules.sv_ttk import sv_ttk

def checkout():
    card_number = card_number_entry.get()
    card_name = card_name_entry.get()
    expiry_date = expiry_date_entry.get()
    cvv = cvv_entry.get()

    # Here you can add actual validation and processing logic
    if not card_number or not card_name or not expiry_date or not cvv:
        messagebox.showerror("Error", "All fields are required!")
    else:
        # Placeholder for processing the payment
        messagebox.showinfo("Success", "Payment processed successfully!")

# Initialize the main window
root = tk.Tk()
root.title("Checkout")
root.geometry("400x300")

# Apply the sv-ttk theme
sv_ttk.set_theme("light")

# Create and place the labels and entry fields
ttk.Label(root, text="Card Number:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
card_number_entry = ttk.Entry(root, width=30)
card_number_entry.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(root, text="Cardholder Name:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
card_name_entry = ttk.Entry(root, width=30)
card_name_entry.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(root, text="Expiry Date (MM/YY):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
expiry_date_entry = ttk.Entry(root, width=10)
expiry_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

ttk.Label(root, text="CVV:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
cvv_entry = ttk.Entry(root, width=10, show="*")
cvv_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Create and place the checkout button
checkout_button = ttk.Button(root, text="Checkout", style="Accent.TButton",command=checkout)
checkout_button.grid(row=4, column=0, columnspan=2, pady=20)

# Run the main loop
root.mainloop()

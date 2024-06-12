import subprocess
from tkinter import *
from PIL import Image, ImageTk
import time

# Create the Tkinter window
w = Tk()

# Set the dimensions and position of the window
width_of_window = 510
height_of_window = 565
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width/2) - (width_of_window/2)
y_coordinate = (screen_height/2) - (height_of_window/2)
w.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

# Load the image using PIL
original_image = Image.open("Assets/splash.png")

# Set the desired zoom factor
zoom_factor = 0.47

# Calculate new dimensions
new_width = int(original_image.width * zoom_factor)
new_height = int(original_image.height * zoom_factor)

# Resize the image
resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

# Convert the image to a format that Tkinter can use
tk_image = ImageTk.PhotoImage(resized_image)

# Create a label to display the resized image
image_label = Label(w, image=tk_image)
image_label.pack()

# Hide the title bar
w.overrideredirect(1)

# Function to open a new window and destroy the current one
def new_win():
    w.destroy()
    file_path = "Scripts/login.pyw"
    subprocess.Popen(['pythonw', file_path])

# Set a timer to open the new window after 3 seconds
w.after(3000, new_win)

# Run the Tkinter event loop
w.mainloop()
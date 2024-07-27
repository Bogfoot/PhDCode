import tkinter as tk

# Define the callback function for the button
def show_singles():
    print("Singles button pressed")

# Create the main window
root = tk.Tk()

# Define the frame and button dimensions
button_frame = tk.Frame(root)
button_frame.pack()

h = 2
w = 10

# Create the button with the correct parameters
button_singles = tk.Button(button_frame, text="Singles", command=show_singles, height=h, width=w)
button_singles.pack()

# Start the Tkinter event loop
root.mainloop()

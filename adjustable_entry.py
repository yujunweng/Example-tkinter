import tkinter as tk

def update_entry_width(event):
    new_width = event.x // 10  # Adjust the division factor to control the width scaling
    entry.config(width=new_width)
    
    if event.x <= 3 or event.x >= entry.winfo_width() - 3:
        entry.config(cursor="arrow")
    else:
        entry.config(cursor="")

# Create the main window
window = tk.Tk()

# Create an entry widget
entry = tk.Entry(window, width=10)  # Set an initial width
entry.pack()

# Bind the mouse motion event to update the width and cursor
entry.bind("<B1-Motion>", update_entry_width)

# Run the GUI main loop
window.mainloop()

import tkinter as tk

root = tk.Tk()

frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")

button = tk.Button(frame, text="Resizable Button")
button.grid(row=0, column=0, sticky="nsew")

button.rowconfigure(0, weight=1)
button.columnconfigure(0, weight=1)

frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

root.mainloop()
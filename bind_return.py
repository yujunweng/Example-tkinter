# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:57:34 2021

@author: F0027
"""

import tkinter as tk

def print_content(message):
    print(message.get())
    message.delete(0, 'end')
    

window = tk.Tk()
window.geometry('300x300')
myLabel = tk.Label(window, text='Hello World')
myLabel.pack()
message = tk.Entry(window)
message.insert(0,"Hi, what's up")
message.pack()

myButton = tk.Button(window, text='print', command=lambda:print_content(message))
myButton.pack()

window.bind('<Return>', lambda event:print_content(message))
window.mainloop()



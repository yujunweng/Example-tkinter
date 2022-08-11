import tkinter as tk
import win32gui
import win32con

root = tk.Tk()
root.title('MinimizeTest')
root.geometry('300x200')

def disable_minbox():
    # get window handle
    win_id = root.winfo_id()
    hwnd = win32gui.GetParent(win_id) 
    # get the current window style of root window
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    # mask out minimize button
    style &= ~win32con.WS_MINIMIZEBOX
    # update the window style of root window
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

# need to do it when root window is displayed
root.after(1, disable_minbox)
root.mainloop()
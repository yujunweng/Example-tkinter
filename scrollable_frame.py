import tkinter as tk
from tkinter import ttk



class VerticalScrolledFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent, gp={'side':'right'}, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient='vertical')
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)        
        if 'grid' in gp:
            canvas.grid(row=gp['grid'][0], column=gp['grid'][1], sticky='nsew')
            vscrollbar.grid(row=gp['grid'][0], column=gp['grid'][1]+4, rowspan=1, sticky='ns')            
        elif 'side' in gp: 
            canvas.pack(side='left', fill='both', expand='true')
            vscrollbar.pack(side='right', fill='y', expand='false')            
        elif 'anchor' in gp:     
            canvas.pack(anchor=gp['anchor'], fill='both', expand='true')         
            vscrollbar.pack(anchor=gp['anchor'], fill='y', expand='false')            
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor='nw')

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


if __name__ == "__main__":

    class SampleApp(tk.Tk):
        def __init__(self, *args, **kwargs):
            root = tk.Tk.__init__(self, *args, **kwargs)

            self.frame = VerticalScrolledFrame(root)
            self.frame.pack()
            self.label = ttk.Label(self, text="Shrink the window to activate the scrollbar.")
            self.label.pack()
            buttons = []
            for i in range(30):
                buttons.append(ttk.Button(self.frame.interior, text="Button " + str(i)))
                buttons[-1].pack()

    app = SampleApp()
    app.mainloop()

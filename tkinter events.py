def onFormEvent( event ):
    for key in dir( event ):
        if not key.startswith( '_' ):
            print ('%s=%s' % ( key, getattr( event, key ) ))
    print()

import tkinter as tk
root = tk.Tk()
lblText = tk.Label( root, text='Form event tester' )
lblText.pack()
root.bind( '<Configure>', onFormEvent )
root.mainloop()
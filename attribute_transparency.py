class winlog():
    """readonly modaless Toplevel log window class"""

    def __init__(self, root=None, title='Log Window', **kw):
        self.win = Toplevel(root)
        self.win.title(title)
        self.st = tklog(master=self.win, **kw)
        self.st.pack(fill='both', expand=True)
        self.win.bind('', self._focusIn)
        self.win.bind('', self._focusOut)

    def _focusIn(self, event):
        self.win.attributes('-alpha', 1.0)

    def _focusOut(self, evnet):
        self.win.attributes('-alpha', 0.6)

    def log(self, content, end='\n'):
        self.st.log(content, end)

    def warning(self, content, end='\n'):
        self.st.warning(content, end)

    def error(self, content, end='\n'):
        self.st.error(content, end)

    def destroy(self):
        self.win.destroy()

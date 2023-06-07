"""
@author: Y.J.W
# 這是一個供所有使用tkinter作為使用者介面的函式模組
# 共用模組應儘可能遵守DRY原則(dot not repeat yourself)
"""

from sources import fileworkercommon
from sources.scrollframe import VerticalScrolledFrame
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import ttk
import os
import threading
import tkinter as tk



class TkinterCommon:
    def __init__(self):
        #for var_name in globals():print(var_name)    
        self.debugMode = False
        self.initdir = os.getcwd()
        self.readFile = None
        self.readPath = None
        self.fileName = None
        self.fileType = None        
        self.dataCount = 0
        self.saveDir = None
        self.message = None
        self.items = None
        
    
    def dragged_files(self, label, filePath, fileTypes, text, cmds=None):
        """紀錄並顯示拖曳到視窗內的檔案名稱"""
        filePath = os.path.normpath(filePath)
        self.readPath, self.fileName, self.fileType = fileworkercommon.split_path_name(filePath)
        if self.fileType in fileTypes:
            #if filePath[0] == '{' and filePath[-1] == '}': 	
                #filePath = filePath[1:-1]
            label.configure(text=filePath)
            self.readFile = filePath
            if cmds is not None:
                for cmd in cmds:
                    cmd()
            #self.new_thread(self.count_data)
            #self.insert_message(text, self.message, clean=False)
        if self.debugMode:
            print('drag:', filePath)
            
        
    def new_thread(self, function):
        # threading.Thread 的function在沒有參數也沒有用括號的情況下
        # 可以解決視窗短暫鎖死的問題
        t = threading.Thread(target=function)
        t.start()
        t.join()


    def count_data(self):
        readFile = self.readFile
        self.dataCount = fileworkercommon.count_rows(readFile)
        self.message = "{} 有 {} 筆資料".format(readFile, self.dataCount)
        fileworkercommon.print_exec_mes_line(self.message)

  
    def choose_file(self, label, fileTypes, text, tAddCmd=None, fAddCmd=None):
        """fileTypes is a tuple, such as ("text files", "*.txt"),
            or filetypes = [("Excel files", ".xlsx .xls")]
        """
        self.readFile = fd.askopenfilename(initialdir=self.initdir, filetypes=fileTypes)
        if self.readFile is not None and self.readFile != '':
            self.readFile = os.path.normpath(self.readFile)
            label.configure(text=self.readFile)
            self.readPath, self.fileName, self.fileType = fileworkercommon.split_path_name(self.readFile)        
            self.message = str(self.readFile)
            self.insert_message(self.resultText, self.message, clean=False)
            if tAddCmd is not None:
               tAddCmd()
        else:
            label.configure(text='')
            if fAddCmd is not None:
                fAddCmd()
            if self.debugMode:
                print(self.readFile)
            

    def choose_dir(self, label):
        self.saveDir = fd.askdirectory(initialdir=self.initdir, title="Select a directory", mustexist=True)
        if self.saveDir is not None and self.saveDir != '':
            fileworkercommon.create_path(self.saveDir)
            label.configure(text=self.saveDir) 
        else:    
            label.configure(text='')
            
        
    def recurrent_configure(self, window):
        # Get all the widgets in the root window
        widgets = window.winfo_children()
        if not len(widgets):
            #print(window)
            window.rowconfigure(0, weight=1)
            window.columnconfigure(0, weight=1)
            return    
        for widget in widgets:    
            self.recurrent_configure(widget)
        #print(window)
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)            
        return


    def insert_message(self, text, message, clean=False):
        text.config(state='normal')
        message = fileworkercommon.strftime_now() + " " + message
        message += "\n"
        if clean:
            self.clean_text(text)
        text.insert('insert', message)
        text.config(state='disabled')


    def clean_text(self, text):
        text.config(state='normal')
        text.delete(1.0, 'end')
        text.config(state='disabled')


    def convert_input_to_num(self, word, type_:str, message):
        """word : numeric word, convert the word to numeric
            type_: int or float
        """    
        try:  
            if type_ == 'int':
                return int(word)
            elif type_ == 'float':
                return float(word)
        except:
            print(message)
            messagebox.showinfo('tip', message)
        
        
    def create_vertical_scroll_frame(self, pasteObject, gp={'side':'left'}):
        """ pasteObect 是要讓frame貼上的物件"""
        frame = VerticalScrolledFrame(pasteObject, width=self.frameWidth, gp=gp)
        #frame.grid(row=2, column=1, padx=(3,3), pady=(5,5), sticky='nsew')
        if 'grid' in gp:
            frame.grid(row=gp['grid'][0], column=gp['grid'][1])
        elif 'side' in gp:
            frame.pack(side=gp['side'], fill='both', expand=True)
        elif 'anchor' in gp:
            frame.pack(anchor=gp['anchor'], fill='both', expand=True)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        return frame
    
    
    def generate_interior_frame(self, frame, gp, recorder):
        """create an interior frame in frame
            gp is a dict like:
            1.{'grid':(0,1)}, means using grid, and row=0, column=1
            2.{'side':'left'}, means using pack, and side='left'
            3.{'anchor':'ne'}, means using pack, and anchor='ne'
        """
        # Use the 'interior' attribute to place widgets inside the scrollable frame.
        interiorFrame = ttk.Frame(frame.interior)
        if 'grid' in gp:
            interiorFrame.grid(row=gp['grid'][0], column=gp['grid'][1])
        elif 'side' in gp:
            interiorFrame.pack(side=gp['side'], padx=3, pady=3, fill='both', expand=True)
        elif 'anchor' in gp:
            interiorFrame.pack(anchor=gp['anchor'], padx=3, pady=3, fill='both', expand=True)
        recorder.append(interiorFrame)
        if self.debugMode:
            print("generate_interior_frame:", frame)
        
        return interiorFrame
    

    def generate_sheet(self, frame, title):
        for i in range(5):
            for j in range(len(title)):
                name=tk.StringVar()
                e = tk.Entry(frame, textvariable=name, justify='center')
                e.grid(row=i, column=j, sticky='nw')
                e.configure(state='disabled')
                if i == 0:
                    name.set(title[j])
                if i > 0:
                    pass
                    #e.grid_forget()

    
    def generate_label(self, pasteObect, gp, recorder, text, width=6):
        """pasteObject is the object for generate label to paste
           gp is a dict like:
            1.{'grid':(0,1)}, means using grid, and row=0, column=1
            2.{'side':'left'}, means using pack, and side='left'    
        """ 
        label = ttk.Label(pasteObect, text=text, width=width, font=self.fontstyle)
        if 'grid' in gp:
            label.grid(row=gp['grid'][0], column=gp['grid'][1], padx=3, pady=3, sticky='nsew')
        elif 'side' in gp:    
            label.pack(side=gp['side'], padx=3, pady=3, fill='both', expand=True)
        elif 'anchor' in gp:     
            label.pack(anchor=gp['anchor'], padx=3, pady=3, fill='both', expand=True)
        recorder.append(label)
        return label
        
        
    def generate_entry(self, pasteObect, gp, recorder, width=8):
        """pasteObject is the object for generate label to paste
           gp is a dict like:
            1.{'grid':(0,1)}, means using grid, and row=0, column=1
            2.{'side':'left'}, means using pack, and side='left'    
        """ 
        entry = tk.Entry(pasteObect, width=width, state='normal')
        if 'grid' in gp:
            entry.grid(row=gp['grid'][0], column=gp['grid'][1], padx=3, pady=3, sticky='nsew')
        elif 'side' in gp:    
            entry.pack(side=gp['side'], padx=3, pady=3, fill='both', expand=True)
        elif 'anchor' in gp:     
            entry.pack(anchor=gp['anchor'], padx=3, pady=3, fill='both', expand=True)
        recorder.append(entry)   
        return entry
    
    
    def generate_button(self, pasteObect, gp, recorder, text, command, width=8):
        """pasteObject is the object for generate label to paste
           gp is a dict like:
            1.{'grid':(0,1)}, means using grid, and row=0, column=1
            2.{'side':'left'}, means using pack, and side='left'    
        """     
        button = ttk.Button(pasteObect, text=text, width=width, command=command)
        if 'grid' in gp:
            button.grid(row=gp['grid'][0], column=gp['grid'][1], padx=3, pady=3, sticky='nsew')
        elif 'side' in gp:    
            button.pack(side=gp['side'], padx=3, pady=3, fill='both', expand=True)
        elif 'anchor' in gp:     
            button.pack(anchor=gp['anchor'], padx=3, pady=3, fill='both', expand=True)
        recorder.append(button)
        return button          
    
    
    def generate_combobox(self, pasteObject, gp, recorder, items, width=10):
        value = tk.StringVar()
        value.set('')
        menu = ttk.Combobox(pasteObject, state='readonly', width=width, values=items)  # 選單
        if 'grid' in gp:
            menu.grid(row=gp['grid'][0], column=gp['grid'][1], padx=(5,5), pady=(5,5), sticky='nsew')
        elif 'side' in gp:    
            menu.pack(side=gp['side'], padx=3, pady=3, fill='both', expand=True)
        elif 'anchor' in gp:     
            menu.pack(anchor=gp['anchor'], padx=3, pady=3, fill='both', expand=True)       
        recorder.append(menu)
        return menu  


    def destroy_and_del(self, group, toDestroyList, recorderList, varsNames):
        """toDestroyList contains the widgets which need to be destroy
           recorderList is a list contains several recorder list of each sub widget
           all widgets in the toDestroyList must have the same order in the recorderList 
           group is a number of the group
        """ 
        for recorder, widget in zip(recorderList, toDestroyList) : recorder.remove(widget) 
        for widget in toDestroyList : widget.destroy() 
        group -= 1
        if self.debugMode:
            childrenObjects = self.get_object_children_name(recorderList, varsNames)
            i = 0
            for child in childrenObjects:
                i += 1
                print(i, child)
                
        return group 


    def repack(self, group, ShtList, shtGorupLabelList):
        if group:
            i = 1
            for label, frame in zip(shtGorupLabelList, ShtList):
                label['text'] = '第{}組'.format(i)
                frame.pack()
                i += 1
    
    
    def destroy_and_repack(self, group, toDestroyList, recorderList, varsNames, ShtList, shtGorupLabelList):
        group = self.destroy_and_del(group, toDestroyList, recorderList, varsNames)
        print(group)
        self.repack(group, ShtList, shtGorupLabelList)
        return group


    def get_object_children_name(self, mother, varsNames):
        """mother is an iterable object 
           varsNames is vars(self), vars() or globals() 
        """
        children = {}
        #for v in varsNames: print(v)
        for element in mother:
            for name, value in varsNames.items():
                if value == element:
                    children[name] = element
        return children

    
    def clear_sheet(self, group, shtRowRecorder, recorderList, varsNames):
        """shtRowRecorder is a list(recorder) to record rows of sheet"""
        #print("recorderList", recorderList)
        if group:
            try:
                for i in range(group):
                    destroyObjects = list()
                    destroyObjects.append(shtRowRecorder[0])
                    for child in shtRowRecorder[0].winfo_children():
                        destroyObjects.append(child)
                    group = self.destroy_and_del(group, destroyObjects, recorderList, varsNames)
            except IndexError:
                print("index error", group)
            #print("shtRowRecorder", shtRowRecorder)
            #print("destroyObjects", destroyObjects)
            #print("recorderList", recorderList)    
        return group  

    
    def generate_items(self):
        if self.readFile is not None and self.readFile.strip() != '':
            if self.fileType in ('csv', 'txt'):
                self.items = fileworkercommon.get_columns(self.readFile) 
                if self.debugMode:
                    print(self.items)
                
                
    def change_combobox_values(self, combobox):
        if self.debugMode:
            print(combobox)
        if isinstance(combobox, list):
            for c in combobox:
                c['values'] = self.items
        elif isinstance(combobox, ttk.Combobox):
            combobox['values'] = self.items
    

    def update_widget(self, widget, kv):
        """當發生綁定事件時, 改變某容器屬性"""
        for key, value in kv.items():
            widget[key] = value
            

    def check_file_source(self, filePath, message):
        """檢查檔案是否存在"""
        if filePath is None or filePath.strip() == '':
            print(message)
            messagebox.showinfo('tip', message)
            return False
        else:    
            return os.path.isfile(filePath)
            
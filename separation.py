from tkinter import ttk
from tkinter import font as tkfont
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from sources import fileworkercommon
from sources.tkintercommon import TkinterCommon
import gc
import os
import time
import tkinter as tk

"""
待修改
5.讀取檔案用try except:UnicodeDecodeError
6.執行中把執行按鈕變成disable
"""

encodes = ('UTF-8', 'big5hkscs', 'ANSI')
code = 'UTF-8'

class FileWorker(TkinterCommon):
    def __init__(self):
        # 設定介面
        self.window = TkinterDnD.Tk()
        
        # 視窗標題
        self.window.title('FileWorker')        
        
        # 視窗大小
        self.width = int(self.window.winfo_screenwidth()*0.75)
        self.height = int(self.window.winfo_screenheight()*0.85)
   
        # 開啟時位於螢幕的位置
        self.xCordinate = int((self.width/2) - (self.width/2))
        self.yCordinate = int((self.height/2) - (self.height/2))
        self.window.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.xCordinate, self.yCordinate))
        
        # 設定共用寬度
        self.framePadx = 20
        self.frameWidth = int(self.width/2 - 2*self.framePadx)    

        # 字體
        self.fontstyle = tkfont.Font(family="Times", size=12)   
        # initialize style function
        self.style = ttk.Style()
        
        # Use clam theme
        self.style.theme_use('vista')
        # Used TLabelframe for styling labelframe widgets, and use red color for border
        #self.style.configure("TLabelframe", bordercolor="blue", borderwidth=5)
        #self.style.configure("TNotebook", bordercolor="blue", borderwidth=5)
        
        # 視窗drag and drop功能
        self.window.drop_target_register(DND_FILES)		# register the self.window as a drop target
        self.window.dnd_bind('<<Drop>>', lambda e:self.dragged_files(self.chooseFileLb, e.data, ('csv', 'txt'), self.resultText))	# 要傳入參數時用lambda, e是一個物件, 其中data屬性是路徑資料, 用vars(e)可以看所有的屬性資料
        self.window.option_add('*Dialog.msg.font', 'Helvetica 40')
        
        # 選單欄
        self.menuBar = tk.Menu(self.window)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='?', menu=self.fileMenu)
        self.fileMenu.add_command(label='關於FileWorker')
        self.window.config(menu=self.menuBar)

        # 分割與合併功能notebook
        self.notebook = ttk.Notebook(self.window)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # 功能notebook --> 分割頁籤
        self.separationFrame = tk.Frame(self.notebook)
        self.separationFrame.grid(row=0, column=0, sticky='nsew')
        self.notebook.add(self.separationFrame, text='分割檔案')
        
        # 功能notebook --> 分割頁籤 --> 左半頁
        self.leftFrame = tk.Frame(self.separationFrame, width=self.frameWidth)
        self.leftFrame.grid(row=0, column=0, sticky='nsew')
        
        # 功能notebook --> 分割頁籤 --> 右半頁
        self.rightFrame = tk.Frame(self.separationFrame, width=self.frameWidth)
        self.rightFrame.grid(row=0, column=1, sticky='nsew')
        
        # 左半頁 --> 選擇檔案標籤
        self.chooseFileFrame = ttk.LabelFrame(self.leftFrame, text='選擇檔案', width=self.frameWidth)
        self.chooseFileFrame.grid(row=0, column=0, padx=(20, 10), pady=5, sticky='ew')
        self.chooseFileBt = ttk.Button(self.chooseFileFrame, text='瀏覽', width=8,
                                      command=lambda:self.choose_file(self.chooseFileLb, [("text or csv", "*.txt *.csv")], self.resultText, 
                                      tAddCmd=self._choose_file_add_t_cmds, fAddCmd=self._choose_file_add_f_cmds)
                                     )
        self.chooseFileBt.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.chooseFileLb = ttk.Label(self.chooseFileFrame, text='', width=40, font=self.fontstyle)#, borderwidth=1, relief="solid")
        self.chooseFileLb.grid(row=0, column=1, sticky='w') 
        
        # 左半頁 --> 輸出檔案標籤
        self.outFileFrame = ttk.LabelFrame(self.leftFrame, text='輸出資料夾', width=self.frameWidth)
        self.outFileFrame.grid(row=1, column=0, padx=(20, 10), pady=5, sticky='ew')
        self.outFileBt = ttk.Button(self.outFileFrame, text='瀏覽', width=8,
                                        command=lambda:self.choose_dir(self.outFileLb))
        self.outFileBt.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.outFileLb = ttk.Label(self.outFileFrame, text='', width=40, font=self.fontstyle)
        self.outFileLb.grid(row=0, column=1, sticky='w')
        
        # 左半頁 --> 確認是檔案是否含欄位名稱標籤
        self.fieldsExistsFrame = ttk.LabelFrame(self.leftFrame, text='檔案是否含欄位名稱', padding=(5, 5), width=self.frameWidth)
        self.fieldsExistsFrame.grid(row=2, column=0, padx=(20, 10), pady=(5, 5), sticky='ew')
        self.fieldsExistChkBtVar = tk.BooleanVar()
        self.writeFieldsChkBtVar = tk.BooleanVar()

        self.fieldsExistChkBt = tk.Checkbutton(self.fieldsExistsFrame, text='檔案第一列是欄位名稱', var=self.fieldsExistChkBtVar, command=self._fields_exist_chkbt_event)
        self.fieldsExistChkBt.grid(row=0, column=0, padx=(5, 5), sticky='nw')
        self.writeFieldsChkBt = tk.Checkbutton(self.fieldsExistsFrame, text='分割時寫入欄位名稱', var=self.writeFieldsChkBtVar, state='disabled')
        self.writeFieldsChkBt.grid(row=0, column=1, padx=(5, 5), sticky='nw')
                
        #self.fieldsExistChkBt.bind('<Button-1>', lambda e:if self.fieldsExistChkBtVar:self.writeFieldsChkBt['state']='normal')
        
        # 左半頁 --> 結果Frame
        self.resultFrame = ttk.LabelFrame(self.leftFrame, text='執行結果', width=self.frameWidth)
        self.resultFrame.grid(row=3, column=0, padx=(20, 10), pady=(5, 5), sticky='nsew')
        
        self.resultText = tk.Text(self.resultFrame, width=50, height=15, wrap='none', state='disabled')   #wrap='word' or 'char' or 'none' 不換行
        self.resultText.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky='nsew')    
        #self.resultText.pack(side='left', padx=(5, 5), pady=(5, 5))        

        # 左半頁--> 結果Frame --> y捲動軸
        self.resultScrollbarY = tk.Scrollbar(self.resultFrame)
        self.resultScrollbarY.grid(row=0, column=1, rowspan=1, sticky='nsew')
        #self.resultScrollbarY.pack(side='right', fill='y')        

        self.resultScrollbarY.config(command=self.resultText.yview)           #Scrollbar 綁定 Text 的水平方向
        self.resultText.config(yscrollcommand=self.resultScrollbarY.set)    #Text 綁定水平捲軸

        # 左半頁--> 結果Frame --> x捲動軸
        self.resultScrollbarX = tk.Scrollbar(self.resultFrame, orient='horizontal')   #建立水平捲
        self.resultScrollbarX.grid(row=1, column=0, columnspan=1, sticky='nsew')
        #self.resultScrollbarX.pack(side='bottom', fill='x')        

        self.resultScrollbarX.config(command=self.resultText.xview)           #Scrollbar 綁定 Text 的水平方向
        self.resultText.config(xscrollcommand=self.resultScrollbarX.set)    #Text 綁定水平捲軸

        self.clrResFrmBt = ttk.Button(self.leftFrame, text='清除', width=8, command=lambda:self.clean_text(self.resultText))
        self.clrResFrmBt.grid(row=4, column=0, pady=5, sticky='ns')
        
        """
        # 右半頁--> 說明標籤
        self.tipFrame = ttk.LabelFrame(self.rightFrame, text='說明', width=60, height=20, padding=(1, 1))
        self.tipFrame.grid(row=0, column=0, padx=(20, 10), pady=10, sticky='nsew')
        self.tipLb = tk.Label(self.tipFrame, text='', width=60, height=20, borderwidth=1, relief="solid", font=self.fontstyle)
        self.tipLb.grid(row=0, column=0, sticky='nsew')
        """
        # 右半頁--> 選擇分割方式Frame
        self.splFileChoiceFrame = ttk.LabelFrame(self.rightFrame, width=self.frameWidth, text='分割方式')
        self.splFileChoiceFrame.pack(anchor='nw', padx=20, pady=20, fill='x', expand=True)
        
        self.splFileWayLb = ttk.Label(self.splFileChoiceFrame, text='選擇分割方式', justify='center', width=18)#, borderwidth=1, relief="solid")
        self.splFileWayLb.grid(row=0, column=0, padx=10, pady=5, sticky='nw')
        self.splFileNumLb = ttk.Label(self.splFileChoiceFrame, text='數量', justify='center', width=18)#, borderwidth=1, relief="solid")
        self.splFileNumLb.grid(row=0, column=2, columnspan=2, padx=10, pady=5, sticky='nw')

        self.splFileWayCombobox = ttk.Combobox(self.splFileChoiceFrame, state='readonly', width=16,
                                            values=('依檔案數分割', '依資料筆數分割', '依檔案大小分割', 
                                                    '依欄位資料分割', '依指定字分割')
                                          )
        self.splFileWayCombobox.grid(row=1, column=0, padx=10, pady=5, sticky='nw')
        self.splFileWayCombobox.bind("<<ComboboxSelected>>", self._splfile_way_combobox_choice)
        self.splFileNumEntry = tk.Entry(self.splFileChoiceFrame, width=16)
        self.splFileNumEntry.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky='nw')      

        self.splFileColNmFileNmChkBtVar = tk.BooleanVar()
        self.splFileColNmFileNmChkBt = tk.Checkbutton(self.splFileChoiceFrame, text='分割的檔案以欄位的內容命名', var=self.splFileColNmFileNmChkBtVar, command=self._given_file_name_chkbt_event)
        self.splFileColNmFileNmChkBt.grid(row=0, column=2, padx=(5, 5), sticky='nw')       
        self.splFileColNmFileNmChkBt.grid_forget()
        
        self.splFileColNmKeepNmChkBtVar = tk.BooleanVar()
        self.splFileColNmKeepNmChkBt = tk.Checkbutton(self.splFileChoiceFrame, text='保留原檔名為前綴', var=self.splFileColNmKeepNmChkBtVar, state='disabled')
        self.splFileColNmKeepNmChkBt.grid(row=1, column=2, padx=(5, 5), sticky='nw')       
        self.splFileColNmKeepNmChkBt.grid_forget()
        
        # 右半頁--> splFileCommonCmdBtFrame
        self.splFileCommonCmdBtFrame = ttk.Frame(self.rightFrame, width=20)
        self.splFileCommonCmdBtFrame.pack(side='left', pady=5, fill='x', expand=True) 
        
        self.splFileColNmCommonCmdBt = ttk.Button(self.splFileCommonCmdBtFrame, text='執行', command=self._splfile_cmd)
        self.splFileColNmCommonCmdBt.pack(anchor='center', pady=5)
        self.splFileCommonCmdBtFrame.pack_forget()

        # 右半頁--> splFileColNmFrame
        self.splFileColNmFrame = ttk.Frame(self.rightFrame, borderwidth=1, relief='solid')
        self.splFileColNmFrame.pack(side='top', padx=5, pady=5, fill='x', expand=True)

        # 右半頁--> splFileColNmFrame --> splFileColNmCmdBtFrame
        self.splFileColNmCmdBtFrame = ttk.Frame(self.splFileColNmFrame, width=self.frameWidth)
        #self.splFileColNmCmdBtFrame.grid(row=0, column=0, padx=(3,3), pady=(5,5), sticky='nsew')   
        self.splFileColNmCmdBtFrame.pack(side='top', padx=5, pady=5, fill='x', expand=True) 
        
        self.addSplFileBt = ttk.Button(self.splFileColNmCmdBtFrame, text='+', width=8, command=lambda:self._splfile_colnm_generate_sheet_cmd(self.splFileColNmSheet))
        self.addSplFileBt.pack(side='left', padx=(5,5), pady=(5,5), fill='x', expand=True)
        
        self.exeSplFileBt = ttk.Button(self.splFileColNmCmdBtFrame, text='執行', width=8, command=self._splfile_cmd)
        self.exeSplFileBt.pack(side='left', padx=(5,5), pady=(5,5), fill='x', expand=True)
        
        self.cleanSplFileBt = ttk.Button(self.splFileColNmCmdBtFrame, text='清除', width=8, command=lambda:self._splfile_colnm_clear_sheet_cmd(self.splFileColNmShtGroup, self.splFileColNmShtList, self.splFileColNmRecorderList)) 
        self.cleanSplFileBt.pack(side='left', padx=(5,5), pady=(5,5), fill='x', expand=True) 
        #self.splFileColNmCmdBtFrame.pack_forget()
        
        # 右半頁--> splFileColNmFrame --> splFileColNmLbFrame
        self.splFileColNmLbFrame = ttk.Frame(self.splFileColNmFrame, width=self.frameWidth)
        self.splFileColNmLbFrame.pack(side='top', padx=(3,3), pady=(5,5), fill='x', expand=True)
        
        self.splFileColNmGpLb = ttk.Label(self.splFileColNmLbFrame, text='組別', width=8, font=self.fontstyle)
        self.splFileColNmGpLb.pack(side='left', padx=(5,5), fill='x', expand=True)
        
        self.splFileColNmFieldsLb = ttk.Label(self.splFileColNmLbFrame, text='欄位名稱', width=10, padding=(7,7), font=self.fontstyle)
        self.splFileColNmFieldsLb.pack(side='left', padx=(7,7), fill='x', expand=True)       
        
        self.splFileColNmDelLb = ttk.Label(self.splFileColNmLbFrame, text='刪除', width=6, padding=(1,1), font=self.fontstyle)
        self.splFileColNmDelLb.pack(side='left', padx=(7,5), fill='x', expand=True) 
        
        # 右半頁--> splFileColNmFrame --> splFileColNmSheet
        self.splFileColNmSheet = self.create_vertical_scroll_frame(self.splFileColNmFrame)
        self.splFileColNmShtGroup = 0
        self.splFileColNmShtList = list()
        self.splFileColNmShtLbList = list()
        self.splFileColNmShtChoiceColList = list()
        self.splFileColNmShtDelBtList = list()
        self.splFileColNmRecorderList = [self.splFileColNmShtList, self.splFileColNmShtLbList, self.splFileColNmShtChoiceColList, self.splFileColNmShtDelBtList]

        # 先隱藏, 選擇以欄位值分割才出現
        self.splFileColNmFrame.pack_forget()

        # 右半頁--> splFileFrame --> splFileSpecWordFrame
        self.splFileSpecWordFrame = ttk.Frame(self.rightFrame, width=self.frameWidth)
        self.splFileSpecWordFrame.pack(side='top', padx=(5,5), pady=(3,3), fill='x', expand=True)

        #  右半頁--> splFileSpecWordFrame --> splFileSpecWordCmdBtFrame
        self.splFileSpecWordCmdBtFrame = ttk.Frame(self.splFileSpecWordFrame, width=self.frameWidth)
        #self.splFileSpecWordCmdBtFrame.grid(row=0, column=0, padx=(3,3), pady=(5,5), sticky='nsew')   
        self.splFileSpecWordCmdBtFrame.pack(anchor='nw', padx=(3,3), pady=(5,5), fill='x', expand=True) 
        
        self.addSpecWordBt = ttk.Button(self.splFileSpecWordCmdBtFrame, text='+', width=8, command=lambda:self._splfile_specword_generate_sheet_cmd(self.splFileSpecWordSheet))
        self.addSpecWordBt.pack(side='left', padx=(5,5), pady=(5,5), fill='x', expand=True)
        
        self.exeSpecWordBt = ttk.Button(self.splFileSpecWordCmdBtFrame, text='執行', width=8, command=None)
        self.exeSpecWordBt.pack(side='left', padx=(5,5), pady=(5,5), fill='x', expand=True)
        
        self.cleanSpecWordBt = ttk.Button(self.splFileSpecWordCmdBtFrame, text='清除', width=8, command=lambda:self.splfile_specword_clear_sheet_cmd(self.splFileSpecWordShtGroup, self.splFileSpecWordShtList, self.splFileSpecWordRecorderList)) 
        self.cleanSpecWordBt.pack(side='left', padx=(5,5), pady=(5,5), fill='x', expand=True)    
                
        #  右半頁 --> splFileSpecWordFrame --> self.splFileSpecWordLbFrame
        self.splFileSpecWordLbFrame = ttk.Frame(self.splFileSpecWordFrame)
        #self.splFileSpecWordLbFrame.grid(row=1, column=0, padx=(3,3), pady=(5,5), sticky='nsew')
        self.splFileSpecWordLbFrame.pack(anchor='nw', padx=(5,5), pady=(3,3), fill='x', expand=True)
        
        self.splFileSpecWordGpLb = ttk.Label(self.splFileSpecWordLbFrame, text='組別', width=8, font=self.fontstyle)
        self.splFileSpecWordGpLb.pack(side='left', padx=(5,5), fill='x', expand=True)
        
        self.splFileSpecWordFieldsLb = ttk.Label(self.splFileSpecWordLbFrame, text='選擇欄位', width=10, padding=(7,7), font=self.fontstyle)
        self.splFileSpecWordFieldsLb.pack(side='left', padx=(7,7), fill='x', expand=True)
                
        self.splFileSpecWordFindWordLb = ttk.Label(self.splFileSpecWordLbFrame, text='尋找的字元', width=10, padding=(7,7), font=self.fontstyle)
        self.splFileSpecWordFindWordLb.pack(side='left', padx=(7,7), fill='x', expand=True)
        
        self.splFileSpecWordDelLb = ttk.Label(self.splFileSpecWordLbFrame, text='刪除', width=6, padding=(1,1), font=self.fontstyle)
        self.splFileSpecWordDelLb.pack(side='left', padx=(7,5), fill='x', expand=True)

        #  右半頁--> splFileSpecWordFrame --> splFileSpecWordSheet
        self.splFileSpecWordSheet = self.create_vertical_scroll_frame(self.splFileSpecWordFrame)
        self.splFileSpecWordShtGroup = 0
        self.splFileSpecWordShtList = list()
        self.splFileSpecWordShtLbList = list()
        self.splFileSpecWordShtEntList = list()
        self.splFileSpecWordShtDelBtList = list()
        self.splFileSpecWordRecorderList = [self.splFileSpecWordShtList, self.splFileSpecWordShtLbList, self.splFileSpecWordShtEntList, self.splFileSpecWordShtDelBtList]
        
        # 先隱藏, 選擇以指定字分割才出現 
        self.splFileSpecWordFrame.pack_forget()

        # 功能notebook --> 合併頁籤
        self.combineFrame = tk.Frame(self.notebook)
        self.combineFrame.grid(row=0, column=0, sticky='ew')
        self.notebook.add(self.combineFrame, text='合併檔案')
        self.combineFrame.grid_propagate(0)

        # 選擇要合併的檔案
        # combineChooseFilesFrame 是可捲動的frame
        self.combineChooseFilesFrame = self.create_vertical_scroll_frame(self.combineFrame, gp={'grid':(0,0)})
        self.combineChooseFilesFrame.grid(row=0, column=0)
        self.combineChooseFilesTitle = ['Seq', 'Name', 'Size', 'Modify Date']
        
        # 產生表格
        self.generate_sheet(self.combineChooseFilesFrame, self.combineChooseFilesTitle)
        """
        # 合併設定
        self.combineSettingFrame = tk.Frame(self.combineFrame)
        self.combineSettingFrame.grid(row=2, column=0)
        self.combimeChoiceCombobox = ttk.Combobox(self.combineSettingFrame, text='')
        
        # 輸出
        self.combineOuputFrame = tk.Frame(self.combineFrame)
        self.combineOuputFrame.grid(row=3, column=0)
        """
        """
        # --擷取字串頁籤
        self.splStrFrame = ttk.Frame(self.notebook, width=self.frameWidth)
        self.splStrFrame.grid(row=0, column=0, sticky='nsew')
        self.notebook.add(self.splStrFrame, text='擷取字串')
              
        # --splStrCmdBtFrame
        self.splStrCmdBtFrame = ttk.Frame(self.splStrFrame, width=self.frameWidth)
        #self.splStrCmdBtFrame.grid(row=0, column=0, padx=(3,3), pady=(5,5), sticky='nsew')   
        self.splStrCmdBtFrame.pack(padx=(3,3), pady=(5,5), fill='x', expand=True) 
        
        self.addSplStrShtBt = ttk.Button(self.splStrCmdBtFrame, text='+', width=8, command=lambda:self.splstr_generate_sheet_cmd(self.splStrSheet))
        self.addSplStrShtBt.pack(side='left', padx=(5,5), pady=(5,5), fill='x', expand=True)
        
        self.exeSplStrBt = ttk.Button(self.splStrCmdBtFrame, text='執行', width=8, command=self.splstr_by_loc_cmd)
        self.exeSplStrBt.pack(side='left', padx=(5,5), pady=(5,5), fill='x', expand=True)
        
        self.cleanSplStrBt = ttk.Button(self.splStrCmdBtFrame, text='清除', width=8, command=lambda:self.splstr_clear_sheet_cmd(self.splStrShtGroup, self.splStrShtList, self.splStrRecorderList)) 
        self.cleanSplStrBt.pack(side='left', padx=(5,5), pady=(5,5), fill='x', expand=True)
        
        # --splStrColNmFrame
        self.splStrColNmFrame = ttk.Frame(self.splStrFrame)
        #self.splStrColNmFrame.grid(row=1, column=0, padx=(3,3), pady=(5,5), sticky='nsew')
        self.splStrColNmFrame.pack(padx=(5,5), pady=(3,3), fill='x', expand=True)
        
        self.splStrCol1 = ttk.Label(self.splStrColNmFrame, text='組別', width=4, font=self.fontstyle, anchor=tk.W)
        self.splStrCol1.pack(side='left', padx=(5,5), fill='x', expand=True)
        
        self.splStrCol2 = ttk.Label(self.splStrColNmFrame, text='新欄位名稱', width=8, padding=(7,7), font=self.fontstyle, anchor=tk.W)
        self.splStrCol2.pack(side='left', padx=(5,5), fill='x', expand=True)       
        
        self.splStrCol3 = ttk.Label(self.splStrColNmFrame, text='擷取起位', width=8, padding=(3,3), font=self.fontstyle, anchor=tk.W)
        self.splStrCol3.pack(side='left', padx=(5,5), fill='x', expand=True)

        self.splStrCol4 = ttk.Label(self.splStrColNmFrame, text='擷取終位', width=8, padding=(3,3), font=self.fontstyle, anchor=tk.W)
        self.splStrCol4.pack(side='left', padx=(5,5), fill='x', expand=True)   
        
        self.splStrCol5 = ttk.Label(self.splStrColNmFrame, text='刪除', width=4, padding=(1,1), font=self.fontstyle, anchor=tk.W)
        self.splStrCol5.pack(side='left', padx=(5,5), fill='x', expand=True)

        # --splStrSheet
        self.splStrSheet = self.create_vertical_scroll_frame(self.splStrFrame)
        self.splStrShtGroup = 0
        self.splStrShtList = list()
        self.splStrShtLbList = list()
        self.splStrShtEntColNmList = list()
        self.splStrShtEntBList = list()
        self.splStrShtEntEList = list()
        self.splStrShtDelBtList = list()        
        self.splStrRecorderList = [self.splStrShtList, self.splStrShtLbList, 
                                  self.splStrShtEntColNmList, self.splStrShtEntBList,  
                                  self.splStrShtEntEList, self.splStrShtDelBtList
                                 ]
        """
       
        # 設定元件大小隨視窗大小調整
        self.recurrent_configure(self.window)
        
        # 共用變數
        self.readFile = None
        self.readPath = None 
        self.fileName = None 
        self.fileType = None
        self.message = None
        self.header = True
        self.writeHeader = True
        self.initdir = os.getcwd()        
        self.dataCount = 0
        self.items = None
        self.debugMode = True
        self._init_save_dir()
        
        # 顯示視窗
        self.window.mainloop()
   
    
    def _init_save_dir(self):
        self.saveDir = os.path.normpath(os.path.join(os.getcwd(), 'fileworker_generate'))
        fileworkercommon.create_path(self.saveDir)
        self.outFileLb.configure(text=self.saveDir) 
      
    
    def _choose_file_add_t_cmds(self):
        self.generate_items()
        self.change_combobox_values(self.splFileColNmShtChoiceColList)
    
    
    def _choose_file_add_f_cmds(self):
        self.items = ''
        if self.debugMode:
            print("self.items:", self.items)
        self.change_combobox_values(self.splFileColNmShtChoiceColList)
    
    
    def _fields_exist_chkbt_event(self):
        if self.fieldsExistChkBtVar.get():
            self.writeFieldsChkBt.config(state='normal')
        else:
            self.writeFieldsChkBtVar.set(False)
            self.writeFieldsChkBt.config(state='disabled')


    def _read_write_with_fields(self):
        return self.fieldsExistChkBtVar.get(), self.writeFieldsChkBtVar.get()
    

    def _splfile_way_combobox_choice(self, event):
        # widget.pack_forget() or grid_forget()
        if self.splFileWayCombobox.current() in (0, 1, 2):
            if self.splFileWayCombobox.current() == 2:
                self.update_widget(self.splFileNumLb, {'text':'MB'})
            else:
                self.update_widget(self.splFileNumLb, {'text':'數量'})
            
            if not self.splFileNumEntry.winfo_viewable():
                self.splFileNumEntry.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky='nsew')
            if not self.splFileCommonCmdBtFrame.winfo_viewable():
                self.splFileCommonCmdBtFrame.pack(side='left', padx=(7,5), fill='both', expand=True)
            
            if self.splFileColNmFrame.winfo_viewable():
                self.splFileColNmFrame.pack_forget()
            if self.splFileSpecWordFrame.winfo_viewable():
                self.splFileSpecWordFrame.pack_forget()
            if self.splFileColNmFileNmChkBt.winfo_viewable():
                self.splFileColNmFileNmChkBt.grid_forget()    
            if self.splFileColNmKeepNmChkBt.winfo_viewable():
                self.splFileColNmKeepNmChkBt.grid_forget()   
   
        elif self.splFileWayCombobox.current() in (3, 4):
            self.update_widget(self.splFileNumLb, {'text':''})
            self.update_widget(self.splFileNumEntry, {}) 
            if self.splFileNumEntry.winfo_viewable():
                self.splFileNumEntry.grid_forget()
            if self.splFileCommonCmdBtFrame.winfo_viewable():
                self.splFileCommonCmdBtFrame.pack_forget()     
            
            if self.splFileWayCombobox.current() == 3:
                if self.splFileSpecWordFrame.winfo_viewable():
                    self.splFileSpecWordFrame.pack_forget()
                if not self.splFileColNmFrame.winfo_viewable():
                    self.splFileColNmFrame.pack(side='top', padx=(5,5), pady=(3,3), fill='x', expand=True)
                if not self.splFileColNmFileNmChkBt.winfo_viewable():
                    self.splFileColNmFileNmChkBt.grid(row=0, column=2, padx=(5, 5), sticky='nw')
                if not self.splFileColNmKeepNmChkBt.winfo_viewable():
                    self.splFileColNmKeepNmChkBt.grid(row=1, column=2, padx=(5, 5), sticky='nw')              
            
            elif self.splFileWayCombobox.current() == 4:
                if self.splFileColNmFrame.winfo_viewable():
                    self.splFileColNmFrame.pack_forget()
                if self.splFileColNmFileNmChkBt.winfo_viewable():
                    self.splFileColNmFileNmChkBt.grid_forget()
                if self.splFileColNmKeepNmChkBt.winfo_viewable():
                    self.splFileColNmKeepNmChkBt.grid_forget()
                if not self.splFileSpecWordFrame.winfo_viewable():
                    self.splFileSpecWordFrame.pack(side='top', padx=(5,5), pady=(3,3), fill='x', expand=True)


    def _given_file_name_chkbt_event(self):
        if self.splFileColNmFileNmChkBtVar.get():
            self.splFileColNmKeepNmChkBt.config(state='normal')
        else:
            self.splFileColNmKeepNmChkBtVar.set(False)
            self.splFileColNmKeepNmChkBt.config(state='disabled')


    def _splfile_colnm_generate_sheet_cmd(self, scrolledFrame):
        # colnm代表 column name
        groupFrame = self.generate_interior_frame(scrolledFrame, {'side':'top'}, self.splFileColNmShtList)
        groupLabel = self.generate_label(groupFrame, {'side':'left'}, self.splFileColNmShtLbList, text='第{}組'.format(self.splFileColNmShtGroup+1))   
        colNmCombobox = self.generate_combobox(groupFrame, {'side':'left'}, self.splFileColNmShtChoiceColList, self.items, width=8)    
        delButton = self.generate_button(groupFrame, {'side':'left'}, self.splFileColNmShtDelBtList, 'x', width=4,
                                            command=lambda:self._splfile_colnm_del_sheet_row_cmd(self.splFileColNmShtGroup, toDestroyList, recorderList))
        
        toDestroyList = [groupFrame, groupLabel, colNmCombobox, delButton]
        recorderList = [self.splFileColNmShtList, self.splFileColNmShtLbList, self.splFileColNmShtChoiceColList, self.splFileColNmShtDelBtList]
        self.splFileColNmShtGroup += 1
        
        # 設定介面元素大小隨視窗調整
        self.recurrent_configure(groupFrame)
        
        if self.debugMode:
            print('_splfile_colnm_generate_sheet_cmd:', self.splFileColNmShtGroup)


    def _splfile_colnm_del_sheet_row_cmd(self, group, toDestroyList, recorderList):
        self.splFileColNmShtGroup = self.destroy_and_repack(group, toDestroyList, recorderList, vars(self), self.splFileColNmShtList, self.splFileColNmShtLbList)


    def _splfile_colnm_clear_sheet_cmd(self, group, sheetRecorder, recorderList):  
        self.splFileColNmShtGroup = self.clear_sheet(group, sheetRecorder, recorderList, vars(self))

    
    def _splfile_write_file(self, fileName, fileType, lines, num=None, fields=None, mode='w'):
        fileName = fileworkercommon.file_name_filter(fileName)
        if num is None:
            newFileName = fileName+'.'+fileType
            writeFile = os.path.join(self.saveDir, newFileName)
        else:  
            newFileName = fileName+'_'+str(num)+'.'+fileType 
            writeFile = os.path.join(self.saveDir, newFileName)
            while os.path.exists(writeFile):
                writeFile, num = fileworkercommon.write_file_pass_exist(writeFile, self.saveDir, num, fileName, fileType)            
        
        self.message = "正在寫入 {}...".format(str(writeFile))
        self.insert_message(self.resultText, self.message)
        if mode == 'wb':
            fileworkercommon.write_file_in_bytes(writeFile, lines, fields=fields)
        else:    
            fileworkercommon.write_txt(writeFile, lines, fields=fields)
        return num


    def _splfile_work(self, perFileCount):
        # 取得檔案路徑、檔名、副檔名
        readPath, fileName, fileType = fileworkercommon.split_path_name(self.readFile)
        # 設定計數器
        num = 1
        count = 0
        lines = []
        # 欄位名稱
        fields = None
        # 讀取檔案
        i = 0
        for line in fileworkercommon.read_txt(self.readFile, encode=code):
            if self.header:
                if self.writeHeader:
                    fields = line
                self.header = False
                continue
            lines.append(line)
            count += 1
            if count == perFileCount:
                num = self._splfile_write_file(fileName, fileType, lines, fields, num)
                count = 0
                lines = []
        
        # 如果剩下的筆數未滿perFileCount
        if len(lines) > 0:
            num = self._splfile_write_file(fileName, fileType, lines, num, fields)
            count = 0
            lines = []            
        # 結束訊息
        self.message = "檔案分割完成!"
        self.insert_message(self.resultText, self.message, clean=False)
            
    
    def _splfile_by_file_num(self):    
        """依輸入的檔案數分割"""
        # 取得分割數量
        part = self.convert_input_to_num(self.splFileNumEntry.get().strip(), 'int', '數量欄位請輸入數字')
        if part is None:
            return False
        # 分割數量太多時, 確認是否分割
        result = True
        if part >= 20:
            result = messagebox.askyesno("Confirmation", "檔案將分割為{}個, 是否執行?".format(part))        
        
        # 確認執行
        if result:
            # 確認是否寫入表頭
            self.header, self.writeHeader = self._read_write_with_fields()
            # 計算每個檔案的資料筆數
            self.dataCount = fileworkercommon.count_rows(self.readFile, encode=code, header=self.header)
            perFileCount, remainder = divmod(self.dataCount, part)
            if remainder > 0:
                perFileCount += 1
            self._splfile_work(perFileCount)
            return True
        return False
        
    
    def _splfile_by_data_num(self): 
        # 取得分割數量
        perFileCount = self.convert_input_to_num(self.splFileNumEntry.get().strip(), 'int', '數量欄位請輸入數字')
        if perFileCount is None:
            return False
        
        # 確認是否寫入表頭
        self.header, self.writeHeader = self._read_write_with_fields() 

        # 計算分割的檔案數        
        self.dataCount = fileworkercommon.count_rows(self.readFile, header=self.header)
        part, remainder = divmod(self.dataCount, perFileCount)
        if remainder > 0: part += 1

        # 分割數量太多時, 確認是否分割
        result = True
        if part >= 20:
            result = messagebox.askyesno("Confirmation", "檔案將分割為{}個, 是否執行?".format(part))
        
        # 確認執行
        if result:        
            self._splfile_work(perFileCount)
            return True
        return False


    def _splfile_by_data_size(self):
        perDataSize = self.convert_input_to_num(self.splFileNumEntry.get().strip(), 'int', '請輸入分割大小')
        if perDataSize is None:
            return False
        perDataSize*=1024**2
        print(perDataSize)
        #dataSize = os.path.getsize(self.readFile)
        readPath, fileName, fileType = fileworkercommon.split_path_name(self.readFile)
        num = 1
        
        # 確認是否寫入欄位名稱
        self.header, self.writeHeader = self._read_write_with_fields()
        
        # 如果有欄位名稱要找出欄位名稱並取的欄位名稱的長度
        with open(self.readFile, 'rb') as rFile:
            if self.header:
                fields = rFile.readline()
                fieldsLen = len(fields)
                print('fields', fields)
                # 如果要寫入欄位名稱                
                if self.writeHeader:
                    # 讀取的大小要扣掉欄位名稱的大小
                    perDataSize -= fieldsLen
            else:
                fields = None
                
            remain = b''
            while True:
                chunk = rFile.read(perDataSize)
                if not chunk:
                    break
                # 找出本次區塊中最後一個換行符號
                # 將此換行符號以後的byte與下次讀取的chunk一起寫到下個檔案
                reverse = chunk[::-1]
                end = 0
                if len(chunk) >= perDataSize:
                    for i, byte in enumerate(reverse):
                        if byte == 13 or byte == 10:
                            end = i
                            print(i, byte)
                            break
                    
                    writeChunk = remain + chunk[:-end]
                    remain = chunk[-end:]
                else:
                    writeChunk = remain + chunk
                print('寫入前fields', fields)    
                num = self._splfile_write_file(fileName, fileType, writeChunk, num, fields=fields, mode='wb')

        return True


    def _splfile_by_column_data(self):
        # 遍歷combobox取得排序
        sortSeq = []
        for combobox in self.splFileColNmShtChoiceColList:
            # 不加入已選擇過的欄位
            if combobox.current() >= 0 and combobox.current() not in sortSeq:
                sortSeq.append(combobox.current())
        print(sortSeq)
        
        # 如果沒有選擇欄位就回傳False    
        if not len(sortSeq):
            messagebox.showinfo('tip', '選擇欄位,當欄位值相同時分割至同一檔案,可選多個欄位')
            return False
        
        # 讀取檔案
        rows = fileworkercommon.read_csv_yield_row(self.readFile, encoding='UTF-8')       
        
        # 確認是否寫入表頭
        self.header, self.writeHeader = self._read_write_with_fields()
        
        # 如果有勾選欄位名稱
        fields = None
        if self.header:         
            for row in rows:
                if self.writeHeader:
                    fields = ','.join(row)
                    if not fileworkercommon.is_line_end(fields):
                        fields = fileworkercommon.add_carriage_return_and_line_feed(fields)
                break
        
        # 排序
        fileworkercommon.print_exec_mes_line('開始排序資料')        
        sortedRows = sorted(rows, key=lambda x:[x[i] for i in sortSeq]) 
        
        # 設定紀錄欄位前一列的值的變數
        for j in range(len(sortSeq)):
            locals()['preColumn%s' %j] = ''
        # 取得檔案路徑、檔名、副檔名
        readPath, fileName, fileType = fileworkercommon.split_path_name(self.readFile)
        oriFileName = fileName
        # 分割檔案
        fileworkercommon.print_exec_mes_line('開始分割檔案')
        lines = []
        num = 1
        i = 0
        for row in sortedRows:
            i += 1
            for k in range(len(sortSeq)):
                if locals()['preColumn%s' %k] != row[sortSeq[k]]:
                    if len(lines) > 0:
                        if self.splFileColNmFileNmChkBtVar:
                            fileNames = []
                            for l in range(len(sortSeq)):
                                fileNames.append(locals()['preColumn%s' %l])
                            print(fileNames)
                            fileName = ''.join(fileNames)
                            if self.splFileColNmKeepNmChkBtVar:
                                fileName = oriFileName + fileName
                                print(fileName)   
                            fileNames = []
                            num = None
                        num = self._splfile_write_file(fileName, fileType, lines, num, fields=fields)   
                        lines = []
                locals()['preColumn%s' %k] = row[sortSeq[k]]   
            newRow = ','.join(row)
            if not fileworkercommon.is_line_end(newRow):
                newRow = fileworkercommon.add_carriage_return_and_line_feed(newRow)
            lines.append(newRow)
            """
            if i == 3:
                self._splfile_write_file(fileName, fileType, lines, num)
                os._exit(0)
            """    
        if len(lines) > 0:
            num = self._splfile_write_file(fileName, fileType, lines, num, fields=fields)
            lines = []                
        return True    


    def _splfile_cmd(self):
        splFileWay = self.splFileWayCombobox.current()
        if self.debugMode:
            print('splFileWay:', splFileWay)
        if self.check_file_source(self.readFile, '請先選擇來源檔案'):
            self.splFileColNmCommonCmdBt.config(state='disabled')
            fileworkercommon.create_path(self.saveDir)
            messagebox.showinfo('info', '開始分割檔案...')
            if splFileWay == 0: 
                splFileExeResult = self._splfile_by_file_num()
            elif splFileWay == 1:  
                splFileExeResult = self._splfile_by_data_num()
            elif splFileWay == 2:
                splFileExeResult = self._splfile_by_data_size()
            elif splFileWay == 3:
                splFileExeResult = self._splfile_by_column_data()
            self.splFileColNmCommonCmdBt.config(state='normal')
            if splFileExeResult:
                messagebox.showinfo('info', '檔案分割完成')


    def _splfile_specword_generate_sheet_cmd(self, scrolledFrame):
        groupFrame = self.generate_interior_frame(scrolledFrame, {'side':'top'}, self.splFileSpecWordShtList)
        groupLabel = self.generate_label(groupFrame, {'side':'left'}, self.splFileSpecWordShtLbList, text='第{}組'.format(self.splFileSpecWordShtGroup+1))   
        
        wordEntry = self.generate_entry(groupFrame, {'side':'left'}, self.splFileSpecWordShtEntList)    
        delButton = self.generate_button(groupFrame, {'side':'left'}, self.splFileSpecWordShtDelBtList, 'x', 
                                            command=lambda:self.splfile_specword_del_sheet_row_cmd(self.splFileSpecWordShtGroup, toDestroyList, recorderList))
        
        toDestroyList = [groupFrame, groupLabel, wordEntry, delButton]
        recorderList = [self.splFileSpecWordShtList, self.splFileSpecWordShtLbList, self.splFileSpecWordShtEntList, self.splFileSpecWordShtDelBtList]
        self.splFileSpecWordShtGroup += 1
        
        # 設定介面元素大小隨視窗調整
        self.recurrent_configure(groupFrame)
        
        if self.debugMode:
            print('_splfile_specword_generate_sheet_cmd:', self.splFileSpecWordShtGroup)       


    def splfile_specword_del_sheet_row_cmd(self, group, toDestroyList, recorderList):
        self.splFileSpecWordShtGroup = self.destroy_and_repack(group, toDestroyList, recorderList, vars(self), self.splFileSpecWordShtList, self.splFileSpecWordShtLbList)


    def splfile_specword_clear_sheet_cmd(self, group, sheetRecorder, recorderList):  
        self.splFileSpecWordShtGroup = self.clear_sheet(group, sheetRecorder, recorderList, vars(self))


    def splfile_specword_cmd(self): 
        writeFile = self.fileName+"SplStrBySymbol"+self.fileType
        fileworkercommon.create_path(self.saveDir)
        writePath = os.path.join(self.saveDir, writeFile)
        garbledWords = self.garbledEntry.get()
        garbledWords = self.splfile_specword_word(garbledWords)
        writeRows = list()
        count = 0
        for row in self.read_txt(encode='UTF-8'):
            for word in garbledWords:
                if row.find(word) > -1:
                    writeRows.append(row)
                    print(row, word)
                    count += 1
                    break
        
        if count > 0:
            self.write_txt(writePath, writeRows, mode='w')
            message = "共%s筆資料, 寫入%s" %(count, writePath) 
        else:
            message = "無資料"
        self.insert_message(self.resultText, message, clean=False)    
    

    def splfile_specword_word(self, words):
        """garbled words, like '�', '□', '―', '【', '〔', '囗', '〈' 
           the garbled words are separated by comma 
        """
        print(words)
        print(words.split(','))
        return words.split(',')
    
    
    def strange_word(self, string, count):
        strangeWords = []
        for word in string:
            if word in strangeWords:
            #if (not 13312 <= ord(word) <= 40883) and (not 63744 <= ord(word) <= 64045):
                print(count, word, ord(word))
                return True
        return False    


    def splstr_generate_sheet_cmd(self, scrolledFrame):
        groupFrame = self.generate_interior_frame(scrolledFrame, {'side':'left'}, self.splStrShtList)
        groupLabel = self.generate_label(groupFrame, {'side':'left'}, self.splStrShtLbList, text='第{}組'.format(self.splStrShtGroup+1))
        colNmEntry = self.generate_entry(groupFrame, {'side':'left'}, self.splStrShtEntColNmList)
        beginEntry = self.generate_entry(groupFrame, {'side':'left'}, self.splStrShtEntBList)    
        endEntry = self.generate_entry(groupFrame, {'side':'left'}, self.splStrShtEntEList)    
        delButton = self.generate_button(groupFrame, {'side':'left'}, self.splStrShtDelBtList, 'x', 
                                            command=lambda:self.splstr_del_sheet_row_cmd(self.splStrShtGroup, toDestroyList, recorderList))

        toDestroyList = [groupFrame, groupLabel, colNmEntry, beginEntry, endEntry, delButton]
        recorderList = [self.splStrShtList, self.splStrShtLbList, self.splStrShtEntColNmList, self.splStrShtEntBList, self.splStrShtEntEList, self.splStrShtDelBtList]
        self.splStrShtGroup += 1
 
        # 設定元件大小隨視窗大小調整
        self.recurrent_configure(groupFrame)

        if self.debugMode:
            print("splstr_generate_sheet_cmd group:", self.splStrShtGroup)       


    def splstr_del_sheet_row_cmd(self, group, toDestroyList, recorderList):
        self.splStrShtGroup = self.destroy_and_repack(group, toDestroyList, recorderList, vars(self), self.splStrShtList, self.splStrShtLbList)


    def splstr_clear_sheet_cmd(self, group, sheetRecorder, recorderList):  
        self.splStrShtGroup = self.clear_sheet(group, sheetRecorder, recorderList, vars(self))
 

    def splstr_by_loc_cmd(self):
        if self.fileName and self.fileType:
            self.exeSplStrBt.config(state='disabled')
            writeFile = self.fileName+"SplStrByLoc"+self.fileType
            writePath = os.path.join(self.saveDir, writeFile)
            data = list()
            for row in self.read_txt(encode='UTF-8'):
                writeDict = self.splstr_by_loc_write_data(row)
                data.append(writeDict)
            fields = data[0].keys()
            self.write_csv(data, writePath, fields)
            message = "字串分割完成, 已寫入{}!".format(writeFile)
            self.insert_message(self.resultText, message, clean=False)
        else:
            messagebox.showinfo('tip', '請先選擇來源檔案')
    """
    def splstr_by_symbol_cmd(self):
        writeFile = self.fileName+"SplStrBySymbol"+self.fileType
        writePath = os.path.join(self.saveDir, writeFile)
        data = list()
        for row in self.read_txt(encode='UTF-8'):
            writeDict = self.splstr_by_loc_write_data(row)
            data.append(writeDict)
        fields = data[0].keys()
        self.write_csv(data, writePath, fields)
        message = "字串分割完成, 已寫入{}!".format(writeFile)
        self.insert_message(self.resultText, message, clean=False)
    """


    def write_txt(self, writeFile, lines, mode='a+'):
        """writeFile is a file path, lines is a list""" 
        fileworkercommon.write_txt(writeFile, lines, mode)
    
    
    def write_csv(self, rows, writeFile, fields, header=True):
        fileworkercommon.cumulate_write_csv(rows, writeFile, fields, header=True, mode='w')
  
  


if __name__ == '__main__':
    worker = FileWorker()
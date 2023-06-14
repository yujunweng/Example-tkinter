'''
为python tkinter界面创建分页栏。
需要使用Notebook()和Frame()。
使用Notebook()创建分页栏,Frame()创建多个框架来当做不同的页面。
'''
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


root = Tk()
root.title('测试')
root.geometry('1600x1000+10+10')
tab_main=ttk.Notebook()#创建分页栏
tab_main.place(relx=0.02, rely=0.02, relwidth=0.887, relheight=0.876)

tab1=Frame(tab_main)#创建第一页框架

tab1.place(x=0,y=30)

tab_main.add(tab1,text='第一页')#将第一页插入分页栏中

Text = Text(tab1,width = 50,height=40)#显示文本框

Text.place(x=10,y=100)

button = Button(tab1,text='1',width=5)

button.place(x=50,y=10)

button1 = Button(tab1,text='2',width=5)

button1.place(x=100,y=10)

button2 = Button(tab1,text='3',width=5)

button2.place(x=150,y=10)

button3 = Button(tab1,text='4',width=5)

button3.place(x=200,y=10)



tab2=Frame(tab_main)

tab2.place(x=100,y=30)

tab_main.add(tab2,text='第二页')

fig = plt.figure(figsize=(7,4),dpi=100)#图像比例

f_plot =fig.add_subplot(111)#划分区域

canvas_spice = FigureCanvasTkAgg(fig,tab2)

canvas_spice.get_tk_widget().place(relx=0.3,rely=0.1)#放置位置

root.mainloop()
#-----------------------------------
#python tkinter 创建页签界面
#https://blog.51cto.com/u_15127608/4197720
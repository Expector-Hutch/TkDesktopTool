from tkinter import *
from tkinter.ttk import *
from tool import *
import ctypes

get_info = ctypes.cdll.LoadLibrary('./tivoli_performance_viewer.dll')

def exit(event):
    root.destroy()

root=TkDesktopTool()
root.geometry('300x300')
root.configure(bg='#141414')

mfc = Canvas(root, width=99, height=99, bg='#323232')
mfc.config(highlightthickness=0)
mfc.pack()
mfs = [-1] * 102
def set_mf():
    global mfs
    mf = get_info.memory_footprint()
    mfs = mfs[1:] + [mf]
    mfc.delete(ALL)
    mfc.create_polygon(-1, 100, *[[i - 1, 100 - mfs[i]] for i in range(102)], 100, 100, outline='black', fill='#66ccff')
    mfc.create_text(50, 50, text=f'RAM\n{mf}%')
    root.after(1000, set_mf)
root.after(1000, set_mf)

cuc = Canvas(root, width=99, height=99, bg='#323232')
cuc.config(highlightthickness=0)
cuc.pack()
cus = [-1] * 102
get_info.Initialize()
def set_cu():
    global cus
    cu = get_info.GetCPUUseRate()
    cus = cus[1:] + [cu]
    cuc.delete(ALL)
    cuc.create_polygon(-1, 100, *[[i - 1, 100 - cus[i]] for i in range(102)], 100, 100, outline='black', fill='#66ccff')
    cuc.create_text(50, 50, text=f'CPU\n{cu}%')
    get_info.Initialize()
    root.after(1000, set_cu)
root.after(1000, set_cu)


root.bind("<Double-Button-1>",exit)

root.mainloop()

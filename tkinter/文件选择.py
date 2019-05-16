import tkinter as tk
from tkinter.filedialog import askdirectory,askopenfile,askopenfilename,askopenfilenames,asksaveasfile,asksaveasfilename

window = tk.Tk()

window.title('我的窗口')
window.geometry('500x500')

def selectPath():
    path = askdirectory()
    print(path)

def selectPath2():
    path = askopenfile()
    print(path)    

def selectPath3():
    path = askopenfilename()
    print(path)    

def selectPath4():
    path = askopenfilenames()
    print(path)    

def selectPath5():
    path = asksaveasfilename()
    print(path)    


button1 = tk.Button(window,text='askdirectory',command=selectPath)
button1.pack(side='left')

button2 = tk.Button(window,text='askopenfile',command=selectPath2)
button2.pack(side='left')

button3 = tk.Button(window,text='askopenfilename',command=selectPath3)
button3.pack(side='left')

button4 = tk.Button(window,text='askopenfilenames',command=selectPath4)
button4.pack(side='left')

button5 = tk.Button(window,text='asksaveasfilename',command=selectPath5)
button5.pack(side='left')

window.mainloop()
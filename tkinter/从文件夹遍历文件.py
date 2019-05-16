import os
import tkinter as tk
from tkinter.filedialog import askdirectory


class RecursionFileSearch:
    '''
    递归搜索特定拓展名文件

    Args:
        base_dir:目录
        extension_name:拓展名，不带点

    Returns:
        文件绝对路径列表
    '''

    def __init__(self):
        self.file_path_list = []

    def recursionFileSearch(self, dir):
        path_list = [os.path.join(dir, i) for i in os.listdir(dir)]
        folder_path_list = [i for i in path_list if os.path.isdir(i) == True]
        file_path_list = [i for i in path_list if os.path.isfile(i) == True]

        self.file_path_list.extend(file_path_list)

        if len(folder_path_list) > 0:
            for dir in folder_path_list:
                self.recursionFileSearch(dir)

    def extensionFilter(self):
        self.file_path_list = filter(lambda x: os.path.splitext(x)[-1] == '.'+self.extension_name, self.file_path_list)
        self.file_path_list = list(self.file_path_list)

    def run(self, base_dir, extension_name):
        self.base_dir = base_dir
        self.extension_name = extension_name

        self.recursionFileSearch(self.base_dir)
        self.extensionFilter()


if __name__ == "__main__":
    r1 = RecursionFileSearch()

    window = tk.Tk()
    window.title('递归文件修改')
    window.geometry('1000x500')

    path_list = tk.StringVar()

    def selectPath():
        base_dir = askdirectory()
        print(base_dir, extension_entry.get())
        r1.run(base_dir, extension_entry.get())
        path_list.set(r1.file_path_list)

    extension_entry = tk.Entry(window)
    extension_entry.grid(row=0, column=0, padx=10, pady=10)
    open_button = tk.Button(window, text='打开目录', command=selectPath)
    open_button.grid(row=0, column=1)
    textarea = tk.Listbox(window,listvariable=path_list,height=15,width=140)
    textarea.grid(row=1,columnspan=10,padx=10,pady=10)

    window.mainloop()

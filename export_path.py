#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.ttk import *
import sqlite3


def select_db_file():
    db_file = askopenfilename(title="请选择BaiduYunCacheFileV0.db文件", filetypes=[('db', '*.db')])
    db.set(db_file)


def select_save_file():
    save_file = asksaveasfilename(filetypes=[('文件', '*.bat')])
    f.set(save_file + ".bat")


def create_baiduyun_filelist():
    conn = sqlite3.connect(db.get())
    cursor = conn.cursor()
    cursor.execute("select * from cache_file")
    while True:
        value = cursor.fetchone()
        if not value:
            break
        path = value[2]
        name = value[3]
        size = value[4]
        md5 = value[5]
        final_path = path[1:].replace("/","\\") + str(name)
        if size == 0:
            with open(f.get(), "a", encoding='utf-8') as fp:
                fp.write('md ' +  '"' + str(final_path) + '"' + '\n')


    with open(f.get(), "a", encoding='utf-8') as fp:
        fp.write('pause')
        fp.close()




root = Tk()
root.title('百度云文件BaiduPCS-Go秒传批处理生成-空目录建立')
db_select = Button(root, text=' 选择DB文件 ', command=select_db_file)
db_select.grid(row=1, column=1, sticky=W, padx=(2, 0), pady=(2, 0))
db = StringVar()
db_path = Entry(root, width=80, textvariable=db)
db_path['state'] = 'readonly'
db_path.grid(row=1, column=2, padx=3, pady=3, sticky=W + E)
save_path = Button(root, text='选择保存地址', command=select_save_file)
save_path.grid(row=2, column=1, sticky=W, padx=(2, 0), pady=(2, 0))
f = StringVar()
file_path = Entry(root, width=80, textvariable=f)
file_path['state'] = 'readonly'
file_path.grid(row=2, column=2, padx=3, pady=3, sticky=W + E)
create_btn = Button(root, text='生成空目录建立批处理命令行', command=create_baiduyun_filelist)
create_btn.grid(row=3, column=1, columnspan=2, pady=(0, 2))
root.columnconfigure(2, weight=1)
root.mainloop()

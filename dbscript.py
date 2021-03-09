from os.path import abspath

import tk as tk

import csv
import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from tkinter import *
import timeit

global running_time

def save():
    script_name = Path(script_full_path).stem

    con = sqlite3.connect("{}/{}.db".format(db_save_path, script_name))
    con.isolation_level = None

    start_time = timeit.default_timer()

    with open(abspath(script_full_path)) as f:
        sqlscript = f.read()

    cur = con.cursor()

    # cur.executescript(sqlscript)  primary key check


    con.commit()
    con.close()

    terminate_time = timeit.default_timer()
    running_time = terminate_time - start_time

    messagebox.showinfo("CSV2DB", "작업 완료! \n소요시간 : {}초 ".format(round(running_time,2)))

###################################################################################

def click(m):
    global script_full_path  # /home/shin/project/csv2db장/csv/temp.csv
    global db_save_path  # /home/shin/project/csv2db/db

    if m == 0:
        z = filedialog.askopenfilename(initialdir="~", title="Select file", filetypes=( ("sql files", "*.sql"), ("All files", "*.*") ) )
        script_full_path = z
        print(script_full_path)
    else:
        z = filedialog.askdirectory(initialdir="~", title="Select folder" )
        db_save_path = z
        print(db_save_path)


    a[m].delete(0, END)
    a[m].insert(tk.END, z)



###################################################################################

if __name__ == "__main__":

    # global section
    root = tk.Tk()
    root.title("csv2db")
    root.geometry("700x500")
    root.resizable(False, False)

    script_full_path = ""  #/home/shin/project/csv2db/csv/temp.csv
    db_save_path = ""  #/home/shin/project/csv2db/db




    ############################################################################


    a = [None for i in range(0,2)]

    Label = ttk.Label(root, text="선택 파일", background="white").grid(row=1, column=0, columnspan=3, padx=20, pady=10)
    a[0] = ttk.Entry(root, width=60, background="gray")
    a[0].grid(row=1 , column=3, columnspan=3, padx=10, sticky="WE")
    ttk.Button(root, text="Search", width=10, command=lambda m=0:click(m)).grid(row=1, column=10, padx=5)

    Label = ttk.Label(root, text="저장 경로", background="white").grid(row=3, column=0, columnspan=3, padx=20, pady=10)
    a[1] = ttk.Entry(root, width=60, background="gray")
    a[1].grid(row=3, column=3, columnspan=3, padx=10, sticky="WE")
    ttk.Button(root, text="Search", width=10, command=lambda m=1: click(m)).grid(row=3, column=10, padx=5)



    ttk.Button(root, text="변환하기", width=60, command=save).grid(row=5, column=3, padx=5)
    per = DoubleVar()
    progressbar = ttk.Progressbar(root, maximum = 100, length = 150, mode = "determinate", variable = per)
    progressbar.grid(row =30, column = 3, padx= 5)




    root.mainloop()


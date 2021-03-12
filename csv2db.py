import tk as tk

import csv
import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from tkinter import *
import timeit

# global csv_full_path  #/home/shin/project/csv2db장/csv/temp.csv
# global db_save_path   #/home/shin/project/csv2db/db
global running_time

def save():
    csv_name = Path(csv_full_path).stem

    print(db_save_path)
    print(csv_name)
    con = sqlite3.connect("{}/{}.db".format(db_save_path, csv_name))
    cur = con.cursor()

    f = open(csv_full_path, 'r', encoding ='utf-8')
    rdr = csv.reader(f)

    datas = list(rdr)

    brt = len(datas)
    a = brt//100

    name = ""
    temp = ""

    for i in range(len(datas[0])):
        name = name + str(datas[0][i]) + " char, "
        temp = temp + str(datas[0][i]) + ', '


    name = name[:-2]
    temp = temp[:-2]

    i = 0

    start_time = timeit.default_timer()
    # con.execute('BEGIN TRANSACTION')

    for line in datas:
        if i == 0:
            con.execute("drop table if exists {}".format(csv_name))
            con.execute("create table {}({})".format(csv_name, name))

        else:
            temp1 = "'" + "','".join(line) + "'"
            # print(temp1)
            # 쿼리문 value에 공백 안들어가게. ' '감싸기

            con.execute("insert into {0}({1}) values ({2})".format(csv_name, temp, temp1))

        i = i + 1

        #
        # if i % 10000 == 0 or i == brt:
        #     percentage = (i/brt)*100
        #     print(percentage)
        #     per.set(percentage)
        #     progressbar.update()

        #
        # if i % a == 0 or i == brt :
        #     percentage = (i/brt)*100
        #     print(percentage)
        #     per.set(percentage)
        #     progressbar.update()



    # con.execute('END TRANSACTION')
    # con.execute('COMMIT TRANSACTION')
    con.commit()
    con.close()

    terminate_time = timeit.default_timer()
    running_time = terminate_time - start_time

    messagebox.showinfo("CSV2DB", "작업 완료! \n소요시간 : {}초 ".format(round(running_time,3)))

###################################################################################

def click(m):
    global csv_full_path  # /home/shin/project/csv2db장/csv/temp.csv
    global db_save_path  # /home/shin/project/csv2db/db

    if m == 0:
        z = filedialog.askopenfilename(initialdir="~", title="Select file", filetypes=( ("csv files", "*.csv"), ("All files", "*.*") ) )
        csv_full_path = z
        print(csv_full_path)
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
    #root.resizable(False, False)

    csv_full_path = ""  #/home/shin/project/csv2db/csv/temp.csv
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
    # section = 100
    # per = DoubleVar()
    # progressbar = ttk.Progressbar(root, maximum = 100, length = 150, mode = "determinate", variable = per)
    #
    # progressbar.grid(row =30, column = 3, padx= 5)




    root.mainloop()


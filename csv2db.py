import csv
import os
import sqlite3
from os.path import abspath
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox


csv_full_path = ""  #/home/shin/project/csv2db장/csv/temp.csv
db_save_path = ""  #/home/shin/project/csv2db/db

###################################################################################
###################################################################################
def message(check):
    # if check == 1:
    #     messagebox.showinfo('파일 경로', '파일 경로는 {}입니다'.format(csv_full_path))
    # else:
    #     messagebox.showinfo('저장 경로', '저장 경로는 {}입니다'.format(db_save장_path))

    # global
    # te = Tk.StringVar(0);
    #
    # aaaa.get()
    # aaaa.set(dsfdfdsdsfddsdsf)


    if check == 1 :
        var1 = StringVar()
        label1 = Label(root, textvariable = var1)
        label1.pack(side = LEFT, padx = 10)
        var1.set("파일위치 : {}".format(csv_full_path))

    if check == 2 :
        var1 = StringVar()
        label1 = Label(root, textvariable=var1)
        label1.pack(side = BOTTOM, padx=10)
        var1.set("저장위치 : {}".format(db_save_path))




    # if check == 1:
    #     e = Entry(root, width = 50, fg = 'black', bg = 'yellow')
    #     e.pack()
    #     # e['visable'] =
    #     e.insert(0, "파일 위치: {}".format(csv_full_path))
    #
    # elif check == 2:
    #     e = Entry(root, width = 50, fg = 'black', bg = 'green')
    #     e.pack()
    #     e.insert(0, "저장 위치: {}".format(db_save_path))
    #
    # else:
    #     e = Entry(root, width = 50, fg = 'white', bg = 'black')
    #     e.pack()
    #     e.insert(0, "csv 파일을 선택해주세요! ")

###################################################################################
###################################################################################

def askfilepath():
    global csv_full_path

    # text_label.set("")


    file = filedialog.askopenfile()
    csv_full_path = file.name
    # label = Label(root, text = "선택 파일 : {}".format(os.path.split(csv_full_path)[1]))

    if csv_full_path[-3:] == "csv":
        message(1)

    else :
        message(3)

    # A = B.get()
    # label.pack()
    # return A


    # print(csv_full_path)
###################################################################################
###################################################################################
def askfolderpath():
    global db_save_path
    db_save_path = filedialog.askdirectory()
    print(db_save_path)
    message(2)

    # # label1 = Label(root, text = "선택 파일 : {}".format(os.path.split(csv_full_path)[1]))
    # # label1.pack()
    #
    # label2 = Label(root, text = "저장 위치 : {}".format(db_save_path))
    # label2.pack()
    #
    #
    # # print(TEST)
    # # return db_save_path

###################################################################################
###################################################################################
def save():
    csv_name = Path(csv_full_path).stem

    con = sqlite3.connect("{}/{}.db".format(db_save_path, csv_name))
    cur = con.cursor()

    f = open(csv_full_path, 'r', encoding = 'utf-8')
    rdr = csv.reader(f)

    datas = list(rdr)

    name = ""
    temp = ""

    for i in range(len(datas[0])):
        name = name + str(datas[0][i]) + " char, "
        temp = temp + str(datas[0][i]) + ', '


    name = name[:-2]
    temp = temp[:-2]

    i = 0

    for line in datas:
        if i == 0:
            con.execute("drop table if exists {}".format(csv_name))
            con.execute("create table {}({})".format(csv_name, name))

        else:
            temp1 = "'" + "','".join(line) + "'"
            print(temp1)
            # 쿼리문 value에 공백 안들어가게. ' '감싸기

            con.execute("insert into {0}({1}) values ({2})".format(csv_name, temp, temp1))

        i = i + 1

    con.commit()
    con.close()

    label1 = Label(root, text = "적재 성공!")
    label2 = Label(root, text = "적재 실패!")

    print(db_save_path + "/{}".format(csv_name))
    if os.path.isfile(db_save_path + "/{}.db".format(csv_name)):
        label1.pack()
    else:
        label2.pack()


###################################################################################
###################################################################################

if __name__ == "__main__":

    root = Tk()
    root.title("csv2db")
    root.geometry("400x450")
    root.resizable(False, False)

    csv_full_path = ""  #/home/shin/project/csv2db/csv/temp.csv
    db_save_path = ""  #/home/shin/project/csv2db/db



    # text_label = StringVar()
    #
    #
    # # Submit = Button(root, text = "Submit", command = lambda: C==askfilepath()).grid(row = 1, column = 1)
    # label_01 = Label(root, text='test', textvariable = text_label)
    # text_label.set("시작")
    # label_01.pack()
    #

    btn1 = Button(root, text = '파일선택', overrelief = "solid", command = askfilepath, background = "yellow")


    btn2 = Button(root, text = '저장위치선택', overrelief = "solid", command = askfolderpath , background = "green")

    btn3 = Button(root, text = '적재하기', overrelief = "solid", command = save, background = "black", fg = "white")

    btn3.pack(side = "bottom", fill = "x")
    btn2.pack(side = "bottom", fill = "x")
    btn1.pack(side = "bottom", fill = "x")

    # var1 = StringVar()
    # label1 = Label(root, textvariable=var1)
    # label1.pack(side=LEFT, padx=10)
    # var1.set("Aaa")

    # btn1.grid(row = 1, column = 1)
    # btn2.grid(row = 1, column = 2)
    # btn3.grid(row = 1, column = 3)


    # btn3.grid(row =1, column = 3)
    # btn3.place (x = 270, y = 50 )



    root.mainloop()

    # # def ask():
    # #     csv_path = filedialog.askopenfile(parent = root, initialdir = "/", title = "Please select a file")
    # #     csv_name = Path(csv_path).stem
    # #     print(csv_path)
    # #     return csv_name
    # #
    # # def askfolderpath(db_name):
    # #     db_path = filedialog.askdirectory(parent = root, initialdir = "/", title = "Please select a folder")
    #
    # def ask():
    #     root.dirname = filedialog.askdirectory()
    #     root.file = filedialog.askopenfile(initialdir = "path", title = "select file")
    #     print(root.dirname)
    #     return
    #
    #

    # btn1 = Button(root, width =10, text = "ask", command = ask)
    # btn1.pack(side = "top")







    # current_path = os.path.dirname(os.path.abspath(__file__))
    # db_path = abspath(current_path + '/../db')
    # csv_path = abspath(current_path + '/../csv/temp.csv')
    # csv_name = Path(csv_path).stem
    #
    #
    # con = sqlite3.connect("{}/{}.db".format(db_path, csv_name))
    # cur = con.cursor()
    #
    # f = open(csv_path, 'r', encoding = 'utf-8')
    # rdr = csv.reader(f)
    #
    # datas = list(rdr)
    #
    # name = ""
    # temp = ""
    #
    # for i in range(len(datas[0])):
    #     name = name + str(datas[0][i]) + " char, "
    #     temp = temp + str(datas[0][i]) + ', '
    #
    #
    # name = name[:-2]
    # temp = temp[:-2]
    #
    # i = 0
    #
    # for line in datas:
    #     if i == 0:
    #         con.execute("create table if not exists temp({})".format(name))
    #
    #     else:
    #         temp1 = "'" + "','".join(line) + "'"
    #         print(temp1)
    #         # 쿼리문 value에 공백 안들어가게. ' '감싸기
    #
    #         con.execute("insert into temp({0}) values ({1})".format(temp, temp1))
    #
    #     i = i + 1
    #
    # con.commit()
    # con.close()

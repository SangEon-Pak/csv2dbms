import csv
import os
import sqlite3
from os.path import abspath
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import timeit

csv_full_path = ""  #/home/shin/project/csv2db장/csv/temp.csv
db_save_path = ""  #/home/shin/project/csv2db/db

###################################################################################
###################################################################################
def message(check):
    statusvar.set("")
    runtime.set("")
    savepath.set("")

    if check == 1 :
        print(filelocation)
        filelocation.set("파일위치 : {}".format(csv_full_path))
        print(filelocation)
        savepath.set("")

    elif check == 2 :
        if os.path.isdir(db_save_path):
            savepath.set("저장위치 : {}".format(db_save_path))

        # else:  애초에 디렉토리밖에 설정 안됨. 그리고 set 에서 설정 못하는듯.
       #     savepath.set("디렉토리를 선택해 주세요!",font = 40, fg = "red")


    else:
        filelocation.set("CSV 파일을 선택해주세요!")




###################################################################################
###################################################################################

def askfilepath():
    global csv_full_path

    file = filedialog.askopenfile()
    csv_full_path = file.name

    if csv_full_path[-3:] == "csv":
        message(1)

    else:
        message(3)


###################################################################################
###################################################################################
def askfolderpath():
    global db_save_path
    db_save_path = filedialog.askdirectory()
    print(db_save_path)
    message(2)


###################################################################################
###################################################################################
def save():
    global terminate_time
    global start_time


    if filelocation.get() == "":
        savepath.set("CSV 파일을 선택해 주세요!")

    if savepath.get() == "":
        savepath.set("저장 경로를 선택해 주세요!")



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

    start_time = timeit.default_timer()

    # for line in datas:
    #     if i == 0:
    #         con.execute("drop table if exists {}".format(csv_name))
    #         con.execute("create table {}({})".format(csv_name, name))
    #
    #     else:
    #         temp1 = "'" + "','".join(line) + "'"
    #         # print(temp1)
    #         # 쿼리문 value에 공백 안들어가게. ' '감싸기
    #
    #         con.execute("insert into {0}({1}) values ({2})".format(csv_name, temp, temp1))
    #
    #     i = i + 1
    #
    # con.commit()
    # con.close()
    #


    con.execute('BEGIN TRANSACTION')

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

    # con.execute('END TRANSACTION')
    con.execute('COMMIT TRANSACTION')


    con.commit()
    con.close()




    if os.path.isfile(db_save_path + "/{}.db".format(csv_name)):
        statusvar.set("변환 완료!")
    else:
        statusvar.set("변환 실패!")

    terminate_time = timeit.default_timer()
    runtime.set("소요 시간 : {}초".format(terminate_time - start_time))

###################################################################################
###################################################################################

if __name__ == "__main__":

    root = Tk()
    root.title("csv2db")
    root.geometry("600x600")
    root.resizable(False, False)

    csv_full_path = ""  #/home/shin/project/csv2db/csv/temp.csv
    db_save_path = ""  #/home/shin/project/csv2db/db





    btn1 = Button(root, text = '파일선택', overrelief = "solid", command = askfilepath, background = "yellow")
    btn2 = Button(root, text = '저장위치선택', overrelief = "solid", command = askfolderpath , background = "green")
    btn3 = Button(root, text = '적재하기', overrelief = "solid", command = save, background = "black", fg = "white")


    btn3.pack(side = "bottom", fill = "x")     # 버튼 위젯 배치
    btn2.pack(side = "bottom", fill = "x")
    btn1.pack(side = "bottom", fill = "x")


    # tempvar.set(terminate_time - start_time)  set 은 함수에서 해주기!


    filelocation = StringVar()
    filelocationlbl = Label(root, textvariable = filelocation, font = 70)
    filelocationlbl.pack()

    savepath = StringVar()
    savepathlbl = Label(root, textvariable = savepath, font = 70)
    savepathlbl.pack()

    statusvar = StringVar()
    statuslbl = Label(root, textvariable = statusvar, font = 70, fg = "red" )
    statuslbl.pack()

    runtime = StringVar()
    runtimelbl = Label(root, textvariable = runtime, font = 70)
    runtimelbl.pack()

    root.mainloop()


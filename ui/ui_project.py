from tkinter import *
from tkinter import filedialog

from xlsxwriter.workbook import Workbook

import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import os
import glob
import shutil as stl
import csv

import tabula
import pandas as pd


root = Tk()
root.title('RnE')


### Key Variable ###

# current_path where this program is located
current_path = os.path.dirname(os.path.realpath(__file__))

# folder_name of pdf files
folder_pdf = 'pdf'

pdf_dir = os.path.join(current_path,folder_pdf)



### Functions ###


# file function

def add_file():
    files = filedialog.askopenfilenames(title='PDF파일을 선택하세요', filetypes=(('pdf파일','*.pdf'),('모든 파일','*.*')))

    for f in files:
        list_file.insert(END, f)

def rm_file():

    for idx in reversed(list_file.curselection()):
        list_file.delete(idx)


# Save path function

def appoint_save_path():
    folder = filedialog.askdirectory()
    if folder == '': # 취소를 눌렀을 때
        return
    
    txt_dest_path.delete(0,END)
    txt_dest_path.insert(0, folder)


# Convert2csv function

def one_dir():
    
    if os.path.isdir(pdf_dir):
        stl.rmtree(pdf_dir)
    os.mkdir(pdf_dir)

    for i, f in enumerate(list_file.get(0,END)):

        stl.copy(f,pdf_dir)

        progress = (i + 1) / list_file.size() * 10
        p_var.set(progress)
        progress_bar.update()

def convert2csv():

    tabula.convert_into_by_batch(pdf_dir, lattice=True, output_format='csv', pages='all')

    progress = 40
    p_var.set(progress)
    progress_bar.update()

def merge_csv():

    vtcl_opt = cmb_vtcl.get()
    if vtcl_opt == '수직':
        vtcl_opt = 0
    elif vtcl_opt == '수평':
        vtcl_opt = 1

    allFile_list = glob.glob(os.path.join(pdf_dir, '*.csv'))
    
    output_file = os.path.join(txt_dest_path.get(), txt_dest_file.get()+'.csv')

    print(allFile_list)
    allData = []

    for i, file in enumerate(allFile_list):

        df = pd.read_csv(file, encoding='cp949')
        allData.append(df)

        progress = (i + 1) / len(allFile_list) * 40 + 40
        p_var.set(progress)
        progress_bar.update()
    
    dataCombine = pd.concat(allData, axis=vtcl_opt, ignore_index=True) # concat함수를 이용해서 리스트의 내용을 병합
    # axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
    dataCombine.to_csv(output_file, index=False)

    progress = 90
    p_var.set(progress)
    progress_bar.update()

def convert2xlsx():
    output_file = os.path.join(txt_dest_path.get(), txt_dest_file.get()+'.csv')

    workbook = Workbook(output_file[:-4] + '.xlsx')
    worksheet = workbook.add_worksheet()
    with open(output_file, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()

    progress = 100
    p_var.set(progress)
    progress_bar.update()


def start():
    
    # Check file list
    if list_file.size() == 0:
        msgbox.showwarning('경고','pdf 파일을 추가하세요')
        return

    # Check Save path
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning('경고','저장 경로를 선택하세요')
        return

    if len(txt_dest_file.get()) == 0:
        msgbox.showwarning('경고','파일 이름을 선택하세요')
        return

    if os.path.isfile(os.path.join(txt_dest_path.get(), txt_dest_file.get()+'.xlsx')) == True:
        msgbox.showwarning('경고','이미 존재하는 파일입니다.')
        return

    askok = msgbox.askokcancel('실행 확인','다음 설정으로 pdf를 병합합니다: {} {}\nPDF:{}'.format(cmb_format.get(),cmb_vtcl.get(),list_file.get(0,END)))
    if askok != 1: return 

    # Save selected pdf files in one directory & convert pdf files to csv
    try:
        one_dir()       # 10%
        convert2csv()   # 40%

        merge_csv()     # 90%
        convert2xlsx()  # 100%

        msgbox.showinfo('알림', '작업이 완료되었습니다')
    except Exception as err:
        msgbox.showerror('ERROR','다음과 같은 에러가 발생했습니다.\n{}'.format(err))

        progress = 0
        p_var.set(progress)
        progress_bar.update()




### LAYOUT ###


# File Frame ( Add File, Selection Remove)

file_frame = Frame(root)
file_frame.pack(fill='x', padx=5,pady=5)

btn_add_file = Button(file_frame, padx=5,pady=5, width=12, text='파일 추가', command=add_file)
btn_add_file.pack(side='left', padx=5, pady=5)

btn_rm_file = Button(file_frame, padx=5,pady=5, width=12, text='파일 삭제', command=rm_file)
btn_rm_file.pack(side='left', padx=5, pady=5)


# List Frame

list_frame = Frame(root)
list_frame.pack(fill='both', padx=5,pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side='right', fill='y')

list_file = Listbox(list_frame, selectmode='extended', height=10, yscrollcommand=scrollbar.set)
list_file.pack(side='left', fill='both', expand=True)
scrollbar.config(command=list_file.yview)


# Option Frame

option_frame = LabelFrame(root,text='옵션')
option_frame.pack(padx=10,pady=10, fill='x')

# 1. Format Option
lbl_format = Label(option_frame,text='포맷 형식')
lbl_format.pack(side='left', padx=5,pady=5)

opt_format = ['xlsx','csv']

cmb_format = ttk.Combobox(option_frame, state='readonly', value = opt_format, width=15)
cmb_format.current(0)
cmb_format.pack(side='left', padx=5,pady=5)

# 2. Vertical Option

opt_vtcl = ['수직','수평']

cmb_vtcl = ttk.Combobox(option_frame, state='readonly', value = opt_vtcl, width=15)
cmb_vtcl.current(0)
cmb_vtcl.pack(side='right', padx=5,pady=5)

lbl_vtcl = Label(option_frame,text='병합 형식')
lbl_vtcl.pack(side='right', padx=5,pady=5)


# Save Path Frame

path_frame = LabelFrame(root, text='저장 위치')
path_frame.pack(fill='x', padx=5,pady=5)

Label(path_frame,text='저장 경로').pack(side='left')

txt_dest_path = Entry(path_frame,width=30)
txt_dest_path.pack(side='left', fill='x', expand=True, ipady=5, padx=5,pady=5)

btn_dest_path = Button(path_frame, text='디렉토리 검색', width=10, padx=5,pady=5, command=appoint_save_path)
btn_dest_path.pack(side='right')

Label(path_frame,text='파일명').pack(side='left')

txt_dest_file = Entry(path_frame,width=10)
txt_dest_file.insert(END,'result_table')
txt_dest_file.pack(side='left', fill='x', expand=True, ipady=5, padx=5,pady=5)


# Progress Bar option

frame_progress = LabelFrame(root, text='진행 상황')
frame_progress.pack(fill='x', padx=5,pady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill='x', padx=5,pady=5)


# Run Frame

btn_start = Button(root, padx=5, pady=5, text='시작', width=12, command=start)
btn_start.pack(side='right', padx=5,pady=5)



root.resizable(False,False)
root.mainloop()

# from rich import print
# import os
from tkinter import ttk
import tkinter as tk
from ttkwidgets import Table
from helpers import loadFiles
from datetime import datetime


SETUP, CLASS_INFO = loadFiles()
data = list(CLASS_INFO.items())
CURR_TIME = datetime.now().strftime("%H:%M")
CURR_DAY_NUM = datetime.today().weekday()
CURR_DATE = datetime.now().strftime("%d-%m-%Y")
CURR_DAY = datetime.now().strftime("%A")

root = tk.Tk()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

style = ttk.Style(root)
style.theme_use('alt')
supervisorMode = tk.BooleanVar(root, True)
drag_row = tk.BooleanVar(root, False)
drag_col = tk.BooleanVar(root, False)

columns = ["Class Title", "Class Code", "Class Password",
           "Class Joining Time", "Class Leaving Time", "Class Duration"]
table = Table(root, columns=columns, sortable=True, drag_cols=drag_col.get(),
              drag_rows=drag_row.get(), height=10)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=100, stretch=True)

for ind, cls in enumerate(data):
    tableItems = []
    tableItems.append(cls[0])

    for value in cls[1]:
        if value != "time_friday" and value != "time_of_leaving_friday":
            # weekdays
            if CURR_DAY_NUM in range(0, 4):
                tableItems.append(cls[1][value])

        if value != "time_of_leaving_weekday" and value != "time_weekday":
            # friday
            if CURR_DAY_NUM == 4:
                tableItems.append(cls[1][value])

    duration = str(datetime.strptime(
        tableItems[3], "%H:%M") - datetime.strptime(tableItems[4], "%H:%M"))[:-3]
    tableItems.append(duration)
    # print(cls)
    # print(tableItems)
    # print("--------------------------------------------")
    table.insert("", "end", iid=ind, values=list(tableItems))


# add scrollbars
sx = tk.Scrollbar(root, orient='horizontal', command=table.xview)
sy = tk.Scrollbar(root, orient='vertical', command=table.yview)
table.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)

table.grid(sticky='ewns')
sx.grid(row=1, column=0, sticky='ew')
sy.grid(row=0, column=1, sticky='ns')
root.update_idletasks()


# toggle table properties
def toggle_drag_col():
    table.config(drag_cols=drag_col.get())


def toggle_drag_row():
    table.config(drag_rows=drag_row.get())


def toggleSupervisorMode():
    print(supervisorMode.get())
    supervisorMode.set(not bool(supervisorMode))
    print(supervisorMode.get())


frame = tk.Frame(root)
# checkboxes
tk.Checkbutton(frame, text='Drag Columns', variable=drag_col,
               command=toggle_drag_col).grid(column=0, row=0)
tk.Checkbutton(frame, text='Drag Rows', variable=drag_row,
               command=toggle_drag_row).grid(column=1, row=0)
tk.Checkbutton(frame, text='Supervisor Mode', variable=supervisorMode,
               command=toggleSupervisorMode).grid(column=1, row=0)
# labels
tk.Label(root, text=f"{CURR_TIME}").grid()
tk.Label(root, text=f"{CURR_DATE} - {CURR_DAY}").grid()
tk.Label(root, text=f"{supervisorMode.get()}").grid()

frame.grid()

root.title("AutoClass by Shaheer Sarfaraz")
root.geometry('900x300')
root.mainloop()

import sqlite3
import tkinter as tk
from tkinter import *

my_conn = sqlite3.connect('Asset Tracking.s3db')

my_w = tk.Tk()
my_w.geometry("400x250")

r_set = my_conn.execute('''SELECT * from User''')
i = 1  # row value inside the loop
for user in r_set:
    for j in range(len(user)):
        e = Entry(my_w, width=10, fg='blue')
        e.grid(row=i, column=j)
        e.insert(END, user[j])
    i = i+1

e = Label(my_w, width=10, text='ID', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
e.grid(row=0, column=0)
e = Label(my_w, width=10, text='Name', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
e.grid(row=0, column=1)
e = Label(my_w, width=10, text='Surname', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
e.grid(row=0, column=2)
e = Label(my_w, width=10, text='Asset', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
e.grid(row=0, column=3)

i = 1

# add one Label
l1 = tk.Label(my_w,  text='Enter User ID: ', width=25)
l1.grid(row=15, column=6)

# add one text box
t1 = tk.Text(my_w,  height=1, width=5, bg='grey', fg='white')
t1.grid(row=15, column=7)

b1 = tk.Button(my_w, text='Show Details', width=15, bg='light grey', command=lambda: my_details(t1.get('1.0', END)))
b1.grid(row=15, column=10)

my_str = tk.StringVar()
# add one Label
l2 = tk.Label(my_w,  textvariable=my_str, width=30, fg='red')
l2.grid(row=17, column=6, columnspan=2)

my_str.set("Output")


def my_details(id):
    try:
        val = int(id)  # check input is integer or not
        try:
            q = "SELECT * FROM User WHERE ID= "+id
            my_cursor = my_conn.execute(q)
            data_row = my_cursor.fetchone()
            my_str.set(data_row)
        except sqlite3.Error as my_error:
            print("error: ", my_error)
    except:
        my_str.set("Check input")


my_w.mainloop()

import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import *

my_conn = sqlite3.connect('Asset Tracking.s3db')

my_w = tk.Tk()
my_w.geometry("1150x300")


def display_data():
    e = Label(my_w, width=10, text='ID', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
    e.grid(row=0, column=0)
    e = Label(my_w, width=10, text='Name', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
    e.grid(row=0, column=1)
    e = Label(my_w, width=10, text='Surname', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
    e.grid(row=0, column=2)
    e = Label(my_w, width=10, text='Asset', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
    e.grid(row=0, column=3)

    r_set = my_conn.execute('''SELECT * from User''')
    i = 1  # row value inside the loop
    for user in r_set:
        for j in range(len(user)):
            e = Entry(my_w, width=10, fg='blue')
            e.grid(row=i, column=j)
            e.insert(END, user[j])
        e = Button(my_w, text='x', command=lambda d=user[0]: my_delete(d))
        e.grid(row=i, column=j + 1)
        i = i+1


def add_data():
    try:
        my_id = tid2.get('1.0', END)  # read name
        my_asset = options.get()  # read class
        my_name = tName.get('1.0', END)  # read mark
        my_surname = tsname.get('1.0', END)  # read gender
        if int(my_id):
            my_conn.execute("""
            INSERT INTO User(ID, Name, Surname, Asset)
            VALUES (?,?,?,?)
            """, (my_id, my_name, my_surname, my_asset))
            my_conn.commit()
            display_data()
            options.set("")  # reset the option menu
            tid2.delete('1.0', END)  # reset the text entry box
            tName.delete('1.0', END)  # reset the text entry box
            tsname.delete('1.0', END)  # reset the text entry box
        else:
            messagebox.showerror("Error", "Invalid input")
    except:
        messagebox.showerror("Error", "Invalid input")


def search(id):
    try:
        int(id)  # check input is integer or not
        try:
            q = "SELECT * FROM User WHERE ID= "+id
            my_cursor = my_conn.execute(q)
            data_row = my_cursor.fetchone()
            my_str.set(data_row)
        except sqlite3.Error as my_error:
            print("error: ", my_error)
    except:
        my_str.set("Check input")


def countdown(time):
    if time == -1:
        my_w.destroy()
    else:
        l4 = tk.Label(my_w, text="time remaining: %d seconds" % time)
        l4.grid(row=50, column=51)

        my_w.after(1000, countdown, time-1)


def my_delete(id):
    my_var = messagebox.askyesnocancel("Delete ?", "Delete id:"+str(id), icon='warning', default='no')
    if my_var:  # True if yes button is clicked
        r_set = my_conn.execute("DELETE FROM User WHERE ID=" + str(id))
        my_conn.commit()
        messagebox.showerror("Deleted ", "Record deleted")
        display_data()  # refresh the window with new records


def update():
    my_asset2 = options2.get()  # read class
    my_id2 = tid3.get('1.0', END)  # read name
    r_set = my_conn.execute("""UPDATE User SET Asset= ? WHERE ID= ?""", (my_asset2, my_id2))
    my_conn.commit()
    messagebox.showinfo("Updated", "Record updated")
    display_data()


def delete():
    my_id3 = tid4.get('1.0', END)  # read name
    r_set = my_conn.execute("""DELETE FROM User WHERE ID=""" + my_id3)
    my_conn.commit()
    messagebox.showerror("Deleted ", "Record deleted")
    display_data()


display_data()

# add employee label
lSearch = tk.Label(my_w,  text='Search Employee', font=('Helvetica', 12), width=30, anchor="c")
lSearch.grid(row=0, column=9, columnspan=4)

# ID Label for search
lid = tk.Label(my_w,  text='Enter User ID: ', width=25)
lid.grid(row=2, column=10)

# ID text box for search
tid = tk.Text(my_w,  height=1, width=5)
tid.grid(row=2, column=11)

# search user button
b1 = tk.Button(my_w, text='Search User', width=12, bg='light grey', command=lambda: search(tid.get('1.0', END)))
b1.grid(row=2, column=12)

# output Label
my_str = tk.StringVar()

l2 = tk.Label(my_w,  textvariable=my_str, width=30, fg='red')
l2.grid(row=3, column=10, columnspan=2)

my_str.set("Output")

# add employee label
lEmp = tk.Label(my_w,  text='Add Employee', font=('Helvetica', 12), width=30, anchor="c")
lEmp.grid(row=0, column=5, columnspan=4)

# ID label for add_data()
lid2 = tk.Label(my_w,  text='ID: ', width=10, anchor="c")
lid2.grid(row=2, column=6)

# ID text box for add_data()
tid2 = tk.Text(my_w,  height=1, width=10, bg='white')
tid2.grid(row=2, column=7)

# name label for add_data()
lName = tk.Label(my_w,  text='Name: ', width=10, anchor="c")
lName.grid(row=3, column=6)

# name text box for add_data()
tName = tk.Text(my_w,  height=1, width=10, bg='white')
tName.grid(row=3, column=7)

# surname label for add_data()
lsname = tk.Label(my_w,  text='Surname: ', width=10, anchor="c")
lsname.grid(row=4, column=6)

# surname text box for add_data()
tsname = tk.Text(my_w,  height=1, width=10, bg='white')
tsname.grid(row=4, column=7)

# asset label for add_data()
lAsset = tk.Label(my_w,  text='Asset: ', width=10)
lAsset.grid(row=5, column=6)

# options menu for add_data()
options = StringVar(my_w)
options.set("")  # default value

opt1 = OptionMenu(my_w, options, "Car", "Mobile", "Laptop")
opt1.grid(row=5, column=7)

# add record button for add_data()
bAdd = tk.Button(my_w,  text='Add Record', width=10, bg='light grey', command=lambda: add_data())
bAdd.grid(row=7, column=7)

# add update label
lUpdate = tk.Label(my_w,  text='Update Asset', font=('Helvetica', 12), width=30, anchor="c")
lUpdate.grid(row=10, column=6, columnspan=4)

# ID label for update()
lid2 = tk.Label(my_w,  text='ID: ', width=8, anchor="c")
lid2.grid(row=12, column=6)

# ID text box for update()
tid3 = tk.Text(my_w,  height=1, width=10, bg='white')
tid3.grid(row=12, column=7)

# options menu for update()
options2 = StringVar(my_w)
options2.set("")  # default value

opt2 = OptionMenu(my_w, options2, "Car", "Mobile", "Laptop")
opt2.grid(row=13, column=7)

# add record button for update()
bUpdate = tk.Button(my_w,  text='Update Record', width=12, bg='light grey', command=lambda: update())
bUpdate.grid(row=14, column=7)

# add delete label
lDelete = tk.Label(my_w,  text='Delete Record', font=('Helvetica', 12), width=30, anchor="c")
lDelete.grid(row=10, column=10, columnspan=4)

# ID label for delete()
lid3 = tk.Label(my_w,  text='ID: ', width=10, anchor="c")
lid3.grid(row=12, column=10)

# ID text box for delete()
tid4 = tk.Text(my_w,  height=1, width=10, bg='white')
tid4.grid(row=12, column=11)

# add button for delete()
bDelete = tk.Button(my_w,  text='Delete Record', width=10, bg='light grey', command=lambda: delete())
bDelete.grid(row=14, column=11)

# exit button
bExit = tk.Button(my_w, text='Exit', width=8, bg='light grey', command=my_w.destroy)
bExit.grid(row=50, column=50)

countdown(500)

my_w.mainloop()

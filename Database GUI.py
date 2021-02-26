import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import *

# connect to database
my_conn = sqlite3.connect('Asset Tracking.s3db')

# display window
my_w = tk.Tk()
my_w.geometry("1150x300")


# function to display data from database on window
def display_data():
    r_set = my_conn.execute('''SELECT * from User''')  # select all from the User table
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


# function to add data into database
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
            """, (my_id, my_name, my_surname, my_asset))  # SQL to insert user details into database 
            my_conn.commit()
            display_data()
            options.set("")  # reset the option menu
            tid2.delete('1.0', END)  # reset the text entry box
            tName.delete('1.0', END)  # reset the text entry box
            tsname.delete('1.0', END)  # reset the text entry box
        else: # if the input was invalid, throw error
            messagebox.showerror("Error", "Invalid input")
    except: # if the input was invalid, throw error
        messagebox.showerror("Error", "Invalid input")


# function to search for the specified user 
def search(id):
    try:
        int(id)  # check input is integer or not
        try:
            q = "SELECT * FROM User WHERE ID= "+id  # select all from the table which have the specified ID
            my_cursor = my_conn.execute(q)
            data_row = my_cursor.fetchone()
            my_str.set(data_row)
        except sqlite3.Error as my_error:  # if there was an error with the database, throw error
            print("error: ", my_error)
    except:  # if there was invalid input, throw error
        my_str.set("Check input")


# function that counts down to terminate the program
def countdown(time):
    if time == -1:  # if the time reaches -1, terminate the program
        my_w.destroy()
    else:
        l4 = tk.Label(my_w, text="time remaining: %d seconds" % time)  # show with a label how much time is left
        l4.grid(row=50, column=51)

        my_w.after(1000, countdown, time-1)  # every 1000 ms countdown by 1 each time


display_data()  # display table with table data

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

my_str.set("Output")  # set the label by default with this string value

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
bAdd = tk.Button(my_w,  text='Add Record', width=10, command=lambda: add_data())
bAdd.grid(row=7, column=7)

# exit button
bExit = tk.Button(my_w, text='Exit', width=8, bg='light grey', command=my_w.destroy)
bExit.grid(row=50, column=50)

countdown(500)  # call countdown function from 500 s

my_w.mainloop()

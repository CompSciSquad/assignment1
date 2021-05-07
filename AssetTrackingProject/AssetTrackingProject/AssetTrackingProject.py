
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import webbrowser

# connect to database
my_conn = sqlite3.connect('Asset Tracking.s3db')

# region FrameStructure
root = tk.Tk()

root.rowconfigure(0, weight=1)
root.columnconfigure(0,weight=1)

my_w_1 = Frame(root)
my_w_2 = Frame(root)

root.title("Asset Tracking")

def raise_frame(frame):
    frame.tkraise()

#endregion

def _login_btn_clicked():
    username = entry_username.get()
    password = entry_password.get()
    check = var1.get()

    if username == "abc" and password == "123" and check == 1:
        raise_frame(my_w_1)
    elif username == "abc" and password == "123" and check == 0:
        messagebox.showerror("Login error", "Accept Terms and Conditions to continue")
    else:
        messagebox.showerror("Login error", "Incorrect username or password")


def callback(event):
    webbrowser.open_new("https://www.dropbox.com/s/ncqv6pfuj00ecz8/Asset_Policy.html?dl=0")


label_username = tk.Label(my_w_2, text="Username")
label_password = tk.Label(my_w_2, text="Password")

entry_username = tk.Entry(my_w_2)
entry_password = tk.Entry(my_w_2, show="*")

label_username.grid(row=3, sticky='ne')
label_password.grid(row=4, sticky='ne')
entry_username.grid(row=3, column=1)
entry_password.grid(row=4, column=1)

logBtn = tk.Button(my_w_2, text="Log In", bg="light grey", command=_login_btn_clicked)
logBtn.grid(columnspan=2)

var1 = IntVar()
checkBtn = tk.Checkbutton(my_w_2, text="Accept terms and conditions", onvalue=1, offvalue=0, variable=var1).grid(row=9, column=2, sticky=W)


link = tk.Label(my_w_2, text="Policy Document Link", fg="blue", cursor="hand2")
link.grid(row=9, column=3)
link.bind("<Button-1>", callback)

lLogin = tk.Label(my_w_2,  text='Administrator Log In', font=('Helvetica', 12), width=30, anchor="c")
lLogin.grid(row=0, column= 1)

canvas = Canvas(my_w_2, width = 300, height = 300)
canvas.grid(row=20, column=5)
img = PhotoImage(file = "Asset.png")
canvas.create_image(20, 20, anchor=NW, image=img)


#region 2ND WINDOW

# function to display data from database on window
def display_data():
    r_set = my_conn.execute('''SELECT * from User''')  # select all from the User table
    i = 1  # row value inside the loop
    for user in r_set:
        for j in range(len(user)):
            e = Entry(my_w_1, width=10, fg='blue')
            e.grid(row=i, column=j)
            e.insert(END, user[j])
        i = i+1

    e = Label(my_w_1, width=10, text='ID', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
    e.grid(row=0, column=0)
    e = Label(my_w_1, width=10, text='Name', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
    e.grid(row=0, column=1)
    e = Label(my_w_1, width=10, text='Surname', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
    e.grid(row=0, column=2)
    e = Label(my_w_1, width=10, text='Asset', borderwidth=2, relief='ridge', anchor='w', bg='grey', fg='white')
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
            messagebox.showinfo("Employee Details", f"ID: {data_row[0]}\nName: {data_row[1]}\nSurname: {data_row[2]}\nAsset: {data_row[3]}" )
        except sqlite3.Error as my_error:  # if there was an error with the database, throw error
            print("error: ", my_error)
    except:  # if there was invalid input, throw error
        messagebox.showerror("Error","Check input")


# function that counts down to terminate the program
def countdown(time):
    if time == -1:  # if the time reaches -1, terminate the program
        my_w_1.destroy()
    else:
        l4 = tk.Label(my_w_1, text="time remaining: %d seconds" % time)  # show with a label how much time is left
        l4.grid(row=50, column=51)

        my_w_1.after(1000, countdown, time-1)  # every 1000 ms countdown by 1 each time

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
    options2.set("")


def delete():
    my_id3 = tid4.get('1.0', END)  # read name
    r_set = my_conn.execute("""DELETE FROM User WHERE ID=""" + my_id3)
    my_conn.commit()
    messagebox.showerror("Deleted ", "Record deleted")
    display_data()

def destroy_frames():
    my_w_1.destroy()
    my_w_2.destroy()
    root.destroy()

display_data()  # display table with table data

# add employee label
lSearch = tk.Label(my_w_1,  text='Search Employee', font=('Helvetica', 12), width=30, anchor="c")
lSearch.grid(row=0, column=9, columnspan=4)

# ID Label for search
lid = tk.Label(my_w_1,  text='Enter User ID: ', width=25)
lid.grid(row=2, column=10)

# ID text box for search
tid = tk.Text(my_w_1,  height=1, width=5)
tid.grid(row=2, column=11)

# search user button
b1 = tk.Button(my_w_1, text='Search User', width=12, bg='light grey', command=lambda: search(tid.get('1.0', END)))
b1.grid(row=2, column=12)

# output Label
# my_str = tk.StringVar()

# l2 = tk.Label(my_w_1,  textvariable=my_str, width=30, fg='red')
# l2.grid(row=3, column=10, columnspan=2)

# my_str.set("Output")  # set the label by default with this string value

# add employee label
lEmp = tk.Label(my_w_1,  text='Add Employee', font=('Helvetica', 12), width=30, anchor="c")
lEmp.grid(row=0, column=5, columnspan=4)

# ID label for add_data()
lid2 = tk.Label(my_w_1,  text='ID: ', width=10, anchor="c")
lid2.grid(row=2, column=6)

# ID text box for add_data()
tid2 = tk.Text(my_w_1,  height=1, width=10, bg='white')
tid2.grid(row=2, column=7)

# name label for add_data()
lName = tk.Label(my_w_1,  text='Name: ', width=10, anchor="c")
lName.grid(row=3, column=6)

# name text box for add_data()
tName = tk.Text(my_w_1,  height=1, width=10, bg='white')
tName.grid(row=3, column=7)

# surname label for add_data()
lsname = tk.Label(my_w_1,  text='Surname: ', width=10, anchor="c")
lsname.grid(row=4, column=6)

# surname text box for add_data()
tsname = tk.Text(my_w_1,  height=1, width=10, bg='white')
tsname.grid(row=4, column=7)

# asset label for add_data()
lAsset = tk.Label(my_w_1,  text='Asset: ', width=10)
lAsset.grid(row=5, column=6)

# options menu for add_data()
options = StringVar(my_w_1)
options.set("")  # default value

opt1 = OptionMenu(my_w_1, options, "Car", "Mobile", "Laptop")
opt1.grid(row=5, column=7)

# add record button for add_data()
bAdd = tk.Button(my_w_1,  text='Add Record', width=10, bg='light grey', command=lambda: add_data())
bAdd.grid(row=7, column=7)

# add update label
lUpdate = tk.Label(my_w_1,  text='Update Asset', font=('Helvetica', 12), width=30, anchor="c")
lUpdate.grid(row=10, column=6, columnspan=4)

# ID label for update()
lid2 = tk.Label(my_w_1,  text='ID: ', width=8, anchor="c")
lid2.grid(row=12, column=6)

# ID text box for update()
tid3 = tk.Text(my_w_1,  height=1, width=10, bg='white')
tid3.grid(row=12, column=7)

# options menu for update()
options2 = StringVar(my_w_1)
options2.set("")  # default value

opt2 = OptionMenu(my_w_1, options2, "Car", "Mobile", "Laptop")
opt2.grid(row=13, column=7)

# add record button for update()
bUpdate = tk.Button(my_w_1,  text='Update Record', width=12, bg='light grey', command=lambda: update())
bUpdate.grid(row=14, column=7)

# add delete label
lDelete = tk.Label(my_w_1,  text='Delete Record', font=('Helvetica', 12), width=30, anchor="c")
lDelete.grid(row=10, column=10, columnspan=4)

# ID label for delete()
lid3 = tk.Label(my_w_1,  text='ID: ', width=10, anchor="c")
lid3.grid(row=12, column=10)

# ID text box for delete()
tid4 = tk.Text(my_w_1,  height=1, width=10, bg='white')
tid4.grid(row=12, column=11)

# add button for delete()
bDelete = tk.Button(my_w_1,  text='Delete Record', width=10, bg='light grey', command=lambda: delete())
bDelete.grid(row=14, column=11)

# exit button
bExit = tk.Button(my_w_1, text='Exit', width=8, bg='light grey', command=lambda: destroy_frames())
bExit.grid(row=50, column=50)

#endregion


#loads the frames into program
for frame in (my_w_1, my_w_2):
    frame.grid(row=0, column=0,sticky='nsew')

countdown(500)  # call countdown function from 500 s
root.mainloop()
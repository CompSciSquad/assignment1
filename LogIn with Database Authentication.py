import tkinter as tk
from tkinter import *
import tkinter.messagebox as tm
import sqlite3
import webbrowser

#User ID: 1046
#Password: 1046

# Connect to database
db = sqlite3.connect('Asset Tracking.s3db')
c = db.cursor()

# Window
my_w = tk.Tk()
my_w.geometry("400x250")
my_w.title('LogIn page')

# User ID Label
l1 = tk.Label(my_w,  text='Enter User ID: ', width=20)
l1.grid(row=0, column=0)

# Add text box for ID
t1 = tk.Text(my_w,  height=1, width=5, bg='grey', fg='white')
t1.grid(row=0, column=1)

# Password Label
l2 = tk.Label(my_w,  text='Enter password: ', width=20)
l2.grid(row=1, column=0)

# Add text box for Password
t2 = Entry(width=7, bg='grey', fg='white', show='*')
t2.grid(row=1, column=1)

# LogIn button
b1 = tk.Button(my_w, text='Log In', width=10, bg='light grey', command=lambda: my_details(t1.get('1.0', END), t2.get()))
b1.grid(row=7, column=1)


# User details function
def my_details(uid, passw):
    try:
        # check input is integer or not
        int(uid)
        int(passw)
        try:
            check = var1.get()
            # SQL statement to check for the entered ID and password 
            c.execute('SELECT * FROM User_Passwords WHERE ID = ? AND Password = ?', (uid, passw))

            if c.fetchall() and check == 1:  # if the details were found, login is successful
                tm.showinfo("Success", "Welcome")
            elif c.fetchall() or check == 0:  #  if the details were found but the user does't agree to the terms, then login failed
                tm.showerror("Login error", "Accept Terms and Conditions to continue")
            else:  # if the details weren't found then login failed
                tm.showerror("Login error", "Incorrect username or password")
        except sqlite3.Error as my_error:  # if there was an error with the database then print that there was an error
            print("error: ", my_error)
    except:  #if user input was invalid then throw error
        tm.showerror("Error", "Check Input") 


# check box for Terms & Conditions
var1 = IntVar()
Checkbutton(my_w, text="Accept terms and conditions", onvalue=1, offvalue=0,  variable=var1).grid(row=8, column=0,
                                                                                                  sticky=W)

# function for the webpage link to the Terms & Conditions
def callback(event):
    webbrowser.open_new("https://www.dropbox.com/s/ncqv6pfuj00ecz8/Asset_Policy.html?dl=0")


# Policy document label that redirects the user to the webpage when clicked
link = Label(my_w, text="Policy Document Link", fg="blue", cursor="hand2")
link.grid(row=9, column=0)
link.bind("<Button-1>", callback)

my_w.mainloop()

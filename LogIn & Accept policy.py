from tkinter import *
from functools import partial
import webbrowser


def validate_login(username, password):
    print("username entered :", username.get())
    print("password entered :", password.get())
    return


# window
tkWindow = Tk()
tkWindow.geometry('400x150')
tkWindow.title('Login Form')

# username label and text entry box
usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)

# password label and password entry box
passwordLabel = Label(tkWindow, text="Password").grid(row=1, column=0)
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)

validateLogin = partial(validate_login, username, password)

# login button
loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=5, column=1)

var1 = IntVar()
Checkbutton(tkWindow, text="Accept terms and conditions", variable=var1).grid(row=6, column=3, sticky=W)


def callback(event):
    webbrowser.open_new("file:///C:/Users/tasos/Downloads/Asset_Policy.html")


link = Label(tkWindow, text="Policy Document Link", fg="blue", cursor="hand2")
link.grid(row=7, column=3)
link.bind("<Button-1>", callback)

tkWindow.mainloop()

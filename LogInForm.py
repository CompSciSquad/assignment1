import tkinter as tk
import tkinter.messagebox as tm
import webbrowser
from tkinter import *


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class LoginFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.logBtn = Button(self, text="Log In", command=self._login_btn_clicked)
        self.logBtn.grid(columnspan=2)

        self.var1 = IntVar()
        self.checkBtn = Checkbutton(self, text="Accept terms and conditions", onvalue=1, offvalue=0, variable=self.var1
                                    ).grid(row=6, column=3, sticky=W)

        def callback():
            webbrowser.open_new("file:///C:/Users/tasos/Downloads/Asset_Policy.html")

        link = Label(self, text="Policy Document Link", fg="blue", cursor="hand2")
        link.grid(row=7, column=3)
        link.bind("<Button-1>", callback)

    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()
        check = self.var1.get()

        # print(username, password)
        if username == "abc" and password == "123" and check == 1:
            self.parent.switch_frame(PageOne)
        elif username == "abc" and password == "123" and check == 0:
            tm.showerror("Login error", "Accept Terms and Conditions to continue")
        else:
            tm.showerror("Login error", "Incorrect username or password")


class PageOne(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to login page",
                  command=lambda: parent.switch_frame(LoginFrame)).pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

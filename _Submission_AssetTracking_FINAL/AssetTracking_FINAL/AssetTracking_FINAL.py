

import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import webbrowser
from tkinter.ttk import Treeview


# connect to database
my_conn = sqlite3.connect('AssetTrackingFull_creds.s3db')
cur = my_conn.cursor()

# region FrameStructure
root = tk.Tk()

root.rowconfigure(0, weight=1)
root.columnconfigure(0,weight=1)

AdminFrame = Frame(root, bg ="lightcyan1")
EmployeeFrame = Frame(root, bg = "lightcyan1")
LoginFrame = Frame(root, bg = "lightcyan1")
root.geometry('385x360')
root.title("Asset Tracking")
root.resizable(False, False)

def raise_frame(frame):
    frame.tkraise()

#endregion


# function that counts down to terminate the program
def countdown(time, frame):
    if time == -1: 
        AdminFrame.destroy()
        LoginFrame.destroy()
        EmployeeFrame.destroy()
        root.destroy()
    else:
        l4 = tk.Label(frame, text="Time remaining: %d seconds" % time, anchor='w', bg = "lightcyan1")  # show with a label how much time is left
        l4.grid(row=11, column=0)

        frame.after(1000, countdown, time-1, frame)  # every 1000 ms countdown by 1 each time


#region LoginFrame
def _login_btn_clicked():

    username = entry_username.get()
    password = entry_password.get()
    check = var1.get()

    search_user(username, password, check)

#Function to search database for User information, raises appropriiate frame
def search_user(user, password, check):
    query = "SELECT * FROM Credentials WHERE Username = '" + user + "' AND Password = '" + password + "'"  

    result = find_record(my_conn, query)

    if not result:
        messagebox.showerror("Error ", "Invalid username/password")     
        
    elif result and check == 0:
        messagebox.showerror("Login error", "Accept Terms and Conditions to continue")

    elif result and check == 1:
        subquery = "SELECT * FROM Credentials WHERE Username = '" + user + "' AND Admin = 'y'"
        result2 = find_record(my_conn, subquery)

        if result2:
            for frame in (AdminFrame, LoginFrame):
                frame.grid(row=0, column=0,sticky='nsew')
            raise_frame(AdminFrame)
            root.geometry('1000x400')
            countdown(500, AdminFrame)

        elif not result2:
            for frame in (EmployeeFrame, LoginFrame):
                frame.grid(row=0, column=0,sticky='nsew')
            raise_frame(EmployeeFrame)
            root.geometry('780x400')
            countdown(500, EmployeeFrame)

def callback(event):
    webbrowser.open_new("https://www.dropbox.com/s/ncqv6pfuj00ecz8/Asset_Policy.html?dl=0")

label_username = tk.Label(LoginFrame, text="Username", anchor="e", bg = "lightcyan1")
label_password = tk.Label(LoginFrame, text="Password", anchor="e", bg = "lightcyan1")

entry_username = tk.Entry(LoginFrame)
entry_password = tk.Entry(LoginFrame, show="*")

label_username.grid(row=3, sticky='ne')
label_password.grid(row=4, sticky='ne')
entry_username.grid(row=3, column=1)
entry_password.grid(row=4, column=1)

logBtn = tk.Button(LoginFrame, text="Log In", bg="white", command=_login_btn_clicked)
logBtn.grid(columnspan=2)

var1 = IntVar()
checkBtn = tk.Checkbutton(LoginFrame, text="Accept terms and conditions", onvalue=1, offvalue=0, variable=var1, bg = "lightcyan1").grid(row=6, column=1, sticky=W)


link = tk.Label(LoginFrame, text="Policy Document Link", fg="blue", cursor="hand2", bg = "lightcyan1")
link.grid(row=7, column=1)
link.bind("<Button-1>", callback)

lLogin = tk.Label(LoginFrame,  text='Administrator Log In', font=('Helvetica', 12), width=30, anchor="c", bg = "lightcyan1")
lLogin.grid(row=0, column= 1)

canvas = Canvas(LoginFrame, width = 200, height = 200, bg = "lightcyan1", highlightthickness = 0)
canvas.grid(row=20, column=1)
img = PhotoImage(file = "Asset.png")
canvas.create_image(10, 10, anchor=NW, image=img)
#endregion 

#region 2ND_WINDOW_Functions 

def select_user(event): # when user clicks on an entry in the data grid table the selected record is inputted into the 'add employee' boxes
    try:
        clear_boxes()   # function called to reset all text boxes
        global selected_item
        index = Admin_asset_tree_view.selection()[0]                
        selected_item = Admin_asset_tree_view.item(index)['values'] 
        tid2.insert(END, selected_item[0])                      
        tName.insert(END, selected_item[1])                    
        tsname.insert(END, selected_item[2])                    
        options.set(selected_item[3])                           
    except IndexError:
        pass

# function to display data from database on AdminFrame
def display_data():
    for index in Admin_asset_tree_view.get_children():           # loops through all records in the data grid. get_children() returns a list of all row's iid
        Admin_asset_tree_view.delete(index)                      # iterate through all rows, passing the iid to the delete() method to clear the grid ready for population
    r_set = my_conn.execute('''SELECT * from User''')     
    for user in r_set:                                           # for each user record retrieved from the database
        Admin_asset_tree_view.insert('', 'end', values=user)     # insert record into the data grid as a new unique entry

# function to display data from database on EmployeeFrame  
def display_data_emp():
    for index in asset_tree_view.get_children():           
        asset_tree_view.delete(index)                      
    r_set = my_conn.execute('''SELECT * from User''')      
    for user in r_set:                                     
        asset_tree_view.insert('', 'end', values=user)    

# function to add data into database
def add_data():
    try:
        my_id = tid2.get('1.0', END)        
        my_asset = options.get()           
        my_name = tName.get('1.0', END)     
        my_surname = tsname.get('1.0', END) 
        
        if int(my_id):
            my_conn.execute("""INSERT INTO User(ID, Name, Surname, Asset)
            VALUES (?,?,?,?)
            """, (my_id, my_name, my_surname, my_asset))  # SQL to insert user details into database 
            my_conn.commit()
            display_data()                  
            clear_boxes()                   
        else: 
            messagebox.showerror("Error", "Invalid input")
    except: 
        messagebox.showerror("Error", "Invalid input")

# function that can be called to reset/clear all textboxes
def clear_boxes():
    options.set("Select Asset")  
    tid2.delete('1.0', END)      
    tName.delete('1.0', END)     
    tsname.delete('1.0', END)    
    tid4.delete('1.0', END)      

# function to search for the specified user 
def search(id):
    try:
        int(id)  
        try:
            q = "SELECT * FROM User WHERE ID= "+id  
            my_cursor = my_conn.execute(q)
            data_row = my_cursor.fetchone()
            messagebox.showinfo("Employee Details", f"ID: {data_row[0]}\nName: {data_row[1]}\nSurname: {data_row[2]}\nAsset: {data_row[3]}" )
        except sqlite3.Error as my_error:  # if there was an error with the database, throw error
            print("error: ", my_error)
    except:  # if there was invalid input, throw error
        messagebox.showerror("Error","Check input")

def update():
    my_asset2 = options2.get()      
    my_id2 = tid3.get('1.0', END)  
    r_set = my_conn.execute("""UPDATE User SET Asset= ? WHERE ID= ?""", (my_asset2, my_id2))
    my_conn.commit()
    messagebox.showinfo("Updated", "Record updated")
    display_data()
    tid3.delete('1.0', END)
    options2.set("Select Asset")


def delete():
    my_id3 = tid4.get('1.0', END)           
    if len(tid4.get("1.0", END)) <= 1 :     # if the length of the inputted data in the delete text box is less than 0 (box is empty)
        my_id3 = tid2.get('1.0', END)       # take the ID value from the 'add ID' textbox which was populated by user selection

    result = find_record(my_conn, """SELECT * FROM User WHERE ID=""" + my_id3)  

    if not result:
        messagebox.showerror("Error ", "Record does not exist")            
    else:
        r_set = my_conn.execute("""DELETE FROM User WHERE ID=""" + my_id3)  
        my_conn.commit()    
        messagebox.showerror("Deleted ", "Record deleted")
        clear_boxes()       
        display_data()      # update the data grid and re-display correct records

def find_record(connection, query):
    cursor = connection.cursor()
    result = None
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def destroy_frames():
    AdminFrame.destroy()
    LoginFrame.destroy()
    root.destroy()

#endregion

# DATA GRID for AdminFrame
Admin_asset_frame = Frame(AdminFrame)
Admin_asset_frame.grid(row=0, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

columns = ['ID', 'Name', 'Surname', 'Asset']                                # set column headings
Admin_asset_tree_view = Treeview(Admin_asset_frame, columns=columns, show="headings")   # creates treeview widget, asset tree_view, in the asset_frame with specified column names
Admin_asset_tree_view.column("ID", width=20)          
for col in columns[0:]:                         # for all columns in the data 
    Admin_asset_tree_view.column(col, width=120)      # set each column width, looking through column names from the above array
    Admin_asset_tree_view.heading(col, text=col)      # set column heading to the text from the columns array
Admin_asset_tree_view.bind('<<TreeviewSelect>>', select_user)
Admin_asset_tree_view.pack(side="left", fill="y")
Admin_scrollbar = Scrollbar(Admin_asset_frame, orient='vertical')   # creates a vertical scrollbar widget for the data grid
Admin_scrollbar.configure(command=Admin_asset_tree_view.yview)
Admin_scrollbar.pack(side="right", fill="y")                  # sets scrollbar to right aligned
Admin_asset_tree_view.config(yscrollcommand=Admin_scrollbar.set)

display_data()  # display table with table data

#LabelFrame for Add Data Function
label_frame_AddData = LabelFrame(AdminFrame, text='Add Employee',bg="lightcyan1")
label_frame_AddData.grid(row=0,column=5,rowspan=5,columnspan=3,sticky=N)
# ID label for add_data()
lid2 = tk.Label(label_frame_AddData,  text='ID: ', width=10, anchor="e", font=('bold', 10), bg = "lightcyan1")
lid2.grid(row=1, column=6, sticky = E)

# ID text box for add_data()
tid2 = tk.Text(label_frame_AddData,  height=1, width=10, bg='white')
tid2.grid(row=1, column=7)

# name label for add_data()
lName = tk.Label(label_frame_AddData,  text='Name: ', width=10, anchor="e", font=('bold', 10), bg = "lightcyan1")
lName.grid(row=2, column=6, sticky = E)

# name text box for add_data()
tName = tk.Text(label_frame_AddData,  height=1, width=10, bg='white')
tName.grid(row=2, column=7)

# surname label for add_data()
lsname = tk.Label(label_frame_AddData,  text='Surname: ', width=10, anchor="e", font=('bold', 10), bg = "lightcyan1")
lsname.grid(row=3, column=6, sticky = E)

# surname text box for add_data()
tsname = tk.Text(label_frame_AddData,  height=1, width=10, bg='white')
tsname.grid(row=3, column=7)

# asset label for add_data()
lAsset = tk.Label(label_frame_AddData,  text='Asset: ', width=10, anchor="e", font=('bold', 10), bg = "lightcyan1")
lAsset.grid(row=4, column=6, sticky = E)

# options menu for add_data()
options = StringVar(label_frame_AddData)
options.set("Select Asset")  # default value

opt1 = OptionMenu(label_frame_AddData, options, "Car", "Mobile", "Laptop")
opt1.config(width = 10)
opt1.grid(row=4, column=7)

# add record button for add_data()
bAdd = tk.Button(label_frame_AddData,  text='Add Record', width=10, bg="white", command=lambda: add_data())
bAdd.grid(row=5, column=7)

#LabelFrame for Update Function
label_frame_UpdateLabel = LabelFrame(AdminFrame, text='Update Asset',bg="lightcyan1")
label_frame_UpdateLabel.grid(row=4,column=6,rowspan=4,columnspan=1,sticky=N)
# ID label for update()
lid2 = tk.Label(label_frame_UpdateLabel,  text='ID: ', width=6, anchor="e", font=('bold', 10), bg = "lightcyan1")
lid2.grid(row=10, column=6)

# ID text box for update()
tid3 = tk.Text(label_frame_UpdateLabel,  height=1, width=10, bg='white')
tid3.grid(row=10, column=7)

# options menu for update()
options2 = StringVar(label_frame_UpdateLabel)
options2.set("Select Asset")  # default value

opt2 = OptionMenu(label_frame_UpdateLabel, options2, "Car", "Mobile", "Laptop")
opt2.config(width = 10)
opt2.grid(row=12, column=7)

# add record button for update()
bUpdate = tk.Button(label_frame_UpdateLabel,  text='Update Record', width=12, bg='white', command=lambda: update())
bUpdate.grid(row=14, column=7)

#LabelFrame for Delete Function
label_frame_DeleteLabel = LabelFrame(AdminFrame, text='Delete Record',bg="lightcyan1")
label_frame_DeleteLabel.grid(row=0,column=10,rowspan=3,columnspan=1,sticky=N)
# ID label for delete()
lid3 = tk.Label(label_frame_DeleteLabel,  text='ID: ', width=6, anchor="e", font=('bold', 10), bg = "lightcyan1")
lid3.grid(row=4, column=10, sticky = 'ne')

# ID text box for delete()
tid4 = tk.Text(label_frame_DeleteLabel,  height=1, width=10, bg='white')
tid4.grid(row=4, column=11, sticky = 'ne')

# add button for delete()
bDelete = tk.Button(label_frame_DeleteLabel,  text='Delete Record', width=10, bg='white', command=lambda: delete())
bDelete.grid(row=6, column=11)

#LabelFrame for Search Function
label_frame_SearchGrid = LabelFrame(AdminFrame, text='Search Record',bg="lightcyan1")
label_frame_SearchGrid.grid(row=4,column=10,rowspan=4,columnspan=2,sticky=N)
# ID Label for search
lid_e = tk.Label(label_frame_SearchGrid,  text='Enter User ID: ', width=11, font = ('bold', 10), anchor = "e", bg = "lightcyan1")
lid_e.grid(row=4, column=10)

# ID text box for search
tid_e = tk.Text(label_frame_SearchGrid,  height=1, width=6)
tid_e.grid(row=4, column=11)

# search user button
b1_e = tk.Button(label_frame_SearchGrid, text='Search User', width=10, bg='white', command=lambda: search(tid_e.get('1.0', END)), font = ('bold', 10))
b1_e.grid(row=5, column=11)

# exit button
bExit = tk.Button(AdminFrame, text='Exit', width=8, bg='white', command=lambda: destroy_frames())
bExit.grid(row=10, column=0)


'''Following code is for the Employee Frame'''

# DATA GRID for EmployeeFrame
asset_frame = Frame(EmployeeFrame)
asset_frame.grid(row=0, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

columns = ['ID', 'Name', 'Surname', 'Asset']                               
asset_tree_view = Treeview(asset_frame, columns=columns, show="headings")   
asset_tree_view.column("ID", width=20)          
for col in columns[0:]:                         
    asset_tree_view.column(col, width=120)     
    asset_tree_view.heading(col, text=col)      
asset_tree_view.bind('<<TreeviewSelect>>', select_user)
asset_tree_view.pack(side="left", fill="y")
scrollbar = Scrollbar(asset_frame, orient='vertical')   
scrollbar.configure(command=asset_tree_view.yview)
scrollbar.pack(side="right", fill="y")                  
asset_tree_view.config(yscrollcommand=scrollbar.set)

display_data_emp()  # display table with table data

#LabelFrame for Search Function
label_frame_SearchGrid = LabelFrame(EmployeeFrame, text='Search Record',bg="lightcyan1")
label_frame_SearchGrid.grid(row=0,column=5,rowspan=4,columnspan=2,sticky=N)
# ID Label for search
lid = tk.Label(label_frame_SearchGrid,  text='Enter User ID: ', width=11, font = ('bold', 10), anchor = "e", bg = "lightcyan1")
lid.grid(row=4, column=5)

# ID text box for search
tid = tk.Text(label_frame_SearchGrid,  height=1, width=6)
tid.grid(row=4, column=6)

# search user button
b1 = tk.Button(label_frame_SearchGrid, text='Search User', width=10, bg='white', command=lambda: search(tid.get('1.0', END)), font = ('bold', 10))
b1.grid(row=5, column=6)

# exit button
bExit = tk.Button(EmployeeFrame, text='Exit', width=8, bg='white', command=lambda: destroy_frames())
bExit.grid(row=10, column=0)

#endregion

#loads the frames into program
for frame in (AdminFrame, LoginFrame, EmployeeFrame):
    frame.grid(row=0, column=0,sticky='nsew')

root.mainloop()


from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
import sqlite3



class Database:



    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS User (UID integer primary key, Name text, Surname text, Asset text)")
        self.conn.commit()

    def fetch(self, UID=''):
        self.cur.execute(
            "SELECT * FROM User WHERE ID LIKE ?", ('%'+UID+'%',))
        rows = self.cur.fetchall()
        return rows

    def fetch2(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def insert(self, UID, Name, Surname, Asset):
        self.cur.execute("INSERT INTO User VALUES ( ?, ?, ?, ?)", #NULL,
                         (UID, Name, Surname, Asset))
        self.conn.commit()

    def remove(self, UID):
        self.cur.execute("DELETE FROM User WHERE id=?", (UID,))
        self.conn.commit()

    def update(self, UID, Name, Surname, Asset):
        self.cur.execute("UPDATE User SET ID = ?, Name = ?, Surname = ?, Asset = ? WHERE row_number() = ?", #WHERE id = ?
                         (UID, Name, Surname, Asset, self))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


db = Database('Asset Tracking.s3db') 


def populate_list(UID=''):
    for i in router_tree_view.get_children():
        router_tree_view.delete(i)
    for row in db.fetch(UID):
        router_tree_view.insert('', 'end', values=row)

def populate_list2(query='select * from User'): 
    for i in router_tree_view.get_children():
        router_tree_view.delete(i)
    for row in db.fetch2(query):
        router_tree_view.insert('', 'end', values=row)

def add_user():
    if name_text.get() == '' or uid_text.get() == '' or surname_text.get() == '' or asset_text.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    db.insert(uid_text.get(), name_text.get(),
              surname_text.get(), asset_text.get())
    clear_text()
    populate_list()


def select_user(event):
    try:
        global selected_item
        index = router_tree_view.selection()[0]
        selected_item = router_tree_view.item(index)['values']
        uid_entry.delete(0, END)
        uid_entry.insert(END, selected_item[0])
        name_entry.delete(0, END)
        name_entry.insert(END, selected_item[1])
        surname_entry.delete(0, END)
        surname_entry.insert(END, selected_item[2])
        asset_entry.delete(0, END)
        asset_entry.insert(END, selected_item[3])
    except IndexError:
        pass

def remove_user():
    db.remove(selected_item[0])
    clear_text()
    populate_list()

def update_user():
    db.update(selected_item[0], uid_text.get(), name_text.get(),
              surname_text.get(), asset_text.get())
    populate_list()

def clear_text():
    name_entry.delete(0, END)
    uid_entry.delete(0, END)
    surname_entry.delete(0, END)
    asset_entry.delete(0, END)

def search_uid():
    uid = uid_search.get()
    populate_list(uid)


def execute_query():
    query = query_search.get()
    populate_list2(query)


app = Tk()
frame_search = Frame(app)
frame_search.grid(row=0, column=0)

lbl_search = Label(frame_search, text='Search by ID',
                   font=('bold', 12), pady=20)
lbl_search.grid(row=0, column=0, sticky=W)
uid_search = StringVar()
uid_search_entry = Entry(frame_search, textvariable=uid_search)
uid_search_entry.grid(row=0, column=1)

lbl_search = Label(frame_search, text='Search by Query',
                   font=('bold', 12), pady=20)
lbl_search.grid(row=1, column=0, sticky=W)
query_search = StringVar()
query_search.set("Select * from User") 
query_search_entry = Entry(frame_search, textvariable=query_search, width=40)
query_search_entry.grid(row=1, column=1)

frame_fields = Frame(app)
frame_fields.grid(row=1, column=0)
# ID
uid_text = StringVar()
uid_label = Label(frame_fields, text='ID', font=('bold', 12))
uid_label.grid(row=0, column=0, sticky=E)
uid_entry = Entry(frame_fields, textvariable=uid_text)
uid_entry.grid(row=0, column=1, sticky=W)
# NAME
name_text = StringVar()
name_label = Label(frame_fields, text='Name', font=('bold', 12))
name_label.grid(row=0, column=2, sticky=E)
name_entry = Entry(frame_fields, textvariable=name_text)
name_entry.grid(row=0, column=3, sticky=W)
# SURNAME
surname_text = StringVar()
surname_label = Label(frame_fields, text='Surname', font=('bold', 12))
surname_label.grid(row=1, column=0, sticky=E)
surname_entry = Entry(frame_fields, textvariable=surname_text)
surname_entry.grid(row=1, column=1, sticky=W)
# ASSET
asset_text = StringVar()
asset_label = Label(frame_fields, text='Asset', font=('bold', 12), pady=20)
asset_label.grid(row=1, column=2, sticky=E)
asset_entry = Entry(frame_fields, textvariable=asset_text)
asset_entry.grid(row=1, column=3, sticky=W)

frame_router = Frame(app)
frame_router.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

# DATA GRID
columns = ['ID', 'Name', 'Surname', 'Asset'] 
router_tree_view = Treeview(frame_router, columns=columns, show="headings")
router_tree_view.column("ID", width=20)
for col in columns[0:]:
    router_tree_view.column(col, width=120)
    router_tree_view.heading(col, text=col)
router_tree_view.bind('<<TreeviewSelect>>', select_user)
router_tree_view.pack(side="left", fill="y")
scrollbar = Scrollbar(frame_router, orient='vertical')
scrollbar.configure(command=router_tree_view.yview)
scrollbar.pack(side="right", fill="y")
router_tree_view.config(yscrollcommand=scrollbar.set)

# GUI BUTTONS
frame_btns = Frame(app)
frame_btns.grid(row=3, column=0)

add_btn = Button(frame_btns, text='Add User', width=12, command=add_user)
add_btn.grid(row=0, column=0, pady=20)

remove_btn = Button(frame_btns, text='Remove User',
                    width=12, command=remove_user)
remove_btn.grid(row=0, column=1)

update_btn = Button(frame_btns, text='Update User',
                    width=12, command=update_user)
update_btn.grid(row=0, column=2)

clear_btn = Button(frame_btns, text='Clear Input',
                   width=12, command=clear_text)
clear_btn.grid(row=0, column=3)

search_btn = Button(frame_search, text='Search ID',
                    width=12, command=search_uid)
search_btn.grid(row=0, column=2)

search_query_btn = Button(frame_search, text='Search Query',
                          width=12, command=execute_query)
search_query_btn.grid(row=1, column=2)

# MAIN FORM
app.title('Asset Tracking')
app.geometry('560x550')

# Populate data
populate_list()

# Start program
app.mainloop()



import socket
from typing import ForwardRef, Match
import pyodbc
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

LARGE_FONT = ("verdana", 13,"bold")

HOST = "127.0.0.1"
PORT = 65234
SERVER_NAME = "MON-PC\SQLEXPRESS"
DATABASE_NAME = 'BOOKSMANAGER'
FORMAT = "utf-8"

LOGIN = "login"
LOGOUT = "logout"
SIGNUP = "signup"
SEARCH = "search"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((HOST, PORT))
s.listen(1)

def run_Server():
    print('waiting')
    conn, addr = s.accept()
    
    # while True:
    #     print('waiting')
    #     conn, addr = s.accept()
    #     try:
    #          print('waiting')
    #     #     print('Connected by', addr)
    #     #     while True:
    #     #         data = conn.recv(1024)
    #     #         str_data = data.decode("utf8")
    #     #         if str_data == "quit":
    #     #             break
    #     #         """if not data:
    #     #             break
    #     #         """
    #     #         print("Client: " + str_data)

    #     #         # Server send input
    #     #         msg = input("Server: ")
    #     #         conn.sendall(bytes(msg, "utf8"))
    #     finally:
    #         conn.close()
    #         s.close()

    conn.close()
    s.close()


class Book_Admin(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # self.icon=PhotoImage(file='soccer_ball.png')
        # self.iconphoto(False,self.icon)
        self.title("Book Sever")
        self.geometry("500x200")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage,HomePage):
            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)


    def showFrame(self, container):
        
        frame = self.frames[container]
        if container==HomePage:
            self.geometry("500x350")
        else:
            self.geometry("500x200")
        frame.tkraise()

    # close-programe function
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def logIn(self,curFrame):

        user = curFrame.entry_user.get()
        pswd = curFrame.entry_pswd.get()

        if pswd == "":
            curFrame.label_notice["text"] = "password cannot be empty"
            return 

        if user == "admin" and pswd == "server":
            self.showFrame(HomePage)
            curFrame.label_notice["text"] = ""
        else:
            curFrame.label_notice["text"] = "invalid username or password"

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")
        
        
        label_title = tk.Label(self, text="\nLOG IN FOR SEVER\n", font=LARGE_FONT,fg='#20639b',bg="bisque2").grid(row=0,column=1)

        label_user = tk.Label(self, text="\tUSERNAME ",fg='#20639b',bg="bisque2",font='verdana 10 bold').grid(row=1,column=0)
        label_pswd = tk.Label(self, text="\tPASSWORD ",fg='#20639b',bg="bisque2",font='verdana 10 bold').grid(row=2,column=0)

        self.label_notice = tk.Label(self,text="",bg="bisque2",fg='red')
        self.entry_user = tk.Entry(self,width=30,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=30,bg='light yellow')

        button_log = tk.Button(self,text="LOG IN",bg="#20639b",fg='floral white',command=lambda: controller.logIn(self))

        button_log.grid(row=4,column=1)
        button_log.configure(width=10)
        self.label_notice.grid(row=3,column=1)
        self.entry_pswd.grid(row=2,column=1)
        self.entry_user.grid(row=1,column=1)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.configure(bg="bisque2")
        label_title = tk.Label(self, text="\n ACTIVE ACCOUNT ON SEVER\n", font=LARGE_FONT,fg='#20639b',bg="bisque2").pack()
        
        self.conent =tk.Frame(self)
        self.data = tk.Listbox(self.conent, height = 10, 
                  width = 40, 
                  bg='floral white',
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg='#20639b')
        
        # button_log = tk.Button(self,text="REFRESH",bg="#20639b",fg='floral white',command=self.Update_Client)
        # button_back = tk.Button(self, text="LOG OUT",bg="#20639b",fg='floral white' ,command=lambda: controller.showFrame(StartPage))

        button_log = tk.Button(self,text="REFRESH",bg="#20639b",fg='floral white')
        button_back = tk.Button(self, text="LOG OUT",bg="#20639b",fg='floral white')

        button_log.pack(side= BOTTOM)
        button_log.configure(width=10)
        button_back.pack(side=BOTTOM)
        button_back.configure(width=10)
        
        self.conent.pack_configure()
        self.scroll= tk.Scrollbar(self.conent)
        self.scroll.pack(side = RIGHT, fill= BOTH)
        self.data.config(yscrollcommand = self.scroll.set)
        
        self.scroll.config(command = self.data.yview)
        self.data.pack()
        
    # def Update_Client(self):
    #     self.data.delete(0,len(Live_Account))
    #     for i in range(len(Live_Account)):
    #         self.data.insert(i,Live_Account[i])
    


def connect_db():
    server = SERVER_NAME
    database = DATABASE_NAME
    username =  "sv"
    password = "svcntt"
    cnxn = pyodbc.Connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

def insert_new_client(user, pw):
    cursor = connect_db()
    cursor.execute('INSERT INTO MEMBERS(USERNAME, PASS_WORD) VALUES (?,?);', (user, pw))
    cursor.commit()

def check_clientSignup(username):
    if username == 'admin':
        return False
    cursor = connect_db()
    cursor.execute('SELECT M.USERNAME FROM MEMBERS M')
    for row in cursor:
        parse = str(row)
        parse_check = parse[2:]
        parse = parse_check.find("'")
        parse_check = parse_check[:parse]
        if parse_check == username:
            return False
        return True


live_Account = []
ID = []
AD = []

def check_liveAccount(username):
    for row in live_Account:
        parse = row.find("-")
        parse_check = row[(parse+1)]
        if parse_check == username:
            return False
        return True

def remove_liveAccount(conn, addr):
    for row in live_Account:
        parse = row.find("-")
        parse_check = row[:parse]
        if parse_check == str(addr):
            parse = row.find("-")
            AD.remove(parse_check)
            user = row[(parse+1):]
            ID.remove(user)
            live_Account.remove(row)
            conn.sendall("TRUE".encode(FORMAT))

def check_login(username, pw):
    cursor = connect_db()
    cursor.execute('SELECT M.USERNAME FROM MEMBERS M')
    if check_liveAccount(username) == False:
        return 0
    if username == 'admin' and pw == 'admin2021':
        return 1
    
    for row in cursor:
        parse = str(row)
        parse_check = parse[2:]
        parse = parse_check.find("'")
        parse_check = parse_check[:parse]
        if parse_check == username:
            cursor.execute('SELECT M.PASS_WORD FROM MEMBERS M WHERE M.USERNAME = (?)', (username))
            parse = str(cursor.fetchone())
            parse_check = parse[2:]
            parse = parse_check.find("'")
            parse_check = parse_check[:parse]
            if pw == parse_check:
                return 1
    return 2

def login(socket):
    user = socket.recv(1024).decode(FORMAT)
    print ("username: --" + user +"--")

    socket.sendall(user.encode(FORMAT))

    pw = socket.recv(1024).decode(FORMAT)
    print ("password: --" + pw + "--")

    accepted = check_login(user, pw)
    if accepted == 1:
        ID.append(user)
        account = str(AD[AD.__len__()-1]) + '-' + str(ID[ID.__len__()-1])
        live_Account.append(account)
    
    print ("accepted: ", accepted)
    socket.sendall(str(accepted).encode(FORMAT))
    print ("end-login")
    print ("")

def signup(socket, addr):
    user = socket.recv(1024).decode(FORMAT)
    print("username: --" + user + "--")

    socket.sendall(user.encode(FORMAT))

    pw = socket.recv(1024).decode(FORMAT)
    print("password: --"+pw+"--")

    accepted = check_clientSignup(user)
    print ("accepted: ", accepted)
    socket.sendall(str(accepted).encode(FORMAT))

    if accepted:
        insert_new_client(user, pw)

        AD.append(str(addr))
        ID.append(user)

        account = str(AD[AD.__len__()-1]) + '-' + str(ID[ID.__len__()-1])
        live_Account.append(account)
    
    print ("end-login")
    print("")

def get_all_ID():
    cursor = connect_db()
    cursor.execute("SELECT ID FROM BOOKS")
    results =  []
    for row in cursor:
        parse = str(row)
        parse_check = parse[2:]
        parse = parse_check.find("'")
        parse_check = parse_check[:parse]
        results.append(parse_check)
    return results

def insert_NewBook(socket):
    data = ""
    match = []
    for i in range(4):
        data = socket.recv(1024).decode(FORMAT)
        print(data)
        socket.sendall(data.encode(FORMAT))
        match.append(data)

    res = get_all_ID()
    for row in res:
        if row == match[0]:
            socket.sendall("failed".endcode(FORMAT))
            return FALSE
    
    try:
        cursor = connect_db()
        cursor.execute("INSERT INTO BOOKS (ID, BOOK_NAME, AUTHOR, PUBLICING_YEAR) VALUES (?,?,?,?)", (match[0], match[1], match[2], match[3], match[4]))
        cursor.commit

    except pyodbc.Error:
        socket.sendall("failed".encode(FORMAT))
        return False

    socket.sendall("success".encode(FORMAT))
    return True

def find_1Match(id):
    ids = get_all_ID()
    for row in ids:
        if row == id:
            cursor = connect_db()
            cursor.execute("SELECT *  FROM BOOKS WHERE ID=?", (id))
            match = cursor.fetchone()
            return match
    return False

def getMatchs():
    cursor = connect_db()
    cursor.execute("SELECT * FROM BOOKS")
    results = []

    for row in cursor:
        results.append(row)

    return results

def client_Search(socket):
    id = socket.recv(1024).decode(FORMAT)
    
    match = find_1Match(id)
    if match == False:
        msg = "no id"
        socket.sendall(msg.encode(FORMAT))

    else:
        msg = "find"
        socket.sendall(msg.encode(FORMAT))

    msg = "end"
    socket.sendall(msg.encode(FORMAT))

def clien_Handle(conn, addr):

    option = conn.recev(1024).decode(FORMAT)

    if option == LOGIN:
        AD.append(str(addr))
        login(conn)

    elif option == LOGOUT:
        remove_liveAccount(conn,addr)
    
    elif option == SIGNUP:
        signup(conn, addr)

    elif option == SEARCH:
        client_Search(conn)
    
    remove_liveAccount(conn, addr)
    conn.close
    print("end")



app = Book_Admin()
app.mainloop()
